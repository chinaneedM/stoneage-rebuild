import unittest

from tools.stoneage_tw10_25_bridge_model import (
    ItemTemplateBridge,
    NpcCreateBridge,
    NpcRuntimeLink,
    NpcTemplateBridge,
    PetSkillTemplateBridge,
    PetTemplateBridge,
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

    def test_item_template_builds_exact_nine_field_v1_view(self):
        item = ItemTemplateBridge.from_itemset(
            {
                "id": 500,
                "name": "ordinary",
                "secretname": "visible",
                "effectstring": "effect",
                "imagenumber": 24002,
                "fieldtype": 0,
                "target": 1,
                "level": 0,
            }
        )
        view = item.client_view_fields(
            secondary_runtime_text="runtime",
            color=3,
            send_or_use_flags=7,
        )
        self.assertEqual(
            list(view),
            [
                "name",
                "secondary_or_secret_name",
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
        self.assertEqual(view["secondary_or_secret_name"], "runtime")
        self.assertEqual(item.ordinary_name, "ordinary")
        self.assertEqual(item.template_ref.template_id, 500)
        self.assertNotIn("template_id", view)

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
