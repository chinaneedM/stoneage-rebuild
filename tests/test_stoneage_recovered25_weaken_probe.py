"""Synthetic probe fixtures are not claims about unprobed recovered rows."""
from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_weaken_probe import analyze_runtime_objects


def fixture():
    raw='虛 turn=3 成=50'.encode('cp950')
    entries = {i: Recovered25PetSkillEntry(i,1,3,2,1000,'PETSKILL_Weaken',raw)
               for i in (575,576)}
    enemies = {i: SimpleNamespace(skill_slot_ids=(575+i%2,0,-1)) for i in range(6)}
    enemies[0].skill_slot_ids=(575,576,-1)
    return SimpleNamespace(skills=entries),SimpleNamespace(templates=enemies)


class WeakenProbeTests(unittest.TestCase):
    def test_exact_family_population_and_safe_options(self):
        result = analyze_runtime_objects(*fixture())
        self.assertTrue(result['population_closed'])
        self.assertTrue(result['option_domain_closed'])
        self.assertEqual([r['turn'] for r in result['rows']], [3,3])
        self.assertEqual((result['slot_references'], result['templates']), (7, 6))

    def test_similarly_spelled_modifyattack_does_not_join_family(self):
        pets, enemies = fixture()
        pets.skills[544] = replace(pets.skills[575], skill_id=544, function_name='PETSKILL_Modifyattack')
        enemies.templates[0].skill_slot_ids = (575,576,544)
        self.assertTrue(analyze_runtime_objects(pets, enemies)['population_closed'])

    def test_bad_option_preserves_population_but_not_semantic_closure(self):
        for raw in (b'bad',b'\0',b'\xff','虛 turn=0 成=50'.encode('cp950'),'虛 turn=3 成=0'.encode('cp950')):
            pets, enemies = fixture()
            pets.skills[575] = replace(pets.skills[575], option_bytes=raw)
            result = analyze_runtime_objects(pets, enemies)
            with self.subTest(raw=raw):
                self.assertTrue(result['population_closed'])
                self.assertFalse(result['option_domain_closed'])

    def test_missing_or_extra_callback_record_keeps_gate_open(self):
        for mutation in ('missing', 'extra'):
            pets, enemies = fixture()
            if mutation == 'missing':
                del pets.skills[575]
            else:
                pets.skills[577] = replace(pets.skills[575], skill_id=577)
            self.assertFalse(analyze_runtime_objects(pets, enemies)['population_closed'])

    def test_slot_and_template_counts_are_independent(self):
        pets, enemies = fixture()
        enemies.templates[0].skill_slot_ids = (575,575,576)
        result = analyze_runtime_objects(pets, enemies)
        self.assertEqual((result['slot_references'], result['templates']), (8, 6))
        self.assertFalse(result['population_closed'])

    def test_derived_output_preserves_full_metadata_and_hash(self):
        pets, enemies = fixture()
        pets.skills[575] = replace(pets.skills[575], field=7, target=6, cost=11, illegal=1000)
        row = analyze_runtime_objects(pets, enemies)['rows'][0]
        self.assertEqual((row['field'], row['target'], row['cost'], row['illegal']), (7, 6, 11, 1000))
        self.assertEqual(len(row['option_sha256']), 64)
        self.assertNotIn('option_text', row)


if __name__ == '__main__':
    unittest.main()
