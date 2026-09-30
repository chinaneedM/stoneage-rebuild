import unittest

from tools.stoneage_enemy_ai_petskill_bridge import (
    resolve_enemy_ai_basic_petskill_command,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
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
    participant = BattleParticipant(
        participant_id="enemy:0",
        side="enemy",
        kind="enemy",
        level=5,
        hp=100,
        max_hp=100,
        attack=20,
        defense=20,
        quick=20,
        name=None,
    )
    return SpawnedEnemy(
        spawn_index=0,
        variant=variant,
        template=template,
        birth=object(),
        participant=participant,
    )


def entry(skill_id, callback):
    return Recovered25PetSkillEntry(
        skill_id=skill_id,
        field=1,
        target=3,
        cost=2,
        illegal=0,
        function_name=callback,
        option_bytes=b"",
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
