"""Build the fictional Cedar Valley Works authoring example (stdlib only).
This is an example-specific builder, not a general FUSE/RailForge converter.
"""
from pathlib import Path
import copy, json, math

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "package" / "ExampleAuthor.CedarValleyWorks"
VERSION = "1.1.0"
PLACEMENT = json.loads((ROOT / "placement.json").read_text(encoding="utf-8"))
if PLACEMENT["rotation"]["x"] or PLACEMENT["rotation"]["z"]:
    raise ValueError("Example placement supports yaw only; pitch/roll needs an extended transform")
def write(rel, value):
    path=ROOT/rel
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def vec(x=0,y=0,z=0): return dict(x=x,y=y,z=z)

def rotate_offset(p):
    """Rotate a direction/parent-local offset about Unity's positive Y axis."""
    a=math.radians(PLACEMENT["rotation"]["y"]-PLACEMENT["authoringHeadingDegrees"])
    c,s=math.cos(a),math.sin(a)
    return vec(round(c*p["x"]+s*p["z"],6),p["y"],round(-s*p["x"]+c*p["z"],6))
def world_position(p):
    """Place a point from the original drawing frame, pivoting on the entrance."""
    anchor=PLACEMENT["position"];origin=PLACEMENT["authoringEntrance"]
    delta=rotate_offset({k:p[k]-origin[k] for k in ("x","y","z")})
    return {k:round(anchor[k]+delta[k],6) for k in ("x","y","z")}
def world_rotation(p):
    # These specimens have upright poses; this is not a general Euler converter.
    if p["x"] or p["z"]:raise ValueError("Placement supports upright example poses only")
    return vec(0,round((p["y"]+PLACEMENT["rotation"]["y"]-PLACEMENT["authoringHeadingDegrees"])%360,6),0)
def place_pose(item,default_rotation=False):
    """Only known world-pose records enter here; clone-local transforms do not."""
    r=copy.deepcopy(item)
    for k in ("position","center"):
        if k in r:r[k]=world_position(r[k])
    if default_rotation:r.setdefault("rotation",vec())
    if "rotation" in r:r["rotation"]=world_rotation(r["rotation"])
    if "points" in r:
        r["points"]=[place_pose(p) if "position" in p else world_position(p) for p in r["points"]]
    return r
def place_fuse(fragment):
    r=copy.deepcopy(fragment)
    tracks=r.get("tracks",{})
    for kind in ("nodes","areas"):
        if kind in tracks:tracks[kind]={k:place_pose(v) if v is not None else None for k,v in tracks[kind].items()}
    ops=r.get("operations",{})
    for i in ops.get("industries",{}).values():
        if i is not None and "position" in i:i["position"]=rotate_offset(i["position"])
    for kind in ("loaders","stations","turntables"):
        if kind in ops:ops[kind]={k:place_pose(v,True) if v is not None else None for k,v in ops[kind].items()}
    world=r.get("world",{})
    for kind in ("scenery","mapLabels","mapMasks","splineys","waterSurfaces","telegraphPoles"):
        if kind in world:
            world[kind]={k:place_pose(v,kind=="scenery") if v is not None else None for k,v in world[kind].items()}
    if "spawnPoints" in world:world["spawnPoints"]=[place_pose(p) for p in world["spawnPoints"]]
    for movement in world.get("telegraphPoleMovements",[]):
        if "offset" in movement:movement["offset"]=rotate_offset(movement["offset"])
    return r
