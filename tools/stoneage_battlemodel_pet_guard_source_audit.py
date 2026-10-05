"""Native literal target+5 pet guard witnesses, explicit reduced SIDE_OFFSET10.

Compiles original fixed helper bodies transiently with controlled shared stubs.
No original build, multiplayer SIDE_OFFSET12 or complete round exit is claimed.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_battlemodel_source_audit import _normalized_identifier
from tools.stoneage_battlemodel_hit_lifecycle_source_audit import PREFIX


def analyze_profile(name: str, root: Path) -> tuple[str, int]:
    root = root.resolve()
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if sha != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    path = root / LAYOUTS[name] / "battle/battle_event.c"
    helper = _normalized_identifier(_definition(_text(path), "BATTLE_BattleModel_ATTACK"))
    original_check = "if(n==0)return target_live;"
    if PREFIX.count(original_check) != 1:
        raise ValueError("controlled TargetCheck stub drift")
    prefix = PREFIX.replace(original_check, "if(n>=5&&n<=9)return target_live;")
    main = r'''
int main(void){
  int target,ownerflag,oppositeflag;
  while(scanf("%d%d%d",&target,&ownerflag,&oppositeflag)==3){
    memset(stats,0,sizeof(stats));memset(works,0,sizeof(works));
    memset(BattleArray,0,sizeof(BattleArray));
    stats[target][CHAR_HP]=200;stats[target][CHAR_WHICHTYPE]=CHAR_TYPEPET;
    stats[10][CHAR_HP]=200;stats[10][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;
    works[target][CHAR_NPCWORKINT1]=77;
    BattleArray[0].Side[0].Entry[target-5].flg=ownerflag?BENT_FLG_ULTIMATE:0;
    BattleArray[0].Side[1].Entry[target-5].flg=oppositeflag?BENT_FLG_ULTIMATE:0;
    seq_calls=damage_calls=wake_calls=status_calls=rng_calls=protocol_calls=0;
    seq_state=BATTLE_RET_NORMAL;seq_damage=1;seq_guardian=-1;
    target_live=1;guardian_live=0;reaction=0;status_hit=0;gDamageDiv=0.0;
    AttackObject object={0,target,123};
    BATTLE_BattleModel_ATTACK(0,10,&object,2,1,30,5);
    printf("%d %d %d %d\n",seq_calls,damage_calls,stats[target][CHAR_HP],
           works[target][CHAR_NPCWORKINT1]);
  }
  return 0;
}
'''
    cases = list(product(range(5, 10), (0, 1), (0, 1)))
    with tempfile.TemporaryDirectory(prefix="sa-battlemodel-pet-guard-") as folder:
        source, binary = Path(folder) / "oracle.c", Path(folder) / "oracle"
        source.write_text(prefix + "\n" + helper + "\n" + main)
        subprocess.run(["cc", "-std=c99", "-O0", str(source), "-o", str(binary)],
                       check=True, capture_output=True, text=True)
        rows = subprocess.check_output([str(binary)],
            input="".join(" ".join(map(str, c)) + "\n" for c in cases), text=True).splitlines()
    if len(rows) != len(cases):
        raise ValueError("pet guard native output count drift")
    for (target, owner, opposite), row in zip(cases, rows):
        wanted = (0, 0, 200, 77) if opposite else (1, 1, 199, 77)
        if tuple(map(int, row.split())) != wanted:
            raise ValueError(f"pet guard mapping drift target={target} owner={owner} opposite={opposite}")
    return _sha(path), len(cases)


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", required=True, type=Path)
    args = parser.parse_args()
    print("StoneAge BattleModel pet guard — explicit reduced SIDE_OFFSET10")
    for name in PINNED:
        digest, count = analyze_profile(name, getattr(args, name + "_dir"))
        print(f"PROFILE|profile={name}|sha={PINNED[name]}|source_sha256={digest}|native_pet_guard_cases={count}")
    print("FACT|reduced_SIDE_OFFSET10_pet_slots5_9_guard_opposite_entries10_14_not_ordinary_owner0_4")
    print("BOUNDARY|original_TargetCheck_AttackSeq_settlement_and_multiplayer_SIDE_OFFSET12_not_certified")
    print("RESOLUTION|BATTLEMODEL_LITERAL_PET_GUARD_REDUCED10_NATIVE_PASS")


if __name__ == "__main__":
    main()
