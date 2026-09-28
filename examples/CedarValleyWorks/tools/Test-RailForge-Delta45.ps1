#Requires -Version 7.4
# Offline policy/scanner checks. No game initializer or Unity object creation is called.
param(
 [Parameter(Mandatory)][string]$RailForgeAssemblyPath,
 [Parameter(Mandatory)][string]$GamePath,
 [Parameter(Mandatory)][string]$ScratchDirectory,
 [switch]$BaselineCatalogOnly
)
$ErrorActionPreference='Stop'
$checks=0
function Check([bool]$Ok,[string]$Name){if(-not $Ok){throw "FAIL: $Name"};$script:checks++}
$managed=Join-Path $GamePath 'Railroader_Data/Managed'
foreach($name in @('Newtonsoft.Json.dll','UnityEngine.CoreModule.dll','UnityEngine.dll')){
 [Reflection.Assembly]::LoadFrom((Join-Path $managed $name))|Out-Null
}
$rf=[Reflection.Assembly]::LoadFrom([IO.Path]::GetFullPath($RailForgeAssemblyPath))
$static=[Reflection.BindingFlags]'Public,NonPublic,Static'
$instance=[Reflection.BindingFlags]'Public,NonPublic,Instance'
function Field($Object,[string]$Name){return ,$Object.GetType().GetField($Name,$instance).GetValue($Object)}
$run=Join-Path ([IO.Path]::GetFullPath($ScratchDirectory)) ('delta45-probe-'+[Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($run)|Out-Null
$scanner=$rf.GetType('RailForge.RailForgeContentScanner',$true)
$indexType=$rf.GetType('RailForge.RailForgeContentIndex',$true)
function NewIndex{return ,[Activator]::CreateInstance($indexType,$true)}
function MakePack([string]$Name,[string]$Catalog,[string]$Bundle='present'){
 $path=Join-Path $run $Name
 [IO.Directory]::CreateDirectory($path)|Out-Null
 [IO.File]::WriteAllText((Join-Path $path 'Catalog.json'),$Catalog,[Text.UTF8Encoding]::new($false))
 # One byte exercises discovery only. This is NOT a usable Unity bundle.
 if($Bundle -eq 'present'){[IO.File]::WriteAllBytes((Join-Path $path 'Bundle'),[byte[]]@(1))}
 if($Bundle -eq 'empty'){[IO.File]::WriteAllBytes((Join-Path $path 'Bundle'),[byte[]]@())}
 return [string]$path
}
$valid='{"identifier":"ExampleAuthor.CVW.Parts","name":"Cedar Valley Parts","shared":false,"assets":{"cvw-tank":{"name":"CVW Tank","type":"GameObject","filename":"cvw-tank.prefab"}}}'
$package=Join-Path $run 'package'
[IO.Directory]::CreateDirectory($package)|Out-Null
[IO.File]::WriteAllText((Join-Path $package 'Info.json'),'{"Id":"ExampleAuthor.CatalogProbe","Version":"1.0.0","DisplayName":"Offline catalog probe"}')
$pack=MakePack 'package/parts' $valid
$record=$scanner.GetMethod('ReadModRecord',$static).Invoke($null,[object[]]@([string]$package))
$index=NewIndex
$discover=$scanner.GetMethod('AddLegacyStandaloneAssetPackRoots',$static)
$owners=[Activator]::CreateInstance($discover.GetParameters()[2].ParameterType)
$discover.Invoke($null,[object[]]@($index,$record,$owners))|Out-Null
$packs=Field $index 'AssetPackDirectories'
if($BaselineCatalogOnly){
 Check ($packs.Count -eq 0) 'DELTA25 does not discover standalone Catalog + Bundle without Definitions'
 Write-Output "PASS: $checks baseline assertion; $($rf.GetName().Version). Fixture: $run"
 exit 0
}
Check ($rf.GetName().Version -eq [version]'0.14.45.0') 'exact audited RF assembly version'
Check ($packs.Count -eq 1 -and [IO.Path]::GetFullPath($packs[0]) -ieq [IO.Path]::GetFullPath($pack)) 'DELTA45 discovers catalog-only immediate child pack'
Check (-not (Test-Path -LiteralPath (Join-Path $pack 'Definitions.json'))) 'discovery fixture has no Definitions'
$validateCatalog=$scanner.GetMethod('IsStandaloneCatalogAssetPack',$static)
function CatalogOK([string]$Path){
 $i=NewIndex
 return [bool]$validateCatalog.Invoke($null,[object[]]@($i,[string]$Path,[string](Join-Path $Path 'Catalog.json')))
}
Check (CatalogOK $pack) 'valid catalog preflight'
foreach($case in @(
 @('missing-bundle',$valid,'missing'),
 @('empty-bundle',$valid,'empty'),
 @('empty-assets','{"identifier":"parts","assets":{}}','present'),
 @('empty-id','{"identifier":"","assets":{"x":{}}}','present'),
 @('bad-shared','{"identifier":"parts","shared":"true","assets":{"x":{}}}','present'),
 @('bad-entry','{"identifier":"parts","assets":{"x":{"filename":42}}}','present'),
 @('duplicate-key','{"identifier":"parts","identifier":"other","assets":{"x":{}}}','present')
)){
 $path=MakePack $case[0] $case[1] $case[2]
 Check (-not (CatalogOK $path)) ("reject catalog "+$case[0])
}
$policy=$rf.GetType('RailForge.RailForgeBunkerFuelPolicy',$true)
$build=$policy.GetMethod('BuildPatch',$static)
function Graph{
 return ,[Newtonsoft.Json.Linq.JObject]::Parse('{"loads":{},"tracks":{"spans":{"cvw-span":{}}},"areas":{"cvw-area":{"industries":{"cvw-interchange":{"components":{"exchange":{"type":"Model.Ops.Interchange","trackSpans":["cvw-span"]},"diesel-supplier":{"type":"Model.Ops.InterchangedIndustryLoader","name":"CVW Supply","loadId":"diesel-fuel","trackSpans":["cvw-span"]}}}}}}}')
}
function Plan([Newtonsoft.Json.Linq.JObject]$Graph,[string[]]$Excluded=@()){
 $argsIn=[object[]]::new(2);$argsIn[0]=$Graph;$argsIn[1]=[string[]]$Excluded
 return ,$build.Invoke($null,$argsIn)
}
function Purchase($Plan){return ,(Field $Plan 'Patch')['areas']['cvw-area']['industries']['cvw-interchange']['components']['bmr-universal-bunker-c']}
$g=Graph;$original=$g.DeepClone();$plan=Plan $g;$patch=Field $plan 'Patch';$load=$patch['loads']['bunker-c']
Check ([Newtonsoft.Json.Linq.JToken]::DeepEquals($g,$original)) 'pure planner leaves input unchanged'
Check ((Field $plan 'AddedLoad') -and (Field $plan 'AddedPurchaseLoaders') -eq 1) 'default load and eligible purchase planned'
Check ($load['units'].Value -ceq 'Gallons' -and $load['density'].Value -eq 65 -and $load['importable'].Value) 'default load definition'
Check ([Math]::Abs([double]$load['costPerUnit'].Value-0.12) -lt 0.000001) 'fallback price'
$purchase=Purchase $plan
Check ($purchase['carTypeFilter'].Value -ceq 'TM' -and $purchase['loadId'].Value -ceq 'bunker-c') 'managed purchase cargo/filter'
Check ($purchase['trackSpans'][0].Value -ceq 'cvw-span') 'managed purchase uses interchange spans'
foreach($price in @('0','null')){
 $g=Graph;$g['loads']['bunker-c']=[Newtonsoft.Json.Linq.JObject]::Parse('{"description":"Authored Oil","units":"Gallons","density":70,"importable":true,"costPerUnit":'+$price+'}')
 $plan=Plan $g;$patch=Field $plan 'Patch'
 Check ((Field $plan 'AppliedFallbackPrice') -and @($patch['loads']['bunker-c'].Properties()).Count -eq 1) ("price-only fallback for "+$price)
 Check ($g['loads']['bunker-c']['density'].Value -eq 70) 'authored density preserved'
}
$g=Graph;$g['loads']['bunker-c']=[Newtonsoft.Json.Linq.JObject]::Parse('{"units":"Gallons","density":70,"importable":true,"costPerUnit":0.25}')
$plan=Plan $g
Check (-not (Field $plan 'AppliedFallbackPrice') -and $null -eq (Field $plan 'Patch')['loads']) 'positive authored price preserved'
foreach($definition in @(
 '{"units":"Pounds","density":65,"importable":true,"costPerUnit":0.25}',
 '{"units":"Gallons","density":0,"importable":true,"costPerUnit":0.25}',
 '{"units":"Gallons","density":65,"importable":false,"costPerUnit":0.25}',
 '{"units":"Gallons","density":65,"importable":true,"costPerUnit":-1}'
)){
 $g=Graph;$g['loads']['bunker-c']=[Newtonsoft.Json.Linq.JObject]::Parse($definition);$plan=Plan $g
 Check (@((Field $plan 'Patch').Properties()).Count -eq 0 -and (Field $plan 'Notices').Count -gt 0) 'invalid authored cargo held without replacement'
}
$g=Graph;$g['loads']['Bunker-C']=[Newtonsoft.Json.Linq.JObject]::new();$plan=Plan $g
Check (@((Field $plan 'Patch').Properties()).Count -eq 0) 'case collision held'
$g=Graph;$plan=Plan $g @('cvw-interchange')
Check ((Field $plan 'AddedLoad') -and (Field $plan 'AddedPurchaseLoaders') -eq 0) 'industry exclusion leaves cargo available'
$g=Graph;$industries=$g['areas']['cvw-area']['industries'];$industries['Oconalufty-RR-INT']=$industries['cvw-interchange'].DeepClone();$industries.Remove('cvw-interchange')|Out-Null;$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0) 'built-in interchange exclusion'
$g=Graph;$g['areas']['cvw-area']['industries']['cvw-interchange']['components'].Remove('diesel-supplier')|Out-Null;$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0) 'bare interchange does not receive automatic purchase destination'
$g=Graph;$components=$g['areas']['cvw-area']['industries']['cvw-interchange']['components'];$components['custom-oil']=[Newtonsoft.Json.Linq.JObject]::Parse('{"type":"Model.Ops.InterchangedIndustryLoader","loadId":"bunker-c","trackSpans":["cvw-span"]}');$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0) 'authored oil supplier prevents duplicate'
$g=Graph;$components=$g['areas']['cvw-area']['industries']['cvw-interchange']['components'];$components['other-exchange']=$components['exchange'].DeepClone();$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0 -and (Field $plan 'Notices').Count -gt 0) 'multiple interchange components held'
$g=Graph;$components=$g['areas']['cvw-area']['industries']['cvw-interchange']['components'];$components['bmr-universal-bunker-c']=[Newtonsoft.Json.Linq.JObject]::Parse('{"type":"Model.Ops.IndustryUnloader","loadId":"diesel-fuel"}');$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0) 'reserved managed-ID collision preserved'
$g=Graph;$components=$g['areas']['cvw-area']['industries']['cvw-interchange']['components'];$components['bmr-universal-bunker-c']=[Newtonsoft.Json.Linq.JObject]::Parse('{"type":"Model.Ops.InterchangedIndustryLoader","loadId":"bunker-c","name":"Old label","trackSpans":[],"progressionDisabled":true,"disabled":true}');$plan=Plan $g;$p=Purchase $plan
Check ((Field $plan 'UpdatedPurchaseLoaders') -eq 1 -and $p['progressionDisabled'].Value -and $p['disabled'].Value) 'planner preserves existing disable flags'
$g=Graph;$g['tracks']['spans'].Remove('cvw-span')|Out-Null;$plan=Plan $g
Check ((Field $plan 'AddedPurchaseLoaders') -eq 0) 'unresolved interchange span held'
$plan=Plan ([Newtonsoft.Json.Linq.JObject]::new())
Check (@((Field $plan 'Patch').Properties()).Count -eq 0) 'missing load table held'
# Exercise the actual core and the new explicit freight recipe through the pure policy.
$example=Split-Path $PSScriptRoot -Parent
$coreFile=Join-Path $example 'package/ExampleAuthor.CedarValleyWorks/RailForge/game-graph/cedar-valley.json'
$core=[Newtonsoft.Json.Linq.JObject]::Parse([IO.File]::ReadAllText($coreFile))
$corePlan=Plan $core
Check ((Field $corePlan 'AddedLoad') -and (Field $corePlan 'AddedPurchaseLoaders') -eq 0) 'Cedar Valley bare interchange does not gain automatic oil purchasing'
$recipeFile=Join-Path $example 'recipes/16-bunker-c-freight.recipe.json'
$recipe=[Newtonsoft.Json.Linq.JObject]::Parse([IO.File]::ReadAllText($recipeFile))
$ctor=$rf.GetType('RailForge.Patcher',$true).GetConstructor(@([Newtonsoft.Json.Linq.JObject]))
$argsIn=[object[]]::new(1);$argsIn[0]=$core
$patcher=$ctor.Invoke($argsIn)
$merged=$patcher.ApplyPatch('CedarValley-bunker-recipe',[Newtonsoft.Json.Linq.JObject]$recipe['railforgeFragment'])
$recipePlan=Plan $merged
Check ((Field $recipePlan 'AddedPurchaseLoaders') -eq 0 -and -not (Field $recipePlan 'AppliedFallbackPrice')) 'explicit Cedar Valley oil supplier and positive price are preserved'

Write-Output "PASS: $checks DELTA45 policy/discovery assertions. RF $($rf.GetName().Version)."
Write-Output "SHA256 $((Get-FileHash -LiteralPath $RailForgeAssemblyPath).Hash)"
Write-Output "Scratch fixtures retained at $run. Stub bundles were not loaded. No live refueling, steam or Unity materialization tested."
