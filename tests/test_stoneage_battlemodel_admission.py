"""Controlled synthetic OPTIONs exercise admission without preserved payloads."""
from dataclasses import replace
import hashlib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import PROFILE_BIG5, PROFILE_UTF8
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry, Recovered25PetSkillRuntime,
)


def fixture():
    rows = {}
    identities = {}
    for skill_id in (638, 641, 649, 650):
        # Independent control data, not the preserved seven-field OPTION.
        raw = ("5|4|麻|1|30|攻23|7 8|control-" + str(skill_id)).encode("big5")
        illegal = 20000 if skill_id == 649 else 10000
        rows[skill_id] = Recovered25PetSkillEntry(
            skill_id, 1, 3, 3, illegal, bridge.CALLBACK_NAME, raw,
        )
        identities[skill_id] = (1, 3, 3, illegal, len(raw), hashlib.sha256(raw).hexdigest())
    return Recovered25PetSkillRuntime(rows, "synthetic admission fixture"), identities


def spawned(tempno=1178):
    graphic, base = {1178: (101867, (38, 40, 15, 37, 150)),
                     1179: (101868, (42, 35, 20, 34, 150))}[tempno]
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy", side="enemy", kind="enemy"),
        template=SimpleNamespace(
            tempno=tempno, graphic_id=graphic, base_vital=base[0],
            base_strength=base[1], base_toughness=base[2], base_dexterity=base[3],
            ai=base[4], skill_slot_ids=(0, 0, 638, 0, 0, 0, 0),
        ),
    )


class BattleModelAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.runtime, identities = fixture()
        # Replace only evidence digests/lengths with controlled fixture identity.
        # Production slot/graphic/base/AI/profile rules remain untouched.
        self.identity_patch = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        self.identity_patch.start()
        self.addCleanup(self.identity_patch.stop)

    def resolve(self, *, actor=None, runtime=None, **kwargs):
        inputs = dict(skill_slot=2, target_slot=5, petskill_runtime=runtime or self.runtime,
                      profile=PROFILE_BIG5, source_profile="iris", powers_before=(100, 80, 60))
        inputs.update(kwargs)
        return bridge.resolve_enemy_ai_battlemodel_submission(actor or spawned(), **inputs)

    def test_both_exact_positive_templates_use_runtime_index2(self):
        for tempno in (1178, 1179):
            with self.subTest(tempno=tempno):
                result = self.resolve(actor=spawned(tempno))
                self.assertEqual((result.template_tempno, result.skill_slot, result.skill_id),
                                 (tempno, 2, 638))
                self.assertEqual(result.semantic_command_name, "BATTLE_COM_S_BATTLE_MODEL")
                self.assertEqual(result.setup.rng_draws, 0)
                self.assertEqual((result.setup.attack_type, result.setup.object_count), (5, 4))
                self.assertEqual(result.setup.skill_array, 0)

    def test_explicit_source_and_charset_profiles_preserve_separate_effects(self):
        for source in ("gavin", "iris", "bismarck"):
            with self.subTest(source=source):
                big5 = self.resolve(source_profile=source)
                utf8 = self.resolve(source_profile=source, profile=PROFILE_UTF8)
                self.assertEqual(big5.setup.powers, (23, 80, 60))
                self.assertEqual(big5.option_shape.status_kind, "paralysis")
                self.assertEqual(big5.option_shape.status_index, 2)
                self.assertEqual(utf8.setup.powers, (100, 80, 60))
                self.assertFalse(utf8.option_shape.status_known)
                self.assertIsNone(utf8.option_shape.status_index)
        for kwargs in ({"profile": ""}, {"source_profile": ""}, {"profile": "cp950"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.resolve(**kwargs)

    def test_unselected_rows_are_part_of_admission_identity(self):
        for skill_id in (641, 649, 650):
            for field, value in (("illegal", 0), ("option_bytes", b"different control"),
                                 ("function_name", "PETSKILL_BecomeFox")):
                rows = dict(self.runtime.skills)
                rows[skill_id] = replace(rows[skill_id], **{field: value})
                with self.subTest(skill_id=skill_id, field=field), self.assertRaises(ValueError):
                    self.resolve(runtime=Recovered25PetSkillRuntime(rows, "mutated control"))
        for missing in (638, 641):
            rows = dict(self.runtime.skills)
            del rows[missing]
            with self.subTest(missing=missing), self.assertRaises(ValueError):
                self.resolve(runtime=Recovered25PetSkillRuntime(rows, "missing row"))
        rows = dict(self.runtime.skills)
        rows[777] = replace(rows[638], skill_id=777)
        with self.assertRaisesRegex(ValueError, "population"):
            self.resolve(runtime=Recovered25PetSkillRuntime(rows, "extra row"))

    def test_selected_metadata_and_bytes_drift_are_rejected(self):
        for field, value in (("target", 7), ("cost", 2), ("field", 0),
                             ("option_bytes", b"mutated"), ("option_bytes", b"nul\0control")):
            rows = dict(self.runtime.skills)
            rows[638] = replace(rows[638], **{field: value})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.resolve(runtime=Recovered25PetSkillRuntime(rows, "selected mutation"))

    def test_template_graphic_stats_ai_and_positive_population_are_exact(self):
        mutations = (("tempno", 1180), ("graphic_id", 101868),
                     ("base_vital", 39), ("base_strength", 41),
                     ("base_toughness", 16), ("base_dexterity", 38), ("ai", 151),
                     ("skill_slot_ids", (0, 0, 0, 638, 0, 0, 0)),
                     ("skill_slot_ids", (0, 0, 638, 638, 0, 0, 0)),
                     ("skill_slot_ids", (0, 0, 638, 641, 0, 0, 0)),
                     ("skill_slot_ids", (0, 0, 638)))
        for field, value in mutations:
            actor = spawned()
            setattr(actor.template, field, value)
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.resolve(actor=actor)

    def test_unreferenced_ids_wrong_actors_and_carrier_indices_are_rejected(self):
        for skill_id in (641, 649, 650):
            actor = spawned()
            actor.template.skill_slot_ids = (0, 0, skill_id, 0, 0, 0, 0)
            with self.subTest(skill_id=skill_id), self.assertRaises(ValueError):
                self.resolve(actor=actor)
        for key, value in (("side", "player"), ("kind", "pet")):
            actor = spawned()
            setattr(actor.participant, key, value)
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.resolve(actor=actor)
        for kwargs in ({"skill_slot": 3}, {"skill_slot": True},
                       {"target_slot": 10}, {"target_slot": -1},
                       {"powers_before": (-1, 80, 60)}, {"powers_before": (100, True, 60)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.resolve(**kwargs)

    def test_forged_typed_submission_cannot_bypass_callback_or_slot_rules(self):
        valid = self.resolve()
        for change in ({"skill_slot": 3}, {"skill_id": 641},
                       {"callback": "PETSKILL_BatFly"}, {"template_graphic": 101868},
                       {"semantic_command_name": "BATTLE_COM_ATTACK"},
                       {"setup": replace(valid.setup, powers=(100, 80, 60))},
                       {"setup": replace(valid.setup, packed_com2=5)},
                       {"powers_before": (100, 81, 60)}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(valid, **change)
        self.assertNotIn("control-638", repr(valid))

    def test_target_plan_uses_live_snapshot_instead_of_scheduling_carrier(self):
        valid = self.resolve(target_slot=5)
        plan = valid.target_plan(living_opposing_slots=(0, 6), excess_target_rolls=(1, 0))
        self.assertEqual([a.target_slot for a in plan.attacks], [0, 6, 6, 0])
        self.assertEqual([a.object_index for a in plan.attacks], [0, 1, 2, 3])
        self.assertEqual([a.action_number for a in plan.attacks], [7, 8, 7, 8])
        self.assertEqual(plan.target_rng_draws, 2)
        covered = valid.target_plan(living_opposing_slots=(0, 1, 2, 3, 4), excess_target_rolls=())
        self.assertEqual([a.object_index for a in covered.attacks], [0, 1, 2, 3, 0])
        for slots, draws in (((), ()), ((10,), (0, 0, 0)), ((0, 0), (0, 0)),
                             ((0, 6), (0,)), ((0, 6), (2, 0)), ((0, 6), (True, 0))):
            with self.subTest(slots=slots, draws=draws), self.assertRaises(ValueError):
                valid.target_plan(living_opposing_slots=slots, excess_target_rolls=draws)


if __name__ == "__main__":
    unittest.main()
