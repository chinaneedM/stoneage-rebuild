import unittest

from tools.stoneage_enemy_ai_petskill_bridge import (
    resolve_enemy_ai_basic_petskill_command,
    resolve_enemy_ai_mighty_petskill_command,
    resolve_enemy_ai_powerbalance_petskill_command,
    resolve_enemy_ai_statuschange_petskill_command,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_tw10_25_bridge_model import (
    PetTemplateBridge,
    build_pet_birth_bridge,
)
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BATTLE_COM_S_MIGHTY,
    BATTLE_COM_S_POWERBALANCE,
    BATTLE_COM_S_STATUSCHANGE,
    battle_command3_high,
    battle_command3_low,
)


def spawned_with_slots(slots):
    template = PetTemplateBridge.from_enemybase(
        {
            "TEMPNO": 88,
            "INITNUM": 1,
            "LVUPPOINT": 5,
            "BASEVITAL": 20,
            "BASESTR": 20,
            "BASETGH": 20,
            "BASEDEX": 20,
            "MODAI": 0,
            "GET": 0,
            "EARTHAT": 50,
            "WATERAT": 50,
            "FIREAT": 0,
            "WINDAT": 0,
            "SLOT": 4,
            "IMGNUMBER": 1,
            "SIZE": 0,
            **{
                f"PETSKILL{index}": value
                for index, value in enumerate(slots, 1)
            },
        }
    )
    variant = EnemyVariantBridge.from_enemy(
        {
            "ID": 700,
            "TEMPNO": 88,
            "LV_MIN": 5,
            "LV_MAX": 5,
            "CREATEMAXNUM": 1,
            "CREATEMINNUM": 1,
            "TACTICS": 1,
            "EXP": 100,
            "DUELPOINT": 0,
            "STYLE": 0,
            "PETFLG": 1,
        }
    )
    birth = build_pet_birth_bridge(
        template,
        level=5,
        birth_offsets=(0, 0, 0, 0),
        spawn_allocation_rolls=(0, 1, 2, 3, 0, 1, 2, 3, 0, 1),
    )
    projection = birth.combat_projection()
    participant = BattleParticipant(
        participant_id="enemy:0",
        side="enemy",
        kind="enemy",
        level=5,
        hp=projection["hp"],
        max_hp=projection["max_hp"],
        attack=projection["attack"],
        defense=projection["defense"],
        quick=projection["quick"],
        name=None,
    )
    return SpawnedEnemy(
        spawn_index=0,
        variant=variant,
        template=template,
        birth=birth,
        participant=participant,
    )


def entry(skill_id, callback, option=b""):
    return Recovered25PetSkillEntry(
        skill_id=skill_id,
        field=1,
        target=3,
        cost=2,
        illegal=0,
        function_name=callback,
        option_bytes=option,
    )


