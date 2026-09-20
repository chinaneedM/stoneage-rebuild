import unittest

from tools.stoneage_singleplayer_domain import (
    EnemyVariantId,
    HistoricalStaticData,
    InventorySlot,
    ItemTemplateId,
    NpcTemplateId,
    PetTemplateId,
    RuntimeObjectId,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_tw10_gameplay_model import CharacterState, DecodedRecord
from tools.stoneage_tw10_25_bridge_model import (
    ItemTemplateBridge,
    NpcCreateBridge,
    NpcTemplateBridge,
    PetSkillTemplateBridge,
    PetTemplateBridge,
    build_npc_runtime_bridge,
    build_reconstructed_pet_state,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def enemy_row(enemy_id=700, tempno=88):
    return {
        "ID": enemy_id,
        "TEMPNO": tempno,
        "LV_MIN": 3,
        "LV_MAX": 5,
        "CREATEMAXNUM": 2,
        "CREATEMINNUM": 1,
        "TACTICS": 1,
        "EXP": -1,
        "DUELPOINT": 0,
        "STYLE": 0,
        "PETFLG": 1,
    }


def pet_template_row():
    return {
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
        "PETSKILL1": 41,
    }


def build_npc():
    template = NpcTemplateBridge(
        "elder",
        "Windowman",
        character_name="Village Elder",
        image_number=30001,
        default_type=1,
    )
    create = NpcCreateBridge.from_create(
        floor_id=1000,
        template_names=["elder"],
        create_num=1,
        direction=6,
        create_index=77,
    )
    return build_npc_runtime_bridge(
        template,
        create,
        runtime_object_id=34567,
        spawn_x=12,
        spawn_y=34,
        object_type=2,
        default_level=1,
        default_name_color=0,
    )


def build_pet():
    variant = EnemyVariantBridge.from_enemy(enemy_row())
    template = PetTemplateBridge.from_enemybase(pet_template_row())
    return build_reconstructed_pet_state(
        variant,
        template,
        pet_slot=2,
        level_roll=0,
        birth_offsets=(-2, -1, 1, 2),
        spawn_allocation_rolls=(0, 0, 0, 1, 1, 2, 2, 2, 3, 3),
        mp=80,
        max_mp=100,
        exp=12,
        max_exp=200,
        rename_flag=1,
        free_name="Buddy",
        runtime_object_id=9001,
    )


def skill_41():
    return PetSkillTemplateBridge.from_petskill(
        {
            "ID": 41,
            "FIELD": 1,
            "TARGET": 4,
            "NAME": "Skill",
            "COMMENT": "Memo",
            "COST": 7,
            "ILLEGAL": 0,
            "FUNCNAME": "PETSKILL_Foo",
            "OPTION": "x",
        }
    )


def item_500():
    template = ItemTemplateBridge.from_itemset(
        {
            "id": 500,
            "name": "ordinary",
            "secretname": "visible",
            "effectstring": "effect",
            "imagenumber": 24002,
            "type": 20,
            "fieldtype": 0,
            "target": 1,
            "level": 0,
            "canpetmail": 1,
            "canmergefrom": 1,
        }
    )
    return template.instantiate(
        secondary_display_text="runtime",
        instance_cdkey="bound-owner",
        merge_flag=True,
    )


class SinglePlayerHistoricalDomainTests(unittest.TestCase):
    def test_in_process_boundary_exposes_player_world_inventory_pet_skill_and_session(self):
        domain = SinglePlayerHistoricalDomain()

        player = domain.set_player_from_v1(
            CharacterState(
                DecodedRecord(
                    "status_player_full",
                    {"level": 7, "name": "Hero", "gold": 123},
                )
            )
        )
        self.assertEqual(player.fields["level"], 7)

        item = domain.put_item(3, item_500())
        self.assertEqual(item.slot, InventorySlot(3))
        self.assertEqual(item.template_id, ItemTemplateId(500))
        self.assertEqual(item.view["name"], "visible")

        pet = domain.put_pet(build_pet(), {41: skill_41()})
        self.assertEqual(pet.variant_id, EnemyVariantId(700))
        self.assertEqual(pet.template_id, PetTemplateId(88))
        self.assertEqual(pet.runtime_object_id, RuntimeObjectId(9001))
        self.assertEqual(pet.skills[0].template_id, 41)
        self.assertEqual(pet.skills[0].view["name"], "Skill")

        npc_runtime = build_npc()
        npc = domain.place_npc(npc_runtime)
        self.assertEqual(npc.runtime_object_id, RuntimeObjectId(34567))
        self.assertEqual(npc.template_id, NpcTemplateId("elder"))
        self.assertEqual(npc.position.floor_id, 1000)

        session = domain.open_npc_session(
            npc_runtime,
            window_type=1,
            button_mask_or_type=3,
            sequence_number=105,
            data="payload",
        )
        self.assertEqual(session.source_runtime_object_id, RuntimeObjectId(34567))
        self.assertEqual(session.sequence_number, 105)
        self.assertIn(105, domain.interactions.npc_sessions)

        self.assertNotEqual(item.slot, item.template_id)
        self.assertNotEqual(pet.variant_id, pet.template_id)

    def test_npc_session_requires_world_presence(self):
        domain = SinglePlayerHistoricalDomain()
        with self.assertRaises(KeyError):
            domain.open_npc_session(
                build_npc(),
                window_type=1,
                button_mask_or_type=3,
                sequence_number=1,
                data="payload",
            )

    def test_encounter_request_is_deterministic_and_uses_inventory_template_gate(self):
        enemy = EnemyVariantBridge.from_enemy(enemy_row())
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "APPEAR_ITEM": 500,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21,
                "FLOOR": 1000,
                "X1": 0,
                "Y1": 0,
                "X2": 20,
                "Y2": 20,
                "PROB_MIN": 10,
                "PROB_MAX": 20,
                "ENEMY_MAX": 3,
                "ZORDER": 1,
                "GROUP_ID1": 100,
                "GROUP_PROB1": 100,
            }
        )
        static = HistoricalStaticData(
            encounter_areas=(area,),
            encounter_groups={100: group},
            enemy_variants={700: enemy},
        )
        domain = SinglePlayerHistoricalDomain(static=static)
        domain.move_player(floor_id=1000, x=10, y=10)

        with self.assertRaises(ValueError):
            domain.request_encounter(group_roll=0, enemy_roll=0, level_roll=0)

        domain.put_item(0, item_500())
        request = domain.request_encounter(
            group_roll=0,
            enemy_roll=0,
            level_roll=1,
        )
        self.assertIsNotNone(request)
        self.assertEqual(request.area_index, 21)
        self.assertEqual(request.group_id, 100)
        self.assertEqual(request.enemy_variant_id, EnemyVariantId(700))
        self.assertEqual(request.pet_template_id, PetTemplateId(88))
        self.assertEqual(request.level, 4)
        self.assertEqual(request.max_enemy_count, 2)

    def test_encounter_request_outside_area_returns_none(self):
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21,
                "FLOOR": 1000,
                "X1": 0,
                "Y1": 0,
                "X2": 20,
                "Y2": 20,
                "PROB_MIN": 10,
                "PROB_MAX": 20,
                "ENEMY_MAX": 3,
                "ZORDER": 1,
            }
        )
        domain = SinglePlayerHistoricalDomain(
            static=HistoricalStaticData(encounter_areas=(area,))
        )
        domain.move_player(floor_id=2000, x=10, y=10)
        self.assertIsNone(
            domain.request_encounter(group_roll=0, enemy_roll=0, level_roll=0)
        )

    def test_static_data_rejects_identity_key_aliasing(self):
        enemy = EnemyVariantBridge.from_enemy(enemy_row())
        with self.assertRaises(ValueError):
            HistoricalStaticData(enemy_variants={88: enemy})


if __name__ == "__main__":
    unittest.main()
