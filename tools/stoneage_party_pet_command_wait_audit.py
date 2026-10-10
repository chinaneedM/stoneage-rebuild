"""Execute original BATTLE_Command WAIT path through original BATTLE_Loop.

This is not a full combat round. All four actors keep their original command
status, and the original source must refrain from calling battle action/AI.
The latter functions remain fail-closed original-header adapters.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_party_pet_loop_dispatch_audit import code as original_loop
from tools.stoneage_party_pet_realheader_audit import patch_source
from tools.stoneage_player_battle_audit import domain as solo_domain,pinned_identity,PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen,loaded_oracle,eligible,pp_file
from tools.stoneage_guard_break2_source_audit import PINNED,LAYOUTS
from tools.stoneage_enemy_creation_audit import definition,trap_definitions

EXIT_ANCHOR="  int exit0=BATTLE_Exit(0,battle_at);"
ACTUAL_NAMES=("BATTLE_CommandWait","BATTLE_TimeOutCheck","BATTLE_Command")
NEW_UNREACHED=("BATTLE_ai_all","BATTLE_Battling","BATTLE_OnlyRescue",
               "BATTLE_MakeCharaString","BATTLE_BpSendToWatch",
               "CHAR_DischargePartyNoMsg","BATTLE_CommandSend")
WAIT_OBSERVATIONS=r"""
  /* This is one more tick in original BATTLE_MODE_BATTLE; no command
     has been submitted by the two players or the selected pet. */
  int previous_packets=init_packets,previous_settings=act_setting_packets;
  int previous_turn=battle->turn,previous_enemies=Battle_getTotalBattleNum();
  demand(previous_turn==0,"prewait turn zero");
  demand(slots[0].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"player0 ready for input");
  demand(slots[1].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"player1 ready for input");
  demand(slots[2].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,"pet2 ready for input");
  demand(battle->pNext==NULL,"controlled no watch arena");
  demand(BATTLE_Loop()==1,"original BATTLE_Loop BATTLE_Command dispatched");
  demand(battle->turn==previous_turn,"unsubmitted original Command must not advance turn");
  demand(battle->mode==BATTLE_MODE_BATTLE,"Command wait stays in BATTLE");
  demand(init_packets==previous_packets&&act_setting_packets==previous_settings,
         "Command wait must not reissue Init packets");
  demand(slots[0].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT &&
         slots[1].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT &&
         slots[2].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_C_WAIT,
         "Command wait must not alter actor modes");
  demand(slots[0].workint[CHAR_WORKBATTLEINDEX]==battle_at&&
         slots[1].workint[CHAR_WORKBATTLEINDEX]==battle_at&&
         slots[2].workint[CHAR_WORKBATTLEINDEX]==battle_at,
         "Command wait must preserve actor battle indexes");
  demand(Battle_getTotalBattleNum()==previous_enemies,"Command wait battle arena unchanged");
  demand(slots[0].data[CHAR_DEFAULTPET]==0&&CHAR_getCharPet(0,0)==2,"Command wait ownership unchanged");
  printf("\nREAL_HEADER_COMMAND_WAIT|mode=%d|battle=%d|turn=%d|leader_wait=1|member_wait=1|pet_wait=1|owner=2|retained=1\n",
      mode,battle_at,battle->turn);
