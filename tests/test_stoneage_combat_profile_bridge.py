import unittest
from types import MappingProxyType

from tools.stoneage_combat_profile_bridge import (
    birth_combat_profile,
    fixed_attribute_projection,
    group_battle_combat_profiles,
    player_combat_profile,
    reconstructed_pet_combat_profile,
    spawned_enemy_combat_profile,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    GroupEncounterRequest,
    MapPosition,
    PlayerState,
)
from tools.stoneage_tw10_25_bridge_model import (
    PetBirthBridgeState,
    PetTemplateBridge,
    ReconstructedPetBridgeState,
)
from tools.stoneage_tw10_gameplay_model import TemplateRef
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge


def player_state(**overrides):
    fields = {
        "hp": 100,
        "max_hp": 100,
        "mp": 50,
        "max_mp": 50,
        "vital": 40,
        "strength": 40,
        "toughness": 35,
        "dexterity": 42,
        "exp": 0,
        "max_exp": 1000,
        "level": 5,
        "attack": 100,
        "defense": 80,
        "quick": 99,
        "charm": 10,
        "luck": 7,
        "earth": 50,
        "water": 50,
        "fire": 0,
        "wind": 0,
        "gold": 0,
        "name": "Hero",
    }
    fields.update(overrides)
    return PlayerState(MappingProxyType(fields))


def birth(
    *,
    internal_dexterity=4200,
    earth=50,
    water=50,
    fire=0,
    wind=0,
):
    return PetBirthBridgeState(
        template_ref=TemplateRef("enemybase.TEMPNO", 88),
        level=5,
        pet_rank=80,
        individualized_growth_base=(20, 20, 20, 20),
        alloc_point=0,
        spawn_allocation_counts=(0, 0, 0, 0),
        internal_vital=4000,
        internal_strength=4000,
        internal_toughness=3500,
        internal_dexterity=internal_dexterity,
        graphic_id=10088,
        ai=4,
        earth=earth,
        water=water,
        fire=fire,
        wind=wind,
        max_skill_slots=4,
        skill_ids=(),
    )


def participant(
    pid,
    side,
    kind,
    *,
    quick=42,
    source_variant_id=None,
    source_template_id=None,
    source_pet_slot=None,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=5,
        hp=100,
        max_hp=100,
        attack=100,
        defense=80,
        quick=quick,
        name=pid,
        fixed_vital=40,
        source_variant_id=source_variant_id,
        source_template_id=source_template_id,
        source_pet_slot=source_pet_slot,
    )


