import unittest
from tools.stoneage_pet_atlas_r3_visual_reuse import select_rd, digest
class ExactReuseTest(unittest.TestCase):
    def test_no_collision_or_bad_geometry(self):
        a=dict(bitmapno="1",rd="a",size="20",width="2",height="3")
        b=dict(a,bitmapno="2",width="0")
        c=dict(a,bitmapno="3")
        self.assertEqual(select_rd([a,b,c,c],{1,2,3},"rd"),{1:("a",20,2,3)})
    def test_descriptor_order(self):
        self.assertNotEqual(digest([[1,0,0,0],[2,0,0,0]]),digest([[2,0,0,0],[1,0,0,0]]))
        self.assertNotEqual(digest([[1,0,0,0]]),digest([[1,0,0,1]]))
