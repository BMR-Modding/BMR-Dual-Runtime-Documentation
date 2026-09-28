import sys
sys.dont_write_bytecode = True
from pathlib import Path
import importlib.util, copy, json
spec=importlib.util.spec_from_file_location("example",Path(__file__).with_name("build-example.py"))
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
v=b.vec
def recipe(name,title,status,prerequisites,fuse=None,railforge=None,notes=()):
    d=dict(title=title,status=status,prerequisites=prerequisites,notes=list(notes))
    if fuse is not None:d["fuseFragment"]=fuse
    if name=="13-audio":d["schemaStatus"]="known-audio-path-mismatch"
    if railforge is not None:d["railforgeFragment"]=railforge
    if name=="10-settings-and-conditional-content":
        optional=b.header("optional","Optional Cedar Valley Warehouse")
        optional["mixinto"]={"target":"game-graph","requires":[{"id":"ExampleAuthor.OptionalAssets","notBefore":"1.0.0"}],
                             "conflictsWith":[{"id":"ExampleAuthor.ConflictingLayout"}]}
        optional["world"]={"scenery":{"cvw-optional-warehouse":{"assetIdentifier":"scenery://freight-house-general","position":v(900,500,1050)}}}
        d["conditionalExample"]={
          "note":"Alternative to the setting-driven fragment above. Provider IDs are fictional conditions to replace, not bundled mods.",
          "infoFragment":{"FuseDataFiles":["game-graph.fuse.json","optional.fuse.json"]},
          "definitionFragment":{"mixintos":{"game-graph":[{"mixinto":"file(RailForge/conditional/optional.json)",
             "requires":[{"id":"ExampleAuthor.OptionalAssets","notBefore":"1.0.0"}],
             "conflictsWith":[{"id":"ExampleAuthor.ConflictingLayout"}]}]}},
          "fuseFile":{"path":"optional.fuse.json","payload":optional},
          "railforgeFile":{"path":"RailForge/conditional/optional.json","payload":{"scenery":{"cvw-optional-warehouse":{
             "modelIdentifier":"freight-house-general","position":v(900,500,1050)}}}}}
    b.write("recipes/"+name+".recipe.json",b.place_recipe(d))
def industry(components):
    return dict(operations=dict(industries={"cvw-works":dict(name="Cedar Valley Crate Works",areaId="cvw-area",position=v(-30,0,20),components=components)}))
def rf_ind(components):
    return dict(areas={"cvw-area":dict(industries={"cvw-works":dict(components=components)})})
recipe("01-partial-and-replace","Patch a component; append versus replace spans","paired",
 ["Apply after the core graph; these are alternatives, not all steps of one upgrade."],
 industry({"receive":dict(partial=True,maxStorage=160000,trackSpanPatch=dict(append=["cvw-p-team"]))}),
 rf_ind({"receive":dict(maxStorage=160000,trackSpans=[{"$append":["cvw-p-team"]}])}),
 ["FUSE partial trackSpanIds appends distinct IDs; [] there does not clear. Use trackSpanPatch.replace: [] to clear.",
  "RF ordinary trackSpans arrays replace. The RF append shown here is not a uniqueness guarantee.",
  "For whole component replacement, FUSE replaceComponents: true corresponds to RF components: {\"$replace\": {complete component dictionary}}.",
  "FUSE segment preservation flags become omission of supported RF fields. Do not emit zero/default values when preserving."])
recipe("02-track-locations","Normalized positions, distance, partial segments and metadata","partial",
 ["The 15 m conversion below assumes a straight 120-metre segment; measure the edited cvw-s-factory curve before applying it."],
 {"tracks":{"spans":{"cvw-p-factory":{"upper":{"segmentId":"cvw-s-factory","end":"A","normalized":0.125},
 "lower":{"segmentId":"cvw-s-factory","end":"B","normalized":0.125},"normalize":True}},
 "segments":{"cvw-s-factory":{"startNodeId":"cvw-n-f0","endNodeId":"cvw-n-f1","partial":True,
 "preserveStyle":True,"preserveTrackClass":True,"preserveSpeedLimit":True,"preservePriority":True,"preserveGroupId":True}}}},
 {"tracks":{"spans":{"cvw-p-factory":{"upper":{"segmentId":"cvw-s-factory","end":"A","distance":15},
 "lower":{"segmentId":"cvw-s-factory","end":"B","distance":15},"normalize":True}}}},
 ["Do not use this 120-metre calculation for arbitrary curved segments. Obtain the actual segment length.",
  "FUSE trackLocation chooses normalized OR distance, never both. RF end A/B and distance are canonical.",
  "FUSE location offset, node isDiamond/tags and segment gauge/tags/yard/bridgeSupportsSteel lack general RF field parity.",
  "FUSE span groupId and area spanIds/groupId likewise require a deliberate target design."])
