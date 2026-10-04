"""Synthetic probe fixtures are not claims about unprobed recovered rows."""
from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_mdfyattack_probe import analyze_runtime_objects


def fixture():
    entries = {548 + i: Recovered25PetSkillEntry(548 + i, 1, 1, 2, 0,
               'PETSKILL_Mdfyattack', code + b'|60')
               for i, code in enumerate((b'EA', b'WA', b'FI', b'WI'))}
    enemies = {i: SimpleNamespace(skill_slot_ids=(548 + i % 4, 0, -1)) for i in range(8)}
    return SimpleNamespace(skills=entries), SimpleNamespace(templates=enemies)


class MdfyAttackProbeTests(unittest.TestCase):
    def test_exact_family_population_and_safe_options(self):
        result = analyze_runtime_objects(*fixture())
        self.assertTrue(result['population_closed'])
        self.assertTrue(result['option_domain_closed'])
        self.assertEqual([r['element'] for r in result['rows']], ['earth', 'water', 'fire', 'wind'])
        self.assertEqual((result['slot_references'], result['templates']), (8, 8))

    def test_similarly_spelled_modifyattack_does_not_join_family(self):
        pets, enemies = fixture()
        pets.skills[544] = replace(pets.skills[548], skill_id=544, function_name='PETSKILL_Modifyattack')
        enemies.templates[0].skill_slot_ids = (548, 544)
        self.assertTrue(analyze_runtime_objects(pets, enemies)['population_closed'])

    def test_bad_option_preserves_population_but_not_semantic_closure(self):
        for raw in (b'EA', b'ea|60', b'EA|-1', b'EA|32768', b'WI|60\0', b'WI|\xff'):
            pets, enemies = fixture()
            pets.skills[548] = replace(pets.skills[548], option_bytes=raw)
            result = analyze_runtime_objects(pets, enemies)
            with self.subTest(raw=raw):
                self.assertTrue(result['population_closed'])
                self.assertFalse(result['option_domain_closed'])

    def test_missing_or_extra_callback_record_keeps_gate_open(self):
        for mutation in ('missing', 'extra'):
            pets, enemies = fixture()
            if mutation == 'missing':
                del pets.skills[548]
            else:
                pets.skills[552] = replace(pets.skills[548], skill_id=552)
            self.assertFalse(analyze_runtime_objects(pets, enemies)['population_closed'])

    def test_slot_and_template_counts_are_independent(self):
        pets, enemies = fixture()
        enemies.templates[0].skill_slot_ids = (548, 548)
        result = analyze_runtime_objects(pets, enemies)
        self.assertEqual((result['slot_references'], result['templates']), (9, 8))
        self.assertFalse(result['population_closed'])

    def test_derived_output_preserves_full_metadata_and_hash(self):
        pets, enemies = fixture()
        pets.skills[548] = replace(pets.skills[548], field=7, target=6, cost=11, illegal=1000)
        row = analyze_runtime_objects(pets, enemies)['rows'][0]
        self.assertEqual((row['field'], row['target'], row['cost'], row['illegal']), (7, 6, 11, 1000))
        self.assertEqual(len(row['option_sha256']), 64)
        self.assertNotIn('option_text', row)


if __name__ == '__main__':
    unittest.main()
