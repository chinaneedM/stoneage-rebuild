import struct,unittest
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity,linear_references,inspect_verified,MAX_SAMPLES
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
ROOT=0x1000;BASE=0x400000;TARGET=0x60000;VA=BASE+TARGET
class TestR12(unittest.TestCase):
 def call(self,raw,imports=None):return call_identity(Decoder(raw,ROOT,BASE),ROOT,imports or {},[])
 def test_exact_absolute_iat_association(self):
  r=self.call(b'\xff\x15'+struct.pack('<I',VA),{VA:('KERNEL32.dll','TestImport')});self.assertTrue(r['import_slot_association_proven']);self.assertEqual(r['import_identity']['iat_rva'],TARGET);self.assertFalse(r['runtime_target_or_effects_proven'])
 def test_segmented_memory_is_not_iat_association(self):
  r=self.call(b'\x64\xff\x15'+struct.pack('<I',VA),{VA:('KERNEL32.dll','TestImport')});self.assertIsNone(r['import_identity'])
 def test_indexed_memory_does_not_associate_displacement(self):
  r=self.call(b'\xff\x14\x85'+struct.pack('<I',VA),{VA:('KERNEL32.dll','TestImport')});self.assertIsNone(r['import_identity']);self.assertEqual(r['memory_target']['index_register'],'eax')
 def test_register_call_unknown(self):
  r=self.call(b'\xff\xd0');self.assertEqual(r['register_target'],'eax');self.assertFalse(r['import_slot_association_proven'])
 def test_direct_call_not_iat(self):
  r=self.call(b'\xe8'+struct.pack('<i',VA-(BASE+ROOT+5)),{VA:('KERNEL32.dll','TestImport')});self.assertEqual(r['kind'],'direct');self.assertIsNone(r['import_identity'])
 def test_unknown_absolute_slot_stays_unknown(self):self.assertIsNone(self.call(b'\xff\x15'+struct.pack('<I',VA))['import_identity'])
 def test_non_call_rejected(self):
  with self.assertRaises(ValueError):self.call(b'\xc3')
 def refs(self,raw):return linear_references(Decoder(raw,ROOT,BASE),(TARGET,))
 def test_absolute_read_write_and_address_candidates(self):
  r=self.refs(b'\xa1'+struct.pack('<I',VA)+b'\xa3'+struct.pack('<I',VA)+b'\x68'+struct.pack('<I',VA)+b'\xc3')
  counts=r['globals'][0]['counts'];self.assertEqual(counts['read_candidate'],1);self.assertEqual(counts['write_candidate'],1);self.assertEqual(counts['address_candidate'],1);self.assertFalse(r['all_indirect_references_covered'])
 def test_based_operand_does_not_prove_absolute_reference(self):
  r=self.refs(b'\x8b\x80'+struct.pack('<I',VA));self.assertEqual(sum(r['globals'][0]['counts'].values()),0)
 def test_x87_store_unknown_despite_access_bits(self):
  r=self.refs(b'\xd9\x1d'+struct.pack('<I',VA));self.assertEqual(r['globals'][0]['counts']['unknown_candidate'],1)
 def test_samples_bounded_counts_retained(self):
  r=self.refs((b'\xa1'+struct.pack('<I',VA))*(MAX_SAMPLES+4));row=r['globals'][0];self.assertEqual(len(row['samples']),MAX_SAMPLES);self.assertEqual(row['counts']['read_candidate'],MAX_SAMPLES+4);self.assertTrue(row['samples_truncated'])
 def test_decode_gap_explicit(self):
  r=self.refs(b'\x0f');self.assertEqual(r['decode_gap_bytes'],1);self.assertEqual(r['decoded_instructions'],0)
 def test_duplicate_global_rejected(self):
  with self.assertRaises(ValueError):linear_references(Decoder(b'\xc3',ROOT,BASE),(TARGET,TARGET))
 def test_wrong_original_hash(self):
  with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'')
if __name__=='__main__':unittest.main()
