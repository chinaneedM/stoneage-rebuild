"""Counterexamples for data-cell scope and interpreting documentary recipes."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_cooking_effect_source as m


def table(rows):
    return '<table>' + ''.join('<tr>' + ''.join('<td>' + v + '</td>' for v in row) + '</tr>' for row in rows) + '</table>'


def page(body, date):
    title = '料理大全' if '15:04' in date else 'PK使用类'
    return ('<html><meta charset=gb2312><body><!-- include 发布时间 begin -->' + date +
            '<!-- include 发布时间 end --><table><tr><td height=30 colspan=4><b>' + title +
            '</b></td></tr><tr><td class=l15z>' + body +
            '</td></tr></table></body></html>').encode('gb18030')


def fixture():
    header = ['名称', '效果', '原料']
    ingredients = '测试材4+对照材4'
    first = table([header, ['占位料理', '回复耐力1', '其他材料']])
    group = '<p>耐力回复类（全体）</p>' + table([header, [m.NAMES[1], '回复耐力222(全体)', ingredients]])
    pk = table([header, [m.NAMES[0], '恢复耐力12+气力34', ingredients + '（只能平时使用，战斗中无效）'],
                [m.NAMES[1], '全体耐力222以上', ingredients], [m.NAMES[2], '单体异常状态恢复', '测试蛋+测试鱼']])
    return [page(first + group, '2003-04-02 15:04'), page(pk, '2003-04-02 16:01')]


class SourceTests(unittest.TestCase):
    def test_catalog_cannot_detach_source_promote_rights_or_create_item_ids(self):
        report = json.loads(m.REPORT.read_text())
        for change in [lambda d: d['catalog_records'][0].update(source_refs=['S2']),
                       lambda d: d['catalog_records'][0].update(rights_status='RELEASE_APPROVED'),
                       lambda d: d['catalog_records'][0].update(game_ids={'item': 7}),
                       lambda d: d['catalog_records'][0].pop('version_profile')]:
            changed = copy.deepcopy(report)
            change(changed)
            with self.assertRaises(ValueError):
                m.verify_report(changed)
        changed = copy.deepcopy(report)
        changed['extraction']['rows'][0]['ingredient_quantities'] = [4, 4]
        changed['catalog_records'] = m.catalog_records(changed['extraction'])
        with self.assertRaises(ValueError):
            m.verify_report(changed)

    def test_values_come_from_cells_without_inventing_grade_count_or_resource_ids(self):
        rows = m.derive(fixture())['rows']
        self.assertEqual(rows[1]['effect_as_written'], '恢复耐力12+气力34')
        self.assertEqual(rows[1]['ingredient_tokens_as_written'], ['测试材4', '对照材4'])
        self.assertNotIn('（', '+'.join(rows[1]['ingredient_tokens_as_written']))
        for row in rows:
            for field in ('ingredient_suffix_meaning', 'ingredient_quantities', 'ingredient_grades',
                          'resource_to_hp_mp_mapping', 'item_id', 'recipe_id', 'success_rate'):
                self.assertIsNone(row[field])

    def test_pk_category_and_hidden_note_cannot_cancel_row_restriction(self):
        raws = fixture()
        old = '只能平时使用，战斗中无效'
        raws[1] = raws[1].decode('gb18030').replace(old, '<script>' + old + '</script>').encode('gb18030')
        with self.assertRaises(ValueError):
            m.derive(raws)
        raws = fixture()
        raws[1] = raws[1].decode('gb18030').replace('<b>PK使用类</b>', '<b>宠物使用</b>').encode('gb18030')
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_hidden_date_or_outside_body_table_cannot_repair_evidence(self):
        raws = fixture()
        raws[0] = raws[0].replace(b'2003-04-02 15:04', b'<script>2003-04-02 15:04</script>')
        with self.assertRaises(ValueError):
            m.derive(raws)
        raws = fixture()
        raws[1] = raws[1].replace(b'class=l15z', b'class=chrome')
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_duplicate_counterpart_and_reordered_pk_rows_rejected(self):
        raws = fixture()
        text = raws[0].decode('gb18030')
        duplicate = '<tr><td>' + m.NAMES[1] + '</td><td>回复耐力222(全体)</td><td>测试材4+对照材4</td></tr>'
        marker = '</table></td>'
        raws[0] = text.replace(marker, duplicate + marker).encode('gb18030')
        with self.assertRaises(ValueError):
            m.derive(raws)
        raws = fixture()
        text = raws[1].decode('gb18030').replace(m.NAMES[0], 'TEMP').replace(m.NAMES[2], m.NAMES[0]).replace('TEMP', m.NAMES[2])
        raws[1] = text.encode('gb18030')
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_invalid_cell_layout_note_and_empty_ingredient_rejected(self):
        for old, new in [('测试蛋+测试鱼', '测试蛋++测试鱼'),
                         ('</td></tr></table></td>', '</tr></table></td>'),
                         ('<td>铁人', '<td colspan="2">铁人')]:
            raws = fixture()
            text = raws[1].decode('gb18030')
            self.assertIn(old, text)
            raws[1] = text.replace(old, new).encode('gb18030')
            with self.assertRaises(ValueError):
                m.derive(raws)

    def test_wording_difference_is_not_a_proven_runtime_conflict(self):
        result = m.derive(fixture())
        self.assertFalse(result['counterpart']['effect_literals_equal'])
        self.assertFalse(result['counterpart']['runtime_contradiction_proven'])
        self.assertFalse(result['counterpart']['same_item_id_established'])
        raws = fixture()
        raws[1] = raws[1].decode('gb18030').replace('单体异常', '全体异常').encode('gb18030')
        with self.assertRaises(ValueError):
            m.derive(raws)

    def test_scope_and_physical_parent_evidence_required(self):
        report = json.loads(m.REPORT.read_text())
        m.verify_report(report)
        changed = copy.deepcopy(report)
        changed['negative_boundaries']['official_operator_authorship_verified'] = True
        with self.assertRaises(ValueError):
            m.verify_report(changed)
        changed = copy.deepcopy(report)
        changed['negative_boundaries'].pop('official_operator_authorship_verified')
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
