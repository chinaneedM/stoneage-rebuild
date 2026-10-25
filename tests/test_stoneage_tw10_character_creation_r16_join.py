import copy
import unittest
from tools.stoneage_tw10_character_creation_r16_join import load, qualify, LOGIN, ANIM

class CreationJoinTests(unittest.TestCase):
    def setUp(self):
        d=load();self.l=d[LOGIN];self.a=d[ANIM]
    def test_verified_bounded_expression(self):
        r=qualify(self.l,self.a)
        self.assertEqual(r["body_writer_bounded_source"]["indexed_table_va"],4558376)
        self.assertIsNone(r["actual_table_length"])
        self.assertIsNone(r["original_body_id"])
    def test_refuse_fabricated_producer(self):
        x=copy.deepcopy(self.l)
        x["selector_writer_inventory"]["lineage_body_candidate"]["write_candidates"][0]["bounded_operand_operations"][4]["operands"][1]["displacement"]=0
        with self.assertRaises(ValueError):qualify(x,self.a)
    def test_no_automatic_identity(self):
        x=copy.deepcopy(self.l);x["original_character_count"]=12
        with self.assertRaises(ValueError):qualify(x,self.a)

if __name__=="__main__":unittest.main()
