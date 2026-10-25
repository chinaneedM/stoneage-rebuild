"""Queryable, non-destructive logical alias catalog from pinned derived tables.

Only original metadata and block digests are consumed. No original programs,
artwork, client downloads, inferred species names or runtime last-write choice.
"""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile

ROOT=Path(__file__).resolve().parents[1]
DEST=Path('research/recovered/logical-alias-catalog-r1')
PATCH='research/recovered/wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz'
NATIVE='research/recovered/adrn129-tw85-real-pair/NATIVE-R1.tsv.gz'
PAIRS='research/recovered/adrn129-tw85-real-pair/PAIRS-R1.tsv.gz'
ACCEPT='research/recovered/STONEAGE-ADRN129-REAL-ACCEPTANCE-R1.json'
UI='research/recovered/STONEAGE-WAYI-LOGIN-SCENE-ALIAS-BINDING-R1.json'
EARLY={p:f'research/recovered/{d}-resource-metadata/' for p,d in [('TW10','tw10'),('CN50','cn50')]}
PINS={PATCH:'d8049cb6ce74a2c048372aa51fc81b6921a995b6fa45b03dd5511a93509958ca',
 NATIVE:'495928a0a44d7c81bf1d6ef7b06d26decfc5096803fbd60b9e8e0aa9752a45ce',
 PAIRS:'ee41e4266b3bbab162d9271c1b86cceaa85354e60ff3e389fffccd68010b1314',
 ACCEPT:'8b5e82e28fccff244d4fe5b3dddf58e4b6663ae0fd3bbdb8243c47433d720b6f',
 UI:'a5cf9e071d34076b5108949b127a5b615ca2453b2fe7010757d27142e244aa52',
 EARLY['TW10']+'ADRN-R1.tsv.gz':'c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea',
 EARLY['TW10']+'COLLISION-ATTR-R1.tsv.gz':'d26b318ea73833bd7cc68abc8b5798a81b76ef9309cc91b137f7a55c6c8275dc',
 EARLY['TW10']+'MANIFEST-R1.txt':'fb9b2dbe52a305f5ff2934cc1dcdf275be1215e2a89b326dd76fd7f80b6d9743',
 EARLY['CN50']+'ADRN-R1.tsv.gz':'e24afc513d28c7f25bd26bde9c69ddc0de4000147a2b11f50b5176655d8558fd',
 EARLY['CN50']+'COLLISION-ATTR-R1.tsv.gz':'4417afac7caffee86bf64ca36d9bfdff06fef61b9e3af200bf59b153280dc8df',
 EARLY['CN50']+'MANIFEST-R1.json':'73181d1de1efadc971eaea254891103bd69fd7d3121fc450ec3b148ca8d06fa8'}
PROFILES={
 'TW10':{'view':'ORIGINAL_SNAPSHOT_PLUS_EXACT_ATTR_SHA_FIELD_RECOVERY','retained_refs':9289,'original_snapshot_refs':9286,
         'reported_extra_alias_writes':3,'original_snapshot_overwritten_positions_available':False,
         'hash_qualified_extra_occurrences':3,
         'provenance':'ACCEPTED_EARLY_RETAIL_BASELINE_METADATA'},
 'CN50':{'view':'ORIGINAL_SNAPSHOT_PLUS_EXACT_ATTR_SHA_FIELD_RECOVERY','retained_refs':14114,'original_snapshot_refs':13529,
         'reported_extra_alias_writes':585,'original_snapshot_overwritten_positions_available':False,
         'hash_qualified_extra_occurrences':585,
         'provenance':'PRESERVED_CN50_NOT_AUTHENTICATED_CLEAN_PRESSING'},
 'PATCH129':{'view':'FULL_NONZERO_ALIAS_OCCURRENCES','retained_refs':20229,
             'reported_extra_alias_writes':586,'original_table_all_occurrence_positions_available':True,
             'provenance':'OFFICIAL_PATCH_CAPTURE_20060911_NOT_FULL_CLIENT'}}
REF_FIELDS=['profile','logical_alias','source_index','physical_bitmapno','adrn_offset','adrn_size',
 'xoff','yoff','width','height','attr_sha256','record_sha256','content_id','alias_evidence','alias_witness_patch_index',
 'source_rd_status','catalog_rd_qualification','physical_record_multiplicity']