def enemy_variant():
    return EnemyVariantBridge.from_enemy(
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


def pet_template():
    return PetTemplateBridge.from_enemybase(
        {
            "NAME": "Wolf",
            "TEMPNO": 88,
            "INITNUM": 100,
            "LVUPPOINT": 5,
            "BASEVITAL": 20,
            "BASESTR": 20,
            "BASETGH": 20,
            "BASEDEX": 20,
            "IMGNUMBER": 10088,
            "MODAI": 4,
            "EARTHAT": 50,
            "WATERAT": 50,
            "FIREAT": 0,
            "WINDAT": 0,
            "SLOT": 4,
            "SIZE": 0,
        }
    )


class CombatProfileBridgeTests(unittest.TestCase):
    def test_player_profile_uses_dexterity_not_quick(self):
        profile = player_combat_profile(
            player_state(dexterity=42, quick=99, luck=7),
            weapon_critical=6,
        )
        self.assertEqual(profile.fixed_dex, 42)
        self.assertEqual(profile.fixed_luck, 7)
        self.assertEqual(profile.elements, (50, 50, 0, 0))
        self.assertEqual(profile.weapon_critical, 6)

    def test_player_profile_requires_fixed_luck_and_elements(self):
        fields = dict(player_state().fields)
        del fields["luck"]
        with self.assertRaisesRegex(ValueError, "luck"):
            player_combat_profile(
                PlayerState(MappingProxyType(fields)),
                weapon_critical=0,
            )

        with self.assertRaisesRegex(ValueError, "nonnegative"):
            player_combat_profile(
                player_state(fire=-1),
                weapon_critical=0,
            )

    def test_fixed_attribute_projection_preserves_source_overwrite_order(self):
        self.assertEqual(
            fixed_attribute_projection(50, 50, 0, 0),
            (50, 50, 0, 0),
        )
        # Earth is visited first and writes opposite fire negative. The later
        # fire branch therefore no longer runs, exactly like the stable source.
        self.assertEqual(
            fixed_attribute_projection(50, 0, 25, 0),
            (50, 0, 0, 0),
        )
        self.assertEqual(
            fixed_attribute_projection(0, 0, 25, 0),
            (0, 0, 25, 0),
        )

    def test_birth_profile_uses_internal_dex_not_client_quick_guess(self):
        source = birth(internal_dexterity=4200, earth=50, fire=25)
        profile = birth_combat_profile(source)
        self.assertEqual(profile.fixed_dex, 42)
        self.assertEqual(profile.fixed_luck, 0)
        self.assertEqual(profile.elements, (50, 50, 0, 0))
        self.assertEqual(profile.weapon_critical, 0)

    def test_reconstructed_pet_profile_reads_preserved_birth_source(self):
        source_birth = birth(internal_dexterity=3700)
        reconstructed = ReconstructedPetBridgeState(
            variant_ref=TemplateRef("enemy.ID", 700),
            template_ref=TemplateRef("enemybase.TEMPNO", 88),
            pet_slot=0,
            runtime_object_id=None,
            birth=source_birth,
            v1_fields=MappingProxyType(
                {
                    "quick": 999,
                    "earth": 50,
                    "water": 50,
                    "fire": 0,
                    "wind": 0,
                }
            ),
            skill_ids=(),
        )
        profile = reconstructed_pet_combat_profile(reconstructed)
        self.assertEqual(profile.fixed_dex, 37)
        self.assertNotEqual(profile.fixed_dex, reconstructed.v1_fields["quick"])

    def test_spawn_profile_detects_birth_participant_drift(self):
        source_birth = birth(internal_dexterity=4200)
        variant = enemy_variant()
        template = pet_template()
        good = SpawnedEnemy(
            spawn_index=0,
            variant=variant,
            template=template,
            birth=source_birth,
            participant=participant(
                "enemy:700:0",
                "enemy",
                "enemy",
                quick=42,
                source_variant_id=700,
                source_template_id=88,
            ),
        )
        self.assertEqual(spawned_enemy_combat_profile(good).fixed_dex, 42)

        bad = SpawnedEnemy(
            spawn_index=0,
            variant=variant,
            template=template,
            birth=source_birth,
            participant=participant(
                "enemy:700:0",
                "enemy",
                "enemy",
                quick=41,
                source_variant_id=700,
                source_template_id=88,
            ),
        )
        with self.assertRaisesRegex(ValueError, "QUICK"):
            spawned_enemy_combat_profile(bad)

    def test_group_profiles_cover_player_and_spawned_enemies(self):
        player = participant("player", "player", "player", quick=99)
        enemy = participant(
            "enemy:700:0",
            "enemy",
            "enemy",
            quick=42,
            source_variant_id=700,
            source_template_id=88,
        )
        encounter = GroupEncounterRequest(
            area_index=21,
            position=MapPosition(2000, 10, 11),
            group_id=100,
            max_enemy_count=1,
        )
        battle = BattleSession(
            origin_position=encounter.position,
            encounter=encounter,
            player=player,
            allied_pets=(),
            enemies=(enemy,),
        )
        spawn = SpawnedEnemy(
            spawn_index=0,
            variant=enemy_variant(),
            template=pet_template(),
            birth=birth(),
            participant=enemy,
        )
        profiles = group_battle_combat_profiles(
            battle,
            player_state=player_state(),
            player_weapon_critical=3,
            spawned_enemies=(spawn,),
        )
        self.assertEqual(set(profiles), {"player", "enemy:700:0"})
        self.assertEqual(profiles["player"].fixed_dex, 42)
        self.assertEqual(profiles["player"].weapon_critical, 3)
        self.assertEqual(profiles["enemy:700:0"].fixed_dex, 42)

    def test_allied_pet_requires_provenance_bearing_birth_source(self):
        player = participant("player", "player", "player", quick=99)
        pet = participant(
            "pet:0",
            "player",
            "pet",
            quick=99,
            source_variant_id=700,
            source_template_id=88,
            source_pet_slot=0,
        )
        encounter = GroupEncounterRequest(
            area_index=21,
            position=MapPosition(2000, 10, 11),
            group_id=100,
            max_enemy_count=1,
        )
        battle = BattleSession(
            origin_position=encounter.position,
            encounter=encounter,
            player=player,
            allied_pets=(pet,),
            enemies=(),
        )
        with self.assertRaisesRegex(ValueError, "missing provenance-bearing"):
            group_battle_combat_profiles(
                battle,
                player_state=player_state(),
                player_weapon_critical=0,
                spawned_enemies=(),
                allied_pet_sources=(),
            )


if __name__ == "__main__":
    unittest.main()
