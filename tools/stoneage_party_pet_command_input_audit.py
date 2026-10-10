"""Full original command parser on real-header populated party/pet arenas.
Only admission/readiness is accepted: no AI/action or completed round.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from tools.stoneage_party_pet_command_wait_audit import (
    extend_native, EXIT_ANCHOR, patch_source, solo_domain, pinned_identity,
    PIN_PATH, compile_probe, specimen, loaded_oracle, eligible, pp_file,
    PINNED, LAYOUTS, definition,
)
ACTUAL_NAMES=("BattleCommandDispach","checkErrorStatus","BATTLE_MpDown","BATTLE_PetDefaultCommand")
INPUT_OBSERVATIONS=r"""
  int before_settings=act_setting_packets,before_recv=recv_count;
  Char input_before[7];memcpy(input_before,slots,sizeof input_before);
  BATTLE input_arena=*battle;
  BattleCommandDispach(-1,"H|F");
  BattleCommandDispach(9,"H|F");
  demand(!memcmp(input_before,slots,sizeof input_before)&&!memcmp(&input_arena,battle,sizeof(BATTLE)),"invalid descriptor and pet-as-player rejected");
  demand(act_setting_packets==before_settings&&recv_count==before_recv,"invalid source early returns have no output");
  BattleCommandDispach(7,"?");
  demand(!memcmp(input_before,slots,sizeof input_before)&&!memcmp(&input_arena,battle,sizeof(BATTLE)),"unknown command leaves complete actors and arena unchanged");
  demand(act_setting_packets==before_settings+1&&recv_count==before_recv,"unknown command status-only acknowledgement");
  int packet_target=mode==0?15:-1;
  char *leader_packet=mode==0?"H|F":mode==1?"H|oops":mode==2?"H|14":"G";
  Char expected_leader=slots[0];
  expected_leader.workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
  expected_leader.workint[CHAR_WORKBATTLECOM1]=mode==3?BATTLE_COM_GUARD:BATTLE_COM_ATTACK;
  if(mode!=3){
    expected_leader.workint[CHAR_WORKBATTLECOM2]=packet_target;
    expected_leader.workint[CHAR_WORKBATTLECOM3]=(expected_leader.workint[CHAR_WORKBATTLECOM3]&0xFFFF0000)|1;
  }
  BattleCommandDispach(7,leader_packet);
  demand(!memcmp(&expected_leader,&slots[0],sizeof(Char)),"full original leader command delta");
  demand(!memcmp(&input_before[1],&slots[1],sizeof(Char))&&!memcmp(&input_before[2],&slots[2],sizeof(Char)),"leader command does not prepare teammate or pet");
  demand(!memcmp(&input_arena,battle,sizeof(BATTLE)),"input at turn zero retains arena and freeDP");
  demand(act_setting_packets==before_settings+2,"leader command output-only collector");
  Char submitted_before[7];memcpy(submitted_before,slots,sizeof submitted_before);
  BATTLE partial_expected=*battle;
  /* SOURCE_PROFILE_PARTIAL_DELTA */
  demand(BATTLE_Loop()==1,"partial leader ready original dispatch");
  demand(battle->turn==0&&!memcmp(&partial_expected,battle,sizeof(BATTLE)),"partial ready must not increment turn");
  demand(!memcmp(submitted_before,slots,sizeof submitted_before),"waiting for member/pet preserves all seven actor slots");
  demand(BATTLE_PetDefaultCommand(-1)==FALSE,"invalid original default-pet command rejected");
  demand(!memcmp(submitted_before,slots,sizeof submitted_before),"invalid default pet unchanged");
  Char expected_pet=slots[2];
  expected_pet.workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_ATTACK;
  expected_pet.workint[CHAR_WORKBATTLECOM2]=-1;
  expected_pet.workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
  demand(BATTLE_PetDefaultCommand(2)==TRUE,"original pet default command");
  demand(!memcmp(&expected_pet,&slots[2],sizeof(Char)),"complete original pet default command delta");
  memcpy(submitted_before,slots,sizeof submitted_before);
  demand(BATTLE_Loop()==1&&battle->turn==0,"leader plus pet still waits for teammate");
  demand(!memcmp(&partial_expected,battle,sizeof(BATTLE))&&!memcmp(submitted_before,slots,sizeof submitted_before),"second partial readiness has no arena/actor changes");
  Char expected_member=slots[1];
  expected_member.workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_GUARD;
  expected_member.workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
  BattleCommandDispach(8,"G");
  demand(!memcmp(&expected_member,&slots[1],sizeof(Char)),"complete original teammate guard delta");
  memcpy(submitted_before,slots,sizeof submitted_before);
  BattleCommandDispach(7,"W|FFFF");
  demand(!memcmp(submitted_before,slots,sizeof submitted_before),"invalid pet skill range retains prepared pet intent");
  demand(act_setting_packets==before_settings+4,"exact four status acknowledgements");
  demand(recv_count==before_recv+INPUT_RECV_DELTA,"exact source-profile receive-time notifications");
  demand(BATTLE_CommandWait(battle_at,0)==TRUE&&BATTLE_CommandWait(battle_at,1)==TRUE,"original full allied and enemy-side readiness predicates");
  demand(BATTLE_TimeOutCheck(battle_at)==FALSE,"prepared input remains below timeout");
  demand(battle->turn==0&&battle->mode==BATTLE_MODE_BATTLE,"ready predicate does not execute a round");
  demand(CHAR_getCharPet(0,0)==2&&slots[0].data[CHAR_DEFAULTPET]==0,"prepared selected owned pet retained");
  printf("\nREAL_HEADER_COMMAND_INPUT|mode=%d|battle=%d|turn=0|leader=%s|target=%d|member_guard=1|pet_default_attack=1|partial_waits=2|allied_ready=1|unknown_ack=1|invalid_rejected=1|settings_delta=4|recv_delta=%d|round_executed=0\n",mode,battle_at,mode==3?"guard":"attack",mode==3?expected_leader.workint[CHAR_WORKBATTLECOM2]:packet_target,recv_count-before_recv);
