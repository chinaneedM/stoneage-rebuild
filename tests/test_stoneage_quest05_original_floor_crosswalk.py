"""QUEST05 original-source floor crosswalk: no private assets, native execution claims, or inferred world geography."""
import collections
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json"


def load_path(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


class Quest05FloorSourceCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(TARGET.read_text(encoding="utf-8"))
        cls.sources = {}
        for cohort, pin in cls.report["original_sources_public_git_blobs"].items():
            raw = (ROOT / pin["path"]).read_bytes()
            assert git_blob_sha(raw) == pin["blob_sha"], (cohort, pin["path"])
            cls.sources[cohort] = json.loads(raw)
        cls.dat = {
            int(row[0].removesuffix(".dat")): row
            for row in cls.sources["map955"]["per_floor_source_rows"]
        }
        cls.source_ready = cls.sources["map09"]["maps"]
        cls.map10 = cls.sources["map10"]["maps"]

    def qualification(self, floor):
        dat = self.dat.get(int(floor))
        if dat is None:
            return ("NO_MATCHING_DAT_IN_955", None, None, None)
        name, num_bytes, sha = dat[:3]
        if str(floor) in self.source_ready:
            self.assertEqual(sha, self.source_ready[str(floor)]["source_sha256"])
            kind = "MAP09_GT99_RD_SOURCE_READY_CANDIDATE"
        elif str(floor) in self.map10:
            self.assertEqual(sha, self.map10[str(floor)]["source_DAT_sha256"])
            kind = "MAP10_GT99_RD_SOURCE_BOUND_LOW_VALUES_OPEN"
        else:
            kind = "DAT_PRESENT_GT99_QUALIFIED_RD_MISSING"
        return (kind, name, sha, num_bytes)

    def source_creates(self):
        q1, q2, q3, q4 = (self.sources[x] for x in ["quest01", "quest02", "quest03", "quest04"])
        for x in q1["source_creation_references"]:
            yield ("QUEST01", x["create_source_path"], x["create_brace_ordinal"], "WHOLE_CREATE_FILE", x["create_source_sha"], x["original_script_path"], x["original_script_sha"], x["floorid"], x["graphic_alias_numeric"], "npcgen_changeevent")
        for x in q2["source_create_references"]:
            yield ("QUEST02", x["source_create_path"], x["source_create_brace_ordinal"], "WHOLE_CREATE_FILE", x["source_create_sha256"], x["original_source_script_path"], x["original_source_script_sha256"], x["floor_id"], x["graphic_alias_numeric"], "npcgen_warp")
        for x in q3["source_creation_references"]:
            yield ("QUEST03", x["source_create_path"], x["create_block_ordinal"], "ORIGINAL_CREATE_BLOCK", x["original_create_block_sha256"], x["source_parameter_path"], x["original_parameter_sha256"], x["original_floorid_numeric"], x["original_graphic_alias_numeric"], x["family"])
        for x in q4["source_create_references"]:
            yield ("QUEST04", x["create_source_path"], x["create_source_block_ordinal"], "ORIGINAL_CREATE_BLOCK", x["source_create_block_sha256"], x["source_param_path"], x["source_param_sha256"], x["floorid_numeric"], x["graphic_numeric"], x["function_token"])

    def test_01_exact_population_and_every_source_create_row(self):
        r = self.report
        self.assertEqual(len(self.dat), 955)
        self.assertEqual(len(self.source_ready), 691)
        self.assertEqual(len(self.map10), 60)
        self.assertTrue(set(self.source_ready).isdisjoint(self.map10))
        self.assertEqual(len(r["source_CREATE_references"]), 598)
        expected = []
        for c, path, ordinal, scope, sha, param, param_sha, floor, graphic, family in self.source_creates():
            st, dat, datsha, datbytes = self.qualification(floor)
            expected.append({
                "cohort": c, "source_CREATE_file": path,
                "source_CREATE_block_ordinal": ordinal, "source_CREATE_SHA_scope": scope,
                "source_CREATE_sha256": sha,
                "source_parameter_file": param,
                "source_parameter_sha256": param_sha,
                "source_floor_id": floor, "source_graphic_alias": graphic,
                "source_family": family, "quest_origin_class": "ORIGIN_UNRESOLVED",
                "map_status": st, "source_DAT_file": dat,
                "source_DAT_sha256": datsha, "source_DAT_bytes": datbytes
            })
        self.assertEqual(r["source_CREATE_references"], expected)
        unique = {(x["cohort"], x["source_CREATE_file"], x["source_CREATE_block_ordinal"]) for x in expected}
        self.assertEqual(len(unique), 598)
        self.assertEqual(len(set(x["source_floor_id"] for x in expected)), 236)
        self.assertEqual(r["source_original_mixed25_RAR_sha256"], self.sources["map955"]["provenance"]["original_mixed25_community_RAR_sha256"])
        self.assertEqual(r["source_original_mixed25_RAR_sha256"], self.sources["quest01"]["source"]["original_RAR_sha256"])
        self.assertEqual(r["source_original_mixed25_RAR_sha256"], self.sources["quest02"]["source"]["parent_RAR_sha256"])

    def test_02_categorized_floor_index_and_unsupported_statuses(self):
        r = self.report
        expected = {}
        for x in r["source_CREATE_references"]:
            k = str(x["source_floor_id"])
            if k not in expected:
                expected[k] = {
                    "source_floor_id": x["source_floor_id"], "map_status": x["map_status"],
                    "source_DAT_file": x["source_DAT_file"], "source_DAT_sha256": x["source_DAT_sha256"],
                    "source_CREATE_ref_count": 0, "source_cohorts": {}
                }
            y = expected[k]
            y["source_CREATE_ref_count"] += 1
            y["source_cohorts"][x["cohort"]] = y["source_cohorts"].get(x["cohort"], 0) + 1
        self.assertEqual(r["floors"], sorted(expected.values(), key=lambda x: x["source_floor_id"]))
        s = r["summary"]
        self.assertEqual(s["source_CREATE_refs"], 598)
        self.assertEqual(s["distinct_source_floor_ids"], 236)
        c = collections.Counter(x["map_status"] for x in r["source_CREATE_references"])
        self.assertEqual(dict(c), {
            "MAP09_GT99_RD_SOURCE_READY_CANDIDATE": 352,
            "MAP10_GT99_RD_SOURCE_BOUND_LOW_VALUES_OPEN": 11,
            "DAT_PRESENT_GT99_QUALIFIED_RD_MISSING": 147,
            "NO_MATCHING_DAT_IN_955": 88
        })
        self.assertEqual(s["source_CREATE_ref_map_status_counts"], dict(c))
        self.assertEqual(s["distinct_source_floor_ids_by_map_status"], dict(collections.Counter(x["map_status"] for x in r["floors"])))
        for x in r["source_CREATE_references"]:
            if x["map_status"] == "NO_MATCHING_DAT_IN_955":
                self.assertIsNone(x["source_DAT_file"])
                self.assertIsNone(x["source_DAT_sha256"])
            else:
                self.assertEqual(x["source_DAT_file"], f'{x["source_floor_id"]}.dat')

    def test_03_exact_original_conditional_warp_candidate_edges(self):
        r = self.report
        expected = []
        excluded_zero = 0
        by_script = collections.defaultdict(list)
        for x in r["source_CREATE_references"]:
            if x["cohort"] == "QUEST02":
                by_script[x["source_parameter_file"]].append(x)

        def edge(create, kind, ordinal, coords, guard, segsha):
            nonlocal excluded_zero
            if coords[0] == 0:
                excluded_zero += 1
                return
            st, name, sha, _bytes = self.qualification(coords[0])
            expected.append({
                "source_cohort": create["cohort"],
                "source_CREATE_file": create["source_CREATE_file"],
                "source_CREATE_block_ordinal": create["source_CREATE_block_ordinal"],
                "source_floor_id": create["source_floor_id"],
                "source_parameter_file": create["source_parameter_file"],
                "source_parameter_sha256": create["source_parameter_sha256"],
                "source_literal_kind": kind,
                "source_segment_ordinal": ordinal, "source_segment_sha256": segsha,
                "condition_keyword_counts": guard,
                "literal_target_floor_id": coords[0],
                "literal_target_x": coords[1], "literal_target_y": coords[2],
                "target_map_status": st, "target_DAT_file": name,
                "target_DAT_sha256": sha
            })
        for segment in self.sources["quest02"]["source_control_segments"]:
            connected = by_script[segment["script_path"]]
            self.assertTrue(connected)
            for create in connected:
                self.assertEqual(segment["original_file_sha256"], create["source_parameter_sha256"])
                for triple in segment["source_warp_coordinate_triples"]:
                    edge(create, "QUEST02_WARP_LITERAL", segment["source_segment_ordinal"], triple, segment["source_condition_keywords"], segment["source_segment_decoded_cp950_utf8_sha256"])
        pfiles = {x["path"]: x for x in self.sources["quest04"]["source_parameter_files"]}
        for create in (x for x in r["source_CREATE_references"] if x["cohort"] == "QUEST04"):
            param = pfiles[create["source_parameter_file"]]
            self.assertEqual(param["original_sha256"], create["source_parameter_sha256"])
            if param["template_family"] == "npcgen_janken":
                edge(create, "QUEST04_JANKEN_WINWARP_LITERAL", None, param["winwarp_literal"], {}, None)
                edge(create, "QUEST04_JANKEN_LOSEWARP_LITERAL", None, param["losewarp_literal"], {}, None)
            elif param["template_family"].startswith("event69") and isinstance(param.get("warp_literal"), list):
                edge(create, "QUEST04_EVENT69_WARP_LITERAL", None, param["warp_literal"], {}, None)
        self.assertEqual(len(expected), 234)
        self.assertEqual(excluded_zero, 94)
        self.assertEqual(r["conditional_warp_literal_candidate_edges"], expected)
        self.assertEqual(r["summary"]["warp_literal_candidate_edges"], 234)
        self.assertEqual(r["summary"]["warp_zero_floor_sentinels_excluded_from_edges"], 94)
        self.assertEqual(r["summary"]["warp_edges_by_kind"], dict(collections.Counter(x["source_literal_kind"] for x in expected)))
        self.assertFalse(any(x["literal_target_floor_id"] == 0 for x in expected))

    def test_04_historical_negative_gates(self):
        q = self.report["qualified_limits"]
        for key in [
            "unverified_world_island_or_village_classification", "source_literal_WARP_not_verified_original_runtime_transition",
            "source_q02_zero_WARP_triples_never_treated_as_floor_zero",
            "community_mixed25_source_RAR_custody_does_not_prove_actual_server_deployment",
            "source_CREATE_ref_count_not_number_of_distinct_quests",
            "quest_origins_all_remain_UNRESOLVED",
        ]:
            self.assertIs(q[key], True)
        for key in ["native_warp_execution_observed", "original_TW10_commercial_server_same_deployment_verified", "original_private_commercial_asset_or_script_body_published"]:
            self.assertIs(q[key], False)
        self.assertEqual(q["stage_B"], "GATED")
        self.assertEqual(q["wiki"], "GATED")
        self.assertIsNone(q["overall_percent"])


if __name__ == "__main__":
    unittest.main()
