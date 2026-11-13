"""Source-derived-only validation of the INTEGRATION99 bounded floor cross-file relation."""
import hashlib
import json
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-INTEGRATION99-THREE-DUNGEON-SOURCE-HUBS-R1.json"
SOURCES = {
    "d0": ("research/recovered/STONEAGE-INTEGRATION95-DUNGEON00-147-ORIGINAL-WARP-AND-PRIOR-DAT-R1.json", "285857ec36ffe7cdadec5f6093a861ed0e5be05a"),
    "d1": ("research/recovered/STONEAGE-INTEGRATION96-DUNGEON01-SEVEN-WARPMAN-ORIGINAL-SOURCE-R1.json", "f98ebaad7c730df91737f293f109dc4eda7a3bc3"),
    "d3": ("research/recovered/STONEAGE-INTEGRATION80-DUNGEON03-NPC-WARP-DAT-SOURCE-R1.json", "af8bfb07a1446cde2cdd727a57e032c6b77cc13b"),
}

def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

def canonical(k, r):
    if k == "d0":
        return {"family":"dungeon00","record_ordinal":r["ordinal"],"source_floor":r["source_floor"],"source_xy":r["source_xy"],"target_floor":r["target_floor"],"target_xy":r["target_xy"],"create_block_sha256":r["original_block_SHA256"]}
    if k == "d1":
        return {"family":"dungeon01","record_ordinal":r["create_index_0based"],"source_floor":r["source"]["floor"],"source_xy":[r["source"]["x"],r["source"]["y"]],"target_floor":r["handler_target"]["floor"],"target_xy":[r["handler_target"]["x"],r["handler_target"]["y"]],"create_block_sha256":r["create_block_sha256"],"handler_full_sha256":r["handler_sha256"]}
    return {"family":"dungeon03","record_ordinal":r["create_order"],"source_floor":r["source_floorid"],"source_xy":r["source_xy"],"target_floor":r["target_floorid"],"target_xy":r["target_xy"],"create_block_sha256":r["original_create_block_sha256"]}

def graph_components(rows):
    graph = defaultdict(set)
    for x in rows:
        a, b = x["source_floor"], x["target_floor"]
        graph[a].add(b)
        graph[b].add(a)
    seen, components = set(), []
    for vertex in graph:
        if vertex in seen: continue
        q = [vertex]
        seen.add(vertex)
        for v in q:
            for w in graph[v]:
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        components.append(sorted(q))
    return sorted(components, key=lambda x:(-len(x), x[0]))

class TestDungeonSourceHubBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.fixtures = {k:json.loads((ROOT / v[0]).read_text(encoding="utf-8")) for k,v in SOURCES.items()}
        f = cls.fixtures
        cls.rows = [canonical("d0", x) for x in f["d0"]["original_warp_raw_source_rows_numeric_only"]] + [canonical("d1", x) for x in f["d1"]["seven_guardians"]] + [canonical("d3", x) for x in f["d3"]["static_warp_creates"]]

    def test_exact_prior_git_blobs(self):
        for path, expected in SOURCES.values():
            with self.subTest(path=path):
                self.assertEqual(blob_sha(ROOT / path), expected)

    def test_167_records_and_78_floor_ids(self):
        self.assertEqual([sum(1 for r in self.rows if r["family"] == t) for t in ("dungeon00", "dungeon01", "dungeon03")], [147, 7, 13])
        self.assertEqual(len(self.rows), 167)
        floors = {x[k] for x in self.rows for k in ("source_floor", "target_floor")}
        self.assertEqual(len(floors), 78)
        self.assertEqual(self.report["counts"]["source_records_total"], 167)
        self.assertEqual(self.report["counts"]["distinct_floor_ids"], 78)

    def test_only_two_shared_numeric_floor_ids(self):
        groups = defaultdict(set)
        for row in self.rows:
            for key in ("source_floor","target_floor"):
                groups[str(row[key])].add(row["family"])
        actual = {floor:sorted(g) for floor,g in groups.items() if len(g) >= 2}
        self.assertEqual(actual, {"100":["dungeon00","dungeon03"], "200":["dungeon00","dungeon01","dungeon03"]})
        self.assertEqual(actual, self.report["shared_floor_groups"])

    def test_exact_26_incident_source_rows(self):
        for floor, number in (("100",19),("200",7)):
            expected = [r for r in self.rows if int(floor) in (r["source_floor"],r["target_floor"])]
            expected.sort(key=lambda r:(r["family"],r["record_ordinal"]))
            self.assertEqual(len(expected), number)
            self.assertEqual(self.report["hub_incident_source_records"][floor], expected)

    def test_weak_component_sizes_only(self):
        components = graph_components(self.rows)
        self.assertEqual([len(c) for c in components], [46,10,9,8,3,1,1])
        self.assertEqual(self.report["source_only_weak_components"], [{"floor_id_count":len(c),"floor_ids":c} for c in components])

    def test_dungeon01_static_250_not_silently_included(self):
        f = self.fixtures["d1"]
        self.assertEqual(f["counts"]["CREATE_blocks"],257)
        self.assertEqual(f["counts"]["npcgen_warpman"],7)
        self.assertEqual(f["counts"]["npcgen_warp_static"],250)
        self.assertEqual(len(f["seven_guardians"]),7)

    def test_negative_boundaries_and_historical_original(self):
        b = self.report["bounds"]
        for k in ("floor_100_prior_DAT_qualified_in_three_fixtures","floor_200_prior_DAT_qualified_in_three_fixtures","source_records_are_effective_warp_execution","native_client_or_server_executed_this_unit","full_original_DAT_reread_this_unit","raw_proprietary_source_republished"):
            self.assertIs(b[k],False)
        self.assertIs(b["not_proof_of_passability_collision_gate_trigger_or_original_same_deployment"],True)
        self.assertEqual(self.report["baseline"]["CURRENT_preserved_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(self.report["historical_stage"]["stage_A"],"7 PARTIAL + 2 OPEN")
        self.assertIsNone(self.report["historical_stage"]["overall_percent"])

if __name__ == "__main__":
    unittest.main()
