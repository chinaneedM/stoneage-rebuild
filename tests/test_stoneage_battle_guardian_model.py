import unittest

from tools.stoneage_battle_guardian_model import (
    GuardianRegistration,
    guardian_redirect_allowed,
)


class BattleGuardianModelTests(unittest.TestCase):
    def test_registration_validates_slot_and_barrier(self):
        self.assertEqual(GuardianRegistration(5).guardian_slot,5)
        with self.assertRaises(ValueError):
            GuardianRegistration(20)
        with self.assertRaises(ValueError):
            GuardianRegistration(5,guardian_barrier=-1)

    def test_healthy_flagged_guardian_redirects_without_rng(self):
        self.assertTrue(
            guardian_redirect_allowed(
                guardian_exists=True,
                guardian_slot=5,
                defender_slot=0,
                guardian_alive=True,
                guardian_flag=True,
            )
        )

    def test_source_rejection_gates(self):
        base=dict(
            guardian_exists=True,
            guardian_slot=5,
            defender_slot=0,
            guardian_alive=True,
            guardian_flag=True,
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_sleep=1)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_confusion=1)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_paralysis=1)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_stone=1)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_barrier=1)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base,guardian_is_attacker=True)
        )
        self.assertFalse(
            guardian_redirect_allowed(
                **base,attacker_uses_throw_weapon=True
            )
        )

    def test_missing_dead_or_self_registered_guardian_rejects(self):
        self.assertFalse(
            guardian_redirect_allowed(
                guardian_exists=False,
                guardian_slot=5,
                defender_slot=0,
                guardian_alive=True,
                guardian_flag=True,
            )
        )
        self.assertFalse(
            guardian_redirect_allowed(
                guardian_exists=True,
                guardian_slot=5,
                defender_slot=0,
                guardian_alive=False,
                guardian_flag=True,
            )
        )
        self.assertFalse(
            guardian_redirect_allowed(
                guardian_exists=True,
                guardian_slot=0,
                defender_slot=0,
                guardian_alive=True,
                guardian_flag=True,
            )
        )


if __name__ == "__main__":
    unittest.main()
