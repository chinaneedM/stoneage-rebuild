#!/usr/bin/env python3
"""Inventory recovered StoneAge gameplay-data candidates without copying payload bytes."""

import argparse
import collections
import hashlib
from pathlib import Path

CATEGORY_TERMS = {
    "pet": ("pet", "enemybase", "enemy_base"),
    "item": ("item",),
    "skill_magic": ("skill", "magic", "spell"),
    "character_npc_enemy": ("char", "chara", "npc", "enemy"),
    "battle_progression": (
        "battle", "encount", "encounter", "exp", "level", "rank",
        "profession", "job", "status", "duel", "parameter", "param",
    ),
    "quest_event": ("quest", "mission", "event", "schedule"),
    "economy_shop": ("shop", "gold", "money", "bank", "auction"),
}

def sha256(path: Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def labels_for(rel: str):
    s=rel.lower().replace("\\","/")
    labels=[]
    for name,terms in CATEGORY_TERMS.items():
        if any(term in s for term in terms):
            labels.append(name)
    return tuple(labels)

def scan(root: Path, side: str):
    rows=[]; ext=collections.Counter(); dirs=collections.Counter()
    total_bytes=0
    if not root.exists():
        return rows,ext,dirs,total_bytes
    for p in sorted((x for x in root.rglob("*") if x.is_file()), key=lambda x:str(x).lower()):
        rel=str(p.relative_to(root)).replace("\\","/")
        parts=rel.split("/")
        if any(part.lower()=="map" for part in parts[:-1]):
            continue
        size=p.stat().st_size; total_bytes+=size
        suffix=p.suffix.lower() or "<none>"
        ext[suffix]+=1; dirs[parts[0] if len(parts)>1 else "<root>"]+=1
        rows.append({
            "side":side,"rel":rel,"size":size,"suffix":suffix,
            "labels":labels_for(rel),
        })
    return rows,ext,dirs,total_bytes

def analyze(client_root: Path, server_root: Path):
    client,cext,cdirs,cbytes=scan(client_root,"client")
    server,sext,sdirs,sbytes=scan(server_root,"server")
    rows=client+server
    candidates=[r for r in rows if r["labels"]]
    return {
        "client":client,"server":server,"candidates":candidates,
        "cext":cext,"sext":sext,"cdirs":cdirs,"sdirs":sdirs,
        "cbytes":cbytes,"sbytes":sbytes,
    }

def emit(r, client_root: Path, server_root: Path):
    print("StoneAge recovered gameplay-data inventory — R1")
    print("No proprietary payload bytes are stored in this report.")
    print(f"CLIENT_DATA_FILE_COUNT|{len(r['client'])}")
    print(f"CLIENT_DATA_BYTES|{r['cbytes']}")
    print(f"SERVER_DATA_FILE_COUNT_EXCLUDING_MAP_DIRS|{len(r['server'])}")
    print(f"SERVER_DATA_BYTES_EXCLUDING_MAP_DIRS|{r['sbytes']}")
    print(f"GAMEPLAY_CANDIDATE_COUNT|{len(r['candidates'])}")
    for side,c in (("CLIENT",r["cext"]),("SERVER",r["sext"])):
        for ext,n in c.most_common():
            print(f"{side}_EXTENSION|{ext}|{n}")
    for side,c in (("CLIENT",r["cdirs"]),("SERVER",r["sdirs"])):
        for d,n in c.most_common():
            print(f"{side}_TOPLEVEL|{d}|{n}")
    for row in r["candidates"]:
        root=client_root if row["side"]=="client" else server_root
        path=root/row["rel"]
        print("CANDIDATE|{}|{}|{}|{}|{}|{}".format(
            row["side"],",".join(row["labels"]),row["rel"],row["size"],
            row["suffix"],sha256(path)
        ))
    # Preserve a filename-level view of all non-map server data so unknown historical
    # table names can be reviewed without exposing file contents.
    for row in r["server"]:
        print(f"SERVER_FILE|{row['rel']}|{row['size']}|{row['suffix']}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--client-data",type=Path,required=True)
    ap.add_argument("--server-data",type=Path,required=True)
    a=ap.parse_args()
    emit(analyze(a.client_data,a.server_data),a.client_data,a.server_data)

if __name__=="__main__":
    main()
