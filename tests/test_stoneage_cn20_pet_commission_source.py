"""Parser behavior and evidence boundaries, using independent synthetic fragments."""
import unittest
from tools.stoneage_cn20_pet_commission_source import between, parse_block, visible, catalog


SAMPLE = ('渔村宠物委托书A：甲、甲乙各2只成本：3S报酬：?宠物出没地点：'
          '甲乙：地下二楼（东9,南8）甲：村口（东1,南2）（东3,南4）')


class PetCommissionParserTests(unittest.TestCase):
    def test_prefix_names_do_not_cross_bind_when_habitat_order_differs(self):
        row = parse_block(SAMPLE, 'SYNTHETIC')
        self.assertEqual([t['species_label'] for t in row['targets']], ['甲', '甲乙'])
        self.assertEqual([h['species_label'] for h in row['habitats_in_source_order']], ['甲乙', '甲'])
        self.assertEqual(row['habitats_in_source_order'][0]['location_text'], '地下二楼（东9,南8）')

    def test_two_coordinates_do_not_become_spawn_rectangle_or_level(self):
        habitat = parse_block(SAMPLE, 'SYNTHETIC')['habitats_in_source_order'][1]
        self.assertEqual(habitat['coordinate_pairs_in_source_order'], [[1, 2], [3, 4]])
        self.assertIsNone(habitat['map_id'])
        self.assertIsNone(habitat['spawn_level'])
        self.assertIsNone(habitat['spawn_weight'])
        self.assertFalse(habitat['coordinate_frame_verified'])

    def test_unknown_reward_is_not_extrapolated_from_cost(self):
        row = parse_block(SAMPLE, 'SYNTHETIC')
        self.assertEqual(row['listed_cost_S'], 3)
        self.assertIsNone(row['listed_reward_S'])
        self.assertIsNone(row['net_profit_S'])
        self.assertIsNone(row['deposit_refund'])

    def test_duplicate_or_missing_habitat_fails_closed(self):
        for sample in [SAMPLE.replace('甲乙：地下二楼', '甲：地下二楼'),
                       SAMPLE.split('甲：村口')[0]]:
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                parse_block(sample, 'SYNTHETIC')

    def test_duplicate_target_and_zero_quantity_are_rejected(self):
        for sample in [SAMPLE.replace('甲、甲乙', '甲、甲'), SAMPLE.replace('各2只', '各0只')]:
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                parse_block(sample, 'SYNTHETIC')

    def test_html_hidden_text_does_not_create_habitat_or_link(self):
        text, links = visible('<script>假地点<a href="wrong">wrong</a></script>'
                              '<style>假坐标</style><!--假宠物--><p>真地点&amp;名<a href="ok">页</a>')
        self.assertEqual(text, '真地点&名页')
        self.assertEqual(links, ['ok'])

    def test_duplicate_or_reversed_article_markers_are_rejected(self):
        for source in ['BEGINxBEGINyEND', 'ENDxBEGIN', 'no markers']:
            with self.subTest(source=source), self.assertRaises(ValueError):
                between(source, 'BEGIN', 'END')

    def test_numeric_reward_preserves_listed_value_without_payment_claim(self):
        row = parse_block(SAMPLE.replace('报酬：?', '报酬：123S'), 'SYNTHETIC')
        self.assertEqual(row['listed_reward_S'], 123)
        self.assertFalse(row['actual_handover_or_payment_verified'])

    def test_catalog_requires_source_rights_and_version_contract(self):
        archive = {'future_website': {'required_collections': ['quests', 'encounters'],
                    'record_contract': {'required': ['source_refs', 'rights_status', 'verification_status']}}}
        with self.assertRaises(ValueError):
            catalog({'commissions': [parse_block(SAMPLE, 'SYNTHETIC')]}, archive)

    def test_catalog_links_location_to_quest_without_promoting_game_ids(self):
        archive = {'future_website': {'required_collections': ['quests', 'encounters'],
                    'record_contract': {'required': ['source_refs', 'rights_status', 'verification_status', 'version_profile']}}}
        out = catalog({'commissions': [parse_block(SAMPLE, 'SYNTHETIC')]}, archive)
        quest, first, second = out['records']
        self.assertEqual(first['source_relation']['quest_record'], quest['record_id'])
        self.assertEqual(second['source_relation']['quest_record'], quest['record_id'])
        self.assertEqual(len({r['record_id'] for r in out['records']}), 3)
        self.assertTrue(all(r['game_ids'] is None and r['rights_status'] != 'RELEASE_APPROVED' for r in out['records']))
        self.assertFalse(out['public_release_approved'])


if __name__ == '__main__':
    unittest.main()
