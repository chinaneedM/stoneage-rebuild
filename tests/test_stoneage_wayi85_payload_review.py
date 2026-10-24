import copy
import json
import unittest
from collections import Counter
from tools.stoneage_wayi85_payload_review import ROOT, RAW, analyze, validate


class Wayi85PayloadReviewTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT/RAW).read_bytes())

    def test_full_file_table_join_and_replay(self):
        self.assertEqual(validate()['file_count'], 557)

    def test_outer_wrapper_success_not_payload_success(self):
        self.report['status'] = 'BYTE_ACQUISITION_AND_STATIC_INSPECTION_COMPLETE'
        with self.assertRaises(ValueError):
            analyze(self.report)

    def test_missing_extracted_file_rejected(self):
        self.report['inspection']['inventory']['samples'][0]['files'].pop()
        with self.assertRaises(ValueError):
            analyze(self.report)

    def test_msi_destination_size_mismatch_rejected(self):
        i = self.report['inspection']
        i['msi_tables']['File'] = i['msi_tables']['File'].replace('sa.exe\t371200', 'sa.exe\t371201', 1)
        with self.assertRaises(ValueError):
            analyze(self.report)

    def test_directory_cycle_rejected(self):
        i = self.report['inspection']
        i['msi_tables']['Directory'] = i['msi_tables']['Directory'].replace('DATA\tINSTALLDIR\tdata', 'DATA\tDATA\tdata')
        with self.assertRaises(ValueError):
            analyze(self.report)

    def test_auxiliary_bgm_files_not_counted_as_numeric_maps(self):
        result = analyze(self.report)
        self.assertEqual(len(result['numeric_map_dat_candidates']), 42)
        self.assertEqual({x['path'] for x in result['map_directory_auxiliary_dat_files']},
                         {'map/bgm0.dat', 'map/bgm1.dat', 'map/bgm2.dat'})
        self.assertFalse(result['boundaries']['full_world_map_coverage_proven'])

    def test_server_and_publisher_promotions_rejected(self):
        for field in ('official_clean_client_authenticated', 'server_quest_pet_data_inferred', 'original_payload_published'):
            with self.subTest(field=field):
                r = copy.deepcopy(self.report)
                r[field] = True
                with self.assertRaises(ValueError):
                    analyze(r)

    def test_map_byte_differences_not_merged_by_filename(self):
        result = analyze(self.report)
        self.assertEqual(Counter(x['status'] for x in result['numeric_map_same_path_comparison_with_mixed25']),
                         {'EXACT_SAME_PATH_BYTES': 1, 'DIFFERENT_SAME_PATH_BYTES': 34, 'ABSENT_FROM_BRIDGE_PATH': 7})
        self.assertFalse(result['boundaries']['byte_change_proves_world_geometry_or_patch_change'])
