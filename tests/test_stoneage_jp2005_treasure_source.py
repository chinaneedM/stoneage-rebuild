"""Phase, ownership, hidden source and durable provenance boundary counterexamples."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2005_treasure_source as m


def fixture():
    # Synthetic numerical schedule and counts deliberately differ from the live source.
    intro = 'ガイアックスは，MMORPG「ストーンエイジ」で，9月13日（金）から"試験イベント"と題した二部構成のイベント＃＃＃＃＃以下，リリースより＃＃＃＃＃'
    quote = '''第一部9月10日（水）11:00（定期メンテナンス明けから）～11日（木）12:00（定期メンテナンスに入るまで）
    第二部9月11日（木）15:00（定期メンテナンス明けから）～12日（金）10:00（定期メンテナンスに入るまで）
    ●開催場所全サーバーの一部のダンジョン●参加条件特になし（全ユーザーが参加できます）
    全サーバーの試験村にNPC『試験人物』が登場；精霊の力の結晶を集めてくるよう、プレイヤーキャラクターに伝えます（クエストを与えます）
    一部のエリアの恐竜が低確率で特殊なイベントアイテムを落とす；全種類集めてイベントの第二部で『試験人物』に渡す
    第一部で4種類、第二部で2種類の計6種類；第一部と第二部では異なる；第一部でしか手に入らないアイテム
    繰り返し行えるクエストであるため、何度でもチャレンジすることが可能
    イベントアイテムは他プレイヤーとの受け渡しが可能；他プレイヤーとの売買でアイテムを手に入れるのも一つの方法
    イベントアイテムと賞品の交換は第二部から開始；賞品（このイベント限定のアイテム）'''
    outro = '＃＃＃＃＃限定アイテムの詳細は，まだ明かされていない<a href="http://stoneage.to/info/event_020.html">「こちら」</a>（TeT）'
    return ('<meta charset=shift_jis><h5>MMORPG「ストーンエイジ」で，限定アイテムが入手できるイベント</h5>'
        '<div class="news_txt1">2005/09/06 17:23</div><td class="newstext"><!-- 本文開始 -->' + intro +
        '<FONT color=#880000>' + quote + '</FONT>' + outro + '<!-- 本文終了 --></td><!-- tDialy:END -->').encode('cp932')


class TreasureTests(unittest.TestCase):
    def test_cross_version_types_thresholds_and_identity_remain_distinct(self):
        report = json.loads(m.REPORT.read_text())
        relation = m.compare_event_shapes(report['extraction'])
        self.assertEqual(relation['jp2005']['collectible_types'], 5)
        self.assertIsNone(relation['jp2005']['specified_per_type_quantities'])
        self.assertTrue(all(r['individual_cost'] is None and r['actual_unlock_verified'] is False
                            for r in relation['jp2008']['reported_delivery_thresholds']))
        self.assertIsNone(relation['jp2008']['counter_scope'])
        for change in [lambda d: d['cross_version_comparison'].update(historical_evolution_proven=True),
                       lambda d: d['cross_version_comparison']['jp2008']['reported_delivery_thresholds'][0].update(individual_cost=5)]:
            changed = copy.deepcopy(report); change(changed)
            with self.assertRaises(ValueError): m.verify_report(changed)

    def test_dynamic_values_preserve_types_schedule_and_unresolved_weekday(self):
        ex = m.derive(fixture())
        self.assertEqual(ex['event_name'], '試験イベント')
        self.assertEqual(ex['collectible_type_counts_by_phase'], [4, 2])
        self.assertEqual(ex['total_collectible_types'], 6)
        self.assertEqual(ex['phases'][0]['start']['day'], 10)
        self.assertEqual(ex['phases'][0]['start']['time'], '11:00')
        self.assertEqual(ex['npc']['name'], '試験人物')
        self.assertEqual(ex['locations']['npc_village_as_written'], '試験村')
        self.assertTrue(ex['editorial']['weekday_literals_disagree'])
        self.assertFalse(ex['editorial']['conflict_resolved'])
        self.assertIsNone(ex['per_type_required_quantity'])
        self.assertIsNone(ex['exchange']['reward_transferability'])

    def test_quote_must_be_visible_and_inside_unique_real_article_body(self):
        source = fixture().decode('cp932')
        quote = source.split('<FONT color=#880000>')[1].split('</FONT>')[0]
        cases = [source.replace('class="newstext"', 'class="chrome"'),
                 source.replace(quote, '<script>' + quote + '</script>'),
                 source.replace('<!-- 本文開始 -->', '<!-- wrong marker -->'),
                 source.replace('</FONT>', '</FONT><FONT color=#880000>' + quote + '</FONT>'),
                 '<script>' + source + '</script>']
        for changed in cases:
            with self.assertRaises(ValueError): m.derive(changed.encode('cp932'))
        self.assertEqual(m.derive(fixture()), m.derive(fixture() + b'<script>chrome=1</script>'))

    def test_release_cannot_borrow_restrictions_or_trade_claims_from_editorial(self):
        source = fixture().decode('cp932')
        for old, new in [('低確率', '必ず'), ('一部のダンジョン', 'すべてのダンジョン'),
                         ('受け渡しが可能', '受け渡し禁止'), ('第二部から開始', '第一部から開始'),
                         ('何度でもチャレンジ', '一度だけチャレンジ')]:
            changed = source.replace(old, new).replace('（TeT）', old + '（TeT）')
            with self.assertRaises(ValueError): m.derive(changed.encode('cp932'))

    def test_phase_membership_and_exchange_recipient_cannot_drift(self):
        source = fixture().decode('cp932')
        for old, new in [('計6種類', '計7種類'), ('第二部9月11日', '第一部9月11日'),
                         ('第二部で『試験人物』に渡す', '第二部で『別人物』に渡す')]:
            with self.assertRaises(ValueError): m.derive(source.replace(old, new).encode('cp932'))

    def test_unknown_numeric_values_catalog_rights_and_claim_scope_cannot_be_promoted(self):
        report = json.loads(m.REPORT.read_text()); m.verify_report(report)
        for change in [lambda d: d['negative_boundaries'].pop('five_types_are_five_units'),
                       lambda d: d.update(version_profile='TW10'),
                       lambda d: d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
                       lambda d: d['catalog_records'][1].update(source_refs=['S1-EDITORIAL']),
                       lambda d: d['extraction']['drop'].update(probability=0.01),
                       lambda d: d['extraction']['exchange'].update(reward_transferability=True),
                       lambda d: d['extraction']['editorial'].update(conflict_resolved=True)]:
            changed = copy.deepcopy(report); change(changed)
            with self.assertRaises(ValueError): m.verify_report(changed)
        changed = copy.deepcopy(report)
        changed['extraction']['per_type_required_quantity'] = 1
        changed['catalog_records'] = m.catalog(changed['extraction'])
        with self.assertRaises(ValueError): m.verify_report(changed)

    def test_actual_parent_file_missing_or_same_length_change_rejected(self):
        report = json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for pin in report['parent_pins']:
                dst = root / pin['path']; dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes((m.ROOT / pin['path']).read_bytes())
            with patch.object(m, 'ROOT', root):
                m.verify_report(report)
                dst = root / report['parent_pins'][0]['path']; raw = dst.read_bytes()
                dst.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
                with self.assertRaises(ValueError): m.verify_report(report)
                dst.unlink()
                with self.assertRaises(FileNotFoundError): m.verify_report(report)


if __name__ == '__main__': unittest.main()
