"""Static checks for the connected example. Python 3.10+, standard library only."""
import json,math,copy,importlib.util,hashlib
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PKG=ROOT/"package"/"ExampleAuthor.CedarValleyWorks"
checks=0
def check(ok,msg):
    global checks
    if not ok:raise AssertionError(msg)
    checks+=1
def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError("duplicate key "+k)
        d[k]=v
    return d
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
for p in ROOT.rglob("*.json"):read(p);check(True,"JSON "+str(p))
f=read(PKG/"game-graph.fuse.json");r=read(PKG/"RailForge/game-graph/cedar-valley.json")
info=read(PKG/"Info.json");d=read(PKG/"Definition.json")
check(info["Id"]==d["id"] and info["Version"]==d["version"],"manifest parity")
check(info["FuseDataFiles"]==["game-graph.fuse.json"],"FUSE discovery")
check(not info["Requirements"] and not d["requires"],"no runtime/provider requirements")
check(len(list((PKG/"RailForge/game-graph").glob("*.json")))==1,"one RF graph")
check("AssemblyName" not in info and "assemblies" not in d,"no initializer")
nodes=f["tracks"]["nodes"];segments=f["tracks"]["segments"];spans=f["tracks"]["spans"]
neighbors={n:set() for n in nodes}
for id,s in segments.items():
    a=s["startNodeId"];b=s["endNodeId"];check(a in nodes and b in nodes and a!=b,id+" endpoints")
    check(math.dist(list(nodes[a]["position"].values()),list(nodes[b]["position"].values()))>=1.0,id+" non-degenerate chord (not a curve-safety certificate)")
    neighbors[a].add(b);neighbors[b].add(a);t=r["tracks"]["segments"][id]
    check(t["startId"]==a and t["endId"]==b,id+" RF endpoints")
    check(t["trackClass"]=={"main":"Mainline","industrial":"Industrial"}[s["trackClass"]],id+" class")
    check(t["style"]=={"standard":"Standard","yard":"Yard"}[s["style"]],id+" style")
    check(not {"class","yard","bridgeSupportsSteel","partial","gauge"}.intersection(t),id+" RF fields")
seen=set();pending=[next(iter(nodes))]
while pending:
    n=pending.pop()
    if n not in seen:seen.add(n);pending+=list(neighbors[n]-seen)
check(seen==set(nodes),"connected topology");check(max(map(len,neighbors.values()))<=3,"node degree <= 3")
check(r["tracks"]["nodes"]==nodes,"node parity");check(r["tracks"]["spans"]==spans,"span parity")
for id,p in spans.items():
    check(p["upper"]["end"]=="A" and p["lower"]["end"]=="B",id+" inward endpoint directions")
    for k in ("upper","lower"):
        loc=p[k];check(loc["segmentId"] in segments,id+" span reference")
        check(("distance" in loc)!=("normalized" in loc),id+" location form")
        s=segments[loc["segmentId"]];x=nodes[s["startNodeId"]]["position"];y=nodes[s["endNodeId"]]["position"]
        chord=math.sqrt(sum((x[k]-y[k])**2 for k in x))
        check(0<=loc["distance"]<=chord,id+" distance <= chord")
loads=set(f["operations"]["loads"]);vanilla={"repair-parts","coal","diesel-fuel","building-supplies","rails"}
industries=f["operations"]["industries"]
for id,i in industries.items():
    check(i["areaId"] in f["tracks"]["areas"],id+" area")
    ri=r["areas"][i["areaId"]]["industries"][id]
    check(ri["localPosition"]==i["position"],id+" local position")
    check(set(ri["components"])==set(i["components"]),id+" component IDs")
    for cid,c in i["components"].items():
        rc=ri["components"][cid];check(rc["name"]==c["name"],cid+" name")
        for prop in ("trackSpanIds","inputSpanIds","outputSpanIds"):
            for target in c.get(prop,[]):check(target in spans,cid+" span")
        if "trackSpanIds" in c:check(rc["trackSpans"]==c["trackSpanIds"],cid+" span mapping")
        for prop in ("loadId","convertedLoadId"):
            if prop in c:check(c[prop] in loads|vanilla,cid+" load")
        for prop in ("inputTermsPerDay","outputTermsPerDay"):
            for load in c.get(prop,{}):check(load in loads|vanilla,cid+" formula")
        for profile in c.get("teamProfiles",{}).values():check(profile["loadId"] in loads|vanilla,"team cargo")
        if "carTypeFilter" in c:check(all(t==t.strip() for t in c["carTypeFilter"].split(",")),"filter tokens")
