"""O12 provenance gate: native Taiwan-1.0 compiled SFX IDs != soundaddr ordinal.

Only source-derived metadata lives in public Git. Original executable and WAV
payloads must remain private. This module never executes historic game code.
"""
from __future__ import annotations
import argparse, hashlib, json, re, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/recovered/STONEAGE-O12-NATIVE-SOUND-NAMESPACE-R1.json"
RUNTIME_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
TABLE_SHA = "d8d2bee5e424be75b35cc4b8a1ac10d398f7fd53e98035ba6980e9e4dc9b389f"
PAIRS_SHA = "29bcaf29b196e9b0dfdb53de210cb158dc71f82d94ee5be80f032e06f0586119"
LITERAL_PATHS_SHA = "d9358c322f4a9e372e84a3d4cd2ad58d0412d54bae1ac7cea6b32a9e8963197c"
BGM_PATHS_SHA = "775c7feb2ba11a9394579737860f94123f7061e4ee0ba3efef18c02141a81a2b"
UNRESOLVED = (
    "data\\se\\sad_01.wav", "data\\se\\sad_02.wav", "data\\se\\sad_03.wav",
    "data\\se\\sad_04.wav", "data\\se\\sad_05.wav",
    "data\\se\\sak_09a.wav", "data\\se\\sak_09b.wav",
    "data\\se\\sam_24.wav", "data\\se\\sap_01.wav",
    "data\\se\\sap_02.wav", "data\\se\\sap_04.wav",
)

def require(ok, reason):
    if not ok: raise ValueError(reason)

