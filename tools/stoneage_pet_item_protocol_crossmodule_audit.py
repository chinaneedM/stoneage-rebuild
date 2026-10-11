"""Correct and extend PET equipment call-path evidence across server/common.

Do not extrapolate the earlier zero-call result beyond its server/gmsv subtree.
The protocol wrapper and native equipment body share an optional _PET_ITEM
gate. Neither checked-in-default compilation nor natural client reachability
is established by seeing disabled raw source bodies.
"""
from pathlib import Path
import argparse
import hashlib
import re
from tools.stoneage_pet_item_identity_source_audit import PROFILES,read_pinned,git_blob_id,demand
from tools.stoneage_pet_item_build_gate_audit import run

ORIGINAL={
 "repo":"BismarckDD/stoneage",
 "commit":"999ffdf1d220ec6666eb65339180689c9caf1876",
 "handler":"088db5e38a1bc0dd47b3c3120480af93ab24c4c7",
 "dispatch":"84dd1b2d9fbac10fe39983e6b8984aaebf1b3075",
 "common_make":"263ef622f4c0c3ac495d783ff35b078277984d43",
 "equipment":"970b7b3f975965c6c5e77352a2e0382adf943753",
}
SYMBOLS=("CHAR_movePetItem","GmsvServer_PETITEM_recv")

def c_source(root,path,blob):
    raw=(root/path).read_bytes()
    demand(git_blob_id(raw)==blob,"pinned historical descendant file changed: "+path)
    return raw.decode("utf-8",errors="replace")

def cpp(repo_root,source,forced=False):
    root=repo_root/"server"
    includes=[root/"common",root/"common"/"utils",root/"gmsv"/"include",
              root/"gmsv",repo_root/"shared"/"lua51"]
    cmd=["gcc","-E","-P","-std=gnu99",*[f"-I{x}" for x in includes],
         *(["-D_PET_ITEM"] if forced else []),str(source)]
    return run(cmd)

