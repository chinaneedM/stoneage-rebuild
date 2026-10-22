"""Adversarial source, image and evidence-boundary checks; no historical game execution."""
import copy
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from tools import stoneage_jp2009_kokuen_source as m


def fixture():
    # Numerical values, NPC and mix are deliberately synthetic.
    rows=[
      '耐久のほら貝袋(黒炎)使用すると、何度でも自分の耐久力が回復できるアイテムが出現。',
      '気力のほら貝袋(黒炎)使用すると、何度でも自分の気力が回復できるアイテムが出現。',
      '黒炎変身薬使用するとペット「コクエン」に変身できる薬']
    for i in range(3):
        rows[i]+='「耐久のほら貝袋」「気力のほら貝袋」「黒炎変身薬」合計12個で「黒炎変身鎧チケット」と交換。'
        if i==0:rows[i]+='例）「耐久のほら貝袋」2個＋「気力のほら貝袋」3個＋「黒炎変身薬」7個で交換。'
        if i<2:rows[i]+='※出現するアイテムは、ログアウト/ドロップで消滅'
    rows += ['黒炎変身鎧チケットCP交換所にいるNPC「試験交換員」にてペット「コクエン」に変身できる鎧と交換。7枚で「黒炎再抽選チケット」と交換。',
        '黒炎再抽選チケットCP交換所にいるNPC「試験交換員」にてペット「コクエン」のステータス再抽選ができるチケット。9枚で「黒炎交換チケット」と交換。',
        '黒炎交換チケットCP交換所にいるNPC「試験交換員」にてペット「コクエン」と交換できるチケット。']
    marker='■期間限定！便利商店に新しいペット「コクエン」追加！'
    return ('<head><meta charset=utf-8></head><header>2009/06/29 16:55「ストーンエイジ」の公式サイトがリニューアル。新ペットも実装</header>'
        '<div class="entry-content"><table><tr><td class="release_maker">デジパーク</td><td>2009/06/29</td></tr></table>'
        'メーカー発表文の内容をそのまま掲載しています'+marker+'目次'+marker+
        '新ペット「コクエン」や「コクエン」に変身できるアイテム。'
        '開始：2009年6月24日（火）定期メンテナンス終了から終了：2009年7月22日(火)定期メンテナンス開始まで'
        'ステータスは一定値を基準にランダムです。必ずしも、このような数値になるとは限りません。'
        '<img src="/games/013/G001377/20090629031/TN/001.jpg" onclick="return OVERLAY_SS_open(event,\'/games/013/G001377/20090629031/SS/001.jpg\',\'270\',\'363\');">'
        '黒炎の袋731 Gstone使用するとランダムでアイテムが１つ手に入ります。黒炎の袋出現アイテム）全6種類'+
        ''.join(rows)+'一発逆転!?別のイベント掛け金が２倍</div>').encode()


