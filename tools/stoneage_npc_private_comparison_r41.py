"""Independently replay the R41 text change from private original files.

The observed character map is a bounded difference description, not a general
Traditional/Simplified converter. No whole script or dialogue is exported.
"""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_preserved_npc_delta_r41 import EXPECTED,modern_argument,arg_delta
from tools.stoneage_native_album_source_r36 import need

def sha(raw):return hashlib.sha256(raw).hexdigest()
def compare(directory,modern_path):
 directory=Path(directory);pins={};originals={}
 for name,(size,digest) in EXPECTED.items():
  raw=(directory/name).read_bytes();need((len(raw),sha(raw))==(size,digest),'private exact original source '+name)
  originals[name]=raw;pins[name]={'bytes':len(raw),'sha256':sha(raw)}
 modern_raw=Path(modern_path).read_bytes();modern,qualified=modern_argument(modern_raw)
 old=originals['sb_kbu.arg'].decode('cp950','strict');old_big5=originals['sb_kbu.arg'].decode('big5','strict')
 need(old==old_big5,'two original decoder texts agree')
 target=modern.decode('gb18030','strict');old_fields=dict(x.split(':',1) for x in old.splitlines());new_fields=dict(x.split(':',1) for x in target.splitlines())
 need(list(old_fields)==list(new_fields),'ordered field names same')
 differences=[];mapping={}
 for field,old_value in old_fields.items():
  new_value=new_fields[field];need(len(old_value)==len(new_value),'equal per-field Unicode lengths')
  for i,(a,b) in enumerate(zip(old_value,new_value)):
   if a==b:continue
   need(a not in mapping or mapping[a]==b,'consistent observed character replacement')
   mapping[a]=b;differences.append({'field':field,'character_index_0':i,'old_character':a,'modern_character':b})
 reconstructed=old.translate(str.maketrans(mapping)).encode('gb18030','strict')
 need(reconstructed==modern,'observed replacements plus encoding reproduce entire modern argument')
 delta=arg_delta(originals['sb_kbu.arg'],modern)
 return {'schema':'stoneage.npc_private_original_comparison.r41','original_file_pins':pins,
  'modern_yaml_git_blob':qualified['upstream_blob'],'modern_argument_sha256':sha(modern),
  'source_unicode_cp950_big5_equal':True,'whole_unicode_text_equal_before_replacement':old==target,
  'original_cp950_roundtrip_equal':old.encode('cp950')==originals['sb_kbu.arg'],
  'original_big5_roundtrip_equal':old_big5.encode('big5')==originals['sb_kbu.arg'],
  'raw_byte_difference_count':len(delta['different_byte_offsets']),
  'character_differences':differences,'observed_character_map':mapping,
  'exact_modern_bytes_reproduced_after_observed_map_and_gb18030':True,
  'whole_script_or_dialogue_published':False,'official_same_build_authenticated':False,
  'classification':'ENCODING_CHANGE_AND_OBSERVED_CHARACTER_REPLACEMENTS_NUMERIC_FIELDS_IDENTICAL'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--modern',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 result=compare(a.directory,a.modern);a.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'status':'PASS','character_changes':len(result['character_differences']),'observed_character_pairs':len(result['observed_character_map'])}))
if __name__=='__main__':main()
