"""Synthetic source-layout and evidence-attribution counterexamples."""
import copy
import json
import unittest
from tools import stoneage_dinosaur_quest_source as m


def fixtures():
    # Artificial short HTML; unrelated names distinguish extraction from fixed output.
    credit = '游民部落网友松鼠1206提供'
    i = credit + '<a href="/handbook/0101/01186091_c2.shtml#17">入口</a>'
    s = (credit + '<a name="17">恐龙博士<p>过桥后的测试兽甲，等级十五以上。'
         '练到十八级以上就可换到测试护符（光之精灵）或同等的装备。'
         '第二个是南岛的测试兽乙（绿毛老虎），等级三十，养到三十级，'
         '叫测试赠宠的银色小龙LV1。<a name="18">其它任务')
    t = ('2003-05-29 11:37 网友投稿 恐龙博士（一）1.等级要求：建议等级15级。'
         '"柯奥山的小洞窟"（东328，南633）六楼，"恐龙博士"。'
         '恐龙博士"测试博士"（东11，南12），"助手测试助理"详细询问。'
         '等级15级以上的测试兽丙，如果。超过1只以上的鲁尼帖斯。'
         '最好的东西为"测试护符乙"（魅+1光的精灵）。'
         '恐龙博士（二）1.等级要求：建议等级25级。特殊要求：解过恐龙博士（一）'
         '确定博士要的恐龙是等级30的测试兽丁（绿虎），并没有等级30以上的贝鲁卡。'
         '超过1只以上的贝鲁卡。连身上骑的贝鲁卡也要小心。获得宠物："测试赠宠乙"。'
         '7.柯奥山的小洞窟')
    # The early page must explicitly carry the top-floor wording.
    s = s.replace('恐龙博士<p>', '恐龙博士<p>最上层')
    return [v.encode('gb18030') for v in (i, s, t)]


class SourceTests(unittest.TestCase):
    def test_captures_actual_names_without_crossing_previous_quote(self):
        d = m.extract(fixtures())
        self.assertEqual(d['dated_2003']['npc']['name'], '测试博士')
        self.assertEqual(d['dated_2003']['assistant']['name'], '测试助理')
        self.assertEqual(d['compiler']['quest_1']['target_label'], '测试兽甲')
        self.assertEqual(d['dated_2003']['quest_1']['target_label'], '测试兽丙')

    def test_player_recommendations_never_become_pet_or_access_gates(self):
        d = m.extract(fixtures())['dated_2003']
        self.assertEqual(d['quest_2']['recommended_player_level'], 25)
        self.assertEqual(d['quest_2']['requested_level'], 30)
        self.assertIsNone(d['quest_1']['required_player_level'])
        self.assertIsNone(d['quest_2']['reward_level'])

    def test_actual_link_and_order_are_required(self):
        for i, a, b in [(0, '#17', '#18'), (1, 'name="18"', 'name="17"')]:
            raws = fixtures()
            raws[i] = raws[i].replace(a.encode(), b.encode())
            with self.assertRaises(ValueError):
                m.extract(raws)

    def test_hidden_text_cannot_repair_missing_level_predecessor(self):
        raws = fixtures()
        phrase = '特殊要求：解过恐龙博士（一）'.encode('gb18030')
        raws[2] = raws[2].replace(phrase, b'<script>' + phrase + b'</script>')
        with self.assertRaises(ValueError):
            m.extract(raws)

    def test_selected_encoding_damage_is_rejected_not_silently_ignored(self):
        raws = fixtures()
        raws[1] = raws[1].replace('最上层'.encode('gb18030'), b'\x81')
        with self.assertRaises(ValueError):
            m.extract(raws)

    def test_archive_rejects_promotion_and_source_detachment(self):
        d = json.loads(m.REPORT.read_text())
        m.check_archive(d)
        for field, value in [('runtime_verified', True), ('exact_build', 'TW10'),
                             ('historical_bytes_authenticated', True),
                             ('independent_source_authors_established', True)]:
            changed = copy.deepcopy(d)
            changed['scope'][field] = value
            with self.assertRaises(ValueError):
                m.check_archive(changed)
        for transform in [lambda r: r.pop('source_refs'),
                          lambda r: r.update(game_ids={'npc': 1}),
                          lambda r: r.update(version_profile='TW10'),
                          lambda r: r['source_relation'].update(target_label='鲁尼帖斯')]:
            changed = copy.deepcopy(d)
            transform(changed['archive_records'][0])
            with self.assertRaises((ValueError, KeyError)):
                m.check_archive(changed)


if __name__ == '__main__':
    unittest.main()
