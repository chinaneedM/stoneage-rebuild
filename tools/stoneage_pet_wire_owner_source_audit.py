"""Pinned later-descendant optional PET packet/slot/unique-code source-chain gate.

This checks guarded source semantics, not compiled/deployed runtime reachability.
No original source or proprietary asset is placed in the rebuilt repository.
"""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess

ORIGINAL_REPO="BismarckDD/Stoneage"
COMMIT="999ffdf1d220ec6666eb65339180689c9caf1876"
PIN={
 "client/stoneage/system/menu.cpp":"62754fdd0db1b84c358d61418d253012d149e1d4",
 "client/stoneage/proto/protocol.cpp":"17f1900d8845c15308a4b429905ec009e5fd4c0f",
 "client/stoneage/proto/protocol.h":"bb70087ef1b1915748da23935584eda2c8178cb0",
 "server/common/gmsv_server.h":"708fe1b9f73be4952677fda474f10e86d9a56306",
 "server/common/gmsv_server_send.c":"84dd1b2d9fbac10fe39983e6b8984aaebf1b3075",
 "server/common/gmsv_server_recv.c":"088db5e38a1bc0dd47b3c3120480af93ab24c4c7",
 "server/gmsv/char/char_item.c":"970b7b3f975965c6c5e77352a2e0382adf943753",
 "server/gmsv/char/char_base.c":"5f646eba671b39f5e90f53e3a95cbcc70ff56975",
 "server/gmsv/include/version.h":"b3fc0c80705973bc8d088287c98a5d66171bb6c2",
}
MARK="RESOLUTION|PET_WIRE_OWNER_SOURCE_BOUNDARY_PASS"

def demand(value, msg):
    if not value: raise ValueError(msg)

def read_pinned(root):
    def git(*args):return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()
    demand(git("rev-parse","HEAD")==COMMIT,"original checkout commit drift")
    out={}
    for path,sha in PIN.items():
        demand(git("hash-object",path)==sha,"original file blob changed: "+path)
        out[path]=(root/path).read_text(encoding="utf-8-sig",errors="replace")
    return out

def segment(txt,beg,end):
    x=txt.find(beg)
    demand(x>=0,"missing start "+beg)
    y=txt.find(end,x+len(beg))
    demand(y>=0,"missing terminator "+end)
    return txt[x:y]

def requires_order(txt,tokens,name):
    prev=-1
    for token in tokens:
        at=txt.find(token,prev+1)
        demand(at>prev,name+" missing or reordered "+token)
        prev=at