def canonical_sha(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def verify(report):
    require(report["schema"]=="stoneage.o12.tw1_compiled_sfx_number_namespace_source_audit.r1", "schema")
    src=report["original_source"]
    require(src["original_runtime_bytes"]==425984 and src["original_runtime_sha256"]==RUNTIME_SHA,"runtime source SHA")
    require(src["original_sfx_address_table_bytes"]==2873 and src["original_sfx_address_table_sha256"]==TABLE_SHA,"table source SHA")
    require(src["official_sample_scope"]=="ACCEPTED_TW_WAEI_JSS_V1_RETAIL_SA_3_EXE", "version")
    require(src["base_address"]==4194304 and src["static_text_raw_extent"]==[4096,332687], "native section")
    lit=report["compiled_static_names"]
    require(lit["sfx_unique"]==113 and lit["bgm_unique"]==11,"literal counts")
    require(lit["sfx_literal_paths_sha256"]==LITERAL_PATHS_SHA and lit["bgm_literal_paths_sha256"]==BGM_PATHS_SHA,"literal identities")
    idx=report["indexed_sfx"]
    require(idx=={"entry_count":114,"last_contiguous_byte":3695418,"not_in_compiled_static_paths":["sak_98.wav"],
                  "index72":"sam_17.wav","index73":"sam_18.wav","index74":"sam_19.wav"},"indexed table distinct")
    group=report["bounded_native_x86_machine_join"]
    rows=group["verified_pairs"]
    require(group["exact_concrete_number_to_path_pairs"]==102 and len(rows)==102, "verified ID count")
    require(group["all_verified_machine_pairs_sha256"]==PAIRS_SHA and canonical_sha(rows)==PAIRS_SHA, "102 direct machine witnesses")
    require(group["no_guess_for_alternate_codegen"] is True and group["unmatched_static_names_due_to_alternate_codegen"]==list(UNRESOLVED),"11 alternate-codegen boundaries")
    ids=[x["compiled_sound_number"] for x in rows]
    paths=[x["compiled_filepath"] for x in rows]
    require(ids==sorted(set(ids)) and len(set(paths))==102,"unique direct ID/path")
    require(all(set(r)=={"compiled_sound_number","compiled_filepath","instruction_file_offset","stack_sound_id_displacement",
                        "source_string_VA","load_instruction_file_offset","store_instruction_file_offset"} for r in rows),"exact source triple fields")
    require(all(r["compiled_filepath"].startswith("data\\se\\") and 4096 <= r["instruction_file_offset"] < 332687
                and 0x454000<=r["source_string_VA"]<0x466000 for r in rows), "physical source bounds")
    sound={r["compiled_sound_number"]:r for r in rows}
    require([sound[n]["compiled_filepath"] for n in (72,73,74)]==["data\\se\\sae_22.wav","data\\se\\sae_23.wav","data\\se\\sae_24.wav"], "native SFX namespace")
    key=report["key_number_73"]
    require(key["value_as_unsigned_16bit"]==73 and key["compiled_native_sound_number_filepath"]==sound[73]["compiled_filepath"],"73 compiled ID")
    require(key["compiled_source_imm_store_file_offset"]==sound[73]["instruction_file_offset"] and key["compiled_load_file_offset"]==sound[73]["load_instruction_file_offset"]
            and key["compiled_stack_store_file_offset"]==sound[73]["store_instruction_file_offset"],"73 physical offsets")
    require(key["compiled_source_imm_store_sha256"]==KEY_INSTRUCTION_SHA,"73 instruction SHA")
    require(key["address_table_zero_based_73"]=="sam_18.wav" and key["address_table_one_based_73"]=="sam_17.wav", "73 ordinal split")
    require(key["native_compiled_number_namespace_differs_from_address_table_ordinal"] is True, "namespace actually different")
    require(key["frame_word_73_uses_this_compiled_namespace_verified"] is False
        and key["original_frame_word_to_audio_event_selector_found"] is False,"no false event selector")
    prior=report["prior_O11_source_control"]
    require(prior=={"spr_groups":[100250,100251,100252],"verified_same_source_animation_segments":24,
                    "frame_positions":352,"frame_word_73_positions":24,"frame_word_10000_positions":24,"other_zero_positions":304},"O11 lineage")
    require(len(report["negative_scope"])==8 and all(v is False for v in report["negative_scope"].values()),"unproven historic gameplay")
    notes=report["evidence_notes"]
    require(notes=={"source_original_bytes_replayed_locally":True,"objdump_independent_102_machine_triples_passed":True,
        "original_filename_paths_are_identifiers_not_proprietary_media":True,"git_actions_will_verify_only_frozen_derived_source":True,
        "runtime_original_engine_not_executed":True,"same_version_client_scope_yes":True,"frame_sound_word_true_selector_unknown":True},"private vs CI scope")
    require(report["stage_A_partial"]==7 and report["stage_A_open"]==2 and report["stage_B_gated"] is True
        and report["wiki_gated"] is True and report["R79_paused_nonblocking"] is True and report["overall_percent"] is None,"restoration status")
    require(report["next"]=="O13_CROSS_DOMAIN_ORIGINAL_ENTITY_MASTER_OR_NPC_EVENT_INPUT_WITH_QUALIFIED_SAME_SOURCE_ONLY","next")
    return {"native_compiled_sfx_literals":113,"original_address_rows":114,"native_verified_id_paths":102,
            "compiled_73":"sae_23.wav","table_73":"sam_18.wav","pet_trigger_unproven":True}

# Stable byte witness for MOV WORD PTR [ESP+0x1d70],73, known from actual original .text.
KEY_INSTRUCTION_SHA = "9faef18b4098fd5a416b4a9926403d87da3d9ae14386313a4a527f4c5ed11fa1"

def bounded_original_source_check(runtime:bytes,table:bytes):
    """Optional exact original-file validation; GitHub CI never has these inputs."""
    require(len(runtime)==425984 and hashlib.sha256(runtime).hexdigest()==RUNTIME_SHA,"wrong original executable")
    require(len(table)==2873 and hashlib.sha256(table).hexdigest()==TABLE_SHA,"wrong original address table")
    require(hashlib.sha256(runtime[0x42b76:0x42b80]).hexdigest()==KEY_INSTRUCTION_SHA, "original x86 ID73 witness")
    require(runtime[0x641a8:0x641a8+18].decode("ascii")=="data\\se\\sae_23.wav", "original filename literal")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--verify",action="store_true")
    ap.add_argument("--runtime",type=Path)
    ap.add_argument("--table",type=Path)
    args=ap.parse_args()
    if args.runtime or args.table:
        require(args.runtime is not None and args.table is not None,"need both original sources")
        bounded_original_source_check(args.runtime.read_bytes(),args.table.read_bytes())
        print("O12_ORIGINAL_RUNTIME_BOUNDED_MACHINE_REPLAY=PASS")
    print("STONEAGE_O12_SOURCE_ONLY=PASS",json.dumps(verify(json.loads(SOURCE.read_text(encoding="utf-8"))),sort_keys=True))
if __name__=="__main__":main()
