#!/usr/bin/env python3
"""Analyze StoneAge server per-level EXP configuration without preserving source payload."""

import argparse
import collections
import hashlib
from pathlib import Path

SAMPLE_LEVELS=(1,2,3,5,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,199)
SETUP_KEYS=("USEREXP","MAXLEVEL","LEVEL","REVLEVEL","CHARTRANS","PETTRANS","YBLEVEL")

def file_sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def parse_exp(path):
    rows=[]; malformed=[]
    for lineno,raw in enumerate(path.read_text(errors="replace").splitlines(),1):
        line=raw.split("#",1)[0].strip()
        if not line:continue
        parts=line.split()
        if len(parts)<2:
            malformed.append((lineno,"too_few_tokens"));continue
        try: value=int(parts[1],10)
        except ValueError:
            malformed.append((lineno,"non_integer_exp"));continue
        try: label=int(parts[0],10)
        except ValueError: label=None
        rows.append((label,value))
        if len(rows)>=199:break
    return rows,malformed

def parse_setup(path):
    out={}
    if not path or not path.exists():return out
    for raw in path.read_text(errors="replace").splitlines():
        line=raw.split("#",1)[0].strip()
        if not line or "=" not in line:continue
        k,v=line.split("=",1);k=k.strip().upper();v=v.strip()
        if k in SETUP_KEYS:out[k]=v
    return out

def analyze(exp_path,setup_path=None):
    rows,malformed=parse_exp(exp_path)
    vals=[v for _,v in rows]
    labels=[x for x,_ in rows]
    cumulative=[]; total=0
    for v in vals:
        total+=v;cumulative.append(total)
    decreases=sum(1 for a,b in zip(vals,vals[1:]) if b<a)
    duplicates=sum(1 for a,b in zip(vals,vals[1:]) if b==a)
    sequential=all(label==i for i,label in enumerate(labels,1) if label is not None)
    return {
        "rows":rows,"values":vals,"cumulative":cumulative,"malformed":malformed,
        "decreases":decreases,"duplicates":duplicates,"sequential_labels":sequential,
        "setup":parse_setup(setup_path),"sha256":file_sha256(exp_path),
        "bytes":exp_path.stat().st_size,
    }

def emit(r):
    vals=r["values"]; rows=r["rows"]; cum=r["cumulative"]
    print("StoneAge recovered server EXP probe — R1")
    print("No original EXP table payload is stored in this report.")\n    print("EXP_VALUE_SEMANTICS|server_LoadEXP_second_token_per_level_required_experience")
    print(f"EXP_SHA256|{r['sha256']}")
    print(f"EXP_BYTES|{r['bytes']}")
    print(f"EXP_ROWS|{len(rows)}")
    print(f"MALFORMED_ROWS|{len(r['malformed'])}")
    print(f"SEQUENTIAL_NUMERIC_LABELS|{int(r['sequential_labels'])}")
    if vals:
        print(f"EXP_MIN|{min(vals)}")
        print(f"EXP_MAX|{max(vals)}")
        print(f"EXP_DECREASE_TRANSITIONS|{r['decreases']}")
        print(f"EXP_EQUAL_TRANSITIONS|{r['duplicates']}")
        print(f"CUMULATIVE_TO_LAST_ROW|{cum[-1]}")
    for k in SETUP_KEYS:
        if k in r["setup"]:print(f"SETUP|{k}|{r['setup'][k]}")
    for level in SAMPLE_LEVELS:
        if 1<=level<=len(vals):
            print(f"LEVEL_SAMPLE|{level}|need={vals[level-1]}|cumulative={cum[level-1]}")
    for lo,hi in ((10,20),(20,40),(40,60),(60,80),(80,100),(100,120),(120,140),(140,160)):
        if hi<=len(vals) and vals[lo-1]:
            print(f"GROWTH_RATIO|{lo}|{hi}|{vals[hi-1]/vals[lo-1]:.6f}")
    for lineno,reason in r["malformed"][:20]:
        print(f"MALFORMED|{lineno}|{reason}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exp",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args();emit(analyze(a.exp,a.setup))

if __name__=="__main__":main()
