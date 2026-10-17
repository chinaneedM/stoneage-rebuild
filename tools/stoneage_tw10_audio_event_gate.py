"""Bounded real Taiwan-v1 audio playback import and original WAV index facts.

Authenticates the original sa_3.exe byte SHA, traverses direct imported-call
or jump-thunk references and preserves only metadata. Does not claim that
an API import identifies music for a village, battle, UI or pet action.
"""
from __future__ import annotations
import argparse, hashlib, json, tempfile
from collections import Counter
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_INVALID
from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import image_layout, offset_to_rva
from tools.stoneage_pet_asset_growth_catalog import ROOT, gitblob, require

DATASET=ROOT/"research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt"
DATASET_BLOB="094becbc92397ee8abf72a014deffffabc97a316"
RUNTIME_REPORT=ROOT/"research/recovered/STONEAGE-TW10-RUNTIME-SOUND-R1.txt"
RUNTIME_REPORT_BLOB="0054c8c0c2a34652caec4ab89feac5bf821d75f7"
SHA_RUNTIME="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
TARGET_DLLS=("DSOUND.dll","WINMM.dll")
CANDIDATE_LITERALS={
  "container":b"sound_1.bin",
  "container_table":b"soundaddr_1.txt",
  "sfx_directory":b"data\\se\\",
  "bgm_directory":b"data\\bgm\\",
  "bgm_prefix":b"sabgm_",
}

def audio_catalog():
    raw=DATASET.read_bytes()
    require(gitblob(raw)==DATASET_BLOB,"original TW1 audio catalog drift")
    runtime=RUNTIME_REPORT.read_bytes()
    require(gitblob(runtime)==RUNTIME_REPORT_BLOB,"prior original TW1 import report drift")
    lines=raw.decode("utf-8").splitlines()
    index=[]
    count=Counter()
    for line in lines:
        if "|" not in line:continue
        parts=line.split("|")
        cat=parts[0]
        count[cat]+=1
        if cat=="INDEXED":
            row=dict(s.split("=",1) for s in parts[1:] if "=" in s)
            index.append(row)
    require(count["INDEXED"]==114 and count["UNINDEXED_SFX"]==2 and count["BGM"]==11,"audio count drift")
    require(len(index)==114,"missing sound-container index rows")
    expected_offset=0
    variants=Counter()
    for i,row in enumerate(index):
        require(int(row["index"])==i,"index sequence")
        require(int(row["offset"])==expected_offset,"sound-index byte discontinuity")
        expected_offset+=int(row["size"])
        variants[row["relation"]]+=1
    require(expected_offset==3695418,"original audio container extent drift")
    require(variants==Counter({"exact_file":107,"variant_same_pcm":1,"variant_pcm_diff":6}),"original audio variants drift")
    old=runtime.decode("utf-8").splitlines()
    imports=[line for line in old if line.startswith("PE_IMPORT|label=sa_3.exe|")]
    pinned={(row.split("|dll=",1)[1].split("|",1)[0],row.split("|name=",1)[1]) for row in imports}
    require({("DSOUND.dll","#1"),("WINMM.dll","mciSendCommandA"),("WINMM.dll","mmioOpenA")}<=pinned,
            "prior original audio IAT witnesses drift")
    return {
      "indexed_sfx":114,"loose_sfx":116,"loose_bgm":11,
      "original_container_bytes":expected_offset,
      "identical_full_wave_pairs":variants["exact_file"],
      "same_pcm_different_wrapper":variants["variant_same_pcm"],
      "different_pcm_pairs":variants["variant_pcm_diff"],
      "unindexed_sfx":2,
      "metadata_variants":[{"index":int(r["index"]),"name":r["name"],"comparison":r["relation"]}
                           for r in index if r["relation"]!="exact_file"],
      "old_preexisting_audio_imports":[{"dll":dll,"name":name} for dll,name in sorted(pinned) if dll in TARGET_DLLS],
    }

