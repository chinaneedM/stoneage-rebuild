import copy
import json
import unittest
from pathlib import Path
from tools import stoneage_jp2004_named_village_r105 as s

def contract():
    return json.loads(s.SOURCE.read_bytes())

def index(rows=None):
    rows = contract()['operator_rows'] if rows is None else rows
    return ('<table>' + ''.join('<tr><td>' + r['date'] + '</td><td><a href="' + r['href'] + '">' + r['title'] + '</a></td></tr>' for r in rows) + '</table>').encode('cp932')

def press():
    d = contract()
    return ('<table><td>■ ストーンエイジ 運営元 <a href="http://www.bothtec.co.jp/">ボーステック</a> 開発元 Digi Park <a href="http://stoneage.to/">http://stoneage.to/</a> 11月9日にアップデートを実施。' + ''.join('・' + x + '<br>' for x in d['press_bullets']) + '<a href="http://stoneage.to/">http://stoneage.to/</a></td></table>').encode()

class NamedVillage(unittest.TestCase):
    def test_four_same_row_operator_date_title_links(self):
        self.assertEqual(s.operator_rows(index(), contract()['operator_rows']), contract()['operator_rows'])

    def test_title_date_or_destination_swaps_rejected(self):
        expected = contract()['operator_rows']
        for field in ('date', 'title', 'href'):
            rows = copy.deepcopy(expected)
            rows[1][field], rows[2][field] = rows[2][field], rows[1][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                s.operator_rows(index(rows), expected)

    def test_hidden_and_duplicate_operator_entries_rejected(self):
        raw = index().decode('cp932')
        for body in ('<script>' + raw + '</script>', '<div hidden>' + raw + '</div>', '<div style="display: none">' + raw + '</div>', raw + raw):
            with self.assertRaises(ValueError):
                s.operator_rows(body.encode('cp932'), contract()['operator_rows'])

    def test_press_scope_capacity_and_attribution(self):
        d = contract()
        result = s.press(press(), d['press_bullets'])
        self.assertEqual(result['reported_update_date'], '2004-11-09')
        for a, b in [('8人', '9人'), ('ボーステック', '他社'), ('■ ストーンエイジ', '■ 別のゲーム'), ('11月9日', '11月8日')]:
            with self.subTest(value=a), self.assertRaises(ValueError):
                s.press(press().replace(a.encode(), b.encode()), d['press_bullets'])

    def test_sibling_game_or_hidden_claim_cannot_supply_bus(self):
        d = contract()
        fake = press().decode().replace('■ ストーンエイジ', '■ 別のゲーム')
        removed = press().decode().replace('マンモスバスが8人乗りになる', '')
        for body in (fake + removed, '<script>' + press().decode() + '</script>' + removed):
            with self.assertRaises(ValueError):
                s.press(body.encode(), d['press_bullets'])

    def test_contract_native_or_runtime_promotion_rejected(self):
        d = contract()
        s.validate(d)
        for key, value in [('game_ids', 1000), ('coordinates', [1, 2]), ('runtime_verified', True)]:
            altered = copy.deepcopy(d)
            altered['records'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                s.validate(altered)
        self.assertIsNone(d['interpretation']['previous_bus_capacity'])
        self.assertIsNone(d['interpretation']['specific_facility_names_or_transactions'])
        self.assertFalse(d['gaps']['patch_and_result_bodies']['linked_title_is_full_body'])

    def test_old_unknowns_and_seven_field_archive_contract_retained(self):
        d = contract()
        parent = json.loads((s.ROOT / 'research/recovered/STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-R1.json').read_bytes())
        self.assertEqual(parent['coverage']['qualified_images'], 0)
        self.assertEqual(parent['coverage']['unattempted_image_urls'], 12)
        archive = json.loads((s.ROOT / 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_bytes())
        required = set(archive['future_website']['record_contract']['required'])
        for row in d['records']:
            self.assertLessEqual(required, row.keys())
            self.assertIsNone(row['new_world_map_census_increment'])
        report = json.loads((s.ROOT / 'research/recovered/STONEAGE-JP2004-NAMED-VILLAGE-LOCAL-REPLAY-R105.json').read_bytes())
        self.assertEqual(report['operator_rows'], d['operator_rows'])
        self.assertEqual(report['records'], d['records'])
        self.assertFalse(report['contest']['planned_is_executed'])
        self.assertFalse(report['negative_http_probes_repeated_by_ci'])

if __name__ == '__main__':
    unittest.main()