passenger=b.comp("passengerStop","Cedar Valley Passenger Stop","cvw-p-team",passengerStopId="cvw-passenger-stop",timetableCode="CVW",
 basePopulation=250,neighborIds=["REPLACE-WITH-EXISTING-STOP-ID"],branch="REPLACE-WITH-EXISTING-BRANCH",
 branchDefinitions=[dict(branch="REPLACE-WITH-EXISTING-BRANCH",traverseTimeToNext=10)])
station=dict(position=v(935,500,1060),rotation=v(),prefab="vanilla://flagStopStation",passengerStopId="cvw-passenger-stop")
f=industry({"passengers":passenger});f["operations"]["stations"]={"cvw-station":station}
r=rf_ind({"passengers":b.rfcomp(passenger)})
rs=copy.deepcopy(station);rs["passengerStop"]=rs.pop("passengerStopId");rs["handler"]="AlinasMapMod.Stations.StationAgentBuilder";r["splineys"]={"cvw-station":rs}
recipe("03-passengers-and-station","Passenger component plus physical station","requires-topology",["Replace neighbor and branch IDs with an authored timetable network; choose final area order."],f,r,
 ["A station prefab alone does not create passenger service. The prefab must contain exactly one StationAgent.",
  "This alternative shares the team-track span only for teaching. Build a suitable passenger siding for actual service.",
  "RF branch intermediates are not established as fully supported. Main occurrence plus at most one junction duplicate is the inspected boundary."])
tt=dict(position=v(975,500,1210),rotation=v(),radius=15,subdivisions=16,roundhouse=dict(stalls=3,trackLength=46,startPrefab="vanilla://roundhouseStart",endPrefab="vanilla://roundhouseEnd",stallPrefab="vanilla://roundhouseStall"))
rt=dict(handler="AlinasMapMod.Turntable.TurntableBuilder",position=tt["position"],rotation=tt["rotation"],radius=15,subdivisions=16,roundhouseStalls=3,roundhouseTrackLength=46,startPrefab=tt["roundhouse"]["startPrefab"],endPrefab=tt["roundhouse"]["endPrefab"],stallPrefab=tt["roundhouse"]["stallPrefab"])
recipe("04-turntable","Turntable and roundhouse","paired-builder",["Inspect generated helper-node IDs and connect the approach after building; this recipe supplies no fabricated attachment IDs."],
 {"operations":{"turntables":{"cvw-turntable":tt}}},{"splineys":{"cvw-turntable":rt}},
 ["No roundhouse: omit FUSE roundhouse; still emit RF roundhouseStalls: 0 and a valid roundhouseTrackLength.",
  "Portable subset: radius 5-50, even subdivisions 4-32. Legacy IDs, custom visuals, controller, startAngle and stallAngle need separate implementation."])
special={
 "remote-load":b.comp("interchangedLoader","Remote Crate Shipper","cvw-p-team",loadId="cvw.finished-crates",carTypeFilter="XM*",carLoadPeriod=1,carLengthFeet=50),
 "transfer":b.comp("teleportLoading","Captive Transfer","cvw-p-team",loadId="cvw.finished-crates",inputSpanIds=["cvw-p-team"],outputSpanIds=["cvw-p-factory"],carTransferRate=60000),
 "convert-in":b.comp("ConfusingSupplements.IndustryComponents.CaptiveConversionUnloader","Captive Receiving","cvw-p-team",loadId="cvw.unfinished-crates",convertedLoadId="cvw.finished-crates",carTransferRate=60000,maxStorage=120000,title="Crate Conversion"),
 "convert-out":b.comp("ConfusingSupplements.IndustryComponents.CaptiveConversionLoader","Captive Shipping","cvw-p-factory",loadId="cvw.unfinished-crates",convertedLoadId="cvw.finished-crates",carTransferRate=60000,title="Crate Conversion"),
 "paid":b.comp("ConfusingSupplements.IndustryComponents.Pay4Resource","Paid Crates","cvw-p-team",loadId="cvw.finished-crates",carTransferRate=60000,notBeforeHour=6,notAfterHour=20,costPerUnit=0.02,fillPercentage=1,bookReasons=["Cedar Valley supply"],title="Buy Crates"),
 "empty":b.comp("ConfusingSupplements.IndustryComponents.Empty","Reserved Component")}
