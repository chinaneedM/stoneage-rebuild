"""Reproduce default checked-in PET item macro gate and raw caller inventory.

Late pinned descendants only. No original assets/sources stored. GNU GCC
preprocessing of the checked-in default recipe is NOT a deployed binary
configuration certificate. -D_PET_ITEM is a controlled counterfactual.
"""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path
from tools.stoneage_pet_item_identity_source_audit import PROFILES,read_pinned,git_blob_id,demand

EXTRA={
 "gavin":{"make":("Makefile","d2be7a699c909c8e9515971b906dbc79586beb73"),
          "char_make":("char/makefile","e1843e9684078d23cc36a93c63f1c1adec90d4e4")},
 "bismarck":{"make":("makefile","8afd1f288a1d07a5cf0075af04e51e64741dcc81"),
             "char_make":("char/makefile","2c624e29639dc43169dfa5378d28e4086413c663"),
             "cmake":("../CMakeLists.txt","1523d12c3543e3d2a8c3a1401f92d79d11d85413"),
             "pet":("char/pet.c","5f18dbc539b2177e80c9616f772e0f58be5b8bdf")}}
MACROS=("_UNIQUE_P_I","_SIMPLIFY_ITEMSTRING","_PET_ITEM")

def run(cmd,input=None):
    p=subprocess.run(cmd,input=input,capture_output=True,text=True,timeout=100)
    if p.returncode:
        raise ValueError("original default compile probe failed: "+p.stderr[-1000:])
    return p.stdout

def inspect(profile,checkout):
    read_pinned(profile,checkout)
    root=checkout/PROFILES[profile]["root"]
    files={}
    for name,(path,sha) in EXTRA[profile].items():
        raw=(root/path).read_bytes()
        demand(git_blob_id(raw)==sha,"build file source drift "+profile+" "+name)
        files[name]=raw.decode("utf-8",errors="replace")
    for k in ("make","char_make"):
        s=files[k]
        demand("CFLAGS=" in s and "-I" in s and not re.search(r"(?m)^\s*(?:CFLAGS|CPPFLAGS|INCFLAGS)\s*[:+?]?=.*-D_PET_ITEM\b",s),"build flags changed")
    if profile=="bismarck":
        match=re.search(r"set\s*\(\s*STONEAGE_WINDOWS_DEFINITIONS\b(.*?)\)",files["cmake"],re.S)
        demand(match and "_PET_ITEM" not in match.group(1) and
               "target_compile_definitions" in files["cmake"],"Windows checked-in definitions changed")
    inc=[root/"include",root,root.parent/"common",root.parent/"common"/"utils",root.parent.parent/"shared"/"lua51"]
    flags=[f"-I{x}" for x in inc if x.exists()]
    macros=set(re.findall(r"(?m)^#define\s+([A-Za-z_]\w*)",run(
        ["gcc","-dM","-E","-x","c",*flags,"-include","version.h","-"],input="")))
    demand(all(x in macros for x in MACROS[:2]) and MACROS[2] not in macros,
           "default preprocessor macros differ from pinned source-only evidence")
    cfile=root/"char/char_item.c"
    def preprocess(path,more=()):
        return run(["gcc","-E","-P","-std=gnu99",*flags,*more,str(path)])
    baseline=preprocess(cfile)
    demand("CHAR_addItemSpecificItemIndex(" in baseline,"generic item add unexpectedly absent")
    raw=cfile.read_text(errors="replace")
    if profile=="bismarck":
        demand(re.search(r"#ifdef\s+_PET_ITEM[\s\S]*?void CHAR_movePetItem\s*\(",raw)!=None,
               "expected original source positive PET gate absent")
        demand("void CHAR_movePetItem(" not in baseline,"default PET equip unexpectedly compiled")
        toggled=preprocess(cfile,("-D_PET_ITEM",))
        demand("void CHAR_movePetItem(" in toggled and
               "CHAR_setItemIndex(petindex" in raw,
               "counterfactual enablement and original raw PET equipment setter disagree")
        demand("CHAR_sendPetItemData(" not in preprocess(root/"char/pet.c"),
               "default protocol PET send unexpectedly compiled")
    else:
        demand("void CHAR_movePetItem(" not in raw,"Gavin unexpected raw PET equipment handler")
        pet=preprocess(root/"char/char_base.c")
        demand("CHAR_getItemIndex( petindex, i)" not in pet and
               "CHAR_getItemIndex(petindex, i)" not in pet,
               "Gavin default preprocessing contains PET save branch")
    # No source code is emitted. This is a full recursive search over the
    # pinned C tree for the named equipment function.
    sites=[]
    for path in sorted(root.rglob("*.c")):
        for n,line in enumerate(path.read_text(errors="replace").splitlines(),1):
            if re.search(r"\bCHAR_movePetItem\s*\(",line):
                is_def=int(bool(re.search(r"^\s*void\s+CHAR_movePetItem\s*\(",line)))
                sites.append((path.relative_to(root).as_posix(),n,is_def))
    demand(sum(v[2] for v in sites)==int(profile=="bismarck"),
           "pinned PET equipment source definition count changed")
    h=hashlib.sha256()
    for path,line,is_def in sites:h.update(f"{path}:{line}:{is_def}\n".encode())
    out=dict(profile=profile,make_blob=EXTRA[profile]["make"][1],
             char_make_blob=EXTRA[profile]["char_make"][1],
             macro_unique=1,macro_simplify=1,macro_pet=0,
             default_pet_equip=0,forced_pet_equip=int(profile=="bismarck"),
             default_pet_send=0,raw_equip_definitions=int(profile=="bismarck"),
             raw_equip_callers=sum(1 for a in sites if not a[2]),
             raw_equip_occurrences=len(sites),site_sha256=h.hexdigest(),
             production_binary_verified=0,natural_pet_alias_proven=0,early_build_proven=0)
    rows=["SOURCE_PET_BUILD_GATE|"+"|".join(f"{k}={v}" for k,v in out.items())]
    rows += [f"SOURCE_PET_EQUIP_SITE|profile={profile}|path={a}|line={n}|definition={d}" for a,n,d in sites]
    return rows

