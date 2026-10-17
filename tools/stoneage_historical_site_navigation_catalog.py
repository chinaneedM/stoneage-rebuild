"""Replay a finite source-link graph and proposed research collection routing."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
from tools.stoneage_historical_site_navigation_probe import TARGETS, TOPICS, archive_parts, identity, require

ROUTES = {'login_splash': 'screens', 'character_creation': 'characters', 'pet_species': 'pets',
          'quest_content': 'quests', 'world_map': 'maps', 'battle_ui_rules': 'tutorials',
          'item_equipment_economy': 'items', 'reference_web': 'historical_sites', 'helper_versions': 'helper_programs'}
QUALIFIED = 'ARCHIVED_HTML_LINK_METADATA_QUALIFIED'


def page_key(url):
    return identity(urllib.parse.urldefrag(url)[0])


def build(report):
    require(report['schema'] == 'stoneage.historical_site_navigation.r1', 'source schema')
    require(set(report['targets']) == set(TARGETS), 'finite target set')
    for flag in ['historical_site_structure_fully_recovered', 'website_implemented', 'original_html_images_or_binaries_retained', 'source_absence_established']:
        require(report[flag] is False, 'source boundary: ' + flag)
    pages, by_url, gaps = [], {}, []
    for key, source in sorted(report['targets'].items()):
        require(source['requested_original'] == TARGETS[key][0], 'target identity: ' + key)
        if source['status'] != QUALIFIED:
            require('NOT_GLOBAL_ABSENCE' in source['status'], 'gap promoted to absence')
            gaps.append({'target_id': key, 'status': source['status'], 'reopen': 'NAMED_EARLY_CAPTURE_OR_BOUNDED_ALTERNATE_ARCHIVE_INDEX'})
            continue
        ts, original = archive_parts(source['final_url'])
        require(ts == source['actual_capture'] and '19990101000000' <= ts <= '20021231235959', 'capture date')
        require(identity(original) == identity(source['requested_original']), 'changed replay original')
        require(source['visual_layout_verified'] is False and source['linked_destination_contents_verified'] is False and source['full_historical_site_recovered'] is False, 'unsupported visual/site claim')
        require(source['replacement_characters'] == 0, 'requalify damaged decoding')
        require(len(source['links']) == source['link_count'], 'link count')
        node = {'page_id': key, 'original_url': original, 'capture': ts, 'source_sha256': source['sha256'],
                'source_role': source['source_role'], 'game_build_scope': None,
                'scope': 'ARCHIVED_WEB_PAGE_NOT_ORIGINAL_GAME_DATABASE'}
        pages.append(node); by_url.setdefault(page_key(original), []).append(key)
    require(report['qualified_pages'] == len(pages), 'qualified page count')
    edges, routes = [], []
    for page in pages:
        key = page['page_id']; source = report['targets'][key]
        for ordinal, link in enumerate(source['links']):
            require(link['source_order'] == ordinal, 'source link order')
            require(link['topic_match_basis'] == 'ANCHOR_LABEL_HEURISTIC_NOT_DESTINATION_VERIFICATION', 'topic confidence promoted')
            target = link['target_url']; parsed = urllib.parse.urlsplit(target)
            require(parsed.scheme in ('http', 'https') and not parsed.username and not parsed.password, 'unsafe URL')
            same_host = parsed.hostname == urllib.parse.urlsplit(source['actual_original']).hostname
            require(same_host == link['same_host'], 'same-host metadata drift')
            candidates = by_url.get(page_key(target), [])
            checks = [{'target_page_id': target_id,
                       'fragment_present_in_acquired_snapshot': parsed.fragment in report['targets'][target_id]['document_anchor_ids'] if parsed.fragment else None,
                       'same_capture_timestamp': report['targets'][target_id]['actual_capture'] == source['actual_capture']}
                      for target_id in candidates]
            edge_id = key + ':LINK:' + str(ordinal)
            edges.append({'edge_id': edge_id, 'source_page_id': key, 'target_url': target, 'link_kind': link['link_kind'],
                          'target_kind': link['target_kind'], 'source_order': ordinal,
                          'target_snapshot_candidates': checks, 'historical_click_execution_verified': False})
            require(set(link['topic_candidates']) <= set(TOPICS), 'unknown domain candidate')
            for domain in link['topic_candidates']:
                routes.append({'edge_id': edge_id, 'domain_candidate': domain, 'collection_candidate': ROUTES[domain],
                               'status': 'PROPOSED_RESEARCH_ROUTING_NOT_HISTORICAL_CONTENT_ATTRIBUTION'})
    return {'schema': 'stoneage.historical_site_navigation_catalog.r1',
            'pages': pages, 'links': edges, 'routing_candidates': routes, 'gaps': gaps,
            'counts': {'qualified_pages': len(pages), 'link_records': len(edges),
                       'distinct_target_urls': len({e['target_url'] for e in edges}),
                       'routing_candidates': len(routes), 'unqualified_targets': len(gaps)},
            'all_historical_sites_recovered': False, 'historical_layout_verified': False,
            'linked_game_content_verified': False, 'website_implemented': False, 'public_export_enabled': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); raw = args.source.read_bytes(); result = build(json.loads(raw))
    result['source_report_sha256'] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps(result['counts']))


if __name__ == '__main__': main()
