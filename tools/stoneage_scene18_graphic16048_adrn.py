"""SCENE18: bounded same-carrier NPC image-key ADRN source record qualification.

Fetch only the original ADRN index member; do not fetch gigantic REAL, claim
actual pixels, render original game, or assign the archived NPC a TW1.0 identity.
"""
from __future__ import annotations
import argparse,hashlib,json,struct,subprocess,tempfile,pathlib,zlib

from tools.stoneage_native_album_source_r36 import SparseParts,fetcher_factory,isolated_rar
from tools.stoneage_private_scene_graphic_join_r1 import ADRN_SIZE,ADRN_SHA,REAL_SIZE,REAL_SHA
from tools.stoneage_scene17_derived_acceptance import validate,REPORT

PREFIX="石器2.5客戶端+服務端+登入器/SA2.5主程式/stoneage2.5/data/"
TARGET="adrn_15.bin"
REAL="real_15.bin"
KEY=16048
MAX_BYTES=64*1024*1024
MAX_REQUESTS=1024

def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)

def collect(reader):
 import rarfile
 seen=0;selected={}
 def callback(i):
  nonlocal seen
  seen+=1
  need(seen<=10000,"original header traversal budget exceeded")
  if i.type!=rarfile.RAR_BLOCK_FILE:return
  pathname=i.filename.replace("\\","/")
  for leaf,expected in ((TARGET,ADRN_SIZE),(REAL,REAL_SIZE)):
   if pathname!=PREFIX+leaf:continue
   need(leaf not in selected,"duplicate exact source member")
   need(i.file_size==expected,"original file length from header differs from independently pinned member")
   selected[leaf]={
    "name":pathname,"size":i.file_size,"packed_size":i.compress_size,
    "flags":i.flags,"crc32":i.CRC,"method":i.compress_type,
    "header_offset":i.header_offset,"data_offset":i.data_offset}
 rarfile.RarFile(reader,info_callback=callback,errors="strict")
 need(TARGET in selected and REAL in selected,"missing paired ADRN/REAL original member headers")
 return selected,seen

def rows(raw):
 need(len(raw)==ADRN_SIZE and sha(raw)==ADRN_SHA,"whole original ADRN15 hash qualification")
 need(len(raw)%80==0,"original ADRN 80 byte record alignment")
 found=[]
 for pos in range(0,len(raw),80):
  field=struct.unpack_from("<I",raw,pos+76)[0]
  if field!=KEY:continue
  row=raw[pos:pos+80]
  bitmap,offset,size,xoff,yoff,width,height=struct.unpack_from("<IIIiiii",row)
  need(size>16 and offset<=REAL_SIZE and size<=REAL_SIZE-offset,"source RD extent outside named REAL")
  need(0<width<=4096 and 0<height<=4096,"original recorded graphic dimensions")
  found.append({"index":pos//80,"numeric_graphic_key":field,"bitmapno":bitmap,
   "original_real_offset":offset,"original_real_size":size,
   "width":width,"height":height,"xoff":xoff,"yoff":yoff,
   "adrn_record_sha256":sha(row)})
 need(len(found)<=16,"excessive alias collisions, cannot assume identity")
 return found

