"""R24 invented controls; fixture envelopes are not historical evidence."""
import copy
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r24 import *
from tools.stoneage_tw10_savedata_upstream_r24_guard import validate
BASE=0x400000;ROOT=0x1000

def fixture():
    audits=[]
    for row,anchors in zip(CALLS,PREFIXES):
        items=[]
        for anchor in anchors:
            raw=b'\x90'*(row[2]-anchor-1)+b'\x50\xff\xd0\xc3'
            items.append(prefix_audit(Decoder(raw,anchor,BASE),[],anchor,row[2]))
        audits.append(dict(name=row[0],call_rva=row[2],candidate_prefixes=items,
                           r23_suffix_revalidated=True,selected_function_entry_proven=False))
    raw=bytearray(b'\x90'*(CALLS[2][2]-SCALAR_ROOT+3))
    raw[SCALAR_SITE-SCALAR_ROOT:SCALAR_SITE-SCALAR_ROOT+3]=bytes.fromhex('c1e004')
    raw[-3:]=bytes.fromhex('ffd0c3')
    dec=Decoder(bytes(raw),SCALAR_ROOT,BASE)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r23_original_identity_revalidated=True,r23_exact_report_sha256=PRIOR_REPORT_SHA256,static_only=True,
                prefix_audits=audits,realloc_eax_definition=scalar_definition(dec,[]),
                realloc_branch_frontier=branch_frontier(dec,[]),**{k:False for k in FLAGS})

class R24Synthetic(unittest.TestCase):
    def prefix(self,raw):return prefix_audit(Decoder(raw+b'\xff\xd0',ROOT,BASE),[],ROOT,ROOT+len(raw))
    def test_partial_push_barrier_exact_width(self):
        d=self.prefix(bytes.fromhex('665750'))
        self.assertEqual(d['last_suffix_barrier']['kind'],'partial_or_other_push')
        self.assertEqual(d['last_suffix_barrier']['operand_shapes'][0]['width_bytes'],2)
        self.assertEqual(len(d['r23_suffix']['pushes']),1)
    def test_memory_write_barrier(self):self.assertEqual(self.prefix(bytes.fromhex('890050'))['last_suffix_barrier']['kind'],'memory_write')
    def test_stack_barrier(self):self.assertEqual(self.prefix(bytes.fromhex('83c40450'))['last_suffix_barrier']['kind'],'stack_register_write')
    def test_control_barrier(self):self.assertEqual(self.prefix(bytes.fromhex('eb0050'))['last_suffix_barrier']['kind'],'control_transfer')
    def test_implicit_writer_is_memory_barrier(self):self.assertEqual(self.prefix(bytes.fromhex('ab50'))['last_suffix_barrier']['kind'],'memory_write')
    def test_no_verified_entry_in_straight_prefix(self):self.assertFalse(self.prefix(bytes.fromhex('5057'))['verified_entry_or_alignment'])
    def test_boundary_gap_suppresses_barrier(self):
        d=prefix_audit(Decoder(bytes.fromhex('b801000000'),ROOT,BASE),[],ROOT,ROOT+2)
        self.assertFalse(d['linear_boundary_reached']);self.assertIsNone(d['last_suffix_barrier'])
    def test_shift_mask_and_unknown_result(self):
        s=scalar_definition(Decoder(bytes.fromhex('c1e024'),ROOT,BASE),[],site=ROOT,root=ROOT)
        self.assertEqual(s['conditional_scalar_model']['literal_shift_count'],4)
        self.assertIsNone(s['conditional_scalar_model']['evaluated_runtime_result'])
    def test_other_arithmetic_unmodeled(self):
        s=scalar_definition(Decoder(bytes.fromhex('83c004'),ROOT,BASE),[],site=ROOT,root=ROOT)
        self.assertEqual(s['conditional_scalar_model']['kind'],'unmodeled')
    def test_partial_eax_alias_is_not_full_eax_definition(self):
        with self.assertRaises(ValueError):scalar_definition(Decoder(bytes.fromhex('b001'),ROOT,BASE),[],site=ROOT,root=ROOT)
    def test_call_kills_flag_provenance(self):
        d=branch_frontier(Decoder(bytes.fromhex('ffd0740090ffd0c3'),ROOT,BASE),[],root=ROOT,call=ROOT+5)
        self.assertEqual(d['branches'][0]['flag_sources'],[{'origin':'unknown_call','rva':ROOT,'semantic':None}])
        self.assertFalse(d['branches'][0]['branch_outcome_known'])
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')
    def test_valid_invented_envelope(self):self.assertTrue(validate(fixture()))

class R24Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_runtime_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_hash(self):self.reject(lambda d:d.update(runtime_sha256='wrong'))
    def test_prior_digest(self):self.reject(lambda d:d.update(r23_exact_report_sha256='wrong'))
    def test_entry_promotion(self):self.reject(lambda d:d['prefix_audits'][0]['candidate_prefixes'][0].update(verified_entry_or_alignment=True))
    def test_prefix_abi(self):self.reject(lambda d:d['prefix_audits'][0]['candidate_prefixes'][0]['r23_suffix'].update(abi_roles_applied=True))
    def test_call_identity(self):self.reject(lambda d:d['prefix_audits'][0].update(call_rva=1))
    def test_scalar_result(self):self.reject(lambda d:d['realloc_eax_definition']['conditional_scalar_model'].update(evaluated_runtime_result=128))
    def test_wrong_shift_mask(self):self.reject(lambda d:d['realloc_eax_definition']['conditional_scalar_model'].update(shift_count_mask=63))
    def test_allocation_role(self):self.reject(lambda d:d['realloc_eax_definition'].update(allocation_size_or_role_proven=True))
    def test_no_call_flag_havoc(self):self.reject(lambda d:d['realloc_branch_frontier'].update(opaque_calls_kill_flags=False))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
    def test_graph_cap(self):self.reject(lambda d:d['realloc_branch_frontier'].update(nodes=129))
if __name__=='__main__':unittest.main()
