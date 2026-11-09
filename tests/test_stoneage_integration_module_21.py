"""Public, source-limited INTEGRATION21 relation audit; private original bytes are not in Git.

Original 3400.MAP cells were separately checked against a SHA-verified private
source. CI checks only the preserved derived receipt and qualifying source pins.
"""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
TARGET = "STONEAGE-INTEGRATION21-TEN-PET-ROOMS-SOURCE-ATLAS-R1.json"
PINS = {
    "i13": ("STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json", "728d5e2ecc9bf8944d326850bf604da42eb90309"),
    "i15": ("STONEAGE-INTEGRATION15-HOTORU-PET-SERVICE-BRIDGE-R1.json", "a46b23789bc4659580a466f67f3378d840030461"),
    "i16": ("STONEAGE-INTEGRATION16-THREE-PET-ROOMS-SOURCE-R1.json", "40e65fbabb8cb1216dd65782b92473f75aadfbf8"),
    "i17": ("STONEAGE-INTEGRATION17-THREE-PET-ROOMS-SOURCE-R1.json", "e716f01bbf7d08be2e13654909282a198f5334dd"),
    "i19": ("STONEAGE-INTEGRATION19-THREE-PET-SERVICES-SOURCE-R1.json", "8a3eccfb28c266c36c4ba764807e6b3ef64de620"),
    "i20": ("STONEAGE-INTEGRATION20-TWO-PET-ROOMS-ORIGINAL-SOURCE-R1.json", "53497d591604794b74180c3162e07204cdd0c9f8"),
}

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def load():
    q = json.loads((REC / TARGET).read_bytes())
    src = {}
    for key, (file, blob) in PINS.items():
        raw = (REC / file).read_bytes()
        assert git_blob(raw) == blob, ("source pin drift", key)
        assert q["upstream_reports"][key] == {"path": "research/recovered/" + file, "git_blob": blob}
        src[key] = json.loads(raw)
    return q, src

def service_signature(s):
    return (
        s["role"], s["xy"], s["graphic_alias"], s["create_file"],
        s["create_ordinal"], s["create_sha256"],
        s["parameter_file"], s["parameter_sha256"],
    )

def edge_signature(e):
    return (
        e["mapwarp_line"], e["start"], e["target"], e["source_row_sha256"],
        e["warp_CREATE_ordinal"], e["warp_CREATE_sha256"],
    )

def expected_edge(line, source, target, row_sha=None, create_ord=None, create_sha=None):
    return (line, source, target, row_sha, create_ord, create_sha)

