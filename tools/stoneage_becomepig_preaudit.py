"""Reproduce pinned BecomePig structural facts without admitting runtime semantics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _function, _compact,
)
from tools.stoneage_mdfyattack_source_audit import _definition, _strip


def postattack_block(source: str) -> str:
    match = re.search(r'if\s*\(\s*\(?\s*COM\s*==\s*BATTLE_COM_S_BECOMEPIG', source)
    if match is None:
        raise ValueError("BecomePig postattack block missing")
    return _function(source[match.start():], match.group())


def analyze_profile(name: str, root: Path) -> dict:
    root = root.resolve()
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    receipt = json.loads((Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-BECOMEPIG-PRELIMINARY-SOURCE-OBSERVATION-R1.json").read_text())
    identity = next(row for row in receipt["profiles"] if row["profile"] == name)
    hashes = {}
    for kind, row in identity["paths"].items():
        raw = (root / row["path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != row["git_blob"]:
            raise ValueError("pinned callback/dispatcher blob drift")
        hashes[kind] = {"git_blob": blob, "sha256": hashlib.sha256(raw).hexdigest()}
    base = root / LAYOUTS[name]
    pet = _text(base / "battle/pet_skill.c").replace("char_index", "charaindex")
    battle = _text(base / "battle/battle.c").replace("char_index", "charaindex")
    event_path = base / "battle/battle_event.c"
    event = _text(event_path).replace("char_index", "charaindex")
    callback = _compact(_strip(_definition(pet, "PETSKILL_BecomePig")))
    hit = _compact(_strip(postattack_block(battle)))
    side = _compact(_strip(_definition(event, "BATTLE_CheckSameSide")))
    exit_body = _compact(_strip(_definition(battle, "_BATTLE_Exit")))
    checks = {
        "callback_symbolic_command_target_ready_and_low_array": all(x in callback for x in (
            "CHAR_WORKBATTLECOM1,BATTLE_COM_S_BECOMEPIG", "CHAR_WORKBATTLECOM2,toNo",
            "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK", "CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)")),
        "callback_has_no_option_parse_or_rng": all(x not in callback for x in ("PETSKILL_OPTION", "sscanf(", "rand(", "RAND(")),
        "postattack_rejects_miss_dodge_allguard": all("!=BATTLE_RET_"+x in hit for x in ("MISS", "DODGE", "ALLGUARD")),
        "living_before_player_before_option_before_draw": hit.index("BATTLE_TargetCheck") < hit.index("CHAR_WHICHTYPE") < hit.index("PETSKILL_OPTION") < hit.index("rand()%100<petrate"),
        "target_is_exact_player": "CHAR_WHICHTYPE)==CHAR_TYPEPLAYER" in hit,
        "same_side_site_reads_attacker_and_defno": "BATTLE_CheckSameSide(charaindex,defNo)!=1" in hit,
        "same_side_helper_first_arg_is_character_index": "CHAR_getWorkInt(charaindex,CHAR_WORKBATTLEINDEX)" in side,
        "counter_guard_is_strict_preaddition_two_billion": "CHAR_BECOMEPIG)<2000000000" in hit and hit.index("<2000000000") < hit.index("PETSKILL_OPTION"),
        "option_lookup_uses_command3_low_array": "PETSKILL_getChar(CHAR_GETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3),PETSKILL_OPTION)" in hit,
        "three_decimal_conversion_return_is_unchecked": 'sscanf(pszOption,"%d%d%d",&petrate,&pettime,&pigbbi);else' in hit,
        "only_pig_image_is_initialized_in_local_declaration": "compute,petrate,pettime,pigbbi=100250;" in hit,
        "exact_one_rate_draw_after_parse": hit.count("rand()%100") == 1 and hit.index("sscanf(") < hit.index("rand()%100<petrate"),
        "successful_hit_clears_item_npc_and_fox": all(x in hit for x in ("CHAR_WORKITEMMETAMO,0", "CHAR_WORKNPCMETAMO,0", "CHAR_WORKFOXROUND,-1")),
        "magic_effect_identifiers_are_literal": "BATTLE_MagicEffect(battleindex,defNo,ToList,101120,101750)" in hit,
        "success_can_dismount_and_set_petfall": all(x in hit for x in ("CHAR_RIDEPET,-1", "BATTLE_changeRideImage(defindex)", "CHAR_WORKPETFALL,1")),
        "pig_image_saved_in_ordinary_field": "CHAR_setInt(defindex,CHAR_BECOMEPIG_BBI,pigbbi)" in hit,
        "base_image_reads_saved_pig_image": "CHAR_setInt(defindex,CHAR_BASEIMAGENUMBER,CHAR_getInt(defindex,CHAR_BECOMEPIG_BBI))" in hit,
        "first_hit_counter_is_pettime_plus_one_plus_minusone": "if(compute==-1)CHAR_setInt(defindex,CHAR_BECOMEPIG,pettime+1+compute)" in hit,
        "repeat_hit_accumulates_ordinary_counter": "elseCHAR_setInt(defindex,CHAR_BECOMEPIG,pettime+compute)" in hit,
        "no_round_marker_or_fixed_power_write_in_transform": all(x not in hit for x in ("pBattle->turn", "CHAR_WORKFIXSTR", "CHAR_WORKFIXTOUGH", "CHAR_WORKFIXDEX")),
        "exit_retains_active_player_pig_image": "CHAR_BECOMEPIG)>-1" in exit_body and "CHAR_BECOMEPIG_BBI" in exit_body,
    }
    if name == "bismarck":
        checks["literal_pointer_comparison_not_string_content"] = 'if(pszOption=="\\0")sscanf(' in hit
        checks["different_else_defaults_preserved"] = "elsepetrate=30,pettime=60,pigbbi=100250" in hit
        checks["arrange_and_same_side_sites_have_separate_guards"] = "#ifdef_EQUIT_ARRANGE" in hit and "#ifdef_PREVENT_TEAMATTACK" in hit
        option_profile = "POINTER_LITERAL_COMPARISON_ELSE_30_60_100250"
        guard_profile = "CONDITIONAL_ARRANGE_AND_PREVENT_TEAMATTACK"
    else:
        checks["nonnull_pointer_branch_not_empty_string_check"] = "if(pszOption)sscanf(" in hit
        checks["nonnull_absent_option_defaults_preserved"] = "elsepetrate=100,pettime=60,pigbbi=100250" in hit
        checks["arrange_and_same_side_sites_unconditional_in_block"] = "!=BATTLE_RET_ARRANGE" in hit and "#ifdef" not in hit
        option_profile = "NONNULL_POINTER_ELSE_100_60_100250"
        guard_profile = "UNCONDITIONAL_ARRANGE_AND_SAME_SIDE"
    if not all(checks.values()):
        raise ValueError(f"{name} BecomePig gates failed: {[k for k,v in checks.items() if not v]}")
    hashes["same_side_helper_file"] = {"sha256": _sha(event_path)}
    return {"profile": name, "sha": head, "gates": checks, "hashes": hashes,
            "option_profile": option_profile, "guard_profile": guard_profile}


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir", type=Path, required=True)
    args = parser.parse_args()
    print("StoneAge BecomePig pinned source preaudit R1; structural observation only.")
    for name in PINNED:
        r = analyze_profile(name, getattr(args, name+"_dir"))
        print(f"PROFILE|name={name}|sha={r['sha']}|passed_gates={len(r['gates'])}|option_profile={r['option_profile']}|guard_profile={r['guard_profile']}")
        for gate in r["gates"]:
            print(f"GATE|profile={name}|name={gate}|pass=1")
        for kind, hashes in r["hashes"].items():
            print(f"SOURCE_IDENTITY|profile={name}|file={kind}|"+"|".join(f"{k}={v}" for k,v in hashes.items()))
    print("OPEN|unchecked_conversion_uninitialized_ints_literal_pointer_identity_and_signed_addition_overflow")
    print("OPEN|active_build_guards_elapsed_time_owner_ordered_runtime_and_persistence")
    print("BOUNDARY|source_structure_only_no_executable_profile_or_runtime_acceptance_zero_promotions")
    print("RESOLUTION|BECOMEPIG_PINNED_SOURCE_PREAUDIT_PASS_NOT_REFERENCE_OR_RUNTIME_ACCEPTANCE")


if __name__ == "__main__":
    main()