CONTENT_FIELDS=['content_id','rd_sha256','bytes','rd_flag','rd_width','rd_height','rd_size_field','reference_count','profiles']
RD_FIELDS=['rd_sha256','bytes','rd_flag','rd_width','rd_height','rd_size_field']
SIGNED_ATTR='height_flag broken indamage outdamage inpoison innumb inquiet instone indark inconfuse outpoison outnumb outquiet outstone outdark outconfuse effect1 effect2'.split()


def need(ok,message):
 if not ok:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def tsv(root,path):
 with gzip.open(root/path,'rt',encoding='utf-8',newline='') as f:
  yield from csv.DictReader(f,delimiter='\t')


def source_pins(root):
 pins={}
 for p,h in PINS.items():
  b=(root/p).read_bytes();need(sha(b)==h,'pinned original metadata changed: '+p)
  pins[p]={'bytes':len(b),'sha256':h,'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
 return pins


def reference(profile,logical,index,header,rd,status,qualification):
 need(profile in PROFILES and type(logical) is int and logical>0,'invalid logical namespace')
 r={'profile':profile,'logical_alias':logical,'source_index':index,
    'physical_bitmapno':int(header['bitmapno']),'adrn_offset':int(header['adder']),
    'adrn_size':int(header['size']),'attr_sha256':header['attr_sha256'],
    'record_sha256':header.get('record_sha256',''),'source_rd_status':status,
    'catalog_rd_qualification':qualification,'alias_evidence':'ORIGINAL_COMPLETE_OCCURRENCE_TABLE',
    'alias_witness_patch_index':-1}
 r.update({k:int(header[k]) for k in ['xoff','yoff','width','height']})
 need(r['adrn_offset']>=0 and r['adrn_size']>=16,'invalid original block extent')
 need(len(r['attr_sha256'])==64 and len(rd['rd_sha256'])==64,'missing source content/attribute hash')
 need(rd['bytes']==r['adrn_size'],'content size differs from ADRN-authoritative block size')
 r['_rd']=rd
 return r


def attribute_dictionary(records):
 """Prove the numeric alias field by reconstructing its entire original 52B block."""
 result={}
 for r in records:
  a=struct.pack('<BBH18h3H2xI',int(r['atari_x']),int(r['atari_y']),int(r['hit_raw']),
      *[int(r[k]) for k in SIGNED_ATTR],*[int(r[k]) for k in ['damy_a','damy_b','damy_c','map_number']])
  fingerprint=sha(a);need(fingerprint==r['attr_sha256'],'numeric attribute block does not reproduce original SHA')
  value=int(r['map_number']);index=int(r['index'])
  if fingerprint in result:need(result[fingerprint]['logical_alias']==value,'conflicting field values for identical attribute SHA')
  else:result[fingerprint]={'logical_alias':value,'witness_patch_index':index}
 return result


def resolve_early_alias(header,snapshots,dictionary):
 need(len(snapshots)<=1,'multiple snapshot rows for one original occurrence')
 known=dictionary.get(header['attr_sha256'])
 if snapshots:
  s=snapshots[0];need(s['bitmapno']==header['bitmapno'],'snapshot physical identifier/index mismatch')
  value=int(s['map_number'])
  if known:need(known['logical_alias']==value,'original snapshot and exact-attribute recovery disagree')
  return value,'ORIGINAL_SNAPSHOT',known['witness_patch_index'] if known else -1
 if known:
  return known['logical_alias'],'EXACT_ORIGINAL_ATTR_SHA_FIELD_RECOVERY',known['witness_patch_index']
 return None,'UNRESOLVED_ORIGINAL_ATTRIBUTE_FIELD',-1


def early_references(root,profile,dictionary):
 prefix=EARLY[profile];by_index=defaultdict(list)
 for c in tsv(root,prefix+'COLLISION-ATTR-R1.tsv.gz'):
  by_index[int(c['adrn_index'])].append(c)
 refs=[];physical=Counter();records=0;unknown=[];recovered=0;snapshot_count=0;hash_known=0
 for h in tsv(root,prefix+'ADRN-R1.tsv.gz'):
  records+=1;physical[int(h['bitmapno'])]+=1
  snapshots=by_index.pop(int(h['index']),[]);snapshot_count+=len(snapshots)
  hash_known+=h['attr_sha256'] in dictionary
  logical,evidence,witness=resolve_early_alias(h,snapshots,dictionary)
  if logical is None:unknown.append(int(h['index']))
  elif logical:
   rd={'rd_sha256':h['rd_block_sha256'],'bytes':int(h['size']),
       **{k:int(h[k]) for k in ['rd_flag','rd_width','rd_height','rd_size_field']}}
   item=reference(profile,logical,int(h['index']),h,rd,'PRIOR_ORIGINAL_BLOCK_METADATA','PRIOR_ORIGINAL_BLOCK_HASH')
   item['alias_evidence']=evidence;item['alias_witness_patch_index']=witness
   recovered+=evidence=='EXACT_ORIGINAL_ATTR_SHA_FIELD_RECOVERY';refs.append(item)
 need(not by_index,'snapshot points outside complete source table')
 for r in refs:r['physical_record_multiplicity']=physical[r['physical_bitmapno']]
 need(records=={'TW10':125996,'CN50':303197}[profile],'early physical source count changed')
 need(not unknown,'unresolved original alias fields; never assume zero')
 need(snapshot_count==PROFILES[profile]['original_snapshot_refs'] and recovered==PROFILES[profile]['hash_qualified_extra_occurrences'],'early snapshot/recovery counts drift')
 return refs,{'physical_records_in_parent':records,'distinct_physical_ids_in_parent':len(physical),
   'attribute_fingerprint_known_rows':hash_known,'snapshot_only_attribute_rows':records-hash_known,
   'unresolved_original_alias_fields':len(unknown),'hash_qualified_recovered_occurrences':recovered}


def patch_reference(h,n,p,accepted_raw):
 index=int(h['index']);physical=int(h['bitmapno'])
 need(int(p['patch_index'])==index and int(p['bitmapno'])==physical and
      int(n['bitmapno'])==physical,'patch/native pair identity mismatch')
 need(h['record_sha256']==n['record_sha256']==p['patch_record_sha256'],'original full-record hashes disagree')
 need(p['native_exact_indices']==n['index'],'ambiguous or wrong native exact occurrence')
 for k in ['adder','size','xoff','yoff','width','height','attr_sha256']:
  need(h[k]==n[k],'patch/native header or attr mismatch: '+k)
 need(n['rd_sha256']==p['rd_sha256'] and n['rd_status']==p['rd_status'],'actual RD pair differs')
 need([int(n[k]) for k in ['rd_width','rd_height']]==[int(h['width']),int(h['height'])],'RD dimensions differ')
 if n['rd_status']=='HEADER_MATCH':
  need(p['qualification']=='EXACT_NATIVE_RECORD_AND_RD_STRUCTURE' and int(n['rd_size'])==int(h['size']),'strict RD qualification differs')
  qualification='MATCHING_RD_HEADER'
 else:
  need(index in accepted_raw and n['rd_status']=='HEADER_MISMATCH' and
       p['qualification']=='RD_STRUCTURE_NOT_QUALIFIED','unaccepted historical mismatch')
  need(int(n['rd_flag'])==0 and int(h['size'])==16+int(h['width'])*int(h['height'])
       and int(n['rd_size'])-int(h['size'])==8621844,'raw flag0 exception changed')
  qualification='RAW_FLAG0_ADRN_LENGTH_AUTHORITATIVE'
 rd={'rd_sha256':n['rd_sha256'],'bytes':int(h['size']), 'rd_size_field':int(n['rd_size']),
     **{k:int(n[k]) for k in ['rd_flag','rd_width','rd_height']}}
 return reference('PATCH129',int(h['map_number']),index,h,rd,n['rd_status'],qualification)


def patch_references(root):
 selected={};physical=Counter();count=0
 for h in tsv(root,PATCH):
  count+=1;physical[int(h['bitmapno'])]+=1
  if int(h['map_number']):
   index=int(h['index']);need(index not in selected,'duplicate source occurrence index');selected[index]=h
 pairs={int(p['patch_index']):p for p in tsv(root,PAIRS) if int(p['patch_index']) in selected}
 need(len(pairs)==len(selected),'missing patch source pair')
 target={p['native_exact_indices'] for p in pairs.values()}
 native={n['index']:n for n in tsv(root,NATIVE) if n['index'] in target}
 accepted={r['patch_index'] for r in json.loads((root/ACCEPT).read_bytes())['patch_raw_length_exceptions']}
 refs=[]
 for index,h in sorted(selected.items()):
  p=pairs[index];need(p['native_exact_indices'] in native,'native exact occurrence unavailable')
  r=patch_reference(h,native[p['native_exact_indices']],p,accepted)
  r['physical_record_multiplicity']=physical[r['physical_bitmapno']];refs.append(r)
 need(count==389698 and len(physical)==389670,'original patch source count changed')
 return refs,{'physical_records_in_parent':count,'distinct_physical_ids_in_parent':len(physical)}


def normalize(refs):
 """Deduplicate blocks while retaining every source-reference occurrence."""
 keys=set();objects={};seen=set()
 for r in refs:
  identity=(r['profile'],r['logical_alias'],r['source_index'],r['physical_bitmapno'])
  need(identity not in seen,'same occurrence supplied twice');seen.add(identity)
  rd=r['_rd'];need(len(rd['rd_sha256'])==64 and rd['bytes']==r['adrn_size'],'bad content identity or block size')
  key=(rd['bytes'],rd['rd_sha256']);keys.add(key)
  if key in objects:need(objects[key]==rd,'same block hash/length has conflicting original header metadata')
  else:objects[key]=rd
 ids={key:i for i,key in enumerate(sorted(keys),1)};groups={};out=[]
 for key,i in ids.items():groups[i]={'content_id':i,**objects[key],'reference_count':0,'_profiles':set()}
 for r in sorted(refs,key=lambda x:(x['logical_alias'],x['profile'],x['source_index'],x['physical_bitmapno'])):
  item={k:v for k,v in r.items() if k!='_rd'};key=(r['_rd']['bytes'],r['_rd']['rd_sha256'])
  item['content_id']=ids[key];out.append(item);g=groups[ids[key]];g['reference_count']+=1;g['_profiles'].add(r['profile'])
 content=[]
 for g in groups.values():g['profiles']='|'.join(sorted(g.pop('_profiles')));content.append(g)
 need(sum(x['reference_count'] for x in content)==len(out),'content/reference conservation failed')
 return out,content


def table_bytes(fields,rows):
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fields,delimiter='\t',lineterminator='\n',extrasaction='raise')
 w.writeheader();w.writerows(rows);return buf.getvalue().encode('utf-8')


