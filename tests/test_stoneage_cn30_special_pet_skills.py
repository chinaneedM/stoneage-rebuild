"""Source eligibility, hearsay, battle-state and original-identity counterexamples."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cn30_special_pet_skills as m


def fixture():
    skill = '这些宠物技能有：测试技甲、测试技乙、捐献、测试技丙、测试技丁、测试技戊、测试技己。其中除了捐献外，有T字的宠技只能让特殊的宠物学习，那就是“帖拉所伊朵”。然而“捐献”的技能，也只有“扑满乌力”。如果你用其他的宠物去学这些技能，是学不来的。'
    donation = '不是攻击用，也不是合成或料理的技能。必需使用在战斗中，不管对手是人物还是宠物，只能得到石币。战斗结束后发现可以从克克尔身上取得123石币。目前设定使用“捐献”技能后，扑满乌力就会变成“等待”状态，你必需再召唤他回到“战斗”状态，才能进行下一回合的捐献。'
    gp = '超级可爱逗趣GP宠物诞生。便恢复成单人状况。然而原先骑乘的宠物，也不能叫出来战斗。落马者必需等回合结束后，才能对原先骑乘的宠物做调度。落马技的使用是不限次数的。'
    block = ('开放宠物新技能。卡鲁它那的庄园（南岛12，34）卡鲁它那庄园56，78）。不是该庄园家族族员也是进得去的。' + skill + donation +
        '听说“捐献”技能也可能会使用在自己队友身上。机暴是五转的转生宠，只有五转后的人物才能驾驭机暴；用交易换来的话，也要看你有没有资格（五转）使用。'
        '扑满乌力目前尚无任务或可以补抓到的地方，扑满乌力抽奖活动，如果你可以用交易方式取得，等级是否低于交易的扑满乌力。')
    portal = ('<meta charset=gb2312><h2>石器时代3.0新增要素</h2><a name="3"></a>' + gp +
              '<a name="4"></a>其他栏目<a name="5"></a>' + block + '<a name="6"></a>其他栏目')
    essay = ('<meta charset=gb2312><td style=padding-left:40px>黄建枝</td><!-- include 发布时间 begin -->2003-05-01 06:52<!-- include 发布时间 end -->'
        '<td class=l15z><p>我是从石器时代5.0开始玩的。</p><p>据杂志报道：“开放宠物新技能：《石器时代3.0版本伊甸新大陆》'
        '卡鲁它那的庄园里的坐标56，78)。' + skill + '</p><p>新技能“捐献”我也不够清楚。</p><p>杂志报道：“这是只有扑满乌力' + donation +
        '</p><p>也听说：“‘捐献’的技能也可能会使用在自己队友身上。”</p></td>')
    return [portal.encode('gb18030'), essay.encode('gb18030'), (portal + '<!-- archival wrapper difference -->').encode('gb18030')]


class SpecialSkillTests(unittest.TestCase):
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
                           lambda d: d.update(current_http_pages_are_authenticated_historical_bytes=True),
                           lambda d: d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job'])]:
                changed = copy.deepcopy(receipt); change(changed); path.write_text(json.dumps(changed))
                with self.assertRaises(ValueError): m.verify_custody(root)
            path.unlink()
            with self.assertRaises(FileNotFoundError): m.verify_custody(root)



    def test_archived_reference_is_required_and_does_not_become_publication_or_build(self):
        raws=fixture();ex=m.derive(raws)
        self.assertEqual(ex['historical_comparison']['capture_timestamp'],'20030324221124')
        self.assertFalse(ex['historical_comparison']['same_game_build_authenticated'])
        with self.assertRaises(ValueError):m.derive(raws[:2])
        raws[2]=raws[2].decode('gb18030').replace('南岛12，34','南岛13，34').encode('gb18030')
        with self.assertRaises(ValueError):m.derive(raws)

    def test_values_are_extracted_and_numeric_example_is_not_a_formula(self):
        ex = m.derive(fixture())
        self.assertEqual(ex['source_skill_rows'][0]['name_as_written'], '测试技甲')
        self.assertEqual(ex['training_locations'][0]['outer_south_island_coordinate'], [12, 34])
        self.assertEqual(ex['training_locations'][0]['inside_manor_coordinate'], [56, 78])
        self.assertEqual(ex['donation_descriptions'][0]['example']['amount'], 123)
        self.assertIsNone(ex['donation_descriptions'][0]['fixed_payout'])
        self.assertEqual(ex['source_skill_rows'][2]['eligible_pet_label_as_reported'], '扑满乌力')
        self.assertEqual(ex['source_skill_rows'][0]['eligible_pet_label_as_reported'], '帖拉所伊朵')
        self.assertFalse(ex['source_relationship']['independent_witnesses_established'])

    def test_hidden_or_navigation_evidence_cannot_repair_selected_sections(self):
        for idx, old, new in [(0, '<a name="5"></a>', '<a href="#5"></a>'),
                              (0, '不是该庄园家族族员也是进得去的', '<script>不是该庄园家族族员也是进得去的</script>'),
                              (1, 'class=l15z', 'class=chrome'),
                              (1, '黄建枝</td>', '<script>黄建枝</script></td>')]:
            raws = fixture();raws[idx] = raws[idx].decode('gb18030').replace(old,new).encode('gb18030')
            with self.assertRaises(ValueError): m.derive(raws)
        raws = fixture();raws[0] += b'<script>chrome=1</script>'
        self.assertEqual(m.derive(fixture()), m.derive(raws))

    def test_duplicate_or_wrong_source_attribution_and_hearsay_rejected(self):
        for idx, old, new in [(1, '据杂志报道：', '亲自实测：'),
                              (1, '也听说：', '已证实：'),
                              (0, '听说“捐献”技能也可能', '证实“捐献”技能肯定'),
                              (1, '我是从石器时代5.0开始玩的', '我是从石器时代1.0开始玩的'),
                              (0, '<a name="5"></a>', '<a name="5"></a><a name="5"></a>')]:
            raws=fixture();raws[idx]=raws[idx].decode('gb18030').replace(old,new).encode('gb18030')
            with self.assertRaises(ValueError):m.derive(raws)

    def test_waiting_to_battle_and_turn_end_constraints_are_not_interchangeable(self):
        for idx,old,new in [(0,'变成“等待”状态','变成“休息”状态'),
                            (1,'回到“战斗”状态','回到“骑乘”状态'),
                            (0,'等回合结束后','等战斗结束后'),
                            (0,'使用是不限次数的','使用是仅限一次的'),
                            (0,'只有五转后的人物','只有四转后的人物')]:
            raws=fixture();raws[idx]=raws[idx].decode('gb18030').replace(old,new).encode('gb18030')
            with self.assertRaises(ValueError):m.derive(raws)

    def test_catalog_source_rights_and_unknown_skill_fields_cannot_be_promoted(self):
        report=json.loads(m.REPORT.read_text());m.verify_report(report)
        for change in [lambda d:d['negative_boundaries'].pop('eighty_is_fixed_payout'),
                       lambda d:d['catalog_records'][0].update(source_refs=['S2']),
                       lambda d:d['catalog_records'][0].update(version_profile='TW10'),
                       lambda d:d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
                       lambda d:d['extraction']['source_relationship'].update(magazine_original_acquired=True),
                       lambda d:d['extraction']['ally_target_claims'][0].update(tested=True)]:
            changed=copy.deepcopy(report);change(changed)
            with self.assertRaises(ValueError):m.verify_report(changed)
        changed=copy.deepcopy(report);changed['extraction']['donation_descriptions'][0]['fixed_payout']=80
        with self.assertRaises(ValueError):m.verify_report(changed)
        changed=copy.deepcopy(report);changed['extraction']['source_skill_rows'][0]['skill_id']=10
        changed['catalog_records']=m.catalog(changed['extraction'])
        with self.assertRaises(ValueError):m.verify_report(changed)

    def test_actual_parent_bytes_and_git_identity_cannot_be_substituted(self):
        report=json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for pin in report['parent_pins']:
                dst=root/pin['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((m.ROOT/pin['path']).read_bytes())
            with patch.object(m,'ROOT',root):
                m.verify_report(report)
                dst=root/report['parent_pins'][0]['path'];raw=dst.read_bytes()
                dst.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
                with self.assertRaises(ValueError):m.verify_report(report)
                dst.unlink()
                with self.assertRaises(FileNotFoundError):m.verify_report(report)


if __name__ == '__main__':unittest.main()
