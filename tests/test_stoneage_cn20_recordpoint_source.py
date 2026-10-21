import copy
import json
import unittest
from tools import stoneage_cn20_recordpoint_source as m


class RecordPointSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(m.REPORT.read_text())
        cls.local = json.loads((m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r); node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            m.validate(r)

    def test_capture_dates_not_publication_build_or_named_author(self):
        m.validate(self.r)
        self.assertEqual([x['capture_timestamp'] for x in self.r['sources']], ['20011204194619', '20011204000349', '20011204220248', '20011204213609'])
        self.assertEqual(self.r['extracted']['authorship'], 'OPERATOR_HOSTED_GUIDE_AUTHOR_UNVERIFIED')
        self.reject(['sources', 1, 'publication_date'], '2001-12-04')
        self.reject(['sources', 2, 'exact_client_build'], '1.82')

    def test_seventeen_rows_in_three_original_island_tables(self):
        rows = self.r['extracted']['rows']
        self.assertEqual([sum(x['island_label'] == k for x in rows) for k in ['北岛', '南岛', '吉鲁岛']], [7, 8, 2])
        self.assertEqual(rows[0]['place_as_written'], '萨姆吉尔村')
        self.assertEqual(rows[-1]['meat_cell_as_written'], '扬奇洛斯X1')
        self.reject(['extracted', 'rows', 0, 'meat_cell_as_written'], '凯比特X2')
        self.reject(['records', 3, 'version_profile'], 'TW10')
        self.reject(['records', 3, 'game_ids'], [1000])

    def test_duplicate_coordinates_are_preserved_without_location_merge(self):
        rows = {x['place_as_written']: x for x in self.r['extracted']['rows']}
        self.assertEqual(rows['加加村']['coordinate_cell_as_written'], rows['塔姆塔姆村']['coordinate_cell_as_written'])
        self.assertNotEqual(rows['加加村']['meat_cell_as_written'], rows['塔姆塔姆村']['meat_cell_as_written'])
        self.reject(['extracted', 'rows', 12, 'coordinate_cell_as_written'], '500，500')

    def test_space_separated_coordinates_and_unknown_meat_remain_source_text(self):
        rows = {x['place_as_written']: x for x in self.r['extracted']['rows']}
        self.assertEqual(rows['阿布洞窟前']['coordinate_cell_as_written'], '191 365')
        self.assertEqual(rows['柯尔克通路附近']['coordinate_cell_as_written'], '342 466')
        self.assertEqual(rows['奇喀喀村']['meat_cell_as_written'], '不详')
        self.reject(['extracted', 'rows', 11, 'meat_cell_as_written'], '乌力X1')

    def test_multiple_pairs_and_meats_do_not_become_npc_positions_or_and_or(self):
        for row in self.r['extracted']['rows']:
            self.assertIsNone(row['multiple_coordinate_meaning'])
            self.assertIsNone(row['multi_meat_operator'])
            self.assertFalse(row['coordinates_are_verified_npc_positions'])
        self.reject(['extracted', 'rows', 5, 'multi_meat_operator'], 'AND')
        self.reject(['extracted', 'rows', 0, 'coordinates_are_verified_npc_positions'], True)

    def test_ordinary_and_in_place_logout_destinations_keep_original_labels(self):
        self.assertEqual(self.r['extracted']['logout']['in_place_label_as_written'], '原地登出')
        self.assertEqual(self.r['extracted']['recordpoint']['in_place_label_as_written'], '原地注销')
        self.assertEqual(self.r['extracted']['recordpoint']['ordinary_logout_reentry'], 'LAST_RECORD_POINT')
        self.reject(['extracted', 'logout', 'in_place_reentry'], 'LAST_RECORD_POINT')
        self.reject(['extracted', 'recordpoint', 'original_save_storage'], 'data/savedata.dat')

    def test_meat_tribute_and_population_are_not_bank_or_server_transaction(self):
        self.assertTrue(self.r['extracted']['recordpoint']['requires_place_specific_meat_tribute'])
        self.reject(['extracted', 'recordpoint', 'consume_or_check_only'], 'CONSUME')
        self.reject(['extracted', 'recordpoint', 'count_scope_refresh_or_protocol'], 'ALL_SERVERS_LIVE')
        self.reject(['extracted', 'recordpoint', 'knocked_away_destination'], 'LOGOUT_LOCATION')

    def test_trade_yes_is_only_receiving_permission_not_complete_exchange(self):
        self.assertEqual(self.r['extracted']['trade']['recipient_permission_as_written'], 'YES')
        self.reject(['extracted', 'trade', 'full_exchange_confirmation_or_atomicity'], 'BOTH_OK')
        self.reject(['records', 1, 'runtime_verified'], True)

    def test_declared_picture_404_is_not_recovered_image_or_global_absence(self):
        self.assertEqual(self.r['image_reference']['path_as_written'], 'img/image011.jpg')
        self.reject(['image_reference', 'image_bytes_obtained'], True)
        self.reject(['image_reference', 'all_archives_missing_proven'], True)
        self.reject(['image_reference', 'capture_timestamp_verified'], '20011204213609')

    def test_twenty_real_mutations_and_outer_positive(self):
        audit = self.local['audit']; cases = audit['real_source_mutations']
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 20)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(audit['outer_script_positive'])
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_BANK_OR_SAVEDATA_HELPERS')


if __name__ == '__main__':
    unittest.main()
