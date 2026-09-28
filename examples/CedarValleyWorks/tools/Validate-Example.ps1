#Requires -Version 7.4
param([string]$FuseSchema,[string]$GamePath,[string]$RailForgeAssemblyPath)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$package=Join-Path $root 'package/ExampleAuthor.CedarValleyWorks'
$checks=0
function Check([bool]$Condition,[string]$Name){if(-not $Condition){throw "FAIL: $Name"};$script:checks++}
if($FuseSchema){
 $schema=Get-Content -LiteralPath $FuseSchema -Raw|ConvertFrom-Json -AsHashtable
 Check (Test-Json -LiteralPath (Join-Path $package 'game-graph.fuse.json') -SchemaFile $FuseSchema -ErrorAction Stop) 'core schema'
 foreach($file in Get-ChildItem -LiteralPath (Join-Path $root 'recipes') -Filter '*.recipe.json'){
  $recipe=Get-Content -LiteralPath $file.FullName -Raw|ConvertFrom-Json -AsHashtable
  if($recipe.ContainsKey('conditionalExample')){
   Check (Test-Json -Json ($recipe.conditionalExample.fuseFile.payload|ConvertTo-Json -Depth 80) -SchemaFile $FuseSchema -ErrorAction Stop) 'conditional FUSE payload schema'
  }
  if($recipe.ContainsKey('fuseFragment')){
   $doc=@{schemaVersion='1.0';id='ExampleAuthor.CVW.Recipe';name=$recipe.title;author='Example Author'}
   foreach($key in $recipe.fuseFragment.Keys){$doc[$key]=$recipe.fuseFragment[$key]}
   $isAudioException=$recipe.ContainsKey('schemaStatus') -and $recipe.schemaStatus -ceq 'known-audio-path-mismatch'
   if($isAudioException){
    Check (-not (Test-Json -Json ($doc|ConvertTo-Json -Depth 80) -SchemaFile $FuseSchema -ErrorAction SilentlyContinue)) 'documented audio schema mismatch'
    # Test the same structure in schema-only URI form; runtime recipe retains the working relative paths.
    foreach($catalog in $doc.audio.Values){
     foreach($entry in $catalog.Values){
      foreach($key in @('file','clip')){if($entry.ContainsKey($key)){$entry[$key]='file://'+$entry[$key]}}
      foreach($layer in $entry.layers){$layer.file='file://'+$layer.file}
     }
    }
   }
   Check (Test-Json -Json ($doc|ConvertTo-Json -Depth 80) -SchemaFile $FuseSchema -ErrorAction Stop) ("recipe "+$file.Name)
  }
 }
 $atlas=Get-Content -LiteralPath (Join-Path $root 'reference/fuse-field-examples.json') -Raw|ConvertFrom-Json -AsHashtable
 Check ((Get-FileHash -LiteralPath $FuseSchema).Hash -ieq $atlas.sha256) 'atlas source hash'
 foreach($entry in $atlas.entries){
  $node=$schema
  foreach($bit in $entry.pointer.TrimStart('/').Split('/')){
   $bit=$bit.Replace('~1','/').Replace('~0','~')
   if($node -is [System.Collections.IList]){$node=$node[[int]$bit]}else{$node=$node[$bit]}
  }
  $sub=@{'$schema'=$schema.'$schema';'$defs'=$schema.'$defs';allOf=@($node)}|ConvertTo-Json -Depth 100 -Compress
  $value=ConvertTo-Json -InputObject $entry.example -Depth 80 -Compress
  Check (Test-Json -Json $value -Schema $sub -ErrorAction SilentlyContinue) ("atlas "+$entry.field)
 }
 Write-Output "PASS: core, recipe fragments, conditional payload, audio schema-only alternate and $($atlas.entries.Count) field values; runtime audio path exception confirmed."
}
if($GamePath){
 $managed=Join-Path $GamePath 'Railroader_Data/Managed'
 foreach($name in @('Newtonsoft.Json.dll','UnityEngine.CoreModule.dll','UnityEngine.dll')){[Reflection.Assembly]::LoadFrom((Join-Path $managed $name))|Out-Null}
 $flags=[Reflection.BindingFlags]'Public,NonPublic,Static'
 $rfPath=if($RailForgeAssemblyPath){[IO.Path]::GetFullPath($RailForgeAssemblyPath)}else{Join-Path $GamePath 'Mods-Railforge/RTM.RailForge/RailForge.dll'};$fusePath=Join-Path $GamePath 'Mods/FUSE/FUSE.dll'
 $rf=[Reflection.Assembly]::LoadFrom($rfPath);$scanner=$rf.GetType('RailForge.RailForgeContentScanner',$true)
 $record=$scanner.GetMethod('ReadModRecord',$flags).Invoke($null,[object[]]@([string]$package))
 Check ($record.Id -ceq 'ExampleAuthor.CedarValleyWorks' -and $record.ManifestAllowed -and -not $record.PrimaryManifestInvalid) 'RF manifest'
 Check ($record.ManifestWarnings.Count -eq 0 -and $record.PrimaryManifestIssues.Count -eq 0) 'RF manifest diagnostics'
 $indexType=$rf.GetType('RailForge.RailForgeContentIndex',$true);$index=[Activator]::CreateInstance($indexType,$true)
 $scanner.GetMethod('AddContentRoot',$flags).Invoke($null,[object[]]@($index,[string]$package,'ExampleAuthor.CedarValleyWorks','RailForge'))|Out-Null
 $mixintos=@($indexType.GetField('Mixintos',[Reflection.BindingFlags]'Public,NonPublic,Instance').GetValue($index))
 $nativePath=Join-Path $package 'RailForge/game-graph/cedar-valley.json'
 Check ($mixintos.Count -eq 1 -and [IO.Path]::GetFullPath($mixintos[0].Mixinto) -ieq [IO.Path]::GetFullPath($nativePath)) 'RF exact graph discovery'
 $patcherType=$rf.GetType('RailForge.Patcher',$true);$ctor=$patcherType.GetConstructor(@([Newtonsoft.Json.Linq.JObject]))
 function Patch([Newtonsoft.Json.Linq.JObject]$Base,[Newtonsoft.Json.Linq.JObject]$Delta){
  $argsArray=[object[]]::new(1);$argsArray[0]=$Base;$patcher=$ctor.Invoke($argsArray)
  return ,$patcher.ApplyPatch('CedarValleyWorks-probe',$Delta)
 }
 $graph=[Newtonsoft.Json.Linq.JObject]::Parse([IO.File]::ReadAllText($nativePath))
 $base=[Newtonsoft.Json.Linq.JObject]::Parse('{"progressions":{"ewh":{"sections":{"base-section":{"displayName":"Keep Me"}},"enableFeaturesAtStart":["wh-el","ewh-intch"]}}}')
 $merged=Patch $base $graph
 Check ($merged['progressions']['ewh']['sections']['base-section']['displayName'].Value -ceq 'Keep Me') 'preserve base section'
 Check ($merged['progressions']['ewh']['enableFeaturesAtStart'].Count -eq 2) 'preserve base grants'
 foreach($key in @('tracks','areas','loads','scenery','loaders','mapLabels','mapFeatures')){Check ([Newtonsoft.Json.Linq.JToken]::DeepEquals($merged[$key],$graph[$key])) ("RF namespace "+$key)}
 $fixtures=Get-Content -LiteralPath (Join-Path $root 'fixtures/rf-patch-cases.json') -Raw|ConvertFrom-Json -AsHashtable
 foreach($case in $fixtures.cases){
  $base=[Newtonsoft.Json.Linq.JObject]::Parse(($fixtures.base|ConvertTo-Json -Depth 40))
  $delta=[Newtonsoft.Json.Linq.JObject]::Parse(($case.patch|ConvertTo-Json -Depth 40))
  $expected=[Newtonsoft.Json.Linq.JObject]::Parse(($case.expected|ConvertTo-Json -Depth 40))
  $actual=Patch $base $delta
  Check ([Newtonsoft.Json.Linq.JToken]::DeepEquals($actual,$expected)) ("RF operator "+$case.name)
 }
 $fuse=[Reflection.Assembly]::LoadFrom($fusePath);$loader=$fuse.GetType('FUSE.Loading.FuseModLoader',$true)
 $paths=@($loader.GetMethod('ResolveDefinitionPaths',$flags).Invoke($null,[object[]]@([string]$package)));$fuseFile=Join-Path $package 'game-graph.fuse.json'
 Check ($paths.Count -eq 1 -and [IO.Path]::GetFullPath($paths[0]) -ieq [IO.Path]::GetFullPath($fuseFile)) 'FUSE exact discovery'
 $serializer=$fuse.GetType('FUSE.Authoring.Serialization.FuseSerializer',$true)
 $parsed=$serializer.GetMethod('FromJson',$flags).Invoke($null,[object[]]@([IO.File]::ReadAllText($fuseFile)))
 Check ($parsed.Tracks.Nodes.Count -eq 19 -and $parsed.Tracks.Segments.Count -eq 19 -and $parsed.Tracks.Spans.Count -eq 6) 'FUSE typed tracks'
 Check ($parsed.Operations.Loads.Count -eq 2 -and $parsed.Operations.Industries.Count -eq 4 -and $parsed.Operations.Loaders.Count -eq 3) 'FUSE typed operations'
 Check ($parsed.World.Scenery.Count -eq 2 -and $parsed.World.MapLabels.Count -eq 1) 'FUSE typed world'
 $audioType=$fuse.GetType('FUSE.Runtime.API.FuseAudioAPI',$true)
 $resolver=$audioType.GetMethod('ResolveAudioPath',$flags)
 $expectedAudio=Join-Path $package 'Audio/cvw-bell.wav'
 $relativeAudio=$resolver.Invoke($null,[object[]]@([string]$package,'Audio/cvw-bell.wav'))
 $wrappedAudio=$resolver.Invoke($null,[object[]]@([string]$package,'file(Audio/cvw-bell.wav)'))
 $uriAudio=$resolver.Invoke($null,[object[]]@([string]$package,'file://Audio/cvw-bell.wav'))
 Check ($relativeAudio -ieq $expectedAudio -and $wrappedAudio -ieq $expectedAudio) 'FUSE relative audio paths resolve'
 Check ($uriAudio -ine $expectedAudio) 'recorded FUSE file URI discrepancy still reproduces'
 Write-Output 'CONFIRMED: FUSE relative/file(...) audio paths resolve; file:// does not resolve to the intended package file in this build.'

 Write-Output "PASS: installed-runtime discovery, deserialization, graph patching and $($fixtures.cases.Count) operator fixtures."
 Write-Output "RF $($rf.GetName().Version) SHA256 $((Get-FileHash -LiteralPath $rfPath).Hash)"
 Write-Output "FUSE $($fuse.GetName().Version) SHA256 $((Get-FileHash -LiteralPath $fusePath).Hash)"
}
if(-not $FuseSchema -and -not $GamePath){throw 'Supply -FuseSchema and/or -GamePath; run validate-example.py for static checks.'}
Write-Output "PASS: $checks assertions. No Unity materialization or live gameplay was exercised."