def bounded_probe_runtime(runtime:Path):
    raw=runtime.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SHA_RUNTIME,"not accepted TW1 sa_3.exe")
    data,pe,base,sections,imports=image_layout(runtime)
    selected={va:(dll,fn) for va,(dll,fn) in imports.items() if dll in TARGET_DLLS}
    require(len(selected)==7,"original audio API import-count changed")
    sec=next(s for s in sections if s["name"]==".text")
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail=True
    md.skipdata=True
    instructions=list(md.disasm(data[sec["raw"]:sec["raw"]+sec["raw_size"]],base+sec["rva"]))
    import_sites=[]
    direct_control=[]
    for ins in instructions:
        if ins.mnemonic not in ("call","jmp") or not ins.operands:
            continue
        op=ins.operands[0]
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_INVALID and op.mem.index==X86_REG_INVALID:
            address=int(op.mem.disp)&0xffffffff
            if address in selected:
                dll,func=selected[address]
                import_sites.append({"rva":ins.address-base,"mnemonic":ins.mnemonic,
                    "import_dll":dll,"import_function":func,"iat_rva":address-base})
        elif op.type==X86_OP_IMM:
            direct_control.append((ins.address-base,int(op.imm)&0xffffffff))
    import_sites.sort(key=lambda x:(x["rva"],x["iat_rva"]))
    # Calls to an IAT trampoline can be verified; this does not identify events.
    thunks={base+item["rva"]:item for item in import_sites if item["mnemonic"]=="jmp"}
    forward=[]
    for src,target in direct_control:
        if target in thunks:
            item=thunks[target]
            forward.append({"caller_rva":src,"thunk_rva":item["rva"],
                "import_dll":item["import_dll"],"import_function":item["import_function"]})
    forward.sort(key=lambda x:(x["caller_rva"],x["thunk_rva"]))
    needles=[]
    low=raw.lower()
    for key,needle in CANDIDATE_LITERALS.items():
        pos=0
        occurrences=[]
        while True:
            off=low.find(needle.lower(),pos)
            if off<0:break
            rv,secname=offset_to_rva(sections,off)
            occurrences.append({"file_offset":off,"rva":rv,"section":secname})
            pos=off+1
        needles.append({"key":key,"literal_present":bool(occurrences),
             "occurrences":occurrences[:12],"truncated":len(occurrences)>12})
    groups=Counter((x["import_dll"],x["import_function"],x["mnemonic"]) for x in import_sites)
    return {
       "original_runtime_sha256":SHA_RUNTIME,"runtime_size":len(raw),
       "image_base":base,"text_rva":sec["rva"],
       "compiled_imported_audio_apis":[{"dll":dll,"name":fn,"iat_rva":addr-base}
                                      for addr,(dll,fn) in sorted(selected.items())],
       "native_import_use_sites":import_sites[:100],
       "native_import_use_site_count":len(import_sites),
       "import_uses_truncated":len(import_sites)>100,
       "native_import_group_counts":[{"dll":a,"name":b,"mnemonic":m,"count":n}
                 for (a,b,m),n in sorted(groups.items())],
       "direct_callers_of_audio_import_thunks":forward[:200],
       "direct_callers_of_audio_import_thunks_total":len(forward),
       "direct_caller_records_truncated":len(forward)>200,
       "audio_filename_literals":needles,
       "compiled_import_is_verified_scene_or_event_selector":False,
       "exact_playback_call_argument_values_observed":False,
       "original_game_player_audio_event_trace_recorded":False,
       "original_sfx_name_equals_trigger_identity_certified":False
    }

def run(disc):
    catalog=audio_catalog()
    image,rows,layout,joliet=find_rows(disc)
    try:
        matches=[r for r in rows if r["path"]=="StoneAge/sa_3.exe" and not r["is_dir"]]
        require(len(matches)==1,"not exactly one accepted runtime in original disc")
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"sa_3.exe"
            extract_row(image,matches[0],path)
            runtime=bounded_probe_runtime(path)
    finally:
        image.close()
    require(runtime["original_runtime_sha256"]==SHA_RUNTIME,"source mismatch")
    return {
      "schema":"stoneage.tw10_audio_event_original_callsite_gate.r1",
      "task":"TW10-AUDIO-EVENT-SOURCE-GATE-01",
      "original_witness":"ACCEPTED_TAIWAN_V1_0_RETAIL_RUNTIME_AND_AUDIO_CATALOG",
      "original_audio_catalog_blob":DATASET_BLOB,
      "original_runtime_import_report_blob":RUNTIME_REPORT_BLOB,
      "audio_assets":catalog,
      "compiled_audio_api_callsite_audit":runtime,
      "source_evidence":"V1_DIRECT_CALLS_AND_ORIGINAL_WAVE_METADATA",
      "original_audio_event_to_track_binding_certified":False,
      "gameplay_trigger_to_sound_file_or_bgm_selector_certified":False,
      "specific_original_village_music_attributed":False,
      "any_pet_sound_species_identity_certified":False,
      "original_audio_bytes_added_to_repo":False,
      "source_limited_nonproduction":True,
      "original_game_restoration_complete":False,
      "next":"PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-03"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--disc",type=Path,required=True)
    parser.add_argument("--write",type=Path)
    args=parser.parse_args()
    report=run(args.disc)
    if args.write:
        args.write.parent.mkdir(parents=True,exist_ok=True)
        args.write.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("TW10_AUDIO_CALLSITE_JSON="+json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))
if __name__=="__main__":main()
