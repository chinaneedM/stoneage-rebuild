"""Reject deployed-rule, species, numeric and time claims absent from the operator plan."""
import json
from pathlib import Path
import unittest
from tools.stoneage_wayi_newbie_riding_plan import INDEX_URL, URL, REPORT, build, index_rows, validate_report


class NewbieRidingPlanTests(unittest.TestCase):
    def reject(self, i, key, value, message):
        o=json.loads(REPORT.read_text());o['records'][i]['source_described_claims'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_planned_gift_not_implemented_reward_or_numeric_growth(self):
        self.reject(2,'status','DEPLOYED_SERVER_RULE','Planned gift')
        self.reject(2,'stat_loyalty_deltas_or_compatibility_matrix',{'loyalty_gain':10},'numeric reward')

    def test_thirty_level_increase_not_destination_30_or_caption_60(self):
        self.reject(4,'destination_level_is_30_proven',True,'Thirty-level')
        self.reject(4,'source_claimed_level_increase',60,'Thirty-level')
        self.reject(4,'caption_one_sexagenary_cycle_is_60_level_reward',True,'metaphor')

    def test_relative_pet_color_labels_not_original_species_probability_or_location(self):
        self.reject(1,'species_ids_capture_rates_or_maps',{'黃虎':1},'original roster')
        self.reject(1,'tiger_relative_acquisition_ease_as_written',[['金虎'],['紅虎'],['黃虎','綠虎']],'Relative labels')

    def test_after_rite_plan_not_imported_player_guide_level_or_quest_id(self):
        self.reject(3,'required_level_npc_or_quest_ids',{'level':30},'invented level')

    def test_index_title_date_bound_in_same_row_without_neighbor_date(self):
        rows=''.join('<tr><td><a href="producer02.asp?idno='+str(i)+'">synthetic title</a></td><td>2003-12-10</td></tr>' for i in range(15))
        self.assertEqual(index_rows('<table>'+rows+'</table>')[0]['index_date_as_written'],'2003-12-10')
        for bad in [rows.replace('<td>2003-12-10</td>','<td></td>',1),rows.replace('<td>2003-12-10</td>','<td>2003-12-10 2004-1-1</td>',1)]:
            with self.assertRaises(ValueError):index_rows(bad)

    def test_2003_index_date_not_capture_or_verified_deployment(self):
        o=json.loads(REPORT.read_text());o['source']['index_date_is_original_body_release_or_deployment_proven']=True
        with self.assertRaisesRegex(ValueError,'2003 index date'):validate_report(o)

    def test_original_body_capture_and_error_page_rejected(self):
        for index_url,body_url in [(INDEX_URL,URL),(INDEX_URL,URL.replace('20051117143741','20031210000000')),
                                   (INDEX_URL.replace('wayi.com.tw','example.org'),URL)]:
            with self.assertRaises(ValueError):build(b'i'*28883,index_url,b'b'*19964,body_url)

    def test_required_record_fields_source_scopes_and_qualified_unread_successor(self):
        o=json.loads(REPORT.read_text());validate_report(o)
        c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(c),r.keys());self.assertEqual(r['collection'],'tutorials')
            self.assertEqual(r['source_refs'][0]['actual_capture'],'20051117143741')
            self.assertIsNone(r['original_game_ids_or_same_build_binding'])
        self.assertFalse(o['qualified_successor']['body_or_images_read'])
        o['records'][0]['actual_server_rule_or_execution_verified']=True
        with self.assertRaisesRegex(ValueError,'server rule'):validate_report(o)


if __name__=='__main__':unittest.main()