def place_rf(fragment):
    r=copy.deepcopy(fragment)
    if "nodes" in r.get("tracks",{}):
        r["tracks"]["nodes"]={k:place_pose(v) if v is not None else None for k,v in r["tracks"]["nodes"].items()}
    for area in r.get("areas",{}).values():
        if area is None:continue
        if "localPosition" in area:area["localPosition"]=world_position(area["localPosition"])
        for i in area.get("industries",{}).values():
            if i is not None and "localPosition" in i:i["localPosition"]=rotate_offset(i["localPosition"])
    for kind in ("scenery","loaders","mapLabels","splineys"):
        if kind in r:r[kind]={k:place_pose(v,kind in ("scenery","loaders")) if v is not None else None for k,v in r[kind].items()}
    for spline in r.get("splineys",{}).values():
        if spline is None:continue
        if "poleMovement" in spline:spline["poleMovement"]=[rotate_offset(p) for p in spline["poleMovement"]]
        if spline.get("handler")=="RailForge.NativeTerrainBrushes":
            for stroke in spline["strokes"]:
                point=world_position(vec(stroke["centerX"],stroke["targetHeight"],stroke["centerZ"]))
                stroke["centerX"],stroke["targetHeight"],stroke["centerZ"]=point["x"],point["y"],point["z"]
    return r
def place_recipe(d):
    r=copy.deepcopy(d)
    if "fuseFragment" in r:r["fuseFragment"]=place_fuse(r["fuseFragment"])
    if "railforgeFragment" in r:r["railforgeFragment"]=place_rf(r["railforgeFragment"])
    if "conditionalExample" in r:
        c=r["conditionalExample"]
        c["fuseFile"]["payload"]=place_fuse(c["fuseFile"]["payload"])
        c["railforgeFile"]["payload"]=place_rf(c["railforgeFile"]["payload"])
    return r
def place_rf_reference(d):
    r=copy.deepcopy(d)
    spawn=r["companyStart"]["payload"]["playerSpawn"]
    spawn["position"]=list(world_position(vec(*spawn["position"])).values())
    spawn["rotationEuler"]=list(world_rotation(vec(*spawn["rotationEuler"])).values())
    r["terrain"]["payload"]=place_rf(r["terrain"]["payload"])
    return r

def header(suffix,name):
    return dict(schemaVersion="1.0",id="ExampleAuthor.CedarValleyWorks."+suffix,name=name,
                author="Example Author",modVersion=VERSION,coordinateSpace="world")
def comp(kind,name,span=None,**kw):
    d=dict(type=kind,name=name)
    if span: d["trackSpanIds"]=[span]
    d.update(kw); return d
TYPES={"loader":"Model.Ops.IndustryLoader","unloader":"Model.Ops.IndustryUnloader",
 "formulaic":"Model.Ops.FormulaicIndustryComponent","repairTrack":"Model.Ops.RepairTrack",
 "teamTrack":"Model.Ops.TeamTrack","interchange":"Model.Ops.Interchange",
 "progression":"Model.Ops.ProgressionIndustryComponent","interchangedLoader":"Model.Ops.InterchangedIndustryLoader",
 "teleportLoading":"Model.Ops.TeleportLoadingIndustry","passengerStop":"RailForge.PassengerStation"}
def rfcomp(c):
    r=copy.deepcopy(c); r["type"]=TYPES.get(r["type"],r["type"])
    for a,b in [("trackSpanIds","trackSpans"),("inputSpanIds","inputSpans"),("outputSpanIds","outputSpans"),("branchDefinitions","branches")]:
        if a in r:r[b]=r.pop(a)
    return r
def ref(ind,component): return dict(areaId="cvw-area",industryId=ind,componentId=component)

