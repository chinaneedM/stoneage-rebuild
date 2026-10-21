"""A contemporary press report, not an authenticated operator release or runtime."""
import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
from tools.stoneage_cn2003_group2_manor_report import Visible, fetch
from tools.stoneage_cn2011_stall_source import jpeg_dimensions

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2004-CHAT-UPDATE'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URL = 'https://www.4gamer.net/news/history/2004.07/20040730231235detail.html'
PROFILE = 'LATER_OFFICIAL:JP_BOTHTEC_HANGAME_2004_PRESS_REPORTED'
BEGIN, END = '<!-- 本文開始 -->', '<!-- 本文終了 -->'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def compact(s):
    p = Visible()
    p.feed(s)
    return re.sub(r'\s+', '', ''.join(p.parts))


def extract(raw):
    t = raw.decode('cp932', errors='strict')
    bodies = re.findall(r'<body\b[^>]*>(.*?)</body\s*>', t, re.S | re.I)
    require(len(bodies) == 1 and '2004/07/3023:12' in compact(bodies[0]), 'Visible publication stamp missing')
    require(t.count(BEGIN) == t.count(END) == 5, 'Template body slots changed')
    slots = re.findall(re.escape(BEGIN) + '(.*?)' + re.escape(END), t, re.S)
    require(len(slots) == 5 and all(not compact(v) for v in slots[1:]), 'Expected one content slot and four empty template slots')
    text = compact(slots[0])
    cutoff = '→「ストーンエイジ」の当サイト内の記事一覧'
    require(text.count(cutoff) == 1, 'Article end boundary changed')
    text = text.split(cutoff)[0]
    month = re.search(r'(2004)年(6)月から正式サービスがスタート', text)
    update = re.search(r'(8)月(1)日に，正式サービス後初の大型アップデートが実施される', text)
    maintenance = re.search(r'メンテナンス作業は，(8)月(1)日の(15)時～(16)時に行われる予定', text)
    trial = re.search(r'新規ユーザー用に(\d+)日間の無料お試し期間', text)
    author = re.search(r'（(Kawamura)）$', text)
    require(month and update and maintenance and trial and author, 'Service phase, planned update, trial or byline changed')
    require('新たに発見されたという，島のマップが追加される' in text, 'Reported unnamed island changed')
    require('すでに一部のNPCが島への移住を開始したようだ' in text and 'この島への渡り方すらも現時点では秘密のようだ' in text, 'Qualified migration/secret route changed')
    require('探し出さねばならないのかもしれない' in text, 'Media exploration speculation changed')
    dungeons = re.search(r'ダンジョンが(二つ)追加される。一つは(サイナス島)，もう一つは(ジャルガ島)', text)
    guide = re.search(r'ゲームの案内役である(マーナ)は(推測している)', text)
    require(dungeons and guide and '入り口の位置なども今のところ秘密' in text, 'Dungeon regions or guide speculation changed')
    require('"チャットフィルタ機能"が実装される' in text and '登録した相手のチャットを遮断する機能' in text, 'Registered-counterpart chat filtering changed')
    placement = re.search(r'(8)月(3)日と(6)日に，今回追加された新マップ上にクエスト関連のNPCが配置される', text)
    duration = re.search(r'(3)日と(6)日にも(\d+)分(程度)の臨時メンテナンス', text)
    inference = re.search(r'新クエストは(3)日と(6)日から発動するということだと(考えていいだろう)', text)
    require(placement and duration and inference, 'NPC placement, approximate duration or media inference changed')
    p = Visible()
    p.feed(t)
    images = [s for s in p.images if s and s.startswith('/news/image/2004.07/20040730231235_')]
    require(len(images) == 3, 'Three actual article images required')
    return {
        'core_sha256': sha(text.encode()),
        'authority': 'CONTEMPORARY_4GAMER_EDITORIAL_REPORT_NOT_VERBATIM_OPERATOR_RELEASE',
        'visible_publication': '2004-07-30 23:12', 'body_byline': author[1],
        'template_slots': {'content_slots': 1, 'empty_slots': 4},
        'context': {'reported_formal_service_month': month[1] + '-' + month[2].zfill(2),
                    'first_major_update_scope': 'AFTER_REPORTED_2004_JUNE_FORMAL_SERVICE_ONLY',
                    'update_month_day_as_reported': update[1] + '-' + update[2],
                    'planned_maintenance_clock_hours': [int(maintenance[3]), int(maintenance[4])],
                    'maintenance_timezone': None, 'actual_deployment_or_completion_verified': False, 'numeric_client_build': None,
                    'trial_days_reported': int(trial[1]), 'trial_audience': 'NEW_USERS', 'actual_grant_or_billing_rules': None},
        'exploration': {'new_island_name_or_id': None, 'island_route': None,
                        'npc_migration_claim_qualified_as': '開始したようだ', 'actual_npc_migration_verified': False,
                        'dungeon_count_as_reported': 2, 'dungeon_regions_as_written': [dungeons[2], dungeons[3]],
                        'dungeon_names_ids_entrances_routes': None, 'media_guess_players_might_find_routes_not_confirmed_rule': True},
        'guide': {'name_as_written': guide[1], 'role_as_written': 'ゲームの案内役',
                  'secret_assessment_as_written': guide[2], 'confirmed_hidden_story_or_boss': None,
                  'original_npc_id_or_same_person_in_images': None},
        'chat_filter': {'feature_label': 'チャットフィルタ機能', 'reported_target': 'REGISTERED_COUNTERPART_CHAT',
                        'reported_action': 'BLOCK_CHAT', 'account_ban_or_trade_restriction_proven': False,
                        'ui_controls_list_capacity_channels_persistence_identity_matching': None, 'actual_filter_execution_verified': False},
        'staging': {'npc_placement_month_as_reported': int(placement[1]), 'npc_placement_days_as_reported': [int(placement[2]), int(placement[3])],
                    'maintenance_days_as_reported': [int(duration[1]), int(duration[2])],
                    'maintenance_minutes_as_reported': int(duration[3]), 'maintenance_duration_qualifier_as_written': duration[4],
                    'exact_maintenance_clocks_or_timezone': None, 'npc_names_ids_quest_conditions': None,
                    'quest_activation_days_are_media_inference': True, 'activation_inference_wording': inference[3],
                    'quests_actually_available_on_those_dates_proven': False},
        'image_paths_in_source_order': images, 'historical_game_executed': False,
    }


