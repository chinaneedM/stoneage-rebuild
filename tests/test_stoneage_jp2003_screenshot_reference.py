"""Bind screenshot evidence to actual pixels/captures without inventing client identity."""
import json
from pathlib import Path
import unittest
from tools.stoneage_jp2003_screenshot_reference import IMAGE_ROOT, IMAGE_URL, REPORT, URL, build, extract_refs, validate_report


class ScreenshotReferenceTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def test_later_2008_image_not_2003_same_instant(self):
        o=self.report();o['records'][0]['actual_image']['same_instant_or_same_bytes_as_2003_page_proven']=True
        with self.assertRaisesRegex(ValueError,'same-time'):validate_report(o)

    def test_web_dimensions_not_native_client_resolution_or_uncropped_frame(self):
        o=self.report();o['records'][0]['actual_image']['native_client_resolution_or_uncropped_frame']=[275,200]
        with self.assertRaisesRegex(ValueError,'native resolution'):validate_report(o)

    def test_observed_status_overlay_not_login_creation_or_numeric_rules(self):
        for key,value in [('login_or_character_creation_screen_proven',True),
                           ('original_map_character_species_ids_or_stat_values',{'floor_id':100})]:
            o=self.report();o['records'][0]['visual_review'][key]=value
            with self.assertRaisesRegex(ValueError,'other UI state'):validate_report(o)

    def test_remaining_seven_refs_not_acquired_or_visually_inspected(self):
        for key in ['actual_image','visual_review']:
            o=self.report();o['records'][1][key]=o['records'][0][key]
            with self.assertRaisesRegex(ValueError,'Unacquired'):validate_report(o)

    def test_visual_review_is_bound_to_image_sha_not_prose_without_pixels(self):
        o=self.report();o['records'][0]['visual_review']['reviewed_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Human visual review'):validate_report(o)

    def test_literal_misspelling_order_dimensions_and_absent_caption_preserved(self):
        tags=''.join('<img src="'+IMAGE_ROOT+'screeshot'+str(i)+'.gif" width="275" height="200">' for i in range(1,9))
        self.assertEqual(len(extract_refs('<!--'+tags+'-->'+tags)),8)
        for bad in [tags.replace('screeshot2.gif','screeshot1.gif'),tags.replace('width="275"','width="640"'),
                    tags.replace('border="1"',''),tags.replace('height="200"','height="200" alt="named place"')]:
            if bad==tags:continue
            with self.assertRaises(ValueError):extract_refs(bad)
        with self.assertRaises(ValueError):extract_refs(tags.replace('screeshot','screenshot'))

    def test_wrong_capture_host_or_error_body_rejected(self):
        for page_url,image_url in [(URL,IMAGE_URL),(URL.replace('20031215093733','20031214050618'),IMAGE_URL),
                                   (URL,IMAGE_URL.replace('20080819022212','20031215093733'))]:
            with self.assertRaises(ValueError):build(b'x'*14113,page_url,b'y'*46583,image_url)

    def test_archive_record_fields_and_exact_partial_visual_coverage(self):
        o=self.report();validate_report(o)
        c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(c),r.keys());self.assertEqual(r['collection'],'screens');self.assertIsNone(r['caption_as_written'])
        o['coverage']['actual_images_reacquired_and_reviewed']=8
        with self.assertRaisesRegex(ValueError,'counted as acquired'):validate_report(o)


if __name__=='__main__':unittest.main()
