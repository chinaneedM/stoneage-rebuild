"""Frozen quest-archive routing audit. No original game execution or public export."""
from __future__ import annotations
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'research/recovered/'
MANIFEST = PREFIX + 'STONEAGE-QUEST-MATERIAL-INPUTS-R116.json'
REPORT = PREFIX + 'STONEAGE-QUEST-MATERIAL-REVIEW-R116.json'
MANIFEST_SHA = '326a25a9cb43b1bba0feb04d0bc4c5e1e9bc9e03152f6cf469525b06a0701827'
HEAD = '1a5bb8d67ab6a4e7189968f53f007c41083a1f63'
TREE = 'a9becaebf199329327f7bd1bb985de5e61fe787f'
OVERLAY = PREFIX + 'STONEAGE-QUEST-ORIGIN-SEPARATION-R1.json'
PORTFOLIO = PREFIX + 'STONEAGE-MATERIAL-PORTFOLIO-REVIEW-R102.json'
CATEGORIES = ('BASE_GAME_QUEST', 'PERMANENT_VERSION_QUEST',
              'OPERATOR_EVENT_QUEST', 'ORIGIN_UNRESOLVED')
FIELDS = {'record_id', 'entity_type', 'version_profile', 'source_refs',
          'verification_status', 'rights_status', 'record_revision'}

