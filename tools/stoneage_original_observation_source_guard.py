"""Independent R1 proof of actual TW1 image-index and WAV source, no pixels stored."""
from __future__ import annotations
import json
from pathlib import Path
from tools.stoneage_original_observation_lab import PINNED, pinned_wav_inventory

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-TW10-ORIGINAL-OBSERVATION-P1-SOURCE-R1.json"
SAMPLES={
    5846:{"dimensions":(52,72),"rdsha":"f4880a27d5aa6fb617a308703ea81bd6db3b67fa7a77436183e0b24667ce1911",
          "decoded":"701a3bb13ec61eadc2531e770d90b1b8744abb682327396eb98e6b351ac0769e",
          "png":"14378bfb36388dd4c96b173966126e9f7dcb285b5d82199fcbbd5458e42a763c"},
    5847:{"dimensions":(40,72),"rdsha":"9575da7cf85d7324def2e7502493d229f50bd07514f2933d3352029e1ea7101f",
          "decoded":"e4efb9a660aa96ba266a6d6229e156511d6287b476e8b84fd267fedd537c0bc1",
          "png":"056bf10474ca155bd7ae6c032795b21ae71107176247fc8e1b4e9e85e8e9b8ac"},
}

def need(test,message):
    if not test: raise AssertionError(message)

def verify(report=None):
    d=json.loads(REPORT.read_text(encoding="utf-8")) if report is None else report
    need(d["schema"]=="stoneage.original_observation_lab.tw10_actual_source_r1","schema")
    need(d["work_package"]=="ORIGINAL-GAME-OBSERVATION-LAB-P1","work package")
    j=d["source_job"]
    need(j["run_id"]==40206034214 and j["job_id"]==121207050316,"raw source job")
    need(j["head_sha"]=="898dfea3cd33ca3f99afc94f4c23f29b80daf203" and j["conclusion"]=="success","source SHA and result")
    need(d["source_qualification"]=="VERIFIED_ACCEPTED_TW10_RETAIL_ORIGINAL_BYTES","source identity")
    original=json.loads((ROOT/"research/recovered/STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json").read_text(encoding="utf-8"))
    by_id={x["bitmapno"]:x for x in original["rows"]}
    need(len(original["rows"])==101 and set(SAMPLES).issubset(by_id),"original resource prior custody")
    decoded=d["original_image_preview_records"]
    need(len(decoded)==2 and {x["record"]["bitmapno"] for x in decoded}==set(SAMPLES),"bitmap sample census")
    for r in decoded:
        row=r["record"]; key=row["bitmapno"]; expected=SAMPLES[key]; prev=by_id[key]
        need(r["schema"]=="stoneage.original_observation_lab.bitmap_v1","image source schema")
        need(r["source_claim"]=="ORIGINAL_TW10_RD_BYTES_DECODED_TO_PALETTE_INDICES_ONLY","palette claim")
        need(row["index"]==key,"selected original record index")
        need((row["width"],row["height"])==expected["dimensions"],"width height")
        need((prev["width"],prev["height"])==expected["dimensions"],"prior original dims")
        need(row["size"]==prev["encoded_bytes"],"previous original source block size")
        need(r["original_rd_block_sha256"]==expected["rdsha"]==prev["rd_block_sha256"],"independent original RD SHA")
        need(r["decoded_palette_index_sha256"]==expected["decoded"],"actual decoded pixels")
        need(r["preview_png_sha256"]==expected["png"],"actual transient preview hash")
        need(r["source_sha256"]["adrn_1.bin"]==PINNED["adrn_1.bin"][1],"source ADRN hash")
        need(r["source_sha256"]["real_1.bin"]==PINNED["real_1.bin"][1],"source REAL hash")
        need(r["rd_flag"]==1 and r["original_colors_reproduced"] is False,"historic palette falsely inferred")
        need(r["original_client_executed"] is False and r["historical_gameplay_screenshot"] is False,"game screenshot falsely claimed")
        need(r["pet_species"] is None and r["npc_name"] is None,"named identity falsely added")
        need(r["server_entity_binding_verified"] is False,"original entity binding falsely claimed")
    wav=d["original_audio_structural_record"]
    need(wav["schema"]=="stoneage.original_observation_lab.wav_v1","wav schema")
    need(wav["original_path"]=="StoneAge/data/se/sas_20.wav","wav name")
    need(wav["original_sha256"]==pinned_wav_inventory()[wav["original_path"]][1],"original sound byte pin")
    need(wav["format"]["sample_rate_hz"]==11025 and wav["format"]["frames"]==1939,"sound metadata witness")
    need(wav["format"]["channels"]==1 and wav["format"]["sample_width_bytes"]==2,"sound format witness")
    need(wav["audio_played_or_heard_by_assistant"] is False,"invents sound listening")
    need(wav["in_game_sound_event_verified"] is False,"invents event")
    for k in ("original_executable_run_observed","actual_game_frame_captured","preview_is_original_color","images_actually_previewed_by_assistant","audio_actually_listened_by_assistant","original_commercial_pixels_or_audio_committed_to_public_git","original_server_world_entered"):
        need(d[k] is False,"false historical completion: "+k)
    need(d["temporary_original_files_cleaned"] is True,"originals not purged")
    need(d["verified_link_to_original_named_npc_pet_quest"]==0,"unproven old entities promoted")
    need(d["overall_restoration_percent"] is None,"invented percentage")
    return True

if __name__=="__main__":
    verify()
    print("OBSERVATION_P1_TWO_ACTUAL_TW10_RD_IMAGES_AND_WAV_SOURCE_CUSTODY=PASS")
    print("AUTHENTIC_PALETTE_CLIENT_BOOT_SERVER_GAMEPLAY=OPEN")
