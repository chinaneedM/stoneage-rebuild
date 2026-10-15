"""Independent R58 source-reverse and adversarial tests with invented instruction rows."""
import copy
import unittest
from tools.stoneage_tw10_savedata_return_r58_audit import reverse_queries, same


def fake_context():
    return {
        'root_candidate_rva': 0x4a657,
        'instruction_shapes': [
            {'site_rva': 0x4a657, 'mnemonic': 'mov', 'decoder_written_registers': ['eax'],
             'decoder_read_registers': [], 'operands': []},
            {'site_rva': 0x4a659, 'mnemonic': 'ret', 'decoder_written_registers': [],
             'decoder_read_registers': [], 'operands': []},
        ],
        'bounded_edges': [[0x4a657, 0x4a659]],
        'return_analysis': {
            'return_contexts': [{
                'shape': {'site_rva': 0x4a659},
                'eax_source_graph': {'queries': [{
                    'site_rva': 0x4a659, 'register': 'eax',
                    'source_candidates': [{'origin': 'definition', 'site_rva': 0x4a657}],
                }]},
            }],
        },
    }


class R58IndependentTests(unittest.TestCase):
    def test_valid_reverse_definition(self):
        self.assertEqual(reverse_queries(fake_context()), [(0x4a659, 'eax')])

    def test_wrong_source_site_rejected(self):
        c = fake_context()
        c['return_analysis']['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates'][0]['site_rva'] += 1
        with self.assertRaises(ValueError):
            reverse_queries(c)

    def test_wrong_source_origin_rejected(self):
        c = fake_context()
        c['return_analysis']['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates'][0]['origin'] = 'entry'
        with self.assertRaises(ValueError):
            reverse_queries(c)

    def test_opaque_call_barrier_cannot_be_promoted_to_definition(self):
        c = fake_context()
        c['instruction_shapes'][0]['mnemonic'] = 'call'
        with self.assertRaises(ValueError):
            reverse_queries(c)
        c['return_analysis']['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates'] = [
            {'origin': 'unknown_call', 'site_rva': 0x4a657}]
        self.assertEqual(len(reverse_queries(c)), 1)

    def test_comparison_is_not_truthiness_or_type_coercion(self):
        self.assertFalse(same({'actual_persistence': False}, {'actual_persistence': 0}))
        self.assertFalse(same({'queries': 3}, {'queries': 4}))


if __name__ == '__main__':
    unittest.main()
