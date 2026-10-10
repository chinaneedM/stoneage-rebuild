"""Source-only profile-aware EXP/config dependency inventory for terminal FINISH.

The full original second Loop has reached BATTLE_Finish/GetProfit/GetExpGold,
but positive reward transfer remains unaccepted. This script only examines
complete pinned preprocessed source function bodies, never executes a payout.
No original source text or assets are committed to this repository.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path

from tools.stoneage_party_pet_original_attack_audit import (
    PINNED, LAYOUTS, definition, pp_file,
)
from tools.stoneage_party_pet_terminal_path_preflight import (
    PREVIOUS_FINGERPRINTS,
)

CONFIG_PATH = {
    "gavin": "configfile.c",
    "bismarck": "config_file.c",
}
CONFIG_OWNER = {
    "gavin": "config",
    "bismarck": "gServerConfig",
}
NAMES = ("BATTLE_Finish", "BATTLE_GetProfit", "BATTLE_GetExpGold", "BATTLE_GetExp")
CALL = re.compile(r"\b((?:BATTLE|CHAR|ITEM|PET|NETWATCH)_[A-Za-z0-9_]+|getBattleexp)\s*\(")
GETTER = re.compile(
    r"\bunsigned\s+int\s+getBattleexp\s*\(\s*void\s*\)\s*"
    r"\{\s*return\s+([A-Za-z_][A-Za-z_0-9]*)\s*\.\s*battleexp\s*;\s*\}",
    re.S,
)

def analyse(profile: str, bodies: dict[str, str], config: str) -> dict:
    if profile not in CONFIG_OWNER:
        raise ValueError("source profile not pinned")
    if set(NAMES) - bodies.keys():
        raise ValueError("missing original terminal EXP source bodies")
    for name in ("BATTLE_Finish", "BATTLE_GetProfit"):
        expected=PREVIOUS_FINGERPRINTS[profile][name]
        if hashlib.sha256(bodies[name].encode()).hexdigest()!=expected:
            raise ValueError("previously accepted original terminal source body drift: "+name)
    by_name={n: set(CALL.findall(b))-{n} for n,b in bodies.items()}
    for parent,child in (
        ("BATTLE_Finish","BATTLE_GetProfit"),
        ("BATTLE_GetProfit","BATTLE_GetExpGold"),
        ("BATTLE_GetExpGold","BATTLE_GetExp"),
    ):
        if child not in by_name[parent]:
            raise ValueError("original terminal reward dependency missing: "+parent+" -> "+child)
    if "CHAR_AddMaxExp" not in by_name["BATTLE_GetExp"]:
        raise ValueError("original EXP persistent write missing")
    match=GETTER.search(config)
    if not match or match.group(1)!=CONFIG_OWNER[profile]:
        raise ValueError("original configured EXP multiplier getter drift")
    # The exact body and hash are retained as provenance. A config getter
    # reference is not a calibrated runtime value for an actual battle.
    return {
        "profile":profile,
        "config_source_relative_path":CONFIG_PATH[profile],
        "original_exp_multiplier_owner":match.group(1),
        "getter_preprocessed_sha256":hashlib.sha256(match.group(0).encode()).hexdigest(),
        "getexp_uses_getBattleexp": "getBattleexp" in by_name["BATTLE_GetExp"],
        "getexp_source_mentions_1e6": bool(re.search(r"\b1e6\b",bodies["BATTLE_GetExp"])),
        "getexp_source_mentions_1000000000": "1000000000" in bodies["BATTLE_GetExp"],
        "source_bodies":{
            name:{
                "sha256":hashlib.sha256(body.encode()).hexdigest(),
                "bytes_utf8":len(body.encode()),
                "named_calls":sorted(by_name[name]),
            } for name,body in bodies.items()
        },
    }

def main():
    parser=argparse.ArgumentParser()
    for p in CONFIG_PATH:parser.add_argument("--"+p+"-dir",required=True,type=Path)
    args=parser.parse_args()
    results=[]
    for profile in CONFIG_PATH:
        root=getattr(args,profile+"_dir")
        sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
        if sha!=PINNED[profile] or dirty:
            raise ValueError("clean exact pinned descendant source required "+profile)
        battle_path=LAYOUTS[profile]/"battle/battle.c"
        config_path=LAYOUTS[profile]/CONFIG_PATH[profile]
        battle=pp_file(profile,root,battle_path)
        config=pp_file(profile,root,config_path)
        bodies={name:definition(battle,name) for name in NAMES}
        record=analyse(profile,bodies,config)
        record["pinned_commit"]=sha
        record["battle_file_sha256"]=hashlib.sha256((root/battle_path).read_bytes()).hexdigest()
        record["config_file_sha256"]=hashlib.sha256((root/config_path).read_bytes()).hexdigest()
        results.append(record)
        print(f"ORIGINAL_EXP_PROFILE|{profile}|finish_sha256={record['source_bodies']['BATTLE_Finish']['sha256']}|getexp_sha256={record['source_bodies']['BATTLE_GetExp']['sha256']}|config_owner={record['original_exp_multiplier_owner']}",flush=True)
    print("SOURCE_EXP_ROUTE_MATRIX|"+json.dumps(results,sort_keys=True,ensure_ascii=True))
    print("BOUNDARY|source_only;runtime_original_Finish_GetExpGold_reached_BATTLE_GetExp_trap;no_config_multiplier_or_positive_reward_oracle")
    print("OPEN|real_server_config_exp_multiplier_justification;original_EXP_calculation;leveling;positive_reward_owner;original_exit_release")
    print("RESOLUTION|ORIGINAL_PARTY_PET_FINISH_EXP_CONFIG_SOURCE_PREFLIGHT_PASS")

if __name__=="__main__":main()
