"""Public-only Stage A evidence gates for INTEGRATION20.

These tests replay source-derived numerical/hash claims. They intentionally do NOT
claim to execute the private original DAT, PNG, RAR or historical client.
"""
from pathlib import Path
import copy
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
NAME = "STONEAGE-INTEGRATION20-TWO-PET-ROOMS-ORIGINAL-SOURCE-R1.json"
PINS = {
    "map09": ("STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json", "137580e7c25aadf3d679b6ebfb5080b79912cc4f"),
    "integration19": ("STONEAGE-INTEGRATION19-THREE-PET-SERVICES-SOURCE-R1.json", "8a3eccfb28c266c36c4ba764807e6b3ef64de620"),
    "integration17": ("STONEAGE-INTEGRATION17-THREE-PET-ROOMS-SOURCE-R1.json", "e716f01bbf7d08be2e13654909282a198f5334dd"),
    "map04": ("STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json", "1ef8c004179128ea44ffa4fb4259748bc8c83911"),
}

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def verified(name, blob):
    raw = (REC / name).read_bytes()
    assert git_blob(raw) == blob, (name, "upstream blob changed")
    return json.loads(raw)

def consistent(q, map09, prior, gfx, map04):
    if q["upstream_git_blobs"] != {k: pin[1] for k, pin in PINS.items()}:
        return False
    row_index = {r[0]: r for r in map04["per_floor_source_rows"]}
    qualified = {"3303": (101, 44, 256), "3403": (162, 45, 32)}
    for key, (draws, aliases, changed) in qualified.items():
        value = q["rooms"][key]
        direct = map09["maps"][key]
        upstream = next(x for x in prior["rooms"] if x["floor"] == int(key))
        if value["original_DAT"]["sha256"] != direct["source_sha256"]:
            return False
        if row_index[key+".dat"][2] != direct["source_sha256"]:
            return False
        if value["original_DAT"]["bytes"] != row_index[key+".dat"][1]:
            return False
        frame = value["candidate_canvas"]
        if frame["full_RGBA_sha256"] != direct["frame_RGBA_sha256"]:
            return False
        if (frame["original_bitmap_candidate_placements"], frame["distinct_source_tile_aliases"]) != (draws, aliases):
            return False
        if value["original_server_LS2MAP"]["changed_cells_server_vs_client"] != [0, changed]:
            return False
        if len(value["services"]) != 2 or len(upstream["services"]) != 2:
            return False
        for actual, before in zip(value["services"], upstream["services"]):
            if (actual["create_ordinal"],actual["create_sha256"],actual["graphic_alias"],actual["spawn_xy"],actual["parameter_source_sha256"]) != (
                before["create_ordinal"],before["create_sha256"],before["graphic"],before["xy"],before["parameter_sha256"]):
                return False
        source_edges = [e for e in prior["directed_warp_edges"] if int(key) in (e["start"][0],e["target"][0])]
        edges = value["original_directed_edges"]
        if len(edges) != len(source_edges):
            return False
        for a,b in zip(edges,source_edges):
            if (a["mapwarp_line"], a["start"], a["target"], a["warp_CREATE_ordinal"], a["warp_CREATE_sha256"], a["reverse_explicit"]) != (
                b["mapwarp_line"],b["start"],b["target"],b["create_ordinal"],b["create_sha256"],b["reverse_present"]):
                return False
    source = next(x for x in gfx["graphics"] if x["graphic"] == 16033)
    g = q["original_3403_static_character_candidate"]
    if any(g.get(k) != source[v] for k,v in [
        ("rd_sha256","rd_sha256"),("png_sha256","png_sha256"),("rgba_sha256","rgba_sha256"),
        ("dimensions","dimensions"),("signed_adrn_offset","signed_adrn_offset")]):
        return False
    return True

