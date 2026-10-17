import copy
import unittest
from tools.stoneage_historical_site_navigation_probe import TARGETS, qualify
from tools.stoneage_historical_site_navigation_catalog import build


def fixture():
    pages = {k: {'requested_original': v[0], 'status': 'NO_CLOSEST_FOR_THIS_QUERY_NOT_GLOBAL_ABSENCE'} for k, v in TARGETS.items()}
    for key, html, ts in [('jss_manual01', '<html>STONEAGE<a href="manual02.html#7030">ペット</a><a href="missing.html">missing</a></html>', '20010418082314'), ('jss_manual02', '<html>STONEAGE<a name="7030"></a></html>', '20010418083149')]:
        pages[key] = qualify(key, html.encode('shift_jis'), f'https://web.archive.org/web/{ts}id_/{TARGETS[key][0]}')
    return {'schema': 'stoneage.historical_site_navigation.r1', 'targets': pages, 'qualified_pages': 2,
            'historical_site_structure_fully_recovered': False, 'website_implemented': False,
            'original_html_images_or_binaries_retained': False, 'source_absence_established': False}


class CatalogTests(unittest.TestCase):
    def test_cross_page_fragment_is_present_only_in_other_capture(self):
        r = build(fixture()); e = r['links'][0]
        self.assertEqual(e['target_snapshot_candidates'], [{'target_page_id': 'jss_manual02', 'fragment_present_in_acquired_snapshot': True, 'same_capture_timestamp': False}])
        self.assertFalse(e['historical_click_execution_verified'])
        self.assertEqual(r['routing_candidates'][0]['collection_candidate'], 'pets')

    def test_missing_target_is_unresolved_not_nonexistent(self):
        r = build(fixture())
        self.assertEqual(r['links'][1]['target_snapshot_candidates'], [])
        self.assertEqual(r['counts']['unqualified_targets'], len(TARGETS) - 2)
        self.assertFalse(r['linked_game_content_verified'])

    def test_layout_game_scope_and_wrong_target_rejected(self):
        for change in [lambda x: x.__setitem__('source_absence_established', True), lambda x: x['targets']['jss_manual01'].__setitem__('visual_layout_verified', True), lambda x: x['targets']['jss_manual01'].__setitem__('requested_original', TARGETS['jss_manual02'][0]), lambda x: x['targets']['jss_manual01'].__setitem__('replacement_characters', 1)]:
            r = copy.deepcopy(fixture()); change(r)
            with self.assertRaises(ValueError): build(r)

    def test_missing_fragment_and_empty_fragment_are_distinct(self):
        r = fixture(); r['targets']['jss_manual02']['document_anchor_ids'] = []
        self.assertIs(build(r)['links'][0]['target_snapshot_candidates'][0]['fragment_present_in_acquired_snapshot'], False)
        r['targets']['jss_manual01']['links'][0]['target_url'] = TARGETS['jss_manual02'][0]
        self.assertIsNone(build(r)['links'][0]['target_snapshot_candidates'][0]['fragment_present_in_acquired_snapshot'])


if __name__ == '__main__': unittest.main()