MUTATIONS = (
    ('first-service-phase', '2004年6月から正式サービス', '2004年7月から正式サービス'),
    ('update-day', '8月1日', '8月2日'),
    ('maintenance-start', '15時～16時', '14時～16時'),
    ('maintenance-end', '15時～16時', '15時～17時'),
    ('planned-not-observed', '行われる予定だ', 'すでに実施完了した'),
    ('migration-qualifier', '移住を開始したようだ', '移住を完了した'),
    ('island-route-secret', '渡り方すらも現時点では秘密のようだ', '渡り方はすでに公開されている'),
    ('dungeon-count', 'ダンジョンが二つ', 'ダンジョンが三つ'),
    ('dungeon-region', '一つはサイナス島', '一つはミライア島'),
    ('guide-name', 'マーナは', 'レーナは'),
    ('guide-inference', '推測している', '確認している'),
    ('chat-target', '登録した相手のチャット', '全員のチャット'),
    ('chat-action', 'チャットを遮断する', 'アカウントを停止する'),
    ('npc-date', '8月3日と6日に', '8月3日と7日に'),
    ('quest-not-guarantee', '考えていいだろう', '実装を確認した'),
    ('maintenance-duration', '30分程度', '60分程度'),
    ('approximate-not-exact', '30分程度', '30分ちょうど'),
    ('trial-audience', '新規ユーザー用に', '全ユーザー用に'),
    ('trial-days', '10日間の無料', '14日間の無料'),
    ('actual-image', '20040730231235_2.jpg', '20040730231235_3.jpg'),
)