"""

def input_native(profile,source,battle,event,root):
    native,has_lua=extend_native(profile,source,battle,event,root)
    # Original pet_skill.h must precede pet_skillinfo.h numeric macros.
    native='#include "version.h"\n#include "pet_skill.h"\n'+native
    command=pp_file(profile,root,LAYOUTS[profile]/"battle/battle_command.c")
    bodies={name:definition(command,name) for name in ACTUAL_NAMES}
    if "BATTLE_ActSettingSend(" not in bodies["BattleCommandDispach"]:
        raise ValueError("original dispatch acknowledgement graph drift")
    anchor="int main(int argc,char **argv){"
    if native.count(anchor)!=1 or native.count(EXIT_ANCHOR)!=1:
        raise ValueError("accepted original command-input injection drift")
    # Explicit synthetic descriptor-to-actor map. The inherited original
    # player fixture still has WORKFD7 for both players; this is not transport.
    extra='#include "battle_command.h"\n#include "magic.h"\n#include "magic_base.h"\n'
    extra+='int BATTLE_MpDown(int,int);int checkErrorStatus(int);int NowBattlerFd;\nint CONNECT_getCharaindex(int fd){if(fd==-1)return -1;if(fd>=7&&fd<=9)return fd-7;abort();}\n'
    char_base=pp_file(profile,root,LAYOUTS[profile]/"char/char_base.c")
    char_main=pp_file(profile,root,LAYOUTS[profile]/"char/char.c")
    extra+='\n'.join(definition(char_base,n) for n in ("CHAR_CHECKCHARDATAINDEX","_CHAR_getChar"))+'\n'
    extra+=definition(char_main,"CHAR_getUseName")+'\n'
    extra+='\n'.join(bodies.values())+'\n' 
    native=native.replace(anchor,extra+anchor,1)
    observation=INPUT_OBSERVATIONS.replace("INPUT_RECV_DELTA","3" if profile=="gavin" else "0")
    delta='partial_expected.PartTime=1120;' if profile=="gavin" else ''
    observation=observation.replace("/* SOURCE_PROFILE_PARTIAL_DELTA */",delta)
    native=native.replace(EXIT_ANCHOR,observation+EXIT_ANCHOR,1)
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
        native,has_lua=input_native(profile,source,battle,event,roots[profile])
        traps=None
        runs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-actual-command-input-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                traps=compile_probe(profile,roots[profile],native,exe,opt,None if opt=="-O0" else traps)
                execute=subprocess.run([str(exe),*map(str,paths)],
                                     input="".join(f"{selected} {mode}\n" for mode in range(4)),
                                     capture_output=True,text=True)
                if execute.returncode or any(not l.startswith("TRACE|") for l in execute.stderr.splitlines() if l.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",execute.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                           capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("native command input "+profile+" "+opt+
                                     " code="+str(execute.returncode)+" stderr="+execute.stderr[-4400:]+
                                     " symbols="+symbols+" stdout="+execute.stdout[-1500:])
                waits=[x for x in execute.stdout.splitlines() if x.startswith("REAL_HEADER_COMMAND_INPUT|")]
                if len(waits)!=4 or execute.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("missing four real command-input/Exit cycles")
                for mode,row in enumerate(waits):
                    if f"|mode={mode}|battle={mode%3}|turn=0|" not in row:
                        raise ValueError("battle cursor/turn drift "+row)
                runs.append(execute.stdout)
        if runs[0]!=runs[1]:
            raise ValueError("original command-input trace O0/O2 divergence "+profile)
        print(f"PROFILE|{profile}|input_dispatches_per_optimization=24|encounters_per_optimization=4|optimizations=O0,O2|sha256={hashlib.sha256(runs[0].encode()).hexdigest()}",flush=True)
        original_path=roots[profile]/LAYOUTS[profile]/"battle/battle_command.c"
        command=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle_command.c")
        print(f"PROVENANCE|{profile}|commit={PINNED[profile]}|command_file_sha256={hashlib.sha256(original_path.read_bytes()).hexdigest()}",flush=True)
        for name in ACTUAL_NAMES:
            print(f"ORIGINAL_FUNCTION|{profile}|{name}|preprocessed_body_sha256={hashlib.sha256(definition(command,name).encode()).hexdigest()}",flush=True)
        for row in runs[0].splitlines():
            if row.startswith("REAL_HEADER_COMMAND_INPUT|"):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|original_command_parser_full_body;prepared_allied_readiness_only;enemy_AI_Battling_not_executed",flush=True)
    print("OPEN|enemy_decision_actual_action_round_completion_BATTLE_Finish_profit_network_Lua",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_COMMAND_INPUT_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