for id,l in f["operations"]["loads"].items():
    expected=copy.deepcopy(l);expected["description"]=expected.pop("name");check(expected==r["loads"][id],id+" load parity")
for id,s in f["world"]["scenery"].items():
    expected=copy.deepcopy(s);expected["modelIdentifier"]=expected.pop("assetIdentifier").removeprefix("scenery://")
    check(expected==r["scenery"][id],id+" known scenery mapping")
for id,l in f["operations"]["loaders"].items():
    check(l["industryId"] in industries,id+" industry")
    expected=copy.deepcopy(l);expected["industry"]=expected.pop("industryId");check(expected==r["loaders"][id],id+" loader parity")
feat=f["progression"]["mapFeatures"]["cvw-feature-service"]
check(feat["unlockIncludeIndustryComponents"]==[],"construction not permanently included")
check(feat["unlockIncludeIndustries"]==["cvw-service"],"service industry gate")
check(set(feat["trackGroupsEnableOnUnlock"])<=set(s["groupId"] for s in segments.values()),"group references")
check(feat["initiallyEnabled"] is False and r["mapFeatures"]["cvw-feature-service"]["defaultEnableInSandbox"] is False,"Sandbox parity")
check(set(feat["gameObjectsEnableOnUnlock"])<=set(f["world"]["scenery"])|set(f["operations"]["loaders"]),"object references")
phase=f["progression"]["progressions"]["ewh"]["sections"]["cvw-build-service"]["deliveryPhases"][0]
rp=r["progressions"]["ewh"]["sections"]["cvw-build-service"]["deliveryPhases"][0]
check(phase["industryComponentId"]=="cvw-works.construction","phase reference")
check(rp["industryComponent"]==dict(areaId="cvw-area",industryId="cvw-works",componentId="construction"),"RF phase reference")
for d,rd in zip(phase["deliveries"],rp["deliveries"],strict=True):
    check(d["destinationIndustryId"]=="cvw-works" and d["loadId"] in vanilla,"delivery references")
    check(rd["direction"]=="LoadToIndustry" and rd["count"]==d["count"] and rd["loadId"]==d["loadId"],"delivery mapping")
check(segments["cvw-s-construction"]["groupId"]=="cvw-base-track","construction reachable before unlock")
check(not list(PKG.rglob("*.dll")) and not list(PKG.rglob("*.recipe.json")),"package contents")

# Placement checks also catch translations applied incorrectly to local offsets.
placement=read(ROOT/"placement.json")
anchor=placement["position"];heading=placement["rotation"]
layout=read(ROOT/"layout-overrides.json")
check(nodes[placement["entranceNodeId"]]["position"]==layout["entranceCorrection"]["to"],"reviewed entrance correction")
check(all(n["rotation"]==heading for n in nodes.values()),"node heading matches upright placement")
check(all(n["position"]["y"]==anchor["y"] for n in nodes.values()),"flat track datum preserved")
def near(a,b,tolerance=0.000003):return all(abs(a[k]-b[k])<=tolerance for k in ("x","y","z"))
def dist(a,b):return math.sqrt(sum((a[k]-b[k])**2 for k in ("x","y","z")))
m0=nodes["cvw-n-m0"]["position"];m1=nodes["cvw-n-m1"]["position"]
check(abs(dist(m0,m1)-40)<0.000003,"corrected entrance has a 40-metre chord")
a=math.radians(heading["y"])
check(near({k:(m1[k]-m0[k])/40 for k in m0},dict(x=math.sin(a),y=0,z=math.cos(a))),"entrance follows existing heading")
area=f["tracks"]["areas"]["cvw-area"]["position"]
check(area==r["areas"]["cvw-area"]["localPosition"],"area origin parity")
check(placement["sourceNodeId"] not in nodes,"reference node is not overwritten or silently joined")
check(layout["referencePlacement"]==placement,"editor overlay and drawing frame agree")
export_path=ROOT/layout["source"]["path"]
check(hashlib.sha256(export_path.read_bytes()).hexdigest()==layout["source"]["sha256"],"unaltered editor export fingerprint")
export=read(export_path)
check(all(n==export["tracks"]["nodes"][id] for id,n in nodes.items() if id!="cvw-n-m0"),"all other editor node poses retained")
check("sceneClones" not in f["world"] and "mandelas" not in r,"no competing loader enabled/pose overrides")
for id,pose in layout["loaders"].items():
    actual=f["operations"]["loaders"][id]
    check(all(actual[k]==v for k,v in pose.items()),id+" reviewed pose")
    check(actual["industryId"]=="cvw-service" and id in feat["gameObjectsEnableOnUnlock"],id+" binding and feature ownership retained")
