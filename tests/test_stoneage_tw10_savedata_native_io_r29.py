"""Invented scalar/address models; synthetic values never evaluate original state."""
import struct,unittest
from tools.stoneage_tw10_savedata_native_io_r29 import *
from tools.stoneage_tw10_savedata_native_io_r29_guard import validate
BASE=0x400000

def scalar(b,reg='eax'):
    dec=Decoder(b,0x1000,BASE);ins=dec.at(0x1000)
    shape={'site_rva':0x1000,'class':ins.mnemonic,'operands':[operand_shape(ins,o,[],BASE) for o in ins.operands]}
    return scalar_model(shape,reg)

def fixture():
    lo=ROWS[0][1];hi=ROWS[-1][1]+768;raw=bytearray(b'\x90'*(hi-lo))
    def put(at,b):raw[at-lo:at-lo+len(b)]=b
    prior={'contexts':[]}
    for api,root,sites,address in ROWS:
        prior['contexts'].append(dict(api=api,root_candidate_rva=root,inputs={'queries':[{'reaching_candidates':[dict(origin='definition',rva=at)]} for at,_ in sites]}))
        for at,reg in sites:put(at,bytes.fromhex('c1f805' if reg=='eax' else '83e61f'))
        put(address,bytes.fromhex('8d1c85')+struct.pack('<I',BASE+SHARED))
        put(sites[-1][0]+10,b'\xc3')
    dec=Decoder(bytes(raw),lo,BASE)
    secs=[dict(name='.data',rva=SHARED,vsize=4096,raw_size=0,raw=0,characteristics=0xc0000040)]
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r28_exact_original_revalidated=True,r28_exact_report_sha256=PRIOR_SHA256,static_only=True,
                contexts=[scalar_context(dec,secs,prior,*r) for r in ROWS],shared_address_references=shared_references(dec,secs),**{k:False for k in FLAGS})

class R29Synthetic(unittest.TestCase):
    def test_valid_invented_fixture(self):self.assertTrue(validate(fixture()))
    def test_sar_negative_rounds_down(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('c1f802')),{'eax':-9}),0xfffffffd)
    def test_sar_sign_fill(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('c1f81f')),{'eax':0x80000000}),0xffffffff)
    def test_shr_zero_fill(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('c1e81f')),{'eax':0x80000000}),1)
    def test_masked_shift_count(self):
        m=scalar(bytes.fromhex('c1e020'));self.assertEqual(m['rhs']['constant'],0);self.assertEqual(eval_synthetic(m,{'eax':0xdeadbeef}),0xdeadbeef)
    def test_shl_wrap(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('c1e002')),{'eax':0xffffffff}),0xfffffffc)
    def test_and_low_bits(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('83e01f')),{'eax':0xdeadbeef}),15)
    def test_add_register_wrap(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('01f0')),{'eax':0xffffffff,'esi':2}),1)
    def test_sub_wrap(self):self.assertEqual(eval_synthetic(scalar(bytes.fromhex('83e801')),{'eax':0}),0xffffffff)
    def test_partial_width_unqualified(self):self.assertEqual(scalar(bytes.fromhex('66c1f805'))['kind'],'unqualified_scalar')
    def test_variable_shift_unqualified(self):self.assertEqual(scalar(bytes.fromhex('d3f8'))['kind'],'unqualified_scalar')
    def test_memory_lhs_unqualified(self):self.assertEqual(scalar(bytes.fromhex('c13805'))['kind'],'unqualified_scalar')
    def test_wrong_destination_unqualified(self):self.assertEqual(scalar(bytes.fromhex('c1f905'))['kind'],'unqualified_scalar')
    def test_mul_unqualified(self):self.assertEqual(scalar(bytes.fromhex('f7e6'))['kind'],'unqualified_scalar')
    def test_original_value_not_evaluated(self):self.assertIsNone(scalar(bytes.fromhex('c1f805'))['evaluated_original_result'])
    def test_exact_indexed_displacement(self):
        refs=fixture()['shared_address_references'];self.assertEqual(refs['count'],2)
        self.assertTrue(all(r['operand']['geometry']['index_scale']==4 for r in refs['samples']))
    def test_segmented_displacement_excluded(self):
        raw=bytes.fromhex('648b0485')+struct.pack('<I',BASE+SHARED)
        self.assertEqual(shared_references(Decoder(raw,0x1000,BASE),[])['count'],0)
    def test_reference_operand_cap(self):
        raw=(b'\xb8'+struct.pack('<I',BASE+SHARED))*40
        refs=shared_references(Decoder(raw,0x1000,BASE),[]);self.assertEqual(refs['count'],40);self.assertEqual(len(refs['samples']),32);self.assertTrue(refs['samples_truncated'])
    def test_original_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R29Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_prior(self):self.reject(lambda d:d.update(r28_exact_report_sha256='wrong'))
    def test_scalar_count(self):self.reject(lambda d:d['contexts'][0]['scalar_definitions'].pop())
    def test_shift_count(self):self.reject(lambda d:d['contexts'][0]['scalar_definitions'][0]['conditional_model']['rhs'].update(constant=0))
    def test_signedness(self):self.reject(lambda d:d['contexts'][0]['scalar_definitions'][0]['conditional_model'].update(sar_uses_signed_reinterpretation=False))
    def test_evaluated_result(self):self.reject(lambda d:d['contexts'][0]['scalar_definitions'][0]['conditional_model'].update(evaluated_original_result=128))
    def test_scalar_api_role(self):self.reject(lambda d:d['contexts'][0]['scalar_definitions'][0]['conditional_model'].update(index_or_api_role_proven=True))
    def test_source_value(self):self.reject(lambda d:d['contexts'][0]['inputs']['queries'][0].update(actual_register_value_known=True))
    def test_index_scale(self):self.reject(lambda d:d['contexts'][0]['shared_address_shape']['operands'][1]['geometry'].update(index_scale=8))
    def test_shared_region(self):self.reject(lambda d:d['contexts'][0]['shared_address_shape']['operands'][1]['geometry']['displacement_region'].update(displacement_rva=0))
    def test_owner(self):self.reject(lambda d:d['contexts'][0].update(effective_address_or_table_owner_proven=True))
    def test_reference_complete(self):self.reject(lambda d:d['shared_address_references'].update(indirect_alias_complete_or_actual_table_contents_proven=True))
    def test_reference_count(self):self.reject(lambda d:d['shared_address_references'].update(count=0))
    def test_read_write_initialization(self):self.reject(lambda d:d['shared_address_references']['samples'][0].update(actual_read_write_initialization_proven=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