rs={k:b.rfcomp(c) for k,c in special.items()}
rs["paid"]["hours"]=[rs["paid"].pop("notBeforeHour"),rs["paid"].pop("notAfterHour")]
recipe("05-special-components","Alternative industry component families","provider-or-runtime-specific",
 ["Choose one intended operating design; do not attach every alternative to the same track.","Resolve the Confusing Supplements types in FUSE; RF embeds compatibility implementations in the inspected build."],
 industry(special),rf_ind(rs),
 ["Captive conversion loads must resolve and have equal units; transfer rates and unloader capacity must be positive.",
  "TeleportLoading needs input/output spans AND explicit RF base trackSpans.",
  "interchangedUnloader and arbitrary custom fields require a real loaded provider with a verified contract; no fictional class is claimed to work.",
  "LoadExporter, LoadImporter and SimplePassengerStop are known RF types without a complete verified public authoring contract here."])
common=dict(falloff=2,enableSetHeight=False,enableCutTrees=True,enableMaskModifier=True,maskName="Object",order=0)
masks={"cvw-mask-circle":dict(type="circle",center=v(950,500,1040),radius=15,**common),
 "cvw-mask-rectangle":dict(type="rectangle",center=v(950,500,1040),size=v(20,1,40),rotation=v(),**common),
 "cvw-mask-curve":dict(type="curve",points=[v(940,500,1000),v(940,500,1100)],width=6,**common)}
rm={}
for k,m in masks.items():
    if m["type"]=="curve":continue
    mm=copy.deepcopy(m);mm["position"]=mm.pop("center");mm["handler"]="AlinasMapMod.Map.MapMaskBuilder";rm[k]=mm
recipe("06-masks-and-labels","Terrain masks and richer labels","partial",["Choose one mask shape for a given purpose; terrain changes require visual verification."],
 {"world":{"mapMasks":masks,"mapLabels":{"cvw-speed-label":dict(text="5 MPH",position=v(940,500,1000),style="speedLimit",speedLimitMph=5,rotation=v(),size=1,color="#FFFFFFFF")}}},
 {"splineys":rm,"mapLabels":{"cvw-speed-label":dict(text="5 MPH",position=v(940,500,1000))}},
 ["RF curve masks use positionA/rotationA/sizeA and positionB/rotationB/sizeB. Fit the intended shape; arbitrary multi-point curves cannot be copied directly.",
  "FUSE speed style, size and color are not claimed as native RF label fields. A map label does not set track speed; segment speedLimit does."])
points=[dict(position=v(900,500,1000),rotation=v(),width=5),dict(position=v(900,500,1120),rotation=v(),width=5)]
recipe("07-splineys-and-water","Road, river, trestle, object line and water polygon","partial",["Replace profile/material/prefab names from a verified loaded catalog; fit the terrain."],
 {"world":{"splineys":{
 "cvw-road":dict(type="road",profile="REPLACE-WITH-LOADED-ROAD-PROFILE",style="Road",offsetY=-0.1,points=points),
 "cvw-river":dict(type="river",profile="REPLACE-WITH-LOADED-RIVER-PROFILE",offsetY=-0.1,points=points),
 "cvw-trestle":dict(type="trestle",headStyle="REPLACE-WITH-VERIFIED-STYLE",tailStyle="REPLACE-WITH-VERIFIED-STYLE",points=points),
 "cvw-object-line":dict(type="objectLine",assetIdentifier="scenery://freight-house-general",spacing=25,instanceScale=v(1,1,1),rotationOffset=v(),lateralOffset=0,verticalOffset=0,snapToTerrain=True,alignToSlope=False,placeAtEnd=True,maximumInstances=32,points=points)},
 "waterSurfaces":{"cvw-pond":dict(points=[v(850,499,1000),v(875,499,1000),v(875,499,1030),v(850,499,1030)],lockHeight=True,snapToTerrain=False,enableCollider=True,uvScale=1,triangleDensity=0.2,maximumTriangleArea=50,yOffset=0)}}},
 {"splineys":{"cvw-road":dict(handler="RailForge.FlowyThingBuilder",profile="REPLACE-WITH-LOADED-ROAD-PROFILE",style="Road",offsetY=-0.1,points=points),
 "cvw-river":dict(handler="RailForge.FlowyThingBuilder",profile="REPLACE-WITH-LOADED-RIVER-PROFILE",style="River",offsetY=-0.1,points=points),
 "cvw-trestle":dict(handler="AutoTrestle",headStyle="REPLACE-WITH-VERIFIED-STYLE",tailStyle="REPLACE-WITH-VERIFIED-STYLE",points=points)}},
 ["FUSE terrainRoad/waterfall/fence/retainingWall and object-line alias are covered in the field atlas. A loaded handler's own contract determines RF support.",
  "The object-line house is an obvious teaching asset, not a useful fence. Replace it with a suitable catalog model; use exactly one of assetIdentifier or prefab.",
  "FUSE waterSurfaces has no verified RF native pair. RF terrain brushes are not an equivalent lake generator.",
  "Handlerless RF points only replace one unambiguous existing AutoTrestle or RiverPath; they do not create any arbitrary spline."])
