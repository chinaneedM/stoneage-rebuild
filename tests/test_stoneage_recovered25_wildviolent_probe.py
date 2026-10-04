from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry
from tools.stoneage_recovered25_wildviolent_probe import analyze_runtime_objects


def fixture():
    # Independent synthetic mechanics; not an asserted recovered OPTION row.
    entry=Recovered25PetSkillEntry(541,1,3,7,1000,'PETSKILL_WildViolentAttack',
                                   '攻%50防%-50避12'.encode('cp950'))
    return (SimpleNamespace(skills={541:entry}),
            SimpleNamespace(templates={i:SimpleNamespace(skill_slot_ids=(541,0,-1)) for i in range(7)}))


class WildViolentProbeTests(unittest.TestCase):
    def test_positive_reference_population_is_exact(self):
        result=analyze_runtime_objects(*fixture())
        self.assertTrue(result['population_closed'])
        self.assertTrue(result['conditional_option_domain_closed'])
        self.assertEqual((result['slot_references'],result['templates']),(7,7))
        self.assertFalse(result['rows'][0]['utf8_execution_matches_conditional_cp950'])

    def test_unreferenced_exact_callback_rows_are_enumerated(self):
        pets,enemies=fixture()
        pets.skills[700]=replace(pets.skills[541],skill_id=700)
        result=analyze_runtime_objects(pets,enemies)
        self.assertEqual([r['id'] for r in result['rows']],[541,700])
        self.assertEqual(result['rows'][1]['slot_references'],0)
        self.assertTrue(result['population_closed'])

    def test_neighbor_spelling_is_not_admitted(self):
        pets,enemies=fixture()
        pets.skills[540]=replace(pets.skills[541],skill_id=540,function_name='PETSKILL_AttackCrazed')
        self.assertEqual(len(analyze_runtime_objects(pets,enemies)['rows']),1)

    def test_negative_high_preserves_observed_value_and_open_domain(self):
        pets,enemies=fixture()
        pets.skills[541]=replace(pets.skills[541],option_bytes='攻%50避-10'.encode('cp950'))
        result=analyze_runtime_objects(pets,enemies)
        self.assertTrue(result['population_closed'])
        self.assertFalse(result['conditional_option_domain_closed'])
        self.assertEqual(result['rows'][0]['additive_dodge_percent_points'],-10)
        self.assertEqual(result['rows'][0]['unsafe_reason'],'SIGNED_HIGH_SHIFT_UNDEFINED')

    def test_unparseable_bytes_fail_closed(self):
        for raw in (b'\xff',b'\0','攻%nan'.encode('cp950')):
            pets,enemies=fixture();pets.skills[541]=replace(pets.skills[541],option_bytes=raw)
            self.assertFalse(analyze_runtime_objects(pets,enemies)['conditional_option_domain_closed'])

    def test_extra_uses_and_extra_referenced_ids_are_detected(self):
        pets,enemies=fixture();enemies.templates[0].skill_slot_ids=(541,541,-1)
        self.assertFalse(analyze_runtime_objects(pets,enemies)['population_closed'])
        pets,enemies=fixture();pets.skills[542]=replace(pets.skills[541],skill_id=542)
        enemies.templates[0].skill_slot_ids=(542,0,-1)
        self.assertFalse(analyze_runtime_objects(pets,enemies)['population_closed'])

    def test_metadata_hash_and_no_raw_text(self):
        row=analyze_runtime_objects(*fixture())['rows'][0]
        self.assertEqual((row['field'],row['target'],row['cost'],row['illegal']),(1,3,7,1000))
        self.assertEqual(len(row['option_sha256']),64)
        self.assertNotIn('option_bytes_raw',row)


if __name__=='__main__':unittest.main()
