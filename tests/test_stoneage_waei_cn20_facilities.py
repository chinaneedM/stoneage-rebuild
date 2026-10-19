from copy import deepcopy
import json
import unittest
from tools import stoneage_waei_cn20_facilities as m


class FacilityArticleTests(unittest.TestCase):
    def setUp(self):self.report=json.loads(m.REPORT.read_bytes())
    def reject(self, change):
        o=deepcopy(self.report);change(o)
        with self.assertRaises((ValueError,AssertionError)):m.validate_report(o)
    def test_actual_fourteen_source_categories(self):
        m.validate_report(self.report)
        self.assertEqual(self.report['records'][6]['name_as_written'],'便利商店')
    def test_no_missing_or_extra_service_row(self):
        self.reject(lambda o:o['records'].pop())
        self.reject(lambda o:o['records'].append(deepcopy(o['records'][-1])))
    def test_no_invented_npc_identity(self):
        self.reject(lambda o:o['records'][1].update(original_npc_ids_or_names=['护士001']))
    def test_no_server_location_or_script(self):
        self.reject(lambda o:o['records'][0].update(map_coordinates_or_server_script=[100,100]))
    def test_no_price_or_reward_formula(self):
        self.reject(lambda o:o['records'][11].update(prices_formulas_or_quest_rewards={'rate':0.1}))
    def test_threshold_not_silently_made_inclusive(self):
        self.reject(lambda o:o['records'][1]['source_qualified_paraphrases'].__setitem__(2,'免费护理含10级。'))
    def test_morning_parenthetical_not_silently_repaired(self):
        self.reject(lambda o:o['records'][11]['source_qualified_paraphrases'].__setitem__(1,'快递日出后营业。'))
    def test_no_actual_pixel_dimension_or_format(self):
        self.reject(lambda o:o['records'][0]['image_reference'].update(actual_dimensions_format_or_capture={'JPEG':[130,98]}))
    def test_no_category_to_npc_or_global_village_promotion(self):
        self.reject(lambda o:o['boundaries'].update(every_village_has_every_facility=True))
        self.reject(lambda o:o['coverage'].update(new_named_npc_instances=14))
    def test_preserve_image_bindings_and_case(self):
        self.reject(lambda o:o['records'][0]['image_reference'].update(relative_src_as_written='img/image002.jpg'))
    def test_preserve_actual_source_capture_and_paragraph_digest(self):
        self.reject(lambda o:o['source'].update(actual_capture='20011023173210'))
        self.reject(lambda o:o['records'][0].update(service_text_sha256='0'*64))
    def test_no_cross_build_or_production_adoption(self):
        self.reject(lambda o:o['boundaries'].update(same_tw10_jss_cn182_or_later_build=True))
        self.reject(lambda o:o['boundaries'].update(automatic_new_game_adoption=True))
    def test_exact_known_entry_required(self):
        with self.assertRaises((ValueError,AssertionError)):m.build(b'',m.ENTRY['strict_replay_url'],b'',m.URL)


if __name__=='__main__':unittest.main()
