"""Synthetic processor inventory completion and tamper replay."""
import copy,unittest
from functools import lru_cache
from tests.test_stoneage_tw10_savedata_native_io_r50 import fixture as prior_fixture
from tools.stoneage_tw10_savedata_native_io_r51 import *
from tools.stoneage_tw10_savedata_native_io_r51_guard import validate
@lru_cache(maxsize=1)
def base_fixture():
    lo,hi,base=0x47160,0x47300,0x400000;raw=bytearray(b'\xcc'*(hi-lo))
    def put(a,b):raw[a-lo:a-lo+len(b)]=b
    # Prior R50 invented processor, including opaque inner CALL and unknown LEAVE.
    put(ROOT,bytes.fromhex('5589e58b75088b7d148b4d0c85c9740b'))
    import struct
    put(ROOT+16,b'\xe8'+struct.pack('<i',0x47200-(ROOT+16)-5))
    put(ROOT+21,bytes.fromhex('880783c60149c9c3'));put(0x47200,b'\xc3')
    sections=[{'name':'.text','rva':lo,'vsize':hi-lo,'raw':0,'raw_size':hi-lo,'characteristics':0x60000020}]
    return derive(Decoder(bytes(raw),lo,base),sections,prior_fixture())
def fixture():return copy.deepcopy(base_fixture())
class R51Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_all_instruction_rows(self):
        d=fixture();self.assertEqual([r['site_rva'] for r in d['processor_instruction_shapes']],d['r50_snapshot']['processing_entry_context']['bounded_node_rvas'])
    def test_unmodeled_stack_remains_open(self):self.assertFalse(fixture()['conditional_consumer_analysis']['processor_entry_stack_coordinates']['actual_call_entry_esp_or_stack_values_proven'])
    def test_local_lea_coordinates(self):self.assertEqual([r['conditional_address_relative_pre_call_esp'] for r in fixture()['conditional_consumer_analysis']['caller_local_lea_coordinates']],[32,36])
    def test_bad_original(self):
        with self.assertRaises(ValueError):inspect_verified(b'bad',b'bad')
class R51Tamper(unittest.TestCase):
    def reject(self,fn):
        d=fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_source(self):self.reject(lambda d:d.update(r50_exact_report_sha256='bad'))
    def test_promotions(self):
        for k in FLAGS:self.reject(lambda d,k=k:d.update({k:True}))
    def test_missing_instruction(self):self.reject(lambda d:d['processor_instruction_shapes'].pop())
    def test_duplicate_instruction(self):self.reject(lambda d:d['processor_instruction_shapes'].append(d['processor_instruction_shapes'][-1]))
    def test_instruction_cap(self):self.reject(lambda d:d.update(processor_instruction_shapes_truncated=True))
    def test_instruction_count(self):self.reject(lambda d:d.update(processor_instruction_count=999))
    def test_prior_shape(self):self.reject(lambda d:next(r for r in d['processor_instruction_shapes'] if r['site_rva']==d['r50_snapshot']['processing_entry_context']['early_frame_shapes'][0]['site_rva']).update(mnemonic='nop'))
    def test_output_alias(self):self.reject(lambda d:d['conditional_consumer_analysis'].update(post_call_esp_change_assumed_zero_or_output_binding_proven=True))
    def test_lea_coordinate(self):self.reject(lambda d:d['conditional_consumer_analysis']['caller_local_lea_coordinates'][0].update(conditional_address_relative_pre_call_esp=0))
    def test_boolean_type(self):self.reject(lambda d:d['conditional_consumer_analysis'].update(caller_local_stack_limit_hit=0))
    def test_processor_total(self):self.reject(lambda d:d['conditional_consumer_analysis'].update(processor_memory_control_total=999))
    def test_schema(self):self.reject(lambda d:d['conditional_consumer_analysis'].update(actual_schema_length_version_migration_or_algorithm_proven=True))
    def test_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))
if __name__=='__main__':unittest.main()
