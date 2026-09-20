import unittest
from types import MappingProxyType

from tools.stoneage_singleplayer_domain import (
    EnemyVariantId,
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
    NpcSession,
    PetActor,
    PetGrowthState,
    PetSkill,
    PetSlot,
    PetTemplateId,
    PersistentPlayerState,
    PlayerState,
    RuntimeObjectId,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_persistence import (
    PERSISTENCE_SCHEMA,
    decode_persistent_state,
    dump_persistent_state,
    encode_persistent_state,
    load_persistent_state,
    restore_domain_persistent_state,
)


def make_state():
    state = PersistentPlayerState(
        character=PlayerState(
            MappingProxyType(
                {
                    "hp": 100,
                    "max_hp": 100,
                    "exp": 50,
                    "level": 5,
                    "name": "Hero",
                }
            )
        )
    )
    item = InventoryItem(
        slot=InventorySlot(3),
        template_id=ItemTemplateId(500),
        view=MappingProxyType(
            {
                "name": "visible",
                "secondary_display_text": "runtime",
                "color": 5,
            }
        ),
    )
    state.inventory[item.slot] = item

    pet = PetActor(
        slot=PetSlot(2),
        variant_id=EnemyVariantId(700),
        template_id=PetTemplateId(88),
        runtime_object_id=RuntimeObjectId(9001),
        state=MappingProxyType(
            {
                "hp": 60,
                "max_hp": 60,
                "exp": 10,
                "level": 4,
                "name": "Stone Wolf",
            }
        ),
        skills=(
            PetSkill(
                template_id=41,
                view=MappingProxyType({"skill_id": 41, "name": "Skill"}),
            ),
        ),
        growth=PetGrowthState(
            pet_rank=4,
            alloc_point=0x12131516,
            internal_vital=1800,
            internal_strength=1900,
            internal_toughness=2100,
            internal_dexterity=2200,
            variable_ai=500,
        ),
    )
    state.pets[pet.slot] = pet
    return state


class SinglePlayerPersistenceTests(unittest.TestCase):
    def test_roundtrip_persists_only_player_owned_state(self):
        state = make_state()
        payload = dump_persistent_state(state)
        self.assertEqual(set(payload), {"schema", "character", "inventory", "pets"})
        self.assertEqual(payload["schema"], PERSISTENCE_SCHEMA)
        self.assertNotIn("runtime_object_id", payload["pets"][0])

        restored = load_persistent_state(payload)
        self.assertEqual(restored.character.fields["name"], "Hero")
        self.assertEqual(
            restored.inventory[InventorySlot(3)].template_id,
            ItemTemplateId(500),
        )
        restored_pet = restored.pets[PetSlot(2)]
        self.assertEqual(restored_pet.variant_id, EnemyVariantId(700))
        self.assertEqual(restored_pet.template_id, PetTemplateId(88))
        self.assertIsNone(restored_pet.runtime_object_id)
        self.assertEqual(restored_pet.skills[0].template_id, 41)
        self.assertIsNotNone(restored_pet.growth)
        self.assertEqual(restored_pet.growth.pet_rank, 4)
        self.assertEqual(restored_pet.growth.alloc_point, 0x12131516)
        self.assertEqual(restored_pet.growth.internal_dexterity, 2200)
        self.assertEqual(restored_pet.growth.variable_ai, 500)

    def test_json_encoding_is_deterministic_and_roundtrips(self):
        state = make_state()
        encoded_a = encode_persistent_state(state)
        encoded_b = encode_persistent_state(state)
        self.assertEqual(encoded_a, encoded_b)

        restored = decode_persistent_state(encoded_a)
        self.assertEqual(restored.character.fields["hp"], 100)
        self.assertEqual(restored.pets[PetSlot(2)].state["name"], "Stone Wolf")

    def test_restore_replaces_only_persistent_partition(self):
        domain = SinglePlayerHistoricalDomain()
        domain.world.player_position = None
        domain.interactions.npc_sessions[7] = NpcSession(
            sequence_number=7,
            source_runtime_object_id=RuntimeObjectId(123),
            window_type=1,
            button_mask_or_type=1,
            data="session",
        )

        payload = dump_persistent_state(make_state())
        restore_domain_persistent_state(domain, payload)

        self.assertEqual(domain.persistent.character.fields["name"], "Hero")
        self.assertIsNone(domain.world.player_position)
        self.assertIn(7, domain.interactions.npc_sessions)

    def test_schema_and_shape_are_strict(self):
        payload = dump_persistent_state(make_state())

        wrong_schema = dict(payload)
        wrong_schema["schema"] = "stoneage.singleplayer.persistence.r999"
        with self.assertRaises(ValueError):
            load_persistent_state(wrong_schema)

        extra = dict(payload)
        extra["world"] = {}
        with self.assertRaises(ValueError):
            load_persistent_state(extra)

        missing = dict(payload)
        del missing["pets"]
        with self.assertRaises(ValueError):
            load_persistent_state(missing)

    def test_r1_payload_migrates_without_inventing_hidden_pet_growth(self):
        payload = dump_persistent_state(make_state())
        payload["schema"] = "stoneage.singleplayer.persistence.r1"
        for pet in payload["pets"]:
            del pet["growth"]

        restored = load_persistent_state(payload)
        self.assertIsNone(restored.pets[PetSlot(2)].growth)
    def test_r2_payload_migrates_variable_ai_to_zero(self):
        payload = dump_persistent_state(make_state())
        payload["schema"] = "stoneage.singleplayer.persistence.r2"
        for pet in payload["pets"]:
            if pet["growth"] is not None:
                del pet["growth"]["variable_ai"]

        restored = load_persistent_state(payload)
        self.assertIsNotNone(restored.pets[PetSlot(2)].growth)
        self.assertEqual(restored.pets[PetSlot(2)].growth.variable_ai, 0)

    def test_duplicate_slots_are_rejected(self):
        payload = dump_persistent_state(make_state())
        payload["inventory"] = payload["inventory"] * 2
        with self.assertRaises(ValueError):
            load_persistent_state(payload)

        payload = dump_persistent_state(make_state())
        payload["pets"] = payload["pets"] * 2
        with self.assertRaises(ValueError):
            load_persistent_state(payload)

    def test_runtime_identity_is_never_restored_as_persistent_identity(self):
        payload = dump_persistent_state(make_state())
        self.assertNotIn("runtime_object_id", payload["pets"][0])
        restored = load_persistent_state(payload)
        self.assertIsNone(restored.pets[PetSlot(2)].runtime_object_id)


if __name__ == "__main__":
    unittest.main()
