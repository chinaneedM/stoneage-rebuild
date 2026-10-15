"""R53 conditional transform specification and invented-fixture verification."""
import argparse,hashlib,json,copy
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r52_guard import validate as validate_r52
from tools.stoneage_tw10_savedata_transform_r53_model import NumericModel,seed_zero_reference,seed_zero_fixture_inverse

SCHEMA='tw10-r53-pinned-conditional-seed-zero-transform-specification'
R51_SHA256='15f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052'
R52_SHA256='99c9252bf3a982db565ab29f43d27e67b2c34978a44990564d74d75949a15179'
FLAGS=('actual_original_input_output_bytes_or_read_count_proven','actual_historical_schema_tag_migration_or_write_inverse_proven','actual_call_abi_memory_alias_or_execution_proven','native_io_executed','original_binary_executed','original_save_payload_evaluated','original_bytes_published')
BLOCKS=(('entry_and_length_store',0x47160,0x4717e),('key_selection',0x4717e,0x4718a),('count_and_pointer_dispatch',0x4718a,0x4719c),
        ('source_index_prefix_guard',0x4719c,0x471ac),('prefix_transform_generic_seed',0x471ac,0x471d3),('source_index_suffix_guard',0x471d3,0x471e3),
        ('suffix_transform',0x471e3,0x47205),('source_loop_tail',0x47205,0x4720e),('final_loop_entry',0x4720e,0x47216),
        ('final_not_predicates',0x47216,0x47251),('final_not_byte',0x47251,0x4725d),('final_loop_tail',0x4725d,0x47264),('normal_return',0x47264,0x47269))

def read_sources(raw51,raw52):
    if len(raw51)!=284533 or hashlib.sha256(raw51).hexdigest()!=R51_SHA256 or len(raw52)!=252332 or hashlib.sha256(raw52).hexdigest()!=R52_SHA256:raise ValueError('R53 pinned metadata custody')
    a,b=json.loads(raw51),json.loads(raw52);validate_r52(b,raw51);return a,b

_VERIFICATION_CACHE={}
def invented_verification(rows,edges):
    cache_key=hashlib.sha256(json.dumps([rows,edges],sort_keys=True).encode()).hexdigest()
    if cache_key in _VERIFICATION_CACHE:return copy.deepcopy(_VERIFICATION_CACHE[cache_key])
    count=0;steps=0;covered=set();outdigest=hashlib.sha256();max_steps=0
    def check(data):
        nonlocal count,steps,max_steps
        r=NumericModel(data).run(rows,edges);want=seed_zero_reference(data)
        if r['output']!=want or len(want)!=len(data)-1 or seed_zero_fixture_inverse(want,data[0])!=data:raise ValueError('R53 independent invented mismatch')
        count+=1;steps+=r['steps'];max_steps=max(max_steps,r['steps']);covered.update(r['site_visits']);outdigest.update(len(data).to_bytes(4,'little'));outdigest.update(want)
    for n in (2,3,4,8):
        for key in range(256):check(bytes([key])+bytes((i*37+key*11+7)&255 for i in range(1,n)))
    for n in (16,58,128,256,4000):check(bytes((i*53+193)&255 for i in range(n)))
    seed_zero_coverage=sorted(covered);generic=set();generic_seeds=(-2147483648,-17,-7,-1,1,2,7,8,17,2147483647)
    for seed in generic_seeds:
        r=NumericModel(bytes((i*53+197)&255 for i in range(16)),seed).run(rows,edges);generic.update(r['site_visits'])
    excluded={0x4723a,0x4723b,0x4723e}
    if (set(seed_zero_coverage)|generic|excluded)!={r['site_rva'] for r in rows} or (set(seed_zero_coverage)|generic)&excluded:raise ValueError('R53 conditional-domain instruction fixture coverage')
    result={'invented_seed_zero_fixture_count':count,'all_256_key_values_lengths':[2,3,4,8],'additional_invented_lengths':[16,58,128,256,4000],
            'seed_zero_model_steps_total':steps,'max_fixture_steps':max_steps,'seed_zero_covered_instruction_rvas':seed_zero_coverage,
            'generic_seed_fixture_count':len(generic_seeds),'generic_seed_covered_instruction_rvas':sorted(generic),
            'all_reachable_shapes_in_conditional_fixture_domain_covered':True,'domain_excluded_negative_index_fixup_rvas':sorted(excluded),
            'excluded_domain_reason':'j is nonnegative and below4000, so AND j,0x80000001 has clear sign and JNS0x47238 bypasses negative-index fixup','invented_output_digest':outdigest.hexdigest(),
            'nonzero_seed_reference_formula_admitted':False,'original_binary_or_save_payload_used':False}
    _VERIFICATION_CACHE[cache_key]=copy.deepcopy(result)
    return result

