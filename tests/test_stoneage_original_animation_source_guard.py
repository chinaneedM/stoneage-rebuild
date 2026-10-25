import copy
import json
import unittest

from tools import stoneage_original_animation_source_guard as guard


class ActualAnimationSourceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(guard.SOURCE.read_bytes())
        cls.report=guard.sample_report()

    def test_actual_source_matches_full_archived_join(self):
        self.assertTrue(guard.validate(self.source,self.report))

    def test_source_boundary_promotions_rejected_without_hash_gate(self):
        for flag in ('original_client_executed','original_colors_reproduced','assistant_viewed_or_heard_original'):
            d=copy.deepcopy(self.source);d['cases'][0][flag]=True
            with self.subTest(flag=flag),self.assertRaises(ValueError):guard.validate(d,self.report)

    def test_changed_source_geometry_namespace_or_missing_frame_block(self):
        for mutation in ('rd','group','count','selector','dropped','duplicate','file'):
            d=copy.deepcopy(self.source);c=d['cases'][0]
            if mutation=='rd':c['bitmap_witnesses'][0]['rd_block_sha256']='0'*64
            elif mutation=='group':c['group_sha256']='0'*64
            elif mutation=='count':c['frames']=8
            elif mutation=='selector':c['selectors'][2]=6
            elif mutation=='dropped':c['bitmap_witnesses'].pop()
            elif mutation=='duplicate':c['bitmap_witnesses'].append(c['bitmap_witnesses'][0])
            else:d['original_files']['spr_1.bin']['sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):guard.validate(d,self.report)

    def test_raw_receipt_bytes_are_pinned(self):
        import hashlib
        self.assertEqual(hashlib.sha256(guard.SOURCE.read_bytes()).hexdigest(),guard.SOURCE_SHA256)


if __name__=='__main__':unittest.main()
