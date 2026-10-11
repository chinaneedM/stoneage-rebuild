"""Functional parser/alignment controls and source/runtime admission mutations."""
import json
from pathlib import Path
import unittest

from tools.stoneage_pet_sb_server_audit import (
    format_fields, empty_fields, alignment, enum_index, ordered, validate,
)


class ServerComparisonTests(unittest.TestCase):
    def test_restricted_format(self):
        self.assertEqual(format_fields('%s|%d|%s'), ['s', 'd', 's'])

    def test_unsupported_formats_rejected(self):
        for x in ('%s|', '%x', '%s|literal', '%s|%2d', '%s|%%', ''):
            with self.subTest(x=x), self.assertRaises(ValueError):
                format_fields(x)

    def test_empty_field_count(self):
        self.assertEqual(empty_fields('|' * 12), 13)
        self.assertEqual(empty_fields(''), 1)

    def test_invalid_empty_record(self):
        for x in ('x|', '|' * 64):
            with self.assertRaises(ValueError):
                empty_fields(x)

    def test_matching_alignment(self):
        r = alignment(14, 14, 7)
        self.assertEqual([x['sender_slot_at_client_start'] for x in r], list(range(7)))
        self.assertFalse(any(x['extends_past_sender_payload'] for x in r))

    def test_mismatched_alignment(self):
        r = alignment(13, 14, 7)
        self.assertEqual([x['sender_field_at_client_start'] for x in r], list(range(1, 8)))
        self.assertTrue(r[-1]['extends_past_sender_payload'])

    def test_alignment_bounds(self):
        for args in ((0, 14, 7), (13, 65, 7), (13, 14, -1), (True, 14, 7)):
            with self.assertRaises(ValueError):
                alignment(*args)

    def test_simple_enum(self):
        self.assertEqual(enum_index('typedef enum { A, B, C } E;', 'C'), 2)
        self.assertEqual(enum_index('enum { A=0x10, B, C=20, D };', 'D'), 21)

    def test_enum_ambiguity_and_expression(self):
        for text, target in [('enum { A=1+1, B };', 'B'),
                             ('enum { A }; enum { A };', 'A'), ('enum { A };', 'X')]:
            with self.assertRaises(ValueError):
                enum_index(text, target)

    def test_ordered_statements(self):
        ordered('alpha beta alpha gamma', ['alpha', 'alpha', 'gamma'])

    def test_missing_or_reordered(self):
        for tokens in (['alpha', 'missing'], ['gamma', 'beta']):
            with self.assertRaises(ValueError):
                ordered('alpha beta gamma', tokens)

    def report(self):
        return json.loads((Path(__file__).resolve().parents[1] /
            'research/recovered/STONEAGE-PET-SB-SERVER-COMPARISON-R1.json').read_text())

    def test_accepted_source_comparison(self):
        self.assertEqual(validate(self.report())['server_fields'][-1], 'type')

    def test_runtime_claims_rejected(self):
        for key in ('original_program_executed', 'wire_packet_captured',
                    'matching_server_verified', 'native_owner_lifecycle_verified',
                    'exact_2005_release_verified', 'early_version_promoted'):
            r = self.report(); r[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(r)

    def test_field_and_macro_promotions_rejected(self):
        for key, value in [('active_item_field_counts', [14, 14]),
                           ('default_pet_item_enabled', True), ('pet_slots', 9),
                           ('empty_item_fields', 14), ('jigsaw_field_emitted', True),
                           ('sender_client_field_width_matches', True)]:
            r = self.report(); r['profiles']['current'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(r)

    def test_source_identity_rejected(self):
        r = self.report(); r['profiles']['current']['commit'] = '0' * 40
        with self.assertRaises(ValueError):
            validate(r)

    def test_update_order_and_checksum_mutations(self):
        for key, value in [('move_update_order', ['pet_item_S46_B', 'player_item_I22']),
                           ('s_sender_string_then_checksum', False),
                           ('source_send_offset_if_new_or_80', 13),
                           ('occupied_remove_backpack_min', 6)]:
            r = self.report(); r['profiles']['current'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(r)
        r = self.report(); r['profiles']['previous']['source_blobs'] = {}
        with self.assertRaises(ValueError):
            validate(r)

    def test_missing_profile_rejected(self):
        r = self.report(); del r['profiles']['previous']
        with self.assertRaises(ValueError):
            validate(r)

    def test_alignment_and_field_order_mutation(self):
        r = self.report(); r['synthetic_alignment'] = alignment(14, 14, 7)
        with self.assertRaises(ValueError):
            validate(r)
        r = self.report(); r['client_fields'].reverse()
        with self.assertRaises(ValueError):
            validate(r)


if __name__ == '__main__':
    unittest.main()