for id,fold in layout["foldedLoaderOverrides"].items():
    original=export["world"]["sceneClones"][fold["sourceKey"]]
    check(f["operations"]["loaders"][id]["position"]==original["localPosition"] and f["operations"]["loaders"][id]["rotation"]==original["localRotation"],id+" Objects pose incorporated")
for id,s in layout["segments"].items():
    check(f["tracks"]["segments"][id]["gauge"]=="Standard" and "gauge" not in r["tracks"]["segments"][id],id+" gauge boundary")
oil=read(ROOT/"recipes/16-bunker-c-freight.recipe.json")
for id,i in oil["fuseFragment"]["operations"]["industries"].items():
    check(i["position"]==industries[id]["position"],id+" recipe stays in correct local space")
conditional=read(ROOT/"recipes/10-settings-and-conditional-content.recipe.json")["conditionalExample"]
fs=conditional["fuseFile"]["payload"]["world"]["scenery"]["cvw-optional-warehouse"]
rs=conditional["railforgeFile"]["payload"]["scenery"]["cvw-optional-warehouse"]
check(fs["position"]==rs["position"] and fs["rotation"]==rs["rotation"]==heading,"conditional pose parity")
clones=read(ROOT/"recipes/08-scene-clones-and-suppression.recipe.json")
check(clones["fuseFragment"]["world"]["sceneClones"]["cvw-clone"]["localPosition"]==dict(x=1,y=0,z=0),"scene-parent local clone offset preserved")
passengers=read(ROOT/"recipes/03-passengers-and-station.recipe.json")
station=passengers["fuseFragment"]["operations"]["stations"]["cvw-station"]
check(station["position"]==passengers["railforgeFragment"]["splineys"]["cvw-station"]["position"],"station position parity")
spline=read(ROOT/"recipes/07-splineys-and-water.recipe.json")
for id in ("cvw-road","cvw-river","cvw-trestle"):
    fp=spline["fuseFragment"]["world"]["splineys"][id]["points"]
    check(fp==spline["railforgeFragment"]["splineys"][id]["points"] and abs(dist(fp[0]["position"],fp[1]["position"])-120)<0.000003,id+" points preserve shared geometry")
pond=spline["fuseFragment"]["world"]["waterSurfaces"]["cvw-pond"]["points"]
check(all(p["y"]==anchor["y"]-1 for p in pond),"pond retains one-metre height offset")
rfref=read(ROOT/"recipes/rf-only.reference.json")
start=rfref["companyStart"]["payload"]["playerSpawn"]
global_spawn=read(ROOT/"recipes/14-maps-tiles-and-spawns.recipe.json")["fuseFragment"]["world"]["spawnPoints"][0]
check(start["position"]==list(global_spawn["position"].values()) and start["rotationEuler"]==list(global_spawn["rotation"].values()),"company/global spawn placement agrees")
terrain=rfref["terrain"]["payload"]["splineys"]["cvw-terrain"]["strokes"][0]
check(near(dict(x=terrain["centerX"],y=terrain["targetHeight"],z=terrain["centerZ"]),area),"terrain teaching brush follows area datum")
check(info["Version"]==f["modVersion"],"graph and manifest version parity")

spec=importlib.util.spec_from_file_location("builder",ROOT/"tools/build-example.py");b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
bf,br=b.graph();check(bf==f and br==r,"graph generator reproducibility")
print(f"PASS: {checks} static assertions; {len(nodes)} nodes, {len(segments)} segments, {len(spans)} spans, {len(industries)} industries.")
