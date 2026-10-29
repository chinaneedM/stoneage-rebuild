"""Adversarial evidence-coverage regressions; public CI contains no original assets."""
import copy
import json
import unittest
from unittest.mock import patch
from tools import stoneage_scene30_tw10_fieldmap_boundary as m


class FieldmapEvidenceTest(unittest.TestCase):
    def altered_source(self, filename, before, after, error):
        source = m.inputs()
        self.assertIn(before, source[filename])
        source[filename] = source[filename].replace(before, after, 1)
        with patch.object(m, 'inputs', return_value=source):
            with self.assertRaisesRegex(ValueError, error):
                m.derive()

    def test_published_report_exact_replay(self):
        self.assertEqual(json.loads(m.OUT.read_text()), m.derive())

    def test_savedata_is_not_world_map(self):
        r = m.derive()
        self.assertEqual(r['retail']['only_core_dat'], ['StoneAge/data/savedata.dat'])
        self.assertEqual(r['retail']['battle_sab_files'], 218)
        self.assertIs(r['overall_percent'], None)

    def test_numeric_dat_outside_map_directory_is_not_missed(self):
        self.altered_source('STONEAGE-TW10-CLIENT-INVENTORY-R1.txt',
            'path=StoneAge/waei.bmp', 'path=StoneAge/1000.dat', 'unexpected retail DAT')

    def test_directory_case_does_not_hide_world_file(self):
        self.altered_source('STONEAGE-TW10-CLIENT-INVENTORY-R1.txt',
            'path=StoneAge/waei.bmp', 'path=StoneAge/MAP/1000.bin', 'field-map directory')

    def test_incomplete_inventory_is_not_negative_evidence(self):
        self.altered_source('STONEAGE-TW10-CLIENT-INVENTORY-R1.txt',
            'CORE_FILE|category=branding_ui_shell|path=StoneAge/waei.bmp',
            'REMOVED|category=branding_ui_shell|path=StoneAge/waei.bmp', 'complete unique retail')

    def test_failed_unshield_does_not_prove_absence(self):
        self.altered_source('STONEAGE-TW10-INSTALLSHIELD-R1.txt',
            'UNSHIELD|list_rc=0|extract_rc=0', 'UNSHIELD|list_rc=0|extract_rc=1',
            'extraction must have succeeded')

    def test_extracted_map_cannot_be_discarded_as_support(self):
        self.altered_source('STONEAGE-TW10-INSTALLSHIELD-R1.txt',
            'map_like=0', 'map_like=1', 'installer map')

    def test_same_cab_name_different_content_is_rejected(self):
        self.altered_source('STONEAGE-TW10-INSTALLSHIELD-R1.txt',
            'sha256=4fa32c9b', 'sha256=0fa32c9b', 'provenance differ')

    def test_lost_callback_branch_cannot_prove_delivery(self):
        self.altered_source('STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt',
            'MAP_SEMANTIC_MODE|name=M|node_rva=0x1da40|instruction_rva=0x1da81|mode=wb',
            'MAP_SEMANTIC_MODE|name=M|node_rva=0x1da40|instruction_rva=0x1da81|mode=rb',
            'update/read distinction')

    def test_review_does_not_claim_new_execution(self):
        r = m.derive()
        self.assertIs(r['installer']['new_installer_execution'], False)
        self.assertIs(r['installer']['script_dynamic_behavior_fully_proven'], False)
        self.assertIs(r['map_delivery']['live_server_payload_obtained'], False)
        self.assertIs(r['original_world_entered'], False)
        self.assertIs(r['later_mixed25_map_is_tw10_official_world'], False)
        self.assertEqual(r['new_historical_map_payloads'], 0)


if __name__ == '__main__':
    unittest.main()
