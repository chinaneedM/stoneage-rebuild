"""INTEGRATION57: source-qualified real mixed25 NPC/map/action0 RD join, negative historical boundaries."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT_PATH=ROOT/"research/recovered/STONEAGE-INTEGRATION57-GIIRU-TWO-TRIBES-31205-ORIGINAL-RD-SOURCE-R1.json"

def git_blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\\0"+raw).hexdigest()

class TestIntegration57(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        cls.source={}
        for name,entry in cls.r["qualified_input_git_blobs"].items():
            raw=(ROOT/entry["path"]).read_bytes()
            assert git_blob_sha(raw)==entry["sha"],"source Git blob changed: "+name
            cls.source[name]=json.loads(raw)

    def test_unmodified_historical_current_full_blob(self):
        c=self.r["preserved_original_current"]
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(git_blob_sha(raw),c["blob_sha"])
        self.assertFalse(c["edited"])

    def test_same_preserved_source_qualification_not_official_build(self):
        r=self.r
        self.assertEqual(r["source_class"],"PRESERVED_MIXED25_COMMUNITY_MIXED_CARRIER_NOT_AUTHENTICATED_OFFICIAL_SAME_DEPLOYMENT")
        self.assertEqual(r["original_parent_RAR_sha256"],self.source["char05"]["original_RAR_sha256"])
        self.assertEqual(self.source["quest11"]["private_source_zip_sha256"],self.source["char05"]["original_NPC_ZIP_sha256"])
        self.assertEqual(r["private_original_replay"]["original_scene13_private_zip"]["sha256"],self.source["char05"]["original_SCENE13_private_ZIP_sha256"])
        self.assertEqual(r["module_path"]["region_and_island"],"UNKNOWN")

    def test_original_31205_DAT_and_map_points(self):
        r=self.r
        q=self.source["quest11"]
        original=next(x for x in q["source_map_observations"] if x["floor"]==31205)
        self.assertEqual(r["exact_qualified_mixed25_source_files"]["map_31205"],{
            "floor":31205, "source_DAT_sha256":original["source_DAT_sha256"],
            "source_DAT_bytes":original["source_DAT_bytes"],
            "geometry":original["geometry"],
            "prior_source_image_sha256":original["marked_thumbnail_sha256"],
            "actual_original_three_plane_cell_reads":2,
            "source_points":original["source_points"]
        })
        self.assertEqual((original["source_DAT_bytes"],original["geometry"]),(3758,[25,25]))

    def test_exact_two_original_CREATE_source_blocks(self):
        q=self.source["quest11"]
        actual=self.r["exact_two_source_creates_with_old_original_sprite_graphics"]
        self.assertEqual([x["source_create_ordinal"] for x in actual],[2,5])
        self.assertEqual([x["source_original_NPC_CREATE_block"]["graphic_alias"] for x in actual],[100250,100252])
        f=next(x for x in q["source_files"] if x["path"]=="giiru/event/garunaev1.create")
        self.assertEqual(self.r["exact_qualified_mixed25_source_files"]["source_create_file"],f)
        for row in actual:
            source=next(x for x in q["source_creates"] if x["ordinal"]==row["source_create_ordinal"])
            self.assertEqual(row["source_original_NPC_CREATE_block"],source)
            self.assertEqual(source["floor"],31205)
            self.assertEqual(source["borncorner_raw"][:2],[12,11] if source["ordinal"]==2 else [12,12])

    def test_exact_native_three_u16_source_cell_values(self):
        q=self.source["quest11"]
        map_=next(x for x in q["source_map_observations"] if x["floor"]==31205)
        for b in self.r["exact_two_source_creates_with_old_original_sprite_graphics"]:
            n=b["source_create_ordinal"]
            item=next(x for x in map_["source_points"] if x["source_create_ordinal_or_target"]==n)
            self.assertEqual(b["original_DAT_cell_u16_source_order"],item["original_three_u16_values"])
        self.assertEqual([x["original_DAT_cell_u16_source_order"] for x in self.r["exact_two_source_creates_with_old_original_sprite_graphics"]],[[4015,0,49152],[4003,0,49152]])

    def test_original_script_byte_identifiers_and_segments(self):
        q=self.source["quest11"]
        for b,expected in zip(self.r["exact_two_source_creates_with_old_original_sprite_graphics"],(13,15)):
            src=b["source_script"]
            original=next(x for x in q["source_event_scripts"] if x["path"]==src["path"])
            self.assertEqual(src["sha256"],original["sha256"])
            self.assertEqual(src["prior_source_TYPE_segments"],len(original["events"]))
            self.assertEqual(len(original["events"]),expected)
            self.assertEqual(b["source_original_NPC_CREATE_block"]["parameter_references"][0][0],src["path"])

    def test_original_SPR_source_segment_reused_not_promoted(self):
        s=self.source["scene13"]
        c=self.source["char05"]
        for b in self.r["exact_two_source_creates_with_old_original_sprite_graphics"]:
            x=b["same_preserved_RAR_original_SPR"]
            old=next(g for g in s["groups"] if g["graphic"]==x["graphic"])
            prior=next(g for g in c["prior_original_SPR_groups"] if g["spr_no"]==x["graphic"])
            self.assertEqual(x["group_index"],old["group_index"])
            self.assertEqual(x["full_segment_sha256"],old["full_segment_sha256"])
            self.assertEqual(x["full_segment_sha256"],prior["full_segment_sha256"])
            self.assertEqual(x["source_action_code"],0)
            self.assertEqual(x["source_directions"],list(range(8)))

    def test_preserve_original_280_frame_positions_with_repeats(self):
        s=self.source["scene13"]
        total=0
        for b in self.r["exact_two_source_creates_with_old_original_sprite_graphics"]:
            g=b["same_preserved_RAR_original_SPR"]
            original=next(x for x in s["groups"] if x["graphic"]==g["graphic"])
            self.assertEqual(len(g["original_direction_sequence_bitmaps"]),8)
            self.assertEqual(g["source_frame_positions"],sum(len(x["frames"]) for x in original["animations"]))
            for actual,old in zip(g["original_direction_sequence_bitmaps"],original["animations"]):
                self.assertEqual(actual["direction"],old["direction"])
                self.assertEqual(actual["duration_word_uninterpreted"],old["duration_word"])
                self.assertEqual(actual["bitmap_positions_preserving_repeats"],[x[0] for x in old["frames"]])
            total+=g["source_frame_positions"]
        self.assertEqual(total,280)

    def test_all_144_actual_replayed_original_RD_PNG_RGBA_receipts(self):
        s=self.source["scene13"]
        lookup={x["bitmapno"]:x for x in s["bitmaps"]}
        manifest=[]
        counts=[]
        for b in self.r["exact_two_source_creates_with_old_original_sprite_graphics"]:
            g=b["same_preserved_RAR_original_SPR"]["graphic"]
            rows=b["reused_original_RD_bitmaps_source_sha_rows"]
            original=next(x for x in s["groups"] if x["graphic"]==g)
            ids=sorted(set(frame[0] for a in original["animations"] for frame in a["frames"]))
            self.assertEqual([x[0] for x in rows],ids)
            for row in rows:
                bm,rd,png,rgba,width,height,xoff,yoff=row
                old=lookup[bm]
                self.assertEqual([rd,png,rgba,width,height,xoff,yoff],[old["RD_sha256"],old["PNG_sha256"],old["candidate_RGBA_sha256"],old["width"],old["height"],old["xoff"],old["yoff"]])
                manifest.append({"graphic":g,"bitmap":bm,"source_png_sha256":png,"source_RD_sha256":rd,"rgba_sha256":rgba,"width":width,"height":height,"xoff":xoff,"yoff":yoff})
            counts.append(len(rows))
        self.assertEqual(counts,[64,80])
        digest=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()
        self.assertEqual(digest,self.r["private_144_bitmap_manifest_sha256"])

    def test_private_archive_provenance_and_no_public_images(self):
        q=self.r["private_original_replay"]
        self.assertEqual((q["original_quest11_private_zip"]["bytes"],q["original_quest11_private_zip"]["verified_CRC_members"]),(264869,56))
        self.assertEqual((q["original_scene13_private_zip"]["bytes"],q["original_scene13_private_zip"]["verified_CRC_members"]),(975186,6))
        p=q["integration57_private_zip"]
        self.assertEqual((p["bytes"],p["verified_CRC_members"],p["private_source_PNG_and_RD_replay"]),(869340,297,144))
        self.assertTrue(p["independent_library_download_and_SHA_CRC_replay"])
        self.assertEqual(p["sha256"],"f43c0bd3a7ff16a2a580ec9a7d024bceb58ab20e31175618a9f174b727306a99")
        self.assertTrue(p["modern_viewer"]["chromium_16_animations_selection_image_loaded"])
        self.assertEqual((p["modern_viewer"]["js_errors"],p["modern_viewer"]["external_network_requests"]),(0,0))
        self.assertEqual(self.r["source_counts"]["published_original_proprietary_assets"],0)

    def test_historical_negative_limits_and_stage_A(self):
        c=self.r["source_counts"]
        self.assertEqual((c["original_NPC_create_blocks_newly_joined_to_same_carrier_original_RD"],c["original_31205_DAT_reopened_count"],c["original_ordered_frame_occurrences"],c["source_distinct_bitmaps"]),(2,1,280,144))
        for k in ("new_original_RD_decodes_this_round","native_original_client_execution","native_original_server_execution","native_original_NPC_render_or_battle_verified","first_party_TW1_same_deployment_identity_verified","published_original_proprietary_assets"):
            self.assertEqual(c[k],0)
        self.assertGreaterEqual(len(self.r["negative_qualification"]),7)
        self.assertEqual(self.r["status"]["stage_b"],"GATED")
        self.assertIsNone(self.r["status"]["overall_percent"])

if __name__=="__main__":
    unittest.main()