def check_source_relations(q, src):
    rooms = {r["floor"]: r for r in q["rooms"]}
    assert list(rooms) == [1103,1203,1303,1403,2003,3103,3203,3303,3403,4003]
    assert len(rooms) == 10
    for key in ("i16", "i17"):
        for floor, original in src[key]["rooms"].items():
            room = rooms[int(floor)]
            assert room["source_report"] == key
            assert room["original_room_name"] == original["original_name"]
            assert room["original_DAT_sha256"] == original["dat"]["sha256"]
            assert room["original_canvas_candidate_RGBA_sha256"] == original["canvas"]["rgba_sha256"]
            assert len(room["services"]) == len(original["services"]) == 2
            for actual, s in zip(room["services"], original["services"]):
                assert service_signature(actual) == (
                    s["role"], s["xy"], s["graphic"], s["create"][0],
                    s["create"][1], s["create"][2], s["parameter"][0], s["parameter"][1])
            assert len(room["warps"]) == len(original["warps"])
            for actual, w in zip(room["warps"], original["warps"]):
                c = w.get("warp_create")
                assert edge_signature(actual) == expected_edge(
                    w["line"], w["source"], w["target"], w["sha256"],
                    c[1] if c else None, c[2] if c else None)
    room = rooms[1303]
    original = src["i13"]["rooms"]["1303"]
    assert room["source_report"] == "i13+i15"
    assert room["original_room_name"] == original["original_name"]
    assert room["original_DAT_sha256"] == original["dat"]["sha256"]
    assert room["original_canvas_candidate_RGBA_sha256"] == original["map07_canvas"]["rgba_sha256"]
    for actual, s in zip(room["services"], src["i15"]["service_joins"]):
        assert service_signature(actual) == (
            s["function_token"], s["xy"], s["graphic_alias"], s["create_path"],
            s["create_ordinal"], s["create_block_sha256"],
            s["original_parameter_path"], s["original_parameter_sha256"])
        match = next(x for x in original["source_create"]
                     if x["path"] == s["create_path"] and x["ordinal"] == s["create_ordinal"])
        assert match["block_sha256"] == s["create_block_sha256"]
    original_warps = [e for e in src["i13"]["warp_rows"]
                      if 1303 in (e["source"][0], e["target"][0])]
    assert len(room["warps"]) == len(original_warps) == 4
    for actual, w in zip(room["warps"], original_warps):
        assert edge_signature(actual) == expected_edge(
            w["line"], w["source"], w["target"], w["row_sha256"])
    assert room["original_graphic_reuse_note"].startswith("16049")
    assert src["i15"]["co_room_constraints"]["townpeople"]["graphic_alias"] == 16049
    assert src["i15"]["co_room_constraints"]["townpeople"]["create_ordinal"] == 61

    original = next(r for r in src["i19"]["rooms"] if r["floor"] == 4003)
    room = rooms[4003]
    assert room["source_report"] == "i19"
    assert room["original_room_name"] is None
    assert room["original_room_name_status"] == "UNKNOWN_IN_SELECTED_REPORT"
    assert room["original_DAT_sha256"] == original["dat"]["sha256"]
    for actual, s in zip(room["services"], original["services"]):
        assert service_signature(actual) == (
            s["role"], s["xy"], s["graphic"], s["create_file"],
            s["create_ordinal"], s["create_sha256"],
            s["parameter_path"], s["parameter_sha256"])
    original_warps = [e for e in src["i19"]["directed_warp_edges"]
                      if 4003 in (e["start"][0], e["target"][0])]
    assert len(room["warps"]) == len(original_warps) == 4
    for actual, e in zip(room["warps"], original_warps):
        assert edge_signature(actual) == expected_edge(
            e["mapwarp_line"], e["start"], e["target"], None,
            e["create_ordinal"], e["create_sha256"])

    for floor in (3303, 3403):
        room = rooms[floor]
        original = src["i20"]["rooms"][str(floor)]
        prior = next(x for x in src["i19"]["rooms"] if x["floor"] == floor)
        assert room["source_report"] == "i20"
        assert room["original_room_name"] == original["original_room_name"]
        assert room["original_DAT_sha256"] == original["original_DAT"]["sha256"]
        assert room["original_canvas_candidate_RGBA_sha256"] == original["candidate_canvas"]["full_RGBA_sha256"]["combined"]
        assert room["original_server_second_plane_diff_cells"] == original["original_server_LS2MAP"]["changed_cells_server_vs_client"][1]
        for actual, s in zip(room["services"], original["services"]):
            matched = next(z for z in prior["services"] if z["role"] == s["role"])
            assert service_signature(actual) == (
                s["role"], s["spawn_xy"], s["graphic_alias"], s["create_file"],
                s["create_ordinal"], s["create_sha256"],
                matched["parameter_path"], s["parameter_source_sha256"])
            assert matched["create_sha256"] == s["create_sha256"]
            assert matched["parameter_sha256"] == s["parameter_source_sha256"]
        for actual, e in zip(room["warps"], original["original_directed_edges"]):
            assert edge_signature(actual) == expected_edge(
                e["mapwarp_line"], e["start"], e["target"], None,
                e["warp_CREATE_ordinal"], e["warp_CREATE_sha256"])
    return rooms

