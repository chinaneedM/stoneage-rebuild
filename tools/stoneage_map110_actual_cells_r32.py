"""R32: derive three changed map-110 cells from two original 2003 archived DATs.

Source workflow may temporarily read original 4MiB map.exe captures. Only a
tiny derived hash/value/coordinate report is suitable for public Git.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT=Path(__file__).resolve().parents[1]
TIMELINE=ROOT/"research/recovered/STONEAGE-2003-MAP-TIMELINE-R1.txt"
ID=110
SOURCES={
 "june": {"capture":"20030623234451","container_sha256":"372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e","file_sha256":"7d3e4e1dd8582268e14b3d21d0b0594c166f28062b05c8af260a6b214c41930d"},
 "dec": {"capture":"20031210092426","container_sha256":"5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc","file_sha256":"c2890121aa58447941b45c3e5041b444f22648bcef4403cb9ab18f6adbf41b7a"}
}

def digest(data):
 return hashlib.sha256(data).hexdigest()

def original_git_blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

def parse_dat(payload):
 if len(payload)<8:raise ValueError("truncated map header")
 w,h=struct.unpack_from("<II",payload)
 n=w*h
 if not w or not h or n>1000000 or len(payload)!=8+6*n:
  raise ValueError("invalid three-plane original map DAT")
 planes=[]
 for ordinal in range(3):
  raw=payload[8+2*n*ordinal:8+2*n*(ordinal+1)]
  plane=[v[0] for v in struct.iter_unpack("<H",raw)]
  if len(plane)!=n:raise ValueError("truncated original uint16 plane")
  planes.append((raw,plane))
 return w,h,planes

def compare(june,dec):
 w,h,j=parse_dat(june)
 wd,hd,d=parse_dat(dec)
 if (w,h)!=(46,45) or (wd,hd)!=(w,h):raise ValueError("source map110 dimensions changed")
 out=[]
 for k in range(3):
  raw_j,aj=j[k]; raw_d,ad=d[k]
  delta=[i for i,(v,z) in enumerate(zip(aj,ad)) if v!=z]
  out.append({"ordinal":k+1,"june_plane_sha256":digest(raw_j),"dec_plane_sha256":digest(raw_d),
              "changed_cell_count":len(delta),
              "old_nonzero_count":sum(x!=0 for x in aj),"new_nonzero_count":sum(x!=0 for x in ad),
              "changes":[{"index":i,"x_rowmajor_candidate":i%w,"y_rowmajor_candidate":i//w,
                          "june_u16":aj[i],"dec_u16":ad[i]} for i in delta]})
 if [q["changed_cell_count"] for q in out]!=[0,0,3]:
  raise ValueError("historical documented map110 0/0/3 counts contradicted")
 return {"width":w,"height":h,"total_cells_per_plane":w*h,"total_actual_cells_compared":w*h*3,
         "plane_diffs":out}

def verify_timeline(text):
 lines=[line for line in text.splitlines() if line.startswith("MAP_TIMELINE|id=110|")]
 if len(lines)!=1:raise ValueError("one pinned timeline witness required")
 fields={}
 for cell in lines[0].split("|")[1:]:
  k,_,v=cell.partition("=")
  fields[k]=v
 expected={"lineage":"DEC_ONLY_DIVERGENCE","compat":"C->C->C","jd_tile_diff":"0",
           "jd_parts_diff":"0","jd_event_diff":"3","jd_total":"3",
           "j_sha256":SOURCES["june"]["file_sha256"],
           "d_sha256":SOURCES["dec"]["file_sha256"],
           "p_sha256":SOURCES["june"]["file_sha256"]}
 if any(fields.get(k)!=v for k,v in expected.items()):
  raise ValueError("original three-state map timeline witness differs")
 return fields

def report(june,dec):
 timeline=TIMELINE.read_bytes()
 verify_timeline(timeline.decode("utf-8"))
 if digest(june)!=SOURCES["june"]["file_sha256"] or digest(dec)!=SOURCES["dec"]["file_sha256"]:
  raise ValueError("actual extracted original map hash mismatch")
 result=compare(june,dec)
 return {"schema":"stoneage.map110_archived_2003_original_cell_delta.r32",
         "source_scope":"ARCHIVED_THIRD_PARTY_MAP_EXE_TWO_DATED_SAMPLES_NOT_OFFICIAL_TW10",
         "map_token":ID,"map_original_path":"map/110.DAT",
         "timeline_git_blob":original_git_blob(timeline),
         "source_packages":{k:{"capture":v["capture"],"container_sha256":v["container_sha256"],
                                "original_dat_sha256":v["file_sha256"]} for k,v in SOURCES.items()},
         "result":result,"no_named_map_or_quest_role":True,"no_map_grid_released":True,
         "event_plane_runtime_semantics_unverified":True,"world_coordinates_not_authenticated":True,
         "june_equals_preserved25_by_whole_file_prior_witness_only":True}

def bounded_read(directory):
 results=[]
 for name in ("june","dec"):
  folder=directory/name
  matches=[p for p in folder.rglob("*") if p.is_file() and
       p.name.lower()=="110.dat" and p.parent.name.lower()=="map"]
  if len(matches)!=1:raise ValueError("missing or ambiguous original map/110.DAT in "+name)
  results.append(matches[0].read_bytes())
 return results

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-maps",type=Path,required=True)
 ap.add_argument("--output",type=Path,required=True)
 args=ap.parse_args()
 j,d=bounded_read(args.source_maps)
 obj=report(j,d)
 args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print("R32_DERIVED_JSON_BEGIN")
 print(json.dumps(obj,ensure_ascii=False,sort_keys=True))
 print("R32_DERIVED_JSON_END")
 print("R32_ORIGINAL_SOURCES_VERIFIED_AND_3_CELL_VALUES_DERIVED=PASS")

if __name__=="__main__":main()
