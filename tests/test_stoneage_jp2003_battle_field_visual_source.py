"""Guard screenshot attribution and acquisition boundaries, not game behavior."""
import copy
import json
import tempfile
from pathlib import Path
import unittest
from tools.stoneage_jp2003_battle_field_visual_source import Page, page, check_catalog, image_metadata, verify_custody

REPORT = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.json'


class VisualSourceTests(unittest.TestCase):
    def setUp(self):
        r = json.loads(REPORT.read_text())
        self.catalog, self.extracted = copy.deepcopy(r['catalog']), r['extracted']

    def test_valid_source_catalog(self):
        check_catalog(self.catalog, self.extracted)

    def test_hidden_script_image_does_not_bind_to_visible_wrapper(self):
        p = Page()
        p.feed('<script><a href="bad"><img src="bad"></a></script>'
               '<a href="wrapper"><img src="thumbnail" alt="position"></a>')
        self.assertEqual(p.pairs, [{'href': 'wrapper', 'src': 'thumbnail', 'alt': 'position'}])

    def test_charset_is_explicit_and_decode_errors_are_not_replaced(self):
        _, text = page('図集'.encode('euc_jp'), 'euc_jp')
        self.assertEqual(text, '図集')
        with self.assertRaises(UnicodeDecodeError):
            page(b'\x83')

    def test_two_valid_images_cannot_exchange_reviewed_positions(self):
        a, b = self.catalog['records'][:2]
        a['acquired_image'], b['acquired_image'] = b['acquired_image'], a['acquired_image']
        with self.assertRaises(ValueError):
            check_catalog(self.catalog, self.extracted)

    def test_unrequested_reference_does_not_gain_a_review(self):
        self.catalog['records'][2]['manual_observation'] = self.catalog['records'][0]['manual_observation']
        with self.assertRaises(ValueError):
            check_catalog(self.catalog, self.extracted)

    def test_development_notice_and_build_scope_cannot_be_promoted(self):
        for field, value in [('development_notice', False), ('exact_build_verified', True),
                             ('version_profile', 'TW10')]:
            with self.subTest(field=field):
                c = copy.deepcopy(self.catalog)
                c['records'][0][field] = value
                with self.assertRaises(ValueError):
                    check_catalog(c, self.extracted)

    def test_web_size_and_date_are_not_native_resolution_or_capture_date(self):
        for field, value in [('original_native_resolution', [640, 480]), ('image_capture_date', '2003-12-12')]:
            with self.subTest(field=field):
                c = copy.deepcopy(self.catalog)
                c['records'][0][field] = value
                with self.assertRaises(ValueError):
                    check_catalog(c, self.extracted)

    def test_no_silent_asset_release_game_id_or_lost_citation(self):
        for field, value in [('rights_status', 'RELEASE_APPROVED'), ('game_ids', {'pet': 1}), ('source_refs', [])]:
            with self.subTest(field=field):
                c = copy.deepcopy(self.catalog)
                c['records'][0][field] = value
                with self.assertRaises(ValueError):
                    check_catalog(c, self.extracted)

    def test_human_judgment_stays_attached_to_reviewed_hash(self):
        self.catalog['records'][0]['manual_observation']['reviewed_image_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            check_catalog(self.catalog, self.extracted)

    def test_invalid_image_is_not_declared_decoded(self):
        with self.assertRaises(OSError):
            image_metadata(b'not an image')

    def test_actual_derived_custody_rejects_removal_and_same_length_corruption(self):
        root = REPORT.parents[2]
        receipt = json.loads((REPORT.parent / 'STONEAGE-JP2003-BATTLE-FIELD-VISUAL-CUSTODY-R1.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory)
            for row in receipt['permanent_derived_files']:
                path = copied / row['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((root / row['path']).read_bytes())
            verify_custody(receipt, copied)
            path = copied / 'research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-CI-MAIN-R1.json'
            raw = path.read_bytes()
            path.write_bytes(raw[:-2] + bytes([raw[-2] ^ 1]) + raw[-1:])
            with self.assertRaises(ValueError):
                verify_custody(receipt, copied)
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                verify_custody(receipt, copied)


if __name__ == '__main__':
    unittest.main()
