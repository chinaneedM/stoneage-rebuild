"""Invented x86 controls only; no original specimen synthesized as evidence."""
import copy
import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r23 import (
    local_push_suffix, heap_link, CALLS, SCHEMA, STATUS, FLAGS,
    RUNTIME_SHA256, SAVEDATA_SHA256, inspect_verified)
from tools.stoneage_tw10_savedata_upstream_r23_guard import validate
BASE = 0x400000
ROOT = 0x1000
SECTIONS = [{"name": ".data", "rva": 0x1721800, "raw_size": 0,
             "vsize": 0x100, "characteristics": 0x80000000},
            {"name": ".rdata", "rva": 0x52000, "raw_size": 0x1000,
             "vsize": 0x1000, "characteristics": 0}]

def fixture():
    links = []
    for row in CALLS:
        name, anchor, call, store, target, slot = row
        raw = bytearray(b'\x90' * (store - anchor + 6))
        raw[call-anchor:call-anchor+6] = b'\xff\x15'+struct.pack('<I', BASE+slot)
        raw[store-anchor:store-anchor+5] = b'\xa3'+struct.pack('<I', BASE+target)
        raw[-1] = 0xc3
        links.append(heap_link(Decoder(bytes(raw),anchor,BASE),SECTIONS,
                              {BASE+slot:('KERNEL32.dll',name)},*row))
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,
                savedata_sha256=SAVEDATA_SHA256,r22_original_identity_revalidated=True,
                static_only=True,heap_links=links,**{k:False for k in FLAGS})

class R23Synthetic(unittest.TestCase):
    def suffix(self, raw):
        return local_push_suffix(Decoder(raw+b'\xff\xd0',ROOT,BASE), [], ROOT, ROOT+len(raw))
    def test_two_push_order_and_offsets(self):
        s=self.suffix(bytes.fromhex('5057'))
        self.assertEqual([p['conditional_pre_call_esp_offset'] for p in s['pushes']],[0,4])
        self.assertEqual([p['input']['register'] for p in s['pushes']],['edi','eax'])
        self.assertFalse(s['abi_roles_applied'])
    def test_register_arithmetic_preserves_suffix_geometry(self):
        s=self.suffix(bytes.fromhex('5083c00457'))
        self.assertEqual(len(s['pushes']),2)
    def test_stack_adjustment_barrier(self):
        s=self.suffix(bytes.fromhex('5083c40457'))
        self.assertEqual(len(s['pushes']),1)
        self.assertEqual(s['stop_reason'],'stack_or_memory_barrier')
    def test_unqualified_stack_alias_store_barrier(self):
        s=self.suffix(bytes.fromhex('50890057'))
        self.assertEqual(len(s['pushes']),1)
    def test_call_barrier(self):
        self.assertEqual(len(self.suffix(bytes.fromhex('50ffd057'))['pushes']),1)
    def test_branch_barrier(self):
        self.assertEqual(len(self.suffix(bytes.fromhex('50eb0057'))['pushes']),1)
    def test_partial_push_is_not_four_byte_geometry(self):
        self.assertEqual(len(self.suffix(bytes.fromhex('506657'))['pushes']),0)
    def test_implicit_memory_write_and_interrupt_are_barriers(self):
        for middle in ('ab','cc'):
            with self.subTest(middle=middle):
                self.assertEqual(len(self.suffix(bytes.fromhex('50'+middle+'57'))['pushes']),1)
    def test_unaligned_call_boundary_has_no_stack_claim(self):
        s=local_push_suffix(Decoder(bytes.fromhex('b801000000'),ROOT,BASE),[],ROOT,ROOT+2)
        self.assertFalse(s['linear_call_boundary_reached']);self.assertEqual(s['pushes'],[])
    def test_suffix_cap(self):
        self.assertEqual(len(self.suffix(b'\x50'*30)['pushes']),24)
    def test_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')
    def test_synthetic_links_guard_and_opaque_return(self):
        d=fixture();self.assertTrue(validate(d))
        for row in d['heap_links']:
            self.assertTrue(row['structural_call_to_store'])
            self.assertEqual(row['store_eax_sources']['reaching_candidates'],
                             [{'origin':'unknown_call','rva':row['call_rva'],'semantic':None}])
    def test_wrong_import_rejected(self):
        row=CALLS[0];slot=row[-1];anchor=row[1]
        raw=b'\x90'*4+b'\xff\x15'+struct.pack('<I',BASE+slot)+b'\x90'*2+b'\xa3'+struct.pack('<I',BASE+row[-2])+b'\xc3'
        with self.assertRaises(ValueError):heap_link(Decoder(raw,anchor,BASE),SECTIONS,
            {BASE+slot:('KERNEL32.dll','Wrong')},*row)
    def test_global_push_correlated_without_same_heap_claim(self):
        row=CALLS[1];name,anchor,call,store,target,slot=row
        raw=bytearray(b'\x90'*(store-anchor+6))
        raw[:6]=b'\xff\x35'+struct.pack('<I',BASE+0x172187c)
        raw[call-anchor:call-anchor+6]=b'\xff\x15'+struct.pack('<I',BASE+slot)
        raw[store-anchor:store-anchor+5]=b'\xa3'+struct.pack('<I',BASE+target)
        raw[-1]=0xc3
        link=heap_link(Decoder(bytes(raw),anchor,BASE),SECTIONS,
                       {BASE+slot:('KERNEL32.dll',name)},*row)
        self.assertEqual(link['global_push_candidates'][0]['global_rva'],0x172187c)
        self.assertEqual(link['local_push_suffix']['pushes'][0]['conditional_pre_call_esp_offset'],0)
        self.assertFalse(link['heap_owner_or_success_known'])

class R23Guard(unittest.TestCase):
    def reject(self,change):
        d=fixture();change(d)
        with self.assertRaises(ValueError):validate(d)
    def test_runtime_promotions(self):
        for key in FLAGS:
            with self.subTest(key=key):self.reject(lambda d:d.update({key:True}))
    def test_wrong_hash(self):self.reject(lambda d:d.update(runtime_sha256='wrong'))
    def test_wrong_import(self):self.reject(lambda d:d['heap_links'][0]['call_identity']['import_identity'].update(name='HeapAlloc'))
    def test_wrong_target(self):self.reject(lambda d:d['heap_links'][1].update(target_global_rva=0x172187c))
    def test_link_reorder(self):self.reject(lambda d:d['heap_links'].reverse())
    def test_abi_promotion(self):self.reject(lambda d:d['heap_links'][1]['local_push_suffix'].update(abi_roles_applied=True))
    def test_actual_return(self):self.reject(lambda d:d['heap_links'][0].update(runtime_return_or_write_known=True))
    def test_source_complete(self):self.reject(lambda d:d['heap_links'][0]['store_eax_sources'].update(all_incoming_paths_proven=True))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
    def test_store_effect(self):self.reject(lambda d:d['heap_links'][2]['write'].update(executed_write_proven=True))
    def test_missing_link(self):self.reject(lambda d:d['heap_links'].pop())
    def test_oversize_graph(self):self.reject(lambda d:d['heap_links'][0].update(nodes=129))
    def test_stack_offset_tamper(self):
        d=fixture();d['heap_links'][0]['local_push_suffix']['pushes']=[
            {'site_rva':CALLS[0][1], 'conditional_pre_call_esp_offset':4,'input':{'width_bytes':4}}]
        with self.assertRaises(ValueError):validate(d)
if __name__=='__main__':unittest.main()