def audit(raw, expected):
    t = raw.decode('cp932')
    checks = []
    for label, old, new in MUTATIONS:
        require(old in t, 'Mutation anchor missing: ' + label)
        b = t.replace(old, new).encode('cp932')
        try:
            x = extract(b)
            rejected = {k: v for k, v in x.items() if k != 'core_sha256'} != {k: v for k, v in expected.items() if k != 'core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        checks.append({'case': label, 'input_sha256': sha(b), 'rejected_without_digest_gate': True})
    require(extract(raw + b'<script>outside only</script>') == expected, 'Outside positive rejected')
    changed = raw.replace(b'name="author" content="Vanquish"', b'name="author" content="OuterEditor"')
    require(changed != raw and extract(changed) == expected, 'HTML meta author became body byline')
    return {'real_source_mutations': checks, 'outer_script_positive': True, 'meta_author_positive': True}


def validate(r):
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'] and r['images'] == local['images'], 'Source or visual semantics changed')
    require(r['source']['url'] == URL and r['source']['encoding'] == 'CP932_STRICT', 'Source URL or encoding changed')
    require(r['source']['authority'] == r['extracted']['authority'] and r['source']['authenticated_2004_original_bytes'] is False, 'Authority promotion')
    require(r['source']['displayed_publication'] == r['extracted']['visible_publication'], 'Publication changed')
    require(r['source']['current_observed_bytes'] == local['http_bytes'] and r['source']['current_observed_sha256'] == local['http_sha256'], 'HTTP pins changed')
    keys = ['context', 'exploration', 'guide', 'chat_filter', 'staging']
    require(len(r['records']) == 6 and len({x['record_id'] for x in r['records']}) == 6, 'Finite six records')
    for row, key in zip(r['records'], keys):
        require(row['evidence'] == r['extracted'][key], 'Record/source alignment changed')
    require(r['records'][5]['evidence'] == r['images'], 'Visual record alignment changed')
    for row in r['records']:
        require(row['version_profile'] == PROFILE and row['game_ids'] is None and row['source_refs'] == ['S1'] and row['runtime_verified'] is False, 'Version/ID/runtime promotion')
    require(len(r['images']) == 3 and [x['path_as_written'] for x in r['images']] == r['extracted']['image_paths_in_source_order'], 'Actual image order changed')
    for im in r['images']:
        require(im['requested_url'] == urljoin(URL, im['path_as_written']), 'Undeclared URL resolution')
        require(im['capture_date'] is None and im['native_client_resolution_proven'] is False and im['shows_chat_filter_ui'] is False, 'Image claim promoted')
    require(all(v is False for v in r['unproven'].values()), 'Unsupported conclusion promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51', 'Queue changed')


def replay(r, raw, pictures):
    validate(r)
    x = extract(raw)
    require(x == r['extracted'], 'Source body changed')
    require(len(pictures) == 3, 'Three image objects required')
    for pin, b in zip(r['images'], pictures):
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'] and jpeg_dimensions(b) == (pin['width'], pin['height']), 'Image bytes/geometry changed')
    return {'schema': 'stoneage.jp2004_chat_update.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': x, 'images': r['images'], 'audit': audit(raw, x),
            'raw_html_or_assets_in_output': False, 'historical_game_executed': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fetch', action='store_true', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = json.loads(REPORT.read_text())
    raw = fetch(URL, 1000000)
    with ThreadPoolExecutor(max_workers=3) as pool:
        pictures = list(pool.map(lambda im: fetch(im['requested_url'], 2000000), r['images']))
    out = replay(r, raw, pictures)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'images': len(pictures), 'semantic_mutations': len(out['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