def pack(path,raw):
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0,compresslevel=9) as z:z.write(raw)


def build(root=ROOT):
 pins=source_pins(root);refs=[];parent_counts={};dictionary=attribute_dictionary(tsv(root,PATCH))
 for profile in ['TW10','CN50']:
  rows,counts=early_references(root,profile,dictionary);refs.extend(rows);parent_counts[profile]=counts
 rows,counts=patch_references(root);refs.extend(rows);parent_counts['PATCH129']=counts
 refs,content=normalize(refs);by_alias=defaultdict(lambda:defaultdict(list))
 for r in refs:by_alias[r['logical_alias']][r['profile']].append(r)
 profiles={}
 for name,scope in PROFILES.items():
  rows=[r for r in refs if r['profile']==name];counts=Counter(r['logical_alias'] for r in rows)
  need(len(rows)==scope['retained_refs'],'reference scope changed: '+name)
  profiles[name]={**scope,**parent_counts[name],'distinct_aliases':len(counts),
   'alias_occurrence_view_complete_for_pinned_parent_metadata':True,
   'duplicate_alias_keys_in_view':sum(n>1 for n in counts.values()),'extra_occurrences_in_view':sum(n-1 for n in counts.values()),
   'raw_length_exception_refs':sum(r['catalog_rd_qualification']=='RAW_FLAG0_ADRN_LENGTH_AUTHORITATIVE' for r in rows)}
 masks=Counter('|'.join(sorted(p)) for p in by_alias.values())
 shared=[p for p in by_alias.values() if len(p)>1]
 shared_identical=sum(len({r['content_id'] for rs in p.values() for r in rs})==1 for p in shared)
 ui=json.loads((root/UI).read_bytes());annotations=[]
 for a in ui['original_patch_alias_bindings']:
  for c in a['candidates']:
   role=next(d['role'] for d in ui['compiled']['draw_calls'] if d['logical_alias']==a['logical_alias'])
   hits=[r for r in refs if r['profile']=='PATCH129' and r['source_index']==c['index'] and r['logical_alias']==a['logical_alias']]
   need(len(hits)==1 and hits[0]['physical_bitmapno']==c['bitmapno'],'prior UI source binding changed')
   annotations.append({'profile':'PATCH129','source_index':c['index'],'logical_alias':a['logical_alias'],
    'role':role,'evidence':'UI12_STATIC_CROSS_SPECIMEN_CANDIDATE_NOT_RUNTIME','game_entity_id':None})
 raw_refs=table_bytes(REF_FIELDS,refs);raw_content=table_bytes(CONTENT_FIELDS,content)
 logical_bytes=sum(r['adrn_size'] for r in refs);distinct_bytes=sum(c['bytes'] for c in content)
 report={'schema':'stoneage.crossversion_logical_alias_catalog.r1','task':'ORIGINAL-RESOURCE-LOGICAL-ALIAS-CROSSVERSION-CATALOG-13',
  'source_pins':pins,'profiles':profiles,'datasets':{
   'REFERENCES-R1.tsv.gz':{'rows':len(refs),'uncompressed_bytes':len(raw_refs),'uncompressed_sha256':sha(raw_refs),'columns':REF_FIELDS},
   'CONTENTS-R1.tsv.gz':{'rows':len(content),'uncompressed_bytes':len(raw_content),'uncompressed_sha256':sha(raw_content),'columns':CONTENT_FIELDS}},
  'distinct_logical_aliases_across_profiles':len(by_alias),'profile_membership_counts':dict(sorted(masks.items())),
  'shared_aliases_across_profiles':len(shared),'shared_aliases_with_single_identical_content':shared_identical,
  'shared_aliases_with_differing_or_multiple_contents':len(shared)-shared_identical,
  'finite_next_review_aliases':[k for k,p in sorted(by_alias.items()) if set(p)=={'CN50'}],
  'content_reference_counts':{'all':len(refs),'distinct_blocks':len(content),'reused_references':len(refs)-len(content),
   'cross_profile_blocks':sum('|' in c['profiles'] for c in content)},
  'byte_reference_budget':{'logical_referenced_bytes':logical_bytes,'distinct_block_bytes':distinct_bytes,
   'repeated_reference_bytes':logical_bytes-distinct_bytes,'actual_original_disk_bytes_deleted':0},
  'annotations':annotations,'default_unannotated_role':'UNKNOWN_RESOURCE_ALIAS',
  'attribute_field_recovery':{'dictionary_fingerprints':len(dictionary),
   'numeric_patch_attributes_reconstructed_and_sha_verified':389698,
   'historical_snapshot_references':43044,'hash_qualified_extra_references':588,
   'uses_same_number_guessing':False,'original_snapshots_modified':False,
   'witness_index_is_an_attribute_preimage_example_not_runtime_selection':True},
  'boundaries':{'content_ids_are_catalog_local':True,'raw_original_payloads_in_catalog':False,
   'pixel_equivalence_from_block_hash_inferred':False,'world_floor_or_species_count_inferred':False,
   'same_alias_means_same_game_entity':False,'same_deployed_official_build_authenticated':False,
   'early_overwritten_alias_occurrences_reconstructed_by_exact_attribute_sha':True,'full_tw85_alias_profile_available':False,
   'tw85_native_records_outside_patch_without_full_numeric_alias_metadata':26522,
   'overall_restoration_percentage':None,'stage_b_wiki':'GATED'},
  'next':'RESOURCE-LOGICAL-ALIAS-MATERIAL-DIFFERENCES-14'}
 return report,raw_refs,raw_content


