"""Source attribution, input drift and non-equivalence guards for the finite crosswalk."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from tools.stoneage_early_mail_venue_crosswalk import ROOT,REPORT,INPUTS,build,pointer,validate_report


def inputs():return {k:(ROOT/f).read_bytes() for k,(f,_) in INPUTS.items()}


class EarlySourceBoundaryTests(unittest.TestCase):
    def test_five_inputs_eight_comparisons_no_new_or_independent_double_count(self):
        o=build(inputs());self.assertEqual(len(o['records']),8)
        self.assertEqual(o['coverage']['distinct_original_bodies_referenced'],4)
        self.assertFalse(o['records'][0]['same_original_manual_two_reports_are_independent_witnesses'])
        bodies={(r['original_source'],r['original_sha256']) for row in o['records'] for r in row['source_refs']}
        self.assertEqual(len(bodies),4)

    def test_input_drift_and_missing_report_rejected(self):
        i=inputs();i['manual']+=b'\n'
        with self.assertRaisesRegex(ValueError,'byte pin'):build(i)
        i=inputs();i.pop('cards')
        with self.assertRaisesRegex(ValueError,'five input'):build(i)

    def test_every_evidence_pointer_exists_with_original_source_capture_and_hash(self):
        o=build(inputs());data={str(ROOT/f):json.loads((ROOT/f).read_bytes()) for f,_ in INPUTS.values()}
        for row in o['records']:
            for r in row['source_refs']:
                pointer(data[r['derived_report']],r['json_pointer'])
                self.assertEqual(len(r['original_sha256']),64);self.assertEqual(len(r['actual_capture']),14)
        with self.assertRaisesRegex(ValueError,'evidence pointer'):pointer(data[next(iter(data))],'/records/9999')

    def test_shared_names_or_omission_not_a_patch_or_entity_proof(self):
        for key in ('automatic_entity_or_rule_merge_allowed','historical_update_or_rule_removal_proven','numeric_id_price_timer_projection_allowed','original_server_execution_proven'):
            o=build(inputs());o['records'][3][key]=True
            with self.assertRaises(ValueError):validate_report(o)

    def test_early_level_not_projected_to_quiz_and_two_roles_not_two_slots(self):
        o=build(inputs());o['records'][2]['source_facts']['later_quiz_threshold_and_fee']={'level':9}
        with self.assertRaisesRegex(ValueError,'exemption projected'):validate_report(o)
        o=build(inputs());o['records'][5]['source_facts']['later_dedicated_slot_count']=2
        with self.assertRaisesRegex(ValueError,'two dedicated slots'):validate_report(o)

    def test_archive_records_keep_comparison_type_and_no_new_content_entities(self):
        o=json.loads(REPORT.read_text());validate_report(o)
        c=json.loads((ROOT/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for r in o['records']:
            self.assertLessEqual(set(c['record_contract']['required']),r.keys());self.assertIn(r['collection'],c['required_collections'])
            self.assertEqual(r['collection'],'sources');self.assertIsNone(r['unknown_identity_or_runtime_details'])
        self.assertEqual(o['coverage']['new_game_entities_or_server_rules_recovered'],0)


if __name__=='__main__':unittest.main()
