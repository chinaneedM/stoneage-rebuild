"""Independent file/object binding and exact-placement mutation controls."""
from dataclasses import replace
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools import stoneage_battlemodel_placement_capability as capability
from tools.stoneage_recovered25_enemybase_runtime import Recovered25EnemybaseRuntime
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_recovered25_petskill_pressure_probe import (
    analyze_runtime_objects, summarize_pressure, classify, CLOSED_RUNTIME_CALLBACKS,
)


class PlacementCapabilityTests(unittest.TestCase):
    def setUp(self):
        self.pets, identities = fixture()
        templates = {}
        for tempno in (1178, 1179):
            t = spawned(tempno).template
            templates[tempno] = PetTemplateBridge(tempno, t.graphic_id, None, t.ai,
                0, 0, 0, 0, 3, (638,), skill_slot_ids=t.skill_slot_ids,
                base_vital=t.base_vital, base_strength=t.base_strength,
                base_toughness=t.base_toughness, base_dexterity=t.base_dexterity)
        self.enemies = Recovered25EnemybaseRuntime(templates)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        # Independent controls replace evidence hashes/parser I/O only.
        # Production ID/slot/graphic/base/MODAI/population rules remain intact.
        contents = (b"independently authored skill file\n", b"independently authored template file\n")
        for name, content in zip(("petskill.txt", "enemybase.txt"), contents):
            (self.root / name).write_bytes(content)
        for target, value in (("EXPECTED_PETSKILL_SHA256", hashlib.sha256(contents[0]).hexdigest()),
                              ("EXPECTED_ENEMYBASE_SHA256", hashlib.sha256(contents[1]).hexdigest())):
            p = patch.object(capability, target, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        p.start(); self.addCleanup(p.stop)
        self.identity = self.certify()

    def certify(self, pets=None, enemies=None):
        pets = self.pets if pets is None else pets
        enemies = self.enemies if enemies is None else enemies
        with patch.object(capability, "load_recovered25_petskill_runtime", return_value=pets), \
             patch.object(capability, "load_recovered25_enemybase_runtime", return_value=enemies):
            return capability.verify_placement_population(pets, enemies, data_dir=self.root, setup=None)

    def qualified(self, pets=None, enemies=None, identity=None, **kwargs):
        return capability.conditional_battlemodel_placements(
            self.pets if pets is None else pets, self.enemies if enemies is None else enemies,
            identity=self.identity if identity is None else identity, **kwargs)

    def mutated_template(self, tempno=1178, **change):
        templates = dict(self.enemies.templates)
        templates[tempno] = replace(templates[tempno], **change)
        return replace(self.enemies, templates=templates)

    def test_only_two_exact_slots_qualify_and_callback_alone_stays_open(self):
        self.assertEqual(self.qualified(), {(1178, 2, 638), (1179, 2, 638)})
        self.assertEqual(classify("PETSKILL_BattleModel"), "open")
        self.assertNotIn("PETSKILL_BattleModel", CLOSED_RUNTIME_CALLBACKS)
        self.assertNotIn("control-", repr(self.identity))

    def test_missing_dict_or_detached_identity_cannot_close_the_callback(self):
        for identity in (None, {"petskill_sha256": capability.EXPECTED_PETSKILL_SHA256}, "verified"):
            self.assertFalse(capability.conditional_battlemodel_placements(self.pets, self.enemies, identity=identity))
        with self.assertRaisesRegex(TypeError, "verify_placement_population"):
            capability.VerifiedPlacementPopulation()
        result = analyze_runtime_objects(self.pets, self.enemies)
        self.assertEqual(result["conditional_placements"], ())
        self.assertEqual(result["rows"][0]["status"], "open")

    def test_wrong_or_broader_execution_scope_never_qualifies(self):
        for scope in ("", "player_magic", "all_BattleModel", "ride_and_equipment", "unbounded", None, True, 3):
            self.assertFalse(self.qualified(scope=scope))

    def test_whole_file_drift_is_rejected_before_parser_admission(self):
        for name in ("petskill.txt", "enemybase.txt"):
            path = self.root / name; original = path.read_bytes()
            path.write_bytes(original + b"changed control")
            with self.assertRaisesRegex(ValueError, "whole-file"):
                self.certify()
            path.write_bytes(original)

    def test_mutated_file_during_reparse_cannot_issue_a_certificate(self):
        def altered(*args, **kwargs):
            (self.root / "enemybase.txt").write_bytes(b"replaced while parsing")
            return self.enemies
        with patch.object(capability, "load_recovered25_petskill_runtime", return_value=self.pets), \
             patch.object(capability, "load_recovered25_enemybase_runtime", side_effect=altered), \
             self.assertRaisesRegex(ValueError, "whole-file"):
            capability.verify_placement_population(self.pets, self.enemies, data_dir=self.root, setup=None)

    def test_objects_detached_from_verified_parser_output_reject(self):
        changed = self.mutated_template(ai=151)
        with patch.object(capability, "load_recovered25_petskill_runtime", return_value=self.pets), \
             patch.object(capability, "load_recovered25_enemybase_runtime", return_value=self.enemies), \
             self.assertRaisesRegex(ValueError, "loaded-object"):
            capability.verify_placement_population(self.pets, changed, data_dir=self.root, setup=None)

    def test_stale_binding_catches_unrelated_semantics_and_both_placements(self):
        changed = self.mutated_template(1179, earth=9)
        self.assertFalse(self.qualified(enemies=changed))
        result = analyze_runtime_objects(self.pets, changed, capability_identity=self.identity)
        self.assertEqual(result["conditional_placements"], ())
        self.assertEqual(result["rows"][0]["status"], "open")

    def test_fresh_identity_does_not_override_row_or_complete_callback_population(self):
        for skill_id in (638, 641, 649, 650):
            for field, value in (("field", 0), ("target", 7), ("cost", 2), ("illegal", 0),
                                 ("function_name", "PETSKILL_NormalAttack"), ("option_bytes", b"drift")):
                rows = dict(self.pets.skills); rows[skill_id] = replace(rows[skill_id], **{field: value})
                changed = replace(self.pets, skills=rows)
                with self.subTest(skill=skill_id, field=field):
                    self.assertFalse(self.qualified(pets=changed, identity=self.certify(pets=changed)))
        for skill_id in (638, 641):
            rows = dict(self.pets.skills); del rows[skill_id]
            changed = replace(self.pets, skills=rows)
            self.assertFalse(self.qualified(pets=changed, identity=self.certify(pets=changed)))
        rows = dict(self.pets.skills); rows[777] = replace(rows[638], skill_id=777)
        changed = replace(self.pets, skills=rows)
        self.assertFalse(self.qualified(pets=changed, identity=self.certify(pets=changed)))

    def test_fresh_identity_rejects_graphic_stats_MODAI_and_moved_extra_sibling_slots(self):
        for field, value in (("graphic_id", 101868), ("base_vital", 39), ("base_strength", 41),
                             ("base_toughness", 16), ("base_dexterity", 38), ("ai", 151),
                             ("skill_slot_ids", (0, 0, 0, 638, 0, 0, 0)),
                             ("skill_slot_ids", (0, 0, 638, 638, 0, 0, 0)),
                             ("skill_slot_ids", (0, 0, 638, 641, 0, 0, 0)),
                             ("skill_slot_ids", (0, 0, 638))):
            changed = self.mutated_template(**{field: value})
            with self.subTest(field=field):
                self.assertFalse(self.qualified(enemies=changed, identity=self.certify(enemies=changed)))
        for skill_id in (641, 649, 650):
            changed = self.mutated_template(skill_slot_ids=(0, 0, skill_id, 0, 0, 0, 0))
            self.assertFalse(self.qualified(enemies=changed, identity=self.certify(enemies=changed)))

    def test_incomplete_or_extra_positive_template_population_stays_open(self):
        for templates in ({1178: self.enemies.templates[1178]},
                          {**self.enemies.templates, 1200: replace(self.enemies.templates[1178], tempno=1200)}):
            changed = replace(self.enemies, templates=templates)
            self.assertFalse(self.qualified(enemies=changed, identity=self.certify(enemies=changed)))

    def test_pressure_is_conditional_and_next_open_advances_without_neighbor_promotion(self):
        rows = dict(self.pets.skills)
        for skill_id, callback in ((1, "PETSKILL_NormalAttack"), (200, "PETSKILL_Merge"), (625, "PETSKILL_BecomeFox")):
            rows[skill_id] = replace(rows[638], skill_id=skill_id, function_name=callback)
        pets = replace(self.pets, skills=rows)
        templates = dict(self.enemies.templates)
        templates[100] = replace(templates[1178], tempno=100, skill_slot_ids=(1, 200, 625, 0, 0, 0, 0))
        enemies = replace(self.enemies, templates=templates)
        identity = self.certify(pets, enemies)
        before = (repr(pets), repr(enemies))
        result = analyze_runtime_objects(pets, enemies, capability_identity=identity)
        self.assertEqual(summarize_pressure(result), dict(total=5, closed=3, open=1, historical_ub=1))
        model = next(row for row in result["rows"] if row["callback"] == "PETSKILL_BattleModel")
        self.assertEqual(model["status"], "closed_conditional_runtime")
        self.assertEqual(model["capability_kind"], "CONDITIONAL_BOUNDED_CAPABILITY")
        self.assertEqual(model["command_entry_reachability"], "OPEN_SEPARATE_AXIS_NOT_INFERRED")
        self.assertEqual(model["skill_ids"], (638,))
        self.assertEqual(result["next_open"]["callback"], "PETSKILL_BecomeFox")
        self.assertEqual((repr(pets), repr(enemies)), before)


if __name__ == "__main__":
    unittest.main()
