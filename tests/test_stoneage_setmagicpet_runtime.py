"""SetMagicPet runtime primitives use synthetic OPTION witnesses."""

from __future__ import annotations

from dataclasses import replace
import hashlib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.stoneage_enemy_ai_setmagicpet_bridge import (
    EXPECTED_OPTION_SHA256_BY_ID,
    EnemyAiSetMagicPetSubmission,
    resolve_enemy_ai_setmagicpet_submission,
    validate_recovered25_setmagicpet_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_setmagicpet_model import (
    SetMagicPetOption,
    SetMagicPetSourceDomain,
    SetMagicPetTargetState,
    parse_setmagicpet_option,
)
from tests.test_stoneage_attack_crazed_runtime import actor
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle,
    participant_snapshot,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime
from tools.stoneage_singleplayer_battle import BattleSession
from tools.stoneage_setmagicpet_runtime_state import (
    PreparedSetMagicPetPowers,
    SetMagicPetActionRolls,
    SetMagicPetParticipantRuntime,
    SetMagicPetRoundOverlay,
    apply_setmagicpet_option,
    prepare_setmagicpet_powers,
    tick_setmagicpet_runtime,
)


SYNTHETIC_OPTION_BY_ID={
    601:b"3|15|TGH",
    602:b"3|3000|HP",
    603:b"3|10|STR",
    604:b"3|15|DEX",
}
SYNTHETIC_HASH_BY_ID={
    skill_id:hashlib.sha256(raw).hexdigest()
    for skill_id,raw in SYNTHETIC_OPTION_BY_ID.items()
}


def runtime():
    return Recovered25PetSkillRuntime(
        skills={
            skill_id:Recovered25PetSkillEntry(
                skill_id,1,2,2,2500,"PETSKILL_SetMagicPet",raw
            )
            for skill_id,raw in SYNTHETIC_OPTION_BY_ID.items()
        },
        source_file="synthetic-petskill.txt",
    )


class SetMagicPetRuntimePrimitiveTests(unittest.TestCase):
    def test_exact_population_and_semantics_are_independent_hash_gates(self):
        with patch.dict(
            EXPECTED_OPTION_SHA256_BY_ID,SYNTHETIC_HASH_BY_ID,clear=True
        ):
            validate_recovered25_setmagicpet_population(runtime())
        broken=runtime()
        skills=dict(broken.skills)
        skills[604]=replace(skills[604],illegal=0)
        with patch.dict(
            EXPECTED_OPTION_SHA256_BY_ID,SYNTHETIC_HASH_BY_ID,clear=True
        ),self.assertRaises(ValueError):
            validate_recovered25_setmagicpet_population(
                Recovered25PetSkillRuntime(
                    skills=skills,source_file="synthetic-petskill.txt"
                )
            )

    def test_bridge_admits_only_positive_601_selected_slot(self):
        spawned=SimpleNamespace(
            participant=SimpleNamespace(
                participant_id="enemy",side="enemy",kind="enemy"
            ),
            template=SimpleNamespace(
                skill_slot_ids=(0,601,0,0,0,0,0)
            ),
        )
        with patch.dict(
            EXPECTED_OPTION_SHA256_BY_ID,SYNTHETIC_HASH_BY_ID,clear=True
        ):
            submission=resolve_enemy_ai_setmagicpet_submission(
                spawned,skill_slot=1,target_slot=3,petskill_runtime=runtime()
            )
        self.assertEqual(
            (
                submission.participant_id,submission.skill_slot,
                submission.skill_id,submission.source_target_slot,
                submission.option.turn,submission.option.amount,
                submission.option.kind,
            ),
            ("enemy",1,601,3,3,15,"TGH"),
        )
        with self.assertRaises(ValueError):
            EnemyAiSetMagicPetSubmission(
                "enemy",0,602,"PETSKILL_SetMagicPet",3,
                parse_setmagicpet_option(SYNTHETIC_OPTION_BY_ID[602]),
            )

    def test_action_rng_is_only_dead_single_retarget_bundle(self):
        self.assertTrue(SetMagicPetActionRolls().is_empty)
        self.assertFalse(SetMagicPetActionRolls((9,0)).is_empty)
        with self.assertRaises(ValueError):
            SetMagicPetActionRolls((10,))

    def test_statusseq_tick_decrements_duck_and_magicpet_together(self):
        runtime0=SetMagicPetParticipantRuntime(
            SetMagicPetTargetState(
                duck_turn=1,
                str_turn=2,str_power=10,
                tgh_turn=1,tgh_power=15,
                dex_turn=3,dex_power=20,
            ),
            PreparedSetMagicPetPowers(100,115,80),
        )
        runtime1,tick=tick_setmagicpet_runtime(runtime0)
        self.assertIsNotNone(tick)
        self.assertEqual(
            (
                runtime1.state.duck_turn,runtime1.state.str_turn,
                runtime1.state.tgh_turn,runtime1.state.dex_turn,
            ),
            (0,1,0,2),
        )
        self.assertEqual(tick.expired_kinds,("DUCK","TGH"))
        self.assertEqual(runtime1.prepared_powers,runtime0.prepared_powers)

    def test_tgh_application_is_blocked_by_duck_or_existing_stat_state(self):
        option=SetMagicPetOption(3,15,"TGH",b"TGH")
        applied,ok=apply_setmagicpet_option(
            SetMagicPetParticipantRuntime(),option
        )
        self.assertTrue(ok)
        self.assertEqual((applied.state.tgh_turn,applied.state.tgh_power),(3,15))
        for state in (
            SetMagicPetTargetState(duck_turn=1),
            SetMagicPetTargetState(str_turn=1),
            SetMagicPetTargetState(tgh_turn=1),
            SetMagicPetTargetState(dex_turn=1),
        ):
            blocked,ok=apply_setmagicpet_option(
                SetMagicPetParticipantRuntime(state),option
            )
            self.assertFalse(ok)
            self.assertEqual(blocked.state,state)

    def test_prepare_tgh_uses_baseline_toughness_basis_and_is_noncompounding(self):
        active=SetMagicPetParticipantRuntime(
            SetMagicPetTargetState(tgh_turn=2,tgh_power=15)
        )
        prepared=prepare_setmagicpet_powers(
            baseline_attack=120,baseline_defense=80,baseline_quick=60,
            runtime=active,
        )
        self.assertEqual(
            (prepared.attack,prepared.defense,prepared.dexterity),
            (120,92,60),
        )
        prepared_again=prepare_setmagicpet_powers(
            baseline_attack=120,baseline_defense=80,baseline_quick=60,
            runtime=replace(active,prepared_powers=prepared),
        )
        self.assertEqual(prepared_again,prepared)

    def test_prepare_rejects_unexecuted_str_dex_domain(self):
        for state in (
            SetMagicPetTargetState(str_turn=1,str_power=10),
            SetMagicPetTargetState(dex_turn=1,dex_power=15),
        ):
            with self.assertRaises(SetMagicPetSourceDomain):
                prepare_setmagicpet_powers(
                    baseline_attack=100,baseline_defense=80,
                    baseline_quick=60,
                    runtime=SetMagicPetParticipantRuntime(state),
                )

    def _submission(self,target=0):
        return EnemyAiSetMagicPetSubmission(
            "enemy",0,601,"PETSKILL_SetMagicPet",target,
            SetMagicPetOption(3,15,"TGH",b"TGH"),
        )

    def _round(self,*,target=0,player_first=False,player_hp=2000,
               player_magic=None,extra_players=None,
               rolls=SetMagicPetActionRolls(),enemy_status=None):
        player=actor(
            "player","player","player",
            hp=player_hp,quick=220 if player_first else 100,
            defense=80,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            quick=100 if player_first else 220,
        )
        players={0:player}
        for slot,participant in (extra_players or {}).items():
            players[int(slot)]=participant
        participants=tuple(players.values())+(enemy,)
        prepared=prepare_battle_round(
            participants,
            {
                **{
                    participant.participant_id:BattleCommand(BATTLE_COM_WAIT)
                    for participant in players.values()
                },
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=target),
            },
            {participant.participant_id:0 for participant in participants},
            tie_break_order=tuple(
                participant.participant_id for participant in participants
            ),
        )
        overlay={
            participant.participant_id:SetMagicPetParticipantRuntime()
            for participant in participants
        }
        if player_magic is not None:
            overlay["player"]=player_magic
        status={
            participant.participant_id:BaseBattleStatusRuntime()
            for participant in participants
        }
        if enemy_status is not None:
            status["enemy"]=enemy_status
        return resolve_ordinary_round(
            prepared,
            slots={
                participant.participant_id:slot
                for slot,participant in players.items()
            }|{"enemy":10},
            profiles={
                participant.participant_id:
                    BattleCombatProfile(100,0,0,0,0,0)
                for participant in participants
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            base_status_runtime_by_participant_id=status,
            setmagicpet_submissions_by_participant_id={
                "enemy":self._submission(target)
            },
            setmagicpet_rolls_by_participant_id={"enemy":rolls},
            setmagicpet_overlay=SetMagicPetRoundOverlay(overlay),
        )

    def test_round_applies_without_damage_and_same_round_target_tick_is_ordered(self):
        result=self._round(player_first=False)
        event=next(
            event for event in result.events
            if event.setmagicpet_skill_id is not None
        )
        self.assertTrue(event.setmagicpet_applied)
        self.assertEqual(event.setmagicpet_kind,"TGH")
        self.assertEqual(result.hp_by_participant_id["player"],2000)
        # Enemy acts first and applies 3; player's later StatusSeq decrements 3->2.
        magic=result.setmagicpet_overlay.runtime_by_participant_id["player"]
        self.assertEqual((magic.state.tgh_turn,magic.state.tgh_power),(2,15))

    def test_target_that_already_acted_keeps_full_three_until_next_round(self):
        result=self._round(player_first=True)
        magic=result.setmagicpet_overlay.runtime_by_participant_id["player"]
        self.assertEqual(magic.state.tgh_turn,3)

    def test_round_blocks_tgh_when_setduck_is_active(self):
        result=self._round(
            player_first=True,
            player_magic=SetMagicPetParticipantRuntime(
                SetMagicPetTargetState(duck_turn=2)
            ),
        )
        event=next(
            event for event in result.events
            if event.setmagicpet_skill_id is not None
        )
        self.assertFalse(event.setmagicpet_applied)
        self.assertEqual(
            result.setmagicpet_overlay.runtime_by_participant_id[
                "player"
            ].state.tgh_turn,
            0,
        )

    def test_dead_single_target_uses_only_explicit_multilist_rng(self):
        pet=actor("pet","player","pet")
        result=self._round(
            target=0,player_hp=0,extra_players={1:pet},
            rolls=SetMagicPetActionRolls((0,)),
        )
        event=next(
            event for event in result.events
            if event.setmagicpet_skill_id is not None
        )
        self.assertEqual(event.resolved_target_slot,1)
        self.assertTrue(event.retargeted)

    def test_live_target_rejects_unused_setmagicpet_rng(self):
        with self.assertRaisesRegex(ValueError,"live single target"):
            self._round(rolls=SetMagicPetActionRolls((0,)))

    def test_persistent_postround_prepares_tgh_for_next_command(self):
        player=actor(
            "player","player","player",defense=80,quick=100
        )
        enemy=actor("enemy","enemy","enemy",quick=220)
        session=BattleSession(player=player,allied_pets=(),enemies=(enemy,))
        state=begin_persistent_battle(
            session,
            slots={"player":0,"enemy":10},
            setmagicpet_overlay=SetMagicPetRoundOverlay({
                "player":SetMagicPetParticipantRuntime(),
                "enemy":SetMagicPetParticipantRuntime(),
            }),
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                pid:BattleCombatProfile(100,0,0,0,0,0)
                for pid in ("player","enemy")
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            setmagicpet_submissions_by_participant_id={
                "enemy":self._submission(0)
            },
            setmagicpet_rolls_by_participant_id={
                "enemy":SetMagicPetActionRolls()
            },
        )
        magic=result.after.setmagicpet_overlay.runtime_by_participant_id[
            "player"
        ]
        self.assertEqual(magic.state.tgh_turn,2)
        self.assertEqual(magic.prepared_powers.defense,92)
        self.assertEqual(participant_snapshot(result.after,"player").defense,92)

    def test_overlay_is_exact_participant_mapping_type(self):
        overlay=SetMagicPetRoundOverlay({
            "p":SetMagicPetParticipantRuntime(),
        })
        self.assertIn("p",overlay.runtime_by_participant_id)
        with self.assertRaises(TypeError):
            SetMagicPetRoundOverlay({"p":object()})


if __name__=="__main__":
    unittest.main()
