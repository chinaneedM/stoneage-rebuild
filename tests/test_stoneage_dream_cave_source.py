"""Meaningful scope and provenance failures, separate from live source replay."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_dream_cave_source as m


def fixture():
    # Deliberately different numerical values, not a copy of the archived article.
    body = '''等级要求：建议等级42级。
    虽然没有硬性规定，但若玩家解过成人仪式，之后才能得到空想系列的装备；否则随机物品一个。
    奇努伊村（东1，南2）（东3，南4）（东5，南6），和村中的老人（东7，南8）谈话
    白天的时候，玩家可以从坐标（东9，南10）的洞口进入晚上则只能由坐标（东11，南12）的洞口进入
    3.交通工具：加美航空。4.精灵的羽毛：无。
    将先见之光弄掉在地上的话，虽然先见之光会立刻消失不见；勇者可以再跟老人拿一次是没问题的
    只要玩家注销，“先见之光”就会如同光束般消失不见。每年都会将先见之光贡献给仙人
    住在“梦幻洞窟”里的“梦见的仙人”；将“先见之光”交给仙人；传说沙姆岛住着一位仙人；红蛙“测试甲”和金蛙“测试乙”率领的宠物大队
    红蛙跟金蛙是仙人聊天的对象；无法跟仙人以外的人类接近
    “空想的竖琴”（攻+9敏-2魅+3睡眠的精灵Lv4）
    “空想的帽子”（防+8敏+7滋润的精灵Lv3）
    “空想的衣服”（攻-4防+6敏+5治愈的精灵Lv2）
    第一次解此任务可以获得“空想的竖琴”；第二次解此任务可以获得“空想的帽子”；第三次解此任务可以获得“空想的衣服”
    第四次以后解此任务则会获得仙人给的随机物品；又可以重复解
    怪物等级：12~34级怪物种类：测试甲、测试乙、旅人上左
    <table><tr><td>传送点路径（去程）：左→右。传送点路径（回程）：上→下。</td></tr></table>
    <table><tr><td>传送点路径（去程）：下→上。传送点路径（回程）：右→左。</td></tr></table>'''
    return ('<meta charset=gb2312><!-- include 发布时间 begin -->2003-05-30 13:51<!-- include 发布时间 end -->'
            '<table><tr><td height=30 colspan=4>《石器时代》任务功略-梦幻洞窟</td></tr>'
            '<tr><td class=l15z>' + body + '</td></tr></table>').encode('gb18030')


class DreamCaveTests(unittest.TestCase):
    def test_custody_rejects_missing_changed_and_misattributed_original_reports(self):
        receipt = m.verify_custody()
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            path = root / f'research/recovered/{m.STEM}-CUSTODY-R1.json'
            for pin in receipt['permanent_pins']:
                p = root / pin['path']; p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((m.ROOT / pin['path']).read_bytes())
            path.write_text(json.dumps(receipt)); m.verify_custody(root)
            for pin in receipt['permanent_pins']:
                p = root / pin['path']; raw = p.read_bytes()
                p.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
                with self.assertRaises(ValueError): m.verify_custody(root)
                p.unlink()
                with self.assertRaises(FileNotFoundError): m.verify_custody(root)
                p.write_bytes(raw)
            for change in [lambda d: d['runs'].append(d['runs'][0]),
                           lambda d: d.update(content_commit='0' * 40),
                           lambda d: d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
                           lambda d: d.update(historical_bytes_authenticated=True),
                           lambda d: d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job'])]:
                changed = copy.deepcopy(receipt); change(changed); path.write_text(json.dumps(changed))
                with self.assertRaises(ValueError): m.verify_custody(root)
            path.unlink()
            with self.assertRaises(FileNotFoundError): m.verify_custody(root)

    def test_values_are_extracted_and_ambiguous_routes_stay_unassigned(self):
        ex = m.derive(fixture())
        self.assertEqual(ex['recommended_level'], 42)
        self.assertEqual(ex['entrances_as_reported'], {'day': [9, 10], 'night': [11, 12]})
        self.assertEqual(ex['rewards'][0]['stats'], {'攻': 9, '敏': -2, '魅': 3})
        self.assertEqual(ex['rewards'][0]['spirit_level'], 4)
        self.assertEqual(ex['named_guards'], ['测试甲', '测试乙'])
        self.assertEqual(ex['monster_level_range_as_reported'], [12, 34])
        self.assertEqual(ex['route_pairs_in_source_order'][0][0]['steps'], ['左', '右'])
        self.assertTrue(all(r['day_night_assignment'] is None for p in ex['route_pairs_in_source_order'] for r in p))
        self.assertIsNone(ex['offering']['disconnect_behavior'])
        self.assertFalse(ex['adult_required_for_admission'])

    def test_article_chrome_hidden_evidence_and_duplicate_roots_rejected(self):
        raw = fixture()
        for mutated in [raw.replace(b'class=l15z', b'class=chrome'),
                        raw.replace('虽然没有硬性规定'.encode('gb18030'), '<script>虽然没有硬性规定</script>'.encode('gb18030')),
                        raw + '<td class=l15z>无关正文</td>'.encode('gb18030'),
                        raw.replace(b'</td></tr></table>', b'')]:
            with self.subTest(case=mutated[-80:]):
                with self.assertRaises(ValueError): m.derive(mutated)
        self.assertEqual(m.derive(raw), m.derive(raw + b'<script>chrome=2</script>'))

    def test_reward_order_and_semantic_preconditions_cannot_be_repaired_by_chrome(self):
        source = fixture().decode('gb18030')
        for old, new in [('第三次解此任务可以获得', '第二次解此任务可以获得'),
                         ('虽然没有硬性规定', '硬性要求成人'), ('注销', '断线'),
                         ('第四次以后', '第五次以后'), ('传送点路径（回程）：右→左。', ''),
                         ('</td></tr></table>\n    <table><tr><td>', '')]:
            with self.subTest(old=old):
                with self.assertRaises(ValueError):
                    m.derive((source.replace(old, new) + '<footer>' + old + '</footer>').encode('gb18030'))

    def test_unknowns_rights_version_and_source_links_cannot_be_promoted(self):
        report = json.loads(m.REPORT.read_text())
        m.verify_report(report)
        changes = [lambda d: d['negative_boundaries'].pop('original_ids_recovered'),
                   lambda d: d.update(version_profile='TW10'),
                   lambda d: d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
                   lambda d: d['catalog_records'][0].update(source_refs=['OTHER']),
                   lambda d: d['extraction'].update(map_ids=[10]),
                   lambda d: d['extraction']['route_pairs_in_source_order'][0][0].update(day_night_assignment='day'),
                   lambda d: d['extraction']['offering'].update(disconnect_behavior='same_as_logout')]
        for change in changes:
            changed = copy.deepcopy(report); change(changed)
            with self.assertRaises(ValueError): m.verify_report(changed)

    def test_parent_bytes_and_original_git_identity_are_required(self):
        report = json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for p in report['parent_pins']:
                dst = root / p['path']; dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes((m.ROOT / p['path']).read_bytes())
            with patch.object(m, 'ROOT', root):
                m.verify_report(report)
                dst = root / report['parent_pins'][0]['path']; raw = dst.read_bytes()
                dst.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
                with self.assertRaises(ValueError): m.verify_report(report)
                dst.unlink()
                with self.assertRaises(FileNotFoundError): m.verify_report(report)


if __name__ == '__main__': unittest.main()
