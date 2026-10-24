import copy,json,unittest
from tools import stoneage_tw10_writer_source_closure_p2b as m
class Guard(unittest.TestCase):
    def test_original_receipt(self):self.assertTrue(m.check())
    def test_negative_promotion_and_rewrite(self):
        j=json.loads(m.P.read_text())
        for k in range(5):
            d=copy.deepcopy(j)
            if k==0:d["sites"][0]["same_object_as_selector_proven"]=True
            if k==1:d["counts"]["named_entities_identified"]=1
            if k==2:d["sites"][7]["nearest_local_value_source"]="STACK_FRAME_MEMORY"
            if k==3:d["artifact"]["raw_sha256"]="0"*64
            if k==4:d["action"]["conclusion"]="failure"
            with self.subTest(k=k),self.assertRaises(AssertionError):m.check(d)
if __name__=="__main__":unittest.main()
