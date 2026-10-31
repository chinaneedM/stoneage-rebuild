import copy,json,unittest
from tools.stoneage_o22_one_pet_skill import REPORT,validate
class O22SkillSourceTests(unittest.TestCase):
    def setUp(self):self.d=json.loads(REPORT.read_bytes())
    def test_positive(self):
        self.assertEqual(validate(self.d)["source_chain"],"21 -> 1230 -> 2250 -> 29 -> 61")
    def test_original_source_and_unsupported_claims_rejected(self):
        for group,k,val in [
            ("source_version",None,"OFFICIAL_TW10"),
            ("source_rows","skill",{"source_line":19,"bytes":120,"sha256":"0"*64}),
            ("bounded_original_source_chain","PETSKILL_slot",2),
            ("bounded_original_source_chain","PETSKILL_id",62),
            ("bounded_original_source_chain","petskill_function_name_original_ascii","PETSKILL_Success"),
            ("bounded_original_source_chain","actual_petskill_callback_executed",True),
            ("bounded_original_source_chain","poison_chance_verified",True),
            ("bounded_original_source_chain","poison_turn_duration_verified",True),
            ("bounded_original_source_chain","TW10_same_named_skill_verified",True),
            ("private_custody","zip_sha256","0"*64),
            ("private_custody","original_text_published_in_public_Git",True),
            ("limits","original_world_entered",True),
            ("limits","overall_percent",100)
        ]:
            with self.subTest(group=group,field=k):
                x=copy.deepcopy(self.d)
                if k is None:x[group]=val
                else:x[group][k]=val
                with self.assertRaises(ValueError):validate(x)
if __name__=="__main__":unittest.main()
