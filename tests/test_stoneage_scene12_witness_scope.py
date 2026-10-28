"""SCENE12 public numeric-only/negative witness checks."""
import copy,json,unittest
from tools.stoneage_scene12_witness_scope import REPORT,R9,validate,select_case,EXPECTED

class WitnessScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(REPORT.read_text())
        cls.r9=json.loads(R9.read_text())
    def test_positive_source_safe(self):
        self.assertEqual(validate(self.report,self.r9)['exact_controlled_inputs'],56)
    def test_reject_unsupported_promotions_and_counts(self):
        for key,val in [('original_client_launched',True),('official_pet_species_authenticated',True),
            ('original_full_frame_phase_order_proven',True),
            ('controlled_case_is_original_world_execution',True),
            ('fallback_is_modern_explicit_only',False),
            ('unwitnessed_viewer_states',0),
            ('verified_source_sha256','0'*64),
            ('exact_source_bitmap_pair_frame_states',6400)]:
            with self.subTest(key=key):
                r=copy.deepcopy(self.report);r[key]=val
                with self.assertRaises(ValueError):validate(r,self.r9)
    def test_no_raw_proprietary_assets_or_extra_fields(self):
        r=copy.deepcopy(self.report);r['source_png_base64']='leak'
        with self.assertRaises(ValueError):validate(r,self.r9)
    def test_exact_input_requires_matching_pet_frame(self):
        c=self.r9['cases'][0]
        h,p=[z['bitmapno'] for z in c['actors']]
        tag,_=select_case(self.r9['cases'],c['anchor'],c['pet_spr'],c['direction'],h,p)
        self.assertEqual(tag,'EXACT_CONTROLLED_R9_NOT_LIVE_RUNTIME')
        tag,_=select_case(self.r9['cases'],c['anchor'],c['pet_spr'],c['direction'],h,p+100000)
        self.assertEqual(tag,'SOURCE_FRAME_DIFFERS_FROM_R9_CASE')
    def test_duplicate_witness_rejected(self):
        c=self.r9['cases'][0]
        copies=self.r9['cases']+[copy.deepcopy(c)]
        with self.assertRaises(ValueError):
            select_case(copies,c['anchor'],c['pet_spr'],c['direction'],c['actors'][0]['bitmapno'],c['actors'][1]['bitmapno'])
if __name__=='__main__':unittest.main()
