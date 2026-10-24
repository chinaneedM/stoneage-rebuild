import copy
import hashlib
import json
import unittest
from tools import stoneage_jp2004_osanpo_r106 as s

def contract():
    return json.loads(s.SOURCE.read_bytes())

def synthetic():
    """Invented short content exercises DOM guards; no original manual fixture."""
    d = copy.deepcopy(contract())
    texts = ['【ペットの技】合成した検証資料。', '[おさんぽ]について別の検証資料。']
    images = d['html_metadata']['image_references']
    def img(e):
        return '<img ' + ' '.join(k + '="' + v + '"' for k, v in e.items() if v is not None) + '>'
    body = img(images[0]) + '<table><tr><td>'
    for i, text in enumerate(texts):
        body += '<table><tr><td></td><td>' + text + '</td><td>' + img(images[i + 1]) + '</td></tr></table>'
        b = s.compact(text).encode()
        d['sections'][i]['identity'] = {'table_close_ordinal': i, 'row': 0, 'column': 1,
                                      'normalized_utf8_bytes': len(b), 'normalized_sha256': hashlib.sha256(b).hexdigest()}
    body += '</td></tr></table><map name="pettec">'
    for a in d['html_metadata']['skill_map_areas']:
        body += '<area coords="' + a['coords'] + '" alt="' + a['alt'] + '">'
    body += '</map><div usemap="#osanpo"></div>'
    return body.encode('cp932'), d

class Osanpo(unittest.TestCase):
    def test_scoped_sections_and_html_metadata_only(self):
        raw, d = synthetic()
        sections, meta = s.extract(raw, d, check_raw=False)
        self.assertEqual(len(sections), 2)
        self.assertEqual(len(meta['skill_map_areas']), 8)
        self.assertEqual(meta['osanpo_fragment_targets'], [])

    def test_changed_text_or_reassigned_section_rejected(self):
        raw, d = synthetic()
        for a, b in [('合成した', '変更した'), ('【ペットの技】', '[おさんぽ]について')]:
            with self.subTest(value=a), self.assertRaises(ValueError):
                s.extract(raw.replace(a.encode('cp932'), b.encode('cp932')), d, check_raw=False)

    def test_hidden_or_outside_table_claims_cannot_repair_missing_section(self):
        raw, d = synthetic()
        marker = '【ペットの技】合成した検証資料。'.encode('cp932')
        for fake in (b'<script>' + marker + b'</script>', b'<div hidden>' + marker + b'</div>', b'<div style="display:none">' + marker + b'</div>', marker):
            with self.assertRaises(ValueError):
                s.extract(fake + raw.replace(marker, b''), d, check_raw=False)

    def test_wrong_image_reference_or_area_meaning_rejected(self):
        raw, d = synthetic()
        for a, b in [(b'pet_osanpo.gif', b'other.gif'), (b'height="127"', b'height="128"'), ('白色'.encode('cp932'), '暗色'.encode('cp932'))]:
            with self.subTest(value=a), self.assertRaisesRegex(ValueError, 'metadata'):
                s.extract(raw.replace(a, b), d, check_raw=False)

    def test_usemap_is_not_an_actual_fragment_target(self):
        raw, d = synthetic()
        for fake in (b'<a name="osanpo"></a>', b'<div id="osanpo"></div>'):
            with self.assertRaisesRegex(ValueError, 'fragment'):
                s.extract(raw + fake, d, check_raw=False)
        self.assertFalse(contract()['page']['fragment_is_verified_scroll_target'])

    def test_nine_qualitative_cases_never_claim_sufficient_success(self):
        rows = s.projection_table()
        self.assertEqual(len(rows), 9)
        self.assertEqual(sum(x['verdict'] == 'BLOCKED_BY_DOCUMENTED_RULE' for x in rows), 5)
        self.assertEqual(s.blocker_projection(False, False)['verdict'], 'SUFFICIENCY_UNPROVEN')
        self.assertEqual(s.blocker_projection(True, True)['documented_blockers'], ['LOW_LOYALTY', 'MAIL_STATE'])
        self.assertTrue(all(not x['original_execution_observed'] for x in rows))

    def test_numeric_loyalty_or_state_ids_are_not_qualitative_inputs(self):
        for pair in [(70, False), (False, 4), (0, None), (None, 'MAIL'), (0.0, True)]:
            with self.subTest(pair=pair), self.assertRaisesRegex(ValueError, 'qualitative'):
                s.blocker_projection(*pair)

    def test_same_length_error_page_and_wrong_raw_identity_rejected(self):
        d = contract()
        with self.assertRaisesRegex(ValueError, 'byte identity'):
            s.extract(b'x' * d['page']['identity']['bytes'], d)

    def test_immutable_contract_cannot_invent_threshold_or_forget(self):
        d = contract()
        s.validate(d)
        for section, key, value in [('osanpo', 'loyalty_threshold', 70), ('learning', 'skill_capacity_number', 8),
                                    ('learning', 'direct_forget_described', True), ('learning', 'reorder_described', True)]:
            altered = copy.deepcopy(d)
            altered['rules'][section][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Immutable source'):
                s.validate(altered)

    def test_old_cross_region_claims_and_archive_boundaries_preserved(self):
        d = contract()
        old = json.loads((s.ROOT / 'research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json').read_bytes())
        self.assertTrue(old['extra_claims']['s1_pet_loyalty_thresholds']['around_70_disobey'])
        self.assertIsNone(d['rules']['osanpo']['loyalty_threshold'])
        archive = json.loads((s.ROOT / 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_bytes())['future_website']
        for row in d['records']:
            self.assertLessEqual(set(archive['record_contract']['required']), row.keys())
            self.assertIn(row['collection'], archive['required_collections'])
            self.assertIsNone(row['game_ids'])
        report = json.loads((s.ROOT / 'research/recovered/STONEAGE-JP2004-OSANPO-LOCAL-REPLAY-R106.json').read_bytes())
        self.assertEqual(report['rules'], d['rules'])
        self.assertFalse(report['image_probe_repeated_by_ci'])
        self.assertIsNone(report['image_probe']['actual_dimensions'])

if __name__ == '__main__':
    unittest.main()
