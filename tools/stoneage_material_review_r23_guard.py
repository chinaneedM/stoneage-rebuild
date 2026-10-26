"""Keep source material, delivered media, original execution and identity distinct."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_client_content_catalog_r24 import fingerprint, need

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-MATERIAL-PORTFOLIO-REVIEW-R23.json'
BASE = 'research/recovered/'


def read(name):
    return json.loads((ROOT/BASE/name).read_bytes())


def validate(doc):
    baseline = json.loads((ROOT/doc['baseline']['path']).read_bytes())
    need(hashlib.sha256((ROOT/doc['baseline']['path']).read_bytes()).hexdigest()
         == doc['baseline']['sha256'], 'R102 baseline source changed')
    need(len(doc['domains']) == len(baseline['domains']) == 22, 'domain coverage drift')
    for row, prior in zip(doc['domains'], baseline['domains']):
        need(row['baseline'] == prior and row['complete'] is False, 'baseline/identity promoted')
        need(set(row['layers']) == {'material', 'visible_or_audible_delivery',
                                    'original_execution', 'identity_and_missing_source'}, 'missing evidence layer')
        need(all(isinstance(x, str) and bool(x.strip()) for x in row['layers'].values()), 'empty review layer')
        need(row['new_material_evidence'] == bool(row['incremental_sources']), 'false material increment')
        for p in [prior['anchor'], *row['incremental_sources']]:
            need(p in doc['source_pins'], 'unqualified review source')
    for p, pin in doc['source_pins'].items():
        need(fingerprint((ROOT/p).read_bytes()) == pin, 'review source byte drift '+p)
    boot = read('STONEAGE-TW10-ORIGINAL-BOOT-P3-CUSTODY-R1.json')
    palette = read('STONEAGE-TW10-PALETTE-P2B-ACTUAL-COLOR-SOURCE-R1.json')
    audio = read('STONEAGE-PRIVATE-AUDIO-R22-DELIVERY-R1.json')
    expected = {
        'domain_count': 22, 'old_880_file_audit_repeated': False,
        'r17_hash_domain_error_corrected': True,
        'original_client_ever_executed': boot['private_visual_observation']['actual_original_login_panel_visible'],
        'original_world_entered': boot['game_world_entered'],
        'p2b_source_generated_color_previews': len(palette['color_animation_previews']),
        'p2b_original_color_previews_durable_user_delivery': False,
        'r22_private_original_wav_durable': audio['private_file_saved'] and audio['independent_complete_readback'],
        'assistant_heard_audio': audio['assistant_listening_confirmed'],
        'user_playback_confirmed': audio['user_playback_confirmed'],
        'named_tw10_entities_added': 0, 'original_npc_pet_quest_identity_closed': False,
        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING',
        'overall_completion_percent': None,
        'dd028': ['BASE_GAME_QUEST', 'PERMANENT_VERSION_QUEST', 'OPERATOR_EVENT_QUEST', 'ORIGIN_UNRESOLVED'],
    }
    need(doc['facts'] == expected, 'material/visible/audible/runtime/identity boundary conflated')
    selected = doc['selected_material_package']
    need(selected['id'] == 'ACQUIRED-FOUR-CLIENT-COMPLETE-FILE-INTEGRATION-24', 'selected material task drift')
    summary = json.loads((ROOT/selected['deliverable']).read_bytes())
    need(summary['occurrences'] == 3655 and summary['unique_complete_file_contents'] == 2488,
         'selected package lacks material result')
    need(summary['r17_correction']['same_index_sha256_equal_count'] == 218, 'R17 error silently repeated')
    need(doc['next']['id'] == 'JP-OFFICIAL-NAMED-PET-VISUAL-BATCH-25', 'finite content rotation absent')
    return {'domains': 22, 'source_reports': len(doc['source_pins']), 'status': 'PASS'}


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REPORT.read_bytes()))))
