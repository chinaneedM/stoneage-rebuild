#!/usr/bin/env python3
"""Audit archived mainland 5.0 original EXE bytes without executing or publishing them."""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
 "sa_5000.exe": (630784, "5dbcc3fa276f9f245fb706bce957e9c3300d870df813889502b789b727e49c97"),
 "StoneAge.exe": (225280, "cb118a01c2673da221fa15b4ae93dbfcbc7786f1142bfffa542459ec6716f61c")
}
def sha(raw):
 return hashlib.sha256(raw).hexdigest()

def text_hits(raw, names, codec):
 hits=[]
 for name in sorted(set(names)):
  try: token=name.encode(codec,"strict")
  except UnicodeEncodeError: continue
  if len(token)<4: continue
  start=0
  while True:
   pos=raw.find(token,start)
   if pos<0: break
   hits.append({"name":name,"offset":pos,"token_sha256":sha(token)})
   start=pos+1
 return sorted(hits,key=lambda x:(x["offset"],x["name"]))

def parse_row(raw, offset, codec):
 if offset<0 or offset+28>len(raw):return None
 slot,field,face=struct.unpack_from("<i20sI",raw,offset)
 if not -1<=slot<=100000 or b"\x00" not in field:return None
 blob,pad=field.split(b"\x00",1)
 if any(pad):return None
 try: name=blob.decode(codec,"strict")
 except UnicodeDecodeError:return None
 if slot==-1:
  if name not in ("無","无") or face!=0:return None
 elif not (1<=len(name)<=10 and 0<face<=5000000 and
            any("\u4e00"<=c<="\u9fff" for c in name)):return None
 return {"slot":slot,"name":name,"face":face}

def table_candidates(raw,codec,min_rows=10):
 out=[];offset=0;limit=len(raw)-28*min_rows
 while offset<=limit:
  if parse_row(raw,offset,codec) is None:
   offset+=1;continue
  rows=[];pos=offset
  while len(rows)<2000:
   row=parse_row(raw,pos,codec)
   if row is None:break
   rows.append(row);pos+=28
  if len(rows)>=min_rows:
   out.append({"file_offset":offset,"stride":28,"rows":len(rows),
               "filled":sum(x["slot"]!=-1 for x in rows),
               "placeholders":sum(x["slot"]==-1 for x in rows),
               "first_names":[x["name"] for x in rows[:5]],
               "table_source_sha256":sha(raw[offset:pos]),
               "native_pet_id_or_release_proven":False})
   offset=pos
  else:offset+=1
 return out

def aligned_region_metadata(raw,start,rows,codec):
 """Read only typed row summaries; never copy raw original table bytes into Git."""
 if start<0 or start+28*rows>len(raw):raise ValueError("out-of-bounds")
 kinds={"populated":0,"empty":0,"unparsed":0}
 bad=[]
 for idx in range(rows):
  off=start+28*idx
  item=parse_row(raw,off,codec)
  if item is None:
   kinds["unparsed"]+=1
   if len(bad)<12:
    slot,_,face=struct.unpack_from("<i20sI",raw,off)
    bad.append({"index":idx,"slot_integer":slot,"face_integer":face})
  else:kinds["empty" if item["slot"]==-1 else "populated"]+=1
 return {"start_offset":start,"rows":rows,"stride":28,"counts":kinds,
         "first_unparsed_row_shapes":bad,"is_whole_region_decodable":kinds["unparsed"]==0,
         "source_span_sha256":sha(raw[start:start+28*rows]),
         "raw_table_bytes_published":False}

def inspect(directory):
 manifest=json.loads((ROOT/"research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json").read_text(encoding="utf-8"))
 tw=json.loads((ROOT/"research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json").read_text(encoding="utf-8"))
 if manifest["status"]!="REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED" or manifest["files"]["count"]!=413:
  raise ValueError("prior-source-manifest-not-qualified")
 files={x["name"]:(x["size"],x["sha256"]) for x in manifest["files"]["inventory"]}
 names=[x["name_as_written"] for x in tw["records"]]
 if len(names)!=124:raise ValueError("unexpected-reference-pet-album")
 output=[]
 for file,identity in EXPECTED.items():
  if files.get(file)!=identity:raise ValueError("old-source-hash-mismatch:"+file)
  content=(directory/file).read_bytes()
  if (len(content),sha(content))!=identity:raise ValueError("actual-EXE-hash-mismatch:"+file)
  if content[:2]!=b"MZ":raise ValueError("MZ-header-missing")
  peoff=struct.unpack_from("<I",content,0x3c)[0]
  if peoff+4>len(content) or content[peoff:peoff+4]!=b"PE\x00\x00":
   raise ValueError("PE-header-missing")
  enc={}
  for codec in ("cp950","gb18030"):
   hits=text_hits(content,names,codec)
   groups=table_candidates(content,codec)
   enc[codec]={"candidate_362_row_contiguous_span":aligned_region_metadata(content,536424,362,codec) if file=="sa_5000.exe" else None,
               "matched_distinct_names":len({x["name"] for x in hits}),
               "matching_occurrences":len(hits),
               "matched_name_offsets":hits[:150],
               "name_hits_truncated":len(hits)>150,
               "tw10_layout_28byte_tables":groups[:10],
               "table_hits_truncated":len(groups)>10}
  output.append({"file":file,"size":identity[0],"sha256":identity[1],
                 "PE_header_verified":True,"encodings":enc})
 return {
  "schema":"stoneage.pet126k.cn50_original_program_pet_name_source_probe.r1",
  "date":"2026-11-21","active_module":"PET",
  "scope":"ORIGINAL_CLASSIC_PC_ONLY",
  "archive":{"identifier":"Stoneage-5","source_tier":"THIRD_PARTY_PRESERVED_WAEI_5_0_PC_OPTICAL_IMAGE_NOT_INDEPENDENTLY_PRESSING_CERTIFIED",
             "CAB_sha256":manifest["source"]["cab_sha256"],
             "source_413_files_previously_SHA_verified":True,
             "source_byte_replayed_this_run":sum(z[0] for z in EXPECTED.values()),
             "new_unique_client_build_count":0,
             "official_original_pressing_authenticated":False},
  "original_TW10_same_name_text_needle_count":len(names),
  "programs":output,
  "negative_guards":{"name_text_not_proven_native_pet_id":True,
                     "tw10_same_name_does_not_prove_cn50_same_species":True,
                     "potential_table_not_official_live_roster":True,
                     "game_binary_never_executed":True,
                     "commercial_program_not_committed":True,
                     "no_server_pet_master":True,
                     "new_official_species":0,
                     "pet_module_closed":False,
                     "year_2026":"NOT_YEAR_AUDITED",
                     "overall_percent":None}
 }
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--source-dir",type=Path,required=True)
 p.add_argument("--output",type=Path,required=True)
 args=p.parse_args()
 result=inspect(args.source_dir)
 args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 for program in result["programs"]:
  print("ORIGINAL_EXE|"+program["file"]+"|"+program["sha256"])
  for codec,group in program["encodings"].items():
   print("TEXT|"+codec+"|names="+str(group["matched_distinct_names"])+
         "|hits="+str(group["matching_occurrences"])+
         "|candidate_tables="+str(len(group["tw10_layout_28byte_tables"])))
 print("RESULT|source-qualified-only|no-native-ID-or-official-release-claimed")
if __name__=="__main__":main()