class Integration20PublicEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((REC / NAME).read_bytes())
        cls.upstream = {k: verified(*value) for k,value in PINS.items()}

    def test_two_newly_replayed_rooms_keep_original_hash_and_frame_identity(self):
        q=self.report; m=self.upstream
        self.assertEqual(set(q["rooms"]), {"3303", "3403"})
        self.assertTrue(consistent(q,m["map09"],m["integration19"],m["integration17"],m["map04"]))
        self.assertEqual(q["rooms"]["3303"]["candidate_canvas"]["full_RGBA_sha256"]["combined"],
                         "bea3b37d97f9a4978952fce9d16618647db01812dce6a0dbf389829b85c8dbe1")
        self.assertEqual(q["rooms"]["3403"]["candidate_canvas"]["full_RGBA_sha256"]["combined"],
                         "34c63c3af687cddd9aa6ab16091da331e72a1c15127e2a0aa3bb4dba030eb280")
        self.assertTrue(all(r["candidate_canvas"]["numpy_and_Pillow_pixel_identical"] for r in q["rooms"].values()))

    def test_actual_original_three_plane_cell_samples_are_not_synthetic_status(self):
        q=self.report["rooms"]
        self.assertEqual([s["original_DAT_u16_at_spawn"] for s in q["3303"]["services"]],
                         [[5002,0,49152],[5000,12631,49152]])
        self.assertEqual([s["original_DAT_u16_at_spawn"] for s in q["3403"]["services"]],
                         [[5019,0,49152],[5001,0,49152]])
        self.assertEqual([e["source_original_DAT_u16_at_room_endpoint"] for e in q["3303"]["original_directed_edges"]],
                         [[5115,0,49155],[5115,0,49155],[5116,0,49155]])
        self.assertEqual([e["source_original_DAT_u16_at_room_endpoint"] for e in q["3403"]["original_directed_edges"]],
                         [[5025,0,49155],[5025,0,49155],[5026,0,49155],[5026,0,49155]])
        self.assertEqual(self.report["original_3300_source_endpoint"]["original_three_u16"], [2023,0,49155])
        self.assertFalse(q["3303"]["original_native_client_or_warp_event_executed"])
        self.assertFalse(q["3403"]["original_native_client_or_warp_event_executed"])

    def test_3400_qualified_MAP_is_not_invented_complete_DAT(self):
        q=self.report; z=q["original_3400_source_boundary"]
        self.assertNotIn("3400", self.upstream["map09"]["maps"])
        self.assertNotIn("3400.dat",{r[0] for r in self.upstream["map04"]["per_floor_source_rows"]})
        self.assertFalse(z["full_original_3400_DAT_qualified_from_MAP09"])
        self.assertTrue(z["full_3400_DAT_named_RAR_member_present"])
        self.assertFalse(z["successful_full_3400_DAT_extraction_this_work"])
        self.assertFalse(z["auxiliary_MAP_as_complete_three_plane_DAT"])
        self.assertFalse(z["original_3400_warp_endpoint_DAT_u16_known"])
        m=z["independently_extracted_3400_MAP"]
        self.assertEqual((m["bytes"],m["crc32"],m["geometry"],m["observed_u16_payload_cells"]),
                         (28808,"8b6c3b59",[120,120],14400))
        self.assertEqual(m["sha256"], "5145335b11bf8b0ae03c7634b6dacc471220c42946da76a17016fb7a95d46bbd")
        self.assertEqual(self.report["rooms"]["3303"]["original_directed_edges"][-1]["reverse_explicit"], False)
        self.assertEqual(self.report["rooms"]["3303"]["original_directed_edges"][-1]["start"], [3303,16,20])

    def test_private_original_pixels_not_mistaken_for_native_runtime(self):
        q=self.report; d=q["private_delivery"]; v=q["verification"]; b=q["bounds"]
        self.assertEqual((d["bytes"],d["members"],d["sha256"]),
                         (2585668,101,"2403ea2ee5928fba93de8b8913859b403d20e449049cfbba19a28ca237f31abb"))
        self.assertTrue(d["crc_all_pass"] and d["Library_retrieval_whole_SHA_and_CRC_verified"])
        self.assertEqual((v["browser_JS_errors"],v["browser_external_HTTP_requests"]),(0,0))
        self.assertFalse(v["direct_file_navigation_succeeded"])
        self.assertEqual(v["private_browser_mode"],"CHROMIUM_IN_MEMORY_EXACT_PNG_BYTES")
        self.assertTrue(v["browser_six_source_frame_modes_loaded"])
        for field in ("native_original_client_executed","native_warp_collision_or_shop_action_executed",
                      "official_TW10_and_mixed25_same_deployment","source_original_proprietary_images_published_in_Git"):
            self.assertIs(b[field],False)
        self.assertIsNone(b["overall_percent"])
        self.assertEqual(b["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(b["R79"],"PAUSED_NON_BLOCKING")

    def test_deliberately_substituted_source_halts_source_consistency(self):
        m=self.upstream;q=self.report
        evil=copy.deepcopy(q)
        evil["rooms"]["3303"]["original_DAT"]["sha256"]="0"*64
        self.assertFalse(consistent(evil,m["map09"],m["integration19"],m["integration17"],m["map04"]))
        evil=copy.deepcopy(q)
        evil["rooms"]["3403"]["services"][0]["graphic_alias"]=16018
        self.assertFalse(consistent(evil,m["map09"],m["integration19"],m["integration17"],m["map04"]))
        evil=copy.deepcopy(q)
        evil["original_3403_static_character_candidate"]["rd_sha256"]="bad"
        self.assertFalse(consistent(evil,m["map09"],m["integration19"],m["integration17"],m["map04"]))

if __name__ == "__main__":
    unittest.main()
