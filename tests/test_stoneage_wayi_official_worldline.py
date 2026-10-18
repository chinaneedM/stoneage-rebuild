import copy
import hashlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from PIL import Image
from tools import stoneage_wayi_official_worldline as world
from tools import stoneage_material_review_r4 as review


def fixture():
    tokens = ['遠古機械文明的消失', '傳說', '記憶中消失', '精靈王的出現創造了尼斯大陸(1.0、2.0、2.5)',
              '新的文明', '後來發現的伊甸大陸(3.0、4.0)', '自己的文明', '特有的文化(5.0、7.0)',
              '海底冒險(6.0)', '越是前往海的深處越是覺得冰冷', '冰壁缺口', '不被外界所知',
              '失落的世界(8.0)', '機械文明的遺跡還是另一個全新的文明？', '只能等待冒險者前去探訪才能得知']
    links = ''.join(f'<a href="game01_0{i}.asp">synthetic</a>' for i in range(1, 5))
    images = ''.join(f'<img src="../images/game/pic2_{i}.gif" width="1" height="2">' for i in range(1, 10))
    return '<p>' + ' synthetic '.join(tokens) + '</p>' + links + images


class WorldlineEvidence(unittest.TestCase):
    def test_publisher_group_order_not_sorted_into_chronology(self):
        r = world.world_contract(fixture())
        self.assertEqual([x['versions_as_written'] for x in r['version_groups_in_source_order']],
                         [['1.0', '2.0', '2.5'], ['3.0', '4.0'], ['5.0', '7.0'], ['6.0'], ['8.0']])
        self.assertFalse(r['chronology']['presentation_order_is_numeric_release_order'])
        self.assertFalse(r['chronology']['fictional_calendar_years_given'])

    def test_lost_world_question_is_not_an_answer(self):
        r = world.world_contract(fixture())['lost_world_identity']
        self.assertTrue(r['operator_leaves_question_open'])
        self.assertIsNone(r['chosen_answer'])
        self.assertEqual(len(r['alternatives_as_paraphrase']), 2)

    def test_changed_question_requires_requalification(self):
        with self.assertRaises(ValueError):
            world.world_contract(fixture().replace('機械文明的遺跡還是另一個全新的文明？', 'confirmed ruins'))

    def test_version_group_cannot_move_to_other_continent(self):
        with self.assertRaises(ValueError):
            world.world_contract(fixture().replace('尼斯大陸(1.0、2.0、2.5)', '尼斯大陸(3.0、4.0)'))

    def test_spirit_king_is_not_automatically_npc_or_destroyer(self):
        r = world.world_contract(fixture())
        self.assertIsNone(r['named_figure']['npc_master_id'])
        self.assertFalse(r['mechanical_civilization']['spirit_king_destroyed_it_proven'])
        self.assertIsNone(r['mechanical_civilization']['date'])

    def test_comment_and_script_do_not_supply_missing_story(self):
        for replacement in ('<!-- 遠古機械文明的消失 -->', '<script>遠古機械文明的消失</script>'):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                world.world_contract(fixture().replace('遠古機械文明的消失', replacement))

    def test_duplicate_story_boundary_rejected(self):
        with self.assertRaises(ValueError):
            world.world_contract(fixture() + '<p>遠古機械文明的消失</p>')

    def test_detail_edges_are_real_but_topics_unverified(self):
        r = world.world_contract(fixture())
        self.assertEqual(len(r['detail_links']), 4)
        self.assertTrue(all(not x['queried'] and not x['topic_from_number_assumed'] for x in r['detail_links']))
        with self.assertRaises(ValueError):
            world.world_contract(fixture().replace('game01_01.asp', 'guessed-story.asp'))

    def test_image_html_dimensions_do_not_prove_pixels(self):
        r = world.world_contract(fixture())
        self.assertEqual(len(r['image_slice_references']), 9)
        for row in r['image_slice_references']:
            self.assertFalse(row['pixels_acquired'])
            self.assertIsNone(row['actual_dimensions'])
            self.assertEqual(row['html_width'], '1')

    def test_all_nine_source_slices_required_without_duplicates(self):
        with self.assertRaises(ValueError):
            world.world_contract(fixture().replace('pic2_9.gif', 'pic2_1.gif'))

    def test_late_redirect_and_wrong_bytes_rejected(self):
        for url in ('https://web.archive.org/web/20100101000000id_/' + world.ROOT,
                    'https://web.archive.org/web/20050615023834id_/' + world.ROOT):
            with self.subTest(url=url), self.assertRaises(ValueError):
                world.build({'home': (b'<html>fake</html>', url)})

    def test_per_version_story_is_not_universal_canon(self):
        r = json.loads(Path(world.REPORT).read_text())
        b = r['boundaries']
        for key in ('jss1999_or_tw10_same_build_promoted', 'all_versions_share_one_universal_canon_proven', 'complete_npc_quest_scripts_or_pet_roster_recovered', 'original_release_or_deployment_witnessed', 'original_html_or_assets_retained_in_git'):
            self.assertFalse(b[key])
        self.assertEqual(r['source_count']['newly_acquired_world_intro_pages'], 1)
        self.assertEqual(r['source_count']['reacquired_previously_authenticated_pages'], 1)

    def test_source_slices_have_actual_dimensions_and_later_capture(self):
        r = json.loads(Path(world.REPORT).read_text())
        slices = r['world']['image_slice_references']
        self.assertEqual(sum(x['pixels_acquired'] for x in slices), 8)
        missing = [x for x in slices if not x['pixels_acquired']]
        self.assertEqual(len(missing), 1)
        self.assertTrue(missing[0]['original_url'].endswith('/pic2_9.gif'))
        self.assertFalse(missing[0]['source_absence_established'])
        self.assertTrue(all(x['actual_capture'].startswith('2006') for x in slices if x['pixels_acquired']))
        self.assertFalse(r['visual_summary']['complete_artwork_acquired_or_reconstructed'])
        self.assertFalse(r['visual_summary']['same_instant_as_2005_html_proven'])

    def test_gif_metadata_comes_from_payload_and_rejects_tamper(self):
        output = io.BytesIO()
        Image.new('P', (2, 3)).save(output, format='GIF')
        raw = output.getvalue()
        name = 'pic2_1.gif'
        original = world.ROOT + 'images/game/' + name
        final = 'https://web.archive.org/web/20060105091436id_/' + original
        pin = {'final_url': final, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        with patch.dict(world.IMAGE_PINS, {name: pin}, clear=True):
            row = world.image_contract(raw, final, original)
            self.assertEqual(row['actual_dimensions'], [2, 3])
            with self.assertRaises(ValueError):
                world.image_contract(raw + b'changed', final, original)
            with self.assertRaises(ValueError):
                world.image_contract(raw, final.replace('20060105', '20050614'), original)

    def test_unacquired_slice_cannot_be_promoted_by_filename(self):
        original = world.ROOT + 'images/game/pic2_9.gif'
        with self.assertRaises(ValueError):
            world.image_contract(b'fake', 'https://web.archive.org/web/20060105000000id_/' + original, original)


class PortfolioReview(unittest.TestCase):
    def setUp(self):
        self.prior = json.loads(Path(world.PRIOR).read_text())
        self.archive = json.loads(Path(world.ARCHIVE).read_text())

    def test_all22_old_statuses_and_order_preserved(self):
        r = review.review(self.prior, self.archive)
        self.assertEqual([(x['domain_id'], x['original_order'], x['baseline_evidence_status']) for x in r],
                         [(x['domain_id'], x['original_order'], x['baseline_evidence_status']) for x in self.prior['reviewed_domains']])
        self.assertTrue(all(not x['historical_status_changed'] for x in r))

    def test_missing_domain_is_not_treated_as_completed(self):
        prior = copy.deepcopy(self.prior)
        prior['reviewed_domains'].pop()
        with self.assertRaises(ValueError):
            review.review(prior, self.archive)

    def test_unknown_domain_does_not_silently_get_notes(self):
        prior = copy.deepcopy(self.prior)
        prior['reviewed_domains'][0]['domain_id'] = 'invented_domain'
        with self.assertRaises(ValueError):
            review.review(prior, self.archive)

    def test_profile_classes_and_contexts_not_complete_official_release_census(self):
        r = review.build()
        coverage = r['official_reference_coverage']
        self.assertFalse(coverage['all_official_release_census_complete'])
        self.assertFalse(coverage['contexts_are_distinct_official_release_count'])
        self.assertTrue(coverage['later_official_content_allowed_on_its_own_version_merits'])
        self.assertEqual(r['boundaries']['stage_a_system_families'], {'PARTIAL': 7, 'OPEN': 2})
        self.assertIsNone(r['boundaries']['overall_restoration_percentage'])


if __name__ == '__main__':
    unittest.main()
