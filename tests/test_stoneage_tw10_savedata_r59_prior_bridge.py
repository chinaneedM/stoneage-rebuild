"""Adversarial R59 existing-original-metadata bridge tests; no original runtime."""
import copy
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_r59_prior_bridge import derive, read_exact, R28_SHA, R57_SHA, R58_SHA

ROOT=Path(__file__).resolve().parents[1]/'research/recovered'
class R59BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=(
            read_exact(ROOT/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json',R28_SHA),
            read_exact(ROOT/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R57-ORIGINAL.json',R57_SHA),
            read_exact(ROOT/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json',R58_SHA))
    def changed(self,index,mutate):
        copies=copy.deepcopy(self.data);mutate(copies[index])
        with self.assertRaises(ValueError):derive(*copies)
    def test_pinned_bridge(self):
        d=derive(*self.data)
        self.assertEqual([x['api_site_rva'] for x in d['writefile_import_syntax_sites']],[0x4c68c,0x4c6f1])
        self.assertFalse(d['actual_bytes_written_error_convention_flush_close_or_persistence_proven'])
    def test_rewrite_writefile_import_rejected(self):
        self.changed(0,lambda d:d['contexts'][2]['api_sites'][0]['identity']['import_identity'].__setitem__('name','Other'))
    def test_graph_frontier_mutation_rejected(self):
        self.changed(0,lambda d:d['contexts'][2]['graph']['frontier'].append({'reason':'invented'}))
    def test_original_wrapper_target_mutation_rejected(self):
        self.changed(1,lambda d:next(c for c in d['contexts'][0]['call_contexts'] if c['site_rva']==0x48c5e)['identity'].__setitem__('direct_target_rva',0))
    def test_shared_call_target_mutation_rejected(self):
        self.changed(2,lambda d:next(c for c in d['contexts'][0]['call_contexts'] if c['site_rva']==0x4a683)['identity'].__setitem__('direct_target_rva',0))
    def test_post_helper_cmp_operand_mutation_rejected(self):
        self.changed(2,lambda d:next(x for x in d['contexts'][0]['instruction_shapes'] if x['site_rva']==0x4a68b)['operands'][1].__setitem__('register','esi'))
    def test_no_native_promotion(self):
        d=derive(*self.data)
        self.assertFalse(d['actual_shared_call_path_reaches_writefile_proven'])
        self.assertFalse(d['actual_call_preservation_argument_values_handle_or_buffer_link_proven'])
        self.assertFalse(d['original_program_or_native_api_executed'])
if __name__=='__main__':
    unittest.main()
