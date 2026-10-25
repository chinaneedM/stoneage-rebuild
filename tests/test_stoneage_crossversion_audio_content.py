import json
import copy
import unittest

from tools import stoneage_crossversion_audio_content as m


def segment(index=0, offset=0, size=20, digest='a'*64):
    return {'tw10_index': index, 'offset': offset, 'bytes': size, 'sha256': digest,
            'tw10_table_name': 'original.wav',
            'wave': {**{k: 1 for k in m.FORMAT}, 'data_sha256': 'b'*64, 'chunk_signature': 'fmt :16,data:1'}}


class AudioContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = m.build()

    def test_complete_report_matches_all_pinned_inputs(self):
        self.assertEqual(self.report, json.loads((m.ROOT/m.OUTPUT).read_bytes()))

    def test_whole_container_sha_and_extent_both_required(self):
        original = {'path': 'old.bin', 'bytes': 20, 'sha256': 'c'*64}
        for change in [{'bytes': 21}, {'sha256': 'd'*64}, {'sha256': ''}, {'sha256': None}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.transfer([segment()], original, {**original, **change})

    def test_container_path_does_not_supply_a_later_runtime_index(self):
        a = {'path': 'sound_1.bin', 'bytes': 20, 'sha256': 'c'*64}
        result = m.transfer([segment()], a, {**a, 'path': 'sound_3.bin'})
        self.assertEqual(result['inherited_byte_span_occurrences'], 1)
        self.assertIsNone(result['later_runtime_indices'])
        self.assertIsNone(result['later_source_filenames'])

    def test_partition_rejects_gaps_overlaps_reordering_bounds_and_tail(self):
        invalid = [([segment(offset=1)], 21), ([segment(), segment(1, 19)], 39),
                   ([segment(1)], 20), ([segment()], 19), ([segment()], 21),
                   ([segment(size=0)], 0)]
        for spans, extent in invalid:
            with self.subTest(spans=spans, extent=extent), self.assertRaises(ValueError):
                m.validate_partition(spans, extent)

    def test_equal_wave_bytes_preserve_distinct_original_spans(self):
        spans = [segment(), segment(1, 20)]
        m.validate_partition(spans, 40)
        r = m.compare_loose({**spans[0], 'path': 'data/se/renamed.wav'}, spans, {})
        self.assertEqual(r['exact_legacy_span_indices'], [0, 1])

    def test_same_pcm_digest_in_different_format_is_not_pcm_equivalence(self):
        s = segment()
        loose = {**s, 'sha256': 'd'*64, 'path': 'data/se/a.wav',
                 'wave': {**s['wave'], 'sample_rate': 22050}}
        result = m.compare_loose(loose, [s], {})
        self.assertEqual(result['relation_to_inherited_sound1'], 'NO_MATCH_IN_LEGACY_CONTAINER_SPANS')

    def test_pcm_identity_compares_every_declared_format_field(self):
        s = segment()
        for field in m.FORMAT:
            loose = {**s, 'sha256': 'd'*64, 'path': 'a.wav', 'wave': {**s['wave'], field: 2}}
            with self.subTest(field=field):
                self.assertFalse(m.compare_loose(loose, [s], {})['matching_pcm_and_format_span_indices'])

    def test_wrapper_only_equivalence_does_not_replace_full_wave_bytes(self):
        s = segment()
        loose = {**s, 'sha256': 'd'*64, 'path': 'a.wav'}
        result = m.compare_loose(loose, [s], {})
        self.assertEqual(result['relation_to_inherited_sound1'], 'EXACT_PCM_AND_FORMAT_ONLY')
        self.assertFalse(result['exact_legacy_span_indices'])
        self.assertEqual(result['matching_pcm_and_format_span_indices'], [0])

    def test_same_path_different_bytes_not_an_exact_file_match(self):
        s = segment()
        result = m.compare_loose({**s, 'path': 'a.wav'}, [s],
                                 {'a.wav': {'bytes': 20, 'sha256': 'f'*64}})
        self.assertTrue(result['original_loose_path_present_in_mixed25'])
        self.assertFalse(result['standalone_exact_file_paths_in_mixed25'])

    def test_full_file_match_requires_size_and_preserves_all_paths(self):
        s = segment()
        files = {'x': {'bytes': 20, 'sha256': s['sha256']},
                 'y': {'bytes': 20, 'sha256': s['sha256']},
                 'z': {'bytes': 21, 'sha256': s['sha256']}}
        result = m.compare_loose({**s, 'path': 'a.wav'}, [s], files)
        self.assertEqual(result['standalone_exact_file_paths_in_mixed25'], ['x', 'y'])

    def test_inventory_scope_ignores_helper_server_and_pre_hash_strings(self):
        root = m.CLIENT_ROOT
        text = f'x{root}data/sound_1.bin|20\n'+'c'*64+f'  /old{root}unqualified.bin\nALL-FILE SHA256\n'+'a'*64+f'  /tmp{root}data/sound_1.bin\n'+'b'*64+'  /server/data/sound_1.bin\n'
        self.assertEqual(list(m.bridge_files(text)), ['data/sound_1.bin'])

    def test_inventory_missing_size_hash_or_duplicate_path_rejected(self):
        root = m.CLIENT_ROOT
        valid = f'x{root}a|20\nALL-FILE SHA256\n'+'a'*64+f'  /tmp{root}a\n'
        cases = [valid.replace(f'x{root}a|20\n', ''), valid.replace('a'*64, 'bad'),
                 valid+f'x{root}a|20\n', valid+'a'*64+f'  /tmp{root}a\n']
        for text in cases:
            with self.subTest(text=text), self.assertRaises(ValueError):
                m.bridge_files(text)

    def test_actual_original_114_occurrences_and_duplicate_109_113_preserved(self):
        self.assertEqual(len(self.report['legacy_byte_spans']), 114)
        self.assertEqual(self.report['summary']['distinct_full_wave_blocks'], 113)
        self.assertEqual(self.report['duplicate_legacy_wave_blocks'][0]['tw10_indices'], [109, 113])

    def test_actual_loose_sfx_conservation_distinguishes_109_1_6(self):
        self.assertEqual(self.report['summary']['loose_sfx_relations'], {
            'EXACT_FULL_WAVE_BYTES': 109, 'EXACT_PCM_AND_FORMAT_ONLY': 1,
            'NO_MATCH_IN_LEGACY_CONTAINER_SPANS': 6})
        rows = {r['path']: r for r in self.report['original_loose_sfx_comparison']}
        self.assertEqual(rows['data/se/sak_91.wav']['exact_legacy_span_indices'], [37])
        self.assertEqual(rows['data/se/sak_92.wav']['exact_legacy_span_indices'], [38])
        self.assertFalse(rows['data/se/sak_01.wav']['exact_legacy_span_indices'])

    def test_actual_wrapper_case45_not_equal_complete_file(self):
        r = next(r for r in self.report['original_loose_sfx_comparison'] if r['path'].endswith('/sak_09a.wav'))
        self.assertEqual(r['matching_pcm_and_format_span_indices'], [45])
        self.assertFalse(r['exact_legacy_span_indices'])

    def test_actual_alternate_container_and_table_have_no_decoded_selector(self):
        audio = {r['path']: r for r in self.report['scope']['mixed25_audio_named_files']}
        self.assertEqual(audio['data/sound_3.bin']['bytes'], 898978)
        self.assertEqual(audio['data/soundaddr_3.txt']['bytes'], 691)
        missing = self.report['precise_missing_evidence']
        self.assertFalse(missing['soundaddr_1_file_in_mixed25'])
        self.assertTrue(missing['soundaddr_3_complete_numeric_rows_retained_in_permanent_metadata'])
        self.assertIsNone(missing['mixed25_effective_sound_selector'])

    def test_bgm_remains_a_separate_original_surface_not_synthetic_indices(self):
        rows = self.report['original_bgm_comparison']
        self.assertEqual(len(rows), 11)
        self.assertTrue(all(not r['exact_legacy_span_indices'] for r in rows))
        self.assertEqual(self.report['summary']['standalone_tw10_bgm_files_exactly_matched_in_client_subtree'], 0)

    def test_reference_budget_is_not_actual_original_disk_reclamation(self):
        b = self.report['summary']['same_container_span_reference_budget']
        self.assertEqual(b['two_specimen_references'], 228)
        self.assertEqual(b['logical_segment_bytes'], b['distinct_segment_bytes']+b['repeated_reference_bytes'])
        self.assertEqual(b['actual_original_bytes_deleted'], 0)

    def test_no_source_runtime_or_entity_promotion(self):
        b = self.report['boundaries']
        self.assertTrue(b['bounded_source_prefix_newly_downloaded'])
        self.assertFalse(b['full_client_or_full_cab_newly_downloaded'])
        self.assertFalse(b['tw10_indices_or_names_promoted_to_later_runtime'])
        self.assertFalse(b['old_loose_paths_absent_means_audio_deleted'])
        self.assertEqual(b['new_named_gameplay_audio_events'], 0)
        self.assertIsNone(b['overall_restoration_percentage'])

    def test_original_sound3_triple_copy_is_81_positions_not_81_new_sounds(self):
        s3 = self.report['sound3_original_content']
        original = s3['original_source_metadata']
        self.assertEqual(original['physical_record_occurrences'], 81)
        self.assertEqual(original['distinct_full_wave_blocks'], 26)
        self.assertEqual(original['duplicate_table_wave_groups'][0]['table_indices'], [14, 15])
        self.assertEqual([b['physical_wave_span_occurrences'] for b in s3['specimen_bindings']], [27, 81, 81])
        self.assertTrue(all(b['table_addresses_first_copy_only'] for b in s3['specimen_bindings']))

    def test_original_sound3_no_full_wave_or_format_pcm_match_to_tw10(self):
        for row in self.report['sound3_original_content']['comparison_to_tw10_surfaces']:
            for field in ['exact_tw10_indexed_matches', 'pcm_format_tw10_indexed_matches',
                          'exact_tw10_loose_sfx_or_bgm_paths', 'pcm_format_tw10_loose_sfx_or_bgm_paths']:
                self.assertFalse(row[field])

    def test_table_or_carrier_hash_change_blocks_cross_specimen_transfer(self):
        files = m.bridge_files((m.ROOT/m.BRIDGE).read_text())
        cn = json.loads((m.ROOT/m.CN50).read_bytes())
        tw = json.loads((m.ROOT/m.TW85).read_bytes())
        original = self.report['sound3_original_content']['original_source_metadata']
        for path in ['data/sound_3.bin', 'data/soundaddr_3.txt']:
            for field, replacement in [('sha256', '0'*64), ('bytes', 1)]:
                changed = copy.deepcopy(files);changed[path][field] = replacement
                with self.subTest(path=path, field=field), self.assertRaises(ValueError):
                    m.sound3_binding(original, changed, cn, tw, self.report['legacy_byte_spans'], [], [])


if __name__ == '__main__':
    unittest.main()
