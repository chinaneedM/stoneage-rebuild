import unittest
from types import MappingProxyType

from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    begin_battle,
    enemy_participant_from_birth,
    apply_battle_outcome,
    preview_physical_damage,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetActor,
    PetGrowthState,
    PetSlot,
    PetTemplateId,
    PlayerState,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_tw10_25_bridge_model import (
    PetTemplateBridge,
    build_pet_birth_bridge,
)
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge


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
                "exp": 0,
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


def enemy_variant():
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


def enemy_template():
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


def encounter(position=MapPosition(2000, 10, 11)):
    return EncounterRequest(
        area_index=21,
        position=position,
        group_id=100,
        enemy_variant_id=EnemyVariantId(700),
        pet_template_id=PetTemplateId(88),
        level=4,
        max_enemy_count=2,
    )


def enemy_spawn(request=None, spawn_index=0):
    request = request or encounter()
    variant = enemy_variant()
    template = enemy_template()
    birth = build_pet_birth_bridge(
        template,
        level=4,
        birth_offsets=(0, 0, 0, 0),
        spawn_allocation_rolls=(0, 0, 0, 1, 1, 2, 2, 2, 3, 3),
    )
    return enemy_participant_from_birth(
        request,
        variant,
        template,
        birth,
        spawn_index=spawn_index,
    )


def domain_for_battle():
    domain = SinglePlayerHistoricalDomain()
    domain.persistent.character = player_state()
    domain.persistent.pets[PetSlot(2)] = allied_pet()
    domain.move_player(floor_id=2000, x=10, y=11)
    return domain


class SinglePlayerBattleLifecycleTests(unittest.TestCase):
    def test_encounter_identity_and_birth_state_form_enemy_participant(self):
        request = encounter()
        enemy = enemy_spawn(request)
        self.assertEqual(enemy.participant_id, "enemy:700:0")
        self.assertEqual(enemy.source_variant_id, 700)
        self.assertEqual(enemy.source_template_id, 88)
        self.assertEqual(enemy.level, 4)
        self.assertEqual(enemy.name, "Stone Wolf")
        self.assertGreater(enemy.hp, 0)
        self.assertGreater(enemy.attack, 0)

    def test_battle_session_requires_explicit_enemy_spawns_and_allied_pet_selection(self):
        domain = domain_for_battle()
        request = encounter()
        session = begin_battle(
            domain,
            request,
            enemies=(enemy_spawn(request),),
            allied_pet_slots=(2,),
        )
        self.assertEqual(session.origin_position, MapPosition(2000, 10, 11))
        self.assertEqual(session.player.name, "Hero")
        self.assertEqual(session.allied_pets[0].source_pet_slot, 2)
        self.assertEqual(session.enemies[0].source_variant_id, 700)

        with self.assertRaises(ValueError):
            begin_battle(domain, request, enemies=())

    def test_enemy_count_and_identity_cannot_exceed_encounter_boundary(self):
        domain = domain_for_battle()
        request = encounter()
        enemies = (
            enemy_spawn(request, 0),
            enemy_spawn(request, 1),
        )
        session = begin_battle(domain, request, enemies=enemies)
        self.assertEqual(len(session.enemies), 2)

        too_many = enemies + (enemies[0],)
        with self.assertRaises(ValueError):
            begin_battle(domain, request, enemies=too_many)

        wrong = encounter()
        wrong_enemy = enemy_spawn(wrong)
        wrong_enemy = type(wrong_enemy)(
            **{
                **wrong_enemy.__dict__,
                "source_variant_id": 999,
            }
        )
        with self.assertRaises(ValueError):
            begin_battle(domain, request, enemies=(wrong_enemy,))

    def test_recovered_battle_core_is_exposed_with_explicit_randomness_and_profile(self):
        domain = domain_for_battle()
        request = encounter()
        session = begin_battle(
            domain,
            request,
            enemies=(enemy_spawn(request),),
        )
        self.assertEqual(session.player.initiative(0), 80)
        self.assertEqual(session.player.initiative(24), 56)

        damage = preview_physical_damage(
            session.player,
            session.enemies[0],
            random_value=0,
            defense_profile="newpower_70pct",
        )
        self.assertIsInstance(damage, int)

        with self.assertRaises(ValueError):
            preview_physical_damage(
                session.player,
                session.enemies[0],
                random_value=0,
                defense_profile="unknown",
            )

    def test_battle_outcome_returns_to_same_world_position_and_updates_existing_state(self):
        domain = domain_for_battle()
        request = encounter()
        session = begin_battle(
            domain,
            request,
            enemies=(enemy_spawn(request),),
            allied_pet_slots=(2,),
        )
        returned = apply_battle_outcome(
            domain,
            session,
            BattleOutcome(
                result="victory",
                player_updates={"hp": 70, "exp": 100},
                pet_updates={2: {"hp": 30, "exp": 50}},
            ),
        )
        self.assertEqual(returned.result, "victory")
        self.assertEqual(returned.world_position, MapPosition(2000, 10, 11))
        self.assertEqual(domain.world.player_position, MapPosition(2000, 10, 11))
        self.assertEqual(domain.persistent.character.fields["hp"], 70)
        self.assertEqual(domain.persistent.character.fields["exp"], 100)
        self.assertEqual(domain.persistent.pets[PetSlot(2)].state["hp"], 30)

        growth = PetGrowthState(
            pet_rank=4,
            alloc_point=0x14141414,
            internal_vital=2000,
            internal_strength=2000,
            internal_toughness=2000,
            internal_dexterity=2000,
            variable_ai=500,
        )
        apply_battle_outcome(
            domain,
            session,
            BattleOutcome(
                result="victory",
                player_updates={},
                pet_updates={},
                pet_growth_updates={2: growth},
            ),
        )
        self.assertEqual(
            domain.persistent.pets[PetSlot(2)].growth,
            growth,
        )

    def test_outcome_does_not_invent_new_fields_or_ignore_world_drift(self):
        domain = domain_for_battle()
        request = encounter()
        session = begin_battle(
            domain,
            request,
            enemies=(enemy_spawn(request),),
        )
        with self.assertRaises(ValueError):
            apply_battle_outcome(
                domain,
                session,
                BattleOutcome(
                    result="victory",
                    player_updates={"unknown_reward": 1},
                    pet_updates={},
                ),
            )

        pet_domain = domain_for_battle()
        pet_session = begin_battle(
            pet_domain,
            request,
            enemies=(enemy_spawn(request),),
            allied_pet_slots=(2,),
        )
        with self.assertRaises(ValueError):
            apply_battle_outcome(
                pet_domain,
                pet_session,
                BattleOutcome(
                    result="victory",
                    player_updates={"hp": 70},
                    pet_updates={2: {"unknown_reward": 1}},
                ),
            )
        self.assertEqual(pet_domain.persistent.character.fields["hp"], 100)
        self.assertEqual(pet_domain.persistent.pets[PetSlot(2)].state["hp"], 60)

        domain.move_player(floor_id=2000, x=11, y=11)
        with self.assertRaises(ValueError):
            apply_battle_outcome(
                domain,
                session,
                BattleOutcome(
                    result="victory",
                    player_updates={},
                    pet_updates={},
                ),
            )


if __name__ == "__main__":
    unittest.main()