def verify_graph_and_bounds(q):
    rows = q["rooms"]
    edges = [edge for r in rows for edge in r["warps"]]
    services = [s for r in rows for s in r["services"]]
    sig = lambda e: tuple(e["start"]), tuple(e["target"])
    index = {sig(e) for e in edges}
    assert len(index) == len(edges) == 38
    unmatched = []
    for e in edges:
        reverse = (tuple(e["target"]), tuple(e["start"])) in index
        assert e["reverse_listed"] is reverse
        if not reverse:
            unmatched.append({
                "mapwarp_line": e["mapwarp_line"], "start": e["start"], "target": e["target"]})
    assert unmatched == [
        {"mapwarp_line": 697, "start": [3103,16,21], "target": [3100,44,69]},
        {"mapwarp_line": 737, "start": [3303,16,20], "target": [3300,51,60]},
    ]
    summary = q["summary"]
    assert summary["original_DAT_room_count"] == len(rows) == 10
    assert summary["original_petshop_CREATE_count"] == sum(s["role"] == "PetShop" for s in services) == 10
    assert summary["original_petskillshop_CREATE_count"] == sum(s["role"] == "PetSkillShop" for s in services) == 10
    assert summary["original_directed_mapwarp_rows"] == len(edges)
    assert summary["reciprocal_directed_rows"] == 36
    assert summary["unpaired_directed_rows"] == unmatched
    reused = {}
    for r in rows:
        for s in r["services"]:
            reused.setdefault(str(s["graphic_alias"]), []).append({
                "floor":r["floor"], "role":s["role"],
                "create_file":s["create_file"], "create_ordinal":s["create_ordinal"]})
    assert summary["service_graphic_alias_reuse"] == {
        key:value for key,value in reused.items() if len(value)>1}
    assert set(summary["service_graphic_alias_reuse"]) == {"16033","16035","16046"}
    a = q["independent_3400_single_plane_auxiliary_observation"]
    assert a["file_bytes"] == 8 + 120 * 120 * 2
    assert (a["header_le_width"], a["header_le_height"], a["single_plane_u16_count"]) == (120,120,14400)
    assert a["source_sha256"] == "5145335b11bf8b0ae03c7634b6dacc471220c42946da76a17016fb7a95d46bbd"
    assert a["source_offsets_and_u16"] == [
        {"xy":[53,49],"offset":8+2*(49*120+53),"u16_le":0},
        {"xy":[54,49],"offset":8+2*(49*120+54),"u16_le":0}]
    assert a["actual_same_source_three_plane_3400_DAT_qualified"] is False
    assert a["original_warp_execution_proven"] is False
    b = q["limits"]
    assert all(b[key] is False for key in (
        "early_official_TW10_same_deployment","native_original_client_executed",
        "native_teleport_or_shop_executed","all_pet_graphic_pixel_candidates_obtained",
        "full_3400_three_plane_DAT_qualified"))
    assert b["stage_A"] == "7_PARTIAL_2_OPEN"
    assert b["stage_B_wiki"] == "GATED" and b["R79"] == "PAUSED_NON_BLOCKING"
    assert b["overall_percent"] is None

class Integration21PublicSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q, cls.src = load()

    def test_six_source_blob_pins_and_exact_twenty_create_joins(self):
        self.assertEqual(set(self.q["upstream_reports"]), set(PINS))
        self.assertEqual(self.q["preserved_CURRENT_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(len(check_source_relations(self.q, self.src)), 10)

    def test_all_38_original_directed_edges_replayed_with_two_real_asymmetries(self):
        check_source_relations(self.q, self.src)
        verify_graph_and_bounds(self.q)

    def test_missing_reverse_must_not_be_invented(self):
        changed = copy.deepcopy(self.q)
        changed["rooms"][5]["warps"][-1]["reverse_listed"] = True
        with self.assertRaises(AssertionError):
            verify_graph_and_bounds(changed)

    def test_source_graphic_alias_must_not_merge_two_create_instances(self):
        changed = copy.deepcopy(self.q)
        changed["rooms"][0]["services"][0]["create_ordinal"] = 83
        with self.assertRaises(AssertionError):
            check_source_relations(changed, self.src)

    def test_3400_aux_map_cannot_promote_to_three_plane_dat_or_native_warp(self):
        changed = copy.deepcopy(self.q)
        changed["independent_3400_single_plane_auxiliary_observation"]["actual_same_source_three_plane_3400_DAT_qualified"] = True
        with self.assertRaises(AssertionError):
            verify_graph_and_bounds(changed)
        changed = copy.deepcopy(self.q)
        changed["limits"]["native_teleport_or_shop_executed"] = True
        with self.assertRaises(AssertionError):
            verify_graph_and_bounds(changed)

if __name__ == "__main__":
    unittest.main()
