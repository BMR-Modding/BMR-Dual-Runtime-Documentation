"""Rebuild the property atlas from a supplied public FUSE schema (no third-party Python packages)."""
import argparse,copy,hashlib,json
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument("--schema",required=True);a=P.parse_args()
source=Path(a.schema);schema=json.loads(source.read_text(encoding="utf-8-sig"))
root=Path(__file__).resolve().parents[1]
def deref(n):return schema["$defs"][n["$ref"].split("/")[-1]] if "$ref" in n else n
def synth(n,key="example",depth=0):
    n=deref(n)
    if depth>10:return {}
    if "const" in n:return n["const"]
    if "enum" in n:return n["enum"][0]
    if "default" in n:return copy.deepcopy(n["default"])
    if "oneOf" in n and "properties" not in n:return synth(n["oneOf"][0],key,depth+1)
    if "allOf" in n:
        merged={}
        for part in n["allOf"]:
            part=deref(part)
            merged.update(part)
        merged.update({k:v for k,v in n.items() if k!="allOf"})
        return synth(merged,key,depth+1)
    t=n.get("type")
    if isinstance(t,list):t=t[0]
    if t=="object" or "properties" in n:
        required=list(n.get("required",[]))
        if "oneOf" in n:required+=n["oneOf"][0].get("required",[])
        if "anyOf" in n:required+=n["anyOf"][0].get("required",[])
        if n.get("minProperties",0) and not required:required=list(n.get("properties",{}))[:n["minProperties"]]
        return {k:synth(n.get("properties",{}).get(k,{}),k,depth+1) for k in dict.fromkeys(required)}
    if t=="array":
        minimum=n.get("minItems",0)
        # A nonempty example is more useful for an ordinary ID list, but default [] remains truthful.
        if not minimum and n.get("items",{}).get("$ref","").endswith(("/id","/idRef")):minimum=1
        return [synth(n.get("items",{}),key,depth+1) for _ in range(minimum)]
    if t=="boolean":return True
    if t=="null":return None
    if t in ("number","integer"):
        val=max(1,n.get("minimum",1))
        if isinstance(n.get("exclusiveMinimum"),(int,float)):val=max(val,n["exclusiveMinimum"]+0.1)
        if "maximum" in n:val=min(val,n["maximum"])
        return int(val) if t=="integer" else val
    if t=="string":
        if key=="color":return "#FFFFFFFF"
        if n.get("format")=="date-time":return "2026-09-21T00:00:00Z"
        if "pattern" in n and "vanilla" in n["pattern"]:return "scenery://freight-house-general"
        if key in ("name","displayName","projectName"):return "Cedar Valley Works"
        if key=="description":return "Fictional syntax example."
        if key in ("carTypeFilter","emptyCarType","loadedCarType"):return "XM*"
        if key in ("file","clip","sourceFile"):return "file://Audio/cvw-example.wav"
        if key in ("targetPath","sourceLakePath"):return "World/REPLACE-WITH-VERIFIED-PATH"
        if key in ("controllerType",):return "ExampleProvider.Controller, ExampleProvider"
        if key in ("directory","mapFolder","sourceFolder"):return "Maps/CedarValley"
        if key=="type":return "loader"
        return "cvw-example"
    if "anyOf" in n:return synth(n["anyOf"][0],key,depth+1)
    return "cvw-example"
entries=[]
def scan(node,pointer,label):
    for name,prop in node.get("properties",{}).items():
        escaped=name.replace("~","~0").replace("/","~1")
        ptr=pointer+"/properties/"+escaped
        entries.append(dict(field=label+"."+name,pointer=ptr,example=synth(prop,name)))
        scan(prop,ptr,label+"."+name)
    for keyword in ("allOf","anyOf","oneOf"):
        for i,sub in enumerate(node.get(keyword,[])):
            scan(sub,pointer+"/"+keyword+"/"+str(i),label)
scan(schema,"","root")
for name,definition in schema.get("$defs",{}).items():scan(definition,"/$defs/"+name,name)
out=dict(schemaId=schema.get("$id"),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),propertyCount=len(entries),entries=entries)
(root/"reference").mkdir(exist_ok=True)
(root/"reference"/"fuse-field-examples.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
lines=["# FUSE field atlas","","[Example walkthrough](../README.md) · [Recipe index](../RECIPES.md) · [Translation matrix](../../../Duality%20mode%20documentation/FUSE-RailForge-Complete-Translation-Matrix.md)","",
 f"This inventory covers **{len(entries)} declared property locations** in the supplied public FUSE schema, including nested objects. It is generated from schema ID §{schema.get('$id')}§, SHA-256 §{out['sha256']}§.",
 "",
 "Each row demonstrates the JSON value of **one field**. Values are syntax specimens, not one combined game graph. IDs, scene paths, profiles, controllers and assets must resolve in your actual package. Defaults in the schema are not proof of runtime support or sensible gameplay.",
 "",
 "Mutually exclusive forms remain separate: choose distance **or** normalized track locations; assetIdentifier **or** prefab for object lines; one mask shape; one setting type. Read the connected core and recipes before combining fields.",
 "",
 "The machine-readable [examples](fuse-field-examples.json) preserve exact schema pointers. §Validate-Example.ps1 -FuseSchema <path>§ checks every value against its own property schema; that does not validate referenced game objects or the enclosing component's behavior.",
 ""]
def compact(n):
    d=deref(n);parts=[]
    if "$ref" in n:parts.append(n["$ref"].split("/")[-1])
    if "type" in d:parts.append(str(d["type"]))
    if "enum" in d:parts.append("enum: "+", ".join(str(x) for x in d["enum"]))
    for k in ("minimum","maximum","exclusiveMinimum","minItems","maxItems","pattern","deprecated"):
        if k in d:parts.append(k+"="+str(d[k]))
    return "; ".join(parts).replace("|","\\|")
def get(ptr):
    n=schema
    for bit in ptr.lstrip("/").split("/"):
        bit=bit.replace("~1","/").replace("~0","~")
        n=n[int(bit)] if isinstance(n,list) else n[bit]
    return n
group=None
for e in entries:
    prefix=e["field"].split(".")[0]
    if prefix!=group:
        lines+=["## "+prefix,"","| Field | Example value | Schema constraints |","| --- | --- | --- |"];group=prefix
    value=json.dumps(e["example"],ensure_ascii=False,separators=(",",":")).replace("|","\\|")
    lines.append("| §"+e["field"]+"§ | §"+value+"§ | "+compact(get(e["pointer"]))+" |")
(root/"reference"/"FUSE-FIELD-ATLAS.md").write_text("\n".join(lines).replace("§",chr(96))+"\n",encoding="utf-8")
print("Generated",len(entries),"property examples")
