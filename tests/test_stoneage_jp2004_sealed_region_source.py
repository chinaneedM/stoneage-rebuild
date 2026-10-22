"""Independent HTML layout and provenance counterexamples, not row-count mirrors."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2004_sealed_region_source as m


def layout(first='仮の<span>中身</span>'):
    tail = '→「ストーンエイジ」の記事一覧'
    slots = m.BEGIN + first + tail + m.END + (m.BEGIN + m.END) * 4
    return ('<html><head><meta charset=Shift_JIS></head><body>2004/09/17 19:12'
            + slots + '</body></html>').encode('cp932')


class SourceTests(unittest.TestCase):
    def test_actual_permanent_replays_reject_missing_and_equal_length_corruption(self):
        receipt = m.verify_custody()
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            paths = [p['path'] for p in receipt['permanent_pins']]
            paths.append(f'research/recovered/{m.STEM}-CUSTODY-R1.json')
            for rel in paths:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((m.ROOT / rel).read_bytes())
            m.verify_custody(root)
            p = root / f'research/recovered/{m.STEM}-CI-MAIN-R1.json'
            b = p.read_bytes()
            p.write_bytes(b[:-1] + bytes([b[-1] ^ 1]))
            with self.assertRaises(ValueError):
                m.verify_custody(root)
            p.unlink()
            with self.assertRaises(ValueError):
                m.verify_custody(root)

    def test_article_uses_visible_text_and_first_slot_only(self):
        raw = layout('仮の<script>隠れた情報</script><style>隠れた装飾</style><b>中身</b>')
        self.assertEqual(m.article(raw)[0], '仮の中身')
        self.assertEqual(m.article(raw + b'<script>outside=1;</script>'), m.article(raw))

    def test_hidden_date_cannot_substitute_for_visible_publication(self):
        raw = layout().replace(b'2004/09/17 19:12', b'<script>2004/09/17 19:12</script>')
        with self.assertRaises(ValueError):
            m.article(raw)

    def test_extra_content_slot_and_duplicate_body_are_rejected(self):
        for raw in [layout().replace((m.BEGIN + m.END).encode('cp932'),
                                     (m.BEGIN + '追加文' + m.END).encode('cp932'), 1),
                    layout() + b'<body>extra</body>']:
            with self.assertRaises(ValueError):
                m.article(raw)

    def test_charset_and_article_end_boundaries_are_not_guessed(self):
        for raw in [layout().replace(b'Shift_JIS', b'UTF-8'),
                    layout().replace(m.END.encode('cp932'), b'', 1)]:
            with self.assertRaises(ValueError):
                m.article(raw)

    def test_catalog_rejects_source_detachment_rights_and_build_promotions(self):
        report = json.loads(m.REPORT.read_text())
        m.verify_catalog(report)
        for change in [lambda d: d['scope'].update(runtime_verified=True),
                       lambda d: d['scope'].update(exact_build='TW10'),
                       lambda d: d['scope'].update(first_party_webpage_retrieved=True),
                       lambda d: d['catalog'][1]['content'].update(name='誤った島'),
                       lambda d: d['catalog'][1].update(game_ids={'floor': 123}),
                       lambda d: d['catalog'][1].update(rights_status='RELEASE_APPROVED'),
                       lambda d: d['catalog'][1].pop('source_refs')]:
            d = copy.deepcopy(report)
            change(d)
            with self.assertRaises((ValueError, KeyError)):
                m.verify_catalog(d)

    def test_unnamed_island_alias_and_mail_timer_must_remain_unproven(self):
        report = json.loads(m.REPORT.read_text())
        for change in [lambda d: d['cross_source_nonjoins'][0].update(identity_established=True),
                       lambda d: d['negative_boundaries'].update(mail_cooldown_or_prior_limit_recovered=True),
                       lambda d: d['negative_boundaries'].update(cave_to_submerged_island_route=True)]:
            d = copy.deepcopy(report)
            change(d)
            with self.assertRaises(ValueError):
                m.verify_catalog(d)

    def test_parent_custody_checks_actual_missing_and_changed_files(self):
        report = json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for pin in report['parent_pins']:
                p = root / pin['path']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((m.ROOT / pin['path']).read_bytes())
            with patch.object(m, 'ROOT', root):
                m.verify_catalog(report)
                p = root / report['parent_pins'][0]['path']
                b = p.read_bytes()
                p.write_bytes(b[:-1] + bytes([b[-1] ^ 1]))
                with self.assertRaises(ValueError):
                    m.verify_catalog(report)
                p.unlink()
                with self.assertRaises(FileNotFoundError):
                    m.verify_catalog(report)


if __name__ == '__main__':
    unittest.main()
