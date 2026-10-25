import copy
import gzip
import json
from pathlib import Path
import tempfile
import unittest
from tools import stoneage_logical_alias_catalog as m


def ref(index=1,alias=26301,profile='PATCH129',digest='a'*64):
 return {'profile':profile,'logical_alias':alias,'source_index':index,'physical_bitmapno':376000+index,
  'adrn_offset':100*index,'adrn_size':20,'xoff':-1,'yoff':-2,'width':2,'height':2,
  'attr_sha256':'b'*64,'record_sha256':'c'*64,'source_rd_status':'HEADER_MATCH',
  'catalog_rd_qualification':'MATCHING_RD_HEADER','physical_record_multiplicity':1,
  'alias_evidence':'ORIGINAL_COMPLETE_OCCURRENCE_TABLE','alias_witness_patch_index':-1,
  '_rd':{'rd_sha256':digest,'bytes':20,'rd_flag':0,'rd_width':2,'rd_height':2,'rd_size_field':20}}


def patch_fixture(raw=False):
 h={k:str(v) for k,v in {'index':1,'bitmapno':376001,'adder':100,'size':20,'xoff':-1,'yoff':-2,
       'width':2,'height':2,'map_number':26301,'record_sha256':'c'*64,'attr_sha256':'b'*64}.items()}
 n={k:v for k,v in h.items() if k!='map_number'}
 n.update(index='10',rd_sha256='a'*64,rd_flag='0',rd_width='2',rd_height='2',
          rd_size=str(20+8621844 if raw else 20),rd_status='HEADER_MISMATCH' if raw else 'HEADER_MATCH')
 p={'patch_index':'1','bitmapno':'376001','patch_record_sha256':'c'*64,'native_exact_indices':'10',
    'rd_sha256':'a'*64,'rd_status':n['rd_status'],
    'qualification':'RD_STRUCTURE_NOT_QUALIFIED' if raw else 'EXACT_NATIVE_RECORD_AND_RD_STRUCTURE'}
 return h,n,p