def apply_editor_layout(f,r):
    """Apply this example's reviewed editor poses, not an arbitrary graph conversion."""
    layout=json.loads((ROOT/"layout-overrides.json").read_text(encoding="utf-8"))
    if layout["referencePlacement"]!=PLACEMENT:
        raise ValueError("Update the editor layout and its referencePlacement together; changing only placement.json would split the district.")
    if set(layout["nodes"])!=set(f["tracks"]["nodes"]):
        raise ValueError("Editor node IDs changed; review topology and spans before rebuilding.")
    f["tracks"]["nodes"]=copy.deepcopy(layout["nodes"])
    r["tracks"]["nodes"]=copy.deepcopy(layout["nodes"])
    for id,fields in layout["segments"].items():
        if fields!={"gauge":"Standard"}:
            raise ValueError("Only the editor's Standard gauge metadata has been reviewed.")
        f["tracks"]["segments"][id].update(fields)
        # This default gauge metadata has no general RF field counterpart.
    for id,pose in layout["loaders"].items():
        if set(pose)!={"position","rotation"}:
            raise ValueError("Only reviewed loader poses belong in layout-overrides.json.")
        f["operations"]["loaders"][id].update(copy.deepcopy(pose))
        r["loaders"][id].update(copy.deepcopy(pose))
    # Normalized loader poses are authoritative. No enabled:true scene override is emitted.
    return f,r

