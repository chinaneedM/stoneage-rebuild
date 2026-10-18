"""Finite22-domain review from immutable local evidence; no network or game IO."""
import argparse
import json
from pathlib import Path
from tools.stoneage_wayi_official_worldline import ARCHIVE, PRIOR, REPORT, dump, metadata, require

NOTES = {
    'version_lineage': 'Official2005 synopsis explicitly groups nine historical version labels; not nine authenticated clients or universal canon.',
    'login_splash': 'No new login pixels or original interaction trace; official site shell is not the game login screen.',
    'character_creation': 'Prior JSS12 bodies/48 appearances retained; no new named avatar roster.',
    'character_sprite_model': 'Original numeric frame joins retained; no new named character-to-animation mapping.',
    'world_map': 'New official names Nis/Eden/lost world and undersea-to-ice-gap story relation; no playable floor IDs, coordinates or map bytes.',
    'npc_identity': 'Spirit King is an official narrative figure; no NPC master ID or proof of an interactable NPC. Prior venue roles remain anonymous.',
    'npc_dialog_ui': 'No original dialogue state trace; narrative paragraph cannot stand in for NPC speech or quest script.',
    'quest_content': 'Prior social announcements/result, FAQ issue labels and dated pet changes remain distinct from scripted quests. Lost-world question remains open.',
    'pet_species': 'Rare contest prize still unnamed; new world synopsis supplies no pet species roster or graphic binding.',
    'pet_visual': 'Prior qualified JSS thumbnails remain; new page has eight individually viewed original GIF slices and one404; partial illustration, not a species census.',
    'pet_stats': 'Prior loyalty description and pet-name/boarding defect labels preserved; no new same-build species parameters.',
    'pet_growth': 'No original growth table; do not derive growth coefficients from civilization or narrative development.',
    'pet_skills': 'Prior1999-11-08 synthesis/cooking additions and dated generic skill fixes retained; exact FAQ symptom joins still unproven.',
    'pet_encounter': 'Prior distinct12-hour and5-minute pet-mail contexts retained; neither supplies original encounter/spawn tables.',
    'ride_mount': 'No new ride unlock source; first-ride emotional value is a future design priority, not proof of launch availability.',
    'battle_ui_rules': 'Prior FAQ duel-ranking refresh and256-color/time-palette description preserved; no new turn rules or actual UI pixels.',
    'item_equipment_economy': 'Prior pet boarding availability and processing descriptions retained; no original fees, recipes or inventory master.',
    'audio_fx': 'Prior FAQ compatibility advice and original API metadata remain; no new scene-to-track mapping.',
    'helper_versions': 'Legacy helper catalog unchanged; community/helper chronology is separate from official fictional history.',
    'helper_capabilities': 'No assistant feature implementation or adoption decision; prior historical feature scope retained.',
    'reference_web': 'New actual home-to-game-intro edge, five source-ordered version groups, four unqueried detail links and nine image references.',
    'future_player_wiki': 'Provenance-bearing derived records only; game/wiki production and original-asset reuse remain gated.',
}


def review(prior, archive):
    old = prior['reviewed_domains']
    require(len(old) == 22 and len({x['domain_id'] for x in old}) == 22, 'prior22-domain coverage changed')
    require({x['domain_id'] for x in old} == set(NOTES), 'review notes do not match domain IDs')
    require(len(archive['version_profiles']) == 7, 'prior coarse profile classes changed')
    return [{'domain_id': x['domain_id'], 'original_order': x['original_order'],
             'baseline_evidence_status': x['baseline_evidence_status'],
             'previous_material_disposition': x['current_material_disposition'],
             'r4_material_outcome_or_gap': NOTES[x['domain_id']],
             'historical_status_changed': False, 'version_promotion_allowed': False,
             'tw10_original_content_completed': False} for x in old]