def derive(raw51,raw52):
    p,prior=read_sources(raw51,raw52);rows=p['processor_instruction_shapes'];g=p['r50_snapshot']['processing_entry_context'];c=p['r50_snapshot']['caller_context'];by={r['site_rva']:r for r in rows}
    blocks=[{'name':name,'lo_rva':lo,'hi_exclusive_rva':hi,'instruction_shapes':[r for r in rows if lo<=r['site_rva']<hi]} for name,lo,hi in BLOCKS]
    if [r['site_rva'] for b in blocks for r in b['instruction_shapes']]!=g['bounded_node_rvas']:raise ValueError('R53 full block partition')
    seed_push=c['processing_call_context']['physical_push_suffix']['pushes'][2]
    if seed_push['conditional_pre_call_esp_offset']!=8 or seed_push['input'].get('constant')!=0:raise ValueError('R53 caller seed shape')
    return {'schema':SCHEMA,'status':'CONDITIONAL_METADATA_AND_INVENTED_FIXTURE_MODEL_ONLY','r51_sha256':R51_SHA256,'r52_sha256':R52_SHA256,
            'no_original_archive_redownload':True,'metadata_and_invented_fixtures_only':True,
            'preconditions':{'caller_seed_literal':0,'invented_input_length_domain':[2,4000],
                'domain_4000_is_model_bound_not_actual_read_size_proof':True,'signed_32bit_scalar_and_8bit_byte_operations':True,
                'source_destination_length_pointer_and_stack_regions_disjoint':True,'source_count_equals_available_input_bytes':True,
                'entry_slots_and_near_call_normal_return_follow_r51_conditional_geometry':True,
                'no_alias_overwrite_of_seed_count_output_pointer_or_length_cell':True,
                'invalid_count_divide_error_overflow_and_alias_cases_excluded_from_reference':True},
            'caller_seed_push_observation':seed_push,'instruction_block_partition':blocks,
            'seed_zero_symbolic_relations':{
                'length_cell_store':'L = N - 1; requires N > 1 and disjoint valid length cell',
                'key_index':'abs(signed_remainder(0, L)) = 0','key_byte':'K = input[0]',
                'omitted_input_index':0,'source_to_output_index':'i = j + 1, 0 <= j < L',
                'byte_before_optional_not':'B[j] = (input[j+1] - (((j+1)*(j+1)) mod 7)*K) mod 256',
                'not_predicate':'(j mod 5 == 0) OR (j mod 2 == 0)',
                'output_byte':'output[j] = B[j] XOR (255 if not_predicate else 0)',
                'prefix_divisor3_path_unreachable_only_under_seed_zero_valid_domain':True,
                'fixture_inverse_is_not_a_historical_savedata_write_path':True},
            'generic_seed_paths_retained':{'key_selector':'abs(signed_remainder(seed, N-1))',
                'source_index_less_than_selector_divisor':3,'source_index_greater_than_selector_divisor':7,
                'final_conditions':'signed_remainder(seed,7)==signed_remainder(j,5) OR signed_remainder(seed,2)==signed_remainder(j,2)',
                'generic_reference_formula_admitted':False},
            'application_conditional_equations':[{'compare_site_rva':0x40195,'output_length_literal':57,'model_input_length_if_L_equals_N_minus_one':58,'actual_historical_record_length_proven':False},
                {'compare_site_rva':0x401c9,'output_length_literal':127,'model_input_length_if_L_equals_N_minus_one':128,'actual_historical_record_length_proven':False}],
            'application_word_compare_and_byte_write_shapes':[r for r in c['literal_effect_input_shapes'] if r['site_rva'] in (0x40195,0x4019f,0x401a8,0x401af,0x401c9,0x401e4)],
            'invented_fixture_verification':invented_verification(rows,g['bounded_edges']),**{k:False for k in FLAGS}}

def validate(report,raw51,raw52):
    if json.dumps(report,sort_keys=True,separators=(',',':'))!=json.dumps(derive(raw51,raw52),sort_keys=True,separators=(',',':')):raise ValueError('R53 exact specification replay differs')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--r51',type=Path,required=True);p.add_argument('--r52',type=Path,required=True);p.add_argument('--verify',type=Path);a=p.parse_args()
    if a.r51.stat().st_size>1000000 or a.r52.stat().st_size>2000000:raise ValueError('source bound')
    if a.verify:
        if a.verify.stat().st_size>1000000:raise ValueError('report bound')
        validate(json.loads(a.verify.read_text()),a.r51.read_bytes(),a.r52.read_bytes());print('TW10_R53_CONDITIONAL_SPEC_AND_INVENTED_MODELS=PASS; ACTUAL_SAVE_SCHEMA=OPEN')
    else:print(json.dumps(derive(a.r51.read_bytes(),a.r52.read_bytes()),sort_keys=True,indent=2))
if __name__=='__main__':main()
