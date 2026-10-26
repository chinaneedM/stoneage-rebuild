"""Replay a finite named web-position to actually acquired illustration join.

This offline guard does not reacquire pixels or claim an original game identity.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from tools.stoneage_jp_pet_visual_r25_source import PARENT, PRIOR, PARENT_SHA, PRIOR_SHA, SELECTION, selected, need

BASE=Path('research/recovered')
SOURCE=BASE/'STONEAGE-JP-PET-VISUAL-R25-ACTUAL-SOURCE-R1.json'
OBSERVATIONS=BASE/'STONEAGE-JP-PET-VISUAL-R25-OBSERVATIONS-R1.json'
REPORT=BASE/'STONEAGE-JP-PET-VISUAL-R25-R1.json'
CUSTODY=BASE/'STONEAGE-JP-PET-VISUAL-R25-CUSTODY-R1.json'
SOURCE_SHA='ffa2bcfcb49aca7335d393c1f5bb680c76b05f61149ce8be72ee59778f565494'


def fingerprint(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def build(source, observations):
    parents=selected(PARENT.read_bytes(),PRIOR.read_bytes())
    need(source['schema']=='stoneage.jp_named_pet_visual_r25.actual_source.v1','source schema changed')
    need(source['selection']==SELECTION and len(source['entries'])==12,'source range changed')
    need(source['source_pins']=={str(PARENT):{'sha256':PARENT_SHA},str(PRIOR):{'sha256':PRIOR_SHA}},'source provenance changed')
    need(all(v is False for v in source['boundaries'].values()),'source evidence boundary promoted')
    reviews=observations['entries'];seen=set();records=[]
    for p,e in zip(parents,source['entries']):
        n=p['web_ordinal'];need(e['web_ordinal']==n and e['attempt_count']==1,'reordered/repeated acquisition')
        need(e['parent_record_id']==p['record_id'] and e['name_as_written']==p['name_as_written']
             and e['version_profile']==p['version_profile'] and e['page_source']==p['source_refs'][0]
             and e['original_url']==p['image']['original_url'],'name/source/epoch rebound')
        need(e['visual_review_performed_at_source'] is False,'source runner cannot assert human/model review')
        good=e['image'] is not None
        image={'original_url':e['original_url'],'pixels_acquired':good,
               'same_instant_as_page_proven':False,'original_client_sprite_or_animation_proven':False}
        refs=[dict(e['page_source'])];review=None
        if good:
            m=e['image'];o=reviews.get(str(n));need(o is not None,'qualified source lacks actual visual review')
            need(e['status']=='SOURCE_GIF_BYTES_QUALIFIED_PENDING_PRIVATE_VISUAL_REVIEW','qualified status changed')
            need(m['strict_replay_url']=='https://web.archive.org/web/'+m['actual_capture']+'id_/'+e['original_url']
                 and re.fullmatch(r'[0-9]{14}',m['actual_capture']) is not None,'capture/path changed')
            need(m['format']=='GIF' and m['actual_size']==[60,65] and m['frames']==1,'image structure changed')
            need(e['http']['status']==200 and e['http']['response_sha256']==m['sha256']
                 and e['http']['response_bytes']==m['bytes'],'response/body digest mismatch')
            for k in ('sha256','rgba_sha256','decoded_png_sha256'):
                need(re.fullmatch('[a-f0-9]{64}',m[k]) is not None,'invalid image digest')
            need(o['decoded_png_sha256']==m['decoded_png_sha256'] and o['rgba_sha256']==m['rgba_sha256'],
                 'viewed PNG pixels differ from source GIF decode')
            need(o['authenticated_decryption'] is True and o['assistant_viewed'] is True
                 and o['method']=='VIEW_IMAGE_AUTHENTICATED_DECODED_PNG_SHEET'
                 and o['identity_or_taxonomy_inferred'] is False and bool(o['observations']),
                 'missing actual bounded visual review')
            seen.add(str(n));review=o;image.update(m)
            refs.append({'source':e['original_url'],'actual_capture':m['actual_capture'],'sha256':m['sha256'],
                         'evidence_role':'NAMED_WEB_ILLUSTRATION_NOT_CLIENT_RESOURCE_ID'})
        else:
            need(e['status']=='UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT' and bool(e['failure']),
                 'unavailable source incorrectly upgraded')
            need(str(n) not in reviews,'unavailable source has invented pixel observation')
            image.update(actual_capture=None,sha256=None,actual_size=None,frames=None)
        records.append({'record_id':f'jp-hangame-pet-web:visual-r25:{n:03d}','record_revision':1,
                        'collection':'pets','entity_type':'OFFICIAL_NAMED_PET_WEB_VISUAL_REFERENCE',
                        'version_profile':p['version_profile'],'parent_record_id':p['record_id'],
                        'web_ordinal':n,'name_as_written':p['name_as_written'],'source_refs':refs,
                        'verification_status':'NAMED_WEB_ILLUSTRATION_BYTES_AND_VISUAL_REVIEW_QUALIFIED' if good
                           else 'REFERENCE_ONLY_UNAVAILABLE_THIS_SINGLE_ATTEMPT',
                        'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'client_species_graphic_ids':None,'cross_region_aliases':None,
                        'stats_growth_habitat_skills':None,'image':image,'visual_review':review,
                        'acquisition_attempt_count':1,'failure_this_attempt':e.get('failure')})
    need(set(reviews)==seen,'unselected/invented observations')
    qualified=sum(x['image']['pixels_acquired'] for x in records)
    counts={'attempted_references':12,'previously_qualified_references':13,'qualified_gifs':qualified,
            'unavailable_or_unqualified':12-qualified,'qualified_reference_total':13+qualified,
            'unacquired_references':111-qualified}
    need(source['counts']==counts,'coverage changed or already-acquired source double counted')
    return {'schema':'stoneage.jp_named_pet_visual_r25.v1','date':'2026-10-26',
            'task':'JP-OFFICIAL-NAMED-PET-VISUAL-BATCH-25','parent_catalog':str(PARENT),
            'prior_sample':str(PRIOR),'source_report':str(SOURCE),'selection':SELECTION,
            'records':records,'counts':counts,
            'new_image_capture_year_counts':dict(sorted(Counter(x['image']['actual_capture'][:4] for x in records if x['image']['pixels_acquired']).items())),
            'boundaries':{'original_assets_in_git':False,'plain_original_assets_in_ci_artifact':False,
                          'original_gif_bytes_independently_rehashed_locally':False,
                          'decoded_png_and_rgba_independently_rehashed_locally':True,
                          'source_pngs_durably_delivered_to_user':False,
                          'web_position_or_filename_is_client_id':False,
                          'tw10_or_cross_region_species_identity_proven':False,
                          'same_contemporaneous_roster_or_client_build_proven':False,
                          'original_game_sprite_or_animation_proven':False,
                          'original_game_executed':False,'original_world_entered':False,
                          'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING',
                          'overall_completion_percent':None},
            'next':'CN5-ADDITIONAL-ANIMATION-MATERIAL-26'}


def validate(doc):
    raw=SOURCE.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'actual source archive byte drift')
    observations=json.loads(OBSERVATIONS.read_bytes())
    need(doc==build(json.loads(raw),observations),'permanent named material join differs from source')
    need(doc['counts']['qualified_gifs']==10 and doc['counts']['unacquired_references']==101,'actual result changed')
    custody=json.loads(CUSTODY.read_bytes())
    need(custody['source_report']==fingerprint(raw),'source raw report custody mismatch')
    need(custody['source_head']=='48cb16d272c57c43bb47ac4cb8e1e72af5709d18'
         and custody['source_run']==40313523035 and custody['source_job']==121540306670
         and custody['artifact_id']==12646430311
         and custody['artifact_zip_sha256']=='5bd2a5b1bc16e206e23202324fae5848fbee20a4bf3a6c1d51f63c3f5a1f3820',
         'source run/artifact chain changed')
    need(custody['artifact_member_allowlist']==['private-png-envelopes.json','source-derived.json'],
         'unqualified or plaintext artifact member')
    return doc['counts']


if __name__=='__main__':
    print(json.dumps({'status':'PASS','counts':validate(json.loads(REPORT.read_bytes()))}))
