"""Verify a bounded operator release series; never execute game rules or scripts.

Only derived metadata is written. HTML is supplied transiently or fetched from
three fixed URLs. Current HTTP hashes are not historical snapshot hashes.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2008-SHADOW-CHAPTERS-SOURCE-R1.json'
IDS = ('20080922005', '20081028007', '20081125066')
URLS = tuple(f'https://www.4gamer.net/games/013/G001377/{x}/' for x in IDS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.blocked = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.blocked += 1
        if not self.blocked:
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.blocked:
            self.blocked -= 1
        if not self.blocked:
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.blocked:
            self.parts.append(data)


def compact(html):
    parser = Visible()
    parser.feed(html)
    return re.sub(r'\s+', '', ''.join(parser.parts))


def extract(payload, chapter):
    require(chapter in (1, 2, 3), 'Only three qualified chapters')
    text = compact(payload.decode('utf-8-sig'))
    marker = '以下，リリースより' if chapter == 1 else 'メーカー発表文の内容をそのまま掲載しています'
    require(text.count(marker) == 1, 'Missing/ambiguous release attribution boundary')
    release = text.split(marker, 1)[1]
    require('株式会社デジパーク' in release[:150], 'Release issuer not qualified')
    start = release.index('新クエストアップデート')
    end_marker = 'アップデート記念キャンペーン' if chapter == 1 else 'ストーンエイジ公式サイト'
    core = release[start:release.index(end_marker, start)]
    overview = core.split('■クエスト概要', 1)[1]
    level = re.findall(r'Lv(\d+)以上', overview)
    require(len(level) == 1, 'Exactly one level condition in quest overview required')
    predecessors = re.findall(r'「影の支配者(\d+)章（序）」をクリアしていること', overview)
    require(len(predecessors) == (0 if chapter == 1 else 1), 'Missing/ambiguous chapter predecessor')
    entries = re.findall(r'「([^「」]+の村)」にいるNPC「([^「」]+)」', overview)
    require(len(entries) == (2 if chapter == 1 else 1), 'Unexpected source entry/hint roles')
    fields = {
        'chapter': chapter,
        'minimum_level_reported': int(level[0]),
        'previous_chapter_required_reported': int(predecessors[0]) if predecessors else None,
        'entry_or_hint_roles': [{'village_as_written': v, 'npc_label_as_written': n,
                                 'role': 'QUEST_START_ALTERNATIVE' if chapter == 1 else 'HINT_NOT_PROVEN_START'} for v, n in entries],
        'exclusive_first_chapter_routes_reported': True if 'どちらかしか片方しかクリアすることができません' in overview else None,
        'prior_chapter_changes_npc_presence_reported': True if '1章のクエストの進行内容によって、一部の登場NPCや、NPCのセリフが変化します' in overview else None,
        'choice_changes_dialogue_reported': True if '進行中の選択肢によって、一部のNPCのセリフが変化します' in overview else None,
    }
    return {'core_sha256': hashlib.sha256(core.encode()).hexdigest(),
            'core_utf8_bytes': len(core.encode()), 'source_facts': fields}


def validate_report(report):
    require(report['schema'] == 'stoneage.jp2008_shadow_chapters.source_contract.r1', 'Unknown report')
    sources, records = report['sources'], report['records']
    require([s['url'] for s in sources] == list(URLS), 'Source list changed')
    require(len(records) == 3 and [r['source_reported']['chapter'] for r in records] == [1, 2, 3], 'Finite chapter sequence changed')
    for i, (source, row) in enumerate(zip(sources, records), 1):
        require(set(('record_id', 'entity_type', 'version_profile', 'source_refs',
                     'verification_status', 'rights_status', 'record_revision')) <= row.keys(), 'Missing archive fields')
        require(source['id'] == f'S{i}' and row['source_refs'] == [source['id']], 'Dangling source reference')
        require(re.fullmatch(r'[0-9a-f]{64}', source['current_http']['sha256']) is not None
                and source['historical_2008_raw_sha256'] is None, 'Current bytes promoted to historical bytes')
        require(source['authority'] == 'OPERATOR_ISSUED_RELEASE_HOSTED_BY_4GAMER'
                and not source['editorial_intro_is_release_body'], 'Source attribution changed')
        require(row['version_profile'] == 'LATER_OFFICIAL:JP_DIGIPARK_2008_SHADOW_SERIES', 'Version promotion')
        require(row['verification_status'] == 'OPERATOR_RELEASE_REPUBLISHED_BY_MEDIA_NOT_RUNTIME', 'Runtime promotion')
        require(row['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Rights promotion')
        require(row['collection'] == 'quests' and row['game_ids'] is None and row['reward'] is None, 'Invented ID/reward')
        facts = row['source_reported']
        require(facts['previous_chapter_required_reported'] == (i - 1 if i > 1 else None), 'Invalid chapter dependency')
        require(facts['minimum_level_reported'] > 0, 'Unknown level cannot default to zero')
        require(all(x['role'] == ('QUEST_START_ALTERNATIVE' if i == 1 else 'HINT_NOT_PROVEN_START')
                    for x in facts['entry_or_hint_roles']), 'Hint promoted to quest acceptance')
        require(row['ending_or_unmasked_identity'] is None and row['exact_dialogue_or_save_flags'] is None
                and row['actual_spawn_coordinates'] is None, 'Invented identity/script/location')
    dependencies = [(x['from_chapter'], x['to_chapter']) for x in report['relations']
                    if x['kind'] == 'SOURCE_EXPLICIT_COMPLETION_PREREQUISITE']
    require(dependencies == [(1, 2), (2, 3)], 'Missing or speculative chapter edge')
    require(report['boundaries'] == {
        'official_host_html_recovered': False, 'historical_2008_snapshot_authenticated': False,
        'server_execution_verified': False, 'exact_client_build': None, 'tw10_backfill': False,
        'jss1999_backfill': False, 'chapter4_or_finale_recovered': False,
        'campaign_items_are_quest_rewards': False, 'npc_alias_or_cross_region_identity_verified': False,
        'images_downloaded': 0, 'game_programs_downloaded': 0, 'raw_html_committed': False,
        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'
    }, 'Evidence boundary changed')
    require(report['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-22', 'Return to portfolio required')


def replay(report, payloads):
    validate_report(report)
    require(len(payloads) == 3, 'Exactly three source payloads required')
    derived = []
    for i, (source, row, payload) in enumerate(zip(report['sources'], report['records'], payloads), 1):
        actual = extract(payload, i)
        require(actual['core_sha256'] == source['release_core_sha256'], 'Release core changed')
        require(actual['core_utf8_bytes'] == source['release_core_utf8_bytes'], 'Core length changed')
        require(actual['source_facts'] == row['source_reported'], 'Source-derived fields differ')
        derived.append({'source_id': source['id'], 'current_http_bytes': len(payload),
                        'current_http_sha256': hashlib.sha256(payload).hexdigest(), **actual})
    return {'schema': 'stoneage.jp2008_shadow_chapters.replay.r1', 'verified_sources': derived,
            'historical_snapshot_or_server_execution_verified': False, 'raw_html_in_output': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-dir', type=Path)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(bool(args.html_dir) != args.fetch, 'Choose supplied transient HTML or fixed live URLs')
    report = json.loads(REPORT.read_text())
    if args.fetch:
        payloads = []
        for url in URLS:
            with urllib.request.urlopen(url, timeout=45) as response:
                require(response.status == 200 and response.url == url, 'Unexpected HTTP response/redirect')
                payloads.append(response.read(2_000_001))
                require(len(payloads[-1]) <= 2_000_000, 'Oversized source response')
    else:
        payloads = [(args.html_dir / f'{ident}.html').read_bytes() for ident in IDS]
    result = replay(report, payloads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('SOURCE_CORES_VERIFIED=3 ORIGINAL_SERVER_EXECUTIONS=0 RAW_HTML_EXPORTED=0')


if __name__ == '__main__':
    main()