def write(root,out):
 report,a,b=build(root);out.mkdir(parents=True,exist_ok=True)
 pack(out/'REFERENCES-R1.tsv.gz',a);pack(out/'CONTENTS-R1.tsv.gz',b)
 (out/'REPORT-R1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 return report


def load_catalog(path):
 report=json.loads((path/'REPORT-R1.json').read_bytes());tables={}
 for filename in ['REFERENCES-R1.tsv.gz','CONTENTS-R1.tsv.gz']:
  raw=gzip.decompress((path/filename).read_bytes());expected=report['datasets'][filename]
  need(len(raw)==expected['uncompressed_bytes'] and sha(raw)==expected['uncompressed_sha256'],'archive canonical table digest differs')
  reader=csv.DictReader(io.StringIO(raw.decode()),delimiter='\t');need(reader.fieldnames==expected['columns'],'table schema changed')
  rows=list(reader);need(len(rows)==expected['rows'],'table count changed');tables[filename]=rows
  strings={'profile','attr_sha256','record_sha256','source_rd_status','catalog_rd_qualification','rd_sha256','profiles','alias_evidence'}
  for row in rows:
   for key in row:
    if key not in strings:row[key]=int(row[key])
 return report,tables['REFERENCES-R1.tsv.gz'],tables['CONTENTS-R1.tsv.gz']


def query(path,alias=None,physical=None,content_sha=None,profile=None,limit=100):
 need(sum(x is not None for x in [alias,physical,content_sha])==1,'choose one explicit identifier namespace')
 need(profile is None or profile in PROFILES,'unknown profile')
 need(type(limit)is int and limit>=0,'invalid result limit')
 need(alias is None or type(alias)is int and alias>0,'logical alias must be positive')
 need(physical is None or type(physical)is int and physical>=0,'physical ID must be nonnegative')
 need(content_sha is None or len(content_sha)==64 and all(c in '0123456789abcdef' for c in content_sha),'expected lowercase SHA256')
 report,refs,content=load_catalog(path);blocks={c['content_id']:c for c in content};matches=[]
 for r in refs:
  if profile and r['profile']!=profile:continue
  c=blocks[r['content_id']]
  if alias is not None and int(r['logical_alias'])!=alias:continue
  if physical is not None and int(r['physical_bitmapno'])!=physical:continue
  if content_sha is not None and c['rd_sha256']!=content_sha:continue
  annotation=next((a for a in report['annotations'] if a['profile']==r['profile'] and a['source_index']==int(r['source_index']) and a['logical_alias']==int(r['logical_alias'])),None)
  matches.append({'reference':r,'content':c,'role_annotation':annotation or {'role':'UNKNOWN_RESOURCE_ALIAS'}})
 total=len(matches)
 return {'matches':matches if not limit else matches[:limit],'total_matches':total,'truncated':bool(limit and total>limit),
         'identifier_namespaces_are_distinct':True,'profile_scope':{p:report['profiles'][p] for p in ({profile} if profile else PROFILES)}}


def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 b=sub.add_parser('build');b.add_argument('--output',type=Path,default=ROOT/DEST)
 v=sub.add_parser('verify');v.add_argument('--catalog',type=Path,default=ROOT/DEST)
 q=sub.add_parser('query');q.add_argument('--catalog',type=Path,default=ROOT/DEST)
 group=q.add_mutually_exclusive_group(required=True);group.add_argument('--alias',type=int);group.add_argument('--physical',type=int);group.add_argument('--content-sha')
 q.add_argument('--profile',choices=list(PROFILES));q.add_argument('--limit',type=int,default=100)
 args=parser.parse_args()
 if args.command=='build':
  r=write(ROOT,args.output);print(json.dumps({'references':r['datasets']['REFERENCES-R1.tsv.gz']['rows'],'contents':r['datasets']['CONTENTS-R1.tsv.gz']['rows']}))
 elif args.command=='verify':
  archived,refs,content=load_catalog(args.catalog);fresh,a,b=build()
  need(archived==fresh,'source-derived catalog summary differs')
  need(table_bytes(REF_FIELDS,refs)==a and table_bytes(CONTENT_FIELDS,content)==b,'exact canonical semantic replay differs')
  print('all source references, content groups, provenance gaps and canonical bytes verified')
 else:print(json.dumps(query(args.catalog,args.alias,args.physical,args.content_sha,args.profile,args.limit),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
