"""Replay a Wayi-attributed seasonal NPC announcement, one early capture and one image.

Original HTML/image bytes stay transient. Source assertions describe announced
rules; neither archive capture nor screenshot establishes original server execution.
"""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-CN2003-CHRISTMAS-NPC-SOURCE-R1.json'
URLS = (
    'https://games.sina.com.cn/newgames/2003/12/122310574.shtml',
    'https://web.archive.org/web/20040218034443id_/http://games.sina.com.cn:80/newgames/2003/12/122310574.shtml',
    'https://image2.sina.com.cn/gm/newgames/2003/12/U163P115T9D10574F167DT20031223152817.JPG',
)
NAMES = ('christmas.html', 'christmas-era.html', 'christmas-tree.jpg')


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.images, self.hidden = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if not self.hidden:
            self.parts.append(' ')
            if tag == 'img':
                self.images.append(dict(attrs).get('src'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        if not self.hidden:
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract(payload):
    html = payload.decode('gb18030')
    require(html.count('<!-- 内容 begin -->') == html.count('<!-- 内容 end -->') == 1,
            'Missing/ambiguous article boundary')
    body = html.split('<!-- 内容 begin -->')[1].split('<!-- 内容 end -->')[0]
    p = Visible()
    p.feed(body)
    text = re.sub(r'\s+', '', ''.join(p.parts))
    require(text.startswith('以下是来自华义的最新官方消息：'), 'No operator credit inside article')
    require('2003-12-23 15:28' in html, 'Publication label missing')
    require(p.images == [URLS[2].replace('https:', 'http:')], 'Actual article image link changed')
    require(text.count('活动自') == 1 and text.count('点击此处查询全部') == 1, 'Ambiguous event core')
    core = text.split('活动自')[1].split('点击此处查询全部')[0]
    dates = re.search(r'^(\d{4}/\d{2}/\d{2})起到(\d{4}/\d{2}/\d{2})止。', core)
    versions = re.search(r'石器时代([\d.]+)及([\d.]+)服务器组([^将]+)将出现NPC——([^和]+)和美丽的圣诞树。', core)
    grant = re.search(r'交出([^需]+)需要的道具后可以得到([^一]+)一份。', core)
    limit = re.search(r'1\.每个([^在]+)在([^只]+)只限领([^圣]+)圣诞大礼包；', core)
    level = re.search(r'2\.领取礼物的人物必须达到([^并]+)并完成([^；]+)；', core)
    require(all((dates, versions, grant, limit, level)), 'Source rule structure changed')
    require(grant[1] == versions[4], 'Different exchange NPC in grant sentence')
    require(core.endswith('3.兑换奖品需要的道具请按照圣诞兑奖员的要求自行准备哦！'), 'NPC-directed material clause missing')
    snow = re.search(r'从(12月24日)起，([^的]+)的服务器中都将大雪普降。', text)
    require(snow, 'Separate snow announcement missing')
    facts = {
        'event_dates_as_written': list(dates.groups()),
        'exchange_server_versions': [versions[1], versions[2]],
        'location_scope_as_written': versions[3], 'exchange_npc': versions[4],
        'reward_label_as_written': grant[2], 'reward_units_per_exchange': 1,
        'limit_subject_as_written': limit[1], 'limit_scope_as_written': limit[2],
        'limit_quantity_as_written': limit[3],
        'level_condition_as_written': level[1], 'required_milestone': level[2],
        'materials_directed_by_npc_not_enumerated': True,
        'snow_start_as_written': snow[1], 'snow_scope_as_written': snow[2],
        'source_image_declared_http': p.images[0],
    }
    return {'core_sha256': sha256(core.encode()).hexdigest(), 'core_utf8_bytes': len(core.encode()), 'facts': facts}


def jpeg_dimensions(payload):
    require(payload[:2] == b'\xff\xd8', 'Not a JPEG')
    pos = 2
    while pos + 4 <= len(payload):
        require(payload[pos] == 255, 'Invalid JPEG marker')
        while pos < len(payload) and payload[pos] == 255:
            pos += 1
        require(pos < len(payload), 'Truncated JPEG')
        marker = payload[pos]
        pos += 1
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        length = int.from_bytes(payload[pos:pos + 2], 'big')
        require(length >= 2 and pos + length <= len(payload), 'Invalid JPEG segment')
        if marker in (0xC0, 0xC1, 0xC2):
            require(length >= 8, 'Short JPEG frame')
            return [int.from_bytes(payload[pos + 5:pos + 7], 'big'), int.from_bytes(payload[pos + 3:pos + 5], 'big')]
        pos += length
    raise ValueError('No JPEG dimensions')


def validate(report):
    require(report['schema'] == 'stoneage.cn2003_christmas_npc_source.r1', 'Wrong schema')
    require([s['http']['url'] for s in report['inputs']] == list(URLS), 'Bounded source set changed')
    require(report['inputs'][0]['authority'] == 'WAYI_OFFICIAL_MESSAGE_EXPLICITLY_ATTRIBUTED_BY_SINA', 'Source authority changed')
    require(report['inputs'][1]['capture_timestamp'] == '20040218034443', 'Different early capture')
    require(report['inputs'][1]['same_publication_not_independent_witness'] is True, 'Snapshot counted as second witness')
    require(report['inputs'][2]['historical_image_bytes_verified'] is False, 'Current image promoted to historical bytes')
    require(len(report['records']) == 4, 'Four bounded research records expected')
    required = {'record_id', 'entity_type', 'version_profile', 'source_refs', 'verification_status', 'rights_status', 'record_revision'}
    for r in report['records']:
        require(required <= r.keys() and r['game_ids'] is None, 'Archive contract or original ID changed')
        require(r['verification_status'] in ('ANNOUNCEMENT_NOT_RUNTIME', 'MANUAL_IMAGE_OBSERVATION_NOT_SPAWN_PROOF'), 'Runtime promotion')
        require(r['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Rights promotion')
    npc, quest, item, screen = report['records']
    require(npc['label_as_written'] == '圣诞兑奖员' and npc['spawn_coordinates'] is None and npc['map_names'] is None, 'Invented NPC location')
    require(quest['source_rules'] == report['inputs'][0]['extracted']['facts'], 'Quest detached from source facts')
    require(quest['source_rules'] == report['inputs'][1]['extracted']['facts'], 'Different early source rules')
    require(quest['eligibility_logic'] == 'LEVEL_CLAUSE_AND_ADULT_CEREMONY_AND_NPC_REQUIRED_ITEMS_AND_CHARACTER_GROUP_LIMIT', 'Conjunction lost')
    require(quest['level_predicate'] is None and quest['server_time_window'] is None and quest['reset_rule'] is None, 'Unknown boundary/time/reset invented')
    require(quest['required_item_list'] is None and quest['exact_dialogue'] is None and quest['original_script'] is None, 'Missing script/materials filled in')
    require(item['contents'] is None and item['item_master_id'] is None, 'Gift contents invented')
    require(screen['dimensions'] == [450, 337] and screen['avatar_or_npc_sprite_binding'] is None, 'Image promoted to original sprite identity')
    require(report['boundaries'] == {
        'original_operator_host_recovered': False, 'original_server_execution_verified': False,
        'exact_client_build': None, 'named_nine_spawn_maps_recovered': False,
        'all_server_snow_claim_expands_exchange_scope': False,
        'once_per_character_group_means_account_global_or_daily': False,
        'numeric_level_boundary_proven': False, 'historical_image_bytes_verified': False,
        'raw_html_or_image_committed': False, 'tw10_or_jss1999_backfill': False,
        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'
    }, 'Historical boundary changed')
    require(report['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-24', 'Portfolio return required')


def replay(report, payloads):
    validate(report)
    require(len(payloads) == 3, 'Exactly current HTML, early HTML and actual linked image required')
    extracted = [extract(payloads[0]), extract(payloads[1])]
    for i, got in enumerate(extracted):
        require(got == report['inputs'][i]['extracted'], 'Source core or announced rule changed')
    # Current wrapper can change independently; early capture and image bytes are exact pins.
    for i in (1, 2):
        b, h = payloads[i], report['inputs'][i]['http']
        require(len(b) == h['bytes'] and sha256(b).hexdigest() == h['sha256'], 'Historical/image bytes changed; no substitute allowed')
    require(jpeg_dimensions(payloads[2]) == report['inputs'][2]['dimensions'], 'Image dimensions changed')
    return {
        'schema': 'stoneage.cn2003_christmas_source.replay.r1',
        'inputs': [{'source_id': s['id'], 'bytes': len(b), 'sha256': sha256(b).hexdigest()} for s, b in zip(report['inputs'], payloads)],
        'announcement': extracted[0], 'early_capture': extracted[1],
        'early_capture_timestamp': '20040218034443', 'early_capture_matches_current_rules': extracted[0] == extracted[1],
        'image_dimensions': jpeg_dimensions(payloads[2]),
        'raw_html_or_image_bytes_in_output': False, 'original_server_or_historical_image_execution_verified': False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fetch', action='store_true')
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    require(a.fetch != bool(a.source_dir), 'Choose fixed URL fetch or supplied transient files')
    payloads = []
    for url, name in zip(URLS, NAMES):
        if a.fetch:
            with urllib.request.urlopen(url, timeout=45) as response:
                require(response.status == 200 and response.url == url, 'Unexpected HTTP/redirect')
                data = response.read(2_000_001)
                require(len(data) <= 2_000_000, 'Oversized source')
        else:
            data = (a.source_dir / name).read_bytes()
        payloads.append(data)
    result = replay(json.loads(REPORT.read_text()), payloads)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('ANNOUNCEMENT_RULESET_VERIFIED=1 EARLY_HTML_CAPTURE_VERIFIED=1 LINKED_IMAGE_VERIFIED=1 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__ == '__main__':
    main()
