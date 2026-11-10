"""Source-bounded regression for the two original event20 dungeon rooms."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered/STONEAGE-INTEGRATION30-EVENT20-DUNGEON-SOURCE-R1.json"

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

class DungeonEvent20(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(R.read_text(encoding="utf-8"))
        cls.up={}
        for k,v in cls.r["upstream"].items():
            raw=(ROOT/v["path"]).read_bytes()
            assert blob(raw)==v["git_blob"],k
            cls.up[k]=json.loads(raw)

    def test_historical_current_and_source_pins(self):
        p=self.r["preserved_CURRENT"]
        self.assertEqual(p,{"bytes":2709173,"git_blob":"c89e0e33537990aa2132b47c40fef49a985a935c"})
        original=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(original),p["bytes"])
        self.assertEqual(blob(original[:p["bytes"]]),p["git_blob"])
        self.assertEqual(self.r["starting_tree"],"f0eef1d408e40278eb08b12f10964f6b0317550b")

    def test_two_real_dat_and_scene_attributions(self):
        m=self.up["map"]["maps"]
        self.assertEqual(set(self.r["maps"]),{"20607","20608"})
        for floor,r in self.r["maps"].items():
            source=m[floor]
            self.assertEqual((r["DAT_sha256"],r["DAT_bytes"]),(source["source_sha256"],source["source_bytes"]))
            self.assertEqual(r["DAT_sha256"],self.r["original_files"]["DAT_sha256"][floor])
            for key,sk in (("geometry","geometry"),("canvas","canvas_size"),("origin","origin"),
                ("draw_positions","draw_positions"),("distinct_tiles","unique_draw_aliases"),
                ("base_RGBA_by_mode","frame_RGBA_sha256")):
                self.assertEqual(r[key],source[sk])
            self.assertNotEqual(r["candidate_RGBA_sha256"],r["base_RGBA_by_mode"]["combined"])
            self.assertFalse(r["original_native_compositing_verified"])
        self.assertEqual([self.r["maps"][k]["draw_positions"] for k in ("20607","20608")],[2329,187])

    def test_original_create_and_14_source_script_sections(self):
        q=self.up["q"]; rows=self.r["npcs"]
        self.assertEqual([x["alias"] for x in rows],[100431,16032,16029])
        self.assertEqual([len(x["events"]) for x in rows],[6,3,5])
        for x,c in zip(rows,q["original_creates"][3:],strict=True):
            self.assertEqual((x["ordinal"],x["floor"],x["xy"],x["alias"],x["direction"],x["create_sha256"],x["script"]),
                (c["ordinal"],c["source_floor"],c["source_borncorner"][:2],c["graphic_alias_not_image_identity"],
                 c["direction"],c["source_block_sha256"],c["script_ref"]))
            s=next(y for y in q["original_scripts"] if y["path"]==x["script"])
            self.assertEqual((x["script_sha256"],x["events"]),(s["source_sha256"],s["events"]))
        self.assertEqual(rows[0]["events"][1]["actions"]["GetRandItem"],["2490,2491,2492,2493,2494"])
        self.assertEqual(rows[2]["events"][0]["actions"]["GetItem"],["2488"])

    def test_cell_samples_and_preserve_two_exits(self):
        cells=self.r["original_cells"]
        index={tuple(x[:3]):x[3:] for x in cells}
        self.assertEqual(len(cells),len(index))
        self.assertEqual(index[(20608,0,7)],[4074,0,49155])
        self.assertEqual(index[(20608,0,8)],[4074,12827,49155])
        for r in self.r["main_exits"]+self.r["other_directed_warps"]:
            self.assertEqual(r["start_u16"],index[tuple(r["start"])])
            self.assertEqual(r["target_u16"],index[tuple(r["target"])])
        exits=self.r["main_exits"]
        self.assertEqual([x["line"] for x in exits],[2308,2309,2310,2311])
        for now,old in zip(exits,self.up["receipt"]["next_source_ready_work"]["all_four_original_directed_records"],strict=True):
            self.assertEqual(now,old)
        self.assertEqual(exits[0]["start"],exits[2]["start"])
        self.assertNotEqual(exits[0]["target"],exits[2]["target"])
        self.assertFalse(self.up["receipt"]["next_source_ready_work"]["native_route_resolution_verified"])

    def test_other_warp_directions_without_invented_reverses(self):
        others=self.r["other_directed_warps"]
        self.assertEqual([x["line"] for x in others],[2307,2460,2461,2462,2463,2464,2465])
        self.assertEqual(others[0]["target"],[20606,8,23])
        self.assertEqual(self.r["original_files"]["mapwarp_sha256"],self.up["prior"]["original_mapwarp_sha256"])

    def test_sprite_namespace_and_art_source_bounds(self):
        art=self.r["graphics"]
        self.assertEqual(set(art),{"100431","16029","16032"})
        self.assertEqual(art["100431"]["bitmap"],87803)
        self.assertEqual([art[x]["bitmap"] for x in ("16032","16029")],[5878,5875])
        spr=self.r["spr_100431"]
        rows=[x for x in self.up["r40"]["material"]["all_index_rows"] if x[1]==100431]
        self.assertEqual(rows,[[394,100431,2623688,104,16]])
        self.assertEqual([spr[k] for k in ("group_index","spr_no","offset","anim_count","reserved")],rows[0])
        self.assertEqual((spr["frame_count"],spr["distinct_non_sentinel_bitmap_keys"]),(592,344))
        self.assertFalse(spr["native_frame_selection_verified"])

    def test_private_material_and_historical_limits(self):
        z=self.r["private_archive"]
        self.assertEqual((z["size"],z["members"],z["sha256"]),(6980092,28,
            "811139ca9f78ccf20a90d05c5e0535ace34a4be7600f8e0efd9335f3e774441b"))
        self.assertTrue(z["crc_all_pass"])
        self.assertEqual(self.r["offline_observation"]["HTML_script_sections"],14)
        self.assertFalse(self.r["offline_observation"]["browser_interaction_verified"])
        for k in ("original_client_running","original_warp_event_execution","original_animation_frame_selection",
                  "early_official_same_deployment","private_assets_published"):
            self.assertFalse(self.r["checks"][k],k)
        self.assertEqual([self.r["checks"][x] for x in ("stage_A","stage_B_wiki","R79","overall_percent")],
                         ["7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None])

if __name__=="__main__":
    unittest.main()
