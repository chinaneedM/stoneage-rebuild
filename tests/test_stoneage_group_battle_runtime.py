import unittest
from dataclasses import replace
from types import MappingProxyType

from tools.stoneage_battle_command_model import ATTACK, WAIT
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
)
from tools.stoneage_battle_state_model import FINISHED, PLAYER_WIN
from tools.stoneage_enemy_spawn_model import EnemyBirthRolls
from tools.stoneage_singleplayer_domain import (
    EnemyVariantId,
    HistoricalStaticData,
    MapPosition,
    PetActor,
    PetSlot,
    PetTemplateId,
    PlayerState,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_runtime import SinglePlayerHistoricalRuntime
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def enemy(enemy_id, tempno, level):
    return EnemyVariantBridge.from_enemy(
        {
            "ID": enemy_id,
            "TEMPNO": tempno,
            "LV_MIN": level,
            "LV_MAX": level,
            "CREATEMAXNUM": 1,
            "CREATEMINNUM": 1,
            "TACTICS": 1,
            "EXP": 100,
            "DUELPOINT": 0,
            "STYLE": 0,
            "PETFLG": 1,
        }
    )


def template(tempno, name, size=0):
    return PetTemplateBridge.from_enemybase(
        {
            "NAME": name,
            "TEMPNO": tempno,
            "INITNUM": 100,
            "LVUPPOINT": 5,
            "BASEVITAL": 20,
            "BASESTR": 20,
            "BASETGH": 20,
            "BASEDEX": 20,
            "IMGNUMBER": 10000 + tempno,
            "MODAI": 4,
            "EARTHAT": 50,
            "WATERAT": 50,
            "FIREAT": 0,
            "WINDAT": 0,
            "SLOT": 4,
            "SIZE": size,
        }
    )


def player_state():
    return PlayerState(
        MappingProxyType(
            {
                "hp": 100,
                "max_hp": 100,
                "mp": 50,
                "max_mp": 50,
                "vital": 40,
                "strength": 40,
                "toughness": 35,
                "dexterity": 30,
                "exp": 0,
                "max_exp": 1000,
                "level": 5,
                "attack": 100,
                "defense": 80,
                "quick": 60,
                "charm": 0,
                "luck": 7,
                "earth": 50,
                "water": 50,
                "fire": 0,
                "wind": 0,
                "name": "Hero",
            }
        )
    )


def allied_pet():
    return PetActor(
        slot=PetSlot(2),
        variant_id=EnemyVariantId(701),
        template_id=PetTemplateId(89),
        runtime_object_id=None,
        state=MappingProxyType(
            {
                "hp": 60,
                "max_hp": 60,
                "mp": 20,
                "max_mp": 20,
                "exp": 10,
                "max_exp": 500,
                "level": 4,
                "attack": 50,
                "defense": 45,
                "quick": 40,
                "name": "Ally",
            }
        ),
        skills=(),
    )


class GroupEncounterBattleRuntimeTests(unittest.TestCase):
    def setUp(self):
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21,
                "FLOOR": 2000,
                "X1": 0,
                "Y1": 0,
                "X2": 20,
                "Y2": 20,
                "PROB_MIN": 10,
                "PROB_MAX": 20,
                "ENEMY_MAX": 2,
                "ZORDER": 1,
                "GROUP_ID1": 100,
                "GROUP_PROB1": 100,
            }
        )
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 50,
                "ENEMY_ID2": 701,
                "CREATE_PROB2": 50,
            }
        )
        enemies = {
            700: enemy(700, 88, 4),
            701: enemy(701, 89, 5),
        }
        self.templates = {
            88: template(88, "Wolf"),
            89: template(89, "Tiger"),
        }
        self.domain = SinglePlayerHistoricalDomain(
            static=HistoricalStaticData(
                encounter_areas=(area,),
                encounter_groups={100: group},
                enemy_variants=enemies,
            )
        )
        self.domain.persistent.character = player_state()
        self.domain.move_player(floor_id=2000, x=10, y=11)
        self.runtime = SinglePlayerHistoricalRuntime(
            self.domain,
            HistoricalWorldTopology(
                maps={2000: HistoricalMapDefinition(2000, 30, 30)}
            ),
        )

    def birth_rolls(self):
        return (
            EnemyBirthRolls(
                level_roll=0,
                birth_offsets=(-2, -1, 0, 1),
                spawn_allocation_rolls=(0, 0, 1, 1, 2, 2, 3, 3, 0, 1),
            ),
            EnemyBirthRolls(
                level_roll=0,
                birth_offsets=(2, 1, 0, -1),
                spawn_allocation_rolls=(3, 3, 2, 2, 1, 1, 0, 0, 3, 2),
            ),
        )

    def test_group_request_preserves_group_before_enemy_slot_generation(self):
        request = self.domain.request_encounter_group(group_roll=0)
        self.assertEqual(request.group_id, 100)
        self.assertEqual(request.area_index, 21)
        self.assertEqual(request.max_enemy_count, 2)
        self.assertEqual(request.position, MapPosition(2000, 10, 11))

    def test_group_spawn_can_create_mixed_enemy_battle(self):
        request = self.domain.request_encounter_group(group_roll=0)
        spawned = self.runtime.spawn_group_enemies(
            request,
            templates=self.templates,
            entry_count_roll=2,
            selection_rolls=(0, 50),
            birth_rolls=self.birth_rolls(),
        )
        self.assertEqual(
            tuple(x.participant.source_variant_id for x in spawned),
            (700, 701),
        )
        self.assertEqual(
            tuple(x.participant.level for x in spawned),
            (4, 5),
        )

        battle = self.runtime.start_group_battle(
            request,
            spawned_enemies=spawned,
        )
        self.assertEqual(len(battle.enemies), 2)
        self.assertEqual(
            tuple(enemy.name for enemy in battle.enemies),
            ("Wolf", "Tiger"),
        )

    def test_first_round_player_command_is_engine_facing_not_wire_server_state(self):
        request = self.domain.request_encounter_group(group_roll=0)
        spawned = self.runtime.spawn_group_enemies(
            request,
            templates=self.templates,
            entry_count_roll=2,
            selection_rolls=(0, 50),
            birth_rolls=self.birth_rolls(),
        )
        battle = self.runtime.start_group_battle(
            request,
            spawned_enemies=spawned,
        )

        attack = self.runtime.prepare_player_action(
            battle,
            "H|0A",
            initiative_random_subtract=12,
        )
        self.assertEqual(attack.command.kind, ATTACK)
        self.assertEqual(attack.command.target_slot, 10)
        self.assertEqual(attack.initiative, 68)

        fallback = self.runtime.prepare_player_action(
            battle,
            "G",
            initiative_random_subtract=0,
            error_status=True,
        )
        self.assertEqual(fallback.command.kind, WAIT)

    def test_group_battle_runtime_resolves_one_ordinary_attack_round(self):
        request = self.domain.request_encounter_group(group_roll=0)
        spawned = self.runtime.spawn_group_enemies(
            request,
            templates=self.templates,
            entry_count_roll=2,
            selection_rolls=(0, 50),
            birth_rolls=self.birth_rolls(),
        )
        battle = self.runtime.start_group_battle(
            request,
            spawned_enemies=spawned,
        )
        enemy_ids = [enemy.participant_id for enemy in battle.enemies]
        commands = {
            "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
            **{
                enemy_id: BattleCommand(BATTLE_COM_WAIT)
                for enemy_id in enemy_ids
            },
        }
        profiles = {
            participant_id: BattleCombatProfile(
                fixed_dex=100,
                fixed_luck=0,
                earth=0,
                water=0,
                fire=0,
                wind=0,
            )
            for participant_id in ("player", *enemy_ids)
        }
        result = self.runtime.resolve_ordinary_battle_round(
            battle,
            commands=commands,
            initiative_random_subtracts={
                participant_id: 0
                for participant_id in ("player", *enemy_ids)
            },
            slots={
                "player": 0,
                enemy_ids[0]: 10,
                enemy_ids[1]: 11,
            },
            profiles=profiles,
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                )
            },
            defense_profile="newpower_70pct",
            tie_break_order=("player", *enemy_ids),
        )
        player_event = next(
            event for event in result.events
            if event.participant_id == "player"
        )
        self.assertEqual(player_event.resolved_target_slot, 10)
        self.assertIn(player_event.result, ("normal", "miss"))
        self.assertLessEqual(
            result.hp_by_slot[10],
            battle.enemies[0].hp,
        )

    def test_runtime_persistent_state_carries_hp_across_rounds_to_victory(self):
        request = self.domain.request_encounter_group(group_roll=0)
        spawned = self.runtime.spawn_group_enemies(
            request,
            templates=self.templates,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(self.birth_rolls()[0],),
        )
        battle = self.runtime.start_group_battle(
            request,
            spawned_enemies=spawned,
        )
        enemy = replace(
            battle.enemies[0],
            hp=150,
            max_hp=150,
            defense=70,
            quick=40,
        )
        battle = replace(battle, enemies=(enemy,))
        enemy_id = enemy.participant_id
        profiles = self.runtime.build_group_battle_combat_profiles(
            battle,
            spawned_enemies=spawned,
            player_weapon_critical=0,
        )
        self.assertEqual(profiles["player"].fixed_dex, 30)
        self.assertEqual(profiles["player"].fixed_luck, 7)
        self.assertEqual(profiles["player"].elements, (50, 50, 0, 0))
        self.assertEqual(
            profiles[enemy_id].fixed_dex,
            spawned[0].participant.quick,
        )
        self.assertNotEqual(
            profiles[enemy_id].fixed_dex,
            battle.enemies[0].quick,
        )
        state = self.runtime.start_persistent_battle_state(
            battle,
            slots={"player": 0, enemy_id: 10},
        )

        def advance(current):
            return self.runtime.resolve_persistent_battle_round(
                current,
                commands={
                    "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                    enemy_id: BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={"player": 0, enemy_id: 0},
                profiles=profiles,
                attack_rolls={
                    "player": OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    )
                },
                defense_profile="newpower_70pct",
            )

        first = advance(state)
        self.assertEqual(first.after.turn, 1)
        self.assertGreater(first.after.hp_by_participant_id[enemy_id], 0)
        self.assertLess(first.after.hp_by_participant_id[enemy_id], 150)

        second = advance(first.after)
        self.assertEqual(second.after.turn, 2)
        self.assertEqual(second.after.hp_by_participant_id[enemy_id], 0)
        self.assertEqual(second.after.phase, FINISHED)
        self.assertEqual(second.after.result, PLAYER_WIN)
        self.assertEqual(second.after.winning_side, 0)

    def test_terminal_persistent_battle_settlement_updates_only_direct_hp(self):
        self.domain.persistent.pets[PetSlot(2)] = allied_pet()
        request = self.domain.request_encounter_group(group_roll=0)
        spawned = self.runtime.spawn_group_enemies(
            request,
            templates=self.templates,
            entry_count_roll=1,
            selection_rolls=(0,),
            birth_rolls=(self.birth_rolls()[0],),
        )
        battle = self.runtime.start_group_battle(
            request,
            spawned_enemies=spawned,
            allied_pet_slots=(2,),
        )
        enemy_id = battle.enemies[0].participant_id
        state = self.runtime.start_persistent_battle_state(
            battle,
            slots={"player": 0, "pet:2": 1, enemy_id: 10},
        )

        with self.assertRaisesRegex(ValueError, "before termination"):
            self.runtime.finish_persistent_battle(state)

        terminal = replace(
            state,
            hp_by_participant_id=MappingProxyType(
                {
                    "player": 73,
                    "pet:2": 21,
                    enemy_id: 0,
                }
            ),
            phase=FINISHED,
            result=PLAYER_WIN,
            winning_side=0,
        )
        returned = self.runtime.finish_persistent_battle(terminal)

        self.assertEqual(returned.result, PLAYER_WIN)
        self.assertEqual(returned.world_position, battle.origin_position)
        self.assertEqual(self.domain.world.player_position, battle.origin_position)
        self.assertEqual(self.domain.persistent.character.fields["hp"], 73)
        self.assertEqual(self.domain.persistent.character.fields["exp"], 0)
        self.assertEqual(self.domain.persistent.pets[PetSlot(2)].state["hp"], 21)
        self.assertEqual(self.domain.persistent.pets[PetSlot(2)].state["exp"], 10)

    def test_old_single_variant_encounter_projection_remains_compatible(self):
        request = self.domain.request_encounter(
            group_roll=0,
            enemy_roll=0,
            level_roll=0,
        )
        self.assertEqual(request.group_id, 100)
        self.assertEqual(request.enemy_variant_id.value, 700)
        self.assertEqual(request.pet_template_id.value, 88)
        self.assertEqual(request.level, 4)


if __name__ == "__main__":
    unittest.main()
