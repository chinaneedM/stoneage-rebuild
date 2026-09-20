import unittest

from tools.stoneage_tw10_25_bridge_model import (
    ItemTemplateBridge,
    NpcCreateBridge,
    NpcRuntimeLink,
    NpcTemplateBridge,
    PetSkillTemplateBridge,
    PetTemplateBridge,
    build_npc_runtime_bridge,
    build_pet_birth_bridge,
    c_atoi,
)


class Taiwan25BridgeModelTests(unittest.TestCase):
    def test_pet_template_exposes_only_direct_copy_fields(self):
        pet = PetTemplateBridge.from_enemybase(
            {
                "TEMPNO": 88,
                "IMGNUMBER": 10123,
                "MODAI": 4,
                "EARTHAT": 50,
                "WATERAT": 50,
                "FIREAT": 0,
                "WINDAT": 0,
                "SLOT": 4,
                "PETSKILL1": 1,
                "PETSKILL2": 2,
                "PETSKILL3": 41,
                "PETSKILL4": 0,
                "PETSKILL5": 0,
                "PETSKILL6": 0,
                "PETSKILL7": 0,
                "BASEVITAL": 20,
                "BASESTR": 18,
                "BASETGH": 19,
                "BASEDEX": 17,
                "LVUPPOINT": 5.0,
            }
        )
        self.assertEqual(
            pet.directly_bridgeable_pet_state(),
            {
                "graphic_id": 10123,
                "ai": 4,
                "earth": 50,
                "water": 50,
                "fire": 0,
                "wind": 0,
                "max_skill_slots": 4,
            },
        )
        self.assertEqual(pet.skill_ids, (1, 2, 41))
        self.assertEqual(pet.template_ref.namespace, "enemybase.TEMPNO")
        self.assertNotIn("hp", pet.directly_bridgeable_pet_state())
        self.assertEqual(pet.growth_inputs()["BASEVITAL"], 20)

    def test_c_atoi_matches_descendant_enemybase_loader(self):
        self.assertEqual(c_atoi("5.00"), 5)
        self.assertEqual(c_atoi("10.75"), 10)
        self.assertEqual(c_atoi("-2.9"), -2)
        self.assertEqual(c_atoi("abc"), 0)

    def test_pet_birth_formula_bridge_is_deterministic_from_explicit_random_inputs(self):
        pet = PetTemplateBridge.from_enemybase(
            {
                "TEMPNO": 88,
                "INITNUM": 100,
                "LVUPPOINT": "5.00",
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
                "PETSKILL1": 1,
                "PETSKILL2": 2,
                "PETSKILL3": 41,
            }
        )
        born = build_pet_birth_bridge(
            pet,
            level=3,
            birth_offsets=(-2, -1, 1, 2),
            spawn_allocation_rolls=(0, 0, 0, 1, 1, 2, 2, 2, 3, 3),
        )
        self.assertEqual(pet.level_up_point, 5)
        self.assertEqual(born.pet_rank, 4)
        self.assertEqual(born.individualized_growth_base, (18, 19, 21, 22))
        self.assertEqual(born.spawn_allocation_counts, (3, 2, 3, 2))
        self.assertEqual(
            (
                born.internal_vital,
                born.internal_strength,
                born.internal_toughness,
                born.internal_dexterity,
            ),
            (2310, 2310, 2640, 2640),
        )
        projected = born.combat_projection()
        self.assertEqual(projected["max_hp"], 168)
        self.assertEqual(projected["attack"], 29)
        self.assertEqual(projected["defense"], 32)
        self.assertEqual(projected["quick"], 26)
        self.assertEqual(projected["graphic_id"], 10123)
        self.assertNotIn("max_mp", projected)

    def test_pet_skill_client_view_excludes_server_behavior_fields(self):
        skill = PetSkillTemplateBridge.from_petskill(
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
        self.assertEqual(
            skill.client_view_fields(),
            {
                "skill_id": 41,
                "field_context": 1,
                "target_class": 4,
                "name": "Skill",
                "comment": "Memo",
            },
        )
        self.assertNotIn("cost", skill.client_view_fields())
        self.assertNotIn("function_name", skill.client_view_fields())

    def test_item_template_builds_exact_nine_field_v1_view_through_instance(self):
        item = ItemTemplateBridge.from_itemset(
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
        instance = item.instantiate(
            secondary_display_text="runtime",
            instance_cdkey="bound-owner",
            merge_flag=True,
        )
        view = instance.client_view_fields()
        self.assertEqual(
            list(view),
            [
                "name",
                "secondary_display_text",
                "color",
                "memo_or_effect_text",
                "graphic_id",
                "field_context",
                "target_class",
                "level",
                "send_or_use_flags",
            ],
        )
        self.assertEqual(view["name"], "visible")
        self.assertEqual(view["secondary_display_text"], "runtime")
        self.assertEqual(view["color"], 5)
        self.assertEqual(view["send_or_use_flags"], 7)
        self.assertEqual(item.ordinary_name, "ordinary")
        self.assertEqual(item.template_ref.template_id, 500)
        self.assertEqual(instance.template_ref.template_id, 500)
        self.assertNotIn("template_id", view)

    def test_item_instance_color_precedence_matches_fixed_descendant_sender(self):
        item = ItemTemplateBridge.from_itemset(
            {
                "id": 501,
                "secretname": "visible",
                "effectstring": "effect",
                "imagenumber": 24003,
                "type": 0,
                "fieldtype": 0,
                "target": 1,
                "level": 0,
                "canpetmail": 0,
                "canmergefrom": 0,
            }
        )
        self.assertEqual(item.instantiate().color, 0)
        self.assertEqual(item.instantiate(merge_flag=True).color, 4)
        self.assertEqual(
            item.instantiate(instance_cdkey="owner", merge_flag=True).color,
            5,
        )
        self.assertEqual(item.instantiate().send_or_use_flags, 0)

    def test_npc_template_create_to_world_and_window_runtime_boundary(self):
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
            image_override=30002,
            name_override="Elder",
            create_index=77,
        )
        runtime = build_npc_runtime_bridge(
            template,
            create,
            runtime_object_id=34567,
            spawn_x=12,
            spawn_y=34,
            object_type=2,
            default_level=1,
            default_name_color=0,
            default_self_title="",
            default_walkable=0,
            default_height=0,
        )
        world = runtime.v1_world_character_fields()
        self.assertEqual(
            list(world),
            [
                "object_type",
                "runtime_object_id",
                "x",
                "y",
                "direction",
                "base_graphic_id",
                "level",
                "name_color",
                "name",
                "self_or_free_title",
                "walkable",
                "height",
            ],
        )
        self.assertEqual(world["runtime_object_id"], 34567)
        self.assertEqual(world["direction"], 6)
        self.assertEqual(world["base_graphic_id"], 30002)
        self.assertEqual(world["name"], "Elder")
        self.assertEqual(runtime.template_ref.template_id, "elder")
        self.assertEqual(runtime.create_index, 77)

        wn = runtime.window_session_fields(
            window_type=1,
            button_mask_or_type=3,
            sequence_number=105,
            data="payload",
        )
        self.assertEqual(wn["source_object_index"], 34567)
        self.assertEqual(wn["sequence_number"], 105)
        self.assertNotEqual(wn["source_object_index"], wn["sequence_number"])

    def test_npc_generation_uses_template_values_when_create_has_no_override(self):
        template = NpcTemplateBridge(
            "guide",
            character_name="Guide",
            image_number=31000,
        )
        create = NpcCreateBridge.from_create(
            floor_id=2000,
            template_names=["guide"],
            direction=2,
            image_override=-1,
        )
        runtime = build_npc_runtime_bridge(
            template,
            create,
            runtime_object_id=10,
            spawn_x=1,
            spawn_y=2,
            object_type=2,
            default_level=1,
            default_name_color=0,
        )
        self.assertEqual(runtime.base_graphic_id, 31000)
        self.assertEqual(runtime.name, "Guide")

    def test_npc_runtime_identity_remains_distinct(self):
        template = NpcTemplateBridge("elder", "Windowman")
        create = NpcCreateBridge.from_create(
            floor_id=1000,
            template_names=["elder"],
            create_num=1,
        )
        link = NpcRuntimeLink.link(34567, template, floor_id=create.floor_id)
        self.assertEqual(link.runtime_object_id, 34567)
        self.assertEqual(link.template_ref.template_id, "elder")
        self.assertEqual(link.floor_id, 1000)
        self.assertNotEqual(link.runtime_object_id, link.template_ref.template_id)

    def test_pet_slot_limit_rejects_later_wider_template(self):
        row = {
            "TEMPNO": 1,
            "IMGNUMBER": 100,
            "MODAI": 1,
            "EARTHAT": 25,
            "WATERAT": 25,
            "FIREAT": 25,
            "WINDAT": 25,
            "SLOT": 8,
        }
        with self.assertRaises(ValueError):
            PetTemplateBridge.from_enemybase(row)


if __name__ == "__main__":
    unittest.main()
