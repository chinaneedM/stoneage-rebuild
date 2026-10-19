"""One exact named web image cannot certify client species or animation data."""
import json
from pathlib import Path
import unittest
from tools.stoneage_waei_cn20_amiduo_visual import REPORT,PARENT,URL,build,validate_report


class AmiduoVisualTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def test_actual_name_and_web_position_not_neighbor_species(self):
        o=self.report();o['records'][0]['source_name_as_written']='艾尔蛙'
        with self.assertRaisesRegex(ValueError,'named source position'):validate_report(o)
        o=self.report();o['records'][0]['source_position']['ordinal']=7+1
        with self.assertRaisesRegex(ValueError,'source position'):validate_report(o)

    def test_page_and_next_day_image_not_same_capture_or_backfilled_html_size(self):
        o=self.report();o['records'][0]['html_declared_dimensions_for_this_position']=[83,90]
        with self.assertRaisesRegex(ValueError,'projected back'):validate_report(o)
        o=self.report();o['records'][0]['image_and_page_are_proven_same_instant_or_build']=True
        with self.assertRaisesRegex(ValueError,'capture projected'):validate_report(o)

    def test_actual_jpeg_dimensions_and_hash_not_filename_claim(self):
        o=self.report();o['records'][0]['acquired_image']['dimensions']=[240,180]
        with self.assertRaisesRegex(ValueError,'image metadata'):validate_report(o)
        o=self.report();o['records'][0]['acquired_image']['format']='GIF'
        with self.assertRaisesRegex(ValueError,'image metadata'):validate_report(o)

    def test_visual_inspection_exact_hash_not_independent_runner_claim(self):
        o=self.report();o['records'][0]['manual_inspection']['exact_image_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Visual inspection'):validate_report(o)
        o=self.report();o['records'][0]['manual_inspection']['independent_runner_repeats_human_visual_inspection']=True
        with self.assertRaisesRegex(ValueError,'attributed to CI'):validate_report(o)

    def test_static_web_file_not_client_animation_model_alias_or_pet_id(self):
        for key,value in [('client_sprite_animation_model_or_native_palette_verified',True),
                          ('static_jpeg_means_pet_has_no_animation',True),
                          ('original_game_pet_id_stats_or_cross_region_alias',{'pet_id':7})]:
            o=self.report();o['records'][0][key]=value
            with self.assertRaisesRegex(ValueError,'Web illustration'):validate_report(o)

    def test_single_image_not_all_forty_or_rewritten_parent(self):
        o=self.report();o['coverage']['other_first_page_image_refs_unacquired']=0
        with self.assertRaisesRegex(ValueError,'broader recovery'):validate_report(o)
        o=self.report();o['coverage']['prior_report_historical_unacquired_state_rewritten']=True
        with self.assertRaisesRegex(ValueError,'historical rewrite'):validate_report(o)

    def test_wrong_parent_error_body_and_other_capture_rejected(self):
        for parent,final in [(b'{}',URL),(PARENT.read_bytes(),URL),(PARENT.read_bytes(),URL.replace('20011205051046','20011204194619'))]:
            with self.assertRaises(ValueError):build(parent,b'x'*4831,final)

    def test_archive_contract_and_existing_position_remains_unacquired_in_parent(self):
        o=self.report();validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        self.assertLessEqual(set(required),o['records'][0].keys())
        parent=json.loads(PARENT.read_bytes());self.assertEqual(parent['coverage']['unacquired_image_references'],40)
        self.assertIsNone(parent['records'][6]['image_reference']['actual_capture'])
        self.assertEqual(o['coverage']['new_game_pet_entities'],0)


if __name__=='__main__':unittest.main()
