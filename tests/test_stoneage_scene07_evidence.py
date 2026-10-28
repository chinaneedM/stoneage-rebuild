import copy,json,unittest
from tools.stoneage_scene07_evidence_guard import REPORT,validate

class Evidence(unittest.TestCase):
    def setUp(self):self.report=json.loads(REPORT.read_text())
    def test_original_derived_report(self):self.assertEqual(validate(self.report)['frame_occurrences'],208)
    def test_false_promotions(self):
        for key in ['original_world_entered','entity_names_verified','live_palette_verified','native_actor_occlusion_verified','native_fps_verified','official_build_authenticated']:
            with self.subTest(key=key):
                r=copy.deepcopy(self.report);r[key]=True
                with self.assertRaises(ValueError):validate(r)
    def test_discarded_occurrence_moved_selector_and_changed_sound(self):
        for change in ['remove','selector','sound','duration','index','png']:
            r=copy.deepcopy(self.report);a=r['groups'][0]['animations'][0]
            if change=='remove':a['frames'].pop()
            if change=='selector':a['direction']=7
            if change=='sound':a['frames'][0][3]+=1
            if change=='duration':a['duration_word']+=1
            if change=='index':r['groups'][0]['reserved_word']=0
            if change=='png':r['bitmaps'][0]['PNG_sha256']='invalid'
            with self.subTest(change=change),self.assertRaises(ValueError):validate(r)
    def test_no_payload_bytes_or_private_identity(self):
        text=REPORT.read_text()
        for needle in ['base64','data:image','library_file_id','PRIVATE KEY','raw_RD_bytes']:
            self.assertNotIn(needle,text)

if __name__=='__main__':unittest.main()
