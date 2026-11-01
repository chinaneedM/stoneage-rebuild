"""Invented full-state capture/save/reentry fixtures; no original game executes."""
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
import tests.test_stoneage_local_runtime_session_coordinator as fixtures
from tools.stoneage_battle_core_model import BattleCaptureInputs
from tools.stoneage_battle_round_model import (
    BATTLE_COM_CAPTURE, BATTLE_COM_WAIT, BattleCommand, BattleCombatProfile,
    OrdinaryCaptureContext, OrdinaryCaptureRolls,
)
from tools.stoneage_enemy_spawn_model import EnemyBirthRolls
from tools.stoneage_local_filesystem_persistence import LocalFilesystemPersistenceStore
from tools.stoneage_local_runtime_core import LocalRuntimeSessionState, load_runtime_bootstrap_file
from tools.stoneage_local_runtime_session_coordinator import LocalRuntimeSessionCoordinator
from tools.stoneage_singleplayer_domain import (
    EnemyVariantId, MapPosition, PetActor, PetGrowthState, PetSkill,
    PetSlot, PetTemplateId, SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_runtime import SinglePlayerHistoricalRuntime
from tools.stoneage_pet_growth_model import PetLevelGrowthRolls
from tools.stoneage_player_growth_model import LEGACY_CUMULATIVE_EXP


class CaptureStateLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.profile = load_runtime_bootstrap_file(
            fixtures.ROOT / 'game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json')
        self.stack = fixtures._FakeStack(self.profile)
        self.coordinator = LocalRuntimeSessionCoordinator(
            self.stack, LocalFilesystemPersistenceStore(Path(self.tmp.name)))
        self.session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1, player_position=MapPosition(1, 0, 0),
            player_state=fixtures._battle_player_state(),
            world_flags=frozenset({'invented-capture-test'}))
        self.rolls = EnemyBirthRolls(1, (0, 0, 0, 0), (0, 1, 2, 3, 0, 1, 2, 3, 0, 1))
        request = self.stack.request_encounter_group(self.session, group_roll=0)
        context = self.coordinator.start_group_battle(
            self.session, request, entry_count_roll=1,
            selection_rolls=(0,), birth_rolls=(self.rolls,))
        self.enemy = replace(context.battle.enemies[0], hp=10, max_hp=100,
                             quick=20, name='Invented Wild Pet',
                             capturable=True, capture_default=99)
        context = replace(context, battle=replace(context.battle, enemies=(self.enemy,)))
        self.context = self.coordinator.begin_persistent_group_battle(
            context, slots={'player': 0, self.enemy.participant_id: 10})
        birth = context.spawned_enemies[0].birth
        # This ordinary fixture has no intervening raw-stat transformation.
        # Remaining MP/EXP/UI/skill values are explicit invented source inputs.
        self.pet = PetActor(
            PetSlot(0), EnemyVariantId(self.enemy.source_variant_id),
            PetTemplateId(self.enemy.source_template_id), None,
            MappingProxyType({
                'update_mask': 1, 'graphic_id': birth.graphic_id,
                'level': self.enemy.level, 'hp': 10, 'max_hp': 100,
                'mp': 17, 'max_mp': 31, 'exp': 0, 'max_exp': 500,
                'attack': self.enemy.attack, 'defense': self.enemy.defense,
                'quick': self.enemy.quick, 'ai': 42,
                'earth': 25, 'water': 25, 'fire': 25, 'wind': 25,
                'max_skill_slots': 2, 'rename_flag': 0,
                'name': self.enemy.name, 'free_name': 'Explicit free name',
                'poison': 2, 'capture_source': 'INVENTED_CURRENT_STATE',
            }),
            (PetSkill(701, MappingProxyType({'name': 'Invented skill', 'mp': 3})),),
            PetGrowthState(birth.pet_rank, birth.alloc_point,
                           birth.internal_vital, birth.internal_strength,
                           birth.internal_toughness, birth.internal_dexterity, 0))

    def capture(self, pet):
        enemy_id = self.enemy.participant_id
        profile = BattleCombatProfile(100, 7, 0, 0, 0, 0)
        return self.coordinator.resolve_persistent_capture_round(
            self.context,
            commands={'player': BattleCommand(BATTLE_COM_CAPTURE, command2=10),
                      enemy_id: BattleCommand(BATTLE_COM_WAIT)},
            initiative_random_subtracts={'player': 0, enemy_id: 0},
            profiles={'player': profile, enemy_id: profile}, attack_rolls={},
            capture_context=OrdinaryCaptureContext(attacker_charm=100, occupied_pet_slots=()),
            capture_rolls=OrdinaryCaptureRolls(1),
            captured_pets_by_target_id={enemy_id: pet}, defense_profile='newpower_70pct')

    def assert_atomic(self):
        self.assertEqual(self.session.player_state.pets, {})
        self.assertIsNone(self.context.working_persistent_state_payload)

    def test_full_capture_disk_reload_reentry_and_controlled_growth(self):
        captured, result = self.capture(self.pet)
        self.assertEqual(result.after.pending_exp_by_participant_id['player'], 0)
        self.assertEqual(result.round.exited_participant_ids, (self.enemy.participant_id,))
        settled = self.coordinator.settle_persistent_group_battle_without_level_crossing(captured)
        self.coordinator.save_game('capture', settled)
        # A fresh coordinator/store instance must read actual temporary disk bytes.
        coordinator = LocalRuntimeSessionCoordinator(
            fixtures._FakeStack(self.profile), LocalFilesystemPersistenceStore(Path(self.tmp.name)))
        restored = coordinator.continue_game('capture')
        pet = restored.player_state.pets[PetSlot(0)]
        self.assertEqual(dict(pet.state), dict(self.pet.state))
        self.assertEqual(pet.skills, self.pet.skills)
        self.assertEqual(pet.growth, self.pet.growth)
        self.assertIsNone(restored.player_state.default_pet_slot)
        self.assert_atomic()
        request = coordinator.stack.request_encounter_group(restored, group_roll=0)
        battle = coordinator.start_group_battle(
            restored, request, entry_count_roll=1, selection_rolls=(0,),
            birth_rolls=(self.rolls,), allied_pet_slots=(0,))
        self.assertEqual(battle.battle.allied_pets[0].hp, 10)
        battle = coordinator.begin_persistent_group_battle(
            battle, slots={'player': 0, 'pet:0': 1, battle.battle.enemies[0].participant_id: 10})
        state = battle.persistent_battle_state
        enemy_id = state.session.enemies[0].participant_id
        # Controlled terminal award isolates the already sourced growth seam.
        # This is not a claim about natural kill allocation or a historical EXP table.
        terminal = replace(state, phase='finished', result='victory', winning_side=0,
            hp_by_participant_id=MappingProxyType({'player': state.session.player.hp,
                                                  'pet:0': 10, enemy_id: 0}),
            pending_exp_by_participant_id=MappingProxyType({'player': 0, 'pet:0': 500}),
            pending_pet_variable_ai_by_participant_id=MappingProxyType({'pet:0': 0}))
        rank_roll = (450, 470, 490, 510, 530, 550)[pet.growth.pet_rank]
        grown = coordinator.settle_persistent_group_battle_with_progression(
            replace(battle, persistent_battle_state=terminal),
            player_exp_profile=LEGACY_CUMULATIVE_EXP, next_player_max_exp_by_level={},
            pet_exp_profile=LEGACY_CUMULATIVE_EXP,
            next_pet_max_exp_by_slot={0: {pet.state['level'] + 1: 900}},
            pet_level_growth_rolls_by_slot={0: (PetLevelGrowthRolls((0,1,2,3,0,1,2,3,0,1), rank_roll),)})
        coordinator.save_game('grown', grown)
        grown_pet = coordinator.continue_game('grown').player_state.pets[PetSlot(0)]
        self.assertEqual(grown_pet.growth.pet_rank, pet.growth.pet_rank)
        self.assertEqual(grown_pet.growth.alloc_point, pet.growth.alloc_point)
        self.assertEqual(grown_pet.growth.variable_ai, 500)
        self.assertEqual(grown_pet.state['level'], pet.state['level'] + 1)
        self.assertEqual(grown_pet.state['hp'], 10)  # no automatic healing
        self.assertEqual((grown_pet.state['mp'], grown_pet.state['max_mp']), (17, 31))
        self.assertEqual(grown_pet.skills, pet.skills)

    def test_six_caller_owned_capture_fields_are_mandatory_and_atomic(self):
        # Source gaps are genuinely unknown. Do not create fabricated MP,
        # EXP, rename or free-name values at the persistent owner boundary.
        for field in ('mp', 'max_mp', 'exp', 'max_exp', 'rename_flag', 'free_name'):
            with self.subTest(missing=field):
                incomplete = dict(self.pet.state)
                incomplete.pop(field)
                with self.assertRaisesRegex(ValueError, 'missing explicit caller state: ' + field):
                    self.capture(replace(self.pet, state=incomplete))
                self.assert_atomic()

        with self.assertRaisesRegex(ValueError, 'missing explicit caller state: mp'):
            self.capture(replace(self.pet, state={**self.pet.state, 'mp': None}))
        self.assert_atomic()

    def test_explicit_caller_owned_fields_survive_capture_and_disk(self):
        captured, _ = self.capture(self.pet)
        settled = self.coordinator.settle_persistent_group_battle_without_level_crossing(captured)
        self.coordinator.save_game('owner-fields', settled)
        restored = self.coordinator.continue_game('owner-fields').player_state.pets[PetSlot(0)]
        for field in ('mp', 'max_mp', 'exp', 'max_exp', 'rename_flag', 'free_name'):
            self.assertEqual(restored.state[field], self.pet.state[field])
        self.assert_atomic()

    def test_wrong_name_round_rejects_atomically(self):
        with self.assertRaisesRegex(ValueError, 'copied name drift'):
            self.capture(replace(self.pet, state={**self.pet.state, 'name': 'Wrong'}))
        self.assert_atomic()

    def test_nonzero_capture_variable_ai_round_rejects_atomically(self):
        with self.assertRaisesRegex(ValueError, 'variable_ai must be zero'):
            self.capture(replace(self.pet, growth=replace(self.pet.growth, variable_ai=500)))
        self.assert_atomic()

    def test_direct_capture_uses_same_name_and_variable_ai_guards(self):
        domain = SinglePlayerHistoricalDomain(static=self.stack.encounter_runtime.static_data,
                                              persistent=self.session.player_state)
        runtime = SinglePlayerHistoricalRuntime(domain, self.coordinator.topology)
        for pet, message in [
            (replace(self.pet, state={**self.pet.state, 'name': 'Wrong'}), 'copied name drift'),
            (replace(self.pet, growth=replace(self.pet.growth, variable_ai=1)), 'variable_ai must be zero')]:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                runtime.resolve_persistent_capture(
                    self.context.persistent_battle_state, attacker_id='player',
                    target_id=self.enemy.participant_id,
                    inputs=BattleCaptureInputs(
                        attacker_level=self.context.battle.player.level, attacker_charm=100,
                        attacker_fixed_dex=100, attacker_fixed_luck=7,
                        target_level=self.enemy.level, target_hp=10, target_max_hp=100,
                        target_fixed_dex=20, target_capture_default=99,
                        target_capturable=True, occupied_pet_slots=()),
                    roll_1_100=1, captured_pet=pet)
            self.assert_atomic()

    def test_unknown_growth_remains_explicit_unknown(self):
        context, _ = self.capture(replace(self.pet, growth=None))
        settled = self.coordinator.settle_persistent_group_battle_without_level_crossing(context)
        self.assertIsNone(settled.player_state.pets[PetSlot(0)].growth)

    def test_unknown_source_name_does_not_invent_name(self):
        enemy = replace(self.enemy, name=None)
        self.context = replace(self.context, persistent_battle_state=replace(
            self.context.persistent_battle_state, session=replace(
                self.context.persistent_battle_state.session, enemies=(enemy,))))
        self.capture(self.pet)  # supplied name remains an explicit source responsibility


if __name__ == '__main__':
    unittest.main()