def check(repo_root):
    read_pinned("bismarck",repo_root)
    srcroot=repo_root/"server"
    h=srcroot/"common/gmsv_server_recv.c"
    char=srcroot/"gmsv/char/char_item.c"
    send=srcroot/"common/gmsv_server_send.c"
    rawh=c_source(srcroot,"common/gmsv_server_recv.c",ORIGINAL["handler"])
    rawc=c_source(srcroot,"gmsv/char/char_item.c",ORIGINAL["equipment"])
    rawsend=c_source(srcroot,"common/gmsv_server_send.c",ORIGINAL["dispatch"])
    mk=c_source(srcroot,"common/makefile",ORIGINAL["common_make"])
    demand("GMSVSERVER_SRC=gmsv_server_send.c gmsv_server_recv.c" in mk and
           "GMSV_CFLAGS=$(CFLAGS) -I../gmsv/include" in mk and
           "-D_PET_ITEM" not in mk,
           "original common library PET macro or protocol source recipe changed")
    demand("#ifdef _PET_ITEM" in rawh and
           "void GmsvServer_PETITEM_recv(" in rawh and
           "CHAR_movePetItem(char_index, petindex, fromindex, toindex);" in rawh,
           "original optional PET protocol callback or direct call changed")
    demand("#ifdef _PET_ITEM" in rawc and "void CHAR_movePetItem(" in rawc and
           "CHAR_setItemIndex(petindex" in rawc,
           "original optional native PET equipment body changed")
    demand("#ifdef _PET_ITEM" in rawsend and
           "LSSPROTO_PET_ITEM_RECV" in rawsend and
           "GmsvServer_PETITEM_recv(fd, x, y, petindex, fromindex, toindex);" in rawsend,
           "original feature-gated opcode decoder source body changed")
    default_send=cpp(repo_root,send)
    enabled_send=cpp(repo_root,send,forced=True)
    demand("GmsvServer_PETITEM_recv(" not in default_send and
           "GmsvServer_PETITEM_recv(" in enabled_send,
           "default or forced PET equipment packet callback emission changed")
    default_h=cpp(repo_root,h)
    enabled_h=cpp(repo_root,h,forced=True)
    default_char=cpp(repo_root,char)
    enabled_char=cpp(repo_root,char,forced=True)
    demand("void GmsvServer_PETITEM_recv(" not in default_h and
           "void CHAR_movePetItem(" not in default_char,
           "checked-in common/GMSV default preprocessor unexpectedly includes PET equipment")
    demand("void GmsvServer_PETITEM_recv(" in enabled_h and
           "CHAR_movePetItem(" in enabled_h and
           "void CHAR_movePetItem(" in enabled_char,
           "explicit -D_PET_ITEM did not expose complete optional callback to equipment chain")
    demand("void GmsvServer_MI_recv(" in default_h and
           "CHAR_moveEquipItem(" in default_h,
           "default regular item movement entry unexpectedly absent")
    # Search *all server C source*, unlike the earlier deliberately narrowed
    # gmsv source-root scan. This includes the independently built common lib.
    sites=[]
    for path in sorted(srcroot.rglob("*.c")):
        content=path.read_text(errors="replace")
        for n,line in enumerate(content.splitlines(),1):
            for symbol in SYMBOLS:
                if re.search(r"\b"+symbol+r"\s*\(",line):
                    is_def=int(bool(re.search(r"^\s*void\s+"+symbol+r"\s*\(",line)))
                    sites.append((symbol,path.relative_to(srcroot).as_posix(),n,is_def))
    def matched(sym):
        return [s for s in sites if s[0]==sym]
    demand(("CHAR_movePetItem","common/gmsv_server_recv.c",1010,0) in sites and
           ("GmsvServer_PETITEM_recv","common/gmsv_server_send.c",1388,0) in sites and
           ("CHAR_movePetItem","gmsv/char/char_item.c",2655,1) in sites and
           ("GmsvServer_PETITEM_recv","common/gmsv_server_recv.c",985,1) in sites,
           "original cross-library handler->item chain callsite drift")
    demand(len(matched("CHAR_movePetItem"))==2 and
           sum(row[3] for row in matched("CHAR_movePetItem"))==1,
           "cross-module original PET equipment caller inventory changed")
    digest=hashlib.sha256()
    for s in sites:digest.update(("|".join(map(str,s))+"\n").encode())
    summary=dict(
      profile="bismarck",handler_blob=ORIGINAL["handler"],dispatch_blob=ORIGINAL["dispatch"],common_make_blob=ORIGINAL["common_make"],
      equipment_blob=ORIGINAL["equipment"],gmsv_subtree_direct_callers=0,
      whole_server_pet_equip_definitions=1,whole_server_pet_equip_direct_callers=1,
      protocol_recv_definitions=1,default_dispatch_compiled=0,forced_dispatch_compiled=1,conditional_opcode_handler_present=1,default_protocol_compiled=0,
      default_equipment_compiled=0,forced_protocol_compiled=1,forced_equipment_compiled=1,
      default_MI_recv_present=1,caller_under_positive_macro=1,
      known_compiled_production_binary=0,natural_pet_item_path_proven=0,early_original_build_proven=0,
      site_sha256=digest.hexdigest())
    lines=["SOURCE_PET_PROTOCOL_GATE|"+"|".join(f"{k}={v}" for k,v in summary.items())]
    lines += [f"SOURCE_PET_PROTOCOL_SITE|symbol={sym}|path={path}|line={n}|definition={d}"
              for sym,path,n,d in sites]
    return lines

def parse(s):
    entries=[x.split("=",1) for x in s.split("|")[1:]]
    if any(len(x)!=2 for x in entries) or len(entries)!=len(dict(entries)):
        raise ValueError("malformed or duplicate protocol evidence")
    return dict(entries)