def check(root):
    data=read_pinned(root)
    ui=data["client/stoneage/system/menu.cpp"]
    client=segment(data["client/stoneage/proto/protocol.cpp"],
                   "void lssproto_PetItemEquip_send(","#endif")
    decoder=segment(data["server/common/gmsv_server_send.c"],
                    "if (func == LSSPROTO_PET_ITEM_RECV)", "#endif\n#ifdef _ASSESS_ABILITY")
    recv=segment(data["server/common/gmsv_server_recv.c"],
                 "void GmsvServer_PETITEM_recv(","void GmsvServer_SKUP_recv(")
    move=segment(data["server/gmsv/char/char_item.c"],
                 "void CHAR_movePetItem(","void CHAR_sendPetItemEmpty(")
    setter=segment(data["server/gmsv/char/char_base.c"],
                   "INLINE int _CHAR_setItemIndex(","INLINE int _CHAR_getPoolItemIndex(")
    unique=segment(data["server/gmsv/char/char_base.c"],
                   "void ITEM_setItemUniCode(","void CHAR_DetainSameItem(")
    h=data["client/stoneage/proto/protocol.h"]
    sh=data["server/common/gmsv_server.h"]
    # The wire is exactly five ordered integers and the additive checksum.
    requires_order(client,[
        "util_mkint(szBuffer, iGx)","util_mkint(szBuffer, iGy)",
        "util_mkint(szBuffer, iPetNo)","util_mkint(szBuffer, iItemNo)",
        "util_mkint(szBuffer, iDestNO)","util_mkint(szBuffer, iChecksum)",
        "util_SendMesg(fd, LSSPROTO_PET_ITEM_EQUIP_SEND, szBuffer)"],"client PET serializer")
    requires_order(decoder,[
        "util_deint(2, &x)","util_deint(3, &y)","util_deint(4, &petindex)",
        "util_deint(5, &fromindex)","util_deint(6, &toindex)",
        "util_deint(7, &check_sum_recv)","if (check_sum_calc != check_sum_recv)",
        "GmsvServer_PETITEM_recv(fd, x, y, petindex, fromindex, toindex)"],"server PET decoder")
    demand("#define LSSPROTO_PET_ITEM_EQUIP_SEND 127" in h and
           "#define LSSPROTO_PET_ITEM_RECV 127" in sh,
           "client/server conditional PET opcode changed")
    requires_order(recv,[
        "CHECKFDANDTIME;","CONNECT_getCharaindex(fd)",
        "CHAR_getWorkInt(char_index, CHAR_WORKTRADEMODE) != CHAR_TRADE_FREE",
        "CHAR_getWorkInt(char_index, CHAR_WORKBATTLEMODE) != BATTLE_CHARMODE_NONE",
        "CHAR_movePetItem(char_index, petindex, fromindex, toindex)"],"server authenticated callback")
    demand("CHAR_getCharPet(char_index, petid)" in move and
           "if (!CHAR_CHECKINDEX(char_index))" in move and
           "CHAR_getFlg(char_index, CHAR_ISDIE)" in move,
           "PET actor resolution / player checks absent")
    # Special -1 is an automatic PET target slot; -2 is a distinct drop path.
    demand("toindex == -1" in move and "ITEM_PET_HEAD" in move
           and "toindex == -2" in move and "CHAR_DropItem(char_index, fromindex)" in move
           and "CHAR_getInt(petindex, CHAR_VARIABLEAI) < 100" in move
           and "ITEM_getInt(charitem_index, ITEM_LEVEL)" in move,
           "PET move modes or rule guards changed")
    # Physical item indices swap across *two* actor slot arrays.
    swaps=[
        "CHAR_setItemIndex(char_index, fromindex, petitem_index)",
        "CHAR_setItemIndex(petindex, toindex, charitem_index)",
        "CHAR_setItemIndex(char_index, toindex, petitem_index)",
        "CHAR_setItemIndex(petindex, fromindex, charitem_index)",
    ]
    demand(all(token in move for token in swaps),"PET slot index swap bodies changed")
    demand(move.count("CHAR_sendPetItemData(char_index, petid)") == 2 and
           move.count("CHAR_sendItemDataOne(char_index,") == 2 and
           "CHAR_complianceParameter(petindex)" in move,
           "PET item update and compliance functions changed")
    demand("CHAR_chara[index].indexOfExistItems[iindex] = id" in setter and
           "#ifdef _UNIQUE_P_I" in setter and
           "ITEM_setItemUniCode(id)" in setter,
           "actor slot setter unique-code hook changed")
    demand('strcmp(ITEM_getChar(item_index, ITEM_UNIQUECODE), "") == 0' in unique and
           'strstr(ITEM_getChar(item_index, ITEM_UNIQUECODE), "_") != NULL' in unique and
           "ITEM_setChar(item_index, ITEM_UNIQUECODE, itembuf)" in unique,
           "unique-code conditional regeneration gate changed")
    # Exact late source UI caller positions and synthetic protocol mode source.
    lines=ui.splitlines()
    for line,mode in [(14824,", mouse.itemNo, i)"),(14966,", i, -1)"),(15333,", mouse.itemNo, -2)")]:
        demand("lssproto_PetItemEquip_send" in lines[line-1] and mode in lines[line-1],
               "client UI send index/mode changed "+str(line))
    # Derive evidence from version-pinned source bodies; hashes allow change detection
    # while retaining only source-free metadata.
    hashes={name:hashlib.sha256(s.encode("utf-8")).hexdigest() for name,s in
            [("client_serializer",client),("server_decoder",decoder),
             ("server_callback",recv),("native_swap",move),
             ("slot_setter",setter),("unique_hook",unique)]}
    row={
      "source_commit":COMMIT,
      "source_blobs":str(len(PIN)),
      "wire_integer_fields":"5",
      "client_server_opcode":"127",
      "decoder_checksum_guard":"1",
      "authenticated_connection_gate":"1",
      "trade_and_battle_restrictions":"1",
      "menu_source_calls":"3",
      "native_actor_slot_index_swaps":"4",
      "native_slot_setter_unique_hook":"1",
      "conditional_unique_code_regenerator":"1",
      "effective_real_pair_verified":"0",
      "emitted_live_packet_verified":"0",
      "native_owner_lifecycle_executed":"0",
      "early_version_verified":"0",
    }
    receipt=["SOURCE_PET_WIRE_OWNER_GATE|"+"|".join(f"{k}={v}" for k,v in row.items())]
    receipt += [f"SOURCE_PET_CHAIN_BODY|name={name}|sha256={digest}"
                for name,digest in hashes.items()]
    receipt += [
        "BOUNDARY|Late pinned source-only optional PET wire-order and actor-slot-index changes; no deployed binary, live packet, item owner/unique-code runtime claim or JSS1999/Taiwan1.0 promotion",
        "OPEN|Build-compatible enabled client/server pair; runtime opcode127 dispatch; natural PET item ownership and persistent unique-code before/after move",
        MARK]
    return receipt

