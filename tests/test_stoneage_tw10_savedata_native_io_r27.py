"""Invented instruction controls, not original API execution evidence."""
import struct,unittest
from tools.stoneage_tw10_savedata_native_io_r27 import *
from tools.stoneage_tw10_savedata_native_io_r27_guard import validate
BASE=0x400000

def fixture():
    lo=CREATE_SITE-16;raw=bytearray(b'\x90'*128)
    sections=[dict(name='.idata',rva=0x52000,vsize=4096,raw_size=4096,raw=0,characteristics=0x40000040)]
    imports={BASE+0x52000+i*4:('KERNEL32.dll',api) for i,api in enumerate(APIS)}
    for i in range(3):
        site=CREATE_SITE+i*32
        raw[site-lo-5:site-lo]=b'\x68'+struct.pack('<I',BASE+EXPECTED_STRING_RVA)
        raw[site-lo:site-lo+6]=b'\xff\x15'+struct.pack('<I',BASE+0x52000+i*4)
    dec=Decoder(bytes(raw),lo,BASE);inv,calls,transfers=scan_apis(dec,sections,imports)
    selected=choose_details(calls)
    return dict(schema=SCHEMA,status=STATUS,runtime_sha256=RUNTIME_SHA256,savedata_sha256=SAVEDATA_SHA256,
                r26_exact_original_revalidated=True,r26_exact_report_sha256=PRIOR_SHA256,static_only=True,
                savedata_literal_rva=EXPECTED_STRING_RVA,inventory=inv,
                selected_api_details=[detail(dec,sections,imports,r) for r in selected],
                nearby_direct_callers=caller_surface(transfers,selected,lo),**{k:False for k in FLAGS})

class R27Synthetic(unittest.TestCase):
    def test_valid_fixture(self):self.assertTrue(validate(fixture()))
    def test_exact_iat_required(self):
        inv,calls,_=scan_apis(Decoder(bytes.fromhex('ff1500204500'),0x1000,BASE),[],{})
        self.assertFalse(calls);self.assertEqual(sum(r['count'] for r in inv['apis']),0)
    def test_register_call_not_import(self):
        self.assertFalse(scan_apis(Decoder(bytes.fromhex('ffd0'),0x1000,BASE),[],{BASE:('KERNEL32.dll','ReadFile')})[1])
    def test_wrong_dll_rejected(self):
        self.assertFalse(scan_apis(Decoder(bytes.fromhex('ff1500204500'),0x1000,BASE),[],{0x452000:('OTHER.dll','ReadFile')})[1])
    def test_wrong_api_rejected(self):
        self.assertFalse(scan_apis(Decoder(bytes.fromhex('ff1500204500'),0x1000,BASE),[],{0x452000:('KERNEL32.dll','ReadFileEx')})[1])
    def test_call_sample_cap(self):
        raw=bytes.fromhex('ff1500204500')*40
        inv,calls,_=scan_apis(Decoder(raw,0x1000,BASE),[],{0x452000:('KERNEL32.dll','WriteFile')})
        self.assertEqual(inv['apis'][2]['count'],40);self.assertEqual(len(inv['apis'][2]['samples']),32)
        self.assertTrue(inv['apis'][2]['samples_truncated'])
    def test_details_require_pinned_create(self):
        with self.assertRaises(ValueError):choose_details([])
    def test_details_cap_two_read_write(self):
        calls=[dict(api='CreateFileA',site_rva=CREATE_SITE)]+[dict(api=a,site_rva=i) for a in APIS[1:] for i in range(10)]
        self.assertEqual(len(choose_details(calls)),5)
    def test_only_direct_calls_in_nearby_surface(self):
        rows=[dict(site_rva=10,target_rva=CREATE_SITE,kind=k) for k in ('call','jump','conditional_jump')]
        s=caller_surface(rows,[dict(site_rva=CREATE_SITE)],0)
        self.assertEqual(s['count'],1);self.assertFalse(s['samples'][0]['executed_or_true_entry_proven'])
    def test_nearby_window_not_whole_program(self):
        s=caller_surface([dict(site_rva=10,target_rva=CREATE_SITE+64,kind='call')],[dict(site_rva=CREATE_SITE)],0)
        self.assertEqual(s['count'],0)
    def test_literal_syntax_not_link(self):
        d=fixture();r=d['selected_api_details'][0]
        self.assertTrue(r['push_candidates'][0]['savedata_literal_address_candidate'])
        self.assertFalse(r['related_to_savedata_literal_proven'])
    def test_literal_join_no_unique_candidate(self):
        token=dict(origin='definition',semantic=dict(kind='constant_assignment',width_bits=32,constant=BASE+EXPECTED_STRING_RVA))
        self.assertFalse(savedata_literal_candidate({'kind':'register'},{'reaching_candidates':[token,token],'candidates_truncated':False},BASE))
    def test_hash_gate(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'wrong')

class R27Guard(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for k in FLAGS:
            with self.subTest(k=k):self.reject(lambda d:d.update({k:True}))
    def test_prior(self):self.reject(lambda d:d.update(r26_exact_report_sha256='wrong'))
    def test_inventory_complete(self):self.reject(lambda d:d['inventory'].update(all_indirect_api_sites_or_runtime_paths_proven=True))
    def test_sample_count(self):self.reject(lambda d:d['inventory']['apis'][0].update(count=2))
    def test_api_name(self):self.reject(lambda d:d['selected_api_details'][0]['identity']['import_identity'].update(name='WriteFile'))
    def test_iat_geometry(self):self.reject(lambda d:d['selected_api_details'][0]['identity']['memory_target'].update(base_register='eax'))
    def test_return(self):self.reject(lambda d:d['selected_api_details'][0].update(external_return_eax_unknown=False))
    def test_entry(self):self.reject(lambda d:d['selected_api_details'][0].update(actual_entry_or_feasible_path_proven=True))
    def test_stack_abi(self):self.reject(lambda d:d['selected_api_details'][0]['suffix'].update(abi_roles_applied=True))
    def test_offset(self):self.reject(lambda d:d['selected_api_details'][0]['suffix']['pushes'][0].update(conditional_pre_call_esp_offset=4))
    def test_literal_tamper(self):self.reject(lambda d:d['selected_api_details'][0]['push_candidates'][0].update(savedata_literal_address_candidate=False))
    def test_source_value(self):self.reject(lambda d:d['selected_api_details'][0]['registers_before_call']['eax'].update(value_known=True))
    def test_window(self):self.reject(lambda d:d['nearby_direct_callers']['windows'][0].update(start_rva=0))
    def test_payload(self):self.reject(lambda d:d.update(instruction_bytes='forbidden'))
if __name__=='__main__':unittest.main()