def fields(line):
    parts=[a.split("=",1) for a in line.split("|")[1:]]
    if any(len(p)!=2 for p in parts) or len(parts)!=len(dict(parts)):
        raise ValueError("malformed source report field")
    return dict(parts)

def validate(report):
    summaries={}
    sites={p:[] for p in PROFILES}
    for line in report.splitlines():
        if line.startswith("SOURCE_PET_BUILD_GATE|"):
            f=fields(line);p=f.get("profile")
            if p not in PROFILES or p in summaries:raise ValueError("profile missing or repeated")
            expected=dict(profile=p,make_blob=EXTRA[p]["make"][1],
                          char_make_blob=EXTRA[p]["char_make"][1],macro_unique="1",
                          macro_simplify="1",macro_pet="0",default_pet_equip="0",
                          forced_pet_equip=str(int(p=="bismarck")),default_pet_send="0",
                          raw_equip_definitions=str(int(p=="bismarck")),
                          production_binary_verified="0",natural_pet_alias_proven="0",
                          early_build_proven="0")
            if set(f)!=set(expected)|{"raw_equip_callers","raw_equip_occurrences","site_sha256"}:
                raise ValueError("source report schema differs")
            if any(f[k]!=v for k,v in expected.items()) or not re.fullmatch(r"[a-f0-9]{64}",f["site_sha256"]):
                raise ValueError("false build or historical claim")
            summaries[p]=f
        elif line.startswith("SOURCE_PET_EQUIP_SITE|"):
            f=fields(line);p=f.get("profile")
            if set(f)!={"profile","path","line","definition"} or p not in sites:
                raise ValueError("bad PET call-site evidence")
            if not (re.fullmatch(r"[\w./-]+\.c",f["path"]) and f["line"].isdigit()
                    and f["definition"] in ("0","1")):raise ValueError("bad call-site type")
            sites[p].append((f["path"],int(f["line"]),int(f["definition"])))
    if set(summaries)!=set(PROFILES) or report.splitlines()[-1]!="RESOLUTION|PET_BUILD_DEFAULT_SOURCE_ONLY_PASS":
        raise ValueError("missing bounded resolution or profile")
    for p,arr in sites.items():
        s=summaries[p];h=hashlib.sha256()
        for path,n,isdef in arr:h.update(f"{path}:{n}:{isdef}\n".encode())
        if (int(s["raw_equip_occurrences"])!=len(arr)
            or int(s["raw_equip_callers"])!=sum(1 for v in arr if not v[2])
            or int(s["raw_equip_definitions"])!=sum(v[2] for v in arr)
            or h.hexdigest()!=s["site_sha256"]):
            raise ValueError("call site or digest mismatch")
    return summaries,sites

def main():
    parser=argparse.ArgumentParser()
    for p in PROFILES:parser.add_argument("--"+p+"-dir",type=Path,required=True)
    args=parser.parse_args()
    lines=[]
    for p in PROFILES:lines.extend(inspect(p,getattr(args,p+"_dir")))
    lines.extend(["BOUNDARY|Pinned late descendant checked-in make and default version.h processed by gcc; Bismarck counterfactual -D_PET_ITEM not deployed; no natural PET use or early binary claim",
                  "OPEN|production binary compile flags, enabled protocol handlers and callers, real PET equipment lifecycle, stable item unique-code across reused indexes, JSS1999/Taiwan1.0",
                  "RESOLUTION|PET_BUILD_DEFAULT_SOURCE_ONLY_PASS"])
    report="\n".join(lines)+"\n"
    validate(report)
    print(report,end="")

if __name__=="__main__":main()
