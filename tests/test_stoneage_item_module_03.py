"""ITEM03 static-source archival checks; CI never reads private copyrighted files."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

REC=Path(__file__).resolve().parents[1]/'research'/'recovered'
REPORT=REC/'STONEAGE-ITEM-MODULE-03-ORIGINAL-COMPOSITION-AND-EXCHANGE-SOURCE-CATALOG-R1.json'
SHARDS=[REC/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1,8)]

def digest(rows):
    return hashlib.sha256(json.dumps(rows,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def verify(m, shards):
    assert m['schema']=='stoneage.item03_source_bound_composition_exchanges_lottery.r1'
    assert m['source_community_mixed25_RAR_SHA256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
    files=m['source_members']
    assert len(files)==7
    assert files['itemset.txt']['source_bytes']==3392473
    assert files['itemset0710.txt']['source_bytes']==3668487
    assert files['itematom.txt']['physical_source_rows']==83
    assert files['bmitem.txt']['physical_source_rows']==36
    assert files['gambleitems.txt']['physical_source_rows']==24
    assert files['magic.txt']['physical_source_rows']==181
    assert files['cook.conf']['physical_source_rows']==165
    assert all(len(x['sha256'])==64 and len(x['archive_member_crc32_hex'])==8 for x in files.values())
    assert m['source_main_itemset_physical_rows']=={'A':13254,'B':13915}
    assert m['raw_hash_prefixed_IDs']=={'A':[13031,19549],'B':[1874,1875,1876,13031,19549],'B_only':[1874,1875,1876]}
    assert m['raw_unprefixed_rows_not_native_active_count']=={'A':13252,'B':13910}
    assert (m['common_ids'],m['later_table_only_ids'],m['later_only_hash_prefixed_ids'])==(13254,661,3)
    assert m['shared_ids_unchanged_composition_fields_zero_based_84_to_93']==13254
    assert m['source_ten_tail_columns_raw_names']==[e for i in range(5) for e in ('ingname'+str(i),'ingvalue'+str(i))]
    for key,rows in [('atom',m['atom_rows_in_original_source_order']),('bm',m['bm_rows_in_original_source_order']),('lot',m['gamble_rows_in_original_source_order'])]:
        fld={'atom':'atom_numeric_rows_json_sha256','bm':'bm_numeric_rows_json_sha256','lot':'gamble_numeric_rows_json_sha256'}[key]
        assert digest(rows)==m[fld]
    atoms=m['atom_rows_in_original_source_order']
    assert len(atoms)==83
    assert len({r[1] for r in atoms})==83
    assert Counter(r[0] for r in atoms)=={0:72,1:11}
    assert sum(r[2] for r in atoms)==43622 and sum(r[3] for r in atoms)==44806
    assert sum(r[2]>0 for r in atoms)==78 and sum(r[3]>0 for r in atoms)==83
    assert all(r[2]<=r[3] for r in atoms)
    assert m['slot_presence_A']=={'total':13254,'named':43622,'empty_both':13647,'unnamed_value':9001,'unnamed_nonzero':1,'hash_prefix':2}
    assert m['slot_presence_B']=={'total':13915,'named':44806,'empty_both':14708,'unnamed_value':10061,'hash_prefix':5,'unnamed_nonzero':1}
    assert all(sum(m['slot_presence_'+c][k] for k in ('named','empty_both','unnamed_value'))==m['slot_presence_'+c]['total']*5 for c in ('A','B'))
    ids=set();old_ids=set()
    for sh in shards:
        for row in sh['rows']:
            ids.add(row[0])
            if row[1] is not None:old_ids.add(row[0])
    assert len(ids)==13915 and len(old_ids)==13254
    assert len(ids-old_ids)==661
    assert set(m['raw_hash_prefixed_IDs']['B_only']).issubset(ids-old_ids)
    bm=m['bm_rows_in_original_source_order']
    assert len(bm)==36 and bm[:12]==bm[12:24]==bm[24:]
    assert Counter(x[0] for x in bm)=={10000:6,20000:18,30000:12}
    assert sum(bool(x[1]) for x in bm)==30
    assert sum(len(x[1]) for x in bm)==45
    bmids={q for x in bm for q in x[1]}
    assert len(bmids)==13 and bmids<=old_ids
    lot=m['gamble_rows_in_original_source_order']
    assert len(lot)==24
    assert Counter(x[3] for x in lot)=={None:20,'NEXT':3,'END':1}
    assert all(x[0] in old_ids for x in lot)
    assert all(x[:3]==[0,0,0] for x in lot if x[3] is not None)
    assert len({x[0] for x in lot if x[3] is None})==20
    assert m['original_source_crc_and_SHA_rechecked'] is True
    assert all(v is False for k,v in m['not_claimed'].items() if k!='overall_completion_percentage')
    assert m['not_claimed']['overall_completion_percentage'] is None
    assert m['phase']=='STAGE_A_SOURCE_BOUNDED_PARTIAL'
    assert m['stage_A']=='7_PARTIAL_2_OPEN' and m['stage_B_and_wiki']=='GATED' and m['R79']=='PAUSED_NON_BLOCKING'
    assert m['next'].startswith('QUEST_STORY_MODULE_01')
    return True

class Item03SourceSafetyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads(REPORT.read_text('utf-8'))
        cls.shards=[json.loads(p.read_text('utf-8')) for p in SHARDS]
    def test_all_83_atoms_36_exchanges_24_lottery_source_rows(self): self.assertTrue(verify(self.m,self.shards))
    def test_tampered_atom_frequency_rejected(self):
        m=deepcopy(self.m);m['atom_rows_in_original_source_order'][0][3]+=1
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_tampered_exchange_item_rejected(self):
        m=deepcopy(self.m);m['bm_rows_in_original_source_order'][0][1].append(0)
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_tampered_lottery_end_rejected(self):
        m=deepcopy(self.m);m['gamble_rows_in_original_source_order'][-1][3]='NEXT'
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_original_game_execution_not_faked(self):
        m=deepcopy(self.m);m['not_claimed']['original_client_or_server_executed']=True
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_hash_prefixed_rows_not_falsely_proven_active(self):
        m=deepcopy(self.m);m['not_claimed']['source_raw_hash_prefix_proven_parser_exclusion']=True
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_original_official_deployment_not_faked(self):
        m=deepcopy(self.m);m['not_claimed']['source_clean_official_deployed_server']=True
        with self.assertRaises(AssertionError):verify(m,self.shards)
    def test_later_only_hash_prefixed_IDs_conserved(self):
        m=deepcopy(self.m);m['raw_hash_prefixed_IDs']['B_only']=[1874,1875]
        with self.assertRaises(AssertionError):verify(m,self.shards)

if __name__=='__main__': unittest.main()