# Explicit reviewed IDs only: no keyword or whole-file inheritance. In particular,
# event-unlocked permanent services do not turn their collection event into a base quest.
EVENTS = {
    'cn-wayi-2003-christmas:exchange': ('CN2003-CHRISTMAS-NPC-SOURCE-R1', 'SEASONAL_EXCHANGE_20031224_26'),
    'cn-wayi-tournament-2003:r107:golden-pet-claim': ('CN2003-TOURNAMENT-REWARD-R107', 'LIMITED_TOURNAMENT_REDEMPTION_NOT_GENERAL_QUEST'),
    'cn-wayi-tournament-2003:r107:semifinal-selection': ('CN2003-TOURNAMENT-REWARD-R107', 'TOURNAMENT_REWARD_APPLICATION_NOT_QUEST_SCRIPT'),
    'jp2004-dec:r110:christmas-claim': ('JP2004-XMAS-PARTY-COMBAT-R110', 'CHRISTMAS_2004_EVENT_REPORT'),
    'jp2004-dec:r110:new-year-shrine': ('JP2004-XMAS-PARTY-COMBAT-R110', 'NEW_YEAR_2005_EVENT_REPORT'),
    'JP2005-R80-challenge': ('JP2005-AUTUMN-COOKING-SOURCE-R1', 'COOKING_EVENT_OCT04_11_2005'),
    'JP2005-R85-quest-0': ('JP2005-GW-STAMP-RALLY-SOURCE-R1', 'GW_STAMP_RALLY_APR28_MAY10_2005'),
    'JP2005-R85-quest-1': ('JP2005-GW-STAMP-RALLY-SOURCE-R1', 'GW_STAMP_RALLY_APR28_MAY10_2005'),
    'JP2005-GAIAX-R69-QUEST': ('JP2005-TREASURE-EVENT-SOURCE-R1', 'TWO_PHASE_LIMITED_TREASURE_EVENT_SEPT2005'),
    'jp-gaiax-stoneage-2006:r108:event': ('JP2006-DINO-GETTERS-R108', 'DINO_GETTERS_MAY23_JUN06_2006'),
    'jp-gaiax-stoneage-2006:r108:per-server-reward': ('JP2006-DINO-GETTERS-R108', 'SERVER_AGGREGATE_EVENT_INCENTIVE_NOT_PERSONAL_QUEST'),
    'JP2008-COOP-07': ('JP2008-COOPERATION-SOURCE-R1', 'LIMITED_COLLECTION_EVENT_JUN24_JUL15_2008'),
    'JP2008-COOP-08': ('JP2008-COOPERATION-SOURCE-R1', 'LIMITED_COLLECTION_EVENT_JUN24_JUL15_2008'),
    'jp-digipark-2009:r111:puzzle-state-machine': ('JP2009-MYSTERY-DUNGEON-R111', 'TENTH_ANNIVERSARY_OCT20_NOV04_2009'),
    'jp-digipark-2009:r111:wild-encounter-boundary': ('JP2009-MYSTERY-DUNGEON-R111', 'ENCOUNTER_CONTEXT_OF_SAME_ANNIVERSARY_EVENT'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def walk(obj, pointer=''):
    if isinstance(obj, dict):
        yield pointer, obj
        for key, value in obj.items():
            yield from walk(value, pointer+'/'+key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from walk(value, pointer+'/'+str(i))

def load_inputs(root=ROOT):
    raw = (root/MANIFEST).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'Frozen manifest changed')
    manifest = json.loads(raw)
    require((manifest['baseline_head'], manifest['baseline_tree']) == (HEAD, TREE), 'Wrong baseline')
    objects = {}
    for entry in manifest['files']:
        path = entry['path']
        require(Path(path).parent.as_posix() == PREFIX.rstrip('/') and path.endswith('.json'), 'Unsafe scope')
        require(path not in objects, 'Duplicate manifest path')
        require(identity((root/path).read_bytes()) == {k: entry[k] for k in ('bytes', 'sha256', 'git_blob')},
                'Source bytes changed: '+path)
        objects[path] = json.loads((root/path).read_bytes())
    return manifest, objects

def selected(row):
    return {'record_id', 'entity_type'} <= row.keys() and (
        row.get('collection') == 'quests' or row['entity_type'] == 'quest')

def summarize(manifest, objects):
    groups = defaultdict(list)
    for path, obj in sorted(objects.items()):
        for pointer, row in walk(obj):
            if selected(row):
                require(FIELDS <= row.keys(), 'Incomplete selected record')
                require(isinstance(row['record_id'], str), 'Non-string record ID')
                groups[row['record_id']].append((path, pointer, row))
    pins = {entry['path']: entry for entry in manifest['files']}
    rows, seen_events = [], set()
    for rid, entries in sorted(groups.items()):
        bodies = {canonical(row) for _, _, row in entries}
        require(len(bodies) == 1, 'Unexplained same-ID body conflict: '+rid)
        row = entries[0][2]
        origin, basis, evidence = 'ORIGIN_UNRESOLVED', 'NO_REVIEWED_RELEASE_BASELINE_OR_PERMANENCE_PROOF', None
        if rid in EVENTS:
            source, basis = EVENTS[rid]
            evidence = PREFIX+'STONEAGE-'+source+'.json'
            require(evidence in objects, 'Missing reviewed event source')
            require(any(path == evidence for path, _, _ in entries), 'Event ID absent from reviewed source')
            origin = 'OPERATOR_EVENT_QUEST'
            seen_events.add(rid)
        rows.append({'record_id': rid, 'entity_type': row['entity_type'],
            'collection_as_stored': row.get('collection'), 'version_profile': row['version_profile'],
            'record_body_sha256': hashlib.sha256(next(iter(bodies)).encode()).hexdigest(),
            'origin_class': origin, 'classification_basis': basis,
            'reviewed_evidence_path': evidence,
            'reviewed_evidence_git_blob': pins[evidence]['git_blob'] if evidence else None,
            'baseline_core_admission': False, 'server_execution_proven_by_this_review': False,
            'occurrences': [{'path': path, 'pointer': pointer, 'git_blob': pins[path]['git_blob']}
                            for path, pointer, _ in entries]})
    require(seen_events == set(EVENTS), 'Reviewed event missing from census')
    overlay = objects[OVERLAY]
    require(len(overlay['records']) == 6, 'Prior report-level overlay changed')
    domains = objects[PORTFOLIO]['domains']
    require(len(domains) == 22 and len({d['id'] for d in domains}) == 22, 'Domain index changed')
    counts = Counter(row['origin_class'] for row in rows)
    return {'schema': 'stoneage.quest_material_review.r116', 'date': '2026-10-24',
        'baseline_head': HEAD, 'baseline_tree': TREE, 'input_manifest_sha256': MANIFEST_SHA,
        'evidence_class': 'DERIVED_ARCHIVE_ROUTING_NO_NEW_HISTORICAL_SOURCE',
        'selection_rule': 'record_id_AND_entity_type_AND_collection=quests_OR_exact_entity_type=quest',
        'scope_exclusions': ['NOT_ALL_LEGACY_SCHEMAS', 'NOT_ALL_EVENTS_OR_NPCS', 'NOT_NATIVE_QUEST_ENTITY_COUNT'],
        'counts': {'frozen_json_files': len(objects),
            'selected_record_occurrences': sum(map(len, groups.values())),
            'files_with_selected_records': len({p for entries in groups.values() for p, _, _ in entries}),
            'unique_research_record_ids': len(rows),
            'identical_repeat_occurrences': sum(map(len, groups.values()))-len(rows),
            'unrouted_collection_ids': sum(r['collection_as_stored'] is None for r in rows),
            'by_origin': {category: counts[category] for category in CATEGORIES}},
        'material_views': {category: [r['record_id'] for r in rows if r['origin_class'] == category]
                           for category in CATEGORIES},
        'records': rows,
        'prior_report_level_overlay': {'path': OVERLAY, 'git_blob': pins[OVERLAY]['git_blob'],
            'record_count': 6, 'entries': overlay['records'],
            'report_level_classes_are_not_inherited_by_every_child_record': True,
            'counts_must_not_be_added_to_research_record_or_game_quest_counts': True},
        'domain_review': [{'id': d['id'], 'order': d['order'], 'baseline_status': d['baseline_status'],
            'anchor': d['anchor'], 'anchor_git_blob': pins[d['anchor']]['git_blob'],
            'remaining_gap': d['remaining_gap'], 'original_source_complete': False} for d in domains],
        'interpretation': {'research_rows_are_native_quests': False, 'new_historical_source_acquired': False,
            'old_source_reports_rewritten': False, 'base_or_permanent_origin_verified_this_review': False,
            'unresolved_means_missing_origin_proof_not_absent_from_original_game': True,
            'repeatability_implies_permanence': False, 'permanent_event_reward_changes_event_origin': False,
            'same_name_cross_version_merge_allowed': False, 'public_export_approved': False,
            'stage_a': '7_PARTIAL_2_OPEN', 'stage_b': 'GATED', 'savedata_r79': 'PAUSED_NON_BLOCKING',
            'overall_restoration_percentage': None},
        'next': {'task': 'EARLY-BASE-QUEST-PROVENANCE-117',
            'target': 'One early adulthood-rite or four-cave quest release-baseline attribution, before unrelated later events',
            'required_new_evidence': 'Same-region dated official release/manual/update or authenticated same-build script; old guide alone insufficient',
            'stop': 'One source-qualified attribution or exact bounded acquisition gap; no inferred permanent/base promotion or helper expansion'}}

def verify(root=ROOT):
    manifest, objects = load_inputs(root)
    expected = summarize(manifest, objects)
    actual = json.loads((root/REPORT).read_bytes())
    require(actual == expected, 'Committed review differs from semantic replay')
    return expected

if __name__ == '__main__':
    result = verify()
    print(json.dumps(result['counts'], ensure_ascii=False, sort_keys=True))
    print('R116 frozen material and quest-origin replay PASS; no original server claim')
