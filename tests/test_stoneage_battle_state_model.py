import unittest
from dataclasses import replace

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
)
from tools.stoneage_battle_state_model import (
    ACTIVE,
    ENEMY_WIN,
    FINISHED,
    PLAYER_WIN,
    begin_persistent_battle,
    living_non_pet_count,
    resolve_persistent_ordinary_round,
    termination_result,
)
from tools.stoneage_singleplayer_battle import (
    BattleParticipant,
    BattleSession,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def participant(
    pid,
    side,
    kind,
    *,
    hp=100,
    attack=100,
    defense=70,
    quick=50,
    level=10,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
    )


def session(player, enemies, pets=()):
    encounter = EncounterRequest(
        position=MapPosition(2000, 10, 10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=max(1, len(enemies)),
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=tuple(pets),
        enemies=tuple(enemies),
    )


def profile():
    return BattleCombatProfile(
        fixed_dex=100,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


class PersistentBattleStateTests(unittest.TestCase):
    def test_two_rounds_preserve_hp_and_increment_turn(self):
        player = participant("player", "player", "player", attack=60, quick=100)
        enemy = participant("enemy", "enemy", "enemy", hp=200, defense=70, quick=40)
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        self.assertEqual(state.phase, ACTIVE)
        self.assertEqual(state.turn, 0)

        first = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=1,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(first.after.turn, 1)
        self.assertEqual(first.after.phase, ACTIVE)
        first_hp = first.after.hp_by_participant_id["enemy"]
        self.assertLess(first_hp, 200)

        second = resolve_persistent_ordinary_round(
            first.after,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=1,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(second.after.turn, 2)
        self.assertLess(second.after.hp_by_participant_id["enemy"], first_hp)

    def test_player_death_finishes_even_if_allied_pet_is_alive(self):
        player = participant("player", "player", "player", hp=30, quick=40)
        pet = participant("pet:0", "player", "pet", hp=100, quick=30)
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=100, attack=200, defense=20, quick=100,
        )
        state = begin_persistent_battle(
            session(player, (enemy,), pets=(pet,)),
            slots={"player": 0, "pet:0": 1, "enemy": 10},
        )
        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_WAIT),
                "pet:0": BattleCommand(BATTLE_COM_WAIT),
                "enemy": BattleCommand(BATTLE_COM_ATTACK, command2=0),
            },
            initiative_random_subtracts={"player": 0, "pet:0": 0, "enemy": 0},
            profiles={
                "player": profile(),
                "pet:0": profile(),
                "enemy": profile(),
            },
            attack_rolls={
                "enemy": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.hp_by_participant_id["player"], 0)
        self.assertEqual(result.after.hp_by_participant_id["pet:0"], 100)
        self.assertEqual(living_non_pet_count(result.after, 0), 0)
        self.assertEqual(result.after.phase, FINISHED)
        self.assertEqual(result.after.result, ENEMY_WIN)
        self.assertEqual(result.after.winning_side, 1)

    def test_last_enemy_death_finishes_with_player_victory(self):
        player = participant(
            "player", "player", "player",
            attack=200, quick=100,
        )
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=30, defense=20, quick=40,
        )
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.hp_by_participant_id["enemy"], 0)
        self.assertEqual(living_non_pet_count(result.after, 1), 0)
        self.assertEqual(result.after.phase, FINISHED)
        self.assertEqual(result.after.result, PLAYER_WIN)
        self.assertEqual(result.after.winning_side, 0)

        with self.assertRaisesRegex(ValueError, "after battle termination"):
            resolve_persistent_ordinary_round(
                result.after,
                commands={},
                initiative_random_subtracts={},
                profiles={},
                attack_rolls={},
                defense_profile="newpower_70pct",
            )

    def test_source_side_check_order_preserves_enemy_win_if_both_are_zero(self):
        player = participant("player", "player", "player", hp=1)
        enemy = participant("enemy", "enemy", "enemy", hp=1)
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        zero = replace(
            state,
            hp_by_participant_id={"player": 0, "enemy": 0},
        )
        self.assertEqual(living_non_pet_count(zero, 0), 0)
        self.assertEqual(living_non_pet_count(zero, 1), 0)
        self.assertEqual(termination_result(zero), (ENEMY_WIN, 1))


if __name__ == "__main__":
    unittest.main()