def graph():
    f=header("graph","Cedar Valley Works")
    f["description"]="Editor-adjusted fictional freight district near Andrews. Validate the approach, track curves, assets and railroad connection in game."
    f["tags"]=["example","fictional","dual-runtime"]
    points={"m0":(0,-160),"m1":(0,-120),"m2":(0,-80),"m3":(0,-40),
      "m4":(0,0),"m5":(0,40),"m6":(0,80),"m7":(0,140),
      "i0":(30,-80),"i1":(30,80),"f0":(-30,-40),"f1":(-30,80),
      "t0":(-60,0),"t1":(-60,100),"c0":(45,40),"c1":(85,110),
      "s0":(-25,80),"s1":(-25,180),"s2":(15,180)}
    nodes={"cvw-n-"+k:dict(position=vec(1000+x,500,1000+z),rotation=vec(),
             flipSwitchStand=False) for k,(x,z) in points.items()}
    segments={}
    def segment(k,a,b,service=False,main=False):
        segments["cvw-s-"+k]=dict(startNodeId="cvw-n-"+a,endNodeId="cvw-n-"+b,
          style="standard" if main else "yard",trackClass="main" if main else "industrial",
          speedLimit=15 if main else 5,priority=0,
          groupId="cvw-service-track" if service else "cvw-base-track",
          bridgeSupportsSteel=False,yard=not main)
    for i in range(7):segment("main-"+str(i),"m"+str(i),"m"+str(i+1),main=True)
    for k,a,b in [("interchange-in","m1","i0"),("interchange","i0","i1"),("interchange-out","i1","m6"),
       ("factory-in","m2","f0"),("factory","f0","f1"),("team-in","m3","t0"),("team","t0","t1"),
       ("construction-in","m4","c0"),("construction","c0","c1")]:segment(k,a,b)
    for k,a,b in [("service-in","m5","s0"),("repair","s0","s1"),("fuel","s0","s2")]:segment(k,a,b,True)
    spans={}
    for k,a,b in [("interchange",15,20),("factory",15,15),("team",10,15),("construction",10,15),("repair",10,15),("fuel",10,15)]:
        spans["cvw-p-"+k]=dict(upper=dict(segmentId="cvw-s-"+k,end="A",distance=a),
           lower=dict(segmentId="cvw-s-"+k,end="B",distance=b),normalize=True)
    area=dict(name="Cedar Valley",position=vec(1000,500,1000),radius=300,tagColor=[0.34,0.61,0.39,1],order=90)
    f["tracks"]=dict(nodes=nodes,segments=segments,spans=spans,areas={"cvw-area":area})
    loads={}
    for id,name,imp in [("cvw.unfinished-crates","Unfinished Crates",True),("cvw.finished-crates","Finished Crates",False)]:
        loads[id]=dict(name=name,units="Pounds",density=40,unitWeightInPounds=0,importable=imp,payPerQuantity=0,costPerUnit=0)
    works={
      "receive":comp("unloader","Crate Receiving","cvw-p-factory",loadId="cvw.unfinished-crates",carTypeFilter="XM*",sharedStorage=True,storageChangeRate=0,maxStorage=120000,carTransferRate=60000,orderAroundEmpties=True,orderAroundLoaded=True),
      "finish":comp("formulaic","Crate Finishing",sharedStorage=True,inputTermsPerDay={"cvw.unfinished-crates":20000},outputTermsPerDay={"cvw.finished-crates":20000}),
      "ship":comp("loader","Finished Crates","cvw-p-factory",loadId="cvw.finished-crates",carTypeFilter="XM*",sharedStorage=True,storageChangeRate=0,maxStorage=120000,carTransferRate=60000,orderAroundEmpties=True,orderAroundLoaded=True),
      "construction":comp("progression","Service Yard Construction","cvw-p-construction",carTypeFilter="XM*,FM*",sharedStorage=False)}
    service={"repair":comp("repairTrack","Cedar Valley Repair Track","cvw-p-repair",loadId="repair-parts",carTypeFilter="*",sharedStorage=True,canOverhaul=True)}
    for key,load,filter,span,cap in [("parts","repair-parts","XM*","repair",100000),("coal","coal","HM*,HT*","fuel",40000),("diesel","diesel-fuel","TM*","fuel",16000)]:
        service[key]=comp("unloader","Service "+key.title(),"cvw-p-"+span,loadId=load,carTypeFilter=filter,
           sharedStorage=True,storageChangeRate=0,maxStorage=cap,carTransferRate=60000,orderAroundEmpties=False,orderAroundLoaded=False)
    industries={}
    for id,name,pos,contract,components in [
      ("cvw-interchange","Cedar Valley Interchange",vec(30,0,0),False,{"exchange":comp("interchange","Cedar Valley Interchange","cvw-p-interchange")}),
      ("cvw-works","Cedar Valley Crate Works",vec(-30,0,20),True,works),
      ("cvw-team","Cedar Valley Team Track",vec(-60,0,50),True,{"public":comp("teamTrack","Public Freight Platform","cvw-p-team",teamProfiles={
        "crate-receipts":dict(loadId="cvw.unfinished-crates",isExport=False,loadingTimeDays=1,carTypeFilter="XM*"),
        "crate-exports":dict(loadId="cvw.finished-crates",isExport=True,loadingTimeDays=1,carTypeFilter="XM*")})}),
      ("cvw-service","Cedar Valley Engine Service",vec(-10,0,130),False,service)]:
        industries[id]=dict(name=name,areaId="cvw-area",position=pos,usesContract=contract,components=components)
    loaders={}
    for id,prefab,x,z in [("water","waterColumn",-30,150),("coal","coalConveyor",10,140),("diesel","dieselFuelingStand",20,150)]:
        loaders["cvw-loader-"+id]=dict(position=vec(1000+x,500,1000+z),rotation=vec(),prefab="vanilla://"+prefab,industryId="cvw-service")
    f["operations"]=dict(loads=loads,industries=industries,loaders=loaders)
    f["world"]=dict(scenery={
      "cvw-scenery-works":dict(assetIdentifier="scenery://freight-house-general",position=vec(950,500,1040),rotation=vec(),scale=vec(1,1,1)),
      "cvw-scenery-service":dict(assetIdentifier="scenery://brick-substation-medium",position=vec(950,500,1150),rotation=vec(),scale=vec(1,1,1))},
      mapLabels={"cvw-label":dict(text="Cedar Valley",position=vec(1000,500,1040))})
    feature=dict(displayName="Cedar Valley Engine Service",description="Repair and fuel facilities for the district.",
      initiallyEnabled=False,trackGroupsEnableOnUnlock=["cvw-service-track"],trackGroupsAvailableOnUnlock=["cvw-service-track"],
      gameObjectsEnableOnUnlock=["cvw-scenery-service",*loaders],unlockIncludeIndustries=["cvw-service"],unlockIncludeIndustryComponents=[])
    section=dict(displayName="Build Cedar Valley Engine Service",description="Deliver construction supplies at the existing construction siding.",
      prerequisiteSectionIds=[],enableFeaturesOnUnlock=["cvw-feature-service"],disableFeaturesOnUnlock=[],enableFeaturesOnAvailable=[],
      deliveryPhases=[dict(cost=2500,industryComponentId="cvw-works.construction",deliveries=[
        dict(carTypeFilter="XM*",loadId="building-supplies",count=2,direction="loadToIndustry",destinationIndustryId="cvw-works"),
        dict(carTypeFilter="FM*",loadId="rails",count=2,direction="loadToIndustry",destinationIndustryId="cvw-works")])])
    f["progression"]=dict(progressions={"ewh":dict(sections={"cvw-build-service":section})},mapFeatures={"cvw-feature-service":feature})
    r=dict(tracks=copy.deepcopy({k:v for k,v in f["tracks"].items() if k!="areas"}),loads={},areas={},scenery={},loaders={},mapLabels=copy.deepcopy(f["world"]["mapLabels"]))
    for s in r["tracks"]["segments"].values():
        s["startId"]=s.pop("startNodeId");s["endId"]=s.pop("endNodeId")
        s["style"]={"standard":"Standard","yard":"Yard"}[s["style"]]
        s["trackClass"]={"main":"Mainline","industrial":"Industrial"}[s["trackClass"]]
        s.pop("yard");s.pop("bridgeSupportsSteel")
    a=copy.deepcopy(area);a["localPosition"]=a.pop("position");a["industries"]={}
    for id,ind in industries.items():
        i=copy.deepcopy(ind);i.pop("areaId");i["localPosition"]=i.pop("position")
        i["components"]={k:rfcomp(c) for k,c in i["components"].items()};a["industries"][id]=i
    r["areas"]["cvw-area"]=a
    for id,l in loads.items():
        l=copy.deepcopy(l);l["description"]=l.pop("name");r["loads"][id]=l
    for id,l in loaders.items():
        l=copy.deepcopy(l);l["industry"]=l.pop("industryId");r["loaders"][id]=l
    for id,s in f["world"]["scenery"].items():
        s=copy.deepcopy(s);s["modelIdentifier"]=s.pop("assetIdentifier").removeprefix("scenery://");r["scenery"][id]=s
    feature=copy.deepcopy(feature);feature["defaultEnableInSandbox"]=feature.pop("initiallyEnabled")
    feature["gameObjectsEnableOnUnlock"]=["scenery://"+x if x in r["scenery"] else x for x in feature["gameObjectsEnableOnUnlock"]]
    r["mapFeatures"]={"cvw-feature-service":feature}
    section=copy.deepcopy(section);section["prerequisiteSections"]=section.pop("prerequisiteSectionIds")
    for phase in section["deliveryPhases"]:
        phase.pop("industryComponentId");phase["industryComponent"]=ref("cvw-works","construction")
        for d in phase["deliveries"]:d.pop("destinationIndustryId");d["direction"]="LoadToIndustry"
    r["progressions"]={"ewh":dict(sections={"cvw-build-service":section})}
    return apply_editor_layout(place_fuse(f),place_rf(r))
def build():
    info=dict(Id="ExampleAuthor.CedarValleyWorks",DisplayName="Cedar Valley Works (Authoring Example)",Author="Example Author",Version=VERSION,
      ManagerVersion="0.27.10",Requirements=[],LoadAfter=["FUSE","RTM.RailForge"],FuseRequires=[],FuseLoadAfter=[],FuseDataFiles=["game-graph.fuse.json"])
    definition=dict(manifestVersion=5,id=info["Id"],name=info["DisplayName"],author=info["Author"],version=info["Version"],requires=[],loadAfter=[])
    for name,obj in [("Info.json",info),("Definition.json",definition),("game-graph.fuse.json",graph()[0]),("RailForge/game-graph/cedar-valley.json",graph()[1])]:
        write("package/ExampleAuthor.CedarValleyWorks/"+name,obj)
if __name__=="__main__": build()
