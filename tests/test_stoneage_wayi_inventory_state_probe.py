"""Synthetic multiplier/field-layout checks; no original client execution."""
import copy
import json
from pathlib import Path
import unittest

from tools.stoneage_wayi_inventory_state_probe import (
    slot_scale, row_positions, layout_signature, same_layout, probe, validate,
)
from tools.stoneage_wayi_saupdate_route_probe import decode_window


class InventoryStateTests(unittest.TestCase):
    def decode(self, code):
        return decode_window(bytes.fromhex(code), 0x1000)

    def report(self):
        return json.loads((Path(__file__).resolve().parents[1] /
            'research/recovered/STONEAGE-WAYI-INVENTORY-STATE-R1.json').read_text())

    def test_linear_multiplier_388(self):
        # Independent synthetic registers, not bytes extracted from the client.
        ins = self.decode('8d1440 c1e205 01c2 c1e202')
        self.assertEqual(slot_scale(ins, {'eax': 1})['edx'], 388)

    def test_register_index_scale(self):
        self.assertEqual(slot_scale(self.decode('8d1448'), {'eax': 1, 'ecx': 1})['edx'], 3)

    def test_unknown_multiplier_input(self):
        with self.assertRaises(ValueError):
            slot_scale(self.decode('8d1448'), {'eax': 1})

    def test_partial_displaced_and_unsupported(self):
        for code in ('66 01c2', '8d5004', '31d2', '83c201'):
            with self.subTest(code=code), self.assertRaises(ValueError):
                slot_scale(self.decode(code), {'eax': 1, 'edx': 1})

    def test_explicit_slot_and_payload_positions(self):
        self.assertEqual(row_positions(0), {'slot': 1, 'name': 2, 'last_item_field': 15})
        self.assertEqual(row_positions(2), {'slot': 31, 'name': 32, 'last_item_field': 45})

    def test_thirteen_field_sender_drift(self):
        self.assertNotEqual(row_positions(1, 13)['slot'], row_positions(1, 14)['slot'])
        self.assertEqual(row_positions(1, 13)['name'], row_positions(1, 14)['slot'])

    def test_row_position_bounds(self):
        for row, fields in ((-1, 14), (65536, 14), (True, 14), (0, 0), (0, 33)):
            with self.assertRaises(ValueError):
                row_positions(row, fields)

    def test_two_ordinary_layouts_match(self):
        r = self.report()
        self.assertTrue(same_layout(r['incremental_fields'], r['full_fields']))

    def test_pet_and_ordinary_layout_match(self):
        path = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-WAYI-COMPILED-PET-SB-STATE-R1.json'
        old = json.loads(path.read_text())
        # The accepted ledger wraps its probe results; find its derived fields.
        def find(value):
            if isinstance(value, dict):
                if 'numeric_field_writes' in value:
                    return value
                for v in value.values():
                    found = find(v)
                    if found is not None:
                        return found
            return None
        p = find(old)
        self.assertIsNotNone(p)
        rows = [{'item_field': x['token_within_slot'], 'label': x['semantic_label_from_source'],
                 'offset': x['offset_in_record'], 'kind': 'numeric', 'width_bytes': x['width_bytes']}
                for x in p['numeric_field_writes']]
        rows += [{'item_field': x['token_within_slot'], 'label': x['semantic_label_from_source'],
                  'offset': x['offset_in_record'], 'kind': 'string', 'width_bytes': None}
                 for x in p['string_destinations']]
        self.assertTrue(same_layout(rows, self.report()['incremental_fields']))

    def test_layout_width_and_offset_difference(self):
        rows = self.report()['incremental_fields']
        changed = copy.deepcopy(rows); changed[2]['width_bytes'] = 2
        self.assertFalse(same_layout(rows, changed))
        changed = copy.deepcopy(rows); changed[0]['offset'] += 1
        self.assertFalse(same_layout(rows, changed))

    def test_missing_and_duplicate_fields(self):
        rows = self.report()['incremental_fields']
        for changed in (rows[:-1], rows[:-1] + [rows[0]]):
            with self.assertRaises(ValueError):
                layout_signature(changed)

    def test_string_capacity_not_inferred(self):
        rows = self.report()['incremental_fields']; rows[0]['width_bytes'] = 29
        with self.assertRaises(ValueError):
            layout_signature(rows)

    def test_record_offsets_bounded(self):
        rows = self.report()['incremental_fields']; rows[0]['offset'] = 388
        with self.assertRaises(ValueError):
            layout_signature(rows)

    def test_accepted_display_state(self):
        self.assertEqual(validate(self.report())['full']['slots_iterated'], 24)

    def test_inflated_clear_and_swap_rejected(self):
        r = self.report(); r['incremental']['empty_clear_width_bytes'] = 388
        with self.assertRaises(ValueError):
            validate(r)
        r = self.report(); r['swap']['alch_offset16_exchanged'] = True
        with self.assertRaises(ValueError):
            validate(r)

    def test_field_stride_and_capacity_promotions(self):
        for section, key, value in [('incremental', 'tokens_per_record', 14),
                                    ('full', 'slots_iterated', 54),
                                    ('incremental', 'observed_upper_slot_guard', True)]:
            r = self.report(); r[section][key] = value
            with self.assertRaises(ValueError):
                validate(r)

    def test_consistently_changed_layout_rejected(self):
        r = self.report()
        r['incremental_fields'][0]['offset'] += 1; r['full_fields'][0]['offset'] += 1
        with self.assertRaises(ValueError):
            validate(r)

    def test_checksum_and_source_pair_claims(self):
        r = self.report(); r['swap']['integer_fields_then_checksum'] = [2, 3, 7]
        with self.assertRaises(ValueError):
            validate(r)
        r = self.report(); r['server_comparison']['profiles_admitted_as_matching_server'] = True
        with self.assertRaises(ValueError):
            validate(r)

    def test_native_runtime_promotions(self):
        for key in ('original_program_executed', 'wire_packet_captured', 'matching_server_verified',
                    'native_owner_lifecycle_verified', 'early_version_promoted'):
            r = self.report(); r[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(r)

    def test_wrong_specimen_rejected(self):
        with self.assertRaises(ValueError):
            probe(b'MZ synthetic')


if __name__ == '__main__':
    unittest.main()
