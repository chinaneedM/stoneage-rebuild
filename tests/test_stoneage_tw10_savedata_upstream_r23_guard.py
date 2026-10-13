"""Independent original R23 semantic tamper controls using invented fixture."""
import unittest
from tests.test_stoneage_tw10_savedata_upstream_r23 import fixture
from tools.stoneage_tw10_savedata_upstream_r23_guard import validate

class R23OriginalGuard(unittest.TestCase):
    def test_fake_return_definition(self):
        d=fixture()
        d['heap_links'][0]['store_eax_sources']['reaching_candidates'][0]['origin']='definition'
        with self.assertRaises(ValueError):validate(d)
    def test_wrong_call_barrier(self):
        d=fixture()
        d['heap_links'][1]['store_eax_sources']['reaching_candidates'][0]['rva']+=1
        with self.assertRaises(ValueError):validate(d)
    def test_global_store_address_alias(self):
        d=fixture();d['heap_links'][1]['write']['destination']['base_register']='eax'
        with self.assertRaises(ValueError):validate(d)
    def test_object_owner_promotion(self):
        d=fixture();d['heap_links'][2]['write']['destination']['table_or_object_ownership_proven']=True
        with self.assertRaises(ValueError):validate(d)

if __name__=='__main__':unittest.main()
