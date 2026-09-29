import hashlib
import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_server_only_static_map_probe import (
    analyze,
    parse_targets,
)


def _server_map(floor, width=2, height=1):
    tiles = (1, 2)
    objects = (10, 11)
    header = (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", width, height)
    )
    return (
        header
        + struct.pack(">2H", *tiles)
        + struct.pack(">2H", *objects)
    )


def _report(raw):
    digest = hashlib.sha256(raw).hexdigest()
    return "\n".join(
        [
            "EVIDENCE_ROLE|LATER_RECOVERED",
            "COUNT|status:SERVER_MAP_ONLY:ids|1",
            (
                "MISSING_DAT_DESTINATION|floor=20002|edge_refs=1|"
                "status=SERVER_MAP_ONLY|client_map_paths=|"
                "client_map_dimensions=|client_map_sha256=|"
                "server_map_paths=dungeon/floor|"
                "server_map_dimensions=2x1|"
                f"server_map_sha256={digest}"
            ),
            "RESOLUTION|MISSING_DAT_WARP_DESTINATION_PAYLOADS_CLASSIFIED",
        ]
    )


class ServerOnlyStaticMapProbeTests(unittest.TestCase):

    def test_realistic_target_requires_path_dimension_and_hash(self):
        raw = _server_map(20002)
        targets = parse_targets(_report(raw))
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0].floor_id, 20002)
        self.assertEqual((targets[0].width, targets[0].height), (2, 1))
        self.assertEqual(targets[0].sha256, hashlib.sha256(raw).hexdigest())

    def test_static_map_and_mapset_close_collision_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "server"
            (server / "dungeon").mkdir(parents=True)
            raw = _server_map(20002)
            (server / "dungeon" / "floor").write_bytes(raw)
            mapset = root / "mapset.txt"
            mapset.write_bytes(
                b"\n".join(
                    [
                        b"1 x x 1 0",
                        b"2 x x 1 0",
                        b"10 x x 1 0",
                        b"11 x x 0 0",
                    ]
                )
            )
            audit = analyze(
                payload_report_text=_report(raw),
                server_map_root=server,
                mapset_path=mapset,
            )
            self.assertEqual(audit.counts["target_floors"], 1)
            self.assertEqual(audit.counts["total_cells"], 2)
            self.assertEqual(
                audit.counts["floors_with_missing_image_metadata"],
                0,
            )
            self.assertEqual(audit.counts["ordinary_walkable_cells"], 1)
            self.assertEqual(audit.rows[0].server_map_sha256, hashlib.sha256(raw).hexdigest())

    def test_server_payload_hash_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "server"
            (server / "dungeon").mkdir(parents=True)
            raw = _server_map(20002)
            (server / "dungeon" / "floor").write_bytes(raw + b"x")
            mapset = root / "mapset.txt"
            mapset.write_bytes(b"1 x x 1 0\n")
            with self.assertRaisesRegex(ValueError, "SHA drift"):
                analyze(
                    payload_report_text=_report(raw),
                    server_map_root=server,
                    mapset_path=mapset,
                )


if __name__ == "__main__":
    unittest.main()
