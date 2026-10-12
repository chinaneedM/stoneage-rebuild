"""Synthetic lifecycle/error traces, independent byte masks and metadata gates."""
import itertools
import json
from pathlib import Path
import unittest

from tools.stoneage_wayi_savedata_lifecycle import (initial_region,
 complemented_backing, create_projection, save_projection, load_projection,
 preamble_projection, validate, probe, settings_factory)
from tools.stoneage_wayi_savedata import encode_key_zero


class LifecycleTests(unittest.TestCase):
    def factory(self): return settings_factory(1, 25, 75, bytes(range(16)))
    def report(self):
        return json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-WAYI-SAVEDATA-LIFECYCLE-R1.json').read_text())

    def test_declared_unbacked_region_is_zero(self):
        sec = {'vaddr': 10, 'vsize': 200, 'raw_ptr': 0, 'raw_size': 3}
        self.assertEqual(initial_region(b'ABC', sec, 20, 127), b'\0'*127)

    def test_region_straddles_raw_and_virtual_without_fake_offset_read(self):
        sec = {'vaddr': 10, 'vsize': 200, 'raw_ptr': 2, 'raw_size': 3}
        self.assertEqual(initial_region(b'xxABCSECRET', sec, 12, 5), b'C'+b'\0'*4)

    def test_fully_raw_backed_region(self):
        sec = {'vaddr': 10, 'vsize': 5, 'raw_ptr': 2, 'raw_size': 5}
        self.assertEqual(initial_region(b'xxABCDE', sec, 11, 3), b'BCD')

    def test_invalid_virtual_range_and_short_raw_file(self):
        sec = {'vaddr': 10, 'vsize': 5, 'raw_ptr': 2, 'raw_size': 5}
        for rva, length in ((9, 2), (14, 2), (10, 128), (10, 0)):
            with self.assertRaises(ValueError): initial_region(b'xxABCDE', sec, rva, length)
        with self.assertRaises(ValueError): initial_region(b'', sec, 10, 2)

    def test_factory_source_mutation_independent_mask_period(self):
        plain = self.factory()
        period = bytes([255, 0, 255, 0, 255, 255, 255, 0, 255, 0])
        expected = bytes(a ^ period[i % 10] for i, a in enumerate(plain))
        self.assertEqual(complemented_backing(plain), expected)
        self.assertEqual(complemented_backing(expected), plain)

    def test_constructor_version_is249_after_encoding(self):
        after, encoded, result = create_projection(self.factory())
        self.assertEqual(after[:2], b'\xf9\0')
        self.assertEqual(encoded, encode_key_zero(self.factory()))
        self.assertTrue(result['success'])

    def test_constructor_open_failure_still_mutates(self):
        after, _, result = create_projection(self.factory(), False)
        self.assertEqual(after, complemented_backing(self.factory()))
        self.assertFalse(result['write_attempted']); self.assertFalse(result['success'])

    def test_constructor_partial_write_no_close_and_mutates(self):
        for written in range(128):
            after, _, result = create_projection(self.factory(), True, written)
            self.assertEqual(after, complemented_backing(self.factory()))
            self.assertFalse(result['success']); self.assertFalse(result['close_attempted'])

    def test_constructor_full_write_attempts_close(self):
        _, _, result = create_projection(self.factory(), True, 128)
        self.assertEqual(result, {'success': True, 'open_attempted': True, 'write_attempted': True, 'close_attempted': True})

    def test_save_stack_copy_preserves_every_backing_byte(self):
        backing = bytes(range(127))
        for opened, written in itertools.product((True, False), (0, 1, 127, 128)):
            after, encoded, _ = save_projection(backing, opened, written)
            self.assertEqual(after, backing); self.assertEqual(encoded, encode_key_zero(backing))

    def test_short_save_write_does_not_close(self):
        for written in range(128):
            self.assertFalse(save_projection(self.factory(), True, written)[2]['close_attempted'])

    def test_close_attempt_is_not_close_success_claim(self):
        result = save_projection(self.factory())[2]
        self.assertTrue(result['success']); self.assertNotIn('close_succeeded', result)

    def test_successful_missing_file_create_reopen_decode_restores_plain(self):
        after, result = load_projection(b'\xff'*127, None, self.factory())
        self.assertEqual(after, self.factory()); self.assertTrue(result['success'])
        self.assertEqual(result['trace'], ['error=0', 'open-existing', 'create', 'reopen', 'read', 'close-read', 'decode'])

    def test_missing_create_open_failure_error1_encoded_backing(self):
        after, result = load_projection(b'\0'*127, None, self.factory(), create_io=(False, 0))
        self.assertEqual(after, complemented_backing(self.factory())); self.assertEqual(result['error'], 1)
        self.assertNotIn('reopen', result['trace'])

    def test_missing_create_short_write_error1_no_close(self):
        after, result = load_projection(b'\0'*127, None, self.factory(), create_io=(True, 127))
        self.assertEqual(result['error'], 1); self.assertFalse(result['creation']['close_attempted'])
        self.assertEqual(after[:2], b'\xf9\0')

    def test_reopen_failure_error2_keeps_constructor_mutation(self):
        after, result = load_projection(b'\0'*127, None, self.factory(), reopen=False)
        self.assertEqual(result['error'], 2); self.assertEqual(after, complemented_backing(self.factory()))
        self.assertNotIn('decode', result['trace'])

    def test_created_file_read_error3_keeps_encoded_backing(self):
        after, result = load_projection(b'\0'*127, None, self.factory(), read_error=True)
        self.assertEqual(result['error'], 3); self.assertEqual(after, complemented_backing(self.factory()))
        self.assertIn('close-read', result['trace'])

    def test_existing_file_read_error_keeps_prior_and_closes(self):
        prior = b'\x44'*127
        after, result = load_projection(prior, encode_key_zero(self.factory()), self.factory(), read_error=True)
        self.assertEqual(after, prior); self.assertEqual(result['error'], 3)
        self.assertEqual(result['trace'][-1], 'close-read')

    def test_v4_all_migration_write_outcomes_return_success(self):
        encoded = encode_key_zero(b'\x04\0'+b'\x41'*55)
        for io in itertools.product((True, False), (0, 127, 128)):
            after, result = load_projection(b'\xcc'*127, encoded, self.factory(), migration_io=io)
            self.assertTrue(result['success']); self.assertEqual(result['error'], 0)
            self.assertEqual(result['write']['success'], io == (True, 128))
            self.assertEqual(after[58:], b'\xcc'*69)
            self.assertEqual(result['trace'][-1], 'call-full-save')

    def test_v5_migration_failure_still_applies_cursor(self):
        old = b'\x05\0'+b'\x80'*125
        after, result = load_projection(b'\0'*127, encode_key_zero(old), self.factory(), migration_io=(False, 0))
        self.assertTrue(result['success']); self.assertFalse(result['write']['success'])
        self.assertEqual(after[:2], b'\x06\0'); self.assertEqual(after[58], 0)

    def test_invalid_file_uses_no_delete_or_recreate(self):
        for plain, error in ((b'\x06\0'+b'\0'*55, 4), (b'\x07\0'+b'\0'*125, 5)):
            _, result = load_projection(b'\0'*127, encode_key_zero(plain), self.factory())
            self.assertEqual(result['error'], error); self.assertFalse(result['success'])
            self.assertNotIn('create', result['trace']); self.assertNotIn('call-full-save', result['trace'])

    def test_retry_v4_after_failed_create_retains_complemented_tail(self):
        prior, _ = load_projection(b'\0'*127, None, self.factory(), create_io=(False, 0))
        old = b'\x04\0'+b'\x22'*55
        after, result = load_projection(prior, encode_key_zero(old), self.factory())
        self.assertTrue(result['success']); self.assertEqual(after[58:], prior[58:])
        self.assertNotEqual(after[59:], b'\0'*68)

    def test_current_version_no_migration_call(self):
        after, result = load_projection(b'\0'*127, encode_key_zero(self.factory()), self.factory())
        self.assertEqual(after, self.factory()); self.assertNotIn('call-full-save', result['trace'])

    def test_all_boolean_preamble_gates_pure_event_order(self):
        for gates in itertools.product((False, True), repeat=5):
            events = preamble_projection(*gates)
            self.assertEqual(events[-1], 'settings-body')
            self.assertEqual('reset-pending-id' in events, gates[0])
            self.assertEqual('OpenProcess' in events, all(gates[:4]))
            self.assertEqual('TerminateProcess' in events, all(gates))
            if all(gates):
                self.assertLess(events.index('TerminateProcess'), events.index('CloseHandle'))
                self.assertLess(events.index('CloseHandle'), events.index('settings-body'))

    def test_zero_pending_process_id_skips_every_external_event(self):
        self.assertEqual(preamble_projection(False, True, True, True, True), ['settings-body'])

    def test_enumeration_failure_resets_and_still_reaches_body(self):
        self.assertEqual(preamble_projection(True, False, True, True, True), ['enumeration', 'reset-pending-id', 'settings-body'])

    def test_no_boolean_gate_accepts_real_pid_or_command(self):
        with self.assertRaises(ValueError): preamble_projection(12345, True, True, True, True)

    def test_native_malformed_decode_remains_excluded(self):
        for encoded in (b'', b'\0', b'\0'*129):
            with self.assertRaises(ValueError): load_projection(b'\0'*127, encoded, self.factory())

    def test_acceptance_ledger(self): validate(self.report())

    def test_loader_zero_promotion_mutation(self):
        r = self.report(); r['probe']['initial_region']['declared_zero_filled'] = False
        with self.assertRaises(ValueError): validate(r)

    def test_indirect_closure_or_execution_promotion_rejected(self):
        for key in ('all_indirect_writers_closed', 'process_api_called', 'authentic_publisher_hash_verified'):
            r = self.report(); r['probe'][key] = True
            with self.assertRaises(ValueError): validate(r)

    def test_call_edge_import_and_sweep_drift_rejected(self):
        r = self.report(); r['probe']['direct_control_edges'].pop()
        with self.assertRaises(ValueError): validate(r)
        r = self.report(); r['probe']['process_imports']['0xa01bc'][1] = 'Sleep'
        with self.assertRaises(ValueError): validate(r)
        r = self.report(); r['probe']['linear_sweep_skipped_bytes'] = 0
        with self.assertRaises(ValueError): validate(r)

    def test_source_unconditional_setup_promotion_rejected(self):
        r = self.report(); r['source_profile']['main_parent_setup_conditional_macro'] = None
        with self.assertRaises(ValueError): validate(r)

    def test_wrong_original_specimen_rejected(self):
        with self.assertRaises(ValueError): probe(b'MZ')