class Catalog(unittest.TestCase):
 def test_content_reuse_preserves_both_source_occurrences(self):
  refs,blocks=m.normalize([ref(),ref(2)])
  self.assertEqual(len(refs),2);self.assertEqual(len(blocks),1)
  self.assertEqual(blocks[0]['reference_count'],2)
  self.assertEqual([r['source_index'] for r in refs],[1,2])

 def test_same_alias_different_content_does_not_choose_last(self):
  refs,blocks=m.normalize([ref(),ref(2,digest='d'*64)])
  self.assertEqual(len(refs),2);self.assertEqual(len(blocks),2)

 def test_same_content_different_offset_and_role_stay_distinct(self):
  a=ref();b=ref(2,alias=26302);b['xoff']=25;b['attr_sha256']='f'*64
  rows,objects=m.normalize([a,b]);self.assertEqual(len(objects),1)
  self.assertEqual([x['xoff'] for x in rows],[-1,25])

 def test_same_source_occurrence_twice_is_rejected(self):
  with self.assertRaises(ValueError):m.normalize([ref(),ref()])

 def test_cross_profile_equal_ids_are_separate_references(self):
  rows,objects=m.normalize([ref(),ref(profile='TW10')]);self.assertEqual(len(rows),2)
  self.assertEqual(objects[0]['profiles'],'PATCH129|TW10')

 def test_conflicting_metadata_for_identical_block_hash_rejected(self):
  a=ref();b=ref(2);b['_rd']['rd_width']=3
  with self.assertRaises(ValueError):m.normalize([a,b])

 def test_declared_block_size_cannot_use_redundant_bad_header_length(self):
  r=ref();r['_rd']['bytes']=8621864
  with self.assertRaises(ValueError):m.normalize([r])

 def test_canonical_order_does_not_depend_on_input_iteration(self):
  a=[ref(2),ref(1,profile='TW10')]
  self.assertEqual(m.normalize(a),m.normalize(a[::-1]))

 def test_real_raw_exception_keeps_historical_mismatch_and_actual_size(self):
  h,n,p=patch_fixture(True);r=m.patch_reference(h,n,p,{1})
  self.assertEqual(r['source_rd_status'],'HEADER_MISMATCH')
  self.assertEqual(r['catalog_rd_qualification'],'RAW_FLAG0_ADRN_LENGTH_AUTHORITATIVE')
  self.assertEqual(r['_rd']['bytes'],20);self.assertEqual(r['_rd']['rd_size_field'],8621864)

 def test_unpinned_raw_exception_not_promoted(self):
  h,n,p=patch_fixture(True)
  with self.assertRaises(ValueError):m.patch_reference(h,n,p,set())

 def test_raw_flag_size_delta_and_dimensions_guarded(self):
  for field,value in [('rd_flag','1'),('rd_size','21'),('rd_width','3')]:
   with self.subTest(field=field):
    h,n,p=patch_fixture(True);n[field]=value
    with self.assertRaises(ValueError):m.patch_reference(h,n,p,{1})

 def test_pair_identity_hash_and_native_index_are_independent_guards(self):
  for field,value in [('bitmapno','26301'),('patch_index','2'),('patch_record_sha256','e'*64),('native_exact_indices','11'),('rd_sha256','f'*64)]:
   with self.subTest(field=field):
    h,n,p=patch_fixture();p[field]=value
    with self.assertRaises(ValueError):m.patch_reference(h,n,p,set())

 def test_full_record_metadata_mismatch_not_collapsed(self):
  h,n,p=patch_fixture();n['attr_sha256']='e'*64
  with self.assertRaises(ValueError):m.patch_reference(h,n,p,set())

 def test_early_profile_gaps_remain_explicit(self):
  self.assertFalse(m.PROFILES['TW10']['original_snapshot_overwritten_positions_available'])
  self.assertFalse(m.PROFILES['CN50']['original_snapshot_overwritten_positions_available'])
  self.assertEqual(m.PROFILES['CN50']['reported_extra_alias_writes'],585)

 def test_attribute_preimage_proves_field_at_original_offset(self):
  row={k:'0' for k in [*m.SIGNED_ATTR,'atari_x','atari_y','hit_raw','damy_a','damy_b','damy_c']}
  row.update(index='9',map_number='17',attr_sha256=m.sha(b'\0'*48+(17).to_bytes(4,'little')))
  dictionary=m.attribute_dictionary([row])
  self.assertEqual(dictionary[row['attr_sha256']],{'logical_alias':17,'witness_patch_index':9})
  row['map_number']='18'
  with self.assertRaises(ValueError):m.attribute_dictionary([row])

 def test_old_occurrence_recovers_only_through_matching_attribute_sha(self):
  h={'bitmapno':'4','attr_sha256':'a'*64}
  self.assertEqual(m.resolve_early_alias(h,[],{'a'*64:{'logical_alias':17,'witness_patch_index':9}}),
                   (17,'EXACT_ORIGINAL_ATTR_SHA_FIELD_RECOVERY',9))

 def test_missing_attribute_match_never_assumed_zero_or_same_id(self):
  h={'bitmapno':'26301','attr_sha256':'a'*64}
  value,evidence,witness=m.resolve_early_alias(h,[],{})
  self.assertIsNone(value);self.assertEqual(witness,-1)

 def test_snapshot_can_supply_field_when_attribute_dictionary_cannot(self):
  h={'bitmapno':'303117','attr_sha256':'a'*64}
  self.assertEqual(m.resolve_early_alias(h,[{'bitmapno':'303117','map_number':'26089'}],{}),
                   (26089,'ORIGINAL_SNAPSHOT',-1))

 def test_snapshot_disagreement_with_exact_hash_never_silently_overwritten(self):
  with self.assertRaises(ValueError):m.resolve_early_alias({'bitmapno':'4','attr_sha256':'a'*64},
     [{'bitmapno':'4','map_number':'18'}],{'a'*64:{'logical_alias':17,'witness_patch_index':9}})

 def test_real_catalog_recovered_all_manifest_extra_alias_occurrences(self):
  report,refs,content=m.load_catalog(m.ROOT/m.DEST)
  recovered=[r for r in refs if r['alias_evidence']=='EXACT_ORIGINAL_ATTR_SHA_FIELD_RECOVERY']
  self.assertEqual(len(recovered),588)
  self.assertEqual(sum(r['profile']=='TW10' for r in recovered),3)
  self.assertEqual(sum(r['profile']=='CN50' for r in recovered),585)
  self.assertTrue(all(p['unresolved_original_alias_fields']==0 for k,p in report['profiles'].items() if k!='PATCH129'))

 def test_published_catalog_real_query_namespace_and_annotation(self):
  r=m.query(m.ROOT/m.DEST,alias=26301,profile='PATCH129')
  self.assertEqual(r['total_matches'],1)
  self.assertEqual(r['matches'][0]['reference']['physical_bitmapno'],376059)
  self.assertEqual(r['matches'][0]['role_annotation']['role'],'PANEL_BACKGROUND')
  self.assertEqual(m.query(m.ROOT/m.DEST,physical=26301,profile='PATCH129')['total_matches'],0)

 def test_query_limit_retains_total_count_and_all_option(self):
  limited=m.query(m.ROOT/m.DEST,alias=1,profile='PATCH129',limit=1)
  full=m.query(m.ROOT/m.DEST,alias=1,profile='PATCH129',limit=0)
  self.assertTrue(limited['truncated']);self.assertEqual(limited['total_matches'],len(full['matches']))
  self.assertEqual(full['total_matches'],48)

 def test_corrupted_archived_table_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)
   for f in ['REPORT-R1.json','REFERENCES-R1.tsv.gz','CONTENTS-R1.tsv.gz']:
    (p/f).write_bytes((m.ROOT/m.DEST/f).read_bytes())
   b=gzip.decompress((p/'REFERENCES-R1.tsv.gz').read_bytes());m.pack(p/'REFERENCES-R1.tsv.gz',b.replace(b'376059',b'376058',1))
   with self.assertRaises(ValueError):m.load_catalog(p)

 def test_query_requires_an_explicit_valid_namespace(self):
  for kwargs in [{},{'alias':1,'physical':1},{'alias':0},{'content_sha':'not-a-hash'}]:
   with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):m.query(m.ROOT/m.DEST,**kwargs)


if __name__=='__main__':unittest.main()
