"""Conservative metadata gate; never equate R10 private viewer with native original execution."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE10-STRUCTURAL-PREFLIGHT-R1.json'
TARGETS=(4368676,4198711,4508177,4356772,4506787)
STARTS=(4494410,4495313,4495615,4495953)
GAPS=(8,5,4,6)

def validate(r):
    def ck(cond,msg):
        if not cond: raise ValueError(msg)
    ck(r['schema']=='stoneage.scene10.structural_preflight.r1','schema')
    ck(r['source_head']=='3b79a2aed14b7922e8f4d2284029a1313763c428' and r['source_tree']=='2d85430e5ab8dab6f7f7261ac5e94cc6caf15002','remote source')
    ck(r['source_current_state_blob']=='031c76a5a8e431f646853909bb2f2e11e6328cd2' and r['source_current_state_bytes']==2680510,'CURRENT')
    ck(r['original_exe_claimed_sha256']=='ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16','EXE claim')
    ck(r['private_viewer_sha256']=='00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4' and r['private_viewer_bytes']==1150992,'viewer identity')
    ck(r['evidence_class']=='PRIVATE_VIEWER_RECORDED_CALLS_NOT_INDEPENDENT_EXE_EXECUTION','scope')
    ck(r['original_exe_bytes_available_for_this_preflight'] is False and r['source_callsite_bytes_independently_verified'] is False,'unqualified native code')
    paths=r['four_candidate_paths'];ck(len(paths)==4,'four paths')
    for i,(p,start,gap) in enumerate(zip(paths,STARTS,GAPS)):
        calls=p['key_calls'];sites=[c['call_va'] for c in calls]
        ck(p['start_va']==start and p['end_va_exclusive']>start,'bounded VA')
        ck(len(calls)==5 and tuple(c['target_va'] for c in calls)==TARGETS,'source order')
        ck(sites==sorted(set(sites)) and sites[0]==start and all(start<=v<p['end_va_exclusive'] for v in sites),'bounded callsites')
        ck(p['unreplayed_intervening_count']==gap and p['outer_path_executed_as_whole'] is False,'unreplayed calls')
    ck(r['unreplayed_intervening_calls_total']==23,'missing callbacks')
    ck(r['candidate_unverified_96_case_claim']==96 and r['R9_referenced_48_cases']==48,'do not promote private cases')
    ck(r['source_private_images']==218 and r['map_placements']==30,'observation inventory')
    ck(all(r[k] is False for k in ('original_world_entered','full_original_frame_proven','native_GPU_actor_occlusion_verified','public_proprietary_assets_included')),'unsupported promotion')
    ck((r['stage_a'],r['stage_b'],r['r79'],r['overall_completion_percent'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING',None),'stage boundary')
    ck(not any(k in r for k in ('original_exe','original_sprite_pixels','private_library_file_id','original_asset_bytes')),'private bytes leakage')
    return {'paths':4,'key_calls':20,'unreplayed_calls':23,'original_source_certification':'OPEN'}
if __name__=='__main__':print(json.dumps(validate(json.loads(REPORT.read_text()))))
