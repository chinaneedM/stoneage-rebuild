"""One acquired named web image; no client sprite, animation or cross-region ID."""
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
from PIL import Image
from tools.stoneage_early_content_probe import require
from tools.stoneage_wayi_newbie_riding_plan import fetch

PARENT=Path('research/recovered/STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1.json')
PARENT_SHA='9a460c23968a714717b375d823308bb5e56848116aaf44880091b75808024df6'
ORIGINAL='http://www.waei.com.cn/ZHUANQU/stoneage2/pet/img/newpet/7.JPG'
CAPTURE='20011205051046'
URL='https://web.archive.org/web/'+CAPTURE+'id_/'+ORIGINAL
SOURCE_SHA='7077cef8cfc23d67b34e3ed54ef6c57eca4c1197b44a2c513c4e43dfa1f85b30'
REPORT=Path('research/recovered/STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-R1.json')


def validate_report(o):
    r=o['records'][0]
    require(len(o['records'])==1 and r['source_name_as_written']=='阿米朵'
            and r['existing_catalog_record_id']=='waei-cn20:new-pet-web-position:007'
            and r['source_position']=={'ordinal':7,'row':2,'column':2},'Actual named source position differs')
    im=r['acquired_image'];require(im['actual_capture']==CAPTURE and im['sha256']==SOURCE_SHA
                                 and im['bytes']==4831 and im['format']=='JPEG' and im['dimensions']==[83,90]
                                 and im['frames_in_this_image_file']==1 and im['mode']=='RGB','Exact acquired image metadata differs')
    require(r['catalog_body_capture']=='20011204194619' and r['html_declared_dimensions_for_this_position'] is None
            and r['image_and_page_are_proven_same_instant_or_build'] is False,
            'Actual image dimensions/capture projected back into the page')
    require(r['manual_inspection']['exact_image_sha256']==SOURCE_SHA
            and r['manual_inspection']['performed_by']=='ASSISTANT_VIEW_IMAGE_ORIGINAL_PIXELS'
            and r['manual_inspection']['independent_runner_repeats_human_visual_inspection'] is False,
            'Visual inspection detached from exact image or attributed to CI')
    require(r['client_sprite_animation_model_or_native_palette_verified'] is False
            and r['static_jpeg_means_pet_has_no_animation'] is False
            and r['original_game_pet_id_stats_or_cross_region_alias'] is None,
            'Web illustration promoted to original sprite, animation, species ID or alias')
    require(o['coverage']['actual_images_acquired']==1 and o['coverage']['other_first_page_image_refs_unacquired']==39
            and o['coverage']['new_game_pet_entities']==0
            and o['coverage']['prior_report_historical_unacquired_state_rewritten'] is False,
            'One acquired image promoted to broader recovery or historical rewrite')


def build(parent_bytes,body,final):
    require(sha256(parent_bytes).hexdigest()==PARENT_SHA,'Exact immutable parent catalog required')
    parent=json.loads(parent_bytes);position=parent['records'][6]
    require(position['record_id']=='waei-cn20:new-pet-web-position:007'
            and position['name_as_written']=='阿米朵' and position['image_reference']['original_url']==ORIGINAL
            and position['image_reference']['actual_capture'] is None,'Actual name-to-reference cell binding differs')
    require(final==URL,'Exact final image original URL/capture required')
    require(len(body)==4831 and sha256(body).hexdigest()==SOURCE_SHA,'Exact image byte pin differs')
    with Image.open(io.BytesIO(body)) as im:
        metadata={'format':im.format,'dimensions':list(im.size),'frames_in_this_image_file':getattr(im,'n_frames',1),'mode':im.mode}
        im.verify()
    require(metadata=={'format':'JPEG','dimensions':[83,90],'frames_in_this_image_file':1,'mode':'RGB'},'Actual file format/dimensions differ')
    r={'record_id':'waei-cn20:new-pet-visual:position-007','collection':'pets',
       'entity_type':'NAMED_WEB_IMAGE_REFERENCE_SUPPLEMENT_NOT_NEW_GAME_PET','record_revision':1,
       'version_profile':'CN_WAEI_2_0_LABEL_PAGE_20011204_IMAGE_20011205_NOT_EXACT_BUILD',
       'source_refs':[{'path':str(PARENT),'derived_sha256':PARENT_SHA,'json_pointer':'/records/6',
                       'catalog_original_url':parent['source']['original_url'],'catalog_sha256':parent['source']['sha256'],
                       'image_original_url':ORIGINAL,'image_capture':CAPTURE,'image_sha256':SOURCE_SHA}],
       'verification_status':'EXACT_NAMED_SOURCE_IMAGE_ACQUIRED_AND_MANUALLY_INSPECTED_NOT_CLIENT_ID',
       'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','source_name_as_written':'阿米朵',
       'existing_catalog_record_id':position['record_id'],'source_position':position['source_position'],
       'catalog_body_capture':parent['source']['actual_capture'],
       'html_declared_dimensions_for_this_position':position['image_reference']['html_declared_dimensions'],
       'acquired_image':{'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,
                         'bytes':len(body),'sha256':SOURCE_SHA,**metadata},
       'image_and_page_are_proven_same_instant_or_build':False,
       'manual_inspection':{'exact_image_sha256':SOURCE_SHA,'performed_by':'ASSISTANT_VIEW_IMAGE_ORIGINAL_PIXELS',
                             'observations':['Small vertically framed creature illustration on mottled green and yellow background.',
                                             'Yellow to olive head, open mouth with red interior, and pale neck/belly areas.',
                                             'Prominent pale horn-like projections and dark-edged projections along the right silhouette.'],
                             'taxonomy_species_stats_or_client_pose_inferred':False,
                             'independent_runner_repeats_human_visual_inspection':False},
       'client_sprite_animation_model_or_native_palette_verified':False,
       'static_jpeg_means_pet_has_no_animation':False,'original_game_pet_id_stats_or_cross_region_alias':None}
    o={'schema':'stoneage.waei_cn20.amiduo_visual_reference.r1','date':'2026-10-19',
       'task':'CN20-NEW-PET-NAMED-VISUAL-REFERENCE-01','records':[r],
       'source_custody':{'parent_git_report_sha256':PARENT_SHA,'original_catalog_or_entry_html_reacquired_by_this_job':False,
                         'initial_requested_capture':'20011204194619','actual_image_capture':CAPTURE,
                         'human_inspection_is_distinct_from_machine_metadata_replay':True},
       'coverage':{'actual_images_acquired':1,'other_first_page_image_refs_unacquired':39,'new_game_pet_entities':0,
                    'prior_report_historical_unacquired_state_rewritten':False,'unread_pagination_bodies':2},
       'boundaries':{'raw_original_image_html_or_program_in_git':False,'production_reuse_approved':False,
                      'jss1999_tw10_cn182_or_25_same_build_or_entity_verified':False,
                      'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
       'next':'CN20-NEW-PET-CATALOG-FINITE-PAGINATION-01'}
    validate_report(o);return o


def main():
    p=argparse.ArgumentParser();p.add_argument('--input-image');p.add_argument('--output',required=True);a=p.parse_args()
    body,final=(Path(a.input_image).read_bytes(),URL) if a.input_image else fetch(URL)
    o=build(PARENT.read_bytes(),body,final);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('PARENT_SHA256='+PARENT_SHA);print('IMAGE_SHA256='+SOURCE_SHA)
    print('ACTUAL_IMAGES=1 JPEG=83x90 FILE_FRAMES=1 OTHER_FIRST_PAGE_IMAGES_UNACQUIRED=39')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
