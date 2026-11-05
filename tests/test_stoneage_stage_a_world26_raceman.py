"""Source/compiled mismatch and version boundaries; CI contains no private EXE."""
import json
from pathlib import Path
import unittest

from tools.stoneage_raceman_source_boundary import compiled_lookup, ascii_function_names

R = Path(__file__).resolve().parents[1] / 'research/recovered'


class RacemanBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads((R / 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-26-RACEMAN-SOURCE-BOUNDARY-R1.json').read_text())

    def test_lookup_domain_and_case_insensitive_exact_name(self):
        b = self.d['compiled_server']
        self.assertEqual((b['lookup_count'], b['record_stride'], b['last_inclusive_index']), (60, 68, 59))
        rows = b['lookup_names']
        self.assertEqual([r[0] for r in rows], list(range(60)))
        names = [r[2].lower() for r in rows]
        self.assertEqual(len(set(names)), 60)
        self.assertNotIn('raceman', names)
        self.assertEqual(b['Raceman_case_insensitive_table_matches'], [])
        self.assertEqual(b['Raceman_case_insensitive_whole_image_substring_count'], 0)
        self.assertEqual(b['static_failed_lookup_return'], -1)
        self.assertEqual(b['comparison_call']['target_va'], 0x55b040)

    def test_other_race_names_do_not_fill_missing_handler(self):
        rows = self.d['compiled_server']['lookup_names']
        self.assertEqual([rows[i][2] for i in (56, 57)], ['PetRaceMaster', 'PetRacePet'])
        self.assertEqual(self.d['different_registered_functions_not_substitutes'], ['PetRaceMaster', 'PetRacePet'])
        self.assertEqual(self.d['conclusion'], 'RACEMAN_HANDLER_NOT_IN_THIS_COMPILED_NAME_LOOKUP_GETITEM_ROLE_OPEN')

    def test_original_source_paths_and_physical_line_hashes_match_old_index(self):
        d = self.d
        old = json.loads((R / 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json').read_text())
        source, = [f for f in old['files'] if any('Raceman' in r[8] for r in f[4])]
        self.assertEqual(d['exact_original_CREATE_refs'], source[4])
        self.assertEqual(d['source_parameter_path'], source[0])
        op, = source[6]
        fields = {f['key']: f for f in d['source_item_fields']}
        f = fields['GetItem']
        self.assertEqual([f['line'], f['key'], f['raw_literal'], f['line_sha256']], op[:4])
        self.assertEqual((fields['CheckItem']['raw_literal'], f['raw_literal']), ('20760', '20760'))
        self.assertEqual(source[4][0][3:6], [3206, 16171, [15, 19, 15, 19]])

    def test_prior_event_identity_preserved_not_rediscovered(self):
        old = json.loads((R / 'STONEAGE-O88-FAMILY-PET-HUNT-DATED-EVENT-R1.json').read_text())
        expected = {r['path'].removeprefix('gmsv/data/npc/'): r for r in old['source']['members'] if r['path'].startswith('gmsv/data/npc/')}
        self.assertEqual(len(self.d['original_three_source_files']), 3)
        for r in self.d['original_three_source_files']:
            e = expected[r['path']]
            self.assertEqual((r['bytes'], r['sha256'], r['crc32']), (e['bytes'], e['sha256'], e['extracted_crc32']))
        self.assertIn('ALREADY_RECORDED', self.d['event_classification'])

    def test_item_missing_in_A_present_in_B_is_not_global_absence(self):
        row = self.d['item01_source_join']
        old = {r[0]: r for p in (R / 'item-module-01').glob('*.json') for r in json.loads(p.read_text())['rows']}
        self.assertEqual(row, old[20760])
        self.assertIsNone(row[1])
        self.assertRegex(row[2], r'^[0-9a-f]{64}$')
        self.assertFalse(self.d['limits']['all_versions_missing_20760'])

    def test_wrong_image_and_unterminated_or_non_ascii_name_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'complete original'):
            compiled_lookup(b'MZ')
        for name in (b'a' * 128, b'\x80\0', b'\0'):
            data = b'\x04\0\0\0' + name
            with self.subTest(name=name[:8]):
                with self.assertRaises(ValueError):
                    ascii_function_names(lambda a, n: data[a:a+n], 0, 1, 4)

    def test_no_original_execution_or_semantics_invented(self):
        self.assertFalse(self.d['compiled_server']['original_program_executed'])
        self.assertTrue(self.d['WORLD23_raw_numeric_index_preserved'])
        self.assertTrue(self.d['all_2205_NPC_members_SHA_size_CRC_reverified'])
        self.assertTrue(all(v is False for k, v in self.d['limits'].items() if k != 'overall_percent'))
        self.assertIsNone(self.d['limits']['overall_percent'])
        self.assertIn('leave compiled item-field helper chain', self.d['next'])


if __name__ == '__main__':
    unittest.main()
