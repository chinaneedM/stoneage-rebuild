"""Join preserved manifest evidence, without fetching or inventing script bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STATIC = 'research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt'
GAME = 'research/recovered/STONEAGE-25-GAMEPLAY-DATA-INVENTORY-R1.txt'
MODERN = 'research/recovered/STONEAGE-NPC-GENKOU-DERIVED-ARG-R1.json'
REPORT = 'research/recovered/STONEAGE-NPC-ORIGINAL-SCRIPT-CARRIER-QUALIFICATION-R1.json'
PREFIX = '石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/'
BUNDLE = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
TARGETS = {
 'npc/100/sb_kbu.arg': (258, '433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b'),
 'npc/100/sb_geno.create': (573, '5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1'),
 'npc/100/sb_geno.template': (321, '76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d')}
PINS = {STATIC: '48feb98aa977c88dcc236b530e0428ab665032ec923787eac0c293d5960159b0',
        GAME: '83f81dec76ce22ee91d965d66080cf2085bfcd02e2598e139183b2e8ff1f63e5',
        MODERN: '6b25033c5a0b4f4b93f4f65abdf6d1c829a7da1e1bf158fa8adefd875dc4021a'}


def qualify(static, gameplay, modern):
    """Semantic cross-check remains active independently of whole-report digests."""
    if static.count(BUNDLE + '  /tmp/sa25/stoneage25-combined.rar') != 1:
        raise ValueError('missing or ambiguous parent archive digest')
    if static.count('/tmp/sa25/stoneage25-combined.rar|361255180') != 1:
        raise ValueError('parent archive size changed')
    rows = []
    for path, (size, sha) in TARGETS.items():
        candidates = [x for x in gameplay.splitlines() if x.startswith('CANDIDATE|server|character_npc_enemy|' + path + '|')]
        expected = f'CANDIDATE|server|character_npc_enemy|{path}|{size}|{Path(path).suffix}|{sha}'
        if candidates != [expected]:
            raise ValueError('gameplay member identity changed: ' + path)
        full = PREFIX + path
        sizes = [x for x in static.splitlines() if x.startswith(full + '|')]
        if sizes != [f'{full}|{size}']:
            raise ValueError('static member length missing or ambiguous: ' + path)
        hashes = re.findall(r'^([0-9a-f]{64})  /tmp/sa25/out/' + re.escape(full) + r'$', static, re.M)
        if hashes != [sha]:
            raise ValueError('static member hash missing or ambiguous: ' + path)
        rows.append({'path': path, 'archive_member_path': full, 'bytes': size,
                     'sha256': sha, 'two_existing_manifests_agree': True})
    if (modern.get('embedded_path'), modern.get('embedded_length'), modern.get('embedded_sha256')) != (
        '100/sb_kbu.arg', 258, '961b87cebad2fd7cb7875f9433df0e301f9f64b06c46a558475fc1a0344e9eec'):
        raise ValueError('modern embedded specimen changed')
    if modern.get('certified_same_official_build') is not False:
        raise ValueError('unsupported official build promotion')
    return {
        'schema': 'stoneage.npc_script_carrier_qualification.r1',
        'task': 'NPC-QUEST-ORIGINAL-SCRIPT-CARRIER-QUALIFICATION-10',
        'evidence_role': 'EXISTING_PRESERVED_MIXED_BUNDLE_MANIFEST_JOIN',
        'parent_archive': {'bytes': 361255180, 'sha256': BUNDLE,
            'source_page': 'https://www.lab.welovesa.com/viewthread.php?extra=&page=1&tid=219',
            'classification': 'MIXED_COMMUNITY_BRIDGE_NOT_AUTHENTICATED_OFFICIAL'},
        'members': rows,
        'modern_arg_comparison': {'bytes_equal': True, 'sha256_equal': False,
            'modern_sha256': modern['embedded_sha256'],
            'semantic_equivalence': 'UNKNOWN_NO_PRESERVED_BODY_READ_THIS_TURN'},
        'raw_archive_reacquired_this_turn': False,
        'preserved_script_bodies_read_this_turn': False,
        'same_official_build_certified': False,
        'original_server_execution': False,
        'origin_class': 'ORIGIN_UNRESOLVED',
        'new_official_npcs_or_quests': 0,
        'overall_restoration_percentage': None,
        'next': 'WAYI-OFFICIAL-SAEXE-LOGIN-RESOURCE-CONTENT-11'}


def build(root=ROOT):
    inputs = {}
    pins = {}
    for path, sha in PINS.items():
        raw = (root / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError('immutable parent changed: ' + path)
        inputs[path] = raw.decode('utf-8')
        pins[path] = {'bytes': len(raw), 'sha256': sha,
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
    result = qualify(inputs[STATIC], inputs[GAME], json.loads(inputs[MODERN]))
    result['source_pins'] = pins
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = (json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
    if args.output:
        args.output.write_bytes(raw)
    elif raw != (ROOT / REPORT).read_bytes():
        raise ValueError('archived qualification differs from semantic replay')
    else:
        print('3 member identities / 2 existing manifests matched; official origin remains OPEN')


if __name__ == '__main__':
    main()
