"""Pinned conditional caller-frame/output/write-request specification; invented only."""
import argparse,copy,hashlib,json
from pathlib import Path
from tools.stoneage_tw10_savedata_frame_r56_model import helper,caller,S
R54_SHA='635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387'
R55_SHA='9f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863'
FLAGS=('actual_helper_allocation_or_rep_values_proven','actual_opaque_call_preservation_or_native_return_semantics_proven','actual_native_write_flush_close_or_persistence_proven','actual_payload_schema_migration_checksum_or_server_authority_proven','original_binary_executed','original_save_payload_evaluated','original_bytes_published')
SCHEMA='tw10-r56-pinned-conditional-application-frame-write-request'

def conditions(helper_valid=None,direction=None,flat_segments=None,opaque_stack_preserved=None,opaque_memory_preserved=None):
    frame=helper_valid is True;copied=frame and type(direction) is int and direction==0 and flat_segments is True
    post=frame and opaque_stack_preserved is True;bound=copied and post and opaque_memory_preserved is True
    return {'assumptions':{'helper_reads_addresses_and_near_return_valid':helper_valid,'direction_flag':direction,'flat_compatible_segments':flat_segments,'opaque_calls_preserve_stack_geometry':opaque_stack_preserved,'opaque_calls_preserve_length_output_and_saved_stack_memory':opaque_memory_preserved},
      'prefix_frame_geometry_qualified':frame,'snapshot_copy_qualified':copied,'post_open_geometry_qualified':post,'output_content_and_count_binding_qualified':bound,
      'conditional_length_cell_relative_entry_esp':-4132 if frame else None,'conditional_output_relative_entry_esp':-4000 if frame else None,
      'conditional_write_request_count':128 if bound else None,'actual_original_conditions_or_persistence_proven':False}

