import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_missing_warp_destination_payload_probe import (
    CLIENT_MAP_AND_SERVER_MAP_PRESENT,
    CLIENT_MAP_ONLY,
    classify,
    parse_missing_dat_destinations,
)


def _first_stage():
    return "\n".join(
        [
            "COUNT|status:CLIENT_DAT_MISSING:edges|2",
            "COUNT|status:CLIENT_DAT_MISSING:ids|2",
            "DESTINATION|floor=20002|edge_refs=1|status=CLIENT_DAT_MISSING|client_paths=",
            "DESTINATION|floor=20004|edge_refs=1|status=CLIENT_DAT_MISSING|client_paths=",
            "RESOLUTION|OUTSIDE_STABLE_WARP_DESTINATIONS_CLASSIFIED",
        ]
    )


def _client_map(floor_id):
    return struct.pack("<IIH", 1, 1, floor_id & 0xFFFF)


def _server_map(floor_id):
    header = (
        b"LS2MAP"
        + struct.pack(">H", floor_id)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", 1, 1)
    )
    return header + struct.pack(">HH", 1, 2)


class MissingWarpDestinationPayloadProbeTests(unittest.TestCase):

    def test_missing_dat_rows_are_closed_against_declared_counts(self):
        self.assertEqual(
            parse_missing_dat_destinations(_first_stage()),
            {20002: 1, 20004: 1},
        )

    def test_independent_client_map_and_server_surfaces_are_classified(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            client = root / "client"
            server = root / "server"
            client.mkdir()
            server.mkdir()

            (client / "20002.MAP").write_bytes(_client_map(20002))
            (client / "20004.MAP").write_bytes(_client_map(20004))
            (server / "a").mkdir()
            (server / "a" / "map20002").write_bytes(_server_map(20002))

            audit = classify(
                first_stage_text=_first_stage(),
                client_map_root=client,
                server_map_root=server,
            )
            by_id = {row.floor_id: row for row in audit.rows}

            self.assertEqual(
                by_id[20002].status,
                CLIENT_MAP_AND_SERVER_MAP_PRESENT,
            )
            self.assertEqual(by_id[20002].client_map_dimensions, ((1, 1),))
            self.assertEqual(by_id[20002].server_map_dimensions, ((1, 1),))
            self.assertEqual(len(by_id[20002].server_map_sha256), 1)
            self.assertEqual(len(by_id[20002].server_map_sha256[0]), 64)

            self.assertEqual(by_id[20004].status, CLIENT_MAP_ONLY)
            self.assertTrue(by_id[20004].client_map_present)
            self.assertFalse(by_id[20004].server_map_present)


if __name__ == "__main__":
    unittest.main()
