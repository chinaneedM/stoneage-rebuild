"""Bounded documentary comparison of two migrated player pages, never game rules."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-SCENE37-NEWBIE-QUEST-PLAYER-SOURCE-R1.json'
URLS = {
    'player2004': 'https://news.17173.com/z/stoneage/content/2004-9-21/n78_994850.html',
    'player2006': 'https://news.17173.com/z/stoneage/content/2006-05-12/1147416247.shtml',
}
PROJECTION_SHA = 'f72d57f2dd24743647c628d3a9f17e6866975a5eef75f9d49d24a23fd08a8600'
REPORT_SHA = 'bcb285db32e1df8085d89f4a5703fc7af1019fe1e4fb6c5a0dfe4cd7e419e94f'


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def compact(s):
    return ''.join(unicodedata.normalize('NFKC', s).split())


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


class NewsText(Text):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.matches = 0
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if dict(attrs).get('id') == 'news':
                need(self.depth == 0, 'nested duplicate article')
                self.matches += 1
                self.depth = 1
            elif self.depth:
                self.depth += 1
        if self.depth and tag in ('script', 'style'):
            self.ignored += 1

    def handle_endtag(self, tag):
        if self.depth and tag in ('script', 'style'):
            self.ignored -= 1
        if self.depth and tag == 'div':
            self.depth -= 1

    def handle_data(self, text):
        if self.depth and not self.ignored:
            self.parts.append(text)


class Rows(HTMLParser):
    """Recover reading lines across four cells; DOM cell-major text scrambles them."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        need(tag not in ('script', 'style', 'font'), 'unexpected selected markup')
        if tag == 'tr':
            need(self.row is None, 'nested row')
            self.row = []
        elif tag == 'td':
            need(self.row is not None and self.cell is None, 'nested or orphan cell')
            self.cell = ['']
        elif tag == 'br':
            need(self.cell is not None, 'orphan line break')
            self.cell.append('')

    def handle_endtag(self, tag):
        if tag == 'td':
            need(self.cell is not None, 'orphan cell end')
            self.row.append([compact(x) for x in self.cell])
            self.cell = None
        elif tag == 'tr':
            need(self.row is not None and self.cell is None, 'unclosed cell')
            need(len(self.row) == 4, 'four source columns required')
            self.rows.append(self.row)
            self.row = None

    def handle_data(self, text):
        if self.cell is not None:
            self.cell[-1] += text


def text_of(html):
    p = Text(); p.feed(html)
    return compact(''.join(p.parts))


def extract_2004(raw):
    s = raw.decode('utf-8', errors='strict')
    need('\ufffd' not in s, 'replacement character')
    heading = '手骑宠跳级任务'
    need(s.count(heading) == 1, 'unique damaged heading')
    begin = s.rfind('<tr>', 0, s.index(heading))
    last = s.find('１０．这个任务只', begin)
    end = s.find('</tr>', last)
    need(begin >= 0 and last > begin and end > last, 'bounded task table')
    selected = s[begin:end + 5]
    p = Rows(); p.feed(selected)
    need(p.row is None and len(p.rows) == 12, 'exact heading/condition/ten rows')
    rows = [''.join(''.join(c[i] if i < len(c) else '' for c in row)
                    for i in range(max(map(len, row)))) for row in p.rows]
    need(rows[0] == heading and rows[1] == '任务条件:30级以下新人', 'literal source heading and gate')
    steps = rows[2:]
    for i, step in enumerate(steps, 1):
        need(step.startswith(str(i) + '.'), 'ordered numbered steps')
    return {'heading_as_written': rows[0], 'condition_as_written': rows[1],
            'selected_raw_sha256': digest(selected.encode()),
            'normalized_steps': steps, 'table_rows': 12, 'table_columns': 4}


def extract_2006(raw):
    s = raw.decode('utf-8', errors='strict')
    need('\ufffd' not in s, 'replacement character')
    p = NewsText(); p.feed(s)
    need(p.matches == 1 and p.depth == 0, 'one complete article container')
    t = compact(''.join(p.parts))
    begin = '任务条件:刚出生的1级人'
    finish = '能力值约是野生的一半'
    starts = [m.start() for m in re.finditer(re.escape(begin), t)]
    ends = [m.end() for m in re.finditer(re.escape(finish), t)]
    need(len(starts) == len(ends) == 2 and starts[0] < ends[0] < starts[1] < ends[1], 'two bounded repeated comparison sections')
    selected = t[starts[0]:ends[0]]
    need(selected == t[starts[1]:ends[1]], 'internal repeated section changed')
    chunks = re.split(r'(?<!\d)(10|[1-9])\.', selected)
    need(chunks[0] == begin and len(chunks) == 21, 'comparison ten steps')
    steps = [chunks[i] + '.' + chunks[i+1] for i in range(1, 21, 2)]
    need([x.split('.', 1)[0] for x in steps] == [str(i) for i in range(1,11)], 'comparison step order')
    return {'condition_as_written': begin, 'normalized_steps': steps,
            'identical_selected_section_occurrences': 2}


