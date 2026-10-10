"""Original-body real-header battle Init after accepted populated party/pet entry.

No original source/header/master bytes are committed. The input driver is
synthetic and two packet emitters are bounded: not original transport.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from tools.stoneage_party_pet_full_exit_audit import make_reentry_native
from tools.stoneage_party_pet_realheader_audit import patch_source
from tools.stoneage_player_battle_audit import domain as solo_domain, pinned_identity, PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen, loaded_oracle, eligible, pp_file
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS
from tools.stoneage_enemy_creation_audit import definition

ACTUAL_FUNCTIONS = (
    "BATTLE_SurpriseCheck", "BATTLE_IsCharge", "BATTLE_AllCharaCWaitSet",
    "BATTLE_CharaBackUp", "BATTLE_TurnParam", "BATTLE_AttReverse",
    "BATTLE_PreCommandSeq", "BATTLE_Init",
)
ENTRY_ANCHOR = "  int exit0=BATTLE_Exit(0,battle_at);"
INIT_OBSERVATIONS = r"""
  demand(battle->mode==BATTLE_MODE_INIT,"original initial arena mode");
  demand(BATTLE_Init(battle_at)==0,"original BATTLE_Init return");
  demand(battle->mode==BATTLE_MODE_BATTLE,"original Init state advance");
  demand(battle->timer==NowTime.tv_sec,"original command timestamp");
  demand((battle->flg&BATTLE_FLG_FREEDP)!=0,"original free DP flag");
  demand(battle->iEntryBack[0]==0&&battle->iEntryBack2[0]==0,"original leader backup");
  demand(battle->iEntryBack[1]==1&&battle->iEntryBack2[1]==1,"original member backup");
  demand(slots[0].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"original leader C_WAIT");
  demand(slots[1].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"original member C_WAIT");
  demand(slots[2].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"original pet C_WAIT");
  demand(battle->Side[0].Entry[0].ENTRY_FIELD==0&&
         battle->Side[0].Entry[1].ENTRY_FIELD==1&&
         battle->Side[0].Entry[5].ENTRY_FIELD==2,"original Init actors unchanged");
  demand(init_packets==1&&act_setting_packets==1,"bounded original Init packet calls");
  demand(CHAR_getCharPet(0,0)==2&&slots[0].data[CHAR_DEFAULTPET]==0,"original Init owner");
  printf("\nREAL_HEADER_INIT|mode=%d|battle=%d|initialized=1|leader_wait=1|member_wait=1|pet_wait=1|backups=0,1|packet_calls=%d,%d|lua_boundary=%d\n",
    mode,battle_at,init_packets,act_setting_packets,lua_start_calls);
