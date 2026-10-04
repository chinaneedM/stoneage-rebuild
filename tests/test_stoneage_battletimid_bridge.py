from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_enemy_ai_battletimid_bridge import (
    EnemyAiBattleTimidSubmission,
    resolve_enemy_ai_battletimid_submission,
)
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry


def spawned(slot_ids=(606,0,0,0,0,0,0)):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy"),
        template=SimpleNamespace(skill_slot_ids=slot_ids),
    )


def runtime(entry=None):
    entry=entry or Recovered25PetSkillEntry(
        606,1,6,2,3000,"PETSKILL_BattleTimid",b""
    )
    return SimpleNamespace(skills={606:entry})


class BattleTimidBridgeTests(unittest.TestCase):
    def test_exact_id606_submission_and_fixed_setup(self):
        result=resolve_enemy_ai_battletimid_submission(
            spawned(),
            skill_slot=0,
            target_slot=1,
            petskill_runtime=runtime(),
            fixed_strength=101,
            fixed_toughness=99,
            fixed_dex=103,
        )
        self.assertIsInstance(result,EnemyAiBattleTimidSubmission)
        self.assertEqual(result.participant_id,"enemy")
        self.assertEqual(result.skill_id,606)
        self.assertEqual(result.source_target_slot,1)
        self.assertEqual(
            (
                result.setup.attack_power,
                result.setup.defence_power,
                result.setup.quick,
            ),
            (70,39,82),
        )
        self.assertEqual(result.setup.packed_com3,0)

    def test_post_damage_preserves_strict_threshold_and_target_kind(self):
        submission=resolve_enemy_ai_battletimid_submission(
            spawned(),skill_slot=0,target_slot=0,petskill_runtime=runtime(),
            fixed_strength=100,fixed_toughness=100,fixed_dex=100,
        )
        pet=submission.post_damage(draw=14,damage=2,target_is_pet=True)
        self.assertTrue(pet.forced_exit)
        self.assertTrue(pet.pet_default_exit)
        self.assertTrue(pet.owner_default_pet_cleared)
        self.assertFalse(pet.player_battle_exit)
        player=submission.post_damage(draw=14,damage=2,target_is_pet=False)
        self.assertTrue(player.player_battle_exit)
        self.assertTrue(player.party_discharged)
        self.assertFalse(submission.post_damage(
            draw=15,damage=2,target_is_pet=False
        ).forced_exit)
        self.assertFalse(submission.post_damage(
            draw=0,damage=1,target_is_pet=False
        ).forced_exit)

    def test_exact_metadata_and_empty_option_are_required(self):
        base=Recovered25PetSkillEntry(
            606,1,6,2,3000,"PETSKILL_BattleTimid",b""
        )
        for kw in (
            {"field":2},
            {"target":1},
            {"cost":3},
            {"illegal":0},
            {"option_bytes":b"0"},
            {"function_name":"PETSKILL_NormalAttack"},
        ):
            with self.subTest(kw=kw):
                bad=replace(base,**kw)
                with self.assertRaises(ValueError):
                    resolve_enemy_ai_battletimid_submission(
                        spawned(),skill_slot=0,target_slot=0,
                        petskill_runtime=runtime(bad),
                        fixed_strength=100,fixed_toughness=100,fixed_dex=100,
                    )

    def test_population_slot_and_target_domain_are_fail_closed(self):
        good=runtime()
        with self.assertRaises(ValueError):
            resolve_enemy_ai_battletimid_submission(
                spawned((0,606,0,0,0,0,0)),
                skill_slot=0,target_slot=0,petskill_runtime=good,
                fixed_strength=100,fixed_toughness=100,fixed_dex=100,
            )
        with self.assertRaises(ValueError):
            resolve_enemy_ai_battletimid_submission(
                spawned(),skill_slot=0,target_slot=10,petskill_runtime=good,
                fixed_strength=100,fixed_toughness=100,fixed_dex=100,
            )
        extra=SimpleNamespace(skills={
            606:good.skills[606],
            607:replace(good.skills[606],skill_id=607),
        })
        with self.assertRaises(ValueError):
            resolve_enemy_ai_battletimid_submission(
                spawned(),skill_slot=0,target_slot=0,petskill_runtime=extra,
                fixed_strength=100,fixed_toughness=100,fixed_dex=100,
            )


if __name__=="__main__":
    unittest.main()
