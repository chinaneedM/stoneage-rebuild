"""INTEGRATION15-R2 public-only provenance gates; never open proprietary source assets."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "research" / "recovered"
def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class Integration15R2EvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r2 = load("STONEAGE-INTEGRATION15-R2-HOTORU-PET-VISUAL-RECEIPT-R1.json")
        cls.r1 = load("STONEAGE-INTEGRATION15-HOTORU-PET-SERVICE-BRIDGE-R1.json")
        cls.room = load("STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json")["rooms"]["1303"]
        cls.w11 = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-11-NPC-STATIC-APPEARANCE-R1.json")

    def test_source_archive_and_room_preservation(self):
        a=self.r2
        self.assertEqual(a["private_source_carriers"]["integration13_zip"]["sha256"], "c4cb208810a8ae0ad1ad76f59f3569f2f19b8bfd0389fe71aa6d3ffa91ff44eb")
        self.assertEqual(a["private_source_carriers"]["world11_zip"]["sha256"], "ef7f658864bcfbbbf7948c110a0a040a075e8127d78a1fba8ecc2a6079619e00")
        self.assertEqual(a["original_room"]["floor"],1303)
        self.assertEqual(a["original_room"]["source_dat_sha256"],self.room["dat"]["sha256"])
        self.assertEqual(a["original_room"]["source_ls2map_sha256"],self.room["server_map"]["sha256"])
        self.assertEqual(a["original_room"]["retained_base_scene_png_sha256"],self.room["map07_canvas"]["png_sha256"])
        self.assertEqual(a["original_room"]["retained_canvas_rgba_sha256"],self.room["map07_canvas"]["rgba_sha256"])
        self.assertFalse(a["original_room"]["pixel_canvas_file_changed"])

    def test_reused_original_pngs_match_WORLD11_precisely(self):
        rows=self.r2["reused_original_static_pngs"]
        self.assertEqual([x["graphic"] for x in rows],[16048,16049])
        for row in rows:
            saved=[x for x in self.w11["decoded_static_graphics"] if x["graphic"]==row["graphic"]]
            self.assertEqual(len(saved),1)
            source=saved[0]
            for new,old in [("adrn_ordinal","adrn_ordinal"),("adrn_record_sha256","adrn_sha256"),("original_rd_sha256","rd_sha256"),("indexed_sha256","indexed_sha256"),("source_png_sha256","png_sha256"),("source_rgba_sha256","rgba_sha256"),("dimensions","dimensions"),("original_signed_adrn_offset","signed_adrn_offset")]:
                self.assertEqual(row[new],source[old],(row["graphic"],new))
            self.assertEqual(row["source_scope"],"WORLD11_MIXED25_RLE_STATIC_PNG_SOURCE_CHECKED")

    def test_three_distinct_create_nodes_and_source_pixel_coordinate_join(self):
        observed=self.r2["configured_overlay_instances"]
        self.assertEqual(len(observed),3)
        self.assertEqual([(x["role"],x["graphic"],x["coordinate"]) for x in observed],
                        [("petshop",16048,[16,13]),("skillshop",16049,[13,13]),("townpeople",16049,[11,6])])
        self.assertEqual([x["ordinal"] for x in observed],[53,54,61])
        self.assertEqual(len({x["create_sha"] for x in observed}),3)
        for x in observed:
            rows=[c for c in self.room["source_create"] if c["ordinal"]==x["ordinal"]]
            self.assertEqual(len(rows),1)
            row=rows[0]
            self.assertEqual(row["xy"],x["coordinate"])
            self.assertEqual(row["graphic_alias"],x["graphic"])
            self.assertEqual(row["block_sha256"],x["create_sha"])
            self.assertEqual(row["parameters"][0]["path"],x["source"])
            self.assertEqual(row["parameters"][0]["sha256"],x["parameter_sha"])
            png=next(z for z in self.r2["reused_original_static_pngs"] if z["graphic"]==x["graphic"])
            self.assertEqual(x["svg_png_xy"],[a+b for a,b in zip(x["marker"],png["original_signed_adrn_offset"])])
        self.assertEqual(observed[0]["create_sha"],self.r1["service_joins"][0]["create_block_sha256"])
        self.assertEqual(observed[1]["create_sha"],self.r1["service_joins"][1]["create_block_sha256"])
        self.assertEqual(observed[2]["create_sha"],self.r1["co_room_constraints"]["townpeople"]["create_block_sha256"])

    def test_private_receipt_and_precise_browser_boundary(self):
        a=self.r2
        pkg=a["saved_private_observer"]
        self.assertEqual(pkg["zip_members"],37)
        self.assertTrue(pkg["zip_CRC_all_members_pass"])
        self.assertTrue(pkg["all_original_34_members_preserved_except_index_html"])
        self.assertTrue(pkg["library_roundtrip_download_sha256_verified"])
        self.assertTrue(pkg["library_roundtrip_zip_crc_passed"])
        self.assertEqual(len(pkg["original_parameter_source_hashes"]),3)
        self.assertEqual(pkg["original_parameter_source_hashes"][0]["sha256"],self.r1["service_joins"][0]["original_parameter_sha256"])
        self.assertEqual(pkg["original_parameter_source_hashes"][1]["sha256"],self.r1["service_joins"][1]["original_parameter_sha256"])
        self.assertEqual(pkg["original_parameter_source_hashes"][2]["sha256"],self.r1["co_room_constraints"]["townpeople"]["original_parameter_sha256"])
        b=a["private_browser_test"]
        self.assertEqual(b["file_url_navigation"],"BLOCKED_BY_ADMINISTRATOR")
        self.assertEqual(b["localhost_url_navigation"],"BLOCKED_BY_ADMINISTRATOR")
        self.assertFalse(b["direct_extracted_file_url_verified"])
        self.assertEqual(b["source_details_card_count"],3)
        self.assertEqual(b["source_marker_link_count"],3)
        self.assertTrue(b["overlay_disabled_returned_exact_baseline_screenshot"])
        self.assertEqual(b["browser_JS_errors"],0)
        self.assertEqual(b["external_HTTP_requests"],0)

    def test_no_unjustified_historical_promotions(self):
        q=self.r2["qualification"]
        self.assertEqual(q["new_original_RD_decodes_this_unit"],0)
        self.assertEqual(q["reused_prior_source_verified_original_static_pngs"],2)
        self.assertEqual(q["new_private_candidate_observer_scene_overlays"],3)
        for flag in ("original_client_executed","same_official_historical_build_proven","native_original_graphic_layer_selection_proven","native_NPC_dialogue_trigger_proven","native_pet_storage_purchase_or_skill_training_verified","read_original_game_from_no_account_offline_legacy_client"):
            self.assertFalse(q[flag],flag)
        self.assertTrue(q["three_people_distinct_source_CREATE_records"])
        self.assertTrue(q["townpeople_image_same_as_skillshop_without_shared_identity_claim"])
        self.assertIsNone(self.r2["stage"]["overall_percent"])

if __name__=="__main__":
    unittest.main()
