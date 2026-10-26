"""Independent R30 archive: exact public custody of encrypted-only source imagery.

The original reconstructed pixels and their private session key must NOT be in
the public Git tree. The two short-lived Actions archives are input carriers;
only SHA-pinned source-derived numerical/geometry metadata is retained.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw85_r30_preview import plan as rebuild_plan

PLAN_SHA="805e6f1ef0039f48f40c7c6cc46296d1297b8e629617e3ddfdf629e8e1204a09"
SOURCE_SHA="f70b5ce996e2fbf4acb8dfa5103d8729bdbf6d2779df86c2a35bc71768f253e6"
ENC_SHA="c689e21a7b1e699951ec6b3014fcb5934670254dcff739a66e0d5bbd652bb02f"
SOURCE_RUN=40329157425
PREFLIGHT_JOB=121593631715
SOURCE_JOB=121594000184
PLAN_ARTIFACT=12653666487
ENC_ARTIFACT=12654905609
PLAN_ZIP_SHA="81b2ac85c8069d76a6f2048d7bd4df38e0ffeb7032fbcd4115baa12185f9bfe8"
ENC_ARTIFACT_ZIP_SHA="265dffe92a7ed89370f9d45ecb3f97ab0241652c9168e175e5852c8fd19bb554"
SOURCE_HEAD="62fe0f95781358cf7b5cd7a5d238727efc1506a4"


def require(cond,msg):
    if not cond:raise ValueError(msg)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def archive(planpath,sourcepath,cipherpath,envelopepath):
    for path,digest in ((planpath,PLAN_SHA),(sourcepath,SOURCE_SHA),(cipherpath,ENC_SHA)):
        require(sha(path)==digest,"source artifact digest drift: "+str(path))
    expected=rebuild_plan()
    plan=json.loads(Path(planpath).read_bytes())
    require(plan==expected,"source plan must replay full original R28 R29 saved data")
    data=json.loads(Path(sourcepath).read_bytes())
    capsule=json.loads(Path(envelopepath).read_bytes())
    require(capsule["schema"]=="stoneage.r30.session_public_key_aes256gcm_encrypted_private_image.r1"
            and capsule["ciphertext_sha256"]==ENC_SHA
            and capsule["ciphertext_bytes"]==Path(cipherpath).stat().st_size
            and capsule["private_key_written_to_ci"] is False
            and capsule["public_source_files_or_unencrypted_original_art_in_artifact"] is False,
            "private preview incorrectly exposed")
    require(capsule["plaintext_zip_sha256"]==
            "1713abc369bb00d59d77d27f27397daebe9d051f40c46f0521c50180c85383c0",
            "private sampled asset capsule source provenance changed")
    require(data["schema"]=="stoneage.tw85_original_rd_private_gray_sample.r30"
            and data["source_claim"]==expected["source_claim"]
            and data["sample"]==expected["sample"],"same-origin original sample changed")
    require(data["historical_palette_rgb_verified"] is False and
            data["named_pet_or_avatar_verified"] is False and
            data["gameplay_sound_event_verified"] is False and
            data["original_game_rendered_or_executed"] is False,
            "source visual observation overpromoted to real game runtime")
    require(len(data["frames"])==8,"sample frame membership changed")
    for position,(actual,pin) in enumerate(zip(data["frames"],plan["sample"]["sample_frames"])):
        require(actual["index"]==pin["index_in_animation"]==position
                and actual["bitmapno"]==pin["bitmapno"]
                and actual["width"]==pin["width"] and actual["height"]==pin["height"]
                and actual["source_record_sha256"]==pin["native_adrn_record_sha256"]
                and actual["source_RD_sha256"]==pin["rd_block_sha256"]
                and actual["original_sprite_x"]==pin["pos_x"]
                and actual["original_sprite_y"]==pin["pos_y"]
                and actual["raw_sound_word"]==pin["raw_sound_word"],
                "original private visual decoded sample does not trace to pinned 4-file indices")
        require(len(actual["source_palette_index_sha256"])==64
                and len(actual["private_png_sha256"])==64
                and actual["private_png_name"]==f"frame_{position:02d}_bmp_{pin['bitmapno']}.png",
                "private PNG frame evidence digest/name invalid")
    return {
     "schema":"stoneage.tw85_r30_source_private_visual_public_custody.r1",
     "status":"SOURCE_AND_PRIVATE_DECRYPTED_VISUAL_MATERIAL_ACCEPTED",
     "source_head":SOURCE_HEAD,
     "source_run":SOURCE_RUN,"preflight_job":PREFLIGHT_JOB,"source_job":SOURCE_JOB,
     "source_artifacts":{
      "numeric_plan":{"id":PLAN_ARTIFACT,"zip_sha256_independently_checked":PLAN_ZIP_SHA,
                      "json_bytes":Path(planpath).stat().st_size,"json_sha256":PLAN_SHA},
      "encrypted_actual_pixel_package":{"id":ENC_ARTIFACT,
           "zip_sha256_independently_checked":ENC_ARTIFACT_ZIP_SHA,
           "derived_original_pixel_manifest_bytes":Path(sourcepath).stat().st_size,
           "derived_original_pixel_manifest_sha256":SOURCE_SHA,
           "AES256_GCM_ciphertext_sha256":ENC_SHA,
           "original_private_preview_encrypted":True,
           "plaintext_zip_sha256_seen_only_during_ephemeral_local_private_decryption":
              capsule["plaintext_zip_sha256"]}
     },
     "original_sample_source":plan["source_claim"],
     "group_index":plan["sample"]["source_group_index"],
     "numeric_spr_group":plan["sample"]["original_spr_no"],
     "numeric_direction":plan["sample"]["original_direction_numeric"],
     "numeric_action":plan["sample"]["original_action_numeric"],
     "original_duration_word":plan["sample"]["original_duration_word"],
     "actual_original_rd_decoded_count":len(data["frames"]),
     "original_bitmapnos":[x["bitmapno"] for x in data["frames"]],
     "original_RD_sha256":[x["source_RD_sha256"] for x in data["frames"]],
     "private_grayscale_png_sha256":[x["private_png_sha256"] for x in data["frames"]],
     "source_index_hash_all_8_exact":True,
     "user_rendered_visual_identification":None,
     "assistant_private_source_grayscale_visual_inspection":
        "eight distinct gray-index sprite poses observed in private decrypted contact sheet; no named identity certified",
     "source_bytes_retained_in_public_repo":0,
     "source_client_executables_or_installer_published":False,
     "private_png_publicly_uploaded":False,
     "community_claimed_build_authenticated_as_clean_official":False,
     "actual_historical_RGB_palette_certified":False,
     "client_original_program_executed":False,
     "pet_species_or_npc_identity_verified":False,
     "original_sounds_heard":False,
     "stage_a":"7_PARTIAL_2_OPEN","stage_b_wiki":"GATED",
     "r79":"PAUSED_NON_BLOCKING","overall_progress_percent":None,
     "next":"WORLD_ENTITY_NAMED_ORIGINAL_SOURCE_31_OR_BOUNDED_22_DOMAIN_MATERIAL_AFTER_VISUAL_PROOF"
    }


def main():
    a=argparse.ArgumentParser()
    for flag in ("plan","source","cipher","envelope","receipt"):
        a.add_argument("--"+flag,required=True,type=Path)
    x=a.parse_args()
    result=archive(x.plan,x.source,x.cipher,x.envelope)
    x.receipt.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":"PASS","group_index":result["group_index"],
                      "original_RD_blocks":result["actual_original_rd_decoded_count"],
                      "raw_bitmap_pixels_in_public_repo":result["source_bytes_retained_in_public_repo"]},sort_keys=True))


if __name__=="__main__":main()
