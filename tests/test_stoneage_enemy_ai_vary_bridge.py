import unittest
from types import SimpleNamespace

from tools.stoneage_enemy_ai_vary_bridge import (
    PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
    resolve_enemy_ai_vary_submission,
    validate_recovered25_vary_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


OPTION = bytes.fromhex(
    "a7f0c0bb2533302e302520a8bea4e7252d35302e302520b1d32533302e30"
)


def runtime(option=OPTION, target=5):
    entry = Recovered25PetSkillEntry(
        skill_id=600,
        field=1,
        target=target,
        cost=2,
        illegal=1000,
        function_name="PETSKILL_Vary",
        option_bytes=option,
    )
    return Recovered25PetSkillRuntime({600: entry}, "petskill.txt")


def spawned(tempno=981, graphic=101427, slot_value=600):
    slots = [0] * 7
    slots[2] = slot_value
    return SimpleNamespace(
        template=SimpleNamespace(
            tempno=tempno,
            graphic_id=graphic,
            skill_slot_ids=tuple(slots),
        ),
        participant=SimpleNamespace(
            participant_id="enemy-vary",
            side="enemy",
            kind="enemy",
        ),
    )


class EnemyAiVaryBridgeTests(unittest.TestCase):
    def test_exact_population_and_option_hash_are_required(self):
        validate_recovered25_vary_population(runtime())
        with self.assertRaisesRegex(ValueError, "metadata"):
            validate_recovered25_vary_population(runtime(target=6))
        bad = bytearray(OPTION)
        bad[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "hash"):
            validate_recovered25_vary_population(runtime(bytes(bad)))

    def test_submission_is_target_none_but_preserves_source_carrier(self):
        row = resolve_enemy_ai_vary_submission(
            spawned(),
            skill_slot=2,
            target_carrier=7,
            petskill_runtime=runtime(),
            profile=PROFILE_GAVIN_IRIS_ATTACK_QUICK,
            fixed_attack=100,
            fixed_defense=80,
            fixed_quick=90,
        )
        self.assertEqual(row.skill_id, 600)
        self.assertEqual(row.skill_slot, 2)
        self.assertEqual(row.source_target_carrier, 7)
        self.assertEqual(row.runtime_after_callback.base_image, 101428)
        self.assertEqual(
            (
                row.runtime_after_callback.attack_power,
                row.runtime_after_callback.defense_power,
                row.runtime_after_callback.quick,
            ),
            (130, 80, 117),
        )

    def test_bismarck_profile_is_explicit_not_silently_promoted(self):
        row = resolve_enemy_ai_vary_submission(
            spawned(),
            skill_slot=2,
            target_carrier=0,
            petskill_runtime=runtime(),
            profile=PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
            fixed_attack=100,
            fixed_defense=80,
            fixed_quick=90,
        )
        self.assertEqual(row.runtime_after_callback.defense_power, 40)
        self.assertFalse(row.runtime_after_callback.visual_effect_enabled)

    def test_wrong_template_slot_graphic_or_profile_fails_closed(self):
        common = dict(
            skill_slot=2,
            target_carrier=0,
            petskill_runtime=runtime(),
            profile=PROFILE_GAVIN_IRIS_ATTACK_QUICK,
            fixed_attack=100,
            fixed_defense=80,
            fixed_quick=90,
        )
        with self.assertRaisesRegex(ValueError, "PETSKILL3"):
            resolve_enemy_ai_vary_submission(spawned(slot_value=0), **common)
        with self.assertRaisesRegex(ValueError, "graphic"):
            resolve_enemy_ai_vary_submission(spawned(graphic=1), **common)
        with self.assertRaisesRegex(ValueError, "profile"):
            resolve_enemy_ai_vary_submission(
                spawned(), **{**common, "profile": "original"}
            )

    def test_all_four_recovered_wolves_are_admitted_with_exact_graphics(self):
        graphics = {981: 101427, 982: 101424, 983: 101425, 984: 101426}
        for tempno, graphic in graphics.items():
            row = resolve_enemy_ai_vary_submission(
                spawned(tempno=tempno, graphic=graphic),
                skill_slot=2,
                target_carrier=0,
                petskill_runtime=runtime(),
                profile=PROFILE_GAVIN_IRIS_ATTACK_QUICK,
                fixed_attack=1,
                fixed_defense=1,
                fixed_quick=1,
            )
            self.assertEqual(row.runtime_after_callback.tempno, tempno)


if __name__ == "__main__":
    unittest.main()
