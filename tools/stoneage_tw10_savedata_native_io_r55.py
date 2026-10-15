"""Conditional historical writer/read specification; pinned metadata + invented fixtures."""
import argparse,copy,hashlib,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r53 import read_sources,validate as validate53
from tools.stoneage_tw10_savedata_writer_r54_contract import derive as contract54
from tools.stoneage_tw10_savedata_writer_r55_model import WriterModel,ModelError
from tools.stoneage_tw10_savedata_writer_r55_reference import reference
from tools.stoneage_tw10_savedata_transform_r53_model import NumericModel,seed_zero_reference,seed_zero_fixture_inverse
SCHEMA='tw10-r55-pinned-conditional-historical-writer-read-model'
R54_SHA='635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387'
R53_SHA='26bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5'
FLAGS=('actual_original_bytes_or_execution_proven','actual_abi_frame_rep_or_alias_validity_proven','actual_native_write_count_or_persistence_proven','actual_schema_checksum_migration_or_cross_version_proven','original_binary_executed','original_save_payload_evaluated','original_bytes_published')
_CACHE={}
def verify_fixtures(wrows,wedges,rrows,redges):
    ck=hashlib.sha256(json.dumps([wrows,wedges,rrows,redges],sort_keys=True).encode()).hexdigest()
    if ck in _CACHE:return copy.deepcopy(_CACHE[ck])
    covered=set();zero=set();generic=set();digest=hashlib.sha256();count=0;steps=0;max_steps=0;keys=set();capacity_cases=0
    def check(data,capacity=4000):
        nonlocal count,steps,max_steps,capacity_cases
        actual=WriterModel(data,capacity=capacity).run(wrows,wedges);want=reference(data,capacity)
        for k in ('output','output_length','mutated_input'):
            if actual[k]!=want[k]:raise ValueError('R55 independent writer mismatch '+k)
        if not want['capacity_fallback']:
            back=NumericModel(actual['output']).run(rrows,redges)
            if back['output']!=data or seed_zero_reference(actual['output'])!=data or seed_zero_fixture_inverse(data,want['key'])!=actual['output']:raise ValueError('R55 independent roundtrip')
            keys.add(want['key']);steps+=back['steps']
        else:capacity_cases+=1
        count+=1;steps+=actual['steps'];max_steps=max(max_steps,actual['steps']);covered.update(actual['site_visits']);zero.update(actual['site_visits'])
        digest.update(len(data).to_bytes(4,'little'));digest.update(capacity.to_bytes(4,'little'));digest.update(actual['output']);digest.update(actual['mutated_input'])
    for n in (1,2,3,7,127):
        for key in range(256):
            tail=bytes((i*37+key*11+7)&255 for i in range(1,n));data=bytes([(key-sum(tail))&255])+tail;check(data)
    for n in (57,255,3999):check(bytes((i*53+193)&255 for i in range(n)))
    for n,cap in ((0,0),(1,0),(16,0),(16,1),(16,15),(16,16),(16,17),(127,127),(127,128)):
        check(bytes((i*29+197)&255 for i in range(n)),cap)
    seeds=(-2147483648,-17,-7,-1,1,2,7,8,17,2147483647)
    for seed in seeds:
        data=bytes((i*53+197)&255 for i in range(16));actual=WriterModel(data,seed).run(wrows,wedges)
        if NumericModel(actual['output'],seed).run(rrows,redges)['output']!=data:raise ValueError('R55 generic fixture roundtrip')
        generic.update(actual['site_visits']);covered.update(actual['site_visits'])
    excluded={0x470a6,0x470a7,0x470aa}
    if covered|excluded!={r['site_rva'] for r in wrows} or covered&excluded or keys!=set(range(256)):raise ValueError('R55 coverage/key domain')
    result={'zero_seed_fixture_count':count,'all_key_values_lengths':[1,2,3,7,127],'additional_lengths':[57,255,3999],
      'capacity_fallback_fixture_count':capacity_cases,'generic_seed_fixture_count':len(seeds),'generic_seed_reference_formula_admitted':False,
      'zero_seed_writer_covered_rvas':sorted(zero),'generic_seed_writer_covered_rvas':sorted(generic),'union_writer_covered_instruction_count':len(covered),
      'domain_excluded_rvas':sorted(excluded),'domain_exclusion_reason':'nonnegative input-loop index below3999 makes JNS0x470a4 skip negative-index repair',
      'writer_plus_read_steps_zero_seed':steps,'maximum_zero_seed_writer_steps':max_steps,'invented_result_digest':digest.hexdigest(),
      'all_256_derived_key_values_covered':True,'zero_seed_writer_formula_mutation_and_read_roundtrip_agree':True,'original_payload_or_binary_used':False}
    _CACHE[ck]=copy.deepcopy(result);return result