recipe("08-scene-clones-and-suppression","Clone, transform or hide a known scene object","requires-scene-path",
 ["Replace both scene paths after inspecting the loaded hierarchy."],
 {"world":{"sceneClones":{"cvw-clone":{"targetPath":"World/CedarValley/ClonedProp","source":"path://World/REPLACE-SOURCE","enabled":True,"localPosition":v(1,0,0),"localRotation":v(),"localScale":v(1,1,1)}},"suppressBaseScenePaths":["World/REPLACE-HIDE-TARGET"]}},
 {"mandelas":{"World/CedarValley/ClonedProp":{"instantiateFrom":"path://World/REPLACE-SOURCE","enabled":True,"localPosition":v(1,0,0),"localRotation":v(),"localScale":v(1,1,1)},"World/REPLACE-HIDE-TARGET":{"enabled":False}}},
 ["These transforms are local to the chosen parent, not necessarily world coordinates.",
  "RF mandela null is hide-only, not destruction. FUSE group/area suppression is visibility intent, not RF deletion."])
recipe("09-removals","Remove old graph records during a controlled upgrade","paired-subset",
 ["The cvw-old-* records must exist in a prior version; remove or rewrite every dependent reference first."],
 {"tracks":{"removals":{"spans":["cvw-old-span"],"segments":["cvw-old-segment"],"nodes":["cvw-old-node"]}},
 "operations":{"removals":{"industries":["cvw-old-industry"]}},
 "world":{"removals":{"scenery":["cvw-old-prop"],"splineys":["cvw-old-road"]}}},
 {"tracks":{"spans":{"cvw-old-span":None},"segments":{"cvw-old-segment":None},"nodes":{"cvw-old-node":None}},
 "areas":{"cvw-area":{"industries":{"cvw-old-industry":None}}},"scenery":{"cvw-old-prop":None},"splineys":{"cvw-old-road":None}},
 ["A component uses FUSE {\"remove\":true} or RF components.<id>: null within its known industry/area.",
  "RF null is supported only in specific keyed materialized collections. Do not generalize to loads, features, progressions, root or scalar fields.",
  "FUSE removals also enumerate waterSurfaces, telegraphPoles, mapLabels and sceneClones; translation depends on their owner/handler."])
recipe("10-settings-and-conditional-content","FUSE settings, feature rules and optional provider fragments","partial",
 ["Settings/rules belong in the SAME FUSE document as the objects they filter. Optional requirements must match real package IDs."],
 {"settings":{"showWarehouse":{"type":"bool","label":"Show warehouse","scope":"user","default":True,"reloadRequired":True}},
 "featureRules":{"warehouse-rule":{"setting":"showWarehouse","operator":"equals","value":True,"targets":{"scenery":["cvw-optional-warehouse"]}}},
 "world":{"scenery":{"cvw-optional-warehouse":{"assetIdentifier":"scenery://freight-house-general","position":v(900,500,1050)}}}},
 None,
 ["There is no verified native RF graph settings/featureRules equivalent; use an adapter or explicit package variant.",
  "For conditional fragments, add top-level mixinto {target:\"game-graph\", requires:[{id:\"ExampleAuthor.OptionalAssets\",notBefore:\"1.0.0\"}]} and list the file in FuseDataFiles.",
  "RF Definition.json mixintos.game-graph can contain {mixinto:\"file(RailForge/conditional/optional.json)\",requires:[{id:\"ExampleAuthor.OptionalAssets\",notBefore:\"1.0.0\"}]}. Keep that payload outside RailForge/game-graph.",
  "Fragment-scoped conflictsWith skip that fragment. Package-wide requirements have different effects. Never require both runtimes."])
