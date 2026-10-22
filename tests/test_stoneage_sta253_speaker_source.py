"""Synthetic counterexamples for quote custody and leaking version attribution."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_sta253_speaker_source as m


def page(title, author, date, body):
    fields = {'newsbiaoti': title, 'newsriqi': date, 'zhuozhe_left': '作者：' + author,
              'news': body + '本文言论'}
    return ('<html><meta charset=utf-8><body>' + ''.join(
        f'<div id="{k}">{v}</div>' for k, v in fields.items()) + '</body></html>').encode()


def fixture():
    quotes = ['STA与SACH没有详细资料。', '练功方面测试乙。', '脚本方面测试丙。', '现在混家族测试丁。']
    replies = ['Sta是有对方详细资料。', '2.53的快速战斗。', '无关导航。',
               '2.53可以自己编辑料理脚本。原地遇敌。']
    outer = 'STA还是没有详细资料。STA有快速战斗。自动料理。'
    appendix = '附录 暗夜之狼的原文Sta2.53。' + ''.join(
        f'引用{i + 1}：“{q}”{r}' for i, (q, r) in enumerate(zip(quotes, replies)))
    beta = 'STA2.53bate7 beta7 WIN2000料理还没试用设置为100等待切换信件战斗消息响应慢关掉不知道是否'
    return [page('Sta2.53评论', 'ZHY', '2002-03-27', outer + appendix),
            page('比较', '地藏乌拉', '2002-03-21', ''.join(quotes) + '总体来讲测试结束。'),
            page('试用', '加林多斯', '2002-03-21', beta)]


class SourceTests(unittest.TestCase):
    def test_permanent_files_and_commit_scoped_artifacts_cannot_be_substituted(self):
        receipt = m.verify_custody()
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            receipt_path = root / f'research/recovered/{m.STEM}-CUSTODY-R1.json'
            for pin in receipt['permanent_pins']:
                p = root / pin['path']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((m.ROOT / pin['path']).read_bytes())
            receipt_path.write_text(json.dumps(receipt))
            m.verify_custody(root)
            for pin in receipt['permanent_pins']:
                with self.subTest(path=pin['path']):
                    p = root / pin['path']
                    raw = p.read_bytes()
                    p.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
                    with self.assertRaises(ValueError):
                        m.verify_custody(root)
                    p.unlink()
                    with self.assertRaises(FileNotFoundError):
                        m.verify_custody(root)
                    p.write_bytes(raw)
            for change in [lambda d: d['runs'].append(d['runs'][0]),
                           lambda d: d.update(content_commit='0' * 40),
                           lambda d: d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='other'),
                           lambda d: d.update(historical_bytes_authenticated=True)]:
                changed = copy.deepcopy(receipt)
                change(changed)
                receipt_path.write_text(json.dumps(changed))
                with self.assertRaises(ValueError):
                    m.verify_custody(root)
            receipt_path.unlink()
            with self.assertRaises(FileNotFoundError):
                m.verify_custody(root)

    def test_title_cannot_assign_version_to_outer_or_quoted_speakers(self):
        result = m.derive(fixture())
        self.assertIsNone(result['speaker_sections']['outer_version'])
        self.assertEqual(result['speaker_sections']['quote_versions'], [None] * 4)
        raws = fixture()
        raws[0] = raws[0].replace('原文Sta2.53'.encode(), '原文unknown'.encode())
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_hidden_appendix_and_chrome_cannot_supply_missing_body(self):
        raws = fixture()
        s = raws[0].decode()
        start, end = s.index('附录'), s.index('本文言论')
        changed = s[:start] + '<script>' + s[start:end] + '</script>' + s[end:]
        raws[0] = changed.encode()
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_duplicate_article_fields_and_hidden_publication_rejected(self):
        for raw in [fixture()[0] + b'<div id="news">extra</div>',
                    fixture()[0].replace(b'2002-03-27', b'<script>2002-03-27</script>')]:
            with self.assertRaises(ValueError):
                m.derive([raw] + fixture()[1:])

    def test_quotes_must_match_separately_retrieved_text_and_order(self):
        for index, old, new in [(0, '引用2', '引用3'), (1, '测试乙', '不同措辞')]:
            raws = fixture()
            raws[index] = raws[index].decode().replace(old, new).encode()
            with self.assertRaises(ValueError):
                m.derive(raws)

    def test_beta_untested_cooking_and_unknown_cause_are_not_promoted(self):
        for old, new in [('没试用', '已试用'), ('不知道是否', '确认原因')]:
            raws = fixture()
            raws[2] = raws[2].decode().replace(old, new).encode()
            with self.assertRaises(ValueError):
                m.derive(raws)
        result = m.derive(fixture())['beta_observations']
        self.assertIsNone(result['setting_unit'])
        self.assertFalse(result['same_binary_as_unqualified_253_proven'])

    def test_invisible_text_or_bad_encoding_cannot_repair_missing_feature(self):
        for change in [lambda s: s.replace('原地遇敌', '<script>原地遇敌</script>'),
                       lambda s: s.replace('charset=utf-8', 'charset=gbk')]:
            raws = fixture()
            raws[0] = change(raws[0].decode()).encode()
            with self.assertRaises(ValueError):
                m.derive(raws)
        raws = fixture()
        raws[2] += bytes([255])
        with self.assertRaises(UnicodeDecodeError):
            m.derive(raws)

    def test_parent_files_and_scope_are_required_physical_evidence(self):
        report = json.loads(m.REPORT.read_text())
        m.verify_report(report)
        changed = copy.deepcopy(report)
        changed['scope']['official_game_rules'] = True
        with self.assertRaises(ValueError):
            m.verify_report(changed)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for pin in report['parent_pins']:
                p = root / pin['path']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((m.ROOT / pin['path']).read_bytes())
            with patch.object(m, 'ROOT', root):
                m.verify_report(report)
                p = root / report['parent_pins'][0]['path']
                raw = p.read_bytes()
                p.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
                with self.assertRaises(ValueError):
                    m.verify_report(report)
                p.unlink()
                with self.assertRaises(FileNotFoundError):
                    m.verify_report(report)


if __name__ == '__main__':
    unittest.main()