class EnemyAiPetSkillBridgeTests(unittest.TestCase):
    def test_sparse_slot_identity_is_not_compacted(self):
        spawned = spawned_with_slots((0, 10, 20, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                10: entry(10, "PETSKILL_NormalAttack"),
                20: entry(20, "PETSKILL_NormalGuard"),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "empty pet-skill slot 0"):
            resolve_enemy_ai_basic_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

        attack = resolve_enemy_ai_basic_petskill_command(
            spawned,
            skill_slot=1,
            target_slot=3,
            petskill_runtime=runtime,
        )
        self.assertEqual(attack.skill_id, 10)
        self.assertEqual(attack.command.command1, BATTLE_COM_ATTACK)
        self.assertEqual(attack.command.command2, 3)

        guard = resolve_enemy_ai_basic_petskill_command(
            spawned,
            skill_slot=2,
            target_slot=4,
            petskill_runtime=runtime,
        )
        self.assertEqual(guard.skill_id, 20)
        self.assertEqual(guard.command.command1, BATTLE_COM_GUARD)
        self.assertEqual(guard.command.command2, 4)

    def test_none_skill_keeps_source_no_action_command(self):
        spawned = spawned_with_slots((30, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                30: entry(30, "PETSKILL_None"),
            },
            source_file="petskill.txt",
        )
        resolved = resolve_enemy_ai_basic_petskill_command(
            spawned,
            skill_slot=0,
            target_slot=4,
            petskill_runtime=runtime,
        )
        self.assertEqual(resolved.skill_id, 30)
        self.assertEqual(resolved.command.command1, BATTLE_COM_NONE)
        self.assertEqual(resolved.command.command2, 4)

    def test_mighty_uses_recovered_option_and_round_bridge(self):
        spawned = spawned_with_slots((60, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                60: entry(
                    60,
                    "PETSKILL_Mighty",
                    "倍2 回避30".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        resolved = resolve_enemy_ai_mighty_petskill_command(
            spawned,
            skill_slot=0,
            target_slot=3,
            petskill_runtime=runtime,
        )
        self.assertEqual(resolved.command.command1, BATTLE_COM_S_MIGHTY)
        self.assertEqual(resolved.command.command2, 3)
        self.assertEqual(battle_command3_low(resolved.command.command3), 200)
        self.assertEqual(battle_command3_high(resolved.command.command3), 30)

    def test_mighty_rejects_unclosed_option_marker_grammar(self):
        spawned = spawned_with_slots((60, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                60: entry(
                    60,
                    "PETSKILL_Mighty",
                    "倍2".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "outside closed"):
            resolve_enemy_ai_mighty_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_mighty_rejects_malformed_numeric_option(self):
        spawned = spawned_with_slots((60, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                60: entry(
                    60,
                    "PETSKILL_Mighty",
                    "倍x 回避30".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "numeric grammar"):
            resolve_enemy_ai_mighty_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_powerbalance_uses_recovered_option_birth_fix_stats_and_round_bridge(self):
        spawned = spawned_with_slots((50, 0, 0, 0, 0, 0, 0))
        option = "攻%25 防%-35".encode("cp950")
        runtime = Recovered25PetSkillRuntime(
            skills={
                50: entry(50, "PETSKILL_PowerBalance", option),
            },
            source_file="petskill.txt",
        )
        resolved = resolve_enemy_ai_powerbalance_petskill_command(
            spawned,
            skill_slot=0,
            target_slot=3,
            petskill_runtime=runtime,
        )
        projection = spawned.birth.combat_projection()
        self.assertEqual(resolved.command.command1, BATTLE_COM_S_POWERBALANCE)
        self.assertEqual(resolved.command.command2, 3)
        self.assertEqual(
            resolved.setup_effects.attack_power,
            projection["attack"] + int(projection["attack"] * 25 / 100),
        )
        self.assertEqual(
            resolved.setup_effects.defense_power,
            projection["defense"] + int(projection["defense"] * -35 / 100),
        )

    def test_powerbalance_rejects_unclosed_dex_extension_marker(self):
        spawned = spawned_with_slots((50, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                50: entry(
                    50,
                    "PETSKILL_PowerBalance",
                    "攻%25 防%-35 敏%10".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "outside closed"):
            resolve_enemy_ai_powerbalance_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_statuschange_uses_recovered_option_birth_fix_stats_and_round_bridge(self):
        spawned = spawned_with_slots((40, 0, 0, 0, 0, 0, 0))
        option = "毒turn4 攻%25 防%-10".encode("cp950")
        runtime = Recovered25PetSkillRuntime(
            skills={
                40: entry(40, "PETSKILL_StatusChange", option),
            },
            source_file="petskill.txt",
        )
        resolved = resolve_enemy_ai_statuschange_petskill_command(
            spawned,
            skill_slot=0,
            target_slot=3,
            petskill_runtime=runtime,
        )
        projection = spawned.birth.combat_projection()
        self.assertEqual(resolved.command.command1, BATTLE_COM_S_STATUSCHANGE)
        self.assertEqual(resolved.command.command2, 3)
        self.assertEqual(battle_command3_low(resolved.command.command3), 1)
        self.assertEqual(battle_command3_high(resolved.command.command3), 4)
        self.assertEqual(
            resolved.setup_effects.attack_power,
            projection["attack"] + int(projection["attack"] * 25 / 100),
        )
        self.assertEqual(
            resolved.setup_effects.defense_power,
            projection["defense"] + int(projection["defense"] * -10 / 100),
        )

    def test_statuschange_rejects_ambiguous_option_codec(self):
        spawned = spawned_with_slots((40, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                40: entry(
                    40,
                    "PETSKILL_StatusChange",
                    b"\xA1\x45",
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "decoding divergence"):
            resolve_enemy_ai_statuschange_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_statuschange_rejects_unmatched_status_grammar(self):
        spawned = spawned_with_slots((40, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                40: entry(
                    40,
                    "PETSKILL_StatusChange",
                    b"turn4",
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "does not match"):
            resolve_enemy_ai_statuschange_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_non_basic_stable_callback_fails_closed(self):
        spawned = spawned_with_slots((30, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={
                30: entry(30, "PETSKILL_ContinuationAttack"),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(
            ValueError,
            "outside basic execution subset",
        ):
            resolve_enemy_ai_basic_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )

    def test_unresolved_skill_id_fails_closed(self):
        spawned = spawned_with_slots((99, 0, 0, 0, 0, 0, 0))
        runtime = Recovered25PetSkillRuntime(
            skills={10: entry(10, "PETSKILL_NormalAttack")},
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError, "unresolved pet-skill ID 99"):
            resolve_enemy_ai_basic_petskill_command(
                spawned,
                skill_slot=0,
                target_slot=0,
                petskill_runtime=runtime,
            )


if __name__ == "__main__":
    unittest.main()
