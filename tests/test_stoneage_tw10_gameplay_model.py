import unittest

from tools.stoneage_tw10_gameplay_model import (
    CharacterState,
    ItemView,
    NPCWindowSession,
    PetSkillView,
    PetState,
    TemplateRef,
    WorldObject,
    a62_to_int,
    decode_record,
    load_gameplay_bridge,
    load_gameplay_schema,
    unescape_legacy_string,
    validate_bridge_against_schema,
)


class TaiwanGameplayModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_gameplay_schema()
        cls.bridge = load_gameplay_bridge()

    def test_base62_matches_old_digit_alphabet(self):
        self.assertEqual(a62_to_int("0"), 0)
        self.assertEqual(a62_to_int("9"), 9)
        self.assertEqual(a62_to_int("a"), 10)
        self.assertEqual(a62_to_int("z"), 35)
        self.assertEqual(a62_to_int("A"), 36)
        self.assertEqual(a62_to_int("Z"), 61)
        self.assertEqual(a62_to_int("10"), 62)
        self.assertEqual(a62_to_int("-10"), -62)
        self.assertEqual(a62_to_int("!"), 0)

    def test_escape_decoder_uses_legacy_alphabet(self):
        self.assertEqual(
            unescape_legacy_string(r"a\zb\cc\yd\ne"),
            "a|b,c\\d\ne",
        )
        self.assertEqual(unescape_legacy_string(r"foo\qbar"), "fooqbar")

    def test_record_width_is_schema_driven(self):
        with self.assertRaises(ValueError):
            decode_record("pet_skill_view_slot", [1, 2, 3, "name"], schema=self.schema)
        got = decode_record(
            "pet_skill_view_slot",
            [12, 1, 4, r"bite\zname", r"memo\ctext"],
            schema=self.schema,
        )
        self.assertEqual(got["skill_id"], 12)
        self.assertEqual(got["name"], "bite|name")
        self.assertEqual(got["comment"], "memo,text")

    def test_character_full_status_uses_26_field_schema(self):
        raw = ["1"] + list(range(101, 124)) + ["hero", "title"]
        self.assertEqual(len(raw), 26)
        state = CharacterState.from_full_status(raw, schema=self.schema)
        self.assertEqual(state.status["update_mask"], 1)
        self.assertEqual(state.status["hp"], 101)
        self.assertEqual(state.status["duel_point_like_state"], 123)
        self.assertEqual(state.status["name"], "hero")
        self.assertEqual(state.status["free_name_or_title"], "title")

    def test_pet_state_keeps_template_ref_separate(self):
        raw = ["1"] + list(range(201, 219)) + ["pet", "free"]
        self.assertEqual(len(raw), 21)
        ref = TemplateRef("enemybase.TEMPNO", 88)
        pet = PetState.from_full_status(2, raw, template_ref=ref, schema=self.schema)
        self.assertEqual(pet.pet_slot, 2)
        self.assertEqual(pet.status["graphic_id"], 201)
        self.assertEqual(pet.template_ref.template_id, 88)
        self.assertNotIn("template_id", pet.status.values)

    def test_item_full_and_incremental_models_share_view_fields(self):
        full = ItemView.from_full_slot(
            4,
            ["secret", "", 0, "effect", 24002, 0, 1, 0, 7],
            schema=self.schema,
        )
        inc = ItemView.from_incremental(
            [4, "secret", "", 0, "effect", 24002, 0, 1, 0, 7],
            schema=self.schema,
        )
        self.assertEqual(full.slot, 4)
        self.assertEqual(inc.slot, 4)
        for key in (
            "name",
            "secondary_or_secret_name",
            "color",
            "memo_or_effect_text",
            "graphic_id",
            "field_context",
            "target_class",
            "level",
            "send_or_use_flags",
        ):
            self.assertEqual(full.view[key], inc.view[key])

    def test_pet_skill_slot_identity_is_separate_from_template_id(self):
        ref = TemplateRef("petskill.ID", 41)
        view = PetSkillView.from_slot(
            1,
            3,
            [41, 1, 4, "skill", "memo"],
            template_ref=ref,
            schema=self.schema,
        )
        self.assertEqual((view.pet_slot, view.skill_slot), (1, 3))
        self.assertEqual(view.view["skill_id"], 41)
        self.assertEqual(view.template_ref.namespace, "petskill.ID")

    def test_world_object_variants(self):
        character = WorldObject.from_character(
            [1, "a", 10, 20, 3, 10001, 5, 2, "npc", "title", 1, 8],
            schema=self.schema,
        )
        item = WorldObject.from_ground_item(
            ["b", 11, 21, 24002, 7, "info"],
            schema=self.schema,
        )
        money = WorldObject.from_ground_money(
            ["c", 12, 22, 500],
            schema=self.schema,
        )
        self.assertEqual(character.variant, "character")
        self.assertEqual(character.view["runtime_object_id"], 10)
        self.assertEqual(item.variant, "ground_item")
        self.assertEqual(item.view["runtime_object_id"], 11)
        self.assertEqual(money.variant, "ground_money")
        self.assertEqual(money.view["money_amount"], 500)

    def test_window_session_is_five_decoded_values(self):
        session = NPCWindowSession.from_transport(
            [1, 3, 99, 1234, "payload"],
            schema=self.schema,
        )
        self.assertEqual(session.view["sequence_number"], 99)
        self.assertEqual(session.view["source_object_index"], 1234)
        self.assertEqual(session.view["data"], "payload")

    def test_bridge_validates_against_baseline_schema(self):
        validate_bridge_against_schema(schema=self.schema, bridge=self.bridge)

    def test_bridge_validator_rejects_unknown_client_field(self):
        bad = load_gameplay_bridge()
        bad["bridges"]["pet_template_to_pet_state"]["mappings"][0]["target_field"] = "later_only"
        with self.assertRaises(ValueError):
            validate_bridge_against_schema(schema=self.schema, bridge=bad)


if __name__ == "__main__":
    unittest.main()
