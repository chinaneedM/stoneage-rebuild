import unittest
from types import MappingProxyType

from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    enemy_participant_from_birth,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRolls,
    HistoricalStaticData,
    MapPosition,
    PlayerState,
    RuntimeObjectId,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_runtime import SinglePlayerHistoricalRuntime
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LegacyWarpEdge,
    place_player_on_topology,
)
from tools.stoneage_tw10_25_bridge_model import (
    NpcCreateBridge,
    NpcTemplateBridge,
    PetTemplateBridge,
    build_npc_runtime_bridge,
    build_pet_birth_bridge,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def make_player():
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
                "name": "Hero",
            }
        )
    )


def make_enemy_variant():
    return EnemyVariantBridge.from_enemy(
        {
            "ID": 700,
            "TEMPNO": 88,
            "LV_MIN": 4,
            "LV_MAX": 4,
            "CREATEMAXNUM": 2,
            "CREATEMINNUM": 1,
            "TACTICS": 1,
            "EXP": 100,
            "DUELPOINT": 0,
            "STYLE": 0,
            "PETFLG": 1,
        }
    )


def make_enemy_template():
    return PetTemplateBridge.from_enemybase(
        {
            "NAME": "Stone Wolf",
            "TEMPNO": 88,
            "INITNUM": 100,
            "LVUPPOINT": 5,
            "BASEVITAL": 20,
            "BASESTR": 20,
            "BASETGH": 20,
            "BASEDEX": 20,
            "IMGNUMBER": 10123,
            "MODAI": 4,
            "EARTHAT": 50,
            "WATERAT": 50,
            "FIREAT": 0,
            "WINDAT": 0,
            "SLOT": 4,
        }
    )


def make_static():
    enemy = make_enemy_variant()
    group = GroupBridge.from_group(
        {
            "GROUP_ID": 100,
            "ENEMY_ID1": 700,
            "CREATE_PROB1": 100,
        }
    )
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
    return HistoricalStaticData(
        encounter_areas=(area,),
        encounter_groups={100: group},
        enemy_variants={700: enemy},
    )


def make_topology():
    return HistoricalWorldTopology(
        maps={
            1000: HistoricalMapDefinition(1000, 20, 20),
            2000: HistoricalMapDefinition(2000, 30, 30),
        },
        legacy_warps=(
            LegacyWarpEdge(
                source=MapPosition(1000, 5, 5),
                destination=MapPosition(2000, 10, 11),
            ),
        ),
    )


def make_npc_runtime():
    template = NpcTemplateBridge(
        "guide",
        "Windowman",
        character_name="Guide",
        image_number=31000,
    )
    create = NpcCreateBridge.from_create(
        floor_id=2000,
        template_names=["guide"],
        direction=2,
        create_index=10,
    )
    return build_npc_runtime_bridge(
        template,
        create,
        runtime_object_id=40000,
        spawn_x=12,
        spawn_y=11,
        object_type=2,
        default_level=1,
        default_name_color=0,
    )


class SinglePlayerHistoricalRuntimeTests(unittest.TestCase):
    def test_end_to_end_world_warp_encounter_battle_and_return_slice(self):
        domain = SinglePlayerHistoricalDomain(static=make_static())
        domain.persistent.character = make_player()
        domain.place_npc(make_npc_runtime())

        topology = make_topology()
        place_player_on_topology(domain, topology, MapPosition(1000, 4, 5))
        runtime = SinglePlayerHistoricalRuntime(domain, topology)

        warp_step = runtime.walk_step(
            destination=MapPosition(1000, 5, 5),
            entry_allowed=True,
            encounter_rolls=EncounterRolls(0, 0, 0),
        )
        self.assertEqual(warp_step.tick_index, 1)
        self.assertTrue(warp_step.walk.warp_triggered)
        self.assertTrue(warp_step.walk.encounter_suppressed)
        self.assertIsNone(warp_step.encounter)
        self.assertEqual(domain.world.player_position, MapPosition(2000, 10, 11))

        encounter_step = runtime.walk_step(
            destination=MapPosition(2000, 11, 11),
            entry_allowed=True,
            encounter_rolls=EncounterRolls(0, 0, 0),
        )
        self.assertEqual(encounter_step.tick_index, 2)
        self.assertFalse(encounter_step.walk.warp_triggered)
        self.assertIsNotNone(encounter_step.encounter)
        self.assertEqual(encounter_step.encounter.enemy_variant_id.value, 700)
        self.assertEqual(encounter_step.encounter.pet_template_id.value, 88)
        self.assertEqual(encounter_step.encounter.level, 4)

        variant = make_enemy_variant()
        template = make_enemy_template()
        birth = build_pet_birth_bridge(
            template,
            level=encounter_step.encounter.level,
            birth_offsets=(0, 0, 0, 0),
            spawn_allocation_rolls=(0, 0, 0, 1, 1, 2, 2, 2, 3, 3),
        )
        enemy = enemy_participant_from_birth(
            encounter_step.encounter,
            variant,
            template,
            birth,
            spawn_index=0,
        )
        battle = runtime.start_battle(
            encounter_step.encounter,
            enemies=(enemy,),
        )
        self.assertEqual(battle.origin_position, MapPosition(2000, 11, 11))
        self.assertEqual(battle.enemies[0].name, "Stone Wolf")

        returned = runtime.finish_battle(
            battle,
            BattleOutcome(
                result="victory",
                player_updates={"hp": 70, "exp": 100},
                pet_updates={},
            ),
        )
        self.assertEqual(returned.result, "victory")
        self.assertEqual(returned.world_position, MapPosition(2000, 11, 11))
        self.assertEqual(domain.world.player_position, MapPosition(2000, 11, 11))
        self.assertEqual(domain.persistent.character.fields["hp"], 70)
        self.assertEqual(domain.persistent.character.fields["exp"], 100)
        self.assertIn(RuntimeObjectId(40000), domain.world.npcs)

    def test_blocked_walk_never_generates_encounter_even_if_rolls_are_supplied(self):
        domain = SinglePlayerHistoricalDomain(static=make_static())
        domain.persistent.character = make_player()
        topology = make_topology()
        place_player_on_topology(domain, topology, MapPosition(2000, 10, 11))
        runtime = SinglePlayerHistoricalRuntime(domain, topology)

        step = runtime.walk_step(
            destination=MapPosition(2000, 11, 11),
            entry_allowed=False,
            encounter_rolls=EncounterRolls(0, 0, 0),
        )
        self.assertFalse(step.walk.moved)
        self.assertIsNone(step.encounter)
        self.assertEqual(domain.world.player_position, MapPosition(2000, 10, 11))


if __name__ == "__main__":
    unittest.main()