recipe("11-company-start-grant","Preserve base Company start features while adding one","paired-patch",
 ["Define cvw-feature-base before using this recipe; the core intentionally has no such feature."],
 {"progression":{"progressions":{"ewh":{"enableFeaturesAtStart":{"cvw-feature-base":True}}}}},
 {"progressions":{"ewh":{"enableFeaturesAtStart":[{"$find":"cvw-feature-base","$optional":True,"$remove":True},{"$append":["cvw-feature-base"]}]}}},
 ["FUSE boolean dictionary merges by ID; plain array replaces. RF recipe removes an existing occurrence then appends one.",
  "A start-granted feature is reapplied on Company load. Do not also use it in section enable/disable/available arrays.",
  "initiallyEnabled/defaultEnableInSandbox apply to Sandbox; they do not grant a Company start.",
  "Section-level FUSE fan-out must become an explicit RF map feature plus section reference. baseProgression must be flattened deliberately."])
recipe("12-telegraph-poles","Pole line, individual pole, and indexed movement","manual-expansion",
 ["Replace pole indices 10001/10002 with inspected existing IDs; they are teaching placeholders, not allocated IDs."],
 {"world":{"telegraphPoles":{"cvw-pole-line":{"spacing":30,"points":[v(1010,500,900),v(1010,500,1080)]}},
 "telegraphPoleMovements":[{"poleIndices":[10001,10002],"offset":v(0,2,0)}]}},
 {"splineys":{"cvw-pole-01":dict(handler="RailForge.MapEditor.TelegraphPoles.TelegraphPoleBuilder",position=v(1010,500,900),rotation=v(),scale=v(1,1,1),variant="Standard Wood Pole",height=5.5,crossarmWidth=1.8,wireCount=4,poleRadius=0.09),
 "cvw-pole-move":{"handler":"RailForge.MapEditor.TelegraphPoleEdits","schemaVersion":4,"createOnly":False,"polesToMove":[10001,10002],"poleMovement":[v(0,2,0),v(0,2,0)]}}},
 ["One RF pole is only an illustration, not a complete translation of the FUSE line. Expand positions, wire connections and identity explicitly.",
  "Pole edit parallel arrays require exact matching lengths. Created IDs must be positive unique and unused; v2 requires tags, v3 scales, v4 permits deletions."])
audio={"whistles":{"cvw-whistle":{"name":"Cedar Valley Whistle","clip":"Audio/cvw-whistle.wav","rampUpPitch":0.1,"lerpSpeed":1,"airLerpSpeed":1}},
 "horns":{"cvw-horn":{"name":"Cedar Valley Horn","layers":[{"file":"Audio/cvw-horn.wav","keyframes":[{"t":0,"value":0},{"t":0.2,"value":1},{"t":1,"value":0}]}]}},
 "bells":{"cvw-bell":{"name":"Cedar Valley Bell","file":"Audio/cvw-bell.wav","indexTimes":[0.2,0.7]}}}
recipe("13-audio","Whistle, horn and bell catalogs","requires-assets-schema-exception",
 ["Supply your own licensed audio files; none are shipped. This recipe uses working package-relative paths; the public URI-only schema rejects them."],
 {"audio":audio},None,
 ["FUSE schema requires URI-shaped strings, but installed FUSE SHA256 9A30D165... resolves file://Audio incorrectly. Relative Audio/... and file(Audio/...) resolve correctly; tested 2026-09-21 without loading audio.",
  "RF uses three catalog ARRAY files declared under manifest mixintos.whistles/horns/bells; these are not graph roots.",
  "RF horn keys rename t to time; FUSE whistle pitch/lerp fields lack RF catalog equivalents.",
  "Use package-relative Audio/cvw-*.wav paths in RF catalogs. Horns allow one or two layers; ordered keyframe times/values are fractions; bell index times are positive and increasing."])
