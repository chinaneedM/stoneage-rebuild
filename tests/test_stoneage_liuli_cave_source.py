"""Independent synthetic values and adversarial perspective/eligibility/lifetime boundaries."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_liuli_cave_source as m


def fixture():
    # Minimal grammar with new coordinates, durations, levels and stats; no original article payload.
    coord=''.join(f'（东{i}，南{i+20}）'+('、' if i<8 else '。') for i in range(1,9))
    main='''1.等级要求：建议等级42级。2.特殊要求：解过成人仪式。3.交通工具：步行或骑宠。4.精灵的羽毛：琉璃的羽毛。
    前往南岛奇喀喀村（东1，南2）（东3，南4）东方「森林的独栋房屋"（东5，南6），一位中年人「拉鲁"，由于拉鲁的儿子"伊布"在两个星期前整理房子时，发现他母亲9年前所写的日记。
    拉鲁只有跟伊布讲说他的母亲去世的事情，寻找母亲"雅哈奴"的行踪，伊布还没行成人仪式，因此不可能进入琉璃洞窟。
    "拉鲁的项链"（魅力+7回避率上升+8），交出"雅哈奴的日记"。项链与日记只要掉到地上便会马上消失不见。
    伊布所出现的坐标位置如下：'''+coord+'''
    前往琉璃洞窟（东7，南8），琉璃洞窟9楼时，勇者会遇到一只46级以上的"测试守护甲"；来到14楼后，勇者还会遇到一只57级以上的"测试守护乙"。
    击败9楼的"大地守护兽"才能继续前进，到达11楼时，有些洞口通往死路，有些洞口会让勇者走回10楼，而通往12楼的洞口在（东9，南10）。
    在15楼看到"女神蒂亚特"，此时的宿身正是拉鲁的妻子雅哈奴，宿身是37年改变一次，在宿身改变的那一年第一个生下小孩的母亲，就会被选为宿身。
    雅哈奴在未完成使命前，是无法再次与拉鲁父子相会，一直等伊布来跟她相见。6.获得物品：测试羁绊（攻-8防+9魅+6测试证据）
    此任务是四大属性洞窟之一，与转生任务相关，解过此任务才得以进入碧青的洞窟与漆黑的洞窟；收集四大洞窟的证明，就可以换取不错的宝物。'''
    side='''琉璃洞窟（二）1.等级要求：33级，建议等级44级。2.特殊要求：解过成人仪式。3.交通工具：步行或骑宠。4.精灵的羽毛：琉璃的羽毛。
    前往南岛琉璃洞窟（东7，南8）4楼和"测试审判"（东11，南12）对话，回到琉璃洞窟2楼打一只等级40几级的测试怪，打败测试怪后就可获得"测试羽毛"。
    再次前往琉璃洞窟15楼，和女神蒂亚特说话，再向旁边「测试主人"说话，即可选择大袋或小袋的礼物。哇~我得到了一块测试石6.获得物品：随机。
    玩家可以跟琉璃洞窟（一）一起解，不过由于跟转生没有相关，因此玩家可自行斟酌解或者不解。
    7.琉璃的洞窟坐标：（东7，南8）怪物等级：23~56级怪物种类：甲、乙、丙、丁、戊、己、庚、辛、壬琉璃的洞窟1楼'''
    return ('<meta charset=gb2312><!-- include 发布时间 begin -->2003-06-06 14:55<!-- include 发布时间 end -->'
      '<header>《石器时代》任务功略-琉璃洞窟</header><td class=l15z>'+main+side+'</td>').encode('gb18030')


class LiuliTests(unittest.TestCase):
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

    def test_dynamic_levels_stats_story_intervals_and_coordinates_are_extracted(self):
        ex=m.derive(fixture())
        self.assertEqual(ex['main_quest']['recommended_level'],42)
        self.assertIsNone(ex['main_quest']['hard_entry_level'])
        self.assertEqual(ex['side_quest']['reported_level_requirement'],33)
        self.assertEqual(ex['side_quest']['recommended_level'],44)
        self.assertEqual(ex['delivery_and_reward_items'][0]['stats_as_written'],{'魅力':7,'回避率上升':8})
        self.assertEqual(ex['delivery_and_reward_items'][2]['stats_as_written'],{'攻':-8,'防':9,'魅':6})
        self.assertEqual(ex['narrative']['diary_written_years_before_as_reported'],9)
        self.assertEqual(ex['narrative']['host_cycle_years_as_reported'],37)
        self.assertEqual(ex['guard_occurrences'][1]['level_lower_word_以上'],57)
        self.assertEqual(ex['npc_occurrences'][1]['reported_search_positions'][7],[8,28])
        self.assertEqual(ex['side_quest']['target']['level_literal'],'40几级')
        self.assertIsNone(ex['narrative']['son_age'])
        self.assertFalse(ex['side_quest']['rebirth_required_as_reported'])

    def test_duplicate_hidden_missing_or_unclosed_roots_are_not_evidence(self):
        raw=fixture()
        for changed in [raw+raw,raw.replace(b'class=l15z',b'class=chrome'),raw.replace(b'</td>',b''),
            raw.replace('项链与日记只要掉到地上便会马上消失不见'.encode('gb18030'),'<script>项链与日记只要掉到地上便会马上消失不见</script>'.encode('gb18030'))]:
            with self.assertRaises(ValueError):m.derive(changed)
        self.assertEqual(m.derive(raw),m.derive(raw+b'<script>chrome=2</script>'))

    def test_branch_requirements_perspectives_and_reward_scopes_cannot_be_repaired_by_chrome(self):
        text=fixture().decode('gb18030')
        for old,new in [('特殊要求：解过成人仪式','特殊要求：无需成人仪式'),
            ('掉到地上便会马上消失','注销便会马上消失'),('无法再次与拉鲁父子相会','已经再次与拉鲁父子相会'),
            ('第一个生下小孩的母亲','所有生下小孩的母亲'),('大袋或小袋','大袋和小袋'),
            ('跟转生没有相关','跟转生密切相关'),('获得物品：随机','获得物品：固定')]:
            with self.subTest(old=old):
                with self.assertRaises(ValueError):m.derive((text.replace(old,new)+'<footer>'+old+'</footer>').encode('gb18030'))

    def test_unknowns_rights_source_history_and_narrative_are_not_promoted(self):
        r=json.loads(m.REPORT.read_text());m.verify_report(r)
        changes=[lambda d:d.update(version_profile='TW10'),lambda d:d['negative_boundaries'].pop('diary_age_is_son_age'),
            lambda d:d['catalog_records'][0].update(source_refs=['OTHER']),
            lambda d:d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
            lambda d:d['extraction']['narrative'].update(son_age=14),
            lambda d:d['extraction']['narrative'].update(father_initial_account='MOTHER_IS_DEAD'),
            lambda d:d['extraction']['narrative'].update(real_time_host_rotation_implemented=True),
            lambda d:d['extraction']['main_quest'].update(hard_entry_level=80),
            lambda d:d['extraction']['side_quest'].update(caption_is_guaranteed=True),
            lambda d:d['extraction']['delivery_and_reward_items'][0].update(logout_behavior='vanish'),
            lambda d:d['extraction']['npc_occurrences'][1].update(spawn_selection='EIGHT_INSTANCES'),
            lambda d:d['extraction']['delivery_and_reward_items'][2].update(spirit_name='EARTH'),
            lambda d:d['historical_comparison'].update(independent_witness_count=2)]
        for change in changes:
            d=copy.deepcopy(r);change(d)
            if d['extraction']!=r['extraction']:d['catalog_records']=m.catalog(d['extraction'])
            with self.assertRaises(ValueError):m.verify_report(d)

    def test_parent_and_shared_parser_original_bytes_are_required(self):
        r=json.loads(m.REPORT.read_text())
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for pin in r['parent_pins']+[r['parser_dependency_pin']]:
                p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((m.ROOT/pin['path']).read_bytes())
            with patch.object(m,'ROOT',root):
                m.verify_report(r)
                for pin in r['parent_pins']+[r['parser_dependency_pin']]:
                    p=root/pin['path'];b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]))
                    with self.assertRaises(ValueError):m.verify_report(r)
                    p.unlink()
                    with self.assertRaises(FileNotFoundError):m.verify_report(r)
                    p.write_bytes(b)


if __name__=='__main__':unittest.main()
