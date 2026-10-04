import unittest
from dataclasses import replace
from types import SimpleNamespace
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_attack_crazed_probe import analyze_runtime_objects

def fixture():
    pets=SimpleNamespace(skills={613:Recovered25PetSkillEntry(613,1,6,2,1000,'PETSKILL_AttackCrazed',b'3')})
    enemies=SimpleNamespace(templates={i:SimpleNamespace(skill_slot_ids=(613,0,-1)) for i in range(9)})
    return pets,enemies

class AttackCrazedProbeTests(unittest.TestCase):
    def test_population_and_safe_option_close(self):
        r=analyze_runtime_objects(*fixture())
        self.assertTrue(r['population_closed']);self.assertTrue(r['option_domain_closed'])
        self.assertEqual(r['rows'][0]['attack_count'],3)

    def test_invalid_option_does_not_close_data_gate(self):
        for raw in (b'',b'-1',b'20',b'3\0'):
            p,e=fixture();p.skills[613]=replace(p.skills[613],option_bytes=raw)
            r=analyze_runtime_objects(p,e)
            self.assertTrue(r['population_closed']);self.assertFalse(r['option_domain_closed'])

    def test_missing_row_or_extra_row_remains_open(self):
        for mutation in ('missing','extra'):
            p,e=fixture()
            if mutation=='missing':p.skills.clear()
            else:p.skills[614]=replace(p.skills[613],skill_id=614)
            self.assertFalse(analyze_runtime_objects(p,e)['population_closed'])

    def test_duplicate_slots_count_independently_of_templates(self):
        p,e=fixture();e.templates[0].skill_slot_ids=(613,613)
        r=analyze_runtime_objects(p,e)
        self.assertEqual((r['slot_references'],r['templates']),(10,9));self.assertFalse(r['population_closed'])

    def test_template_drift_remains_open(self):
        p,e=fixture();del e.templates[0]
        self.assertFalse(analyze_runtime_objects(p,e)['option_domain_closed'])
if __name__=='__main__':unittest.main()