def fields(s):
    pairs=[x.split("=",1) for x in s.split("|")[1:]]
    if not pairs or any(len(x)!=2 for x in pairs) or len(pairs)!=len(dict(pairs)):
        raise ValueError("malformed/duplicated evidence field")
    return dict(pairs)

def validate_report(report):
    lines=report.splitlines()
    demand(len(lines)==10 and lines[0].startswith("SOURCE_PET_WIRE_OWNER_GATE|")
           and lines[-1]==MARK,"missing source gate/report records")
    gate=fields(lines[0])
    expected={
      "source_commit":COMMIT,"source_blobs":"9","wire_integer_fields":"5",
      "client_server_opcode":"127","decoder_checksum_guard":"1",
      "authenticated_connection_gate":"1","trade_and_battle_restrictions":"1",
      "menu_source_calls":"3","native_actor_slot_index_swaps":"4",
      "native_slot_setter_unique_hook":"1","conditional_unique_code_regenerator":"1",
      "effective_real_pair_verified":"0","emitted_live_packet_verified":"0",
      "native_owner_lifecycle_executed":"0","early_version_verified":"0",
    }
    demand(gate==expected,"false source or executable reachability claim")
    names=["client_serializer","server_decoder","server_callback","native_swap",
           "slot_setter","unique_hook"]
    for idx,name in enumerate(names,1):
        demand(lines[idx].startswith("SOURCE_PET_CHAIN_BODY|"),"missing hashed source body")
        d=fields(lines[idx])
        demand(set(d)=={"name","sha256"} and d["name"]==name and
               bool(re.fullmatch(r"[0-9a-f]{64}",d["sha256"])),
               "bad source body fingerprint")
    demand(lines[7].startswith("BOUNDARY|") and "source-only" in lines[7] and
           "no deployed binary" in lines[7] and "JSS1999/Taiwan1.0" in lines[7]
           and lines[8].startswith("OPEN|"),"source-only OPEN boundary missing")
    return gate

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--checkout",type=Path,required=True)
    args=ap.parse_args()
    result="\n".join(check(args.checkout))+"\n"
    validate_report(result)
    print(result,end="")
if __name__=="__main__":main()
