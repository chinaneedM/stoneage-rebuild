"""CHAR04 source-derived NPC/SRP ID association, with explicit non-identity gates."""
import collections
import copy
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1] / 'research' / 'recovered'

def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def replay(o, s, p, r40):
    assert o['schema']=='stoneage.character_npc_module_04_source_graphic_template_function_vs_SPR_numeric_join.r1'
    assert o['original_private_RAR_sha256']==s['original_rar_sha256']==p['preserved_original_rar']['sha256']
    assert len(s['source_files'])==2205
    assert len(s['create_rows'])==len(o['create_source_rows'])==4985
    assert len(s['template_rows'])==len(o['original_template_type_numeric_receipts'])==119
    spr=collections.defaultdict(list)
    for ix,key,off,n,reserved in p['source_rows']['spradrn_5.bin']:
        spr[key].append(ix)
    assert len(p['source_rows']['spradrn_5.bin'])==847
    template={(r[0],r[1]):r for r in s['template_rows']}
    ttypes={(r[0],r[1]):r[2] for r in o['original_template_type_numeric_receipts']}
    assert set(template)==set(ttypes)
    metrics=collections.Counter()
    roles=collections.Counter()
    yes=collections.Counter()
    no=collections.Counter()
    mismatch=[]
    selected=[]
    for prior,row in zip(s['create_rows'],o['create_source_rows']):
        path,index,role,gfx,indices=row
        assert (path,index,gfx)==(prior[0],prior[1],prior[6])
        assert indices==(spr.get(gfx,[]) if gfx is not None else [])
        matches=prior[13]
        if len(matches)==1:
            k=tuple(matches[0]);assert role==template[k][4]
        else:
            assert role=='AMBIGUOUS_OR_MISSING';k=None
        roles[role]+=1
        metrics['create_blocks']+=1
        metrics['has_numeric_graphic']+=gfx is not None
        metrics['no_numeric_graphic']+=gfx is None
        metrics['indexed_create_occurrences']+=bool(indices)
        metrics['unindexed_numeric_create_occurrences']+=gfx is not None and not indices
        metrics['source_templates_resolved']+=k is not None
        if gfx is not None:
            (yes if indices else no)[gfx]+=1
        ty=ttypes.get(k) if k else None
        if gfx is not None and ty is not None:
            metrics['both_independent_numeric_create_graphic_and_template_type']+=1
            if gfx!=ty:mismatch.append([path,index,gfx,k[0],k[1],ty,role])
        if gfx in (100250,100251,100252):selected.append([path,index,role,gfx])
    metrics.update({
        'distinct_indexed_numeric_graphic_ids':len(yes),
        'distinct_unindexed_numeric_graphic_ids':len(no),
        'numeric_template_type_mismatches':len(mismatch),
        'numeric_template_type_exact_matches':metrics['both_independent_numeric_create_graphic_and_template_type']-len(mismatch),
        'source_original_SPR_index_occurrences':len(p['source_rows']['spradrn_5.bin']),
        'original_NPC_config_files':189,
        'original_NPC_subtree_files_verified':2205,
        'original_NPC_template_blocks_verified':119,
        'source_file_ref_occurrences':s['counts']['source_file_reference_occurrences'],
        'source_file_ref_resolved_exact_subtree':s['counts']['reference_exact_subtree_target_present'],
        'source_file_ref_unresolved_subtree':s['counts']['reference_exact_subtree_target_missing']})
    assert dict(metrics)==o['counts']
    assert dict(roles)==o['functionset_source_occurrences']
    assert metrics['indexed_create_occurrences']==617
    assert metrics['no_numeric_graphic']==2503
    assert metrics['numeric_template_type_mismatches']==35
    assert metrics['source_templates_resolved']==4984
    assert roles['Warp']==2904
    assert [[g,spr[g],n] for g,n in sorted(yes.items())]==o['indexed_graphic_source_summary']
    assert [[g,n] for g,n in sorted(no.items())]==o['nonindexed_numeric_graphic_counts']
    assert mismatch==o['distinct_original_source_type_conflicts']
    assert selected==o['prior_R40_full_SPR_segment_source_create_refs']
    assert len(selected)==30 and {a[3] for a in selected}=={100250,100251,100252}
    assert o['already_prior_R40_full_SPR_segment_graphic_numbers_only']==[100250,100251,100252]
    assert r40['source_scope']=='MIXED25_PRESERVED_SAME_ARCHIVE_CLIENT_SERVER_SUBTREES_NOT_SAME_DEPLOYED_BUILD_OR_OFFICIAL_RELEASE'
    assert r40['source_index_rows']==847
    assert o['bounds']['total_restoration_percent'] is None
    assert all(v is False for k,v in o['bounds'].items() if k!='total_restoration_percent')

class CharacterNPC04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=load('STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json')
        cls.source=load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')
        cls.pet=load('STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json')
        cls.r40=load('STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json')
    def go(self,r):replay(r,self.source,self.pet,self.r40)
    def test_entire_4985_original_create_source_join(self):self.go(self.out)
    def test_false_historical_identity_rejected(self):
        o=copy.deepcopy(self.out);o['bounds']['matching_numeric_graphic_ids_prove_historical_NPC_identity']=True
        with self.assertRaises(AssertionError):self.go(o)
    def test_false_original_pixel_claim_rejected(self):
        o=copy.deepcopy(self.out);o['bounds']['indexed_SPR_group_is_rendered_original_pixels_in_this_run']=True
        with self.assertRaises(AssertionError):self.go(o)
    def test_false_template_type_substitution_rejected(self):
        o=copy.deepcopy(self.out);next(x for x in o['create_source_rows'] if x[3] is not None)[3]+=1
        with self.assertRaises(AssertionError):self.go(o)
    def test_mismatching_numeric_templates_cannot_be_erased(self):
        o=copy.deepcopy(self.out);o['distinct_original_source_type_conflicts'].pop()
        with self.assertRaises(AssertionError):self.go(o)
    def test_warps_cannot_be_called_characters(self):
        o=copy.deepcopy(self.out);next(x for x in o['create_source_rows'] if x[2]=='Warp')[2]='TownPeople'
        with self.assertRaises(AssertionError):self.go(o)
if __name__=='__main__': unittest.main()
