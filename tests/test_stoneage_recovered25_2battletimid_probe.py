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

    def test_exact_metadata_option_and_placement_drift_fail_independently(self):
        import hashlib
        expected=((636,1,6,2,0,2,0,hashlib.sha256(b'').hexdigest(),False,True,True),)
        placements=((1,101,(1,),(636,)),(2,102,(2,),(636,)))
        def analyze(pets,enemies):
            return analyze_runtime_objects(pets,enemies,expected_callback_ids=(636,),
                expected_exact_rows=expected,expected_template_rows=placements)
        self.assertTrue(analyze(*fixture())['exact_rows_closed'])
        self.assertTrue(analyze(*fixture())['exact_templates_closed'])
        for key,value in (('illegal',1),('target',7),('option_bytes',b'x')):
            pets,enemies=fixture();setattr(pets.skills[636],key,value)
            result=analyze(pets,enemies)
            self.assertTrue(result['population_closed'])
            self.assertFalse(result['exact_rows_closed'])
        pets,enemies=fixture();enemies.templates[1].graphic_id=103
        self.assertFalse(analyze(pets,enemies)['exact_templates_closed'])


if __name__=='__main__':unittest.main()
