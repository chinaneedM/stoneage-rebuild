import copy
import unittest
from tools import stoneage_item08_pixel_source_gate as gate

class PixelCarrier(unittest.TestCase):
    def setUp(self):
        self.patch={'source_record_sha256':'a'*64,'original_patch_physical_bitmapno':12,
                    'source_original_rd_sha256':'b'*64,'source_original_rd_size':24,'source_width':4,'source_height':2}
        self.native={'record_sha256':'a'*64,'bitmapno':'12','rd_sha256':'b'*64,'size':'24','width':'4','height':'2',
                     'rd_width':'4','rd_height':'2','rd_size':'24','rd_status':'HEADER_MATCH','index':'99','adder':'1000'}
    def test_exact_native_location_does_not_select_patch_position(self):
        result=gate.qualify_occurrence(self.patch,self.native)
        self.assertEqual(result['tw85_native_record_index'],99)
        self.assertEqual(result['tw85_real_byte_offset'],1000)
        self.assertEqual(result['pixel_carrier'],'TW85_PRESERVED_real_158.bin')
        self.assertIn('NOT_PIXEL_DECODE',result['qualification'])
    def test_same_bitmap_number_cannot_replace_original_record_or_rd(self):
        for key in ['record_sha256','rd_sha256','width','size','rd_status']:
            with self.subTest(key=key):
                bad=copy.deepcopy(self.native);bad[key]='wrong'
                with self.assertRaises(ValueError):gate.qualify_occurrence(self.patch,bad)
    def test_reject_matching_index_dimensions_with_wrong_rd_header(self):
        bad=copy.deepcopy(self.native);bad['rd_width']='8'
        with self.assertRaises(ValueError):gate.qualify_occurrence(self.patch,bad)
    def test_full_report_preserves_ambiguity_and_source_boundary(self):
        report=gate.build()
        self.assertEqual(report['summary']['candidate_record_locations'],411)
        self.assertEqual(report['summary']['candidate_aliases'],409)
        multiple=next(x for x in report['recovery_candidates'] if x['mixed25_item_image_alias']==21600)
        self.assertEqual(len(multiple['patch_source_occurrences']),3)
        self.assertEqual(multiple['distinct_patch_rd_candidates'],2)
        self.assertFalse(report['boundaries']['official_patch_contains_real_pixels'])
        self.assertFalse(report['boundaries']['full_tw85_alias_search_performed'])
        self.assertEqual(report['summary']['new_pixels_decoded'],0)
        self.assertEqual(report['source_roles']['pixel_fingerprint_carrier']['real']['name'],'real_158.bin')

if __name__=='__main__':unittest.main()
