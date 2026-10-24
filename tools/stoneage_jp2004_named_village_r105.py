"""Bounded operator-index chronology and separately attributed press claims."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-JP2004-NAMED-VILLAGE-SOURCE-R105.json'
SOURCE_SHA = '530fa72dcb0ffe6265677713af4350ffee0a0e7cec4d5685d57ea5ab3b31692a'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}

def compact(value):
    return ''.join(value.split())

class Page(HTMLParser):
    """Keep visible rows and their own anchors; exclude hidden claim injections."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = []
        self.stack = []
        self.rows = []
        self.visible = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        void = tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr')
        style = compact(a.get('style', '').lower())
        hidden = tag in ('script', 'style') or 'hidden' in a or a.get('aria-hidden', '').lower() == 'true' or 'display:none' in style or 'visibility:hidden' in style
        if self.hidden or hidden:
            if not void:
                self.hidden.append(tag)
            return
        if tag == 'table':
            self.stack.append({'rows': [], 'row': None, 'text': [], 'links': []})
        if tag == 'tr' and self.stack:
            row = {'text': [], 'links': []}
            self.stack[-1]['row'] = row
            self.stack[-1]['rows'].append(row)
        if tag == 'a' and self.stack:
            self.stack[-1]['links'].append(a.get('href'))
            if self.stack[-1]['row'] is not None:
                self.stack[-1]['row']['links'].append(a.get('href'))

    def handle_endtag(self, tag):
        if self.hidden:
            if tag in self.hidden:
                self.hidden = self.hidden[:len(self.hidden) - 1 - self.hidden[::-1].index(tag)]
            return
        if tag == 'tr' and self.stack:
            self.stack[-1]['row'] = None
        if tag == 'table' and self.stack:
            table = self.stack.pop()
            self.tables.append(table)
            self.rows.extend(table['rows'])

    def handle_data(self, value):
        if self.hidden:
            return
        self.visible.append(value)
        if self.stack:
            self.stack[-1]['text'].append(value)
            if self.stack[-1]['row'] is not None:
                self.stack[-1]['row']['text'].append(value)

def parse(raw, codec):
    p = Page()
    p.feed(raw.decode(codec, errors='strict'))
    return p

def operator_rows(raw, expected):
    p = parse(raw, 'cp932')
    result = []
    for e in expected:
        found = [r for r in p.rows if e['href'] in r['links']]
        require(len(found) == 1, 'Missing or ambiguous operator announcement link')
        r = found[0]
        require(r['links'] == [e['href']] and compact(''.join(r['text'])) == compact(e['date'] + e['title']),
                'Operator date/title/anchor reassigned')
        result.append(dict(e))
    return result

def press(raw, expected):
    p = parse(raw, 'utf-8')
    matches = [t for t in p.tables if compact(''.join(t['text'])).startswith('■ストーンエイジ運営元')]
    require(len(matches) == 1, 'Missing or ambiguous StoneAge press section')
    t = matches[0]
    v = compact(''.join(t['text']))
    require('ボーステック' in v and 'DigiPark' in v and '11月9日にアップデートを実施。' in v, 'Press attribution/date changed')
    require(t['links'] == ['http://www.bothtec.co.jp/', 'http://stoneage.to/', 'http://stoneage.to/'], 'Press source links changed')
    bullets = v.split('・')[1:]
    require(bullets == [compact(x) for x in expected[:-1]] + [compact(expected[-1]) + 'http://stoneage.to/'], 'Press update list changed')
    return {'operator_as_reported': 'ボーステック', 'developer_as_reported': 'Digi Park',
            'reported_update_date': '2004-11-09', 'claims': expected,
            'authority': 'CONTEMPORARY_PRESS_NOT_OPERATOR_PATCH_BODY_OR_RUNTIME'}

def contest(raw):
    v = compact(''.join(parse(raw, 'cp932').visible))
    for x in ['応募期間：2004年10月16日～11月2日(23:59まで)',
              '結果発表：2004年11月9日定期メンテナンス終了後、ゲーム内にて反映されます。',
              'ネーミングコンテストの募集は締め切りました。', '11月9日の結果発表をお待ちください！！']:
        require(x in v, 'Contest planned date or closed status changed')
    require('ミライア' not in v and 'カラの村' not in v, 'Pre-result page cannot supply winning names')
    return {'applications': ['2004-10-16', '2004-11-02T23:59'], 'timezone': None,
            'planned_result_and_ingame_reflection': '2004-11-09_AFTER_REGULAR_MAINTENANCE',
            'applications_closed_in_capture': True, 'winning_names_in_this_capture': None,
            'planned_is_executed': False}

def validate(d):
    require(pin(SOURCE.read_bytes())['sha256'] == SOURCE_SHA and d == json.loads(SOURCE.read_bytes()), 'Immutable source contract changed')
    for path, identity in d['parents'].items():
        require(pin((ROOT / path).read_bytes()) == identity, 'Parent changed: ' + path)
    for r in d['records']:
        require(r['game_ids'] is None and r['coordinates'] is None and r['asset_refs'] is None and
                r['runtime_verified'] is False, 'Native map/runtime identity promoted')
    require(d['boundaries']['overall_completion_percentage'] is None and
            d['boundaries']['stage_b_and_wiki'] == 'GATED', 'Project boundary changed')
    return d

def replay(inputs, d):
    validate(d)
    require(set(inputs) == set(d['sources']), 'Finite three source bodies required')
    actual = {}
    for k, raw in inputs.items():
        require(pin(raw)['bytes'] == d['sources'][k]['bytes'] and pin(raw)['sha256'] == d['sources'][k]['sha256'], 'Source bytes changed: ' + k)
        actual[k] = pin(raw)
    return {'schema': 'stoneage.jp2004.named_village_replay.r105', 'source_sha256': SOURCE_SHA,
            'actual_sources': actual, 'operator_rows': operator_rows(inputs['operator_index'], d['operator_rows']),
            'contest': contest(inputs['contest']), 'press': press(inputs['press'], d['press_bullets']),
            'records': d['records'], 'gaps': d['gaps'], 'boundaries': d['boundaries'],
            'negative_http_probes_repeated_by_ci': False, 'original_server_transactions_observed': 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--local-input-dir')
    ap.add_argument('--write', required=True)
    args = ap.parse_args()
    d = json.loads(SOURCE.read_bytes())
    inputs = {}
    for k, e in d['sources'].items():
        if args.local_input_dir:
            raw = (Path(args.local_input_dir) / (k + '.html')).read_bytes()
        else:
            with urlopen(Request(e['url'], headers={'User-Agent': 'Mozilla/5.0 StoneAgeResearch'}), timeout=45) as r:
                require(r.status == 200 and r.url == e['url'], 'Source redirected or failed: ' + k)
                raw = r.read()
        inputs[k] = raw
    report = replay(inputs, d)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    Path(args.write).write_bytes(payload.encode())
    print(json.dumps({'sources': len(inputs), 'operator_rows': len(report['operator_rows']),
                      'report': pin(payload.encode()), 'runtime_observed': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