rf_audio={}
for kind,entries in audio.items():
    arr=[]
    for e in entries.values():
        e=copy.deepcopy(e)
        for key in ("rampUpPitch","lerpSpeed","airLerpSpeed"):e.pop(key,None)
        for key in ("file","clip"):
            if key in e:e[key]=e[key].removeprefix("file://")
        for layer in e.get("layers",[]):
            layer["file"]=layer["file"].removeprefix("file://")
            for frame in layer["keyframes"]:frame["time"]=frame.pop("t")
        arr.append(e)
    rf_audio[kind]=arr
b.write("recipes/audio-catalogs.reference.json",dict(explanation="Values are separate root-array files, not a single RF graph.",catalogs=rf_audio,
 manifestFragment=dict(mixintos={kind:["file(Audio/"+kind+".json)"] for kind in rf_audio})))
recipe("14-maps-tiles-and-spawns","Selectable map, tiles and global spawn points","partial-package-layout",
 ["Create real map metadata/tiles before using map or mapTiles; declaring map can suppress the base world."],
 {"map":dict(displayName="Cedar Valley Test Map",description="Isolated authoring map",mapFolder="Maps/CedarValley",suppressBaseWorld=True),
 "world":{"mapTiles":{"cvw-tiles":dict(directory="CedarValley",sourceFolder="Maps/CedarValley",priority=10)},
 "spawnPoints":[dict(name="Cedar Valley",position=v(950,500,1000),rotation=v(),radius=3,priority=1)]}},
 None,
 ["RF has no matching selectable-map graph root. Its tile candidate is Maps/<active-map-directory>/tile_<x>_<y>.data, with exact required PNG encoding; a renamed arbitrary image is not sufficient.",
  "RF root spawn-points.json is "+json.dumps({"title":"Cedar Valley","spawnPoints":[{"name":"Cedar Valley","position":b.world_position(v(950,500,1000))}]})+". Package discovery must be anchored by an editable game-graph file mixinto.",
  "RF global points fix radius 3 and priority Int32.MinValue; FUSE rotation/priority are not portable. Company playerSpawn is a separate format."])
recipe("15-migrations","Rename saved destination/property identifiers","runtime-compatibility-subset",
 ["Map real old save identifiers to verified new ones, then test an old save copy."],
 {"extensions":{"gameMigrations":{"waybillDestinations":{"cvw-old-works.receive":"cvw-works.receive"},"properties":{"cvw.old-setting":"cvw.new-setting"}}}},
 None,
 ["RF RailForge/game-migrations files use top-level waybillDestinations, properties and carTypes dictionaries, with scalar targets or supported target objects.",
  "FUSE compatibility executes scalar waybillDestinations/properties only. Object-valued RF records and carTypes are not FUSE execution parity."])
