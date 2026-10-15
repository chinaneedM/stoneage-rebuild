"""Synthetic-only R58 bridge/return contract tests."""
import copy
import unittest
from tools.stoneage_tw10_savedata_native_io_r58 import TARGETS, find_bridges

def fake_prior():
    return {'contexts': [
        {'root_candidate_rva': root,
         'call_contexts': [{'site_rva': call,
                            'identity': {'direct_target_rva': target}}
                           for label, target, edges in TARGETS
                           for wrapper, call in edges if wrapper == root]}
        for root in (0x48bbc, 0x4856c)]}

class TestR58Bridges(unittest.TestCase):
    def test_independent_roots_and_edges(self):
        bridges = find_bridges(fake_prior())
        self.assertEqual([b['root_candidate_rva'] for b in bridges],
                         [0x4a657, 0x4a53e])
        self.assertEqual([len(b['r57_caller_bridges']) for b in bridges],
                         [2, 1])
    def test_modified_target_rejected(self):
        d = fake_prior()
        d['contexts'][0]['call_contexts'][0]['identity']['direct_target_rva'] ^= 1
        with self.assertRaises(ValueError):
            find_bridges(d)
    def test_missing_call_rejected(self):
        d = fake_prior()
        d['contexts'][1]['call_contexts'] = []
        with self.assertRaises(ValueError):
            find_bridges(d)
    def test_no_native_claims(self):
        from tools.stoneage_tw10_savedata_native_io_r58 import FLAGS
        self.assertIn('actual_native_flush_close_or_persistence_proven', FLAGS)

if __name__ == '__main__':
    unittest.main()
