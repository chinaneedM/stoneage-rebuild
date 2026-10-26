"""Replay one authenticated public-source stop; never upgrade it to acquisition."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_kr_netmarble120_r27_source import URL, TOKEN, need

BASE=Path('research/recovered')
SOURCE=BASE/'STONEAGE-KR-NETMARBLE120-R27-ACTUAL-SOURCE-R1.json'
CUSTODY=BASE/'STONEAGE-KR-NETMARBLE120-R27-CUSTODY-R1.json'
REPORT=BASE/'STONEAGE-KR-NETMARBLE120-R27-R1.json'
SOURCE_SHA='4e1ca148ec2571f13983e3d3d125116404ed3d6c57eb2d73b9110c2ab919b2f1'


def fingerprint(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def build(source,custody):
    need(source['schema']=='stoneage.kr_netmarble120_r27.actual_public_source.v1','source schema changed')
    need(source['requested_url']==URL and source['target_token']==TOKEN and source['public_source_attempts']==1,
         'source or finite attempt scope changed')
    o=source['observation']
    need(o['state']=='PUBLIC_SOURCE_ACCESS_GATED_STOP' and o['http_status']==200 and o['final_url']==URL,
         'actual access denial state lost')
    need(o['target_token_in_title'] is True and o['target_token_in_post'] is False
         and o['access_gate_markers']==['您無權進行當前操作'] and o['public_package_links']==[],
         'title/body/package gate conflated')
    need((o['response_bytes'],o['response_sha256'])==(10543,'586ce9a4f2b8eb4d0e4f9b21b8e5e87a66f48d50fada01063da844e0610c8f3f'),
         'HTTP response metadata changed')
    need(source['package']=={'downloaded':False,'bytes':None,'sha256':None,'declared_version':None,
          'extracted_client_files':0,'official_clean_authenticated':False},'unobtained package promoted')
    need(all(v is False or type(v) is int and v==0 for v in source['boundaries'].values()),'unsupported source claim')
    need(custody['source_run']==40317910236 and custody['source_job']==121555053832
         and custody['source_head']=='29c043ccf1691e35cb90a85e31324f2f2dfd1ac0'
         and custody['artifact_id']==12647084542
         and custody['artifact_zip_sha256']=='23ccdf79c873b50ca1c00c559c7d7f011570fa76a0139dd397e60eae7526e8d8'
         and custody['artifact_member_allowlist']==['source-derived.json'],'source custody chain changed')
    return {'schema':'stoneage.kr_netmarble120_r27.bounded_outcome.v1','date':'2026-10-26',
        'task':'KR-NETMARBLE120-CLIENT-SOURCE-27','status':'OPEN_PUBLIC_SOURCE_ACCESS_GATED_NO_PACKAGE_OBTAINED',
        'observed_source':{'url':URL,'title':o['title'],'response_bytes':o['response_bytes'],
            'response_sha256':o['response_sha256'],'visible_title_token':True,
            'post_body_available':False,'access_denial':o['access_gate_markers'],
            'unambiguous_download_link_obtained':False},
        'material_result':{'new_client_samples':0,'new_package_bytes':0,'new_extracted_client_files':0,
            'package_sha256':None,'client_version':None,'official_clean_authenticated':False,
            'existing_four_client_corpus_extended':False},
        'source_custody':str(CUSTODY),'source_raw_report':str(SOURCE),
        'boundaries':{'source_workflow_success_means_download_success':False,
            'historical_client_or_website_does_not_exist_proven':False,
            'source_requires_specific_account_or_payment_mechanism_proven':False,
            'korean_174_or_token_120_version_identity_proven':False,'access_gate_bypassed':False,
            'original_program_executed':False,'new_npc_pet_quest_identity_proven':False,
            'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING',
            'overall_completion_percent':None},
        'reopen_only':'New explicitly public downloadable carrier link or owner-provided legitimately accessible package; not repeated permission probes',
        'next':'TW85-SPR137-ORIGINAL-MATERIAL-28'}


def validate(doc):
    raw=SOURCE.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'raw original source report changed')
    custody=json.loads(CUSTODY.read_bytes());need(custody['source_report']==fingerprint(raw),'raw report custody changed')
    need(doc==build(json.loads(raw),custody),'permanent bounded source outcome differs')
    return {'status':'PASS','source_state':doc['status'],'new_client_samples':0,'package_bytes_obtained':0}


if __name__=='__main__':print(json.dumps(validate(json.loads(REPORT.read_bytes()))))
