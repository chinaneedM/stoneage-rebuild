from collections import Counter
from fractions import Fraction
import json
import unittest

from tools.stoneage_recovery_source import BOUNDARY, REPORT, SOURCE_SCOPE, WORLD30, catalog, sha


class World31RecoverySourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding='utf-8'))

    def test_frozen_scope_and_same_archive_sources(self):
        self.assertEqual(sha(REPORT.read_bytes()), 'f92d0d0be3055ee773d7e1fa846c492613ab05c3ab4e10e80f9260031ad788af')
        self.assertEqual(self.report['scope'], SOURCE_SCOPE)
        self.assertTrue(all(self.report[key] is False for key in BOUNDARY))
        parent = json.loads(WORLD30.read_text(encoding='utf-8'))
        self.assertEqual(self.report['archive_sha256'], parent['archive_sha256'])
        self.assertEqual(self.report['configured_item_source'], 'itemset6file=data/itemset.txt')
        witness = {entry['target']: entry for entry in parent['archive_witness']['members']}
        self.assertEqual(len(self.report['selected_source_members']), 3)
        for entry in self.report['selected_source_members']:
            self.assertEqual(entry, witness[entry['target']])

    def test_catalog_coverage_and_source_field_separation(self):
        source = self.report['catalog']
        self.assertEqual(source['physical_callback_rows'], 644)
        self.assertEqual(source['raw_hash_prefix_ids'], [13031])
        counts = Counter()
        for kind, _scene, _target, count in source['shape_scene_target_counts']:
            counts[kind] += count
        self.assertEqual(counts, {'HP': 389, 'MP': 147, 'HP_MP': 48, 'OTHER': 60})
        rows = {row['id']: row for row in source['sample_rows']}
        self.assertEqual({key: [row['scene'], row['target']] for key, row in rows.items()},
                         {12530: [0, 1], 12500: [0, 1], 12555: [2, 1], 12780: [0, 0], 12754: [0, 1]})
        self.assertEqual(rows[12555]['values'], {'氣': 20, '體': 185})

    def test_original_program_dispatch_edges(self):
        program = self.report['program']
        edges = {edge['address']: edge['target'] for edge in program['edges']}
        self.assertEqual(edges[0x41324c], edges[0x5296bb])
        self.assertEqual(edges[0x50060f], '_ITEM_useRecovery_Battle')
        self.assertEqual(edges[0x500629], '_ITEM_useRecovery_Field')
        self.assertEqual(edges[0x55927c], '_BATTLE_MultiRecovery')
        self.assertEqual(edges[0x5593bb], '__CHAR_DelItem')
        self.assertEqual(program['field_current_hp_mp_keys'], [10, 11])
        self.assertEqual(program['field_max_hp_mp_work_keys'], [13, 14])

    def test_all_replayed_parameters_against_independent_arithmetic(self):
        emulated = self.report['emulated']
        runs = emulated['ordinary_option_replays']
        self.assertEqual(emulated['common_fixture']['x87_control_word'], 0x037f)
        self.assertEqual(len({tuple(map(tuple, row['tokens'])) for row in runs}), 116)
        self.assertEqual(sum(row['source_rows'] for row in runs), 583)
        for run in runs:
            values = dict(run['tokens'])
            hp = values.get('體')
            kind, amount = (0, hp) if hp is not None else (1, values['氣'])
            self.assertEqual(run['battle_request_kind_value_percent'], [kind, amount, 0])
            for rand, key in ((0, 'field_rand_0'), (2**31 - 1, 'field_rand_max')):
                expected = []
                for token, start in (('體', 100), ('氣', 10)):
                    if token in values:
                        amount = values[token]
                        low = amount * 0.9
                        width = amount * 1.1 - low + 1
                        offset = int(Fraction(width) * Fraction(rand, 2**31))
                        expected.append(start + int(Fraction(low) + offset))
                self.assertEqual(run[key], expected)

    def test_boundary_fixture_writes_and_consumption_requests(self):
        fixtures = self.report['emulated']['boundary_fixture_replays']
        for name in ('initializing_battle', 'field_pet_mp_only', 'field_cure_denied',
                     'battle_position_invalid', 'invalid_caster', 'invalid_item'):
            for event in ('changes', 'battle_requests', 'deleted'):
                self.assertEqual(fixtures[name][event], [], (name, event))
        self.assertEqual(fixtures['field_pet_mixed']['changes'], [[9, 10, 266]])
        self.assertEqual(fixtures['field_full_hp_mp']['changes'], [[9, 10, 1000], [9, 11, 100]])
        self.assertEqual(fixtures['field_full_hp_mp']['deleted'], [[8, 7, 1, 0]])
        self.assertEqual(fixtures['field_self_mp']['changes'], [[8, 11, 14]])
        self.assertEqual(fixtures['field_marker_full']['rand_calls'], 0)
        self.assertEqual(fixtures['field_missing_hp_number']['changes'], [[9, 10, 101]])
        self.assertEqual(fixtures['battle_missing_hp_number']['battle_requests'][0][3:6], [0, 0, 0])

    def test_catalog_does_not_promote_partial_or_duplicate_options(self):
        rows = []
        for index, option in enumerate(('氣20體185', '氣2氣3', '體7全', '全'), 1):
            fields = [''] * 94
            fields[0], fields[3], fields[10] = '道具', option, 'ITEM_useRecovery'
            fields[16], fields[20], fields[21] = str(index), '0', '1'
            rows.append(','.join(fields).encode('cp950') + b'\n')
        self.assertEqual([r['shape'] for r in catalog(b''.join(rows))], ['HP_MP', 'OTHER', 'OTHER', 'OTHER'])
