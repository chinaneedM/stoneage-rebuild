"""Synthetic documentary inputs test values, scope, evidence gaps and attribution."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_five_brothers_source as m


def fixture(root_tag='td'):
    # New coordinates, labels, answers and stats; this is not an archived article.
    body = ['等级要求：建议等级42级。2.交通工具：步行或骑宠。3.精灵的羽毛：福尔德村、达那村。',
        '由红、蓝、黄、绿、灰人龙所聚集的地盘',
        '前往"五兄弟的山寨"（东1，南2）地下1楼入口的红人龙"测试介绍人"（东3，南4）',
        '道具栏预留五个空位，留一个宠物栏的空格']
    for i, digit in enumerate('一二三四五',1):
        body.append(f'作答区的看板（东{i+10}，南{i+20}）问题{digit}：测试{i}？甲，乙。正确解答为"乙"。一张"问题{i}的答案用纸"')
    body += ['带着五张正确的答案纸，和五兄弟的山寨地下5楼的蓝人龙"奇洛斯"（东5，南6）',
        '玩家一定要和奇洛斯说话两次才能顺利往下一层楼走，假若智能的水晶掉落或是离开这个世界时，就会瞬间消失',
        '和黄人龙"测试通行人"（东7，南8）说话，黄人龙见勇者身上带有五兄弟的秘宝，即会传送勇者至最后的地下6楼',
        '找到问题看板（东9，南10）地下6楼入口右边的"测试返程人"说话，将会被传送回地下5楼',
        '和黄人龙"测试对战人"（东11，南12）对话，确定黄人龙就是强者即会展开激战',
        '击败它之后勇者便会被传送至后方的传送点，虽然无法与朋友组队战斗，但玩家可以在战斗时利用HELP按键，以让其它人在后来加入战斗行列',
        '灰色传送点（东13，南14）传送至五兄弟兑奖处，将智能的水晶交出，饰品及一级人龙一只，按下"确定"，按"取消"，就可以重新选择',
        '5.获得物品：'+'或'.join(f'测试饰品{i}（攻-{i}魅+{i+4}测试精灵'+('Lv3' if i==5 else '')+'）' for i in range(1,6))+'.',
        '6.获得宠物：'+'或'.join(f'测试宠{i}' for i in range(1,6))+'。',
        ''.join(f'与{color}人龙对话可获得"测试饰品{i}"和一级"测试宠{i}"。' for i,color in enumerate('红蓝黄绿灰',1)),
        '每一次的转生过后，再解一次任务，五次的转生',
        '7.五兄弟的山寨坐标：（东1，南2）怪物等级：12~34怪物种类：测试甲、测试乙、测试丙、测试丁五兄弟的山寨地下1楼',
        '8.东吉鲁山岭坐标：（东15，南16）、（东17，南18）怪物等级：23~45级怪物种类：样本甲、样本乙、样本丙、样本丁东吉鲁山岭1楼']
    return ('<meta charset=gb2312><!-- include 发布时间 begin -->2003-06-02 14:22<!-- include 发布时间 end -->'
        '<header>《石器时代》任务功略-五兄弟之谜</header>'+
        f'<{root_tag} class=l15z>'+''.join(body)+f'</{root_tag}>').encode('gb18030')


class FiveBrothersTests(unittest.TestCase):
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
                           lambda d: d.update(current_http_bytes_are_historical_bytes=True),
                           lambda d: d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job'])]:
                changed = copy.deepcopy(receipt); change(changed); path.write_text(json.dumps(changed))
                with self.assertRaises(ValueError): m.verify_custody(root)
            path.unlink()
            with self.assertRaises(FileNotFoundError): m.verify_custody(root)

    def test_dynamic_values_and_two_real_wrapper_shapes(self):
        ex=m.derive(fixture())
        self.assertEqual(ex,m.derive(fixture('span')))
        self.assertEqual(ex['recommended_level'],42)
        self.assertEqual(ex['quizzes'][0]['board_coord'],[11,21])
        self.assertEqual(ex['quizzes'][4]['answer_as_written'],'乙')
        self.assertEqual(ex['reward_options'][4]['stats'],{'攻':-5,'魅':9})
        self.assertEqual(ex['reward_options'][4]['spirit_level_as_written'],3)
        self.assertIsNone(ex['reward_options'][0]['spirit_level_as_written'])
        self.assertEqual(ex['npc_occurrences'][2]['name_as_written'],'测试通行人')
        self.assertEqual(ex['npc_occurrences'][3]['name_as_written'],'测试对战人')
        self.assertEqual(ex['ecology'][1]['coordinate_literals_as_reported'],[[15,16],[17,18]])
        self.assertIsNone(ex['crystal']['leaving_world_equates_to_logout_in_this_page'])

    def test_hidden_chrome_duplicate_and_unclosed_roots_cannot_supply_article(self):
        raw=fixture()
        for changed in [raw.replace(b'class=l15z',b'class=chrome'),raw+fixture(),
                raw.replace(b'</td>',b''),raw.replace('说话两次'.encode('gb18030'),'<script>说话两次</script>'.encode('gb18030')),
                raw.replace('《石器时代》任务功略-五兄弟之谜'.encode('gb18030'),b'')]:
            with self.assertRaises(ValueError):m.derive(changed)
        self.assertEqual(m.derive(raw),m.derive(raw+b'<script>unrelated=1</script>'))

    def test_mismatched_rewards_paper_order_and_missing_conditions_rejected(self):
        text=fixture().decode('gb18030')
        changes=[('和一级"测试宠2"','和一级"测试宠1"'),('问题5的答案用纸','问题4的答案用纸'),
            ('说话两次','说话一次'),('在战斗时利用HELP','在战斗前利用HELP'),
            ('按"取消"，就可以重新选择','按"取消"，领取全部奖励'),('掉落或是离开这个世界','掉落或是断线')]
        for old,new in changes:
            with self.subTest(old=old):
                with self.assertRaises(ValueError):m.derive((text.replace(old,new)+'<footer>'+old+'</footer>').encode('gb18030'))

    def test_unknowns_rights_version_source_and_historical_authority_stay_bounded(self):
        report=json.loads(m.REPORT.read_text());m.verify_report(report)
        changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['negative_boundaries'].pop('original_ids_recovered'),
            lambda d:d['catalog_records'][0].update(source_refs=['OTHER']),
            lambda d:d['catalog_records'][1].update(rights_status='RELEASE_APPROVED'),
            lambda d:d['extraction']['crystal'].update(disconnect_behavior='logout'),
            lambda d:d['extraction']['battle'].update(party_admission_restriction_in_this_page=True),
            lambda d:d['extraction']['reward_options'][0].update(pet_growth_stats={'HP':100}),
            lambda d:d['extraction']['ecology'][0].update(capture_eligibility=True),
            lambda d:d['historical_comparison'].update(independent_witness_count=2),
            lambda d:d['historical_comparison'].update(first_publication_authenticated=True)]
        for change in changes:
            d=copy.deepcopy(report);change(d)
            if d['extraction'] != report['extraction']:
                d['catalog_records'] = m.catalog(d['extraction'])
            with self.assertRaises(ValueError):m.verify_report(d)

    def test_same_length_parent_tamper_or_absence_is_not_accepted(self):
        report=json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for p in report['parent_pins']:
                target=root/p['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((m.ROOT/p['path']).read_bytes())
            with patch.object(m,'ROOT',root):
                m.verify_report(report)
                target=root/report['parent_pins'][0]['path'];raw=target.read_bytes()
                target.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
                with self.assertRaises(ValueError):m.verify_report(report)
                target.unlink()
                with self.assertRaises(FileNotFoundError):m.verify_report(report)


if __name__=='__main__':unittest.main()