def validate_report(report):
    summaries=[]
    sites=[]
    for s in report.splitlines():
        if s.startswith("SOURCE_PET_PROTOCOL_GATE|"):
            a=parse(s)
            if summaries:raise ValueError("duplicate protocol gate")
            expected=dict(profile="bismarck",handler_blob=ORIGINAL["handler"],dispatch_blob=ORIGINAL["dispatch"],
                 common_make_blob=ORIGINAL["common_make"],equipment_blob=ORIGINAL["equipment"],
                 gmsv_subtree_direct_callers="0",whole_server_pet_equip_definitions="1",
                 whole_server_pet_equip_direct_callers="1",protocol_recv_definitions="1",
                 default_dispatch_compiled="0",forced_dispatch_compiled="1",conditional_opcode_handler_present="1",
                 default_protocol_compiled="0",default_equipment_compiled="0",
                 forced_protocol_compiled="1",forced_equipment_compiled="1",
                 default_MI_recv_present="1",caller_under_positive_macro="1",
                 known_compiled_production_binary="0",natural_pet_item_path_proven="0",
                 early_original_build_proven="0")
            if set(a)!=set(expected)|{"site_sha256"} or any(a[k]!=v for k,v in expected.items()):
                raise ValueError("false status or cross-module call count")
            if not re.fullmatch(r"[0-9a-f]{64}",a["site_sha256"]):
                raise ValueError("bad site digest")
            summaries.append(a)
        elif s.startswith("SOURCE_PET_PROTOCOL_SITE|"):
            a=parse(s)
            if set(a)!={"symbol","path","line","definition"} or a["symbol"] not in SYMBOLS:
                raise ValueError("unrecognized protocol site")
            if not re.fullmatch(r"[\w./-]+\.c",a["path"]) or not a["line"].isdigit() or a["definition"] not in ("0","1"):
                raise ValueError("invalid source path/line/role")
            row=(a["symbol"],a["path"],int(a["line"]),int(a["definition"]))
            if row in sites:raise ValueError("duplicate protocol source row")
            sites.append(row)
    if len(summaries)!=1 or report.splitlines()[-1]!="RESOLUTION|PET_PROTOCOL_CROSS_MODULE_SOURCE_ONLY_PASS":
        raise ValueError("missing protocol acceptance boundary")
    required={
       ("CHAR_movePetItem","common/gmsv_server_recv.c",1010,0),
       ("CHAR_movePetItem","gmsv/char/char_item.c",2655,1),
       ("GmsvServer_PETITEM_recv","common/gmsv_server_recv.c",985,1),
       ("GmsvServer_PETITEM_recv","common/gmsv_server_send.c",1388,0)}
    if not required.issubset(sites):raise ValueError("cross-library guarded call chain missing")
    if len([x for x in sites if x[0]=="CHAR_movePetItem"])!=2:
        raise ValueError("original PET equipment calls beyond bounded witness")
    digest=hashlib.sha256()
    for x in sites:digest.update(("|".join(map(str,x))+"\n").encode())
    if digest.hexdigest()!=summaries[0]["site_sha256"]:
        raise ValueError("callsite digest mismatch")
    return summaries[0],sites

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--bismarck-dir",type=Path,required=True)
    args=parser.parse_args()
    rows=check(args.bismarck_dir)
    rows += [
      "BOUNDARY|Bismarck pinned late descendant, common opcode decoder->receive callback->equipment conditional -D_PET_ITEM original source chain; default GCC preprocessing disables all three; deployed binaries/client packet emission not verified",
      "OPEN|PET_ITEM deployed feature config; actual packet decoder registration/client emitted opcode; live item and pet owner/unique-code lifecycle; JSS1999/Taiwan1.0",
      "RESOLUTION|PET_PROTOCOL_CROSS_MODULE_SOURCE_ONLY_PASS",
    ]
    text="\n".join(rows)+"\n"
    validate_report(text)
    print(text,end="")

if __name__=="__main__":main()
