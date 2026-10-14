"""Invented caller byte strings test gaps/opaque returns; no retail bytes."""
import copy
import struct
import unittest
from functools import lru_cache
from tools.stoneage_tw10_savedata_native_io_r41 import *
from tools.stoneage_tw10_savedata_native_io_r41_guard import validate


@lru_cache(maxsize=1)
def setup():
    base = 0x400000
    lo = SITES[0][0]
    raw = bytearray(b'\xcc' * (SITES[-1][0] + 192 - lo))
    for root, call in SITES:
        code = b'\x68' + struct.pack('<I', base + EXPECTED_STRING_RVA)
        code += b'\xe8' + struct.pack('<i', OPEN_ROOT - call - 5)
        code += bytes.fromhex('89c66a018d45f85056')  # opaque EAX copy, count/address candidates
        at = root + len(code)
        code += b'\xe8' + struct.pack('<i', 0x486b2 - at - 5)
        code += bytes.fromhex('83c40c85c075016ac3')  # branch joins with decode gap
        raw[root-lo:root-lo+len(code)] = code
    dec = Decoder(bytes(raw), lo, base)
    sections = [{'name': '.text', 'raw': 0, 'rva': lo, 'raw_size': len(raw), 'vsize': len(raw), 'characteristics': 0x60000020},
                {'name': '.data', 'raw': 0, 'rva': 0x63000, 'raw_size': 4096, 'vsize': 4096, 'characteristics': 0xc0000040}]
    # Synthetic entry support is deliberately partial, not a runtime entry proof.
    graph = {'visited': {at: 1 for root, call in SITES for at in (root, call)},
             'edges': {(root, call) for root, call in SITES}, 'limit_hit': False}
    return dec, sections, graph


def fixture():
    dec, sections, graph = setup()
    return derive(dec, sections, {}, graph, dec.lo)


class R41Synthetic(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(fixture()))
    def test_four_independent_contexts(self):
        cs = fixture()['caller_contexts']
        self.assertEqual([c['filename_push_rva'] for c in cs], [r for r, _ in SITES])
        self.assertTrue(all(c['entrygraph_push_to_call_edge_seen'] for c in cs))
        self.assertTrue(all(c['graph']['returning_call_assumption_only'] for c in cs))
    def test_filename_slot0(self):
        for c in fixture()['caller_contexts']:
            ps = c['filename_physical_push_suffix']['pushes']
            self.assertEqual(len(ps), 1)
            self.assertEqual(ps[0]['conditional_pre_call_esp_offset'], 0)
    def test_postcall_eax_is_opaque(self):
        a = fixture()['caller_contexts'][0]['continuation_calls'][0]
        q = next(q for q in a['input_sources']['queries'] if q['register'] == 'ebp' and q['site_rva'] == a['site_rva'])
        self.assertEqual(q['reaching_candidates'][0]['origin'], 'unknown_call')
        self.assertEqual(q['reaching_candidates'][0]['rva'], SITES[0][1])
    def test_copy_source_still_opaque(self):
        a = fixture()['caller_contexts'][0]['continuation_calls'][0]
        q = next(q for q in a['input_sources']['queries'] if q['register'] == 'eax' and q['site_rva'] == SITES[0][1] + 5)
        self.assertEqual(q['reaching_candidates'][0]['origin'], 'unknown_call')
    def test_call_pushes_have_local_geometry(self):
        a = fixture()['caller_contexts'][0]['continuation_calls'][0]
        ps = a['conditional_linear_push_suffix']['pushes']
        self.assertEqual([p['conditional_pre_call_esp_offset'] for p in ps], [0, 4, 8])
        self.assertFalse(a['actual_return_argument_buffer_count_or_io_proven'])
    def test_missing_entry_support_not_promoted(self):
        dec, sections, _ = setup()
        graph = {'visited': {dec.lo: 1}, 'edges': set(), 'limit_hit': False}
        d = derive(dec, sections, {}, graph, dec.lo)
        self.assertTrue(validate(d))
        self.assertFalse(d['caller_contexts'][0]['entrygraph_call_boundary_seen'])
    def test_span_terminal_and_branch_gaps_are_reported(self):
        c = fixture()['caller_contexts'][0]
        self.assertLess(c['graph']['nodes'], NODE_CAP)
        self.assertFalse(c['graph']['node_limit_hit'])
    def test_bad_hash(self):
        with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
            inspect_verified(b'bad', b'bad')
    def test_wrong_filename_source(self):
        dec, sections, graph = setup()
        raw = bytearray(dec.raw);raw[1:5] = struct.pack('<I', dec.base + EXPECTED_STRING_RVA + 1)
        with self.assertRaisesRegex(ValueError, 'filename immediate'):
            derive(Decoder(bytes(raw), dec.lo, dec.base), sections, {}, graph, dec.lo)


class R41Tamper(unittest.TestCase):
    def reject(self, fn):
        d = fixture();fn(d)
        with self.assertRaises(ValueError):
            validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):
                self.reject(lambda d, f=flag: d.update({f: True}))
    def test_prior_digest(self):self.reject(lambda d: d.update(r7_exact_report_sha256='bad'))
    def test_prefix_filename(self):self.reject(lambda d: d['caller_contexts'][0]['filename_prefix_shapes'][0]['operands'][0].update(constant=1))
    def test_prefix_target(self):self.reject(lambda d: d['caller_contexts'][0]['filename_call_identity'].update(direct_target_rva=1))
    def test_prefix_slot(self):self.reject(lambda d: d['caller_contexts'][0]['filename_physical_push_suffix']['pushes'][0].update(conditional_pre_call_esp_offset=4))
    def test_runtime_binding(self):self.reject(lambda d: d['caller_contexts'][0].update(actual_open_return_handle_or_payload_binding_proven=True))
    def test_call_abi(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_calls'][0]['conditional_linear_push_suffix'].update(abi_roles_applied=True))
    def test_call_effects(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_calls'][0].update(actual_return_argument_buffer_count_or_io_proven=True))
    def test_span(self):self.reject(lambda d: d['caller_contexts'][0]['graph'].update(span_bytes=768))
    def test_graph_edge(self):self.reject(lambda d: d['caller_contexts'][0]['bounded_edges'].append([1, 2]))
    def test_graph_scope(self):self.reject(lambda d: d['caller_contexts'][0]['bounded_node_rvas'].append(1))
    def test_source_site_membership(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_calls'][0]['input_sources']['queries'][0].update(site_in_candidate_graph=False))
    def test_def_count(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_calls'][0].update(direct_input_definition_count=99))
    def test_def_cap(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_calls'][0].update(direct_input_definitions_truncated=True))
    def test_call_cap(self):self.reject(lambda d: d['caller_contexts'][0].update(continuation_calls_truncated=True))
    def test_shape_cap(self):self.reject(lambda d: d['caller_contexts'][0].update(continuation_shapes_truncated=True))
    def test_non_candidate_shape(self):self.reject(lambda d: d['caller_contexts'][0]['continuation_shapes'][0].update(mnemonic='nop'))
    def test_native_payload(self):self.reject(lambda d: d.update(raw_bytes='forbidden'))


if __name__ == '__main__':
    unittest.main()
