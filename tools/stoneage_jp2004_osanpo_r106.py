"""Replay one official manual; project negative rules without claiming success."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from .stoneage_cn2003_katan_visual_r100 import Tables, compact

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-JP2004-OSANPO-SOURCE-R106.json'
SOURCE_SHA = '2cd59ffeff87adc4d0fa6c1530df9e970f8404cf84b62bfd72a625462cbfe40c'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}

class Manual(Tables):
    def __init__(self):
        super().__init__()
        self.images = []
        self.map_name = None
        self.skill_areas = []
        self.fragment_targets = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if self.hidden_tags:
            return
        a = dict(attrs)
        if a.get('id') == 'osanpo' or (tag == 'a' and a.get('name') == 'osanpo'):
            self.fragment_targets.append(tag)
        if tag == 'map':
            self.map_name = a.get('name')
        if tag == 'area' and self.map_name == 'pettec':
            self.skill_areas.append({'coords': a.get('coords'), 'alt': a.get('alt')})
        if tag == 'img' and a.get('src') in ('../image/manual/pet_03.gif', '../image/manual/pet_waza.gif', '../image/manual/pet_osanpo.gif'):
            self.images.append({k: a.get(k) for k in ('src', 'width', 'height', 'usemap')})

    def handle_endtag(self, tag):
        hidden = bool(self.hidden_tags)
        super().handle_endtag(tag)
        if tag == 'map' and not hidden:
            self.map_name = None

def extract(raw, d, check_raw=True):
    if check_raw:
        require(pin(raw) == d['page']['identity'], 'Manual byte identity changed')
    p = Manual()
    p.feed(raw.decode('cp932', errors='strict'))
    result = []
    for e in d['sections']:
        cells = [(ti, ri, ci, compact(c['text'])) for ti, rows in enumerate(p.tables)
                 for ri, row in enumerate(rows) for ci, c in enumerate(row)
                 if compact(c['text']).startswith(e['heading'])]
        require(len(cells) == 1, 'Missing or ambiguous manual section')
        ti, ri, ci, text = cells[0]
        actual = {'table_close_ordinal': ti, 'row': ri, 'column': ci,
                  'normalized_utf8_bytes': len(text.encode()),
                  'normalized_sha256': hashlib.sha256(text.encode()).hexdigest()}
        require(actual == e['identity'], 'Manual section position or text changed')
        result.append({'topic': e['topic'], **actual})
    actual_ui = {'image_references': p.images, 'skill_map_areas': p.skill_areas,
                 'osanpo_fragment_targets': p.fragment_targets}
    require(actual_ui == d['html_metadata'], 'Manual HTML image/map/fragment metadata changed')
    return result, actual_ui

def blocker_projection(low_loyalty, mail_state):
    """Derived specification only; the manual gives no complete success predicate."""
    require(all(v is None or type(v) is bool for v in (low_loyalty, mail_state)), 'Only qualitative boolean/unknown inputs; no guessed numeric threshold')
    reasons = []
    if low_loyalty is True:
        reasons.append('LOW_LOYALTY')
    if mail_state is True:
        reasons.append('MAIL_STATE')
    return {'qualitative_low_loyalty': low_loyalty, 'mail_state': mail_state,
            'documented_blockers': reasons,
            'verdict': 'BLOCKED_BY_DOCUMENTED_RULE' if reasons else 'SUFFICIENCY_UNPROVEN',
            'original_execution_observed': False}

def projection_table():
    return [blocker_projection(low, mail) for low in (True, False, None) for mail in (True, False, None)]

def validate(d):
    require(pin(SOURCE.read_bytes())['sha256'] == SOURCE_SHA and d == json.loads(SOURCE.read_bytes()), 'Immutable source contract changed')
    for path, identity in d['parents'].items():
        require(pin((ROOT / path).read_bytes()) == identity, 'Parent identity changed: ' + path)
    rules = d['rules']
    require(rules['osanpo']['loyalty_threshold'] is None and rules['osanpo']['teaching_shop_entry_conditions'] is None and
            rules['learning']['skill_capacity_number'] is None, 'Invented numeric or teaching condition')
    require(rules['learning']['direct_forget_described'] is False and rules['learning']['overwrite_with_another_skill_described'] is True and
            rules['learning']['reorder_described'] is False, 'Learning rule polarity changed')
    require(projection_table() == d['derived_blocker_table'], 'Documented necessary conditions promoted to sufficient success')
    return d

def replay(raw, d):
    validate(d)
    sections, ui = extract(raw, d)
    return {'schema': 'stoneage.jp2004.osanpo_replay.r106', 'source_sha256': SOURCE_SHA,
            'actual_page': pin(raw), 'sections': sections, 'html_metadata': ui,
            'rules': d['rules'], 'derived_blocker_table': projection_table(), 'records': d['records'],
            'image_probe': d['image_probe'], 'image_probe_repeated_by_ci': False,
            'boundaries': d['boundaries'], 'original_server_transactions_observed': 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--local-html')
    ap.add_argument('--write', required=True)
    args = ap.parse_args()
    d = json.loads(SOURCE.read_bytes())
    if args.local_html:
        raw = Path(args.local_html).read_bytes()
    else:
        with urlopen(Request(d['page']['url'], headers={'User-Agent': 'Mozilla/5.0 StoneAgeResearch'}), timeout=45) as r:
            require(r.status == 200 and r.url == d['page']['url'], 'Manual redirected or failed')
            raw = r.read()
    report = replay(raw, d)
    payload = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    Path(args.write).write_bytes(payload)
    print(json.dumps({'page': report['actual_page'], 'sections': len(report['sections']),
                      'qualitative_projection_cases': len(report['derived_blocker_table']),
                      'report': pin(payload), 'runtime_observed': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