_CACHE={}
def fixtures(c,h,w):
    key=hashlib.sha256(json.dumps([c,h,w],sort_keys=True).encode()).hexdigest()
    if key in _CACHE:return copy.deepcopy(_CACHE[key])
    amounts=sorted(set(range(257))|{k*4096+d for k in range(1,16) for d in (-1,0,1)}|{4132,65535,65536})
    hc=set();cc=set();digest=hashlib.sha256();helpersteps=0
    for n in amounts:
        r=helper(h['instruction_shapes'],h['bounded_edges'],n);expected=[-4096*k for k in range(1,n//4096+1)]+[-n]
        if r['caller_esp']!=S-n or [a-S for a in r['probe_addresses']]!=expected:raise ValueError('R56 independent helper relation')
        hc.update(r['site_visits']);helpersteps+=r['steps'];digest.update(json.dumps([n,r['caller_esp']-S,expected]).encode())
    witness=None
    for keybyte in range(256):
        tail=bytes((i*37+keybyte*11+7)&255 for i in range(1,127));data=bytes([(keybyte-sum(tail))&255])+tail
        r=caller(c,h,w,data);cc.update(r['caller_site_visits']);t=r['transform'];slots=r['request_slots']
        if slots[:3]!=[S-4000,1,128] or t['length_cell']!=S-4132 or r['request_bytes']!=t['output'] or t['output'][0]!=keybyte or r['return_value']!=1 or not r['close_stub_seen']:raise ValueError('R56 invented writer request binding')
        digest.update(r['request_bytes'])
        if keybyte==0:witness=r
    cases=[]
    for op,wr,cl in ((0,128,0),(1,0,0),(1,127,0),(1,128,0),(1,129,0),(1,0x80000000,0),(1,0xffffffff,0xffffffff)):
        r=caller(c,h,w,bytes(range(127)),op,wr,cl);cc.update(r['caller_site_visits']);expected=bool(op and wr>=128)
        if r['return_value']!=int(expected) or r['close_stub_seen'] is not expected or (r['request_slots'] is None)!=(op==0):raise ValueError('R56 invented return path')
        cases.append({'invented_open_return':op,'invented_write_return_u32':wr,'invented_close_return':cl,'caller_literal_return':r['return_value'],'close_stub_seen':r['close_stub_seen'],'executed_caller_rvas':sorted(r['caller_site_visits'])})
    normal=caller(c,h,w,bytes(range(127)));changed_count=caller(c,h,w,bytes(range(127)),length_clobber=127);changed_output=caller(c,h,w,bytes(range(127)),output_clobber=True)
    if changed_count['request_slots'][2]!=127 or changed_output['request_bytes']==normal['request_bytes']:raise ValueError('R56 opaque-memory counterexamples')
    if hc!=set(h['bounded_node_rvas']) or cc!=set(c['bounded_node_rvas']):raise ValueError('R56 bounded fixture coverage')
    coords=witness['entry_relative_stack_before_sites'];sites=(0x4005a,0x40069,0x40080,0x40090,0x40095)
    out={'helper_fixture_count':len(amounts),'helper_amounts':amounts,'helper_steps':helpersteps,'helper_covered_rvas':sorted(hc),'caller_success_key_fixtures':256,'caller_return_path_fixtures':cases,
      'caller_covered_rvas':sorted(cc),'caller_all55_shapes_covered_in_invented_paths':True,'helper_all17_shapes_covered_in_invented_paths':True,
      'witness_preinstruction_esp_relative_entry':[{'site_rva':a,'esp_delta':coords[a]} for a in sites],
      'write_request_physical_slots':[{'offset':0,'conditional_pointer_relative_entry':-4000},{'offset':4,'literal':1},{'offset':8,'conditional_count':128},{'offset':12,'opaque_open_return_shape':True}],
      'opaque_memory_counterexamples':{'open_stub_length_cell_overwrite_changes_request_count_to':changed_count['request_slots'][2],'open_stub_output_overwrite_changes_request_bytes':True,'geometry_alone_does_not_bind_contents_or_count':True},
      'invented_digest':digest.hexdigest(),'original_native_io_or_payload_used':False}
    _CACHE[key]=copy.deepcopy(out);return out

def derive(raw54,raw55):
    if len(raw54)!=132329 or hashlib.sha256(raw54).hexdigest()!=R54_SHA or len(raw55)!=103165 or hashlib.sha256(raw55).hexdigest()!=R55_SHA:raise ValueError('R56 pinned source custody')
    d,p=json.loads(raw54),json.loads(raw55);c=d['writer_context'];h=next(x for x in d['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x49160);w=next(x for x in d['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x47010)
    if p['application_candidate']['conditional_output_length']!=128 or c['graph']['frontier'] or h['graph']['frontier']:raise ValueError('R56 prerequisite')
    return {'schema':SCHEMA,'status':'CONDITIONAL_INVENTED_FRAME_AND_WRITE_REQUEST_ONLY','r54_sha256':R54_SHA,'r55_sha256':R55_SHA,'no_original_archive_redownload':True,
      'complete_helper_instruction_shapes':h['instruction_shapes'],'helper_bounded_edges':h['bounded_edges'],'complete_caller_instruction_shapes':c['instruction_shapes'],'caller_bounded_edges':c['bounded_edges'],
      'helper_relation':{'invented_request_domain':[0,65536],'caller_pre_call_esp_symbol':'S','conditional_continuation_esp':'S - requested amount','actual_caller_literal':4132,'conditional_actual_literal_delta':-4132,
        'probe_offset_relation':'[-4096*k for k=1..floor(amount/4096)] followed by [-amount], including duplicate final exact-page address',
        'return_marker_relocated_and_ecx_restored_only_on_valid_invented_storage':True,'real_memory_probe_success_or_allocation_proven':False},
      'binding_with_missing_conditions':conditions(),'binding_under_explicit_model_conditions':conditions(True,0,True,True,True),
      'binding_with_unknown_opaque_memory':conditions(True,0,True,True,None),'binding_with_unknown_opaque_stack':conditions(True,0,True,None,True),
      'conditional_storage_intervals_relative_S':[{'role':'length_cell','lo':-4132,'hi_exclusive':-4128},{'role':'snapshot127','lo':-4128,'hi_exclusive':-4001},{'role':'padding','lo':-4001,'hi_exclusive':-4000},{'role':'output_capacity4000','lo':-4000,'hi_exclusive':0}],
      'copy_preconditions':['clear direction flag','compatible flat source and ES destination segments','valid initialized127 invented source bytes','valid disjoint input/output/count/saved-stack storage'],
      'opaque_call_model':['explicit stubs only at open0x40069/write0x40090/close0x400ac','stubs preserve ESP and saved stack memory','open/write stubs preserve live count cell and output unless counterexample injection','invented return values have no historical error/ABI semantics'],
      'return_control_only':{'write_compare_rva':0x4009c,'unsigned_jae_rva':0x4009e,'close_candidate_call_rva':0x400ac,'close_result_overwritten_by_literal1_rva':0x400b4,'short_write_path_has_no_close_candidate_in_this_bounded_graph':True,'actual_resource_leak_or_error_convention_proven':False},
      'invented_verification':fixtures(c,h,w),**{k:False for k in FLAGS}}

def validate(d,raw54,raw55):
    if json.dumps(d,sort_keys=True,separators=(',',':'))!=json.dumps(derive(raw54,raw55),sort_keys=True,separators=(',',':')):raise ValueError('R56 exact replay')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--r54',type=Path,required=True);p.add_argument('--r55',type=Path,required=True);p.add_argument('--verify',type=Path);a=p.parse_args()
    if a.r54.stat().st_size>1000000 or a.r55.stat().st_size>1000000:raise ValueError('R56 source bound')
    raw54,raw55=a.r54.read_bytes(),a.r55.read_bytes()
    if a.verify:
        if a.verify.stat().st_size>1000000:raise ValueError('R56 report bound')
        validate(json.loads(a.verify.read_text()),raw54,raw55);print('TW10_R56_CONDITIONAL_FRAME_WRITE_REQUEST=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')
    else:print(json.dumps(derive(raw54,raw55),sort_keys=True,indent=2))
if __name__=='__main__':main()