def derive(raw54,raw51,raw52,raw53):
    contract=contract54(raw54)
    if len(raw53)!=104275 or hashlib.sha256(raw53).hexdigest()!=R53_SHA:raise ValueError('R55 R53 custody')
    p,_=read_sources(raw51,raw52);validate53(json.loads(raw53),raw51,raw52)
    original=json.loads(raw54);w=next(x for x in original['prefix_direct_callee_contexts'] if x['root_candidate_rva']==0x47010);rr=p['processor_instruction_shapes'];rg=p['r50_snapshot']['processing_entry_context']
    return {'schema':SCHEMA,'status':'CONDITIONAL_INVENTED_MODELS_ONLY_ACTUAL_NATIVE_PERSISTENCE_OPEN','r54_sha256':R54_SHA,'r53_sha256':R53_SHA,
      'r51_sha256':hashlib.sha256(raw51).hexdigest(),'r52_sha256':hashlib.sha256(raw52).hexdigest(),
      'metadata_and_invented_fixtures_only':True,'no_original_archive_redownload':True,
      'preconditions':{'input_count_equals_available_invented_bytes':True,'normal_domain_n':[1,3999],'capacity_domain':[0,4000],'normal_transform_requires_capacity_at_least_n_plus_one':True,
        'zero_seed_for_reference_formula':True,'disjoint_input_output_length_and_stack':True,'input_is_mutable':True,'valid_conditional_entry_slots_and_near_return':True,
        'model_limits_are_not_actual_read_write_size_proof':True,'negative_count_capacity_and_alias_outside_reference_domain':True},
      'conditional_physical_inputs':contract['physical_pushes'],'complete_writer_instruction_shapes':w['instruction_shapes'],'writer_bounded_edges':w['bounded_edges'],
      'zero_seed_relations':{'key':'K=sum(original invented input bytes) mod256, accumulated before each optional NOT',
        'input_mutation':'T[j]=input[j] XOR (255 if j mod5==0 OR j mod2==0 else0)',
        'output':'output[0]=K; output[j+1]=(T[j]+(((j+1)^2) mod7)*K) mod256',
        'output_length':'N+1 when capacity>=N+1 and N>=1','r53_roundtrip':'R53 zero-seed read(W55(input))=input under valid disjoint modeled storage',
        'capacity_fallback':'when 0<=capacity<N+1, copy input[:capacity], set length=capacity, leave input unchanged; no transform',
        'zero_count':'N=0/capacity0 returns empty fallback; N=0/capacity>=1 reaches division by zero in model',
        'not_arbitrary_inverse_key':'R53 invented inverse key must equal sum(input) mod256 to match this historical writer relation'},
      'application_candidate':{'caller_count_literal':127,'caller_capacity_literal':4000,'caller_seed_literal':0,'conditional_output_length':128,'actual_128_byte_native_write_proven':False},
      'mutable_storage_notes':{'key_local_entry_esp_offset':-1,'key_overlaps_high_byte_of_initial_ecx_push':True,'ecx_preservation_not_required':True,'output_pointer_stack_slot_overwrite_rva':0x470f5},
      'invented_fixture_verification':verify_fixtures(w['instruction_shapes'],w['bounded_edges'],rr,rg['bounded_edges']),**{k:False for k in FLAGS}}

def validate(d,*raws):
    if json.dumps(d,sort_keys=True,separators=(',',':'))!=json.dumps(derive(*raws),sort_keys=True,separators=(',',':')):raise ValueError('R55 exact replay')
    return True

def main():
    p=argparse.ArgumentParser()
    for n in ('r54','r51','r52','r53'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--verify',type=Path);a=p.parse_args();paths=[getattr(a,n) for n in ('r54','r51','r52','r53')]
    if any(p.stat().st_size>1000000 for p in paths):raise ValueError('R55 source bound')
    raws=[p.read_bytes() for p in paths]
    if a.verify:
        if a.verify.stat().st_size>1000000:raise ValueError('R55 report bound')
        validate(json.loads(a.verify.read_text()),*raws);print('TW10_R55_WRITER_READ_CONDITIONAL_MODELS=PASS; ACTUAL_SCHEMA_PERSISTENCE=OPEN')
    else:print(json.dumps(derive(*raws),sort_keys=True,indent=2))
if __name__=='__main__':main()
