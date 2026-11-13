import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"research/recovered/STONEAGE-INTEGRATION90-PORU-DRAGON-HALL-SOURCE-2D-R1.json"
CHAR=ROOT/"research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
PET=ROOT/"research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json"

class PoruOriginalMaterialContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(OUT.read_text(encoding="utf-8"))
        cls.c=json.loads(CHAR.read_text(encoding="utf-8"))
        cls.p=json.loads(PET.read_text(encoding="utf-8"))

    def test_original_file_identity(self):
        d=self.d; f=next(r for r in self.c["source_files"] if r[0]=="poru/boss.create")
        self.assertEqual([f[1],f[2],f[3]],[d["original_sources"]["npc_create_original_bytes"],d["original_sources"]["npc_create_original_sha256"],d["original_sources"]["npc_create_original_crc32"]])
        self.assertEqual(len(d["original_static_NPC_CREATE_source_rows"]),24)

    def test_all_24_original_span_and_static_values(self):
        old=[r for r in self.c["create_rows"] if r[0]=="poru/boss.create"]
        new=self.d["original_static_NPC_CREATE_source_rows"]
        self.assertEqual(len(old),len(new))
        for a,b in zip(old,new):
            self.assertEqual([a[1],a[2],a[3],a[4]],[b["source_index"],b["byte_start"],b["byte_end"],b["original_span_sha256"]])
            self.assertEqual([a[5],a[6],a[8][0],a[8][1],a[10],a[11]],[b["floor"],b["graphic"],*b["xy"],b["direction_value"],b["template_function"]])
            self.assertEqual([a[15][0][0],a[15][0][2]],[b["source_arg_path"],b["original_arg_sha256"]])

    def test_exact_original_floor_function_census(self):
        from collections import Counter
        rows=self.d["original_static_NPC_CREATE_source_rows"]
        self.assertEqual(Counter(r["floor"] for r in rows),{5511:23,5510:1})
        self.assertEqual(Counter(r["template_function"] for r in rows),{"npcgen_man":22,"changeevent":1,"sb_ganzo":1})
        self.assertEqual(Counter(r["graphic"] for r in rows),{100351:6,100353:6,100354:4,100396:4,100371:2,100373:2})

    def test_original_DAT_raw_three_planes_and_bounds(self):
        d=self.d
        dims={r["floor"]:r for r in d["original_sources"]["source_MAP_DAT"]}
        self.assertEqual({5510,5511},set(dims))
        for fl,x in dims.items():
            self.assertEqual(x["bytes"],8+x["width"]*x["height"]*6)
            self.assertEqual(x["raw_3x_u16_layout"],"3_CONTIGUOUS_PLANES")
        for r in d["original_static_NPC_CREATE_source_rows"]:
            w=dims[r["floor"]]["width"]
            self.assertTrue(0<=r["xy"][0]<w and 0<=r["xy"][1]<w)
            self.assertEqual(r["source_map_raw_u16"][1],0)
            self.assertEqual(r["source_map_raw_u16"][2],49152 if r["floor"]==5511 else 49154)
        self.assertEqual([r["source_map_raw_u16"][0] for r in d["original_static_NPC_CREATE_source_rows"]],[4204,4202,4202,4200,4208,4204,4204,4203,4208,4207,4202,4205,4202,4203,4201,4201,4200,4204,4201,4203,4207,4208,4205,4205])

    def test_five_referenced_original_files_preserved(self):
        refs=self.d["source_parameter_file_receipts"]
        self.assertEqual(len(refs),5)
        self.assertEqual(len({x["path"] for x in refs}),5)
        self.assertEqual(len({x["sha256"] for x in refs}),3)
        src={x["path"].removeprefix("npc/"):x["sha256"] for x in refs}
        for row in self.d["original_static_NPC_CREATE_source_rows"]:
            self.assertEqual(src[row["source_arg_path"]],row["original_arg_sha256"])
        self.assertEqual({r["bytes"] for r in refs if "poru5511_" in r["path"]},{13})

    def test_5510_boss_guard_is_only_static(self):
        a=self.d["original_guard_boss_arg_only_static"]
        self.assertEqual((a["source_floor"],a["source_index"],a["warpfl_literal"],a["warpx_literal"],a["warpy_literal"]),(5510,23,5511,6,24))
        self.assertEqual(len(a["enemyno_literal"]),10)
        self.assertFalse(a["proof_of_native_combat_or_warp"])

    def test_six_original_TW1_spr_groups_qualified(self):
        orig={row[0]:row for row in self.p["source_groups"]}
        gs=self.d["separate_retail_tw1_selected_spr_groups"]
        self.assertEqual([r["graphic"] for r in gs],[100351,100353,100354,100371,100373,100396])
        for gr in gs:
            src=orig[gr["graphic"]]
            self.assertEqual([src[1],src[2],src[3],src[4],src[6]],[gr["tw1_source_group_index"],gr["original_full_spr_sha256"],gr["source_total_animation_sequences"],gr["selected_frame_occurrences"],gr["distinct_selected_bitmaps"]])
            self.assertEqual([[s["action"],s["direction"],s["source_frame_count"],s["ordered_source_bitmap_sequence_sha256"],s["source_duration_raw"]] for s in gr["selected_action_direction0"]],src[5])

    def test_92_real_RD_png_receipt_positions(self):
        public={row[0]:row for row in self.p["source_actual_pixel_receipts"]}
        found=set();total=0
        for group in self.d["separate_retail_tw1_selected_spr_groups"]:
            self.assertEqual(len(group["pixel_receipts"]),group["distinct_selected_bitmaps"])
            for v in group["pixel_receipts"]:
                bid=v["original_bitmap_id"];self.assertNotIn(bid,found);found.add(bid)
                source=public[bid]
                self.assertEqual([v["original_RD_sha256"],v["source_palette1_png_sha256"],v["width"],v["height"]],[source[2],source[8],source[5],source[6]])
                self.assertEqual(v["private_old_gallery_png_sha256_observed"],v["source_palette1_png_sha256"])
                total+=1
        self.assertEqual(total,92)
        self.assertEqual(self.d["selected_bitmap_png_match"]["private_legacy_png_SHA256_different"],0)

    def test_actual_18_sequences_187_positions(self):
        gs=self.d["separate_retail_tw1_selected_spr_groups"]
        self.assertEqual(sum(len(g["selected_action_direction0"]) for g in gs),18)
        self.assertEqual(sum(g["selected_frame_occurrences"] for g in gs),187)
        self.assertEqual(sum(g["distinct_selected_bitmaps"] for g in gs),92)
        self.assertEqual(self.d["selected_bitmap_png_match"]["new_RD_blocks_decoded_this_unit"],0)

    def test_private_archive_browser_and_source_boundary(self):
        q=self.d["private_observer_custody"]
        self.assertEqual(q["archive_bytes"],3391913)
        self.assertEqual(q["archive_sha256"],"a59c516ae39683c9a74abb1deb795328b892524fea0f7d8e29747155a3d553ad")
        self.assertEqual(q["archive_member_count"],10)
        self.assertTrue(q["independently_retrieved_same_SHA256"] and q["zip_crc_all_pass"])
        self.assertEqual(q["chromium_JS_errors"],0)
        self.assertEqual(q["chromium_external_HTTP_requests"],0)
        h=self.d["historical_limits"]
        self.assertTrue(all(value is False for value in h.values()))
        self.assertIsNone(self.d["phase_status"]["overall_percent"])

    def test_nonidentity_negative_contract(self):
        d=self.d
        self.assertEqual(d["content_scope"].count("NOT_SAME_DEPLOYED_BUILD"),1)
        self.assertFalse(d["private_observer_custody"]["original_commercial_game_client_executed"])
        self.assertFalse(d["previous_work_boundary"]["not_24_new_independent_characters"] is False)
        self.assertFalse(d["historical_limits"]["native_NPC_spawn"])
        self.assertEqual(d["previous_work_boundary"]["prior_INTEGRATION58_covering_one_boss_create_index"],0)

if __name__=="__main__":
    unittest.main()
