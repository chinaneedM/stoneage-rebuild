import json
import unittest

from tools.stoneage_cooking_source import FALSE, O75, REPORT, SOURCE_SCOPE, compiled, sha, source_rows


class World30CookingSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.prior = json.loads(O75.read_text(encoding='utf-8'))

    def test_frozen_report_and_scope(self):
        self.assertEqual(sha(REPORT.read_bytes()), '0312f4f1f60c88c775a5a4cdd4d6d56a46cb83d099bc1e606a9eacab3cf7f4d5')
        self.assertEqual(self.report['source_scope'], SOURCE_SCOPE)
        self.assertTrue(all(self.report[key] is False for key in FALSE))

    def test_original_archive_and_configuration(self):
        witness = self.report['archive_witness']
        self.assertEqual(witness['all_file_headers_scanned'], 7952)
        self.assertTrue(witness['all_header_CRCs_verified'])
        self.assertTrue(witness['selected_member_CRCs_verified'])
        self.assertTrue(witness['header_parser_is_not_second_decompressor'])
        members = {row['target']: row for row in witness['members']}
        self.assertEqual(len(members), 8)
        for path, old in self.prior['actual_extracted_source_files'].items():
            key = 'gmsv/data/' + path
            if key in members:
                self.assertEqual(members[key]['member_sha256'], old['sha256'])
                self.assertEqual(members[key]['member_crc32'], int(old['rar_crc32'], 16))
        paths = self.report['configured_paths']
        self.assertEqual(paths, {'itemset6file': 'data/itemset.txt', 'petskillfile2': './data/petskill.txt',
                                 'itematomfile': './data/itematom.txt'})
        for path in paths.values():
            self.assertIn('gmsv/' + path.removeprefix('./'), members)
        self.assertEqual(set(paths), set(self.report['compiled']['config_bindings']))

    def test_shared_compiled_callback_and_dataflow(self):
        program = self.report['compiled']
        self.assertEqual([(s['id'], s['kind'], s['callback']) for s in self.report['pet_skill_rows']],
                         [(200, 'PETSKILL_MERGE', 'PETSKILL_Merge'),
                          (201, 'PETSKILL_MERGE2', 'PETSKILL_Merge')])
        self.assertEqual(program['registration']['callback'], program['symbols']['_PETSKILL_Merge'])
        self.assertEqual(program['search_table_min_max'], [[0.8, 1.2], [0.7, 1.3]])
        calls = {call['address']: call['symbol'] for call in program['calls']}
        self.assertEqual([calls[address] for address in (0x553c15, 0x511e8f, 0x5107dd, 0x511f2e, 0x51210f)],
                         ['_ITEM_mergeItem_merge', '_ITEM_mergeItem', '_random', '__CHAR_setItemIndex',
                          '_ITEM_makeItemAndRegist'])

    def test_three_dishes_and_bounded_raw_ingredient_rows(self):
        dishes = {d['id']: d for d in self.report['chef_dishes']}
        old = {d['item_id']: d for d in self.prior['chef_menu_to_itemset'] if d['exact_unique_itemset_name']}
        self.assertEqual(set(dishes), set(old))
        self.assertEqual(len(dishes), 3)
        self.assertEqual((self.report['item_physical_rows'], self.report['atom_dictionary_rows']), (13254, 83))
        candidate_ids = set()
        for item_id, dish in dishes.items():
            self.assertEqual(dish['line'], old[item_id]['itemset_zero_based_line'] + 1)
            self.assertEqual(dish['o75_row_sha256_without_line_ending'], old[item_id]['full_source_row_sha256'])
            self.assertEqual((dish['type'], dish['input_flag'], dish['output_flag']), (20, 0, 1))
            self.assertEqual([slot['target_value'] for slot in dish['atom_slots']], old[item_id]['atom_values'])
            for slot in dish['atom_slots']:
                self.assertIn(slot['atom_dictionary_line'], range(1, 84))
                values = {row['value'] for row in slot['single_atom_input_rows']}
                self.assertEqual(values, {10, 26, 69, 122})
                candidate_ids.update(row['id'] for row in slot['single_atom_input_rows'])
        self.assertEqual(len(candidate_ids), 36)
        self.assertTrue(candidate_ids.isdisjoint(dishes))

    def test_incomplete_program_and_malformed_row_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'complete original compiled GMSV'):
            compiled(b'MZ')
        with self.assertRaisesRegex(ValueError, 'Unexpected source width'):
            list(source_rows(b'one,two\n', 3))


if __name__ == '__main__':
    unittest.main()
