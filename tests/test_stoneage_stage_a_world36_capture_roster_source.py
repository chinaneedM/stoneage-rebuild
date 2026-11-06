"""Check the mixed25 roster receipt without the private GMSV image."""

import json
import unittest

from tools.stoneage_capture_roster_source import (
    CODE, FIELDS, REPORT, SUCCESS_END, FAILURE_END, SYMBOLS, WORLD35,
)


class CaptureRosterSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.cases = {name: case['trace'] for name, case in cls.report['cases'].items()}

    def test_archive_identity_source_windows_and_template(self):
        previous = json.loads(WORLD35.read_bytes())
        self.assertEqual(self.report['archive_sha256'], previous['archive_sha256'])
        member, = [entry for entry in previous['source_members'] if entry['target'] == 'gmsv/gmsv.exe']
        self.assertEqual(self.report['source_member'], member)
        self.assertEqual(self.report['symbols'], SYMBOLS)
        self.assertEqual([tuple(w[:2]) for w in self.report['code_windows']], list(CODE))
        for _, _, sha in self.report['code_windows'] + self.report['data_windows']:
            self.assertRegex(sha, r'^[0-9a-f]{64}$')
        self.assertEqual(self.report['default_template'], {
            'requested_key': 31010, 'table_count': 53, 'matching_entries': 0, 'fallback_address': 0x570dc0,
        })

    def test_first_roster_hole_is_distinct_from_first_free_character_index(self):
        trace = self.cases['two_roster_holes']
        self.assertEqual(trace['roster_before'], [3, 4, -1, 6, -1])
        self.assertEqual(trace['roster_after'], [3, 4, 5, 6, -1])
        self.assertEqual(trace['staged']['slot'], 2)
        self.assertEqual(trace['created_character'], 5)
        self.assertEqual(trace['changed_character_records'], [1, 5])
        self.assertEqual(trace['allocator_partition_start_cursor_end'], [3, 6, 12])
        self.assertEqual(trace['allocation_sequence_after'], 901)
        self.assertEqual(trace['pet']['allocation_sequence'], 900)
        self.assertEqual(trace['staged']['sha256'], '675f01c8c589493e13eb5e923499b5880b912c82d74155c2a4d2d9bfae5ea454')

    def test_owner_and_status_requests_follow_allocation(self):
        for case, pet, slot in (
            ('two_roster_holes', 5, 2), ('last_roster_slot_and_serial_wrap', 7, 4),
            ('low_hp_mp_retained', 5, 2),
        ):
            trace = self.cases[case]
            with self.subTest(case=case):
                self.assertEqual((trace['endpoint'], trace['result_flag'], trace['created_character']),
                                 (SUCCESS_END, 1, pet))
                self.assertEqual(trace['roster_after'][slot], pet)
                self.assertEqual(trace['events'][-6:], [
                    ['work_write', pet, 83, 1], ['attach', 1, slot, pet],
                    ['owner_string_write', pet, 3, 'OwnerAccount'],
                    ['owner_string_write', pet, 4, 'OwnerName'],
                    ['status_request', 1, f'K{slot}'], ['status_request', 1, f'W{slot}'],
                ])
                self.assertEqual(trace['pet']['owner_work_83'], 1)
                self.assertEqual(trace['pet']['owner_account'], 'OwnerAccount')
                self.assertEqual(trace['pet']['owner_name'], 'OwnerName')
                self.assertEqual(trace['pet']['callback_pointers'], [[5, 0x470f20], [8, 0x470740]])

    def test_transfer_retains_skills_and_normalizes_hp_mp(self):
        for name, level, source, final in (
            ('two_roster_holes', 1008, [1010, 1011], [70, 1000]),
            ('low_hp_mp_retained', 35, [25, 20], [25, 20]),
        ):
            trace = self.cases[name]
            pet = trace['pet']
            self.assertEqual(pet['type'], 3)
            self.assertEqual(pet['pet_name'], 'SourcePet')
            self.assertEqual(pet['skill_slots'], [101, 102, -1, 104, -1, 106, 107])
            self.assertIn(['compliance_before', 5, *source], trace['events'])
            self.assertIn(['compliance_after', 5, *final, 70, 1000], trace['events'])
            expected = {key: 1000 + key for key in FIELDS}
            expected.update({8: level, 10: final[0], 11: final[1], 28: level, 58: 0})
            self.assertEqual(dict(pet['fields']), expected)
            self.assertEqual(self.report['fixture']['source_int_key_58'], 98765)

    def test_pet_serial_counter_wrap(self):
        ordinary = self.cases['two_roster_holes']
        boundary = self.cases['last_roster_slot_and_serial_wrap']
        self.assertEqual((ordinary['pet']['pet_serial'], ordinary['serial_counter_after']),
                         ('123456789i241', 42))
        self.assertEqual((boundary['pet']['pet_serial'], boundary['serial_counter_after']),
                         ('123456789i2999', 0))

    def test_comparison_full_roster_and_exhaustion_stop_at_different_points(self):
        for name, points, phase, changed in (
            ('comparison_equal', 1.0, 'work_write', []),
            ('full_roster', 2.0, 'find_carried_slot', [1]),
            ('exhausted_pet_partition', 2.0, 'allocate', [1]),
        ):
            trace = self.cases[name]
            with self.subTest(case=name):
                self.assertEqual((trace['endpoint'], trace['result_flag'], trace['created_character']),
                                 (FAILURE_END, 0, -1))
                self.assertEqual(trace['score'], points)
                self.assertEqual(trace['events'][-1][0], phase)
                self.assertEqual(trace['changed_character_records'], changed)
                self.assertEqual(trace['roster_after'], trace['roster_before'])
                self.assertEqual(trace['allocation_sequence_after'], 900)
                self.assertEqual(trace['serial_counter_after'], 41)
                self.assertNotIn('pet', trace)

    def test_source_and_evidence_boundaries(self):
        for trace in self.cases.values():
            self.assertEqual(trace['events'][0], ['work_write', 1, 32, 0])
            self.assertEqual((trace['roll'], trace['modifier_after']), (1, 0))
            self.assertIs(trace['wild_record_unchanged'], True)
        self.assertIs(self.report['parameter_compliance_executed'], True)
        for flag in ('original_process_started', 'network_messages_delivered',
                     'battle_removal_or_save_executed', 'historical_official_deployment_verified'):
            self.assertIs(self.report[flag], False)
