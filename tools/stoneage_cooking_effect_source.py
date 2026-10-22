"""Bounded documentary cooking rows; no original server formulas or item IDs."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-COOKING-EFFECT'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URLS = ('https://games.sina.com.cn/zhqu/sta/lldq/lldq_2.shtml',
        'https://games.sina.com.cn/zhqu/sta/lldq/lldq_4.shtml')
NAMES = ('铁人关东煮', '豪华生鱼片', '青鱼子')
PROFILE = 'CN2003_SINA_COOKING_DOCUMENT_EXACT_GAME_BUILD_UNKNOWN'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(text):
    return re.sub(r'\s+', '', text)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'iframe'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'iframe') and self.hidden:
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)


def plain(text):
    parser = Visible()
    parser.feed(text)
    return compact(''.join(parser.parts))


class BodyTables(HTMLParser):
    """Keep leaf table cells inside the unique article container, not navigation."""
    def __init__(self):
        super().__init__()
        self.td_depth = 0
        self.active_depth = None
        self.roots = 0
        self.hidden = 0
        self.stack = []
        self.tables = []
        self.visible = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'iframe'):
            self.hidden += 1
        if self.hidden:
            return
        attrs = dict(attrs)
        if tag in ('td', 'th'):
            self.td_depth += 1
            if 'l15z' in attrs.get('class', '').split():
                self.roots += 1
                require(self.active_depth is None, 'Nested article containers')
                self.active_depth = self.td_depth
        if self.active_depth is None:
            return
        if tag == 'table':
            require(not self.stack, 'Nested article tables are not a supported source layout')
            self.stack.append({'context': compact(''.join(self.visible)), 'rows': [], 'row': None, 'cell': None})
        elif tag == 'tr' and self.stack:
            require(self.stack[-1]['row'] is None, 'Unclosed table row')
            self.stack[-1]['row'] = []
        elif tag in ('td', 'th') and self.stack:
            require(self.stack[-1]['row'] is not None and self.stack[-1]['cell'] is None, 'Unscoped table cell')
            require(not any(k in attrs and attrs[k] != '1' for k in ('rowspan', 'colspan')), 'Unexpected cell span')
            self.stack[-1]['cell'] = []

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'iframe'):
            if self.hidden:
                self.hidden -= 1
            return
        if self.hidden:
            return
        if self.active_depth is not None:
            if tag in ('td', 'th') and self.stack:
                table = self.stack[-1]
                require(table['cell'] is not None, 'Table cell end without start')
                table['row'].append(compact(''.join(table['cell'])))
                table['cell'] = None
            elif tag == 'tr' and self.stack:
                table = self.stack[-1]
                require(table['cell'] is None and table['row'] is not None, 'Malformed row end')
                table['rows'].append(table['row'])
                table['row'] = None
            elif tag == 'table':
                require(self.stack and self.stack[-1]['row'] is None, 'Malformed table end')
                table = self.stack.pop()
                self.tables.append({'context': table['context'], 'rows': table['rows']})
            if tag in ('td', 'th') and self.td_depth == self.active_depth:
                require(not self.stack, 'Article ended before table')
                self.active_depth = None
        if tag in ('td', 'th'):
            self.td_depth -= 1

    def handle_data(self, text):
        if self.active_depth is not None and not self.hidden:
            self.visible.append(text)
            if self.stack and self.stack[-1]['cell'] is not None:
                self.stack[-1]['cell'].append(text)


def article(raw, date, title):
    text = raw.decode('gb18030', errors='strict')
    require(re.search(r'charset=["\x27]?gb2312', text, re.I), 'Source charset declaration changed')
    dates = re.findall(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->', text, re.S)
    require(len(dates) == 1 and plain(dates[0]) == date, 'Visible publication changed')
    titles = re.findall(r'<td\b(?=[^>]*\bheight\s*=\s*["\x27]?30\b)(?=[^>]*\bcolspan\s*=\s*["\x27]?4\b)[^>]*>(.*?)</td>',
                        text, re.I | re.S)
    require(len(titles) == 1 and plain(titles[0]) == title, 'Visible article title changed')
    parser = BodyTables()
    parser.feed(text)
    require(parser.roots == 1 and parser.active_depth is None and not parser.stack, 'Article container missing/duplicated/unclosed')
    tables = [table for table in parser.tables if table['rows'] and table['rows'][0] == ['名称', '效果', '原料']]
    return tables


def row_record(source, row, category):
    require(len(row) == 3 and all(row), 'Three nonempty source cells required')
    name, effect, original = row
    ingredients, note = original, None
    if '（' in original:
        require(original.count('（') == original.count('）') == 1 and original.endswith('）'), 'Ambiguous ingredient note')
        ingredients, note = original[:-1].split('（')
    tokens = ingredients.split('+')
    require(all(tokens), 'Empty ingredient token')
    return {'source_ref': source, 'category_as_written': category,
            'name_as_written': name, 'effect_as_written': effect,
            'ingredient_cell_as_written': original, 'ingredient_tokens_as_written': tokens,
            'use_note_as_written': note, 'ingredient_suffix_meaning': None,
            'ingredient_quantities': None, 'ingredient_grades': None,
            'resource_to_hp_mp_mapping': None, 'item_id': None, 'recipe_id': None,
            'success_rate': None, 'runtime_verified': False}


def derive(raws):
    recovery = article(raws[0], '2003-04-0215:04', '料理大全')
    pk = article(raws[1], '2003-04-0216:01', 'PK使用类')
    require(len(recovery) == 2 and len(pk) == 1, 'Unexpected recipe table scope')
    require(recovery[1]['context'].endswith('耐力回复类（全体）'), 'Group-recovery section moved or renamed')
    selected = [r for r in recovery[1]['rows'][1:] if r and r[0] == NAMES[1]]
    require(len(selected) == 1, 'Recovery counterpart missing/duplicated')
    rows = pk[0]['rows'][1:]
    require([r[0] for r in rows] == list(NAMES), 'PK rows changed order or membership')
    records = [row_record('S1', selected[0], '耐力回复类（全体）')]
    records += [row_record('S2', row, 'PK使用类') for row in rows]
    iron, sashimi, roe = records[1:]
    require(re.fullmatch(r'恢复耐力\d+\+气力\d+', iron['effect_as_written']), 'Two reported resource labels changed')
    require(iron['use_note_as_written'] == '只能平时使用，战斗中无效', 'Outside-combat restriction changed')
    require(re.fullmatch(r'回复耐力\d+\(全体\)', records[0]['effect_as_written']) and
            re.fullmatch(r'全体耐力\d+以上', sashimi['effect_as_written']), 'Recovery wording relation changed')
    require(roe['effect_as_written'] == '单体异常状态恢复' and roe['use_note_as_written'] is None,
            'Status cure expanded or note invented')
    require(sashimi['ingredient_tokens_as_written'] == records[0]['ingredient_tokens_as_written'], 'Counterpart ingredient strings differ')
    require(all(re.fullmatch(r'[^0-9]+4', token) for token in iron['ingredient_tokens_as_written'] + sashimi['ingredient_tokens_as_written']),
            'Numeric ingredient suffix changed')
    return {'schema': 'stoneage.cooking_effect.extraction.r1', 'rows': records,
            'counterpart': {'same_display_name': True, 'same_ingredient_literals': True,
                            'effect_literals_equal': records[0]['effect_as_written'] == sashimi['effect_as_written'],
                            'same_item_id_established': False, 'runtime_contradiction_proven': False,
                            'numeric_effects_reconciled': False},
            'category_does_not_override_row_restriction': True,
            'all_abnormal_status_types_recovered': False, 'all_other_recipes_archived': False,
            'exact_game_build': None, 'author_identity': None, 'historical_bytes_authenticated': False}


def catalog_records(extraction):
    return [{'record_id': f'CN2003-SINA-R67-RECIPE-{i + 1:02}',
             'entity_type': 'documentary_recipe_description', 'collection': 'recipes',
             'version_profile': PROFILE, 'source_refs': [row['source_ref']],
             'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME',
             'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'record_revision': 1,
             'game_ids': None, 'content': row} for i, row in enumerate(extraction['rows'])]


def verify_report(report):
    require(report['version_profile'] == PROFILE and report['rights_status'] == 'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
            'Version/rights promotion')
    expected = {k: False for k in ('official_operator_authorship_verified', 'exact_game_build_verified',
                'tw10_rules_backfilled', 'same_item_ids_proven', 'runtime_formula_recovered',
                'all_abnormal_statuses_cured', 'all_recipes_recovered',
                'ingredient_suffix_quantity_or_grade_decoded', 'hp_mp_mapping_proven',
                'original_html_or_assets_committed', 'new_game_production_started')}
    require(report['negative_boundaries'] == expected, 'Missing or promoted evidence boundary')
    require(report['catalog_records'] == catalog_records(report['extraction']), 'Catalog detached from source rows')
    for row in report['extraction']['rows']:
        require(all(row[k] is None for k in ('ingredient_suffix_meaning', 'ingredient_quantities',
                    'ingredient_grades', 'resource_to_hp_mp_mapping', 'item_id', 'recipe_id', 'success_rate')) and
                row['runtime_verified'] is False, 'Unknown row fields promoted')
    for pin in report['parent_pins']:
        raw = (ROOT / pin['path']).read_bytes()
        require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'Parent evidence changed')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest() == pin['git_blob'],
                'Parent Git identity changed')


MUTATIONS = (
    (0, '2003-04-02 15:04', '2003-04-03 15:04'),
    (1, '2003-04-02 16:01', '2003-04-03 16:01'),
    (0, '回复耐力500(全体)', '回复耐力400(全体)'),
    (1, '全体耐力500以上', '全体耐力500'),
    (1, '恢复耐力300+气力100', '恢复耐力100+气力300'),
    (1, '只能平时使用，战斗中无效', '平时战斗均可使用'),
    (1, '单体异常状态恢复', '全体异常状态恢复'),
    (1, '鱼4+螃蟹4+花枝4+章鱼4+虾4', '鱼4+螃蟹4+花枝4+章鱼4+虾5'),
    (1, '刚产的蛋+深海鱼', '刚产的蛋+淡水鱼'),
    (0, '耐力回复类（全体）', '耐力回复类（单体）'),
    (1, '铁人关东煮', '铁人关东烤'),
    (1, '<b>PK使用类</b>', '<b>宠物使用</b>'),
)


def audit(raws, expected):
    for index, old, new in MUTATIONS:
        text = raws[index].decode('gb18030')
        require(old in text, 'Real-source mutation did not match')
        changed = list(raws)
        changed[index] = text.replace(old, new).encode('gb18030')
        try:
            actual = derive(changed)
        except ValueError:
            continue
        require(actual != expected, 'Semantic mutation accepted')
    for index in range(2):
        changed = list(raws)
        changed[index] += b'<script>outside_article=1;</script>'
        require(derive(changed) == expected, 'Peripheral script changed selected rows')
    return {'real_source_semantic_mutations_rejected_without_digest_gate': len(MUTATIONS),
            'two_peripheral_script_positives': True, 'original_game_runtime_verified': False}


def verify_custody(root=None):
    root = ROOT if root is None else Path(root)
    receipt = json.loads((root / f'research/recovered/{STEM}-CUSTODY-R1.json').read_text())
    require(receipt['original_game_runtime_verified'] is False and
            receipt['historical_bytes_authenticated'] is False, 'Custody authority promoted')
    runs = receipt['runs']
    require(len({r['id'] for r in runs}) == len(runs) and all(
        r['head_sha'] == receipt['content_commit'] and r['status'] == 'completed' and
        r['conclusion'] == 'success' for r in runs), 'CI provenance changed')
    pins = receipt['permanent_pins']
    paths = {p['path'] for p in pins}
    required = {f'research/recovered/{STEM}-{s}-R1.json' for s in ('SOURCE', 'CI-CANDIDATE', 'CI-MAIN')}
    require(len(paths) == len(pins) and required <= paths, 'Incomplete/duplicate evidence pins')
    for pin in pins:
        require(not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts, 'Invalid pin path')
        raw = (root / pin['path']).read_bytes()
        require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'Permanent evidence changed')
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest() == pin['git_blob'],
                'Permanent Git identity changed')
    source = json.loads((root / f'research/recovered/{STEM}-SOURCE-R1.json').read_text())
    require({p['path'] for p in source['parent_pins']} <= paths, 'Parent custody incomplete')
    inputs = [{k: p[k] for k in ('id', 'url', 'bytes', 'sha256')} for p in source['source_pages']]
    for role in ('candidate', 'main'):
        proof = receipt['jobs_and_artifacts'][role]
        matches = [r for r in runs if r['id'] == proof['run']]
        artifact = proof['artifact']['workflow_run']
        require(len(matches) == 1 and artifact['id'] == proof['run'] and
                artifact['head_sha'] == receipt['content_commit'] and
                artifact['head_branch'] == matches[0]['branch'] and
                matches[0]['branch'] == ('main' if role == 'main' else receipt['candidate_branch']),
                'Artifact detached from content/run/branch')
        raw = json.loads((root / f'research/recovered/{STEM}-CI-{role.upper()}-R1.json').read_text())
        require(raw['inputs'] == inputs and raw['extraction'] == source['extraction'] and
                raw['catalog_records'] == source['catalog_records'], 'Archived source or catalog replay changed')
        require(raw['audit'] == {'real_source_semantic_mutations_rejected_without_digest_gate': 12,
                                'two_peripheral_script_positives': True, 'original_game_runtime_verified': False} and
                raw['original_html_or_assets_in_output'] is False and
                raw['original_game_runtime_verified'] is False, 'Archived audit boundary promoted')
    return receipt


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true')
    group.add_argument('--inputs', nargs=2)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = json.loads(REPORT.read_text())
    verify_report(report)
    verify_custody()
    raws, inputs = [], []
    for i, url in enumerate(URLS):
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as response:
                require(response.status == 200 and response.url == url, 'HTTP source identity changed')
                raw = response.read(2_000_001)
        else:
            raw = Path(args.inputs[i]).read_bytes()
        require(len(raw) <= 2_000_000, 'Source size exceeds bound')
        raws.append(raw)
        inputs.append({'id': f'S{i + 1}', 'url': url, 'bytes': len(raw), 'sha256': sha(raw)})
    actual = derive(raws)
    require(actual == report['extraction'], 'Selected source semantics changed')
    out = {'schema': 'stoneage.cooking_effect.replay.r1', 'inputs': inputs, 'extraction': actual,
           'catalog_records': catalog_records(actual),
           'audit': audit(raws, actual),
           'original_html_or_assets_in_output': False, 'original_game_runtime_verified': False}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'selected_source_rows': len(actual['rows'])}))


if __name__ == '__main__':
    main()
