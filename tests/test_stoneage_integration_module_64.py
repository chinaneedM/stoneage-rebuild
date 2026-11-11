"""Public derivative-only tests; original commercial script and original RD files are private."""
import json
import re
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
REPORT = BASE / 'STONEAGE-INTEGRATION64-HOUGYOKU-SIX-ITEMS-ORIGINAL-SOURCE-R1.json'
ITEM = BASE / 'item-module-01' / 'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
QUEST01 = BASE / 'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
MAP09 = BASE / 'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
HEX = re.compile(r'^[0-9a-f]{64}$')


class TestHougyokuOriginalSourceBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.rows = {x[0]: x for x in json.loads(ITEM.read_text(encoding='utf-8'))['rows']}
        cls.q = json.loads(QUEST01.read_text(encoding='utf-8'))
        cls.maps = json.loads(MAP09.read_text(encoding='utf-8'))['maps']

    def test_01_one_source_created_npc_matches_old_quest01_path_and_sha(self):
        s = self.r['source']
        self.assertEqual(s['original_event_script_sha256'], 'fbc23c845a63a4fd126f5f0b8aefd85802210950db5818d2f56ab4588aa22888')
        self.assertEqual(s['original_create_sha256'], 'ed001acc16e29c2efaeb146840a2b563bc0265b64b364bf91ff22900abf5e0d5')
        self.assertEqual((s['source_NPC_floor'], s['source_NPC_borncorner_4_literals'], s['source_NPC_graphic_alias']),
                         (6000, [58, 44, 58, 44], 16047))
        old = [a for a in self.q['source_creation_references'] if a['original_script_path'] == 'extra/event/hougyoku']
        self.assertEqual(len(old), 1)
        self.assertEqual(old[0]['create_source_path'], 'extra/event/hougyoku.create')
        self.assertEqual(old[0]['original_script_sha'], s['original_event_script_sha256'])
        self.assertEqual(old[0]['create_source_sha'], s['original_create_sha256'])
        self.assertEqual(old[0]['origin_class'], 'UNRESOLVED')
        self.assertEqual(old[0]['floorid'], 6000)

    def test_02_four_original_type_blocks_match_old_quest01(self):
        b = self.r['four_original_TYPE_blocks']
        self.assertEqual([a['type'] for a in b], ['ACCEPT', 'REQUEST', 'MESSAGE', 'MESSAGE'])
        self.assertEqual([a['event_number_literal'] for a in b], ['45', '45', '-1', '-1'])
        self.assertEqual([a['source_TYPE_line'] for a in b], [9, 21, 35, 41])
        old = [a for a in self.q['source_event_blocks'] if a['script_path'] == 'extra/event/hougyoku']
        self.assertEqual([a['raw_type'] for a in old], [a['type'] for a in b])
        self.assertEqual([a['source_type_line'] for a in old], [a['source_TYPE_line'] for a in b])
        self.assertTrue(all(HEX.fullmatch(a['normalized_source_section_utf8_sha256']) for a in b))

    def test_03_single_accept_has_five_items_and_one_distinct_reward(self):
        x = {a['op']: a['numeric_literal'] for a in self.r['four_original_TYPE_blocks'][0]['commands']}
        self.assertEqual(x['EVENT'], 'LV>59&ITEM=2764&ITEM=2760&ITEM=2761&ITEM=2762&ITEM=2763')
        self.assertEqual(x['DelItem'], '2764,2760,2761,2762,2763')
        self.assertEqual(x['GetItem'], '2765')
        self.assertEqual(x['EndSetFlg'], '45')
        self.assertEqual(self.r['derived']['unique_source_required_item_ids'], [2764, 2760, 2761, 2762, 2763])
        old = [a for a in self.q['source_event_blocks'] if a['script_path'] == 'extra/event/hougyoku'][0]
        self.assertEqual(old['item_numeric_refs']['DelItem'], [2760, 2761, 2762, 2763, 2764])
        self.assertEqual(old['item_numeric_refs']['GetItem'], [2765])
        self.assertEqual(old['item_numeric_refs']['predicate_ITEM'], [2760, 2761, 2762, 2763, 2764])

    def test_04_request_supply_is_separate_from_accept_redemption(self):
        r = self.r['four_original_TYPE_blocks'][1]
        self.assertEqual({x['op']: x['numeric_literal'] for x in r['commands']}, {'EVENT': 'LV>59', 'GetItem': '2764*1'})
        self.assertTrue(self.r['derived']['source_REQUEST_has_GetItem_2764'])
        self.assertNotEqual(r['type'], self.r['four_original_TYPE_blocks'][0]['type'])

    def test_05_literal_four_warp_destinations_never_imply_execution(self):
        x = {a['op']: a['numeric_literal'] for a in self.r['four_original_TYPE_blocks'][0]['commands']}
        self.assertEqual(x['NpcWarp'], '4000.53.101,2000.44.39,5105.14.3,6000.58.44')
        self.assertEqual(self.r['derived']['npcwarp_literal_four_destinations'], [
            {'floor': 4000, 'x': 53, 'y': 101}, {'floor': 2000, 'x': 44, 'y': 39},
            {'floor': 5105, 'x': 14, 'y': 3}, {'floor': 6000, 'x': 58, 'y': 44}])
        self.assertTrue(self.r['limits']['NpcWarp_command_semantics_random_sequence_and_execution_OPEN'])
        self.assertIn('5105', self.maps)
        self.assertNotIn('6000', self.maps)  # scoped MAP09-691 catalog, NOT original-game absence

    def test_06_original_item_rows_join_existing_item01_shard(self):
        items = self.r['item_source_qualified_six_rows']
        self.assertEqual([a['item_id'] for a in items], list(range(2760, 2766)))
        self.assertEqual([a['source_image_alias'] for a in items], [24059, 24055, 24061, 24057, 24198, 22082])
        self.assertEqual([a['source_price_literal'] for a in items], ['5000'] * 4 + ['0', '50000'])
        self.assertEqual([a['source_type_literal'] for a in items], ['16'] * 5 + ['8'])
        for a in items:
            old = self.rows[a['item_id']]
            self.assertEqual(old[1], old[2])
            self.assertEqual(old[1], a['source_original_cp950_row_sha256'])
            self.assertEqual(old[3], old[4])
            self.assertEqual(old[3], a['source_image_alias'])
            self.assertEqual(old[5:7], [a['source_price_literal'], a['source_type_literal']])
            self.assertEqual(old[8:10], ['REAL_RD_DECODED_CROSS_CARRIER'] * 2)
            self.assertEqual(old[10], [])

    def test_07_six_distinct_original_visual_candidates_but_not_same_deployment(self):
        images = [x['tw1_retail_original_RD_candidate'] for x in self.r['item_source_qualified_six_rows']]
        self.assertEqual(len({x['physical_bitmap_number'] for x in images}), 6)
        self.assertEqual(len({x['png_sha256'] for x in images}), 6)
        for x in images:
            self.assertTrue(HEX.fullmatch(x['source_original_RD_sha256']))
            self.assertTrue(HEX.fullmatch(x['png_sha256']))
            self.assertTrue(all(isinstance(n, int) and n > 0 for n in x['size']))
            self.assertEqual(x['source_qualification'], 'TW1_RETAIL_CROSS_CARRIER_VISUAL_CANDIDATE_NOT_SAME_OFFICIAL_DEPLOYMENT')
        self.assertTrue(self.r['limits']['original_official_same_deployment_TW1_and_mixed25_OPEN'])

    def test_08_archival_safety_and_stage_boundaries(self):
        s = self.r['source']
        self.assertEqual((s['NPC_zip_members_verified'], s['ITEM_zip_members_verified']), (2205, 838))
        self.assertTrue(HEX.fullmatch(s['source_NPC_private_archive_sha256']))
        self.assertTrue(HEX.fullmatch(s['source_item_private_archive_sha256']))
        self.assertEqual(self.r['limits']['original_event_origin'], 'ORIGIN_UNRESOLVED')
        self.assertEqual(self.r['limits']['stage_A'], '7_PARTIAL_2_OPEN')
        self.assertEqual(self.r['limits']['stage_B'], 'GATED')
        self.assertIsNone(self.r['limits']['overall_percent'])


if __name__ == '__main__':
    unittest.main()
