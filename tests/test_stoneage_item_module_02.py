"""ITEM02: replay compact source-derived cohorts using ITEM01 public all-ID shards; no proprietary originals in CI."""
import copy, json, unittest
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parents[1]/'research'/'recovered'
NEW=R/'STONEAGE-ITEM02-ORIGINAL-NUMERIC-EQUIPMENT-AND-TW1-RD-BOUNDARY-R1.json'
OLD=R/'STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-ORIGINAL-ITEMSETS-AND-TW1-RD-SUMMARY-R1.json'
SRC=[R/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1,8)]
STATUS={'REAL_RD_DECODED_CROSS_CARRIER':2,'TW1_INDEX_NOT_FOUND':3,'TW1_RD_DECODE_FAILED':4}
def verify(n,o,sh):
 assert n['schema']=='stoneage.item02.original_numeric_cohorts_and_tw1_RD_strict_overflow.r1'
 assert n['source_sha256']['mixed25']==o['provenance']['mixed25_community_RAR_sha256']
 assert n['source_sha256']['itemset_a']==o['provenance']['itemset_a']['sha256']
 assert n['source_sha256']['itemset_b']==o['provenance']['itemset_b']['sha256']
 assert n['source_sha256']['TW1_ADRN']==o['provenance']['TW1_original_ADRN_sha256']
 assert n['source_sha256']['TW1_REAL']==o['provenance']['TW1_original_REAL_sha256']
 assert n['source_sha256']['TW1_P3H']==o['provenance']['TW1_retail_original_P3H_sha256']
 assert (n['itemset_a_rows'],n['itemset_b_rows'],n['common_ids'],n['shared_row_full_sha_equal'],n['source_b_only_ids'])==(13254,13915,13254,4303,661)
 assert n['raw_fields_per_source_row']==94
 got=defaultdict(lambda:[0,0,0,0,0]); total=equal=extra=0
 for shard in sh:
  for r in shard['rows']:
   ty=int(r[6]);a=r[1];b=r[2];v=got[ty]
   v[0]+=1;v[1]+=int(a is None);v[STATUS[r[9]]]+=1
   total+=1;equal+=int(a is not None and a==b);extra+=int(a is None)
 assert (total,equal,extra)==(13915,4303,661)
 assert len(got)==len(n['source_b_32_raw_type_rows'])==32
 seen=set()
 for row in n['source_b_32_raw_type_rows']:
  assert len(row)==7
  ty,*nums=row;assert ty not in seen;seen.add(ty)
  assert nums[:5]==got[ty]
  assert 0<=nums[5]<=nums[0]
  assert nums[0]==o['source_tables']['b']['source_rows_by_type_raw'][str(ty)]
 assert seen==set(got)
 assert n['raw_six_stats_zero_based_columns']==[37,38,39,40,41,42]
 assert sum(r[6] for r in n['source_b_32_raw_type_rows'])==n['source_b_nonzero_any_six_stats_count']==10036
 assert n['common_ids_six_stats_changed']==0 and n['common_ids_raw_column57_changed']==206
 assert [sum(r[j] for r in n['source_b_32_raw_type_rows']) for j in (3,4,5)]==[8144,5764,7]
 e=n['original_tw1_rd_strict_failed_records']
 assert [r[:2] for r in e]==[[24077,6722],[24137,6726],[24138,6727],[24140,6729]]
 assert [r[2] for r in e]==[449,481,472,511]
 assert [r[5] for r in e]==[432,464,455,494]
 assert all(len(r)==9 and len(r[7])==len(r[8])==64 and r[3]*r[4]>0 for r in e)
 assert n['strict_RLE_four_anomalies']=={'source_last_opcode':12,'source_last_run_length':2,'overrun_pixels':1,'all_source_bytes_consumed':True,'original_native_engine_handling_proven':False,'new_original_strict_decoded_pixels_from_four':0}
 assert n['other_source_attempt']['valid_original_source_bytes']==0 and n['other_source_attempt']['archive_corruption_proven'] is False
 bo=n['bounds']
 assert bo['number_of_new_original_graphic_pixels']==0
 assert all(bo[k] is False for k in ('same_historical_official_deployment_proven','raw_type_validated_official_equip_slot','real_native_shop_or_client_executed','rights_restricted_original_item_names_or_art_in_public_git'))
 assert bo['overall_percent'] is None and bo['stage_A']=='7_PARTIAL_2_OPEN' and bo['R79']=='PAUSED_NON_BLOCKING'
 return True
class TestItem02(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(NEW.read_text());cls.b=json.loads(OLD.read_text());cls.c=[json.loads(p.read_text()) for p in SRC]
 def test_all_source_rows(self):self.assertTrue(verify(self.a,self.b,self.c))
 def test_false_raw_type_count(self):
  n=copy.deepcopy(self.a);n['source_b_32_raw_type_rows'][0][1]+=1
  with self.assertRaises(AssertionError):verify(n,self.b,self.c)
 def test_no_fake_pixel_recovery(self):
  n=copy.deepcopy(self.a);n['strict_RLE_four_anomalies']['new_original_strict_decoded_pixels_from_four']=4
  with self.assertRaises(AssertionError):verify(n,self.b,self.c)
 def test_no_fake_native_shop(self):
  n=copy.deepcopy(self.a);n['bounds']['real_native_shop_or_client_executed']=True
  with self.assertRaises(AssertionError):verify(n,self.b,self.c)
 def test_no_false_same_build(self):
  n=copy.deepcopy(self.a);n['bounds']['same_historical_official_deployment_proven']=True
  with self.assertRaises(AssertionError):verify(n,self.b,self.c)
 def test_unreadable_new_ADRN_cannot_be_promoted(self):
  n=copy.deepcopy(self.a);n['other_source_attempt']['valid_original_source_bytes']=18765120
  with self.assertRaises(AssertionError):verify(n,self.b,self.c)
if __name__=='__main__':unittest.main()
