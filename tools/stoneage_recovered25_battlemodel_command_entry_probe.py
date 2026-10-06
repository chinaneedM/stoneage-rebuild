"""Derived-only actual ID638 entry census; no preserved payload is emitted."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from tools.stoneage_recovered25_battlemodel_runtime_probe import verify_files, verify_ai_files
from tools.stoneage_recovered25_battlemodel_admission_probe import analyze_admission
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_encount_chain_probe import configured_file, setup_values, parse_enemy, parse_group, parse_encount
from tools.stoneage_enemy_ai_model import parse_normal_enemy_ai_options
from tools.stoneage_magic_probe import parse as parse_magic
from tools.stoneage_recovered25_petskill_pressure_probe import analyze_runtime_objects

MAGIC_SHA256 = "b3a57b595bd60dfab571fe7af4dd6e2d43a5839c934eb644ba462897b1bcb6bb"
CALLBACK = b"PETSKILL_BattleModel"


def magic_census(parsed, petskills):
    # MAGIC_AttSkill forwards its second token directly to the callback's
    # array parameter. Resolve by loader order, never by skill-ID arithmetic.
    ordered = tuple(petskills.skills.values())
    candidates = []
    for fields, values in parsed:
        parts = fields[3].split(b";")
        if len(parts) < 2 or parts[0] != CALLBACK:
            continue
        # C atoi consumes a signed decimal prefix and returns zero when
        # there are no digits. A strict Python int would miss actual entries.
        token = parts[1].split(b"\0", 1)[0]
        match = re.match(rb"\s*([+-]?[0-9]+)", token)
        array = int(match.group(1)) if match else 0
        if not -(2**31) <= array < 2**31:
            raise ValueError("magic callback array atoi overflow outside bounded audit")
        skill = ordered[array] if array is not None and 0 <= array < len(ordered) else None
        candidates.append(dict(magic_id=values["ID"], callback_array=array,
            resolved_skill_id=None if skill is None else skill.skill_id,
            resolves_BattleModel=skill is not None and skill.function_name == CALLBACK.decode(),
            option_sha256=hashlib.sha256(fields[3]).hexdigest()))
    return dict(rows=len(parsed), callback_option_candidates=candidates,
        resolved_ID638_rows=sum(row["resolved_skill_id"] == 638 and row["resolves_BattleModel"] for row in candidates),
        resolved_other_BattleModel_rows=sum(row["resolved_skill_id"] in (641, 649, 650) and row["resolves_BattleModel"] for row in candidates),
        scope="literal first OPTION token and loader-ordered callback array; equipment ownership/MP not inferred")


def graph_census(enemies, groups, areas):
    first_groups = {}
    for group in groups:
        first_groups.setdefault(group["id"], group)
    results = []
    for tempno, expected_id in ((1178, 2559), (1179, 2560)):
        variants = [row for row in enemies if row["tempno"] == tempno]
        if len(variants) != 1 or variants[0]["id"] != expected_id:
            raise ValueError("actual BattleModel variant identity drift")
        variant = variants[0]
        options = parse_normal_enemy_ai_options(variant["tactics_option"])
        if variant["tactics"] != 1 or options.skill_weights[2] != 0 or options.enemy_attack_ai_random_override is not None:
            raise ValueError("actual BattleModel zero-weight normal configuration drift")
        group_ids = sorted(group_id for group_id, group in first_groups.items()
            if any(enemy == expected_id and weight > 0 for enemy, weight in zip(group["enemyids"], group["enemyprobs"])))
        area_refs = sum(any(group_id in group_ids and weight > 0
            for group_id, weight in zip(area["groupids"], area["groupprobs"])) for area in areas)
        results.append(dict(tempno=tempno, enemy_id=expected_id, tactics=variant["tactics"],
            wa_index2_weight=options.skill_weights[2], capturable_flag=variant["petflg"],
            positive_group_ids=group_ids, positive_area_rows=area_refs,
            scope="structural positive weights only; item/event/location/spawn prerequisites not discharged"))
    return results


def analyze(data_dir, setup):
    verify_files(data_dir, setup)
    verify_ai_files(data_dir, setup)
    petskills = load_recovered25_petskill_runtime(data_dir=data_dir, setup=setup)
    enemybase = load_recovered25_enemybase_runtime(data_dir=data_dir, setup=setup)
    analyze_admission(petskills, enemybase)
    config = setup_values(setup)
    paths = {key: configured_file(data_dir, config, key, [pattern]) for key, pattern in
             (("enemyfile", "enemy*.txt"), ("groupfile", "group*.txt"),
              ("encountfile", "encount*.txt"), ("magicfile", "magic*.txt"))}
    if any(path is None for path in paths.values()):
        raise ValueError("BattleModel entry audit requires active master files")
    if hashlib.sha256(paths["magicfile"].read_bytes()).hexdigest() != MAGIC_SHA256:
        raise ValueError("active magic whole-file identity drift")
    _raw, enemies, enemy_bad, _width, _prefix = parse_enemy(paths["enemyfile"])
    _raw, groups, group_bad, _width = parse_group(paths["groupfile"])
    _raw, areas, area_bad, _width = parse_encount(paths["encountfile"])
    _raw, magic, magic_bad, _counts, _profiles = parse_magic(paths["magicfile"])
    if any((enemy_bad, group_bad, area_bad, magic_bad)):
        raise ValueError("BattleModel entry audit malformed master rows")
    ordered = tuple(petskills.skills.values())
    callback_rows = [dict(skill_id=row.skill_id, illegal=row.illegal, callback_array=index,
                         default_header_pet_entry="blocked_nonzero_ILLEGAL")
                     for index, row in enumerate(ordered) if row.function_name == CALLBACK.decode()]
    ledger = analyze_runtime_objects(petskills, enemybase)
    pressure = dict(total=ledger["total_positive_slot_uses"],
        closed=sum(row["slot_uses"] for row in ledger["rows"] if row["status"] == "closed_runtime"),
        open=sum(row["slot_uses"] for row in ledger["rows"] if row["status"] == "open"),
        historical_ub=sum(row["slot_uses"] for row in ledger["rows"] if row["status"] == "historical_ub"),
        promoted_slots=0, unresolved_skill_ids=list(ledger["unresolved_skill_ids"]))
    if pressure != dict(total=2486, closed=2461, open=22, historical_ub=3,
                        promoted_slots=0, unresolved_skill_ids=[]):
        raise ValueError("complete pressure census drift")
    battlemodel = next(row for row in ledger["rows"] if row["callback"] == CALLBACK.decode())
    if battlemodel["status"] != "open" or battlemodel["slot_uses"] != 2 or battlemodel["skill_ids"] != (638,):
        raise ValueError("BattleModel pressure scope drift")
    return dict(schema="stoneage.battlemodel-command-entry-data.r1",
        file_sha256={key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()},
        callback_rows=callback_rows, positive_placements=graph_census(enemies, groups, areas),
        magic=magic_census(magic, petskills),
        pressure=pressure, pressure_rows=ledger["rows"],
        boundary="entry census only; opaque script/build overrides and full gameplay reachability OPEN",
        resolution="RECOVERED25_BATTLEMODEL_COMMAND_ENTRY_DATA_AUDITED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.data_dir, args.setup)
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(content)
    print(content, end="")


if __name__ == "__main__":
    main()
