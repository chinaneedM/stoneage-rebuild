import unittest
from types import SimpleNamespace as S
from tools.stoneage_recovered25_modifyattack_probe import analyze_runtime_objects


def fixture():
    pets=S(skills={i:S(skill_id=i,field=1,target=6,cost=2,illegal=2000,
        function_name='PETSKILL_Modifyattack',option_bytes=code+b'|20') for i,code in zip((544,545,546,547),(b'EA',b'WA',b'FI',b'WI'))})
    enemies=S(templates={
        18:S(graphic_id=101543,skill_slot_ids=(0,0,0,546,0,0,0)),
        19:S(graphic_id=101533,skill_slot_ids=(0,0,0,0,545,0,0)),
        20:S(graphic_id=101532,skill_slot_ids=(0,0,0,544,0,0,0)),
    })
    return pets,enemies


class ModifyAttackProbeTests(unittest.TestCase):
    def test_full_population_separate_from_positive_pressure(self):
        pets,enemies=fixture();r=analyze_runtime_objects(pets,enemies)
        self.assertTrue(r['positive_references_closed'])
        self.assertTrue(r['population_closed'])
        self.assertTrue(r['exact_rows_closed'])
        self.assertTrue(r['exact_templates_closed'])
        self.assertEqual(r['callback_ids'],(544,545,546,547))
        self.assertEqual(r['referenced_ids'],(544,545,546))
        self.assertEqual(r['rows'][3]['slot_references'],0)
        self.assertEqual(r['rows'][0]['element_index'],0)
        self.assertEqual(r['rows'][0]['percent'],20)

    def test_spelling_neighbor_excluded(self):
        pets,enemies=fixture()
        pets.skills[544].function_name='PETSKILL_Mdfyattack'
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])

    def test_wrong_positive_slot_counts_stay_open(self):
        pets,enemies=fixture()
        enemies.templates[20].skill_slot_ids=(544,544,0,0,0,0,0)
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])

    def test_exact_row_drift_cannot_hide_behind_counts(self):
        for field,value in (('target',7),('illegal',1000),('option_bytes',b'EA|21')):
            pets,enemies=fixture();setattr(pets.skills[544],field,value)
            r=analyze_runtime_objects(pets,enemies)
            self.assertTrue(r['population_closed'])
            self.assertFalse(r['exact_rows_closed'])

    def test_template_graphic_or_slot_drift_cannot_hide_behind_counts(self):
        for field,value in (('graphic_id',101544),('skill_slot_ids',(546,0,0,0,0,0,0))):
            pets,enemies=fixture();setattr(enemies.templates[18],field,value)
            r=analyze_runtime_objects(pets,enemies)
            self.assertTrue(r['population_closed'])
            self.assertFalse(r['exact_templates_closed'])

    def test_unreferenced_population_drift_still_rejected(self):
        pets,enemies=fixture();del pets.skills[547]
        r=analyze_runtime_objects(pets,enemies)
        self.assertTrue(r['positive_references_closed'])
        self.assertFalse(r['population_closed'])
        self.assertFalse(r['exact_rows_closed'])


if __name__=='__main__':
    unittest.main()
