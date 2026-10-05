import unittest
from types import SimpleNamespace as S
from tools.stoneage_recovered25_2battletimid_probe import analyze_runtime_objects


def fixture():
    pets=S(skills={636:S(skill_id=636,field=1,target=6,cost=2,illegal=0,
        function_name='PETSKILL_2BattleTimid',option_bytes=b'')})
    enemies=S(templates={1:S(graphic_id=101,skill_slot_ids=(636,0,0,0,0,0,0)),
                         2:S(graphic_id=102,skill_slot_ids=(0,636,0,0,0,0,0))})
    return pets,enemies


class TwoBattleTimidProbeTests(unittest.TestCase):
    def test_discovery_does_not_accept_unpinned_identity(self):
        r=analyze_runtime_objects(*fixture(),expected_callback_ids=None,expected_exact_rows=None,expected_template_rows=None)
        self.assertTrue(r['positive_references_closed'])
        self.assertFalse(r['population_closed'])
        self.assertFalse(r['exact_rows_closed'])
        self.assertFalse(r['exact_templates_closed'])

    def test_neighbor_callback_does_not_count(self):
        pets,enemies=fixture();pets.skills[636].function_name='PETSKILL_BattleTimid'
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])

    def test_unreferenced_rows_are_in_complete_population(self):
        pets,enemies=fixture();pets.skills[700]=S(**(vars(pets.skills[636])|{'skill_id':700}))
        r=analyze_runtime_objects(pets,enemies,expected_callback_ids=(636,))
        self.assertTrue(r['positive_references_closed'])
        self.assertFalse(r['population_closed'])
        self.assertEqual(r['callback_ids'],(636,700))

    def test_repeated_reference_cannot_hide_template_count_drift(self):
        pets,enemies=fixture();enemies.templates={1:S(graphic_id=101,skill_slot_ids=(636,636,0,0,0,0,0))}
        self.assertFalse(analyze_runtime_objects(pets,enemies)['positive_references_closed'])


if __name__=='__main__':unittest.main()
