#!/usr/bin/env python3
"""Aggregate recovered Bus/Airplane secondary arguments without route/item payloads."""

import argparse
import collections
import hashlib
from pathlib import Path

TEMPLATE_MAGIC=b"NPCTEMPLATE"
CREATE_MAGIC=b"NPCCREATE"

COMMON_KEYS=(
    b"routenum",b"waittime",b"seflg",b"reverse",b"denieditem",
    b"pickupitem",b"allowitem",b"needlevel",b"needstone",
)
AIR_KEYS=(b"WAVE",b"oneway",b"delitem",b"maxlevel")
MESSAGE_KEYS=(
    b"gettingonmsg",b"notpartymsg",b"overpartymsg",b"denieditemmsg",
    b"allowitemmsg",b"levelmsg",b"goldmsg",b"startmsg",b"endmsg",
    b"delitemmsg",b"maxlevelmsg",
)

def source_candidate(path):
    n=path.name.lower()
    return not (
        path.name.endswith("~") or path.name.startswith("#") or n.endswith(".bak")
    )

def magic_kind(path):
    if not source_candidate(path):
        return None
    try:
        with path.open("rb") as f:
            first=f.readline().rstrip(b"\r\n")
    except OSError:
        return None
    if first==TEMPLATE_MAGIC:
        return "template"
    if first==CREATE_MAGIC:
        return "create"
    return None

def iter_blocks(path):
    block=None
    with path.open("rb") as f:
        next(f,b"")
        for raw in f:
            line=raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            if line.startswith(b"{"):
                block=[]
                continue
            if line.startswith(b"}"):
                if block is not None:
                    yield block
                block=None
                continue
            if block is None or b"=" not in line:
                continue
            k,v=line.split(b"=",1)
            block.append((k.strip().lower(),v.strip()))

def template_map(paths):
    out=collections.defaultdict(list)
    for path in paths:
        for entries in iter_blocks(path):
            d=dict(entries)
            name=d.get(b"templatename")
            if name:
                out[name].append(d.get(b"functionset",b""))
    return out

def create_refs(paths):
    for path in paths:
        for entries in iter_blocks(path):
            for key,value in entries:
                if key!=b"enemy":
                    continue
                name,sep,arg=value.partition(b"|")
                yield name.strip(), arg if sep else b""

def assigned_file(arg):
    for token in arg.split(b"|"):
        if b"file" in token:
            parts=token.split(b":")
            if len(parts)>=2:
                return parts[1].decode("utf-8","replace")
    return None

def merge_file(path):
    out=b""
    with path.open("rb") as f:
        for raw in f:
            line=raw.rstrip(b"\r\n")
            if out and not out.endswith(b"|"):
                out+=b"|"
            out+=line
    return out

def field(data,key):
    for token in data.split(b"|"):
        if key in token:
            parts=token.split(b":")
            if len(parts)>=2:
                return parts[1]
    return None

def atoi(value):
    if value is None:
        return None
    s=value.lstrip()
    sign=1
    if s[:1] in (b"+",b"-"):
        sign=-1 if s[:1]==b"-" else 1
        s=s[1:]
    n=0
    found=False
    for ch in s:
        if ch<48 or ch>57:
            break
        found=True
        n=n*10+ch-48
    return sign*n if found else 0

def list_values(value,delim=b","):
    if value is None or value==b"":
        return []
    return [part.strip() for part in value.split(delim)]