def source_projection(raws):
    a, b = extract_2004(raws['player2004']), extract_2006(raws['player2006'])
    for k, expected in [('player2004', ('2004-09-21', '疾风精灵〈武汉1〉')),
                        ('player2006', ('2006-05-12', '神之舞-狼狼'))]:
        t = text_of(raws[k].decode('utf-8'))
        need(all(compact(x) in t for x in expected), 'display date or byline missing')
    for k, x in [('player2004', a), ('player2006', b)]:
        steps = x.pop('normalized_steps')
        x['normalized_step_sha256'] = [digest(t.encode()) for t in steps]
        x['normalized_section_sha256'] = digest((x['condition_as_written'] + ''.join(steps)).encode())
        x['normalized_step_chars'] = [len(t) for t in steps]
        x['normalization'] = 'NFKC_AND_WHITESPACE_ONLY_NOT_TEXT_REPAIR'
        x['original_publication_bytes_verified'] = False
    a_steps = extract_2004(raws['player2004'])['normalized_steps']
    b_steps = extract_2006(raws['player2006'])['normalized_steps']
    equal = [i+1 for i, (x,y) in enumerate(zip(a_steps,b_steps)) if x == y]
    return {'player2004': a, 'player2006': b,
            'equal_numbered_steps_after_declared_normalization': equal,
            'two_independent_runtime_witnesses': False}


def fetch_sources():
    raws, receipts = {}, {}
    for k, url in URLS.items():
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=40) as r:
            raw = r.read(1048577)
            need(len(raw) <= 1048576 and r.status == 200 and r.url == url, 'HTTP scope or redirect')
            need('text/html' in r.headers.get('Content-Type', ''), 'HTML content type')
            raws[k] = raw
            receipts[k] = {'requested': url, 'resolved': r.url, 'status': r.status,
                           'bytes': len(raw), 'sha256': digest(raw)}
    return raws, receipts


def validate(report):
    need(report['schema'] == 'stoneage.scene37.newbie_quest_player_source.r1', 'schema')
    need(len(report['prior_materials']) == 8, 'all eight deduplicated prior reports')
    for p in report['prior_materials']:
        b = (ROOT / p['path']).read_bytes()
        need(len(b) == p['bytes'] and digest(b) == p['sha256'], 'prior material changed')
    need(report['source_projection']['equal_numbered_steps_after_declared_normalization'] == list(range(1,9)) + [10], 'textual dependence boundary')
    need(report['quest']['origin_class'] == 'ORIGIN_UNRESOLVED', 'quest origin not authenticated')
    need(report['quest']['reported_level_targets'] == [10,20,31], 'destination levels, not XP amounts')
    need(report['quest']['server_XP_amounts'] is None and report['quest']['native_NPC_item_quest_ids'] is None, 'no invented native values')
    need(report['source_projection']['player2004']['heading_as_written'] == '手骑宠跳级任务', 'do not repair missing heading character')
    need(report['source_projection']['player2004']['condition_as_written'] == '任务条件:30级以下新人', '2004 gate')
    need(report['source_projection']['player2006']['condition_as_written'] == '任务条件:刚出生的1级人', '2006 gate tension')
    need(digest(canonical(report['source_projection'])) == PROJECTION_SHA, 'fixed selected source identities')
    need(report['quest']['flow'][1]['recipe_numbers_are_quantities_or_grades'] is None, 'recipe tokens not invented quantities')
    need(report['quest']['flow'][2]['source_pet_label'] == '布依', 'source spelling not merged with another pet name')
    need(report['quest']['qualification_disagreement']['level30_inclusive'] is None, 'below-thirty inclusivity unresolved')
    need(report['novelty']['independent_server_witnesses'] == 0, 'text similarity not independent runtime')
    need(all(v is False for v in report['unproven'].values()), 'unproven promotion')
    need(report['overall_percent'] is None, 'completion unknown')
    need(digest(canonical(report)) == REPORT_SHA, 'immutable documentary report')
    return {'documentary_quest_chains': 1, 'player_pages': 2, 'official_deployment_proven': False, 'original_world_entered': False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-dir');p.add_argument('--replay-live',action='store_true');p.add_argument('--output');a=p.parse_args()
    report=json.loads(REPORT.read_bytes()); result=validate(report)
    if a.source_dir or a.replay_live:
        need(not (a.source_dir and a.replay_live), 'one source mode')
        if a.source_dir:
            raws={k:(Path(a.source_dir)/(k+'.html')).read_bytes() for k in URLS};receipts=None
        else:
            raws, receipts=fetch_sources()
        need(source_projection(raws)==report['source_projection'], 'selected source content drift')
        result={'source_projection': source_projection(raws), 'HTTP':receipts, 'raw_sources_in_artifact':False,
                'original_server_executed':False,'original_world_entered':False}
    if a.output:
        Path(a.output).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result if not a.output else {'derived_output_written':True,'original_world_entered':False}))


if __name__ == '__main__':
    main()
