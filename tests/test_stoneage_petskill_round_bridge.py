import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_GUARD,
    BATTLE_COM_S_GUARDIAN_ATTACK,
    BATTLE_COM_S_MIGHTY,
    BATTLE_COM_S_POWERBALANCE,
    BATTLE_COM_S_STATUSCHANGE,
    battle_command3_high,
    battle_command3_low,
)
from tools.stoneage_petskill_core_model import (
    guardian_command,
    mighty_command,
    power_balance_command,
    status_change_command,
)
from tools.stoneage_petskill_round_bridge import (
    bridge_stable_pet_skill_command,
)


STATUS=("NONE","POISON","PARALYSIS","SLEEP","STONE","DRUNK","CONFUSION")


class PetSkillRoundBridgeTests(unittest.TestCase):
    def test_guardian_attack_carries_command_registration_and_power(self):
        payload=guardian_command(
            10,
            "攻%10 防%25",
            fixed_attack=1000,
            fixed_defense=800,
            battle_slot=5,
            battle_side=0,
        )
        submission=bridge_stable_pet_skill_command(payload,actor_slot=5)
        self.assertEqual(
            submission.battle_command.command1,
            BATTLE_COM_S_GUARDIAN_ATTACK,
        )
        self.assertEqual(submission.battle_command.command2,10)
        self.assertEqual(submission.setup_effects.attack_power,1100)
        self.assertEqual(submission.setup_effects.defense_power,1000)
        self.assertTrue(submission.setup_effects.guardian_flag)
        self.assertEqual(submission.setup_effects.guardian_for_slot,0)

    def test_defensive_guardian_stays_plain_guard_with_side_effect_registration(self):
        payload=guardian_command(
            3,
            "COM:防御 防%20",
            fixed_attack=1000,
            fixed_defense=800,
            battle_slot=5,
            battle_side=0,
        )
        submission=bridge_stable_pet_skill_command(payload,actor_slot=5)
        self.assertEqual(submission.battle_command.command1,BATTLE_COM_GUARD)
        self.assertEqual(submission.battle_command.command2,3)
        self.assertEqual(submission.setup_effects.defense_power,960)
        self.assertEqual(submission.setup_effects.guardian_for_slot,3)

    def test_mighty_packs_damage_multiplier_and_dodge_modifier(self):
        payload=mighty_command(10, "倍2.5 回避20")
        submission=bridge_stable_pet_skill_command(payload)
        command=submission.battle_command
        self.assertEqual(command.command1,BATTLE_COM_S_MIGHTY)
        self.assertEqual(command.command2,10)
        self.assertEqual(battle_command3_low(command.command3),250)
        self.assertEqual(battle_command3_high(command.command3),20)

    def test_powerbalance_carries_work_attack_and_defense_into_round(self):
        payload=power_balance_command(
            10,
            "攻%25 防%-35",
            fixed_attack=1000,
            fixed_defense=800,
        )
        submission=bridge_stable_pet_skill_command(payload)
        self.assertEqual(
            submission.battle_command.command1,
            BATTLE_COM_S_POWERBALANCE,
        )
        self.assertEqual(submission.battle_command.command2,10)
        self.assertEqual(submission.setup_effects.attack_power,1250)
        self.assertEqual(submission.setup_effects.defense_power,520)

    def test_statuschange_packs_low_status_and_high_turn_exactly(self):
        payload=status_change_command(
            10,
            "STONE turn4 攻%25 防%-10",
            STATUS,
            fixed_attack=1000,
            fixed_defense=800,
        )
        submission=bridge_stable_pet_skill_command(payload)
        command=submission.battle_command
        self.assertEqual(command.command1,BATTLE_COM_S_STATUSCHANGE)
        self.assertEqual(command.command2,10)
        self.assertEqual(battle_command3_low(command.command3),4)
        self.assertEqual(battle_command3_high(command.command3),4)
        self.assertEqual(submission.setup_effects.attack_power,1250)
        self.assertEqual(submission.setup_effects.defense_power,720)

    def test_guardian_slot_drift_is_rejected(self):
        payload=guardian_command(
            10,
            "",
            fixed_attack=1000,
            fixed_defense=800,
            battle_slot=5,
            battle_side=0,
        )
        with self.assertRaises(ValueError):
            bridge_stable_pet_skill_command(payload,actor_slot=6)

    def test_rejected_or_unmodeled_payload_fails_closed(self):
        with self.assertRaises(ValueError):
            bridge_stable_pet_skill_command(
                {"accepted":False,"command":"S_STATUSCHANGE","target":10}
            )
        with self.assertRaises(ValueError):
            bridge_stable_pet_skill_command(
                {"accepted":True,"command":"S_MIGHTY","target":10}
            )


if __name__=="__main__":
    unittest.main()