"""

def extend_native(profile, source, battle, event, root):
    native,has_lua=original_loop(profile,source,battle,event)
    if native.count(EXIT_ANCHOR)!=1:
        raise ValueError("accepted exit injection anchor drift")
    for name in ACTUAL_NAMES:
        if name+"(" not in battle:
            raise ValueError("original command function missing "+name)
    if "BATTLE_CommandWait(" not in definition(battle,"BATTLE_Command") or \
       "BATTLE_TimeOutCheck(" not in definition(battle,"BATTLE_Command"):
        raise ValueError("source command wait/timeout call graph drift")
    if "BATTLE_Battling(" not in definition(battle,"BATTLE_Command"):
        raise ValueError("source combat action path lost; invalid negative gate")
    old=definition(native,"BATTLE_Command")
    if "UNREACHED_ORIGINAL_LOOP|BATTLE_Command" not in old:
        raise ValueError("accepted fail-closed Command stub drift")
    # Replace ONLY the previous synthetic unvisited Command stub. All
    # three original command functions are taken unmodified from pinned C.
    cmds="\n\n".join(definition(battle,n) for n in ACTUAL_NAMES)
    # The original full translation unit declared these before Command.
    # Restoring exact signatures here prevents C99 implicit extern calls
    # from conflicting with a later private static fail-closed definition.
    prototypes=(
        "int BATTLE_ai_all(int battleindex,int side,int turn);",
        "static int BATTLE_Battling(int battleindex);",
        "int BATTLE_OnlyRescue(int battleindex,int side,int *pOnlyFlg);",
    )
    native=native.replace(old,"\n".join(prototypes)+"\n"+cmds,1)
    body=WAIT_OBSERVATIONS
    native=native.replace(EXIT_ANCHOR,body+EXIT_ANCHOR,1)
    # Need every potential downstream original function in the
    # compiler/linker but never silently execute them: original wait
    # branch returns prior to AI/Battling/finish or timeout network path.
    # Original true C signatures from pinned battle_ai.h, battle.h,
    # battle_command.h, char.h and the private battle.c static declaration.
    # Do not infer signatures from function-call expressions.
    bounded={
        "BATTLE_ai_all": "int BATTLE_ai_all(int battleindex,int side,int turn)",
        "BATTLE_Battling": "static int BATTLE_Battling(int battleindex)",
        "BATTLE_OnlyRescue": "int BATTLE_OnlyRescue(int battleindex,int side,int *pOnlyFlg)",
        "BATTLE_MakeCharaString": "BOOL BATTLE_MakeCharaString(int battleindex,char *pszCommand,int size)",
        "BATTLE_BpSendToWatch": "void BATTLE_BpSendToWatch(BATTLE *pBattle,char *pszBcString)",
        "CHAR_DischargePartyNoMsg": "BOOL CHAR_DischargePartyNoMsg(int char_index)",
        "BATTLE_CommandSend": "BOOL BATTLE_CommandSend(int char_index,char *pszCommand)",
        "_BATTLE_CommandSend": "BOOL _BATTLE_CommandSend(int char_index,char *pszCommand,char *file,int line)",
    }
    required=[n for n in NEW_UNREACHED if n!="BATTLE_CommandSend"]+[
        "_BATTLE_CommandSend" if profile=="bismarck" else "BATTLE_CommandSend"
    ]
    for name in required:
        if re.search(r"(?m)^[^;\n{}]*\b"+re.escape(name)+r"\s*\([^;{}]*\)\s*\{",native):
            continue
        sig=bounded[name]
        native+="\n"+sig+'{fputs("UNREACHED_ORIGINAL_COMMAND|'+name+'\\n",stderr);abort();'+(
            "" if sig.startswith("void ") else "return 0;")+'}'+"\n"
    return native,has_lua

def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument("--"+p+"-dir",type=Path,required=True)
    args=parser.parse_args()
    roots={p:getattr(args,p+"_dir") for p in PINNED}
    for profile,root in roots.items():
        sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
        if sha!=PINNED[profile] or dirty:
            raise ValueError("pinned source drift "+profile)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if accepted["preserved_specimen"]!=receipt:raise ValueError("specimen drift")
    for profile in ("gavin","bismarck"):
        source,identity,*rest=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("accepted original source identity drift "+profile)
        source=patch_source(source,profile)
        if profile=="bismarck":
            previous='if(strncmp(stage,"BATTLE_Finish.",14))abort();netwatch_count++;'
            new='if(strncmp(stage,"BATTLE_Finish.",14)&&!( (strcmp(stage,"BATTLE_Init")==0||strcmp(stage,"BATTLE_Command")==0)&&value>=0&&value<3&&BattleArray[value].use))abort();netwatch_count++;'
            if source.count(previous)!=1:
                raise ValueError("Bismarck monitor collector anchor drift")
            source=source.replace(previous,new,1)
        battle=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c")
        event=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle_event.c")
        source+="\n"+definition(battle,"BATTLE_Index2No")+"\n"
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        templates,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        selected=eligible(loader,templates,enemies,rest[-1])[0]
        native,has_lua=extend_native(profile,source,battle,event,roots[profile])
        traps=[x for x in accepted["profiles"][profile]["unreachable_traps"] if x not in
               ("BATTLE_Index2No","RIDEPET_getPETindex","CHAR_sendCToArroundCharacter","CHAR_send_K_StatusString")]
        runs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-actual-command-wait-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                compile_probe(profile,roots[profile],native,exe,opt,traps)
                execute=subprocess.run([str(exe),*map(str,paths)],
                                     input="".join(f"{selected} {mode}\n" for mode in range(4)),
                                     capture_output=True,text=True)
                if execute.returncode or any(not l.startswith("TRACE|") for l in execute.stderr.splitlines() if l.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",execute.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                           capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("native CommandWait "+profile+" "+opt+
                                     " code="+str(execute.returncode)+" stderr="+execute.stderr[-4400:]+
                                     " symbols="+symbols+" stdout="+execute.stdout[-1500:])
                waits=[x for x in execute.stdout.splitlines() if x.startswith("REAL_HEADER_COMMAND_WAIT|")]
                if len(waits)!=4 or execute.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("missing four real CommandWait/Exit cycles")
                for mode,row in enumerate(waits):
                    if f"|mode={mode}|battle={mode%3}|turn=0|" not in row:
                        raise ValueError("battle cursor/turn drift "+row)
                runs.append(execute.stdout)
        if runs[0]!=runs[1]:
            raise ValueError("original CommandWait trace O0/O2 divergence "+profile)
        print(f"PROFILE|{profile}|actual_wait_dispatches_per_optimization=4|optimizations=O0,O2|sha256={hashlib.sha256(runs[0].encode()).hexdigest()}",flush=True)
        for row in runs[0].splitlines():
            if row.startswith("REAL_HEADER_COMMAND_WAIT|"):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|original_BATTLE_Loop_to_original_Command_to_CommandWait_TimeOutCheck_wait_only_no_AI_no_Battling",flush=True)
    print("OPEN|actual_submitted_attack_enemy_decision_round_completion_BATTLE_Finish_profit_network_Lua",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_COMMAND_WAIT_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