def source():
 import libarchive
 from libarchive import ffi
 v=validate(json.loads(REPORT.read_bytes()))
 need(v["source_graphicname"]==KEY,"genuine NPC source key required")
 fetch,pages=fetcher_factory()
 reader=SparseParts(fetch,max_bytes=MAX_BYTES,max_requests=MAX_REQUESTS)
 receipt={}
 with tempfile.TemporaryDirectory(prefix="scene18-one-adrn-") as directory:
  try:
   selected,count=collect(reader)
   f=selected[TARGET];need(0<f["packed_size"]<=24*1024*1024,"ADRN compressed member download budget")
   need(f["flags"]&(1|2|4|16)==0,"ADRN solid/split/encrypted not independently extractable")
   h=reader.at(f["header_offset"],f["data_offset"]-f["header_offset"])
   p=b"".join(reader.at(f["data_offset"]+i,min(1048576,f["packed_size"]-i)) for i in range(0,f["packed_size"],1048576))
   isolated=isolated_rar(h,p,f["flags"])
   archive=pathlib.Path(directory)/"one-adrn.rar";archive.write_bytes(isolated)
   d=pathlib.Path(directory)/"out";d.mkdir()
   run=subprocess.run(["unar","-f","-o",str(d),str(archive)],capture_output=True,timeout=120)
   need(run.returncode==0,"original static ADRN unar extraction failed")
   found=[x for x in d.rglob("*") if x.is_file() and x.as_posix().endswith(f["name"])]
   need(len(found)==1,"original member extraction ambiguous")
   raw=found[0].read_bytes()
   need(len(raw)==ADRN_SIZE and sha(raw)==ADRN_SHA,"exact original whole ADRN SHA")
   need(zlib.crc32(raw)&0xffffffff==f["crc32"],"original header CRC mismatch")
   secondary_ok=False;secondary_error=None
   try:
    with libarchive.memory_reader(isolated) as lib:
     secondary=[(e.pathname.replace("\\","/"),b"".join(e.get_blocks())) for e in lib]
    need(secondary==[(f["name"],raw)],"independent libarchive decoded bytes differ from unar")
    secondary_ok=True
   except Exception as error:
    need("Parsing filters is unsupported" in str(error),"unexpected independent decoder error")
    secondary_error={"type":type(error).__name__,"message":str(error)[:180]}
   entries=rows(raw)
   receipt={"status":"ADRN15_ONE_DECODER_WHOLE_SHA_CRC_SOURCE_RECORD",
    "original_header_scan_count":count,"source_requests":len(reader.receipts),
    "http206_downloaded_bytes":reader.fetched,"range_receipts":reader.receipts,
    "public_page_receipts":pages,"archived_original_ADRN":{**f,
      "whole_sha256":sha(raw),"original_header_sha256":sha(h),
      "packed_payload_sha256":sha(p),"full_RAR_CRC32_verified":True,
      "unar_result":run.returncode,"libarchive_version":ffi.version_number(),
      "independent_decompressors_equal":secondary_ok,"secondary_decoder_failure":secondary_error},
    "archived_REAL_header_unfetched_payload":selected[REAL],
    "source_graphic_key":KEY,"source_record_matches":entries,"matched_count":len(entries),
    "original_real_bytes_read":0,"original_sprite_pixels_decoded":False,
    "actual_native_game_render_verified":False,
    "original_official_TW10_identity_verified":False,
    "original_archive_whole_sha_reverified":False,
    "original_copyrighted_bytes_uploaded":False,
    "overall_completion_percent":None}
   return receipt
  except Exception as e:
   return {"status":"SOURCE_FAILED_OR_BOUND_REACHED",
    "error":{"type":type(e).__name__,"message":str(e)[:300]},
    "actual_http206_bytes":reader.fetched,"actual_requests":len(reader.receipts),
    "original_sprite_pixels_decoded":False,"overall_completion_percent":None}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--report",type=pathlib.Path,required=True);args=ap.parse_args()
 r={"schema":"stoneage.scene18.original_NPC16048_ADRN_source.r1",
    "source_scope":"PRESERVED_MIXED25_SAME_CARRIER_NOT_TW10_OR_NATIVE_RUNTIME",**source()}
 args.report.write_text(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
 print("SCENE18_BOUNDED_RESULT_BEGIN");print(args.report.read_text());print("SCENE18_BOUNDED_RESULT_END")
 if r["status"]!="ADRN15_ONE_DECODER_WHOLE_SHA_CRC_SOURCE_RECORD":raise SystemExit(2)
if __name__=="__main__":main()
