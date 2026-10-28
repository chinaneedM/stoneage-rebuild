import copy,json,struct,unittest
from tools.stoneage_private_scene_actor_r7 import select_animations
from tools.stoneage_private_scene_pet_r8 import qualified_links,PET_KEYS
from tools.stoneage_scene08_evidence_guard import REPORT,validate

class PetEvidence(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_text())
    def test_actual_pet_evidence(self):self.assertEqual(validate(self.r)['frame_occurrences'],256)
    def test_all_original_template_occurrences_including_zero_flag(self):
        links,_=qualified_links();self.assertEqual(len(links),7)
        zero=[r for r in links if r['server_flag_column_38']==0]
        self.assertEqual([r['server_original_line'] for r in zero],[479])
        r=copy.deepcopy(self.r);r['template_links']=[v for v in r['template_links'] if v['server_flag_column_38']]
        with self.assertRaisesRegex(ValueError,'seven'):validate(r)
    def test_name_must_remain_original(self):
        r=copy.deepcopy(self.r);r['groups'][0]['preserved_template_name']='乌力'
        with self.assertRaisesRegex(ValueError,'names'):validate(r)
    def test_same_integer_is_not_official_species_or_deployment_proof(self):
        for key in ['same_deployed_build_proven','official_species_identity_authenticated','original_world_entered','native_actor_occlusion_verified','native_fps_verified','automatic_action_fallback']:
            r=copy.deepcopy(self.r);r[key]=True
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'promotion'):validate(r)
    def test_repeated_twenty_frames_cannot_be_collapsed_to_eight_images(self):
        r=copy.deepcopy(self.r);a=r['groups'][2]['animations'][0];self.assertEqual(len(a['frames']),20)
        self.assertEqual(len({f[0] for f in a['frames']}),8)
        a['frames']=[f for i,f in enumerate(a['frames']) if f not in a['frames'][:i]]
        with self.assertRaisesRegex(ValueError,'repeats'):validate(r)
    def test_unavailable_human_action_not_invented(self):
        r=copy.deepcopy(self.r);r['groups'][0]['absent_source_action_codes']=[]
        with self.assertRaisesRegex(ValueError,'missing human action'):validate(r)
    def test_explicit_one_action_selector_and_missing_action_rejection(self):
        raw=b''.join(struct.pack('<HHII',d,2,500,1)+struct.pack('<IhhH',123,0,0,0) for d in range(8))
        idx=struct.pack('<IIHH',100250,0,8,16)
        self.assertEqual(len(select_animations(idx,raw,(100250,),actions=(2,))[0]['animations']),8)
        with self.assertRaisesRegex(ValueError,'missing'):select_animations(idx,raw,(100250,),actions=(2,6))
        with self.assertRaisesRegex(ValueError,'unique'):select_animations(idx,raw,(100250,),actions=(2,2))
    def test_reused_human_cannot_be_relabelled_as_pet(self):
        r=copy.deepcopy(self.r);r['human_reused']['group']['spr_no']=100250
        with self.assertRaisesRegex(ValueError,'human'):validate(r)
    def test_no_proprietary_payload_or_private_storage_identity(self):
        raw=REPORT.read_text()
        for key in ['data:image','base64','library_file_id','PRIVATE KEY','raw_RD_bytes']:self.assertNotIn(key,raw)

if __name__=='__main__':unittest.main()
