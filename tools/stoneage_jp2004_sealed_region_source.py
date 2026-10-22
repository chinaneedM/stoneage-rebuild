"""Finite press-qualified map/pet-behavior attribution; no original game runtime."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from tools.stoneage_jp2004_chat_update_source import extract as july_extract

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2004-SEALED-REGION'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URLS = ('https://www.4gamer.net/news/history/2004.07/20040730231235detail.html',
        'https://www.4gamer.net/news/history/2004.09/20040917191201detail.html')
PROFILE = 'JP2004_4GAMER_OFFICIAL_PRODUCT_PRESS_REPORTED_BUILD_UNVERIFIED'
BEGIN, END = '<!-- 本文開始 -->', '<!-- 本文終了 -->'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts, self.links = [], []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if tag == 'a' and not self.hidden:
            self.links.append(dict(attrs).get('href'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def compact(t):
    p = Visible()
    p.feed(t)
    return re.sub(r'\s+', '', ''.join(p.parts)), p.links


def match(pattern, t):
    m = re.search(pattern, t)
    require(m is not None, 'Changed source assertion: ' + pattern)
    return m.groups()


def article(raw):
    s = raw.decode('cp932', errors='strict')
    require('charset=Shift_JIS' in s, 'Source charset declaration changed')
    bodies = re.findall(r'<body\b[^>]*>(.*?)</body\s*>', s, re.I | re.S)
    require(len(bodies) == 1 and '2004/09/1719:12' in compact(bodies[0])[0], 'Visible publication changed')
    slots = re.findall(re.escape(BEGIN) + '(.*?)' + re.escape(END), s, re.S)
    require(s.count(BEGIN) == s.count(END) == len(slots) == 5, 'Template source slots changed')
    require(all(not compact(t)[0] for t in slots[1:]), 'Unexpected extra article text')
    text, links = compact(slots[0])
    cutoff = '→「ストーンエイジ」の記事一覧'
    require(text.count(cutoff) == 1, 'Article end boundary changed')
    text = text.split(cutoff)[0]
    return text, links


def extract(raw):
    text, links = article(raw)
    require(links.count('http://stoneage.to/') == 1, 'Historical official-site literal missing')
    require('本日（9月17日）アップデートが行われた' in text, 'Reported completion changed')
    ordinal, update_name = match(r'今回行われた(第三弾)となるアップデートは，"([^"]+)"と題され', text)
    require('二つの大きな追加' in text, 'Two update categories changed')
    cave, region = match(r'今回，新たに「([^」]+)」と「([^」]+)」と呼ばれる，二つの新マップが追加された', text)
    require(f'「{cave}」は，最初に発見された島の東にあった洞窟' in text, 'Relative east/anonymous island changed')
    require('今までは入ることができなかった' in text and '内部に入ることができるようになった' in text,
            'Previous versus reported current access changed')
    require('内部はかなり入り組んでおり' in text and '新種の恐竜まで生息しているということ' in text,
            'Qualified anonymous habitat claim changed')
    require(f'「{region}」と呼ばれるマップは，なんと海中に水没した島ということ' in text,
            'Submerged island description changed')
    require('辿りつくには地底を進むしかないという' in text and 'このマップの先には秘密が隠されているという' in text,
            'Underground approach or unknown secret changed')
    show, release = match(r'ペットシステムに，新たに"([^"]+)"と"([^"]+)"の機能が追加された', text)
    require(f'"{show}"は，ペットを自分だけが拾える状態でフィールド上に出すことができる' in text,
            'Display owner-only pickup changed')
    require(f'"{release}"は，文字通りペットを手放すコマンド' in text and
            'ペット屋まで行かなくとも，その場で手放せるようになった' in text, 'Local relinquish versus shop changed')
    mail_count = match(r'ペットメールを一度に(一匹)のみにしか送れないように変更された', text)[0]
    byline = match(r'（([A-Za-z]+)）$', text)[0]
    return {
        'core_sha256': sha(text.encode()),
        'authority': 'CONTEMPORARY_4GAMER_EDITORIAL_NOT_DIRECT_OPERATOR_OR_RUNTIME',
        'publication': '2004-09-17 19:12', 'body_byline': byline,
        'update': {'label': update_name, 'ordinal_as_written': ordinal,
                   'reported_status': 'COMPLETED_TODAY_AS_REPORTED_NOT_INDEPENDENTLY_EXECUTED',
                   'category_count': 2, 'numeric_build': None},
        'maps': [
            {'name': cave, 'kind': 'CAVE', 'relative_position': 'EAST_OF_FIRST_DISCOVERED_ISLAND',
             'reference_island_name': None, 'reference_island_id': None,
             'formerly_inaccessible': True, 'reported_access_after_update': True,
             'complex_interior_reported': True, 'map_id': None, 'coordinates': None},
            {'name': region, 'kind': 'SUBMERGED_ISLAND', 'approach': 'UNDERGROUND_ONLY_AS_REPORTED',
             'exact_route_edges': None, 'next_secret_identity': None, 'map_id': None, 'coordinates': None},
        ],
        'encounter_hint': {'map_label': cave, 'description': 'UNNAMED_NEW_DINOSAURS_AS_REPORTED',
                           'certainty': 'QUALIFIED_REPORT_ということ', 'species': None,
                           'species_id': None, 'level': None, 'spawn_rate': None},
        'pet_operations': [
            {'label': show, 'action': 'PLACE_ON_FIELD_WITH_SELF_ONLY_PICKUP_AS_REPORTED',
             'ownership_transfer_proven': False, 'server_object_or_slot_algorithm': None},
            {'label': release, 'action': 'RELINQUISH_LOCALLY_WITHOUT_PET_SHOP_AS_REPORTED',
             'sale_payment_proven': False, 'permanent_deletion_or_recovery_proven': False},
            {'label': 'ペットメール', 'restriction_as_written': mail_count,
             'per_operation_pet_count_as_reported': 1, 'limit_window_or_cooldown': None,
             'previous_limit': None, 'delivery_success_verified': False},
        ],
        'official_link_as_written_not_retrieved': 'http://stoneage.to/',
        'original_game_runtime_verified': False,
    }


MUTATIONS = (
    ('2004/09/17 19:12', '2004/09/18 19:12'),
    ('本日（9月17日）アップデートが行われた', '明日（9月18日）アップデートが行われる予定だ'),
    ('第三弾', '第四弾'), ('封印の開放', '封印の閉鎖'),
    ('「穀嶺の地」', '「谷嶺の地」'),
    ('最初に発見された島の東', '最初に発見された島の西'),
    ('今までは入ることができなかった', '今までも自由に入ることができた'),
    ('内部に入ることができるようになった', '内部はまだ入ることができない'),
    ('生息しているということ', '確実に全種類が生息していること'),
    ('海中に水没した島', '陸上の火山島'),
    ('地底を進むしかないという', '地上を自由に歩けるという'),
    ('このマップの先には秘密が隠されているという', 'このマップの先には機械文明遺跡があると確認された'),
    ('自分だけが拾える状態', '他人でも拾える状態'),
    ('ペット屋まで行かなくとも', 'ペット屋まで行かなければ'),
    ('一度に一匹のみにしか送れない', '一度に二匹まで送れる'),
    ('（Asakura）', '（DifferentAuthor）'),
    ('http://stoneage.to/', 'http://invalid.example/'),
)


def audit(raw, expected):
    text = raw.decode('cp932')
    semantic = lambda d: {k: v for k, v in d.items() if k != 'core_sha256'}
    for old, new in MUTATIONS:
        require(old in text, 'Unexercised counterfactual: ' + old)
        try:
            changed = extract(text.replace(old, new).encode('cp932'))
        except ValueError:
            continue
        require(semantic(changed) != semantic(expected), 'Semantic mutation accepted without digest gate')
    require(extract(raw + b'<script>peripheral_only=1;</script>') == expected, 'Peripheral script rejected')
    meta = raw.replace(b'name="author" content="Vanquish"', b'name="author" content="OtherEditor"')
    require(meta != raw and extract(meta) == expected, 'Meta author substituted for body byline')
    return {'real_input_mutations_rejected_without_digest_gate': len(MUTATIONS),
            'peripheral_script_positive': True, 'meta_author_positive': True,
            'historical_game_execution_verified': False}


def verify_catalog(report):
    require(report['scope']['historical_bytes_authenticated'] is False and
            report['scope']['runtime_verified'] is False and report['scope']['exact_build'] is None,
            'Source/build/runtime status promoted')
    records = report['catalog']
    require(len(records) == 7 and len({r['record_id'] for r in records}) == 7, 'Expected seven documentary records')
    source = report['extraction']
    expected = [('versions', source['update'])] + [('maps', m) for m in source['maps']]
    expected += [('encounters', source['encounter_hint'])] + [('tutorials', p) for p in source['pet_operations']]
    for r, (collection, content) in zip(records, expected):
        require(all(k in r for k in ('record_id', 'entity_type', 'version_profile', 'source_refs',
                                    'verification_status', 'rights_status', 'record_revision')), 'Record provenance missing')
        require(r['collection'] == collection and r['content'] == content, 'Detached record/source content')
        require(r['version_profile'] == PROFILE and r['source_refs'] == ['S2'] and r['game_ids'] is None,
                'Cross-version identity or source promotion')
        require(r['verification_status'] == 'SOURCE_DESCRIPTION_NOT_RUNTIME' and
                r['rights_status'] == 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'Record authority/rights promoted')
    require(all(x['identity_established'] is False for x in report['cross_source_nonjoins']),
            'Anonymous island or later region identity invented')
    require(all(v is False for v in report['negative_boundaries'].values()), 'Unsupported source conclusion promoted')
    require(report['scope']['first_party_webpage_retrieved'] is False and
            report['scope']['new_original_assets_retrieved'] == 0, 'Unretrieved official page or assets claimed')
    for pin in report['parent_pins']:
        b = (ROOT / pin['path']).read_bytes()
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Parent source changed')
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + bytes([0]) + b).hexdigest() == pin['git_blob'],
                'Parent Git identity changed')


def check_custody(root=None):
    """Require durable evidence, exact bytes and commit-scoped CI provenance."""
    root = ROOT if root is None else Path(root)
    receipt = json.loads((root / f'research/recovered/{STEM}-CUSTODY-R1.json').read_text())
    require(receipt['schema'] == 'stoneage.jp2004_sealed_region.custody.r1', 'Wrong custody schema')
    require(receipt['original_game_runtime_verified'] is False and
            receipt['historical_bytes_authenticated'] is False, 'Custody authority promoted')
    runs = receipt['runs']
    require(len({r['id'] for r in runs}) == len(runs) and all(
        r['head_sha'] == receipt['content_commit'] and r['status'] == 'completed' and
        r['conclusion'] == 'success' for r in runs), 'Duplicate or unverified CI run')
    pins = receipt['permanent_pins']
    required = {f'research/recovered/{STEM}-{s}-R1.json' for s in ('SOURCE', 'CI-CANDIDATE', 'CI-MAIN')}
    require(len({p['path'] for p in pins}) == len(pins) and
            required <= {p['path'] for p in pins}, 'Incomplete or duplicate evidence pins')
    for pin in pins:
        path = root / pin['path']
        require(path.is_relative_to(root) and '..' not in Path(pin['path']).parts,
                'Evidence path outside repository')
        b = path.read_bytes()
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Permanent evidence changed')
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + bytes([0]) + b).hexdigest() == pin['git_blob'],
                'Permanent Git identity changed')
    source = json.loads((root / f'research/recovered/{STEM}-SOURCE-R1.json').read_text())
    require({p['path'] for p in source['parent_pins']} <= {p['path'] for p in pins}, 'Parent custody incomplete')
    inputs = [{k: p[k] for k in ('id', 'url', 'bytes', 'sha256')} for p in source['source_pages']]
    for role in ('candidate', 'main'):
        run = receipt['source_jobs_and_artifacts'][role]
        matches = [r for r in receipt['runs'] if r['id'] == run['run']]
        require(len(matches) == 1 and matches[0]['head_sha'] == receipt['content_commit'] and
                matches[0]['status'] == 'completed' and matches[0]['conclusion'] == 'success',
                'CI run not successful at content commit')
        artifact_run = run['artifact']['workflow_run']
        require(artifact_run['id'] == run['run'] and artifact_run['head_sha'] == receipt['content_commit'] and
                artifact_run['head_branch'] == matches[0]['branch'] and
                (matches[0]['branch'] == 'main') == (role == 'main'), 'Artifact detached from run or branch')
        raw = json.loads((root / f'research/recovered/{STEM}-CI-{role.upper()}-R1.json').read_text())
        require(raw['schema'] == 'stoneage.jp2004_sealed_region.replay.r1' and
                raw['inputs'] == inputs and raw['extraction'] == source['extraction'], 'Archived replay detached from source')
        require(raw['runtime_verified'] is False and raw['original_assets_or_html_in_output'] is False and
                raw['july_context_reused_not_new_source'] is True and
                raw['audit'] == {'real_input_mutations_rejected_without_digest_gate': 17,
                                 'peripheral_script_positive': True, 'meta_author_positive': True,
                                 'historical_game_execution_verified': False}, 'Archived evidence boundary changed')
    return receipt


def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true')
    group.add_argument('--inputs', nargs=2)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    report = json.loads(REPORT.read_text())
    verify_catalog(report)
    check_custody()
    raws, inputs = [], []
    for i, url in enumerate(URLS):
        if a.fetch:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge-research/1.0'}), timeout=45) as r:
                require(r.status == 200 and r.url == url, 'Unexpected HTTP identity')
                b = r.read(2_000_001)
        else:
            b = Path(a.inputs[i]).read_bytes()
        require(len(b) <= 2_000_000, 'Source size exceeds bound')
        raws.append(b)
        inputs.append({'id': ['S1', 'S2'][i], 'url': url, 'bytes': len(b), 'sha256': sha(b)})
    old = json.loads((ROOT / report['july_parent_path']).read_text())
    require(july_extract(raws[0]) == old['extracted'], 'Previously archived July context changed')
    actual = extract(raws[1])
    require(actual == report['extraction'], 'September source semantics changed')
    out = {'schema': 'stoneage.jp2004_sealed_region.replay.r1', 'inputs': inputs, 'extraction': actual,
           'july_context_reused_not_new_source': True, 'audit': audit(raws[1], actual),
           'original_assets_or_html_in_output': False, 'runtime_verified': False}
    path = Path(a.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'inputs': inputs, 'audit': out['audit']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