def build():
    prior, archive = [json.loads(Path(p).read_text()) for p in (PRIOR, ARCHIVE)]
    rows = review(prior, archive)
    evidence = [PRIOR, ARCHIVE, REPORT,
        'research/recovered/STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json',
        'research/recovered/STONEAGE-JSS2001-OFFICIAL-EVENT-VENUE-R1.json',
        'research/recovered/STONEAGE-JSS-EVENT-RESULTS-PET-ATTRIBUTION-R1.json',
        'research/recovered/STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1.json',
        'research/recovered/STONEAGE-JSS-PET-PATCH-HISTORY-R1.json',
        'research/recovered/STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json',
        'research/recovered/STONEAGE-WAYI-OFFICIAL-80-DOWNLOAD-CHAIN-R1.json',
        'research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json']
    profiles = [
        ('JSS1999_ORIGIN', 'EARLY_JAPAN', 'CONTEMPORANEOUS_DOCUMENTS_NO_COMPLETE_LAUNCH_BUILD'),
        ('JSS2001_OFFICIAL_WEB', 'JSS_JAPAN', 'QUALIFIED_MANUAL_CONTENT_IMAGES_EVENTS_FAQ_AND_DATED_HISTORY'),
        ('TW10_CLIENT_BASELINE', 'TAIWAN', 'AUTHENTICATED_CLIENT_RESOURCES_NO_ORIGINAL_SERVER_MASTER'),
        ('CN182_GUIDE_LAYER', 'MAINLAND', 'VERSIONED_GUIDES_NOT_AUTHENTICATED_TW10_SERVER'),
        ('TW2005_OFFICIAL_WEB', 'TAIWAN_WAYI', 'QUALIFIED_WORLD_SYNOPSIS_AND_OPERATOR_PAGES'),
        ('TW75_OFFICIAL_DOWNLOAD_POINTER', 'TAIWAN_WAYI', 'OPERATOR_LABEL_AND_URL_NO_FULL_INSTALLER_IDENTITY'),
        ('TW80_OFFICIAL_DOWNLOAD_CHAIN', 'TAIWAN_WAYI', 'DATED_OPERATOR_LISTING_AND_BOUNDED_UPDATER_NOT_FULL_INSTALLER'),
        ('TW85_COMMUNITY_CARRIER_LEAD', 'CLAIMED_TAIWAN', 'COMMUNITY_LANDING_METADATA_NOT_AUTHENTICATED_OFFICIAL_BYTES'),
        ('RECOVERED25_DESCENDANT', 'SOURCE_TREE_LINEAGE', 'DESCENDANT_MATERIAL_NOT_ORIGINAL_OFFICIAL_SERVER_PROOF'),
    ]
    world = json.loads(Path(REPORT).read_text())
    require(world['world']['lost_world_identity']['chosen_answer'] is None, 'unresolved world identity was promoted')
    return {'schema': 'stoneage.cross_domain_material_evidence_review.r4', 'task': 'PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-04',
            'date': '2026-10-18', 'sources': [metadata(p) for p in evidence], 'reviewed_domains': rows, 'reviewed_domains_count': 22,
            'official_reference_coverage': {'coarse_prior_profile_classes': archive['version_profiles'],
                'known_evidence_contexts': [{'context': k, 'region_or_lineage': region, 'actual_evidence_level': level} for k, region, level in profiles],
                'contexts_are_distinct_official_release_count': False, 'all_official_release_census_complete': False,
                'unfilled_coverage': ['COMPLETE_REGION_OPERATOR_PRODUCT_PATCH_INVENTORY', 'NAMED_PET_NPC_QUEST_TABLES_PER_RELEASE', 'SOURCE_QUALIFIED_REGIONAL_BRANCH_AND_RETCON_LINKS'],
                'later_official_content_allowed_on_its_own_version_merits': True, 'same_build_early_promotion_without_source_allowed': False},
            'new_material_result': {'world_synopsis_report': REPORT, 'newly_acquired_world_pages': 1, 'reacquired_existing_home': 1,
                'version_groups': 5, 'literal_version_labels': 9, 'actual_image_slices_acquired': 8, 'unobtained_image_slices': 1,
                'real_release_and_fictional_chronologies_separated': True, 'lost_world_identity_question_answered': False},
            'selected_package': {'task': 'TW-WAYI-OFFICIAL-WORLDLINE-SOURCE-01', 'result': 'ONE_ACTUAL_OFFICIAL_NARRATIVE_PAGE_QUALIFIED',
                'reason': 'Actual operator synopsis directly connects named continents and version labels; adds world/story material rather than more API metadata.',
                'stop_condition_met': 'One actual introduction page via existing authenticated home; eight necessary illustration slices qualified, one404; no further detail/Flash/ActiveX crawl.'},
            'next_priority': {'task': 'TW-WAYI-OFFICIAL-INTRO-DETAIL-01',
                'scope': 'One of four actual game01 detail links, selected from source order if labels remain unknown; validate its own heading/content before attributing topic.',
                'goal': 'One named story, character, pet, environment or gameplay contract in the Taiwan official-web profile.',
                'stop': 'One qualified detail, or one bounded unsuccessful attempt then reassess. Never infer topic/version from numeric filename; no forms or software.'},
            'boundaries': {'stage_a_system_families': {'PARTIAL': 7, 'OPEN': 2}, 'all22_historical_statuses_preserved': True,
                           'original_server_or_full_world_recovered': False, 'stage_b_production': 'GATED', 'public_wiki_implementation_started': False,
                           'r79': 'PAUSED_NON_BLOCKING', 'overall_restoration_percentage': None}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dump(build()), encoding='utf-8')
    print(json.dumps({'reviewed_domains': 22, 'historical_statuses_changed': 0, 'new_official_world_page': 1, 'all_official_releases_recovered': False}))


if __name__ == '__main__':
    main()