def analyze(npc_dir):
    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )
    mapping=template_map([p for p in files if magic_kind(p)=="template"])
    names={
        kind:{
            name for name,defs in mapping.items()
            if len(defs)==1 and defs[0]==kind.encode()
        }
        for kind in ("Bus","Airplane")
    }

    counts=collections.Counter()
    key_blocks=collections.Counter()
    scalars=collections.Counter()
    item_lengths=collections.Counter()
    route_lengths=collections.Counter()
    point_arities=collections.Counter()
    aggregate=hashlib.sha256()

    for kind in ("Bus","Airplane"):
        for key in ("refs","resolved_files","inline","missing_files"):
            counts[(kind,key)]=0

    creates=[p for p in files if magic_kind(p)=="create"]
    for name,arg in create_refs(creates):
        kind=None
        for candidate in ("Bus","Airplane"):
            if name in names[candidate]:
                kind=candidate
                break
        if kind is None:
            continue

        counts[(kind,"refs")]+=1
        filename=assigned_file(arg)
        if filename is not None:
            path=npc_dir/filename
            if not path.is_file():
                counts[(kind,"missing_files")]+=1
                continue
            data=merge_file(path)
            counts[(kind,"resolved_files")]+=1
        else:
            data=arg
            counts[(kind,"inline")]+=1

        aggregate.update(
            kind.encode()+b"|"+str(len(data)).encode()+b"|"+
            hashlib.sha256(data).hexdigest().encode()+b"\n"
        )

        for key in COMMON_KEYS + (AIR_KEYS if kind=="Airplane" else ()) + MESSAGE_KEYS:
            if field(data,key) is not None:
                key_blocks[(kind,key.decode("ascii"))]+=1

        for key in (
            b"routenum",b"waittime",b"seflg",b"reverse",
            b"needlevel",b"needstone",
        ):
            value=field(data,key)
            if value is not None:
                scalars[(kind,key.decode("ascii"),atoi(value))]+=1

        if kind=="Airplane":
            for key in (b"WAVE",b"oneway",b"maxlevel"):
                value=field(data,key)
                if value is not None:
                    scalars[(kind,key.decode("ascii"),atoi(value))]+=1

        for key in (b"denieditem",b"allowitem",b"pickupitem",b"delitem"):
            if kind=="Bus" and key==b"delitem":
                continue
            value=field(data,key)
            if value is not None:
                vals=list_values(value)
                k=key.decode("ascii")
                item_lengths[(kind,k,len(vals))]+=1
                if len(vals)!=len(set(vals)):
                    counts[(kind,k+"_duplicates")]+=1

        routenum=atoi(field(data,b"routenum"))
        if routenum is None:
            counts[(kind,"missing_routenum")]+=1
            routenum=0

        resolved=0
        malformed=0
        for i in range(1,max(0,routenum)+1):
            route=field(data,("routeto%d"%i).encode())
            if route is None:
                counts[(kind,"missing_declared_route")]+=1
                continue
            resolved+=1
            points=list_values(route,b";")
            route_lengths[(kind,len(points))]+=1
            floors=[]
            for point in points:
                fields=list_values(point,b",")
                arity=len(fields)
                point_arities[(kind,arity)]+=1
                expected=2 if kind=="Bus" else 3
                if arity!=expected:
                    malformed+=1
                if kind=="Airplane" and fields:
                    floors.append(fields[0])
            if kind=="Airplane" and len(set(floors))>1:
                counts[(kind,"routes_with_floor_change")]+=1

        counts[(kind,"declared_routes_resolved")]+=resolved
        counts[(kind,"malformed_route_points")]+=malformed

    return {
        "counts":counts,
        "key_blocks":key_blocks,
        "scalars":scalars,
        "item_lengths":item_lengths,
        "route_lengths":route_lengths,
        "point_arities":point_arities,
        "aggregate":aggregate.hexdigest(),
    }

def emit(result):
    print("StoneAge recovered Bus/Airplane usage probe — R1")
    print(
        "No template names, file paths, route names, coordinates, item IDs, "
        "or original argument rows are stored."
    )
    print(
        "SCHEMA|transport refs -> secondary arg merge -> "
        "key/scalar/list/route-shape aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|"+result["aggregate"])
    for (kind,key),n in sorted(result["counts"].items()):
        print(f"COUNT|{kind}|{key}|{n}")
    for (kind,key),n in sorted(result["key_blocks"].items()):
        print(f"KEY_BLOCK|{kind}|{key}|{n}")
    for (kind,key,value),n in sorted(result["scalars"].items()):
        print(f"SCALAR|{kind}|{key}|value={value}|blocks={n}")
    for (kind,key,length),n in sorted(result["item_lengths"].items()):
        print(f"ITEM_LIST_LENGTH|{kind}|{key}|length={length}|blocks={n}")
    for (kind,length),n in sorted(result["route_lengths"].items()):
        print(f"ROUTE_POINT_COUNT|{kind}|points={length}|routes={n}")
    for (kind,arity),n in sorted(result["point_arities"].items()):
        print(f"ROUTE_POINT_ARITY|{kind}|arity={arity}|points={n}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--npc-dir",type=Path,required=True)
    emit(analyze(parser.parse_args().npc_dir))

if __name__=="__main__":
    main()
