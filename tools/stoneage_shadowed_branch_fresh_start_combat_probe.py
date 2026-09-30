#!/usr/bin/env python3
"""Audit an existential fresh-start one-hit combat victory witness.

This probe intentionally asks for a strong sufficient witness, not a general
combat solver.  A qualifying witness must use:

- one of the normal hometown starts already proven coordinate-reachable to the
  key-item award chain;
- a coordinate-reachable, item-ungated, positive-weight EXP encounter already
  accepted by the fresh-start leveling-source audit;
- a legal encounter count of exactly one enemy;
- that enemy at a legal level no higher than the recovered birth level;
- a legal weakest enemy birth roll (all four base offsets -2, with all legal
  distributions of the ten allocation rolls);
- a legal new-character 20-point STR/DEX allocation and a legal pure-element
  allocation;
- ordinary physical attack only, no equipment, no consumables, no pet, no
  critical and no special skill;
- player action strictly before the enemy under legal initiative rolls; and
- one successful ordinary hit whose fixed-descendant damage is at least the
  enemy's full HP.

Fixed-descendant normal enemy AI chooses among weighted attack/guard/magic/
escape/skill branches.  A template merely having skills does not force their
use: a positive `at` weight makes ordinary attack a legal command outcome.
A one-hit kill also suppresses the later counter chain because the defender is
already dead.  Ordinary dodge remains below 100%, so a successful hit is a
legal RNG outcome.  This proves existence of a fresh-character battle victory
path, not guaranteed victory or balance quality.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_battle_core_model import (
    ENEMY,
    PLAYER,
    attribute_adjusted_damage,
    dodge_per_10000,
    early_action_value,
    effective_defense_newpower,
    physical_base_damage,
)
from tools.stoneage_encount_chain_probe import (
    ENEMY_INT_COUNT,
    choose_enemy_prefix,
    clean_rows,
    configured_file,
    setup_values,
)
from tools.stoneage_enemybase_probe import parse_file as parse_enemybase_file
from tools.stoneage_player_growth_model import base_derived_stats
from tools.stoneage_shadowed_branch_fresh_start_leveling_probe import (
    analyze as analyze_leveling,
)
from tools.stoneage_tw10_25_bridge_model import (
    PetTemplateBridge,
    build_pet_birth_bridge,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_FRESH_START_COMBAT_VICTORY_AUDITED"

PURE_ELEMENTS=(
    (100,0,0,0),
    (0,100,0,0),
    (0,0,100,0),
    (0,0,0,100),
)


def _coordinate_valid_ordinals(text:str)->frozenset[int]:
    out=set()
    for raw in str(text).splitlines():
        line=raw.strip()
        if not line.startswith("FRESH_START_COORDINATE_WITNESS|"):
            continue
        fields={}
        for part in line.split("|")[1:]:
            if "=" in part:
                key,value=part.split("=",1)
                fields[key]=value
        if fields.get("reachable")=="1":
            out.add(int(fields["ordinal"]))
    return frozenset(out)


def _normal_ai_attack_weight(option:bytes|str)->int:
    """Return the fixed-descendant normal-AI `at` branch weight."""
    if isinstance(option,bytes):
        text=option.decode("utf-8","replace")
    else:
        text=str(option)
    for segment in text.split("|"):
        key,sep,payload=segment.partition(":")
        if sep and key.strip()=="at":
            head=payload.split(";",1)[0].strip()
            try:
                return max(0,int(head or "0"))
            except ValueError:
                return 0
    return 0


def _normal_ai_profiles(enemy_path:Path)->dict[int,tuple[int,int]]:
    """Map enemy id -> (WORKTACTICS mode, ordinary-attack branch weight)."""
    rows=clean_rows(enemy_path)
    prefix=choose_enemy_prefix(rows)
    expected=prefix+ENEMY_INT_COUNT
    out={}
    for row in rows:
        if len(row)!=expected:
            continue
        try:
            enemy_id=int(row[prefix].strip() or b"0",10)
            tactics_mode=int(row[prefix+6].strip() or b"0",10)
        except ValueError:
            continue
        out[enemy_id]=(tactics_mode,_normal_ai_attack_weight(row[1]))
    return out


def _template_from_row(row:dict)->PetTemplateBridge:
    skills=tuple(
        int(row[f"PETSKILL{i}"])
        for i in range(1,8)
        if int(row[f"PETSKILL{i}"])>0
    )
    return PetTemplateBridge(
        tempno=int(row["TEMPNO"]),
        graphic_id=int(row["IMGNUMBER"]),
        name="WITHHELD",
        ai=int(row["MODAI"]),
        earth=int(row["EARTHAT"]),
        water=int(row["WATERAT"]),
        fire=int(row["FIREAT"]),
        wind=int(row["WINDAT"]),
        skill_slots=int(row["SLOT"]),
        skill_ids=skills,
        init_num=int(row["INITNUM"]),
        base_vital=int(row["BASEVITAL"]),
        base_strength=int(row["BASESTR"]),
        base_toughness=int(row["BASETGH"]),
        base_dexterity=int(row["BASEDEX"]),
        level_up_point=int(row["LVUPPOINT"]),
        size_class=int(row["SIZE"]),
        capture_default=int(row["GET"]),
    )


def _allocation_roll_sequences():
    """Yield one representative sequence for each 10-roll stat composition."""
    for vital in range(11):
        for strength in range(11-vital):
            for tough in range(11-vital-strength):
                dex=10-vital-strength-tough
                yield (
                    (0,)*vital
                    +(1,)*strength
                    +(2,)*tough
                    +(3,)*dex
                )


def _max_physical_damage(attack:int,effective_defense:float)->int:
    attack=int(attack)
    if effective_defense > attack:
        roll=1
    elif attack < effective_defense*(8.0/7.0):
        roll=int(attack*(1.0/16.0))
    else:
        roll=int(attack*(1.0/8.0))
    return max(0,int(physical_base_damage(attack,effective_defense,roll)))


@dataclass(frozen=True)
class OneHitWitness:
    spawn_ordinal:int
    source_floor:int
    source_enemy_id:int
    source_tempno:int
    source_group_id:int
    source_encounter_index:int
    enemy_level:int
    player_strength:int
    player_dexterity:int
    player_attack:int
    player_quick:int
    enemy_hp:int
    enemy_defense:int
    enemy_quick:int
    damage:int
    dodge_per_10000:int


@dataclass(frozen=True)
class CombatAudit:
    coordinate_valid_hometowns:int
    low_level_source_rows:int
    leveling_reward_chain:bool
    unique_candidate_variants:int
    ordinary_attack_candidate_variants:int
    one_hit_witnesses:tuple[OneHitWitness,...]

    @property
    def existential_victory(self)->bool:
        return bool(self.one_hit_witnesses)


def _player_profiles():
    # For a first-action one-hit sufficient witness, vitality/toughness cannot
    # improve attack or initiative more efficiently than reallocating those
    # points to STR/DEX.  Enumerating the STR/DEX frontier is therefore enough.
    for strength in range(21):
        dexterity=20-strength
        stats=base_derived_stats(
            0,
            strength*100,
            0,
            dexterity*100,
        )
        for elements in PURE_ELEMENTS:
            yield strength,dexterity,stats,elements


def analyze(
    *,
    npc_dir:Path,
    data_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
    coordinate_report_text:str,
)->CombatAudit:
    valid_ordinals=_coordinate_valid_ordinals(coordinate_report_text)
    if not valid_ordinals:
        raise ValueError("no coordinate-valid fresh-start hometowns")

    leveling=analyze_leveling(
        npc_dir=npc_dir,
        data_dir=data_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    birth_level=int(leveling.birth_level)
    sources=[
        row for row in leveling.sources
        if row.spawn_ordinal in valid_ordinals
        and row.enemy_can_spawn_at_or_below_birth
        and row.enemy_min_level>=1
        and row.enemy_id>=0
        and row.tempno>=0
    ]

    config=setup_values(setup)
    enemy_path=configured_file(data_dir,config,"enemyfile",["enemy*.txt"])
    enemybase_path=configured_file(
        data_dir,config,"enemybasefile",["enemybase*.txt"]
    )
    if enemy_path is None:
        raise ValueError("active enemy file missing")
    if enemybase_path is None:
        raise ValueError("active enemybase file missing")
    normal_ai_by_enemy=_normal_ai_profiles(enemy_path)
    base_rows,_fc,_bad,_raw,_profiles=parse_enemybase_file(enemybase_path)
    base_by_tempno={int(row["TEMPNO"]):row for row in base_rows}

    unique_variants={}
    for source in sources:
        unique_variants.setdefault(
            (source.enemy_id,source.tempno,source.enemy_min_level),
            source,
        )

    player_profiles=tuple(_player_profiles())
    witnesses=[]
    ordinary_attack_candidates=0

    for (_enemy_id,tempno,min_level),source in unique_variants.items():
        raw_template=base_by_tempno.get(int(tempno))
        if raw_template is None:
            continue
        template=_template_from_row(raw_template)
        # Fixed battle_ai normal mode selects actions by weights in the enemy
        # TACTICSOPTION string.  Skill inventory is only consulted if a wa
        # branch wins that draw.  Counter cannot fire after a lethal first hit.
        tactics_mode,attack_weight=normal_ai_by_enemy.get(
            int(source.enemy_id),(-1,0)
        )
        if tactics_mode!=1 or attack_weight<=0:
            continue
        ordinary_attack_candidates+=1

        best=None
        for rolls in _allocation_roll_sequences():
            birth=build_pet_birth_bridge(
                template,
                level=int(min_level),
                birth_offsets=(-2,-2,-2,-2),
                spawn_allocation_rolls=rolls,
            )
            enemy=birth.combat_projection()
            if int(enemy["max_hp"])<=0:
                continue
            enemy_min_action=early_action_value(
                int(enemy["quick"]),
                int((int(enemy["quick"])+20)*0.30),
            )
            effective_defense=effective_defense_newpower(
                int(enemy["defense"])
            )
            defender_elements=(
                int(template.earth),
                int(template.water),
                int(template.fire),
                int(template.wind),
            )

            for strength,dexterity,player,elements in player_profiles:
                player_max_action=early_action_value(
                    int(player["quick"]),0
                )
                if player_max_action <= enemy_min_action:
                    continue
                base=_max_physical_damage(
                    int(player["attack_power"]),
                    effective_defense,
                )
                damage=attribute_adjusted_damage(
                    base,elements,defender_elements
                )
                if int(damage) < int(enemy["max_hp"]):
                    continue
                dodge=dodge_per_10000(
                    int(player["quick"]),
                    int(enemy["quick"]),
                    attacker_type=PLAYER,
                    defender_type=ENEMY,
                )
                if dodge>=10000:
                    continue
                candidate=OneHitWitness(
                    spawn_ordinal=int(source.spawn_ordinal),
                    source_floor=int(source.floor),
                    source_enemy_id=int(source.enemy_id),
                    source_tempno=int(source.tempno),
                    source_group_id=int(source.group_id),
                    source_encounter_index=int(source.encounter_index),
                    enemy_level=int(min_level),
                    player_strength=int(strength),
                    player_dexterity=int(dexterity),
                    player_attack=int(player["attack_power"]),
                    player_quick=int(player["quick"]),
                    enemy_hp=int(enemy["max_hp"]),
                    enemy_defense=int(enemy["defense"]),
                    enemy_quick=int(enemy["quick"]),
                    damage=int(damage),
                    dodge_per_10000=int(dodge),
                )
                if best is None or (
                    candidate.damage-candidate.enemy_hp,
                    candidate.player_quick-candidate.enemy_quick,
                ) > (
                    best.damage-best.enemy_hp,
                    best.player_quick-best.enemy_quick,
                ):
                    best=candidate
        if best is not None:
            witnesses.append(best)

    return CombatAudit(
        coordinate_valid_hometowns=len(valid_ordinals),
        low_level_source_rows=len(sources),
        leveling_reward_chain=bool(leveling.leveling_reward_chain),
        unique_candidate_variants=len(unique_variants),
        ordinary_attack_candidate_variants=ordinary_attack_candidates,
        one_hit_witnesses=tuple(witnesses),
    )


def emit(audit:CombatAudit)->None:
    print("StoneAge shadowed-branch fresh-start combat victory audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_CONTROL|battle_newpower_enabled=1|"
        "npcenemy_addpower_enabled=1|ordinary_dodge_cap_percent=75|"
        "normal_enemy_ai_weighted_actions=1|counter_requires_surviving_target=1"
    )
    print(
        "RULE|enemy/group/template ids, levels, stats, coordinates, player "
        "allocation values and damage values are withheld"
    )
    print(
        "RULE|witness requires a coordinate-valid fresh-start hometown, "
        "positive-EXP low-level source, one-enemy legal encounter outcome, "
        "fixed-descendant normal enemy AI with a positive ordinary-attack "
        "branch weight, legal enemy birth rolls, legal 20-point new-character "
        "allocation, player-first legal initiative "
        "and ordinary one-hit KO without equipment/pet/item/critical/skill"
    )
    print(
        "RULE|NPCENEMY_ADDPOWER minimum legal defense adjustment is zero under "
        "the fixed-descendant integer expression; no favorable negative modifier "
        "is invented"
    )
    print(f"COUNT|coordinate_valid_hometowns|{audit.coordinate_valid_hometowns}")
    print(f"COUNT|low_level_source_rows|{audit.low_level_source_rows}")
    print(
        "PREREQUISITE_LEVELING_REWARD_CHAIN|witness="
        f"{int(audit.leveling_reward_chain)}"
    )
    print(f"COUNT|unique_candidate_variants|{audit.unique_candidate_variants}")
    print(
        "COUNT|ordinary_attack_ai_candidate_variants|"
        f"{audit.ordinary_attack_candidate_variants}"
    )
    print(f"COUNT|one_hit_witness_variants|{len(audit.one_hit_witnesses)}")
    print(
        "FRESH_START_EXISTENTIAL_COMBAT_VICTORY|witness="
        f"{int(audit.existential_victory)}"
    )
    print(
        "UNIVERSAL_OR_GUARANTEED_COMBAT_VICTORY|closed=0|"
        "reason=existential_rng_and_build_witness_only"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    ap.add_argument("--coordinate-report",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        data_dir=args.data_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
        coordinate_report_text=args.coordinate_report.read_text(
            encoding="utf-8"
        ),
    ))


if __name__=="__main__":
    main()
