"""R30 offline original-source and private-custody acceptance (no resampling original art).

Recomputes the bounded original group selection from the pinned complete
source-derived R28/R06 tables, verifies all 8 original RD hashes and custody.
Runs on public main without original packages or session private images.
"""
import hashlib
import json
from pathlib import Path

from tools.stoneage_tw85_r30_preview import plan as rebuild_plan
from tools.stoneage_tw85_r30_archive import (
    PLAN_SHA,SOURCE_SHA,ENC_SHA,SOURCE_RUN,SOURCE_JOB,PLAN_ARTIFACT,ENC_ARTIFACT
)

BASE=Path(__file__).resolve().parents[1]/"research/recovered/tw85-rd-private-r30"


def need(ok,why):
    if not ok:raise ValueError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay():
    p=BASE/"PLAN-R30.json";s=BASE/"SOURCE-R30.json";c=BASE/"R30-PUBLIC-CUSTODY.json"
    need(digest(p)==PLAN_SHA and digest(s)==SOURCE_SHA,"original public result bytes not immutable")
    plan=json.loads(p.read_bytes());source=json.loads(s.read_bytes());receipt=json.loads(c.read_bytes())
    need(plan==rebuild_plan(),"pinned R28/R06/R29 full original source selection replay differs")
    need(source["schema"]=="stoneage.tw85_original_rd_private_gray_sample.r30"
         and source["sample"]==plan["sample"],"R30 actual original source sample mismatched")
    frames=source["frames"]
    need(len(frames)==8 and len(plan["sample"]["sample_frames"])==8,"8 original visual RD positions not conserved")
    for k,(a,b) in enumerate(zip(frames,plan["sample"]["sample_frames"])):
        need(a["index"]==b["index_in_animation"]==k
             and a["bitmapno"]==b["bitmapno"]
             and a["source_record_sha256"]==b["native_adrn_record_sha256"]
             and a["source_RD_sha256"]==b["rd_block_sha256"]
             and (a["width"],a["height"])==(b["width"],b["height"])
             and a["original_sprite_x"]==b["pos_x"]
             and a["original_sprite_y"]==b["pos_y"],"private original position/bitmap/hash diverged")
        need(a["private_png_name"]==f"frame_{k:02d}_bmp_{b['bitmapno']}.png"
             and len(a["private_png_sha256"])==64
             and len(a["source_palette_index_sha256"])==64,"decoded RGB/index provenance drift")
    need(receipt["schema"]=="stoneage.tw85_r30_source_private_visual_public_custody.r1"
         and receipt["source_run"]==SOURCE_RUN and receipt["source_job"]==SOURCE_JOB
         and receipt["source_artifacts"]["numeric_plan"]["id"]==PLAN_ARTIFACT
         and receipt["source_artifacts"]["encrypted_actual_pixel_package"]["id"]==ENC_ARTIFACT
         and receipt["source_artifacts"]["numeric_plan"]["json_sha256"]==PLAN_SHA
         and receipt["source_artifacts"]["encrypted_actual_pixel_package"]["derived_original_pixel_manifest_sha256"]==SOURCE_SHA
         and receipt["source_artifacts"]["encrypted_actual_pixel_package"]["AES256_GCM_ciphertext_sha256"]==ENC_SHA
         and receipt["actual_original_rd_decoded_count"]==8
         and receipt["original_bitmapnos"]==[x["bitmapno"] for x in frames]
         and receipt["original_RD_sha256"]==[x["source_RD_sha256"] for x in frames]
         and receipt["private_grayscale_png_sha256"]==[x["private_png_sha256"] for x in frames],
         "permanent original-source Actions custody drift")
    for key in ("community_claimed_build_authenticated_as_clean_official",
                "actual_historical_RGB_palette_certified","client_original_program_executed",
                "pet_species_or_npc_identity_verified","original_sounds_heard",
                "private_png_publicly_uploaded","source_client_executables_or_installer_published"):
        need(receipt[key] is False,"unsupported original screenshot or identity promotion: "+key)
    need(receipt["source_bytes_retained_in_public_repo"]==0
         and receipt["overall_progress_percent"] is None
         and receipt["stage_a"]=="7_PARTIAL_2_OPEN"
         and receipt["stage_b_wiki"]=="GATED"
         and receipt["r79"]=="PAUSED_NON_BLOCKING","project status or source ownership altered")
    need(sorted(x.name for x in BASE.iterdir())==["PLAN-R30.json","R30-PUBLIC-CUSTODY.json","SOURCE-R30.json"],
         "private original image copied into public tree")
    return {"status":"PASS","actual_decoded_index_images":8,
      "source_custody_source_run":SOURCE_RUN,"numeric_original_group":plan["sample"]["original_spr_no"],
      "true_palette_verified":False,"named_creature_identity":None,
      "session_private_images_or_game_program_committed":False}


if __name__=="__main__":
    print(json.dumps(replay(),sort_keys=True))
