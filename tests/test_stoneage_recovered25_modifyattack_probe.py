import unittest
from types import SimpleNamespace as S
from tools.stoneage_recovered25_modifyattack_probe import analyze_runtime_objects


def fixture():
    pets=S(skills={i:S(skill_id=i,field=1,target=0,cost=2,illegal=0,
        function_name='PETSKILL_Modifyattack',option_bytes=b'EA|20') for i in (543,544,545,546)})
    enemies=S(templates={i:S(graphic_id=i+100,skill_slot_ids=(skill,0,0,0,0,0,0)) for i,skill in enumerate((544,545,546),10)})
    return pets,enemies


class ModifyAttackProbeTests(unittest.TestCase):
    def test_full_population_separate_from_positive_pressure(self):
        pets,enemies=fixture();r=analyze_runtime_objects(pets,enemies)
        self.assertTrue(r['positive_references_closed'])
        self.assertEqual(r['callback_ids'],(543,544,545,546))
        self.assertEqual(r['referenced_ids'],(544,545,546))
        self.assertEqual(r['rows'][0]['slot_references'],0)
        self.assertEqual(r['rows'][0]['element_index'],0)
        self.assertEqual(r['rows'][0]['percent'],20)

    def test_spelling_neighbor_excluded(self):
        pets,enemies=fixture()
        pets.skills[544].function_name='PETSKILL_Mdfyattack'
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])

    def test_wrong_positive_slot_counts_stay_open(self):
        pets,enemies=fixture()
        enemies.templates[10].skill_slot_ids=(544,544,0,0,0,0,0)
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])


if __name__=='__main__':
    unittest.main()
