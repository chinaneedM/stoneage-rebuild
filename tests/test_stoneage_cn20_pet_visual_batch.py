import copy
import json
import unittest
from tools import stoneage_cn20_pet_visual_batch as m


class PetVisualBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(m.REPORT.read_text())
        cls.local = json.loads((m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r); node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            m.validate(r)

    def test_four_source_positions_match_three_immutable_parent_reports(self):
        m.validate(self.r)
        self.assertEqual([x['ordinal'] for x in self.r['extracted']['selected_cells']], [1, 4, 7, 40])
        self.reject(['parents', 0, 'sha256'], '0' * 64)
        self.reject(['records', 0, 'source_cell', 'ordinal'], 6)

    def test_two_placeholder_labels_are_not_named_by_picture(self):
        a, b = self.r['extracted']['selected_cells'][:2]
        self.assertEqual([a['display_label_as_written'], b['display_label_as_written']], ['???', '??2'])
        self.assertIsNone(a['name_as_written']); self.assertIsNone(b['name_as_written'])
        self.reject(['records', 0, 'source_cell', 'name_as_written'], '绿暴龙')
        self.reject(['extracted', 'selected_cells', 1, 'label_status'], 'NAMED_ON_WEB_PAGE')

    def test_known_amiduo_is_control_and_hubobo_is_new_reference(self):
        self.assertEqual([x['ordinal'] for x in self.r['records']], [1, 4, 40])
        self.assertEqual(self.r['extracted']['selected_cells'][-1]['name_as_written'], '呼波波')
        self.assertEqual(self.r['images'][2]['bytes'], 4831)
        self.reject(['coverage', 'new_image_references_acquired'], 4)
        self.reject(['coverage', 'previously_acquired_replayed_control'], 0)

    def test_source_case_host_and_separate_capture_dates_preserved(self):
        cells = self.r['extracted']['selected_cells']; images = self.r['images']
        self.assertEqual(cells[1]['relative_src_as_written'], 'img/newpet/2.jpg')
        self.assertIn('http://waei.com.cn/', images[1]['strict_replay_url'])
        self.assertEqual([x['actual_capture_timestamp'] for x in images], ['20011205050022', '20011023194345', '20011205051046', '20011023183116'])
        self.reject(['images', 1, 'strict_replay_url'], images[1]['strict_replay_url'].replace('2.jpg', '2.JPG'))
        self.reject(['extracted', 'exact_client_build'], '1.82')

    def test_measured_dimensions_not_backfilled_into_html(self):
        cells = self.r['extracted']['selected_cells']
        self.assertEqual([x['html_declared_dimensions'] for x in cells], [[83, 90], [83, 90], None, None])
        self.assertTrue(all(x['metadata']['dimensions'] == [83, 90] for x in self.r['images']))
        self.reject(['extracted', 'selected_cells', 3, 'html_declared_dimensions'], [83, 90])
        self.reject(['images', 0, 'metadata', 'dimensions'], [640, 480])

    def test_full_jpeg_decode_does_not_prove_animation_or_native_model(self):
        self.assertTrue(all(x['metadata']['format'] == 'JPEG' and x['metadata']['full_pixels_decoded'] and x['metadata']['frames_in_this_file'] == 1 for x in self.r['images']))
        self.reject(['records', 2, 'original_game_pet_id_stats_alias_or_animation'], {'species_id': 40})
        self.reject(['records', 2, 'new_original_game_entity'], True)
        self.reject(['records', 2, 'version_profile'], 'TW10')

    def test_manual_observations_and_initial_redirect_are_separate_from_ci(self):
        for im in self.r['images']:
            self.assertEqual(im['manual_inspection']['exact_image_sha256'], im['sha256'])
            self.assertFalse(im['manual_inspection']['ci_repeats_human_inspection'])
            self.assertFalse(im['ci_repeats_initial_redirect'])
        self.reject(['images', 0, 'manual_inspection', 'ci_repeats_human_inspection'], True)
        self.reject(['images', 0, 'manual_inspection', 'exact_image_sha256'], '0' * 64)

    def test_fourteen_real_html_and_four_image_byte_mutations(self):
        audit = self.local['audit']; html = audit['real_html_mutations']; images = audit['real_image_byte_mutations']
        self.assertEqual(len(html), 14); self.assertEqual(len(images), 4)
        self.assertEqual(len({x['input_sha256'] for x in html}), 14)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in html))
        self.assertTrue(all(x['exact_byte_mutation_rejected'] for x in images))
        self.assertTrue(audit['outer_script_positive'])

    def test_aggregate_counts_are_reference_coverage_not_species_census(self):
        self.assertEqual(self.r['coverage']['acquired_disjoint_references_after_supplement'], 4)
        self.assertEqual(self.r['coverage']['remaining_image_references_without_acquired_pixels'], 100)
        self.assertEqual(self.r['coverage']['newly_resolved_names'], 0)
        self.reject(['coverage', 'new_original_game_entities'], 3)
        self.reject(['coverage', 'unresolved_placeholders_still'], 4)
        self.reject(['coverage', 'parent_historical_reports_rewritten'], True)

    def test_unproven_boundaries_and_production_gates_preserved(self):
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'FETCH_ALL_REMAINING_100_IMAGES')

    def test_permanent_receipt_required_and_actual_dual_replays_pinned(self):
        p = m.ROOT / ('research/recovered/' + m.STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted source material requires permanent custody')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.cn20_pet_visual_batch.custody.r1')
        self.assertEqual(len(r['source_pins']), 13)
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['source_pins'] + r['startup_prefixes']:
            b = (m.ROOT / pin['path']).read_bytes()
            if pin in r['startup_prefixes']:
                b = b[:pin['bytes']]
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(m.sha(b), pin['sha256'])
            self.assertEqual(m.git_blob(b), pin['git_blob'])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['status'] == 'completed' and x['conclusion'] == 'success' and x['head_sha'] == r['content_head'] for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertEqual(meta['actual_unit_tests'], 10)
            self.assertEqual(meta['skipped_tests'], 0)
            self.assertEqual(meta['head'], r['content_head'])
            self.assertEqual(meta['tree'], r['content_tree'])
            self.assertEqual(meta['actual_html_bytes'], 69317)
            self.assertEqual(meta['actual_jpeg_bytes'], [4196, 3785, 4831, 3520])
            self.assertEqual((meta['new_visual_references'], meta['known_control_replayed'], meta['fully_decoded_images']), (3, 1, 4))
            self.assertEqual((meta['real_html_semantic_mutations'], meta['real_image_byte_mutations']), (14, 4))
            self.assertTrue(meta['outer_script_positive'] and meta['all_applicable_workflows_success'])
            self.assertFalse(meta['human_inspection_repeated_by_ci'])
            self.assertFalse(meta['initial_image_redirects_repeated_by_ci'])
            self.assertEqual(meta['zip_entry_names'], ['replay.json'])
            b = (m.ROOT / meta['derived_git_path']).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(m.sha(b), meta['raw_sha256'])
            self.assertEqual(m.git_blob(b), meta['raw_git_blob'])
            copies.append(b)
            branch = 'main' if label == 'main' else 'agent/cn20-pet-visual-r52-20261021'
            runs = [x for x in r['workflow_runs'] if x['head_branch'] == branch]
            self.assertEqual(len(runs), meta['own_workflow_count'])
            self.assertEqual(meta['own_workflow_count'], 11 if label == 'main' else 10)
            self.assertIn(meta['run_id'], [x['id'] for x in runs])
        for k in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][k], r['main'][k])
        self.assertEqual(copies[0], copies[1])
        self.assertEqual(copies[0], (m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_bytes())
        self.assertTrue(r['independent_checks']['same_length_same_geometry_wrong_jpeg_rejected_by_exact_sha'])
        self.assertTrue(all(x is False for x in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
