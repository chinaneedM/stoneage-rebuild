import copy
import json
import struct
import unittest
from tools import stoneage_scene36_riding_image as m


class ActualSourceLimits(unittest.TestCase):
    def setUp(self):self.r=json.loads(m.REPORT.read_bytes())
    def reject(self,change,message):
        r=copy.deepcopy(self.r);change(r)
        with self.assertRaisesRegex(ValueError,message):m.validate(r)

    def test_actual_derived_image_reference(self):
        self.assertEqual(m.validate(self.r)['new_riding_rules'],0)

    def test_each_riding_runtime_or_date_promotion_rejected(self):
        for flag in m.FALSE:
            with self.subTest(flag=flag):
                self.reject(lambda r:r.update({flag:True}),'cannot authenticate riding')

    def test_actual_capture_not_requested_page_capture(self):
        self.reject(lambda r:r['images'][0].update(capture_timestamp='20051117143741'),'capture dates retained')

    def test_no_2003_pixels_from_article_index_date(self):
        self.reject(lambda r:r['images'][0]['HTTP'].update(resolved='https://web.archive.org/web/20031210000000id_/'+m.ORIGINALS[0]),'capture dates retained')

    def test_original_image_not_similar_filename(self):
        self.reject(lambda r:r['images'][0].update(original_url=m.ORIGINALS[1]),'JPEG identity/order')

    def test_original_resource_positions_not_swapped(self):
        self.reject(lambda r:r['images'].reverse(),'JPEG identity/order')

    def test_two_resources_not_two_new_riding_rules(self):
        self.reject(lambda r:r['source_delta'].update(new_riding_rules=2),'no duplicate rule discovery')

    def test_two_resources_not_independent_figures(self):
        self.reject(lambda r:r['source_delta'].update(original_resources_are_two_independent_figures=True),'no duplicate rule discovery')

    def test_old_unacquired_flags_not_rewritten(self):
        self.reject(lambda r:r['source_delta'].update(old_unacquired_flags_preserved_as_capture_time_history=False),'capture-time flags')

    def test_source_pixel_digest_not_inferred_from_dimensions(self):
        self.reject(lambda r:r['images'][0].update(Pillow_RGB_sha256='0'*64),'dimensions/pixels')

    def test_same_URL_other_JPEG_bytes_rejected(self):
        self.reject(lambda r:r['images'][0].update(sha256='0'*64),'JPEG identity/order')

    def test_existing_five_reports_must_remain_bound(self):
        self.reject(lambda r:r['existing_materials'].pop(),'five exact existing')

    def test_public_CI_not_original_source_execution(self):
        self.reject(lambda r:r.update(source_action_run_id=123),'source Action/progress')

    def test_manual_visual_summary_cannot_drift(self):
        self.reject(lambda r:r['visual_review'].update(visible_labels=['騎乘']),'frozen actual image')

    def test_actual_private_audit(self):
        m.validate_audit(json.loads(m.AUDIT.read_bytes()),self.r)

    def test_no_independent_readback_from_save_acknowledgement(self):
        a=json.loads(m.AUDIT.read_bytes());a['save_readback_performed']=True
        with self.assertRaisesRegex(ValueError,'save acknowledgement'):m.validate_audit(a,self.r)

    def test_full_article_not_added_to_image_delivery(self):
        a=json.loads(m.AUDIT.read_bytes());a['full_original_article_HTML_in_deliverable']=True
        with self.assertRaisesRegex(ValueError,'source summary only'):m.validate_audit(a,self.r)


class SyntheticParsing(unittest.TestCase):
    def pair(self):
        return '<a href="'+m.ORIGINALS[0]+'"><img src="'+m.ORIGINALS[1]+'"></a>'

    def test_synthetic_reference_has_one_anchor_image_pair(self):
        self.assertEqual(m.link_pair(self.pair())['img_src'],m.ORIGINALS[1])

    def test_duplicate_reference_cannot_choose_first(self):
        with self.assertRaisesRegex(ValueError,'one actual'):m.link_pair(self.pair()*2)

    def test_unlinked_image_not_accepted(self):
        with self.assertRaisesRegex(ValueError,'one actual'):m.link_pair('<img src="'+m.ORIGINALS[1]+'">')

    def test_wrong_archive_host_or_original_path_rejected(self):
        with self.assertRaisesRegex(ValueError,'archive host'):
            m.capture('https://example.com/web/20040611050307id_/'+m.ORIGINALS[1],m.ORIGINALS[1])

    def test_invalid_capture_calendar_rejected(self):
        with self.assertRaises(ValueError):
            m.capture('https://web.archive.org/web/20041399050307id_/'+m.ORIGINALS[1],m.ORIGINALS[1])

    def test_synthetic_SOF_dimensions(self):
        payload=struct.pack('>BHHB',8,225,300,3)+bytes([1,17,0,2,17,1,3,17,1])
        raw=b'\xff\xd8\xff\xc0'+struct.pack('>H',len(payload)+2)+payload+b'\xff\xd9'
        self.assertEqual(m.jpeg_shape(raw)['size'],[300,225])

    def test_truncated_SOF_rejected(self):
        with self.assertRaisesRegex(ValueError,'segment bounds'):
            m.jpeg_shape(b'\xff\xd8\xff\xc0\x00\xff\x00\xff\xd9')

    def test_HTML_200_not_JPEG(self):
        with self.assertRaisesRegex(ValueError,'JPEG SOI'):m.jpeg_shape(b'<html>not an image</html>')

    def test_synthetic_viewer_preserves_two_payload_occurrences(self):
        images=[b'synthetic target',b'synthetic inline']
        self.assertTrue(m.audit_viewer(m.viewer(images),images)['embedded_JPEG_bytes_equal_originals'])

    def test_viewer_wrong_order_rejected(self):
        images=[b'synthetic target',b'synthetic inline']
        with self.assertRaisesRegex(ValueError,'ordered original'):
            m.audit_viewer(m.viewer(images),list(reversed(images)))

    def test_external_image_not_allowed(self):
        images=[b'synthetic target',b'synthetic inline']
        with self.assertRaisesRegex(ValueError,'inline-only'):
            m.audit_viewer(m.viewer(images)+'<img src="https://example.com/x.jpg">',images)

    def test_script_in_viewer_rejected(self):
        images=[b'synthetic target',b'synthetic inline']
        with self.assertRaisesRegex(ValueError,'no active'):
            m.audit_viewer(m.viewer(images)+'<script>1</script>',images)


if __name__=='__main__':unittest.main()
