import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_supplemental_world_audit_probe import (
    DUPLICATE_DIVERGENT,
    DUPLICATE_IDENTICAL,
    UNIQUE,
    analyze,
    parse_supplemental_targets,
)


def _ls2map(floor, tile=1, obj=10):
    header = (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", 1, 1)
    )
    return header + struct.pack(">HH", tile, obj)


def _reachability():
    return "\n".join(
        [
            "SEMANTIC_SOURCE_VERSION|recovered25",
            "EVIDENCE_ROLE|LATER_RECOVERED",
            "COUNT|supplemental_floor_ids|3",
            (
                "SUPPLEMENTAL_FLOOR|floor=100|depth=1|status=CHANGED|"
                "server_map=1|client_dat=1|client_map=1|"
                "incoming_reachable_warps=2|outgoing_runtime_warps=3"
            ),
            (
                "SUPPLEMENTAL_FLOOR|floor=200|depth=2|"
                "status=CLIENT_DAT_PRESENT_NONSTABLE|server_map=1|"
                "client_dat=1|client_map=1|incoming_reachable_warps=1|"
                "outgoing_runtime_warps=1"
            ),
            (
                "SUPPLEMENTAL_FLOOR|floor=300|depth=3|status=SERVER_ONLY|"
                "server_map=1|client_dat=0|client_map=0|"
                "incoming_reachable_warps=1|outgoing_runtime_warps=0"
            ),
            "RESOLUTION|RECOVERED_RUNTIME_CLASSIC_WARP_REACHABILITY_CLOSED",
        ]
    )


class SupplementalWorldAuditProbeTests(unittest.TestCase):

    def test_reachability_parser_closes_declared_floor_set(self):
        rows = parse_supplemental_targets(_reachability())
        self.assertEqual([row.floor_id for row in rows], [100, 200, 300])

    def test_unique_identical_duplicate_and_divergent_duplicate_are_separated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            maps = root / "maps"
            npc = root / "npc"
            data = root / "data"
            maps.mkdir()
            npc.mkdir()
            data.mkdir()

            (maps / "a").mkdir()
            (maps / "b").mkdir()
            (maps / "c").mkdir()

            # floor 100: one copy.
            (maps / "a" / "100").write_bytes(_ls2map(100))

            # floor 200: two byte-identical copies.
            raw200 = _ls2map(200, tile=2, obj=11)
            (maps / "a" / "200").write_bytes(raw200)
            (maps / "b" / "200").write_bytes(raw200)

            # floor 300: divergent duplicate copies.
            (maps / "a" / "300").write_bytes(_ls2map(300, tile=3, obj=12))
            (maps / "c" / "300").write_bytes(_ls2map(300, tile=4, obj=13))

            mapset = root / "mapset.txt"
            mapset.write_bytes(
                b"\n".join(
                    [
                        b"1 x x 1 0",
                        b"2 x x 1 0",
                        b"3 x x 1 0",
                        b"4 x x 1 0",
                        b"10 x x 1 0",
                        b"11 x x 0 0",
                        b"12 x x 1 0",
                        b"13 x x 1 0",
                    ]
                )
            )

            with patch(
                "tools.stoneage_supplemental_world_audit_probe._npc_floor_counts",
                return_value=({100: 2, 200: 1}, {100: 1}),
            ), patch(
                "tools.stoneage_supplemental_world_audit_probe."
                "_encounter_floor_counts",
                return_value=("encount.txt", {200: 3}, {200: 2}),
            ):
                audit = analyze(
                    reachability_text=_reachability(),
                    server_map_root=maps,
                    mapset_path=mapset,
                    npc_dir=npc,
                    data_dir=data,
                    setup=None,
                )

            by_id = {row.target.floor_id: row for row in audit.floors}
            self.assertEqual(by_id[100].copy_status, UNIQUE)
            self.assertTrue(by_id[100].static_materializable)
            self.assertEqual(by_id[200].copy_status, DUPLICATE_IDENTICAL)
            self.assertTrue(by_id[200].static_materializable)
            self.assertEqual(by_id[300].copy_status, DUPLICATE_DIVERGENT)
            self.assertFalse(by_id[300].static_materializable)
            self.assertIsNone(by_id[300].ordinary_walkable_cells)

            self.assertEqual(
                audit.counts["server_copy_status:UNIQUE:ids"],
                1,
            )
            self.assertEqual(
                audit.counts["server_copy_status:DUPLICATE_IDENTICAL:ids"],
                1,
            )
            self.assertEqual(
                audit.counts["server_copy_status:DUPLICATE_DIVERGENT:ids"],
                1,
            )
            self.assertEqual(audit.counts["static_materializable_floors"], 2)
            self.assertEqual(audit.counts["npc_create_count"], 3)
            self.assertEqual(audit.counts["encounter_rows"], 3)

    def test_missing_mapset_metadata_keeps_floor_unmaterialized(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            maps = root / "maps"
            npc = root / "npc"
            data = root / "data"
            maps.mkdir()
            npc.mkdir()
            data.mkdir()
            (maps / "100").write_bytes(_ls2map(100, tile=999, obj=10))
            (maps / "200").write_bytes(_ls2map(200, tile=1, obj=10))
            (maps / "300").write_bytes(_ls2map(300, tile=1, obj=10))
            mapset = root / "mapset.txt"
            mapset.write_bytes(b"1 x x 1 0\n10 x x 1 0\n")

            with patch(
                "tools.stoneage_supplemental_world_audit_probe._npc_floor_counts",
                return_value=({}, {}),
            ), patch(
                "tools.stoneage_supplemental_world_audit_probe."
                "_encounter_floor_counts",
                return_value=("encount.txt", {}, {}),
            ):
                audit = analyze(
                    reachability_text=_reachability(),
                    server_map_root=maps,
                    mapset_path=mapset,
                    npc_dir=npc,
                    data_dir=data,
                    setup=None,
                )

            by_id = {row.target.floor_id: row for row in audit.floors}
            self.assertFalse(by_id[100].static_materializable)
            self.assertEqual(by_id[100].missing_image_ids, 1)


if __name__ == "__main__":
    unittest.main()