"""
# Preserve original function bodies with real headers; only the two outbound
# packet-generation APIs are explicitly bounded. Their actual payload
# assembly and transport are NOT tested.
OUTPUT_BOUNDARY = r"""
static int init_packets=0,act_setting_packets=0,lua_start_calls=0;
void BATTLE_CharSendAll(int battleindex){
  if(battleindex<0||battleindex>=3||!BattleArray[battleindex].use)abort();
  init_packets++;
}
void BATTLE_ActSettingSend(int battleindex){
  if(battleindex<0||battleindex>=3||!BattleArray[battleindex].use)abort();
  act_setting_packets++;
}
"""
LUA_BOUNDARY = r"""
BOOL BattleStartFunction(int battleindex){
  if(battleindex<0||battleindex>=3||!BattleArray[battleindex].use)abort();
  lua_start_calls++;
  return TRUE;
}
"""

def make_native(profile, source, battle_file, event_file):
    base=make_reentry_native(profile,source)
    added={}
    for name in ACTUAL_FUNCTIONS:
        original=event_file if name=="BATTLE_SurpriseCheck" else battle_file
        part=definition(original,name)
        if not re.search(r"\b"+name+r"\s*\(",part):
            raise ValueError("extracted original body missing "+name)
        added[name]=part
    if "BATTLE_PreCommandSeq" not in added["BATTLE_Init"] or "BATTLE_SurpriseCheck" not in added["BATTLE_Init"]:
        raise ValueError("original Init internal call graph drift")
    if not all(k in added["BATTLE_PreCommandSeq"] for k in
               ("BATTLE_CharSendAll(", "BATTLE_CharaBackUp(",
                "BATTLE_AllCharaCWaitSet(", "BATTLE_ActSettingSend(")):
        raise ValueError("original command preparation graph drift")
    has_lua="BattleStartFunction(" in added["BATTLE_Init"]
    if profile=="gavin" and has_lua:raise ValueError("unexpected original Gavin Lua callback")
    if base.count(ENTRY_ANCHOR)!=1:raise ValueError("previous original Exit anchor drift")
    body=INIT_OBSERVATIONS.replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")
    # Reset output-observation counters per controlled encounter, rather
    # than silently treating the repeated four-fight driver as one battle.
    code=base.replace(ENTRY_ANCHOR,body+ENTRY_ANCHOR,1)
    mark="  born=0;rng_mode=mode;clock_count=netwatch_count=0;"
    if code.count(mark)!=1:raise ValueError("accepted per-fight reset drift")
    code=code.replace(mark,mark+"\n  init_packets=act_setting_packets=lua_start_calls=0;",1)
    anchor="int main(int argc,char **argv){"
    if code.count(anchor)!=1:raise ValueError("main source anchor drift")
    extra=OUTPUT_BOUNDARY
    if has_lua:extra+=LUA_BOUNDARY
    extra+="\n"+"\n".join(added.values())+"\n"
    return code.replace(anchor,extra+anchor,1),has_lua

def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument("--"+p+"-dir",type=Path,required=True)
    args=parser.parse_args()
    roots={p:getattr(args,p+"_dir") for p in PINNED}
    for profile,path in roots.items():
        sha=subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(path),"status","--porcelain"],text=True).strip()
        if sha!=PINNED[profile] or dirty:
            raise ValueError("pinned source drift or dirty "+profile)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if accepted["preserved_specimen"]!=receipt:
        raise ValueError("accepted master source drift")
    for profile in ("gavin","bismarck"):
        source,identity,*remainder=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("accepted source identity drift "+profile)
        source=patch_source(source,profile)
        original_battle=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c")
        original_event=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle_event.c")
        source+="\n"+definition(original_battle,"BATTLE_Index2No")+"\n"
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        templates,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        selected=eligible(loader,templates,enemies,remainder[-1])[0]
        native,has_lua=make_native(profile,source,original_battle,original_event)
        traps=[x for x in accepted["profiles"][profile]["unreachable_traps"] if x not in
               ("BATTLE_Index2No","RIDEPET_getPETindex","CHAR_sendCToArroundCharacter","CHAR_send_K_StatusString")]
        observations=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-realheader-init-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                compile_probe(profile,roots[profile],native,exe,opt,traps)
                run=subprocess.run([str(exe),*map(str,paths)],
                                   input="".join(f"{selected} {i}\n" for i in range(4)),
                                   capture_output=True,text=True)
                if run.returncode or any(not l.startswith("TRACE|") for l in run.stderr.splitlines() if l.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",run.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                            capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("original Init "+profile+" "+opt+" rc="+str(run.returncode)+
                                     " stderr="+run.stderr[-5000:]+" symbols="+symbols+
                                     " stdout="+run.stdout[-1200:])
                lines=[l for l in run.stdout.splitlines() if l.startswith("REAL_HEADER_INIT|")]
                if len(lines)!=4:
                    raise ValueError("original Init missing 4 events "+profile+" rows="+str(len(lines))+
                                     " stdout="+run.stdout[-3000:])
                for i,line in enumerate(lines):
                    if f"|mode={i}|battle={i%3}|initialized=1|" not in line:
                        raise ValueError("original Init battle cursor drift "+profile+":"+str(i))
                    if "|packet_calls=1,1|" not in line:
                        raise ValueError("original Init bounded network call delta drift")
                    if "|lua_boundary="+("1" if has_lua else "0") not in line:
                        raise ValueError("Lua branch expected boundary call drift")
                if run.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("accepted original Exit closure lost")
                observations.append(run.stdout)
        if observations[0]!=observations[1]:
            raise ValueError("native original Init O0/O2 trace drift "+profile)
        print(f"PROFILE|{profile}|actual_original_init=4|optimizations=O0,O2|lua_boundary={int(has_lua)}|sha256={hashlib.sha256(observations[0].encode()).hexdigest()}",flush=True)
        for l in observations[0].splitlines():
            if l.startswith("REAL_HEADER_INIT|"):print("ACTUAL|"+profile+"|"+l,flush=True)
    print("BOUNDARY|original_Init_Surprise_PreCommand_CharaBackup_IsCharge_CWait_TurnParam_AttReverse_2_bounded_outbound_packet_sinks_Lua_callback_when_enabled",flush=True)
    print("OPEN|actual_BATTLE_Loop_Command_Finish_network_payload_Lua_runtime_true_rounds_profit_original_JSS_TW_binary",flush=True)
    print("RESOLUTION|ORIGINAL_PARTY_PET_REALHEADER_INIT_PRECOMMAND_BOUNDED_PASS_NO_PROFIT_PROMOTION",flush=True)

if __name__=="__main__":
    main()
