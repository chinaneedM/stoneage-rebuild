"""Negative evidence boundaries for a closed, mixed-capture web catalog."""
from copy import deepcopy
import json
import unittest
from tools import stoneage_waei_cn20_new_pet_pagination as m


class FiniteCatalogTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(m.REPORT.read_bytes())

    def reject(self, change):
        report = deepcopy(self.report); change(report)
        with self.assertRaises((ValueError, AssertionError)):
            m.validate_report(report)

    def test_exact_complete_finite_catalog(self):
        m.validate_report(self.report)
        self.assertEqual(self.report['records'][83]['name_as_written'], '裘里蛙')
        self.assertEqual(self.report['records'][83]['image_reference']['relative_src_as_written'], 'img/newpet/104.JPG')
        self.assertEqual(self.report['records'][-1]['name_as_written'], '朱利洛斯')

    def source_fixture(self):
        rows = []
        records = self.report['records'][80:]
        for start in range(0,24,5):
            cells = []
            for r in records[start:start+5]:
                im = r['image_reference']; dims = im['html_declared_dimensions']
                attr = f' width="{dims[0]}" height="{dims[1]}"' if dims else ''
                cells.append(f'<td><img src="{im["relative_src_as_written"]}"{attr}><br>{r["name_as_written"]}</td>')
            rows.append('<tr>'+''.join(cells)+('</tr>' if start < 20 else ''))
        return ('<title>石器时代2.0</title>新 增 宠 物<table><tr>'
                '<td><a href="new_pet.asp">1-40</a></td> '
                '<td><a href="new_pet1.asp">41-80</a></td> <td>81-104</td></tr></table>'
                '<table>'+''.join(rows)+'</table>')

    def test_parser_preserves_actual_unclosed_four_cell_final_row(self):
        grid = m.parse_page(self.source_fixture(),1)
        self.assertEqual([len(row) for row in grid],[5,5,5,5,4])
        self.assertEqual(grid[-1][-1][0],'朱利洛斯')

    def test_parser_rejects_invented_blank_cell_and_silent_html_repair(self):
        fixture = self.source_fixture()
        for changed in [fixture[:-8]+'<td></td></table>', fixture[:-8]+'</tr></table>']:
            with self.assertRaises((ValueError, AssertionError)):
                m.parse_page(changed,1)

    def test_no_silent_loss_of_unclosed_last_row(self):
        self.reject(lambda o: o['records'].__delitem__(slice(100,104)))

    def test_no_fabricated_105th_position(self):
        self.reject(lambda o: o['records'].append(deepcopy(o['records'][-1])))

    def test_no_filename_based_reordering(self):
        self.reject(lambda o: o['records'][83]['image_reference'].update(relative_src_as_written='img/newpet/84.JPG'))

    def test_no_image_case_normalization(self):
        self.reject(lambda o: o['records'][40]['image_reference'].update(relative_src_as_written='img/newpet/41.jpg'))

    def test_no_backfill_html_dimensions(self):
        self.reject(lambda o: o['records'][40]['image_reference'].update(html_declared_dimensions=[83,90]))

    def test_no_flattening_capture_dates(self):
        self.reject(lambda o: o['new_page_sources'][0].update(actual_capture='20011204194619'))

    def test_no_same_day_or_build_projection(self):
        self.reject(lambda o: o['source_compilation'].update(same_capture_day_or_exact_build_proven=True))

    def test_no_game_id_or_stats_projection(self):
        self.reject(lambda o: o['records'][40].update(original_game_pet_id=41))
        self.reject(lambda o: o['records'][40].update(stats_growth_capture_skill_or_riding_rules={'attack':41}))

    def test_no_new_pixels_or_expanded_recovery(self):
        self.reject(lambda o: o['records'][40]['image_reference'].update(pixels_requested=True))
        self.reject(lambda o: o['coverage'].update(new_image_requests=64))

    def test_no_placeholder_merge_or_rename(self):
        self.reject(lambda o: o['records'][0].update(name_as_written='未知宠物'))
        self.reject(lambda o: o['records'].__setitem__(1,deepcopy(o['records'][0])))

    def test_prior_visual_is_separate_and_not_new_entity(self):
        self.reject(lambda o: o['known_visual_supplement'].update(newly_reacquired=True))
        self.reject(lambda o: o['records'][6]['image_reference'].update(actual_dimensions=[83,90]))

    def test_no_wrong_page_cell_provenance(self):
        self.reject(lambda o: o['records'][80]['source_refs'][0].update(row=9))

    def test_no_census_or_runtime_promotion(self):
        self.reject(lambda o: o['coverage'].update(full_original_game_species_census_proven=True))
        self.reject(lambda o: o['boundaries'].update(stage_b_and_wiki='OPEN'))

    def test_metadata_and_url_byte_pins(self):
        with self.assertRaises((ValueError, AssertionError)):
            m.pinned_metadata(m.PARENT.read_bytes()+b' ', m.VISUAL.read_bytes())
        with self.assertRaises((ValueError, AssertionError)):
            m.build(m.PARENT.read_bytes(), m.VISUAL.read_bytes(), [(b'',m.PAGES[1]['strict_replay_url'])]*2)
        with self.assertRaises((ValueError, AssertionError)):
            m.build(m.PARENT.read_bytes(), m.VISUAL.read_bytes(), [(b'',p['strict_replay_url']) for p in m.PAGES])


if __name__ == '__main__':
    unittest.main()