b.write("recipes/rf-only.reference.json",b.place_rf_reference(dict(
 explanation="Separate reference surfaces. Place each payload according to placement, never copy this envelope as a graph.",
 companyStart=dict(placement="starts/cedar-valley.json, explicitly declared by mixintos.railforgeCompanyStarts",
 manifestFragment=dict(mixintos=dict(railforgeCompanyStarts=["file(starts/cedar-valley.json)"])),
 payload=dict(schemaVersion=1,startId="cvw-start",displayName="Cedar Valley",progressionId="ewh",showTutorial=False,openingCash=10000,
 playerSpawn=dict(position=[950,500,1000],rotationEuler=[0,0,0],radius=3,priority=1),enabledFeatures=[],
 trainPlacements=[dict(cars=["REPLACE-WITH-REAL-LOCOMOTIVE-DEFINITION-ID"],track=dict(segmentId="cvw-s-main-0",distance=20,end="A"),wreck=False,oil=1,initialFuelWaterPercent=1)],
 locomotiveOverrideSlot=dict(placementIndex=0,carIndex=0))),
 terrain=dict(placement="RF game graph, splineys; terrain identity must come from the map editor",
 payload=dict(splineys={"cvw-terrain":dict(handler="RailForge.NativeTerrainBrushes",formatVersion=1,strokes=[
 dict(operation="flatten",terrain="REPLACE-WITH-EXPORTED-TERRAIN-ID",centerX=1000,centerZ=1000,radius=10,square=False,amount=1,hardness=0.5,targetHeight=500)])}),
 otherOperations=["raise","lower","round","smooth","paint","erasePaint","addTrees","removeTrees","paintGrass","eraseGrass"]),
 infrastructure=dict(placement="RF game graph; replace the existing crossing ID with an inspected target",
 payload=dict(splineys={"RF_MapInfrastructureEdits":dict(handler="RailForge.MapEditor.InfrastructureOverrides",schemaVersion=2,
 crossings={"REPLACE-WITH-EXISTING-CROSSING-ID":dict(enabled=True,segmentId="cvw-s-main-0",distance=40,end="A",width=6,whistleDistance=100)},turntables={})})),
 migrations=dict(placement="RailForge/game-migrations/rename.json",
 payload=dict(waybillDestinations={"cvw-old-works.receive":"cvw-works.receive"},properties={"cvw.old-setting":{"to":"cvw.new-setting"}},carTypes={"REPLACE-OLD-TYPE":"REPLACE-NEW-TYPE"})),
 containers=dict(placement="RailForge/containers/<actual-container-identifier>.json; requires an existing asset container",
 payload={"$objectsByIdentifier":{"REPLACE-WITH-EXISTING-DEFINITION-ID":{"REPLACE-WITH-PROVIDER-FIELD":"REPLACE-WITH-VERIFIED-VALUE"}}},
 note="Only the container addressing envelope is shown. No complete provider object contract is claimed; never use $objectsByIdentifier in game-graph."),
 rollingStock=dict(placement="Inside an actual rolling-stock Definition components array, subject to its owner schema",
 payload=[dict(type="ConfusingSupplements.Bodygroups",name="cvw-details",enabled=True,groups={"lamps":dict(name="Lamps",options={"standard":dict(name="Standard",path=["REPLACE-WITH-MODEL-CHILD-PATH"])})}),
 dict(type="ConfusingSupplements.Refiller",name="cvw-refiller",enabled=True,transferRate=36000),
 dict(type="IndustryRefiller",name="cvw-industry-refiller",enabled=True,transferRate=36000),
 dict(type="CS.LiverySwap",name="cvw-livery",enabled=True)],
 note="DestinationSign and LabelPrinter also belong to Definition components; exact transforms/assets depend on the real rolling-stock schema. Refer to the matrix. Livery options need livery:<definition-id> directory mixintos.")
)))
base={"rows":[{"id":"a","value":1},{"id":"b","value":2}],"keep":True}
cases=[]
def case(name,rows,expected):
    cases.append(dict(name=name,patch=dict(rows=rows),expected=dict(rows=expected,keep=True)))
case("plain-array-replaces",[{"id":"c","value":3}],[{"id":"c","value":3}])
case("replace",[{"$replace":[{"id":"c","value":3}]}],[{"id":"c","value":3}])
case("remove-array",[{"$remove":True}],[])
case("add",[{"$add":{"id":"c","value":3}}],base["rows"]+[{"id":"c","value":3}])
case("append",[{"$append":[{"id":"c","value":3}]}],base["rows"]+[{"id":"c","value":3}])
case("find-patch",[{"$find":{"path":"id","value":"b","comp":"Equals"},"value":9}],[base["rows"][0],{"id":"b","value":9}])
case("optional-miss",[{"$find":{"path":"id","value":"missing"},"$optional":True}],base["rows"])
case("find-remove",[{"$find":{"path":"id","value":"a"},"$remove":True}],[base["rows"][1]])
case("clone",[{"$find":{"path":"id","value":"a"},"$clone":True,"id":"c","value":3}],base["rows"]+[{"id":"c","value":3}])
case("move",[{"$find":{"path":"id","value":"b"},"$moveTo":0}],[base["rows"][1],base["rows"][0]])
case("find-fallback",[{"$find":{"path":"id","value":"c"},"$add":{"id":"c","value":3}}],base["rows"]+[{"id":"c","value":3}])
case("mixed-program",[{"$find":{"path":"id","value":"a"},"value":9},{"id":"c","value":3}],[{"id":"a","value":9},base["rows"][1],{"id":"c","value":3}])
b.write("fixtures/rf-patch-cases.json",dict(base=base,cases=cases))

# DELTA45 follow-up: paired freight authoring, with oil-steam runtime scope kept explicit.
fuel=dict(name="Bunker C",units="Gallons",density=65,unitWeightInPounds=0,importable=True,payPerQuantity=0,costPerUnit=0.12)
purchase=b.comp("interchangedLoader","Cedar Valley Oil Supply","cvw-p-interchange",loadId="bunker-c",carTypeFilter="TM",carLoadPeriod=1,carLengthFeet=50)
receive=b.comp("unloader","Cedar Valley Bunker C Receiving","cvw-p-fuel",loadId="bunker-c",carTypeFilter="TM",sharedStorage=True,
 storageChangeRate=0,maxStorage=16000,carTransferRate=60000,orderAroundEmpties=False,orderAroundLoaded=False)
