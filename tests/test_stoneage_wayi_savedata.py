"""Independent synthetic byte oracles and version/profile mutation controls."""
import json
from pathlib import Path
import random
import unittest

from tools.stoneage_wayi_savedata import (encode_key_zero, decode_key_zero,
 migration, write_pet_selection, clear_pet_selection, read_pet_selection,
 write_options, read_options, settings_factory, validate, probe)


def oracle_encode(plain):
    # Declarative periods independently derived: no squared modulo or branch
    # from implementation, signed byte products reduce to identical low bytes.
    masks = (255, 0, 255, 0, 255, 255, 255, 0, 255, 0)
    coefficients = (1, 4, 2, 2, 4, 1, 0)
    total = sum(plain) % 256
    return bytes([total]+[(b ^ masks[i % 10]) + coefficients[i % 7]*total & 255 for i, b in enumerate(plain)])


class SavedataTests(unittest.TestCase):
    def report(self):
        path = Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-WAYI-SAVEDATA-R1.json'
        return json.loads(path.read_text())

    def test_hand_calculated_single_byte(self):
        # value0x80: complement0x7f + checksum0x80 = 0xff.
        self.assertEqual(encode_key_zero(b'\x80'), b'\x80\xff')
        self.assertEqual(decode_key_zero(b'\x80\xff'), b'\x80')

    def test_hand_calculated_three_bytes(self):
        self.assertEqual(encode_key_zero(b'\x01\x02\x03'), bytes([6, 4, 26, 8]))
        self.assertEqual(decode_key_zero(bytes([6, 4, 26, 8])), b'\x01\x02\x03')

    def test_every_single_byte_against_periodic_oracle(self):
        for value in range(256):
            plain = bytes([value]); encoded = oracle_encode(plain)
            self.assertEqual(encode_key_zero(plain), encoded)
            self.assertEqual(decode_key_zero(encoded), plain)

    def test_all_lengths_and_deterministic_high_byte_oracle(self):
        rng = random.Random(20261012)
        for length in range(1, 128):
            for _ in range(4):
                plain = rng.randbytes(length); expected = oracle_encode(plain)
                self.assertEqual(encode_key_zero(plain), expected)
                self.assertEqual(decode_key_zero(expected), plain)

    def test_zero_checksum_is_not_skipped(self):
        plain = b'\x80\x80'
        self.assertEqual(encode_key_zero(plain), b'\0\x7f\x80')
        self.assertEqual(decode_key_zero(encode_key_zero(plain)), plain)

    def test_plain_input_not_mutated_by_model(self):
        plain = bytes(range(127)); copy_plain = bytes(plain)
        encode_key_zero(plain)
        self.assertEqual(plain, copy_plain)

    def test_exact_factory_size_and_encoding_size(self):
        plain = settings_factory(1, 100, 80, b'\x77'*16)
        self.assertEqual(len(encode_key_zero(plain)), 128)
        self.assertEqual(decode_key_zero(encode_key_zero(plain)), plain)

    def test_no_checksum_authentication_in_decoder(self):
        plain = settings_factory(1, 2, 3, bytes(range(16)))
        encoded = bytearray(encode_key_zero(plain)); encoded[-1] ^= 1
        decoded = decode_key_zero(bytes(encoded))
        self.assertNotEqual(sum(decoded) & 255, encoded[0])
        self.assertTrue(migration(decoded, b'\0'*127)[1]['success'])

    def test_empty_and_division_zero_native_cases_excluded(self):
        for encoded in (b'', b'\0'):
            with self.assertRaises(ValueError): decode_key_zero(encoded)
        with self.assertRaises(ValueError): encode_key_zero(b'')

    def test_native_oversize_not_silently_claimed_safe(self):
        with self.assertRaises(ValueError): decode_key_zero(b'\0'*129)
        with self.assertRaises(ValueError): encode_key_zero(b'\0'*128)

    def test_v4_tail_and_reserved_bytes_retained(self):
        prior = b'\xcc'*127
        old = b'\x04\0'+bytes(range(2, 57))
        after, outcome = migration(old, prior)
        self.assertEqual(outcome, {'success': True, 'error': 0, 'save_requested': True, 'route': 'v4-to-v6'})
        self.assertEqual(after[:57], b'\x06\0'+old[2:])
        self.assertEqual(after[57], 3)
        self.assertEqual(after[58:], b'\xcc'*69)
        self.assertEqual(after[2:26], old[2:26])

    def test_v4_zero_prior_has_explicitly_zero_tail(self):
        after, _ = migration(b'\x04\0'+b'\x12'*55, b'\0'*127)
        self.assertEqual(after[58:], b'\0'*69)

    def test_v5_only_version_low_byte_and_cursor_changed(self):
        plain = bytearray(range(127)); plain[:2] = b'\x05\0'
        after, outcome = migration(bytes(plain), b'\xff'*127)
        changed = [i for i in range(127) if after[i] != plain[i]]
        self.assertEqual(changed, [0, 58]); self.assertTrue(outcome['save_requested'])

    def test_migration_outcome_does_not_require_write_success(self):
        for length, version in ((57, 4), (127, 5)):
            _, outcome = migration(bytes([version, 0])+b'\0'*(length-2), b'\0'*127)
            self.assertTrue(outcome['success']); self.assertTrue(outcome['save_requested'])
            self.assertNotIn('write_succeeded', outcome)

    def test_v6_is_unchanged_no_save(self):
        plain = b'\x06\0'+b'\xa5'*125
        after, outcome = migration(plain, b'\0'*127)
        self.assertEqual(after, plain); self.assertFalse(outcome['save_requested'])
        self.assertTrue(outcome['success'])

    def test_length57_wrong_version_is_error4(self):
        for version in (0, 3, 5, 6, 260):
            _, outcome = migration(version.to_bytes(2, 'little')+b'\0'*55, b'\0'*127)
            self.assertEqual(outcome['error'], 4)
            self.assertFalse(outcome['save_requested'])

    def test_length127_wrong_version_is_error5(self):
        for version in (0, 3, 4, 7, 260):
            _, outcome = migration(version.to_bytes(2, 'little')+b'\0'*125, b'\0'*127)
            self.assertEqual(outcome['error'], 5)

    def test_every_other_bounded_length_rejected4(self):
        for length in range(1, 128):
            if length in (57, 127): continue
            plain = (b'\x04\0'+b'\0'*125)[:length]
            self.assertEqual(migration(plain, b'\0'*127)[1]['error'], 4)

    def test_synthetic_encoded_migration_pipeline(self):
        old = b'\x04\0'+b'\x99'*55
        after, _ = migration(decode_key_zero(oracle_encode(old)), b'\x12'*127)
        self.assertEqual(decode_key_zero(oracle_encode(after)), after)
        self.assertEqual(after[58:], b'\x12'*69)

    def test_reserved_slots_survive_all_named_writers(self):
        initial = b'\xff'*127
        a = write_pet_selection(initial, 1, (True, False, True, False, False), 2)
        a = clear_pet_selection(a, 0)
        a = write_options(a, 1, 2, 3, bytes(range(16)), 4, 5, 6, 7)
        self.assertEqual(a[2:26], initial[2:26]); self.assertEqual(a[59:], initial[59:])

    def test_pet_two_character_five_slot_addressing(self):
        initial = b'\xff'*127
        for character in (0, 1):
            result = write_pet_selection(initial, character, (True, False, True, False, True), 2)
            offset = 26+character*5
            self.assertEqual(result[offset:offset+5], bytes([1, 0, 5, 0, 1]))
            self.assertEqual(result[:offset], initial[:offset]); self.assertEqual(result[offset+5:], initial[offset+5:])

    def test_invalid_character_write_no_change(self):
        initial = b'\xff'*127
        for character in (-1, 2, 99):
            self.assertEqual(write_pet_selection(initial, character, (True,)*5, 0), initial)
            self.assertEqual(clear_pet_selection(initial, character), initial)

    def test_clear_exact_five_slots(self):
        initial = b'\xff'*127
        self.assertEqual(clear_pet_selection(initial, 1), b'\xff'*31+b'\0'*5+b'\xff'*91)

    def test_mail_last_flag_wins_and_unmarked_preserves_prior(self):
        initial = bytearray(127); initial[26:31] = bytes([4, 0, 5, 0, 4])
        self.assertEqual(read_pet_selection(bytes(initial), 0, 2), ((False, False, True, False, False), 4, -1))
        self.assertEqual(read_pet_selection(b'\0'*127, 1, 3), ((False,)*5, 3, -1))

    def test_native_bgm_full_byte_not_source_mute_mask(self):
        a = write_options(b'\0'*127, 255, 255, 255, b'\xfe'*16, 255, 255, 255, 255)
        self.assertEqual(read_options(a)['bgm'], 255)
        self.assertEqual(a[36:59], b'\xff'*3+b'\xfe'*16+b'\xff'*4)

    def test_model_width_guards_not_native_guards(self):
        with self.assertRaises(ValueError): migration(b'\x04\0', b'')
        with self.assertRaises(ValueError): write_options(b'\0'*127, 256, 0, 0, b'\0'*16, 0, 0, 0, 0)

    def test_accepted_evidence(self): validate(self.report())

    def test_native_recursive_recovery_promotion_rejected(self):
        r = self.report(); w = next(x for x in r['probe']['windows'] if x['label'] == 'load-settings')
        w['calls'].append({'direct_target_rva': 0x80760})
        with self.assertRaises(ValueError): validate(r)

    def test_version_and_size_mutations_rejected(self):
        for address in ('0x80825', '0x80859', '0x80864', '0x8089c'):
            r = self.report(); r['probe']['anchors'][address]['operands'][-1]['value'] += 1
            with self.assertRaises(ValueError): validate(r)

    def test_io_error_mutations_rejected(self):
        for address in ('0x80791', '0x807b9', '0x807e7', '0x808a3'):
            r = self.report(); r['probe']['anchors'][address]['operands'][-1]['value'] = 0
            with self.assertRaises(ValueError): validate(r)

    def test_native_and_source_identity_promotions_rejected(self):
        r = self.report(); r['probe']['real_savedata_opened'] = True
        with self.assertRaises(ValueError): validate(r)
        r = self.report(); r['source_profile']['binary_build_identity_verified'] = True
        with self.assertRaises(ValueError): validate(r)

    def test_synthetic_vector_corruption_rejected(self):
        r = self.report(); r['synthetic_vectors'][0]['encoded_hex'] = '0000'
        with self.assertRaises(ValueError): validate(r)

    def test_unchecked_structural_and_source_metadata_drift_rejected(self):
        r = self.report(); r['probe']['windows'][0]['code_sha256'] = '0'*64
        with self.assertRaises(ValueError): validate(r)
        r = self.report(); r['source_profile']['encoder_mutates_source'] = False
        with self.assertRaises(ValueError): validate(r)

    def test_wrong_original_specimen_rejected(self):
        with self.assertRaises(ValueError): probe(b'MZ')
