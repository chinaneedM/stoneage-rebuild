import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_adult_origin_r117 as audit


class AdultOriginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objects, cls.pins = audit.load_inputs()

    def test_exact_replay_and_separate_temporal_semantics(self):
        report = audit.verify()
        self.assertEqual(report['qualification']['origin_class'], 'ORIGIN_UNRESOLVED')
        self.assertEqual(report['documentary_time_evidence']['accepted_capture'], '20011120063019')
        self.assertIsNone(report['qualification']['first_introduced_date'])
        self.assertFalse(report['event_dependency_boundary']['prerequisite_quest_inherits_event_origin_or_window'])
        self.assertFalse(report['new_acquisition_attempts'][0]['admitted_as_historical_date_or_release_evidence'])

    def test_current_guide_without_accepted_archive_match_rejected(self):
        objects = copy.deepcopy(self.objects)
        for key in ('adult', 'adult_ci'):
            objects[key]['observations']['temporal_witness']['selected_task_block_matches_current'] = False
        with self.assertRaisesRegex(ValueError, 'exact archived'):
            audit.build(objects, self.pins)

    def test_duplicate_media_cannot_be_relabelled_independent(self):
        objects = copy.deepcopy(self.objects)
        for key in ('adult', 'adult_ci'):
            objects[key]['observations']['lineage']['duplicate_of'] = {}
        with self.assertRaisesRegex(ValueError, 'lineage'):
            audit.build(objects, self.pins)

    def test_unaccepted_ci_payload_rejected(self):
        objects = copy.deepcopy(self.objects)
        objects['adult_ci']['observations']['temporal_witness']['actual_capture'] = '20000101000000'
        with self.assertRaisesRegex(ValueError, 'CI payload differ'):
            audit.build(objects, self.pins)

    def test_event_prerequisite_cannot_be_substituted_with_other_quest(self):
        objects = copy.deepcopy(self.objects)
        objects['xmas']['observations']['christmas']['s1_required_quest'] = '玄黄の洞窟'
        with self.assertRaisesRegex(ValueError, 'prerequisite evidence'):
            audit.build(objects, self.pins)

    def test_same_length_source_byte_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = audit.P+audit.INPUTS['adult'][0]
            p = root/path
            p.parent.mkdir(parents=True)
            raw = (audit.ROOT/path).read_bytes()
            p.write_bytes(b'!'+raw[1:])
            with self.assertRaisesRegex(ValueError, 'Source bytes changed'):
                audit.load_inputs(root)

    def test_false_promotions_and_bbs_date_admission_rejected(self):
        original = audit.build(self.objects, self.pins)
        for mutation in ('base', 'permanent', 'event', 'bbs', 'percentage'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                report = copy.deepcopy(original)
                if mutation == 'base': report['qualification']['origin_class'] = 'BASE_GAME_QUEST'
                if mutation == 'permanent': report['qualification']['permanence_proven'] = True
                if mutation == 'event': report['event_dependency_boundary']['prerequisite_quest_inherits_event_origin_or_window'] = True
                if mutation == 'bbs': report['new_acquisition_attempts'][0]['admitted_as_historical_date_or_release_evidence'] = True
                if mutation == 'percentage': report['boundaries']['overall_restoration_percentage'] = 80
                p = root/audit.REPORT
                p.parent.mkdir(parents=True)
                p.write_text(json.dumps(report))
                with patch.object(audit, 'load_inputs', return_value=(self.objects, self.pins)):
                    with self.assertRaisesRegex(ValueError, 'source-derived replay'):
                        audit.verify(root)


if __name__ == '__main__':
    unittest.main()
