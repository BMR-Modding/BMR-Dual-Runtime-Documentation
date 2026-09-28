"""Validate repository-local Markdown links/anchors, JSON and code fences (stdlib only)."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import json
import re
import unicodedata

def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError("duplicate key "+key)
        result[key]=value
    return result

def read_json(text):
    def invalid(value):raise ValueError("non-JSON constant "+value)
    return json.loads(text,object_pairs_hook=unique,parse_constant=invalid)

def slug(text):
    text=re.sub(r"<[^>]*>","",text).strip().lower()
    text="".join(c for c in text if c in "-_ " or unicodedata.category(c)[0] in "LN")
    return text.replace(" ","-")

def inspect_markdown(text,path,errors):
    anchors=set();used={};outside=[];blocks=[];opened=None;body=[]
    for number,line in enumerate(text.splitlines(),1):
        fence=re.match(r"^\s{0,3}(\x60{3,}|~{3,})(.*)$",line)
        if fence:
            marker,language=fence.groups()
            if opened is None:
                opened=(marker,language.strip().lower(),number);body=[]
            elif marker[0]==opened[0][0] and len(marker)>=len(opened[0]) and not language.strip():
                blocks.append((opened[1],"\n".join(body),opened[2]));opened=None
            else:body.append(line)
            continue
        if opened is not None:
            body.append(line);continue
        outside.append(line)
        heading=re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$",line)
        if heading:
            base=slug(heading.group(1));count=used.get(base,0);used[base]=count+1
            anchors.add(base if count==0 else base+"-"+str(count))
        for value in re.findall(r'\b(?:id|name)=["\x27]([^"\x27]+)["\x27]',line):
            anchors.add(value)
    if opened is not None:errors.append(f"{path}:{opened[2]} unclosed code fence")
    return anchors,"\n".join(outside),blocks

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root",nargs="?",type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args();root=args.root.resolve()
    files=sorted(p for p in root.rglob("*") if p.is_file() and not any(x in (".git","__pycache__") for x in p.relative_to(root).parts))
    docs=[p for p in files if p.suffix.lower()==".md"]
    errors=[];cache={};local_links=0;fences=0;json_fences=0
    for p in docs:
        data=inspect_markdown(p.read_text(encoding="utf-8-sig"),p.relative_to(root),errors)
        cache[p.resolve()]=data
        for language,body,line in data[2]:
            fences+=1
            if language=="json":
                json_fences+=1
                try:read_json(body)
                except (ValueError,TypeError) as e:errors.append(f"{p.relative_to(root)}:{line} JSON fence: {e}")
    # Repository uses inline Markdown links, including angle-wrapped paths with spaces.
    links=re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)(?:\s+[\"'][^)]*[\"'])?\)")
    for p,(_,outside,_) in cache.items():
        for match in links.finditer(outside):
            target=match.group(1).strip("<>");parts=urlsplit(target)
            if parts.scheme or parts.netloc:continue
            local_links+=1
            path=(p.parent/unquote(parts.path)).resolve() if parts.path else p
            if not path.is_relative_to(root):
                errors.append(f"{p.relative_to(root)}: local link leaves repository: {target}");continue
            if not path.exists():
                errors.append(f"{p.relative_to(root)}: missing link: {target}");continue
            if parts.fragment and path.suffix.lower()==".md":
                anchor=unquote(parts.fragment)
                if path not in cache or anchor not in cache[path][0]:
                    errors.append(f"{p.relative_to(root)}: missing anchor: {target}")
    json_files=[p for p in files if p.suffix.lower()==".json"]
    for p in json_files:
        try:read_json(p.read_text(encoding="utf-8-sig"))
        except (ValueError,TypeError) as e:errors.append(f"{p.relative_to(root)}: {e}")
    report={"markdown_files":len(docs),"local_links":local_links,"code_fences":fences,"json_fences":json_fences,"json_files":len(json_files),"errors":errors}
    print(json.dumps(report,indent=2))
    return 1 if errors else 0

if __name__=="__main__":raise SystemExit(main())
