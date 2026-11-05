"""Check the public map-BGM derivations without loading proprietary bytes."""
from collections import Counter
from hashlib import sha1
import json
from pathlib import Path
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / "research/recovered"
WORLD17 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-17-MAP-BGM-SOURCE-R1.json"
WORLD12 = RECOVERED / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-12-THREE-VILLAGE-WARP-SOURCE-R1.json"
TW10_AUDIO = RECOVERED / "STONEAGE-TW10-AUDIO-DATASET-R1.txt"


def blob_sha(data):
    return sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


class MapBgmSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(WORLD17.read_bytes())
        cls.scan = cls.report["mixed25_map_scan"]

    def test_map_markers_select_slots_from_the_shared_file_table(self):
        rows = self.report["shared_table_rows"]
        self.assertEqual([r["slot"] for r in rows], list(range(12)))
        self.assertEqual(rows[1]["requested_path"], rows[2]["requested_path"])
        self.assertNotEqual(rows[1]["other_fields"], rows[2]["other_fields"])
        cases = self.report["marker_cases_40_to_59"]
        self.assertEqual(set(cases), {str(n) for n in range(40, 60)})
        expected = {40: (4, "t0"), 41: (3, "t1"), 42: (7, "d0"), 43: (8, "d1"),
                    44: (9, "d2"), 45: (10, "f0"), 46: (11, "f1")}
        for n, (slot, suffix) in expected.items():
            self.assertEqual(cases[str(n)], {"slot": slot, "requested_path": f"data/bgm/sabgm_{suffix}.wav"})
            self.assertEqual(rows[slot]["requested_path"], cases[str(n)]["requested_path"])
        for n in range(47, 60):
            self.assertEqual(cases[str(n)], {"slot": None, "requested_path": None})

    def test_taiwan_retail_wavs_match_the_pinned_inventory(self):
        early = self.report["taiwan10"]
        raw = TW10_AUDIO.read_bytes()
        self.assertEqual(blob_sha(raw), early["wav_inventory_git_blob"])
        inventory = {}
        for line in raw.decode().splitlines():
            if line.startswith("BGM|"):
                fields = dict(field.split("=", 1) for field in line.split("|")[1:])
                inventory[fields["name"]] = (int(fields["size"]), fields["sha256"])
        files = early["wav_files_verified_against_retail_inventory"]
        self.assertEqual(inventory, {n: (r["bytes"], r["sha256"]) for n, r in files.items()})
        self.assertEqual(set(files), {r["requested_path"].split("/")[-1] for r in self.report["shared_table_rows"]})
        self.assertEqual(len(files), 11)

    def test_scan_counts_reconcile_without_short_files_or_third_plane(self):
        scan = self.scan
        self.assertEqual(scan["dat_members"], 1011)
        self.assertEqual(scan["previous_map01_bytes_matched"] + scan["independent_recovery_bytes_matched"], 1011)
        self.assertEqual(scan["structured_dat"], 995)
        self.assertEqual(len(scan["zero_byte_members"]), 13)
        small = scan["short_non_map_bgm_members"]
        self.assertEqual({k: (v["bytes"], v["ascii"]) for k, v in small.items()},
                         {"BGM0.DAT": (2, "40"), "BGM1.DAT": (2, "40"), "BGM2.DAT": (2, "52")})
        first, second, third = scan["raw_counts_40_to_59_by_plane"]
        self.assertEqual(first, {})
        self.assertGreater(sum(third.values()), 0)
        expected = {str(n): second[str(n)] for n in range(40, 47)}
        self.assertEqual(expected, scan["mapped_marker_counts_in_first_two_planes"])
        rows = scan["per_floor_mapped_marker_counts"]
        self.assertEqual(len(rows), 438)
        self.assertEqual(len({floor for floor, _ in rows}), 438)
        occurrences = Counter()
        floors = Counter()
        for _, markers in rows:
            self.assertEqual(len(markers), len(dict(markers)))
            for marker, count in markers:
                self.assertIn(str(marker), expected)
                self.assertGreater(count, 0)
                occurrences[str(marker)] += count
                floors[str(marker)] += 1
        self.assertEqual(dict(occurrences), expected)
        self.assertEqual(dict(floors), scan["floor_counts_by_mapped_marker"])
        self.assertEqual(sum(occurrences.values()), 3236)

    def test_village_marker_counts_and_mixed_floor_200(self):
        expected = {"100": {45: 21}, "200": {40: 1, 46: 29}, "1000": {40: 4},
                    "2000": {40: 4}, "3000": {40: 5}, "4000": {40: 3}}
        floors = self.scan["priority_floors"]
        self.assertEqual(set(floors), set(expected))
        for floor, entry in floors.items():
            width, height = entry["dimensions"]
            points = entry["raw_40_to_59_coordinates"]
            self.assertEqual(len(points), len({tuple(p) for p in points}))
            self.assertEqual(Counter(p[3] for p in points), expected[floor])
            self.assertTrue(all(plane == 1 and 0 <= x < width and 0 <= y < height for plane, x, y, _ in points))

    def test_world12_exit_proximity_is_geometry_only(self):
        evidence = self.report["world12_outdoor_exit_geometry"]
        raw = WORLD12.read_bytes()
        self.assertEqual(blob_sha(raw), evidence["world12_git_blob"])
        exits = [(r["floor"], r["destination"]) for r in json.loads(raw)["routes"]
                 if r["destination"][0] in {100, 200}]
        rows = evidence["rows_village_destination_manhattan_distance_nearest_markers"]
        self.assertEqual([(v, d) for v, d, _, _ in rows], exits)
        self.assertEqual(len(rows), 22)
        for _, (floor, x, y), distance, nearest in rows:
            points = self.scan["priority_floors"][str(floor)]["raw_40_to_59_coordinates"]
            distance_of = lambda p: abs(x - p[1]) + abs(y - p[2])
            self.assertEqual(distance, min(map(distance_of, points)))
            self.assertEqual(nearest, [p for p in points if distance_of(p) == distance])
        self.assertFalse(evidence["distance_implies_audible_range"])

    def test_source_boundaries_and_distinct_audio_namespaces(self):
        self.assertEqual(self.report["mixed25_archive"]["loose_audio_members_in_archive"], 0)
        self.assertEqual(self.report["mixed25_archive"]["sound_3_wave_slots"], 27)
        self.assertEqual(self.report["bounds"], {
            "mixed25_requested_wav_payload_verified": False,
            "taiwan10_official_floor_assignment_verified": False,
            "same_official_historical_deployment_verified": False,
            "native_scene_playback_observed": False,
            "unmapped_input_is_proven_silence": False,
        })