class KokuenTests(unittest.TestCase):
    def test_dynamic_dates_price_exchange_counts_and_npc_are_extracted(self):
        ex=m.derive(fixture())
        self.assertEqual(ex['announced_sale']['start_date'],'2009-06-24')
        self.assertEqual(ex['bag']['price'],731)
        self.assertEqual(ex['conversion']['mixed_total_for_armor_ticket'],12)
        self.assertEqual(ex['conversion']['example_mixture_counts'],[2,3,7])
        self.assertEqual(ex['conversion']['armor_tickets_for_reroll_ticket'],7)
        self.assertEqual(ex['conversion']['reroll_tickets_for_pet_ticket'],9)
        self.assertEqual(ex['exchange_npc']['name'],'試験交換員')
        self.assertIsNone(ex['species_base_values'])
        self.assertIsNone(ex['recovery_bags'][0]['outer_bag_logout_behavior'])

    def test_real_image_metadata_is_decoded_without_ocr_or_invented_values(self):
        b=io.BytesIO();Image.new('RGB',(23,17),'purple').save(b,format='JPEG');raw=b.getvalue()
        meta=m.image_metadata(raw);self.assertEqual(meta['size'],[23,17]);self.assertEqual(meta['sha256'],m.sha(raw))
        self.assertEqual(meta['format'],'JPEG');self.assertNotIn('hp_display',meta)
        visual={'image_metadata':meta};self.assertEqual(m.verify_visual(raw,visual),meta)
        padded=raw+b'TESTA';proof={'image_metadata':m.image_metadata(padded)}
        with self.assertRaises(ValueError):m.verify_visual(raw+b'TESTB',proof)
        with self.assertRaises((OSError,ValueError)):m.image_metadata(raw[:20])

    def test_missing_hidden_duplicate_and_unclosed_body_rejected(self):
        raw=fixture()
        for changed in [raw.replace(b'entry-content',b'chrome'),raw+raw,raw.replace(b'</div>',b''),
            raw.replace('ステータスは一定値を基準にランダムです。'.encode(),'<script>ステータスは一定値を基準にランダムです。</script>'.encode())]:
            with self.assertRaises(ValueError):m.derive(changed)
        tag=re.search(b'<img[^>]+>',raw).group()
        moved=raw.replace(tag,b'').replace(b'</div>',tag+b'</div>')
        with self.assertRaises(ValueError):m.derive(moved)
        self.assertEqual(m.derive(raw),m.derive(raw+b'<script>chrome=1</script>'))
        self.assertEqual(m.derive(raw),m.derive(raw.replace('掛け金が２倍'.encode(),'掛け金が９倍'.encode())))

    def test_mix_lifetime_and_function_loss_cannot_be_repaired_from_chrome(self):
        text=fixture().decode()
        for old,new in [('合計12個','合計13個'),('」2個＋','」3個＋'),
            ('※出現するアイテムは、ログアウト/ドロップで消滅','※袋は、ログアウト/ドロップで消滅'),
            ('何度でも自分の気力','何度でも自分の耐久力'),('ステータス再抽選ができる','ステータスを固定できる'),
            ('SS/001.jpg','SS/002.jpg')]:
            with self.subTest(old=old):
                with self.assertRaises(ValueError):m.derive((text.replace(old,new)+'<footer>'+old+'</footer>').encode())

    def test_rights_version_unknowns_sample_and_parent_conflict_cannot_be_promoted(self):
        r=json.loads(m.REPORT.read_text());m.verify_report(r)
        changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['negative_boundaries'].pop('bag_guarantees_pet'),
            lambda d:d['catalog_records'][0].update(source_refs=['OTHER']),
            lambda d:d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
            lambda d:d['extraction'].update(species_base_values={'HP':72}),
            lambda d:d['extraction']['recovery_bags'][0].update(outer_bag_logout_behavior='vanishes'),
            lambda d:d['extraction']['conversion'].update(expected_gstone_cost_for_pet=100000),
            lambda d:d['extraction']['ticket_effects'][2].update(pet_level=1),
            lambda d:d['visual_reference']['sample'].update(element_numeric_values=[8,0,0,2]),
            lambda d:d['visual_reference']['image_metadata'].update(sha256='0'*64),
            lambda d:d['parent_comparison'].update(parent_seventh_item_filled_from_kokuen=True),
            lambda d:d['source_pages'][0].update(historical_capture='20090629165547')]
        for change in changes:
            d=copy.deepcopy(r);change(d)
            if d['extraction']!=r['extraction'] or d['visual_reference']!=r['visual_reference']:
                d['catalog_records']=m.catalog(d['extraction'],d['visual_reference'])
            with self.assertRaises(ValueError):m.verify_report(d)

    def test_parent_missing_or_same_length_tamper_denied(self):
        r=json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for pin in r['parent_pins']:
                p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
            with patch.object(m,'ROOT',root):
                m.verify_report(r)
                p=root/r['parent_pins'][0]['path'];b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]))
                with self.assertRaises(ValueError):m.verify_report(r)
                p.unlink()
                with self.assertRaises(FileNotFoundError):m.verify_report(r)


if __name__=='__main__':unittest.main()
