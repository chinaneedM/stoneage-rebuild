"""Invented savedata wrappers for frame/call/path and tamper controls."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r42 import *
from tools.stoneage_tw10_savedata_native_io_r42_guard import validate
from tools.stoneage_tw10_savedata_native_io_r41 import derive as derive_r41, SITES, EXPECTED_STRING_RVA, OPEN_ROOT


@lru_cache(maxsize=1)
def setup():
    base, lo = 0x400000, SITES[0][0]
    hi = WRAPPERS[0][1] + 800
    raw = bytearray(b'\xcc' * (hi - lo))
    def put(at, code):raw[at-lo:at-lo+len(code)] = code
    def jump(at, target):put(at, b'\xe9' + struct.pack('<i', target - at - 5))
    for root, call in SITES:
        put(root, b'\x68' + struct.pack('<I', base + EXPECTED_STRING_RVA))
        put(call, b'\xe8' + struct.pack('<i', OPEN_ROOT - call - 5))
        put(call+5, b'\xc3')
    for _, wrapper, native, target, callers in WRAPPERS:
        for parent, call in callers:
            open_call = next(c for p, c in SITES if p == parent)
            put(open_call+5, b'\x90' * (call - open_call - 5))
            jump(open_call+5, call-5)
            put(call-5, bytes.fromhex('56506a0151'))
            put(call, b'\xe8' + struct.pack('<i', wrapper-call-5) + b'\xc3')
        # Prolog plus four EBP read spellings, multiplication and a conditional join.
        code = bytes.fromhex('5589e583ec0c538b75088b4d0c8b45108b5d140fafc185c074059090909090')
        put(wrapper, code);jump(wrapper+len(code), native-3)
        put(native-3, bytes.fromhex('505153'))
        put(native, b'\xe8' + struct.pack('<i', target-native-5) + b'\xc3')
        # Multibyte nops bound the optional linear suffix decode to fewer than64 instructions.
        start = wrapper+len(code)+5
        n = native-3-start
        pad = bytes.fromhex('0f1f840000000000')*(n//8)+b'\x90'*(n%8)
        put(start, pad)
    dec = Decoder(bytes(raw), lo, base)
    sections = [{'name': '.text', 'rva': lo, 'raw': 0, 'raw_size': len(raw), 'vsize': len(raw), 'characteristics': 0x60000020}]
    visited = {at: 1 for root, call in SITES for at in (root, call)}
    edges = {(root, call) for root, call in SITES}
    for _, root, call, target, callers in WRAPPERS:
        visited.update({root: 1, call: 5, target: 1});edges.add((call, target))
        for _, caller in callers:visited[caller] = 5;edges.add((caller, root))
    graph = {'visited': visited, 'edges': edges, 'limit_hit': False}
    prior = derive_r41(dec, sections, {}, graph, lo)
    return dec, sections, graph, prior


@lru_cache(maxsize=1)
def base_fixture():
    dec, sections, graph, prior = setup()
    return derive(dec, sections, {}, prior, graph)


def fixture():return copy.deepcopy(base_fixture())


class R42Synthetic(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(fixture()))
    def test_two_native_correspondence_candidates(self):
        ws = fixture()['wrappers']
        self.assertEqual([w['native_context_call']['identity']['direct_target_rva'] for w in ws], [0x4c5b4, 0x4a8dc])
        self.assertTrue(all(w['structural_root_to_native_call_candidate'] for w in ws))
        self.assertTrue(all(w['entrygraph_native_call_target_edge_seen'] for w in ws))
    def test_four_conditional_slots(self):
        for w in fixture()['wrappers']:
            for b in w['savedata_caller_bridges']:
                qualified = [x for x in b['conditional_frame_slot_bridges'] if x['conditional_whole_slot_geometry_candidate']]
                self.assertEqual([x['caller_pre_call_esp_relative_offset'] for x in qualified], [0, 4, 8, 12])
                self.assertFalse(any(x['actual_argument_contents_abi_alias_or_owner_binding_proven'] for x in qualified))
    def test_ebp_frame_before_unknown_sub(self):
        for w in fixture()['wrappers']:
            self.assertEqual(w['frame_definition_esp_summaries'][0]['unique_conditional_esp_delta'], -4)
            self.assertTrue(any(e['syntax_class'] == 'unknown_esp_write' for e in w['stack_effect_candidates']))
    def test_imul_is_syntax_only(self):
        for w in fixture()['wrappers']:
            self.assertTrue(any(r['mnemonic'] == 'imul' for r in w['early_stack_read_or_multiply_shapes']))
        self.assertFalse(fixture()['actual_size_product_count_or_buffer_capacity_proven'])
    def test_branch_flag_sources(self):
        for w in fixture()['wrappers']:
            b = w['pre_native_zf_branches'][0]
            self.assertEqual(b['source_candidates'][0]['shape']['mnemonic'], 'test')
    def test_no_entry_support_does_not_promote(self):
        dec, sections, graph, prior = setup()
        d = derive(dec, sections, {}, prior, {'visited': {}, 'edges': set()})
        self.assertTrue(validate(d));self.assertFalse(d['wrappers'][0]['entrygraph_wrapper_boundary_seen'])
    def test_prior_schema(self):
        dec, sections, graph, prior = setup();prior = dict(prior, schema='wrong')
        with self.assertRaisesRegex(ValueError, 'prerequisite'):derive(dec, sections, {}, prior, graph)
    def test_bad_original_hash(self):
        with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):inspect_verified(b'bad', b'bad')
    def test_wrong_native_target(self):
        dec, sections, graph, prior = setup();raw = bytearray(dec.raw);call=WRAPPERS[0][2]
        raw[call-dec.lo+1:call-dec.lo+5]=struct.pack('<i', 1)
        with self.assertRaisesRegex(ValueError, 'target mismatch'):
            derive(Decoder(bytes(raw),dec.lo,dec.base),sections,{},prior,graph)


class R42Tamper(unittest.TestCase):
    def reject(self, fn):
        d = fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d, f=flag:d.update({f:True}))
    def test_prior_hash(self):self.reject(lambda d:d.update(r41_exact_report_sha256='bad'))
    def test_slot_value(self):self.reject(lambda d:d['wrappers'][0]['savedata_caller_bridges'][0].update(actual_caller_wrapper_parameter_or_owner_binding_proven=True))
    def test_slot_offset(self):self.reject(lambda d:d['wrappers'][0]['savedata_caller_bridges'][0]['conditional_frame_slot_bridges'][0].update(caller_pre_call_esp_relative_offset=8))
    def test_slot_condition(self):self.reject(lambda d:d['wrappers'][0]['savedata_caller_bridges'][0]['conditional_frame_slot_bridges'][0].update(requires_32bit_stack_address_and_near_call_geometry=False))
    def test_frame_summary(self):self.reject(lambda d:d['wrappers'][0]['frame_definition_esp_summaries'][0].update(unique_conditional_esp_delta=0))
    def test_stack_effect(self):self.reject(lambda d:d['wrappers'][0]['stack_effect_candidates'][0].update(esp_delta=-2))
    def test_edge(self):self.reject(lambda d:d['wrappers'][0]['bounded_edges'].append([1,2]))
    def test_path(self):self.reject(lambda d:d['wrappers'][0].update(structural_root_to_native_call_candidate=False))
    def test_branch_value(self):self.reject(lambda d:d['wrappers'][0]['pre_native_zf_branches'][0].update(actual_flag_value_feasibility_or_taken_path_proven=True))
    def test_native_identity(self):self.reject(lambda d:d['wrappers'][0]['native_context_call']['identity'].update(direct_target_rva=1))
    def test_native_effect(self):self.reject(lambda d:d['wrappers'][0]['native_context_call'].update(actual_return_argument_buffer_count_or_io_proven=True))
    def test_caller_push_offset(self):self.reject(lambda d:d['wrappers'][0]['savedata_caller_bridges'][0]['prior_caller_push_candidates'][0].update(conditional_pre_call_esp_offset=4))
    def test_original_payload(self):self.reject(lambda d:d.update(raw_bytes='forbidden'))


if __name__ == '__main__':unittest.main()
