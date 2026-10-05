import unittest
from dataclasses import dataclass

from tools.stoneage_combined_direct_magic_model import RuntimeItemZeroWitness
from tools.stoneage_combined_initiative_model import (
    PROFILE_BISMARCK_FIXED15, PROFILE_GAVIN_IRIS_30PCT,
)
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls, CombinedRuntimeOverlay,
    STATUS_MAGIC_PROFILE_IRIS_CP950,
)


@dataclass(frozen=True)
class Profile:
    earth:int=10
    water:int=20
    fire:int=30
    wind:int=40


def overlay(*,profile=PROFILE_GAVIN_IRIS_30PCT,reversed_player=False):
    return CombinedRuntimeOverlay(
        profile,STATUS_MAGIC_PROFILE_IRIS_CP950,
        RuntimeItemZeroWitness(True,5),
        {"enemy":20},
        {"player":reversed_player,"enemy":False},
    )


class CombinedRuntimeStateTests(unittest.TestCase):
    def test_profiles_and_item_witness_are_explicit(self):
        for profile in ("","original"):
            with self.assertRaisesRegex(ValueError,"initiative profile"):
                overlay(profile=profile)
        with self.assertRaisesRegex(ValueError,"status-magic profile"):
            CombinedRuntimeOverlay(
                PROFILE_BISMARCK_FIXED15,"original",
                RuntimeItemZeroWitness(True,0),{"enemy":1},
                {"player":False,"enemy":False},
            )

    def test_action_rolls_validate_only_owned_ranges(self):
        rolls=CombinedActionRolls((0,9),90,100)
        self.assertEqual(rolls.retarget_draws_0_9,(0,9))
        with self.assertRaisesRegex(ValueError,"0..9"):
            CombinedActionRolls((10,))
        with self.assertRaisesRegex(ValueError,"90..110"):
            CombinedActionRolls(recovery_roll_90_110=111)
        with self.assertRaisesRegex(ValueError,"1..100"):
            CombinedActionRolls(status_roll_1_100=0)

    def test_participant_coverage_keeps_reverse_complete_but_mp_sparse(self):
        overlay().validate_participants(("player","enemy"))
        with self.assertRaisesRegex(ValueError,"participant mismatch"):
            CombinedRuntimeOverlay(
                PROFILE_GAVIN_IRIS_30PCT,STATUS_MAGIC_PROFILE_IRIS_CP950,
                RuntimeItemZeroWitness(True,0),{"enemy":1},{"enemy":False},
            ).validate_participants(("player","enemy"))

    def test_mp_updates_are_persistent_and_fail_closed_when_absent(self):
        row=overlay().with_mp("enemy",15)
        self.assertEqual(row.mp_by_participant_id["enemy"],15)
        with self.assertRaises(KeyError):
            row.with_mp("player",1)

    def test_reverse_cast_on_swaps_now_and_persists_flag(self):
        row=overlay()
        row2,attrs=row.cast_att_reverse("player",Profile())
        self.assertTrue(row2.att_reverse_by_participant_id["player"])
        self.assertEqual(
            (attrs["earth"],attrs["water"],attrs["fire"],attrs["wind"]),
            (30,40,10,20),
        )
        pre=row2.precommand_elements("player",Profile())
        self.assertEqual((pre["earth"],pre["water"],pre["fire"],pre["wind"]),(30,40,10,20))

    def test_reverse_cast_off_keeps_same_round_attrs_until_next_precommand(self):
        row=overlay(reversed_player=True)
        reversed_attrs=row.precommand_elements("player",Profile())
        current=Profile(**reversed_attrs)
        row2,attrs=row.cast_att_reverse("player",current)
        self.assertFalse(row2.att_reverse_by_participant_id["player"])
        self.assertEqual((attrs["earth"],attrs["water"],attrs["fire"],attrs["wind"]),(30,40,10,20))
        pre=row2.precommand_elements("player",Profile())
        self.assertEqual((pre["earth"],pre["water"],pre["fire"],pre["wind"]),(10,20,30,40))


if __name__=="__main__":
    unittest.main()