f={"operations":{"loads":{"bunker-c":fuel},"industries":{
 "cvw-interchange":{"name":"Cedar Valley Interchange","areaId":"cvw-area","position":v(30,0,0),"components":{"cvw-oil-supply":purchase}},
 "cvw-service":{"name":"Cedar Valley Engine Service","areaId":"cvw-area","position":v(-10,0,130),"components":{"cvw-oil-receive":receive}}}}}
rfuel=copy.deepcopy(fuel);rfuel["description"]=rfuel.pop("name")
r={"loads":{"bunker-c":rfuel},"areas":{"cvw-area":{"industries":{
 "cvw-interchange":{"components":{"cvw-oil-supply":b.rfcomp(purchase)}},
 "cvw-service":{"components":{"cvw-oil-receive":b.rfcomp(receive)}}}}}}
recipe("16-bunker-c-freight","Bunker C purchases and engine-service storage","paired-freight-with-RF-specific-refueling",
 ["Apply after the core; reuse an existing compatible bunker-c cargo if another provider owns it.",
  "DELTA45 refueling/steam behavior depends on enabled materializers, valid fuel slots and compatible hooks. FUSE locomotive oil consumption needs separately verified support."],
 f,r,
 ["The paired fragments define freight and storage in both graph formats. They do not implement locomotive fuel simulation in FUSE.",
  "Use exact load ID bunker-c. A positive authored price is preserved by RF; absent/null/zero is replaced by the 0.12 fallback. Wrong units, nonpositive density or importable:false hold automatic purchasing.",
  "The explicit cvw-oil-supply component prevents RF from adding a duplicate automatic supplier. Do not author RF's managed bmr-universal-bunker-c ID or generated -rf-bunker-c receiver suffix.",
  "The core's bare interchange alone is not eligible for automatic purchasing: DELTA45 also needs an existing InterchangedIndustryLoader purchase supplier and valid interchange spans.",
  "For an automatic-RF alternative, add an ordinary diesel purchase supplier instead and let DELTA45 own the added oil supplier. That automatic behavior is not FUSE parity.",
  "The service milestone still gates cvw-service. Buy a tank car, unload bunker-c into that industry's shared storage, then test the existing diesel stand with a compatible oil slot. Empty storage must not provide free fuel.",
  "Do not add a new bunkerFuel or oilSteam graph root: DELTA45 implements these as runtime compatibility services, not new authoring namespaces."])
catalog={"identifier":"CedarValleyParts","name":"Cedar Valley Parts","shared":False,
 "assets":{"cvw-oil-valve":{"name":"CVW Oil Valve","type":"GameObject","filename":"Assets/CedarValley/OilValve.prefab"}}}
recipe("17-catalog-only-parts","Catalog-only parts and sibling asset references","RF-DELTA45-discovery",
 ["Provide a real Unity-exported Catalog.json and matching nonempty Bundle. This recipe does not contain a bundle.",
  "The new standalone-discovery path examines a data package root and its immediate child folders; normal native asset-pack roots have their own discovery path."],
 None,None,
 ["Example layout: Your.Mod/MainAssets/{Catalog.json,Definitions.json,Bundle} and Your.Mod/Parts/{Catalog.json,Bundle}. Parts does not need a dummy Definitions.json for the new RF standalone path.",
  "Catalog identifier and assets object must be nonempty. Optional name/type/filename fields must have accepted types; a Bundle must exist directly in the same folder and be nonempty. Symbolic/link paths are rejected by this path.",
  "Sibling fallback uses the requested catalog identifier in the same physical parent under the active Mods root, among registered stores in validation scope. Multiple matches fail closed.",
  "Use the AssetReference specimen only inside an actual asset Definition field that expects that object; it is not the game-graph modelIdentifier syntax.",
  "FUSE's own asset-pack registration and dependency rules remain separate. Successful RF scanning is not successful Unity bundle loading."])
path=b.ROOT/"recipes/17-catalog-only-parts.recipe.json"
d=json.loads(path.read_text(encoding="utf-8"))
d["catalogExample"]=catalog
d["assetReferenceExample"]={"assetPackIdentifier":"CedarValleyParts","assetIdentifier":"cvw-oil-valve"}
b.write("recipes/17-catalog-only-parts.recipe.json",d)
