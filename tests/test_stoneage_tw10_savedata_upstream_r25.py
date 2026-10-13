"""Invented R25 controls only; a passing fixture is not original custody."""
import struct,unittest
from tools.stoneage_tw10_savedata_upstream_r25 import *
from tools.stoneage_tw10_savedata_upstream_r25_guard import validate
BASE=0x400000;ROOT=0x1000

def fixture():
    lo=SETE_ANCHORS[0];hi=STARTS[1][2]+3
    raw=bytearray(b'\x90'*(hi-lo))
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    put(lo,b'\xe8'+struct.pack('<i',STARTS[0][1]-(lo+5)))
    put(SETE-5,bytes.fromhex('31c085c0'))
    put(SETE,bytes.fromhex('0f94c050'))
    for name,root,call in STARTS:put(call,bytes.fromhex('ffd0c3'))
    dec=Decoder(bytes(raw),lo,BASE)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r24_exact_original_revalidated=True,r24_exact_report_sha256=PRIOR_SHA256,static_only=True,
                linear_boundary_callers=linear_boundary_callers(dec),
                new_start_candidates=[start_probe(dec,[],*row) for row in STARTS],
                sete_partial_frontier=sete_frontier(dec,[]),
                realloc_new_anchor_inputs=[dict(site_rva=site,register=reg,candidate_source=candidate_sources(dec,site,reg,[],STARTS[1][1]),runtime_input_value_proven=False) for site,reg in ((0x4a0ab,'eax'),(0x4a0ab,'ecx'),(0x4a0af,'ecx'))],
                **{k:False for k in FLAGS})

class R25Synthetic(unittest.TestCase):
    def scan(self,raw,targets=(ROOT,ROOT+1),ranges=((ROOT,ROOT+256),)):
        return linear_boundary_callers(Decoder(raw,ROOT,BASE),targets,ranges)
    def test_inside_immediate_not_boundary(self):
        d=self.scan(bytes.fromhex('6840010000c3'))
        self.assertTrue(d['boundary_queries'][0]['is_linear_decode_boundary'])
        self.assertFalse(d['boundary_queries'][1]['is_linear_decode_boundary'])
        self.assertEqual(d['boundary_queries'][1]['instruction_end_rva'],ROOT+5)
    def test_direct_call_syntax_not_executed_entry(self):
        d=self.scan(bytes.fromhex('e800000000c3'))
        self.assertEqual(d['samples'][0]['kind'],'call')
        self.assertFalse(d['samples'][0]['executed_or_true_entry_proven'])
        self.assertFalse(d['all_incoming_callers_covered'])
    def test_indirect_calls_unresolved(self):
        d=self.scan(bytes.fromhex('ffd0c3'))
        self.assertEqual(d['indirect_transfers_not_resolved'],1);self.assertEqual(d['samples'],[])
    def test_conditional_jump_not_function_entry(self):
        d=self.scan(bytes.fromhex('7400c3'))
        self.assertEqual(d['samples'][0]['kind'],'conditional_jump')
    def test_unconditional_jump_distinct(self):self.assertEqual(self.scan(bytes.fromhex('eb00c3'))['samples'][0]['kind'],'jump')
    def test_decode_gap_does_not_establish_boundary(self):
        d=self.scan(bytes.fromhex('0f'),targets=(ROOT,))
        self.assertEqual(d['decode_gap_bytes'],1)
        self.assertIsNone(d['boundary_queries'][0]['instruction_start_rva'])
    def test_transfer_samples_bounded(self):
        d=self.scan(bytes.fromhex('ebfe')*70,targets=(ROOT,))
        self.assertEqual(d['direct_transfer_candidate_count'],70)
        self.assertEqual(len(d['samples']),64);self.assertTrue(d['samples_truncated'])
    def test_duplicate_query_rejected(self):
        with self.assertRaises(ValueError):self.scan(b'\xc3',targets=(ROOT,ROOT))
    def test_missing_call_retains_gap(self):
        d=start_probe(Decoder(bytes.fromhex('c390ffd0'),ROOT,BASE),[],'Test',ROOT,ROOT+2)
        self.assertFalse(d['call_in_candidate_graph']);self.assertFalse(d['true_entry_or_actual_path_proven'])
    def test_sete_partial_does_not_determine_whole_eax(self):
        raw=bytes.fromhex('31c00f94c050c3')
        d=sete_frontier(Decoder(raw,ROOT,BASE),[],anchors=(ROOT,),site=ROOT+2,push=ROOT+5)
        self.assertTrue(d['upper_24_bits_not_written_by_sete'])
        self.assertFalse(d['whole_eax_return_or_argument_known'])
        self.assertFalse(d['candidate_contexts'][0]['whole_eax_composed_value_proven'])
    def test_non_al_sete_rejected(self):
        with self.assertRaises(ValueError):sete_frontier(Decoder(bytes.fromhex('0f94c350'),ROOT,BASE),[],anchors=(ROOT,),site=ROOT,push=ROOT+3)
    def test_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')
    def test_valid_invented_fixture(self):self.assertTrue(validate(fixture()))

class R25Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_runtime_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_hash(self):self.reject(lambda d:d.update(runtime_sha256='wrong'))
    def test_prior_digest(self):self.reject(lambda d:d.update(r24_exact_report_sha256='wrong'))
    def test_complete_callers(self):self.reject(lambda d:d['linear_boundary_callers'].update(all_incoming_callers_covered=True))
    def test_boundary_flag_conflict(self):self.reject(lambda d:d['linear_boundary_callers']['boundary_queries'][0].update(is_linear_decode_boundary=False))
    def test_transfer_entry_promotion(self):self.reject(lambda d:d['linear_boundary_callers']['samples'][0].update(executed_or_true_entry_proven=True))
    def test_count_inconsistent(self):self.reject(lambda d:d['linear_boundary_callers'].update(direct_transfer_candidate_count=0))
    def test_new_start_entry_promotion(self):self.reject(lambda d:d['new_start_candidates'][0].update(true_entry_or_actual_path_proven=True))
    def test_abi_promotion(self):self.reject(lambda d:d['new_start_candidates'][0]['prefix']['r23_suffix'].update(abi_roles_applied=True))
    def test_sete_full_result(self):self.reject(lambda d:d['sete_partial_frontier'].update(whole_eax_return_or_argument_known=True))
    def test_sete_whole_register(self):self.reject(lambda d:d['sete_partial_frontier']['one_byte_destination'].update(register='eax',width_bytes=4))
    def test_flag_actual_value(self):self.reject(lambda d:d['sete_partial_frontier']['candidate_contexts'][0].update(actual_zf_known=True))
    def test_input_anchor(self):self.reject(lambda d:d['realloc_new_anchor_inputs'][0]['candidate_source'].update(candidate_anchor_rva=0x4a0a0))
    def test_input_value(self):self.reject(lambda d:d['realloc_new_anchor_inputs'][1].update(runtime_input_value_proven=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
