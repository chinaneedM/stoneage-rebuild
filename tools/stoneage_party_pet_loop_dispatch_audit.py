"""Original BATTLE_Loop INIT dispatcher exercised over a populated party/pet arena.

Exactly one existing INIT arena is live per loop call. Other dispatch modes
remain hard traps. Original full round/finish/watch logic is NOT executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_party_pet_init_audit import make_native as init_native
from tools.stoneage_party_pet_realheader_audit import patch_source
from tools.stoneage_player_battle_audit import domain as solo_domain,pinned_identity,PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen,loaded_oracle,eligible,pp_file
from tools.stoneage_guard_break2_source_audit import PINNED,LAYOUTS
from tools.stoneage_enemy_creation_audit import definition

DIRECT_INIT="demand(BATTLE_Init(battle_at)==0,\"original BATTLE_Init return\");"
LOOP_INIT="demand(BATTLE_Loop()==1,\"original BATTLE_Loop single arena INIT dispatch\");"
# All branches other than INIT are deliberately unaccepted and must abort
# rather than appear to have undergone a real combat round or Finish.
UNREACHED = ("BATTLE_Command","BATTLE_Finish","BATTLE_Stop",
             "BATTLE_WatchBC","BATTLE_WatchPre","BATTLE_WatchWait",
             "BATTLE_WatchMovie","BATTLE_WatchAfter",
             "BATTLE_CountAlive","BATTLE_FinishSet")
def code(profile, source, battle, event):
    native,has_lua=init_native(profile,source,battle,event)
    if native.count(DIRECT_INIT)!=1:
        raise ValueError("accepted original Init call drift")
    native=native.replace(DIRECT_INIT,LOOP_INIT,1)
    actual=definition(battle,"BATTLE_Loop")
    if "BATTLE_Init(" not in actual or "BATTLE_Command(" not in actual or "BATTLE_Finish(" not in actual:
        raise ValueError("original battle dispatcher mode table drift")
    if "BATTLE_MODE_INIT" not in actual or "BATTLE_MODE_BATTLE" not in actual:
        raise ValueError("original native dispatcher state tags drift")
    if "BATTLE_battlenum" not in actual or "cnt ++" not in actual.replace("cnt++","cnt ++"):
        raise ValueError("original battle arena traversal drift")
    guards=[]
    for name in UNREACHED:
        # Do not replace any original previously accepted concrete functions
        # or their forward declarations. A future duplicate is a hard gate
        # failure and must be explicitly audited instead of being concealed.
        if re.search(r"(?m)^\s*(?:static\s+)?(?:int|BOOL)\s+"+name+r"\s*\(",native):
            # Some predecessor source bundles already include the original
            # function. Do not shadow it; the INIT-only mode oracle must
            # ensure it is never dispatched.
            continue
        guards.append(f"static int {name}(int battleindex"+(",int side" if name=="BATTLE_CountAlive" else "")+")"+
                      '{(void)battleindex;'+("(void)side;" if name=="BATTLE_CountAlive" else "")+
                      f'fputs("UNREACHED_ORIGINAL_LOOP|{name}\\n",stderr);abort();return -1;'+"}")
    anchor="int main(int argc,char **argv){"
    if native.count(anchor)!=1:
        raise ValueError("driver main anchor drift")
    native=native.replace(anchor,"\n".join(guards)+"\n"+actual+"\n"+anchor,1)
    return native,has_lua

def main():
    ap=argparse.ArgumentParser()
    for p in PINNED:ap.add_argument("--"+p+"-dir",type=Path,required=True)
    args=ap.parse_args();roots={p:getattr(args,p+"_dir") for p in PINNED}
    for profile,path in roots.items():
        head=subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(path),"status","--porcelain"],text=True).strip()
        if head!=PINNED[profile] or dirty:raise ValueError("source pin drift "+profile)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if accepted["preserved_specimen"]!=receipt:raise ValueError("original specimen drift")
    for profile in ("gavin","bismarck"):
        source,identity,*remainder=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("original domain identity drift "+profile)
        source=patch_source(source,profile)
        battle=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c")
        event=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle_event.c")
        source+="\n"+definition(battle,"BATTLE_Index2No")+"\n"
        native,has_lua=code(profile,source,battle,event)
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        templates,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        selected=eligible(loader,templates,enemies,remainder[-1])[0]
        traps=[t for t in accepted["profiles"][profile]["unreachable_traps"] if t not in
               ("BATTLE_Index2No","RIDEPET_getPETindex","CHAR_sendCToArroundCharacter","CHAR_send_K_StatusString")]
        outputs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-true-loop-init-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                compile_probe(profile,roots[profile],native,exe,opt,traps)
                run=subprocess.run([str(exe),*map(str,paths)],
                                   input="".join(f"{selected} {mode}\n" for mode in range(4)),
                                   capture_output=True,text=True)
                if run.returncode or any(not x.startswith("TRACE|") for x in run.stderr.splitlines() if x.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",run.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                           capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("actual original BATTLE_Loop "+profile+" "+opt+" rc="+str(run.returncode)+
                                     " stderr="+run.stderr[-5000:]+" symbols="+symbols+" stdout="+run.stdout[-2000:])
                lines=[x for x in run.stdout.splitlines() if x.startswith("REAL_HEADER_INIT|")]
                if len(lines)!=4 or run.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("original dispatcher incomplete repeated Init/Exit")
                for mode,row in enumerate(lines):
                    if f"|mode={mode}|battle={mode%3}|initialized=1|" not in row:
                        raise ValueError("actual dispatcher cursor or Init drift")
                outputs.append(run.stdout)
        if outputs[0]!=outputs[1]:raise ValueError("original BATTLE_Loop output differs under optimization")
        sha=hashlib.sha256(outputs[0].encode()).hexdigest()
        print(f"PROFILE|{profile}|original_loop_init_dispatches=4|optimizations=O0,O2|lua_boundary={int(has_lua)}|sha256={sha}",flush=True)
        for row in outputs[0].splitlines():
            if row.startswith("REAL_HEADER_INIT|"):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|original_BATTLE_Loop_INIT_only_untaken_Command_Finish_Stop_Watch_trap;original_Init_PreCommand_Exit;bounded_outbound_packets",flush=True)
    print("OPEN|real_combat_Command_2nd_Loop_round_Finish_watch_network_Lua_profit_full_server",flush=True)
    print("RESOLUTION|ORIGINAL_PARTY_PET_REALHEADER_LOOP_INIT_DISPATCH_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
