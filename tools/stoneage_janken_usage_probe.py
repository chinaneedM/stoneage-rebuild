#!/usr/bin/env python3
"""Aggregate recovered Janken secondary arguments without dialogue/IDs/coordinates."""

import argparse
import collections
import hashlib
from pathlib import Path

TEMPLATE_MAGIC=b"NPCTEMPLATE"
CREATE_MAGIC=b"NPCCREATE"
KEYS=(b"MainMsg",b"EntryItem",b"NoItem",b"WinItem",b"LoseItem",b"WinWarp",b"LoseWarp")

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

def template_names(files):
    mapping=collections.defaultdict(list)
    for path in files:
        for entries in iter_blocks(path):
            d=dict(entries)
            name=d.get(b"templatename")
            if name:
                mapping[name].append(d.get(b"functionset",b""))
    return {
        name for name,defs in mapping.items()
        if len(defs)==1 and defs[0]==b"Janken"
    }

def refs(files):
    for path in files:
        for entries in iter_blocks(path):
            for key,value in entries:
                if key!=b"enemy":
                    continue
                name,sep,arg=value.partition(b"|")
                yield name.strip(),arg if sep else b""

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

def csv(value):
    if value is None or value==b"":
        return []
    return [x.strip() for x in value.split(b",")]

def atoi(value):
    s=value.lstrip()
    sign=1
    if s[:1] in (b"+",b"-"):
        sign=-1 if s[:1]==b"-" else 1
        s=s[1:]
    n=0
    found=False
    for ch in s:
        if not 48<=ch<=57:
            break
        found=True
        n=n*10+ch-48
    return sign*n if found else 0

def item_shape(value):
    values=csv(value)
    star=0
    plain=0
    quantities=[]
    ids=[]
    for token in values:
        if b"*" in token:
            item_id,count=token.split(b"*",1)
            star+=1
            ids.append(item_id)
            quantities.append(atoi(count))
        else:
            plain+=1
            ids.append(token)
    return (
        len(values),plain,star,tuple(quantities),
        len(ids)!=len(set(ids)),
    )

def analyze(npc_dir):
    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )
    names=template_names([p for p in files if magic_kind(p)=="template"])

    counts=collections.Counter()
    key_blocks=collections.Counter()
    shapes=collections.Counter()
    quantities=collections.Counter()
    warp_arity=collections.Counter()
    aggregate=hashlib.sha256()

    creates=[p for p in files if magic_kind(p)=="create"]
    for name,arg in refs(creates):
        if name not in names:
            continue
        counts["refs"]+=1
        filename=assigned_file(arg)
        if filename is not None:
            path=npc_dir/filename
            if not path.is_file():
                counts["missing_files"]+=1
                continue
            data=merge_file(path)
            counts["resolved_files"]+=1
        else:
            data=arg
            counts["inline"]+=1

        aggregate.update(
            str(len(data)).encode()+b"|"+
            hashlib.sha256(data).hexdigest().encode()+b"\n"
        )

        for key in KEYS:
            if field(data,key) is not None:
                key_blocks[key.decode("ascii")]+=1

        for key in (b"EntryItem",b"WinItem",b"LoseItem"):
            value=field(data,key)
            if value is None:
                continue
            length,plain,star,qs,duplicate=item_shape(value)
            label=key.decode("ascii")
            shapes[(label,"length",length)]+=1
            shapes[(label,"plain_tokens",plain)]+=1
            shapes[(label,"star_tokens",star)]+=1
            if duplicate:
                counts[label+"_duplicate_ids"]+=1
            for quantity in qs:
                quantities[(label,quantity)]+=1

        for key in (b"WinWarp",b"LoseWarp"):
            value=field(data,key)
            label=key.decode("ascii")
            if value is None:
                continue
            arity=len(csv(value))
            warp_arity[(label,arity)]+=1
            if arity!=3:
                counts[label+"_malformed"]+=1

        win=field(data,b"WinWarp")
        lose=field(data,b"LoseWarp")
        if win is not None and lose is not None and win==lose:
            counts["same_win_lose_warp"]+=1

    return {
        "counts":counts,
        "keys":key_blocks,
        "shapes":shapes,
        "quantities":quantities,
        "warp_arity":warp_arity,
        "aggregate":aggregate.hexdigest(),
    }

def emit(result):
    print("StoneAge recovered Janken usage probe — R1")
    print(
        "No NPC/template names, paths, dialogue, coordinates, concrete item IDs, "
        "or original argument rows are stored."
    )
    print(
        "SCHEMA|Janken refs -> secondary arg merge -> "
        "key/item-shape/warp-shape aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|"+result["aggregate"])
    for key,n in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{n}")
    for key,n in sorted(result["keys"].items()):
        print(f"KEY_BLOCK|{key}|{n}")
    for (key,metric,value),n in sorted(result["shapes"].items()):
        print(f"ITEM_SHAPE|{key}|{metric}={value}|blocks={n}")
    for (key,quantity),n in sorted(result["quantities"].items()):
        print(f"ITEM_QUANTITY|{key}|quantity={quantity}|tokens={n}")
    for (key,arity),n in sorted(result["warp_arity"].items()):
        print(f"WARP_ARITY|{key}|arity={arity}|blocks={n}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--npc-dir",type=Path,required=True)
    emit(analyze(parser.parse_args().npc_dir))

if __name__=="__main__":
    main()
