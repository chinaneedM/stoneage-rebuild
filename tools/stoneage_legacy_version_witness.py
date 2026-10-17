"""Bounded historical claims, not authenticated software release notes.

Only derived labels and source fingerprints survive acquisition. No old software
is downloaded, executed, adopted, or reproduced by this module.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_early_content_probe import plain, require

SOURCES = {
    'sade': ('https://news.17173.com/z/stoneage/content/2002-8-19/n337_253594.html?_platform=PC', '2002-08-19', 'E_skyline', '(1)我写这篇东西'),
    'comparison': ('https://news.17173.com/z/stoneage/content/2002-3-21/n936_852654.html?_platform=PC', '2002-03-21', '地藏乌拉', 'STA与SACH推出开始'),
    'sach123': ('https://news.17173.com/z/stoneage/content/2001-11-11/n691_607613.html?_platform=PC', '2001-11-11', '水银水晶VS炎之天舞', '在复制和修改的光环'),
    'settings': ('https://news.17173.com/z/stoneage/content/2002-9-27/n286_202934.html', '2002-09-27', '天行', '看了很久的文章了'),
}
# Source tokens are validation guards; output uses concise capability labels.
SADE = [
    ('0.1a', [('BETA_LIMITED_FUNCTIONS', '测试版')]),
    ('0.2a', [('STATIONARY_ENCOUNTERS', '原地遇敌'), ('NO_ENCOUNTERS', '不遇地'), ('MAP_INFO_EDIT', '地图资料编辑'), ('AMBUSH_AVOIDANCE', '免偷袭'), ('LEVEL_GATE_BYPASS', '不限等级进入')]),
    ('0.2b', [('AUTO_LOGIN', '自动登入')]),
    ('0.2c', [('BATTLE_PET_SWITCH', '战斗中换宠'), ('THREE_STEP_MOVEMENT_MODIFICATION', '3步顺移'), ('QUICK_CHAT', '快捷说话'), ('FORCED_PARTY', '强制组队'), ('BATTLE_EXIT', '战斗脱离')]),
    ('0.2d', [('EXTENDED_PLAYER_PET_NAMES', '长名字'), ('DETAILED_INFO', '详细资料'), ('FULL_TEAM_DISPLAY_DEFECT', '队长消失')]),
    ('0.2e', [('AUTO_TRAINING', '自动练功')]),
    ('0.2f', [('AUTO_MAIL_REPLY', '自动回信')]),
    ('0.2h', [('BATTLE_MAIL', '战斗中送信')]),
]
COMPARISON = [
    ('AUTO_ESCAPE', 'STA', 'USER_REPORTED_AVAILABLE', ['自动逃跑功能']),
    ('ACCESSORY_SWAP', 'STA_vs_SACH', 'USER_REPORTED_DIFFERENCE', ['STA可以换的上', 'SACH却不可以']),
    ('DETAILED_OPPONENT_INFO', 'STA', 'USER_REPORTED_ABSENT', ['没有详细资料这一项']),
    ('AUTO_TRAINING', 'STA_vs_SACHXP', 'SUBJECTIVE_PERFORMANCE_NOT_BENCHMARK', ['练功方面', '五分之一']),
    ('SCRIPT_COLLECTION', 'STA_vs_SACHXP', 'INTERNALLY_AMBIGUOUS_COMPARISON', ['STA是遥遥领先', '3类18个脚本', '数量方面绝对处于领先']),
    ('AUTO_COOKING', 'STA_and_SACHXP', 'BOTH_REPORTED_AVAILABLE_PERFORMANCE_UNVERIFIED', ['都有自动料理功能']),
    ('FUTURE_TRAINING_METHOD', 'STA', 'HEARSAY_NOT_IMPLEMENTED_EVIDENCE', ['还在考虑阶段', '不知道消息可靠不可靠']),
]
SETTINGS = [
    ('HP_THRESHOLD', 'USER_CONFIGURATION_NOT_DEFAULT', ['补血和补气的设定', '人、宠50%']),
    ('MP_THRESHOLD', 'USER_CONFIGURATION_NOT_DEFAULT', ['补气以精灵的等级']),
    ('AUTO_REVIVAL', 'USER_REPORTED_SETTING', ['设定自动复活']),
    ('PLAYER_PET_ACTIONS', 'USER_REPORTED_SETTING', ['人和宠的动作设定']),
    ('DISCONNECT_GUARDS', 'USER_REPORTED_SETTING', ['忠不到100掉线', '脚本出错掉线']),
    ('TIME_LOCK', 'ABE_NAMED_NO_EXACT_BUILD', ['阿背有个锁定时间的功能']),
    ('LUCK_LOCK_EFFECT', 'ANECDOTE_NOT_CAUSAL_GAME_RULE', ['锁定运气', '其实最终决定的还是现实中你的运气']),
]


def compact(text):
    return re.sub(r'\s+', '', plain(text))


def source_body(key, doc):
    _, date, author, start = SOURCES[key]
    for ident, expected in [('newsriqi', date), ('zhuozhe_left', author)]:
        m = re.search(r'<div\s+id=["\x27]' + ident + r'["\x27][^>]*>(.*?)</div>', doc, re.I | re.S)
        require(m is not None and expected in plain(m[1]), key + ': publication header ' + ident)
    s = compact(doc)
    a = s.find(start)
    b = s.find('本文言论', a)
    require(0 <= a < b, key + ': article boundary')
    return s[a:b]


def derive(documents):
    require(set(documents) == set(SOURCES), 'exact four-source set')
    bodies = {k: source_body(k, d) for k, d in documents.items()}
    s = bodies['sade']
    require('部分更新过程' in s and '全凭记忆' in s, 'retrospective qualifiers')
    a = s.index('部分更新过程')
    end = s.index('截至到这个版本为止', a)
    seq = s[a:end]
    matches = list(re.finditer(r'0\.[12][a-h]', seq))
    require([m[0] for m in matches] == [v for v, _ in SADE], 'reported list order changed')
    rows = []
    for i, (version, features) in enumerate(SADE):
        block = seq[matches[i].end():matches[i+1].start() if i+1 < len(matches) else len(seq)]
        require(all(marker in block for _, marker in features), 'version-local feature: ' + version)
        rows.append({'version': version, 'source_order': i, 'features': [f for f, _ in features],
                     'status': 'RETROSPECTIVE_PARTIAL_UPDATE_CLAIM', 'release_date': None,
                     'section_sha256': hashlib.sha256(block.encode()).hexdigest()})
    gstart = s.index('chs做出0.2g版本')
    gend = s.index('这个时候在盒子论坛', gstart)
    g = s[gstart:gend]
    require(all(x in g for x in ['大顺移', '法老版', '大g版']), 'separate g-variant claim')
    rows.append({'version': '0.2g', 'source_order': None, 'features': ['LONG_DISTANCE_MOVEMENT_MODIFICATION'],
                 'status': 'RETROSPECTIVE_RESTRICTED_VARIANT_NOT_LINEAR_RELEASE', 'release_date': None,
                 'section_sha256': hashlib.sha256(g.encode()).hexdigest()})
    compare = []
    for feature, family, status, markers in COMPARISON:
        require(all(x in bodies['comparison'] for x in markers), 'comparison claim: ' + feature)
        compare.append({'feature': feature, 'family_scope': family, 'status': status, 'exact_versions': None})
    settings = []
    for feature, status, markers in SETTINGS:
        require(all(x in bodies['settings'] for x in markers), 'settings claim: ' + feature)
        settings.append({'feature': feature, 'status': status, 'exact_versions': None})
    require('SaCh1.23' in bodies['sach123'], 'exact SaCh identity')
    return {'schema': 'stoneage.legacy_version_witness.r1',
            'source_roles': {'sade': 'PLAYER_RETROSPECTIVE_NOT_CHANGELOG', 'comparison': 'CONTEMPORANEOUS_USER_COMPARISON', 'sach123': 'CONTEMPORANEOUS_PLAYER_OPINION', 'settings': 'CONTEMPORANEOUS_USER_CONFIGURATION'},
            'body_sha256': {k: hashlib.sha256(b.encode()).hexdigest() for k, b in bodies.items()},
            'sade_version_claims': rows, 'comparison': compare, 'settings': settings,
            'sach_version_attestation': {'family': 'SaCh', 'version': '1.23', 'publication_date': '2001-11-11', 'release_date': None, 'feature_list_recovered': False, 'nearby_abuse_claims_attributed_to_this_build': False},
            'settings_family_scope': 'SOURCE_NAMES_MX_SAT_ABE_ANGEL_NO_AUTOMATIC_SACHXP_BUILD_EQUIVALENCE',
            'global_first_introductions_verified': False, 'developer_release_records_obtained': False,
            'current_html_authenticated_at_publication': False, 'exact_official_client_compatibility_verified': False,
            'all_tools_or_features_recovered': False, 'software_executed': False, 'adoption_decided': False,
            'new_game_production_started': False}


def report(acquisitions):
    require(set(acquisitions) == set(SOURCES), 'source acquisition set')
    docs, sources = {}, {}
    for key, (raw, final_url) in acquisitions.items():
        url, date, author, _ = SOURCES[key]
        require(0 < len(raw) <= 2_000_000 and final_url == url, 'source size/origin: ' + key)
        doc = raw.decode('utf-8')
        docs[key] = doc
        sources[key] = {'url': url, 'final_url': final_url, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'codec': 'utf-8', 'publication_date': date, 'author': author}
    return dict(derive(docs), sources=sources)


def fetch(key):
    url = SOURCES[key][0]
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAgeHistoricalResearch/1.0'}), timeout=40) as response:
        require(response.status == 200, 'HTTP status')
        return key, (response.read(2_000_001), response.url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        result = report(dict(pool.map(fetch, SOURCES)))
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps({'sade_versions': len(result['sade_version_claims']), 'comparison': len(result['comparison']), 'settings': len(result['settings'])}))


if __name__ == '__main__':
    main()
