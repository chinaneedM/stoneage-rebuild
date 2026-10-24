"""Verify durable metadata from the completed original-byte acquisition.

This replays custody and the historical SHA join; it does not download or
execute proprietary clients and does not substitute for the source CI run.
"""
import hashlib
import json
from pathlib import Path
import subprocess

from tools.stoneage_tw10_preserved25_file_intersection import ROOT, GIT_BLOBS, git_blob, replay, validate as validate_join

REPORT = 'research/recovered/STONEAGE-ORIGINAL-BYTE-REACQUISITION-R1.json'
RECEIPT = 'research/recovered/STONEAGE-ORIGINAL-BYTE-CUSTODY-R1.json'
PREFIX_PATHS = {'docs/CURRENT-STATE.md', 'docs/HISTORICAL-TIMELINE.md',
                'docs/SOURCE-REGISTRY.md', 'docs/RESTORATION-ROADMAP-R2.md'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_report(report):
    require(report['schema'] == 'stoneage.original_source_reacquired_sha_join_r1', 'schema')
    require(report['status'] == 'SOURCE_BYTES_REACQUIRED_AND_REHASHED', 'source status')
    require(report['github_head_sha'] == '2c93130f10b4414ab1e3226fe0c88aec9edabf41', 'source HEAD')
    require(report['github_run_id'] == '40067698285', 'source run')
    require(report['historical_manifest_git_blobs'] == GIT_BLOBS, 'source manifests')
    require(report['counts'] == replay()['counts'], 'source count replay')
    require(report['tw_core_bytes'] == 373564663, 'Taiwan byte length')
    require(report['bridge_subtree_logical_bytes'] == 863480809, 'bridge byte length')
    for field in ('official_purity_of_bridge_qualified', 'original_payload_published', 'pet_npc_quest_server_data_inferred'):
        require(report[field] is False, 'unsupported promotion: ' + field)
    require(report['archive_digest_gates'] == {
        'tw_archive_md5': 'b37a4a47f4eb608cac67e4ddf7a1621a',
        'tw_archive_sha1': 'b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded',
        'bridge_combined_sha256': 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'}, 'archive gates')


def validate_receipt(receipt):
    require(receipt['base_main'] == 'bab09ab6c9453cbd0e9af2b1631ad5ffe46004d6', 'base identity')
    require(set(receipt['historical_prefixes']) == PREFIX_PATHS, 'incomplete historical coverage')
    require(set(receipt['derived_files']) == {REPORT,
        '.github/workflows/reacquire-stoneage-cross-version-original-bytes.yml',
        'docs/STONEAGE-ORIGINAL-BYTE-REACQUISITION-R1.md'}, 'incomplete source coverage')
    require(receipt['source_run']['id'] == 40067698285 and
            receipt['source_run']['job_id'] == 120794301801 and
            receipt['source_run']['conclusion'] == 'success', 'source job')
    require(receipt['artifact']['zip_bytes'] == 977 and
            receipt['artifact']['member'] == 'stoneage-original-cross-version-derived.json', 'artifact shape')
    for field in ('original_source_payload_retained_after_runner_cleanup',
                  'original_server_entities_recovered', 'local_validation_reexecutes_original_client'):
        require(receipt['boundaries'][field] is False, 'receipt overclaim: ' + field)
    require(receipt['boundaries']['new_official_versions_acquired'] == 0, 'new official version overclaim')


def validate(root=ROOT):
    validate_join()
    receipt = json.loads((root / RECEIPT).read_bytes())
    validate_receipt(receipt)
    raw = (root / REPORT).read_bytes()
    validate_report(json.loads(raw))
    for path, expected in receipt['derived_files'].items():
        data = (root / path).read_bytes()
        require(expected == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': git_blob(data)}, 'derived bytes changed: ' + path)
    require(receipt['artifact']['id'] == 12550560415, 'artifact ID')
    require(receipt['artifact']['zip_sha256'] == '766629c9795a0326b7a767f12ffb7abd7e245202436f69cb65a319cd21a70433', 'artifact ZIP identity')
    require(receipt['source_run']['job_id'] == 120794301801 and receipt['source_run']['conclusion'] == 'success', 'source job')
    require(receipt['source_run']['head_sha'] == json.loads(raw)['github_head_sha'], 'receipt source HEAD')
    for path, pin in receipt['historical_prefixes'].items():
        old = subprocess.check_output(['git', 'show', receipt['base_main'] + ':' + path], cwd=root)
        require(git_blob(old) == pin['git_blob'] and len(old) == pin['bytes'], 'old prefix pin: ' + path)
        require((root / path).read_bytes().startswith(old), 'historical prefix lost: ' + path)
    return {'status': 'PASS', 'scope': 'durable derived custody; original-byte execution belongs to source run 40067698285'}


if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
