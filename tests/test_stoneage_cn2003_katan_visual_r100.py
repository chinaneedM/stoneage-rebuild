import copy
import json
import hashlib
import io
import unittest
from tools import stoneage_cn2003_katan_visual_r100 as m


class KatanVisual(unittest.TestCase):
    def setUp(self):
        self.d = json.loads(m.SOURCE.read_text())
        self.html = self.synthetic()

    def synthetic(self):
        d = self.d
        cells = ''.join('<td><a href="' + x['original_href'] + '"><img src="' + x['thumbnail'] + '"></a></td>' for x in d['images'])
        captions = ''.join('<td>' + x['caption'] + '</td>' for x in d['images'])
        return (d['source']['title'] + d['source']['display_date'] + '网友投稿<table><tr>' + cells + '<td><img src="third.jpg"></td></tr><tr>' + captions + '<td>third caption</td></tr></table>').encode('gb18030')

    def test_actual_source_contract_and_two_selected_links(self):
        m.validate_source(self.d)
        self.assertEqual(m.parse_page(self.html, self.d), [x['url'] for x in self.d['images']])

    def test_hidden_or_duplicated_table_cannot_supply_evidence(self):
        for before, after in [(b'<!--', b'-->'), (b'<script>', b'</script>'), (b'<style>', b'</style>'), (b'<div hidden>', b'</div>'), (b'<div style="display: none">', b'</div>'), (b'<div aria-hidden="true">', b'</div>')]:
            with self.subTest(before=before), self.assertRaises(ValueError):
                m.parse_page(before + self.html + after, self.d)
        with self.assertRaises(ValueError):
            m.parse_page(self.html + self.html, self.d)

    def test_caption_target_and_thumbnail_mutations_rejected(self):
        changes = [('卡坦', '卡拉'), ('四种鱼类', '三种鸟类'), ('-232-', '-999-'), ('-231-', '-999-'), ('2003-05-29', '2004-05-29'), ('网友投稿', '官方公告')]
        for old, new in changes:
            with self.subTest(old=old), self.assertRaises(ValueError):
                m.parse_page(self.html.replace(old.encode('gb18030'), new.encode('gb18030')), self.d)

    def test_swapped_images_rejected(self):
        a, b = self.d['images']
        raw = self.html.replace(a['original_href'].encode(), b['original_href'].encode())
        with self.assertRaises(ValueError):
            m.parse_page(raw, self.d)

    def test_image_payload_and_fake_image_rejected(self):
        for b in (b'', b'not a jpeg', b'\xff\xd8\xff\xd9'):
            with self.assertRaises(ValueError):
                m.decode_image(b, self.d['images'][0])

    def test_full_decoder_accepts_synthetic_and_rejects_matching_hash_truncation(self):
        from PIL import Image
        output = io.BytesIO()
        Image.new('RGB', (8, 8), (20, 40, 60)).save(output, format='JPEG')
        raw = output.getvalue()
        expected = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'format': 'JPEG', 'size': [8, 8], 'mode': 'RGB', 'frames': 1}
        self.assertEqual(m.decode_image(raw, expected)['size'], [8, 8])
        truncated = raw[:len(raw) // 2]
        expected.update(bytes=len(truncated), sha256=hashlib.sha256(truncated).hexdigest())
        with self.assertRaises(OSError):
            m.decode_image(truncated, expected)

    def test_forged_build_server_and_identity_claims_rejected(self):
        for key, value in [('tw10_same_build_authenticated', True), ('original_render_selector_proven', True), ('native_npc_id', 16000), ('server_handover_executed', True), ('ring_loss_conflict_resolved', True), ('stage_a_closed', True), ('overall_percent', 100)]:
            d = copy.deepcopy(self.d)
            d['boundaries'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                m.validate_source(d)

    def test_outside_script_does_not_change_selected_evidence(self):
        self.assertEqual(m.parse_page(self.html + b'<script>wrong npc 9999</script><!-- wrong links -->', self.d), [x['url'] for x in self.d['images']])


if __name__ == '__main__':
    unittest.main()
