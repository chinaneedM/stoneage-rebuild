from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_refresh_probe import analyze_runtime_objects


def fixture():
    # Synthetic three-row family; not a claim about the real full population.
    skills={i:Recovered25PetSkillEntry(i,1,2,2,2000,'PETSKILL_Refresh',s.encode('cp950'))
            for i,s in ((326,'全'),(583,'默'),(592,'全'))}
    templates={i:SimpleNamespace(skill_slot_ids=(583 if i%2 else 592,0,-1)) for i in range(6)}
    return SimpleNamespace(skills=skills),SimpleNamespace(templates=templates)


class RefreshProbeTests(unittest.TestCase):
    def test_unpinned_full_population_remains_open(self):
        result=analyze_runtime_objects(*fixture(),expected_ids=None)
        self.assertTrue(result['references_match'])
        self.assertFalse(result['population_closed'])
        self.assertTrue(result['conditional_options_safe'])
        self.assertEqual(result['rows'][0]['slot_references'],0)

    def test_exact_callback_family_and_explicit_full_pin(self):
        pets,enemies=fixture()
        pets.skills[700]=replace(pets.skills[583],skill_id=700,function_name='PETSKILL_RefreshExtra')
        result=analyze_runtime_objects(pets,enemies,expected_ids=(326,583,592))
        self.assertTrue(result['population_closed'])
        self.assertEqual(result['callback_ids'],(326,583,592))

    def test_unreferenced_extra_or_missing_row_breaks_population_pin(self):
        for mutation in ('extra','missing'):
            pets,enemies=fixture()
            if mutation=='extra':pets.skills[777]=replace(pets.skills[326],skill_id=777)
            else:del pets.skills[326]
            self.assertFalse(analyze_runtime_objects(pets,enemies,expected_ids=(326,583,592))['population_closed'])

    def test_option_drift_does_not_hide_bad_unreferenced_rows(self):
        for raw in (b'',b'bad',b'\xff',b'\0','默'.encode()):
            pets,enemies=fixture();pets.skills[326]=replace(pets.skills[326],option_bytes=raw)
            result=analyze_runtime_objects(pets,enemies,expected_ids=(326,583,592))
            self.assertTrue(result['population_closed'])
            self.assertFalse(result['conditional_options_safe'])

    def test_slot_counts_templates_and_metadata_independent(self):
        pets,enemies=fixture();enemies.templates[0].skill_slot_ids=(592,592,583)
        pets.skills[583]=replace(pets.skills[583],field=9,target=6,cost=11,illegal=1000)
        result=analyze_runtime_objects(pets,enemies,expected_ids=(326,583,592))
        self.assertEqual((result['slot_references'],result['templates']),(8,6))
        self.assertFalse(result['population_closed'])
        row=result['rows'][1]
        self.assertEqual((row['field'],row['target'],row['cost'],row['illegal']),(9,6,11,1000))
        self.assertEqual(len(row['option_sha256']),64)
        self.assertNotIn('option_text',row)


if __name__=='__main__':unittest.main()
