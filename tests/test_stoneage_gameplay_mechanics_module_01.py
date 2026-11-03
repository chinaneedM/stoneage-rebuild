"""Public metadata-only tests; original proprietary NPC source bytes are never in GitHub Actions."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]/'research'/'recovered'
EVIDENCE=ROOT/'STONEAGE-GAMEPLAY01-ORIGINAL-FAMILY-ARENA-PET-REBIRTH-R1.json'
SOURCE=ROOT/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')
def verify(d,c):
    assert d['schema']=='stoneage.gameplay_mechanics_module01_original_family_arena_rebirth_source_graph.r1'
    s=d['source'];assert s['all_2205_source_NPC_files_replayed'] is True and s['all_original_NPC_bytes_replayed']==1930332
    assert s['upstream_parent_RAR_not_reopened_this_unit'] is True and HEX.fullmatch(s['private_original_NPC_ZIP_SHA256'])
    ref=d['source_CREATE_references'];files=d['source_parameter_files'];r=d['summary']
    assert len(ref)==37 and len(files)==33
    assert (r['family_source_CREATE_references_total'],r['original_parameter_file_references'],r['rider_create_refs_without_file'])==(37,33,4)
    originalrows={(r[0],r[1]):r for r in c['create_rows']}
    originalfiles={f[0]:f for f in c['source_files']}
    src={}
    for f in files:
        p=f['source_path'];assert p not in src and p in originalfiles
        assert (f['original_bytes'],f['original_sha256'],f['original_crc32'])==tuple(originalfiles[p][1:4]);assert HEX.fullmatch(f['original_sha256'])
        assert f['origin_class']=='ORIGIN_UNRESOLVED';src[p]=f
    count=Counter();family=Counter()
    for row in ref:
        o=originalrows[(row['create_source_path'],row['create_ordinal'])]
        assert row['family']==o[11] and row['create_block_sha256']==o[4]
        assert row['source_floorid']==o[5] and row['source_graphicnum']==o[6]
        assert row['origin_class']=='ORIGIN_UNRESOLVED';family[row['family']]+=1
        p=row['original_source_file']
        if p is None:
            assert row['family']=='riderman' and not o[15] and row['source_file_sha256'] is None
        else:
            assert o[15]==[[p,'EXACT_SAME_NPC_SUBTREE_PATH',row['source_file_sha256']]]
            assert src[p]['original_sha256']==row['source_file_sha256'];count[p]+=1
    assert all(f['create_refs']==count[f['source_path']] for f in files)
    assert r['family_CREATE_counts']==dict(sorted(family.items()))
    assert family==Counter({'npcgen_fmwarpman':9,'npcgen_fmpkman':9,'npcgen_fmpkcallman':5,'scheduleman':5,'manorsman':4,'npc_transmigration':1,'riderman':4})
    assert r['original_33_parameter_file_bytes']==sum(f['original_bytes'] for f in files)==14611
    assert r['arena_id_exact_both_source_families']==[1,2,3,4,11,12,13,14,15]
    assert r['five_schedule_ids']==[11,12,13,14,15] and r['four_manor_ids']==[1,2,3,4]
    byfam=lambda fam:[f for f in files if f['family']==fam]
    fm={f['arena_id']:f for f in byfam('npcgen_fmwarpman')};pk={f['arena_id']:f for f in byfam('npcgen_fmpkman')}
    assert set(fm)==set(pk)==set(r['arena_id_exact_both_source_families'])
    getfloor={x['original_source_file']:x['source_floorid'] for x in ref if x['original_source_file']}
    for i in fm:
        assert fm[i]['arena_entry_candidate_1'][0]==fm[i]['arena_entry_candidate_2'][0]==getfloor[pk[i]['source_path']]
        assert pk[i]['arena_exit_candidate'][0]==getfloor[fm[i]['source_path']]
    assert all(f['call_member_warp_candidate'][0]==getfloor[f['source_path']] for f in byfam('npcgen_fmpkcallman'))
    assert {f['arena_id'] for f in byfam('scheduleman')}=={11,12,13,14,15}
    assert {f['arena_id'] for f in byfam('manorsman')}=={1,2,3,4}
    for f in byfam('scheduleman'):
        assert f['source_numeric_params']=={'loopinterval':1000,'challengetimeout':1200,'settingtimeout':60,'fightinterval':60}
    for f in byfam('manorsman'):
        assert f['source_numeric_params']['challengewait']==86400 and f['source_numeric_params']['peacewait']==172800
        assert f['source_numeric_params']['manorid']==f['arena_id']
    t=byfam('npc_transmigration');assert len(t)==1
    assert t[0]['original_TENSEI_stage_numbers']==[1,2,3,4,5,6]
    assert len(t[0]['regional_source_parameters'])==4
    assert t[0]['original_dialogue_contains_second_rebirth_no_mount_warning'] is True
    assert t[0]['actual_mount_state_change_executed'] is False
    bounds=d['limits'];assert bounds['not_official_TW10_CN182_JSS1999_same_build'] is True
    assert bounds['original_transmigration_or_riding_execution_seen'] is False
    assert bounds['original_fmPK_server_routing_or_victory_seen'] is False
    assert bounds['original_clock_units_and_timeouts_runtime_verified'] is False
    assert bounds['private_commercial_dialogue_or_art_in_public_git'] is False
    assert bounds['stage_A']=='7_PARTIAL_2_OPEN' and bounds['overall_percent'] is None
    assert d['next'].startswith('GAMEPLAY-MECHANICS-MODULE-02')
    return True
class TestGameplay01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(EVIDENCE.read_text('utf-8'));cls.c=json.loads(SOURCE.read_text('utf-8'))
    def test_all_original_source_sha_and_arena_id_joins(self):self.assertTrue(verify(self.d,self.c))
    def reject(self,change):
        d=deepcopy(self.d);change(d)
        with self.assertRaises((AssertionError,KeyError,StopIteration)):verify(d,self.c)
    def test_arena_false_warp_rejected(self):self.reject(lambda d:next(x for x in d['source_parameter_files'] if x['family']=='npcgen_fmwarpman')['arena_entry_candidate_1'].__setitem__(0,999999))
    def test_false_rider_source_rejected(self):self.reject(lambda d:next(x for x in d['source_CREATE_references'] if x['family']=='riderman').__setitem__('original_source_file','fake.arg'))
    def test_wrong_schedule_id_rejected(self):self.reject(lambda d:next(x for x in d['source_parameter_files'] if x['family']=='scheduleman').__setitem__('arena_id',999))
    def test_wrong_manor_wait_rejected(self):self.reject(lambda d:next(x for x in d['source_parameter_files'] if x['family']=='manorsman')['source_numeric_params'].__setitem__('challengewait',1))
    def test_fake_mount_execution_rejected(self):self.reject(lambda d:d['limits'].__setitem__('original_transmigration_or_riding_execution_seen',True))
    def test_unproven_clock_unit_rejected(self):self.reject(lambda d:d['limits'].__setitem__('original_clock_units_and_timeouts_runtime_verified',True))
    def test_original_pet_stage_fabrication_rejected(self):self.reject(lambda d:next(x for x in d['source_parameter_files'] if x['family']=='npc_transmigration').__setitem__('original_TENSEI_stage_numbers',[1,2,3,4,5,6,7]))
    def test_proprietary_source_publication_rejected(self):self.reject(lambda d:d['limits'].__setitem__('private_commercial_dialogue_or_art_in_public_git',True))
if __name__=='__main__':unittest.main()
