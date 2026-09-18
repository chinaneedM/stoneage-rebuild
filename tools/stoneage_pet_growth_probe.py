#!/usr/bin/env python3
"""Profile recovered enemybase templates through the descendant PETRANK rule."""

import argparse,collections
from pathlib import Path
from tools.stoneage_enemybase_probe import analyze as analyze_enemybase
from tools.stoneage_pet_growth_model import pet_rank_from_template_base,RANK_ROLL_RANGES


def analyze(data_dir,setup=None):
    active,files=analyze_enemybase(data_dir,setup)
    out=[]
    for f in files:
        rank_counts=collections.Counter()
        sums=collections.Counter()
        for r in f["rows"]:
            total=r["BASEVITAL"]+r["BASESTR"]+r["BASETGH"]+r["BASEDEX"]
            rank=pet_rank_from_template_base(
                r["BASEVITAL"],r["BASESTR"],r["BASETGH"],r["BASEDEX"])
            rank_counts[rank]+=1
            sums[total]+=1
        out.append({
            "name":f["name"],"active":f["active"],"rows":len(f["rows"]),
            "rank_counts":rank_counts,"sums":sums,
            "min_sum":min(sums) if sums else None,
            "max_sum":max(sums) if sums else None,
            "unique_sums":len(sums),
        })
    return active,out


def emit(data_dir,setup=None):
    active,files=analyze(data_dir,setup)
    print("StoneAge recovered pet-growth rank probe — R1")
    print("No original pet names or raw enemybase rows are stored in this report.")
    print("RANK_SOURCE|descendant_ENEMY_getRank")
    print("LEVELUP_SOURCE|descendant_CHAR_PetLevelUp")
    print(f"ENEMYBASE_ACTIVE_CONFIG|{active or 'UNKNOWN'}")
    for rank,(lo,hi) in enumerate(RANK_ROLL_RANGES):
        print(f"RANK_ROLL_RANGE|{rank}|{lo}|{hi}")
    for f in files:
        print(f"FILE|{f['name']}|rows={f['rows']}|active={int(f['active'])}|base_sum_min={f['min_sum']}|base_sum_max={f['max_sum']}|unique_sums={f['unique_sums']}")
        for rank in range(6):
            print(f"RANK_COUNT|{f['name']}|{rank}|{f['rank_counts'].get(rank,0)}")
        for total,n in sorted(f["sums"].items()):
            print(f"BASE_SUM|{f['name']}|{total}|{n}")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path)
    a=ap.parse_args()
    emit(a.data_dir,a.setup)


if __name__=="__main__":
    main()
