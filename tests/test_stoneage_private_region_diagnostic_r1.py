"""Synthetics assert map-ID diagnostics cannot masquerade as historical pixels."""
import json
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
from tools.stoneage_private_region_diagnostic_r1 import build, export_private


def sample(server=False):
    ev = None if server else (3, 0, 1, 0)
    kind = "SERVER_LS2MAP_TWO_PLANE" if server else "CLIENT_DAT_THREE_PLANE"
    stat = "ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE" if server else "RECOVERED_CLIENT_DAT"
    area = SimpleNamespace(
        floor_id=104, map_width=2, map_height=2, x1=0, y1=0, x2=1, y2=1,
        tile_ids=(1, 2, 1, 3), object_ids=(0, 22, 0, 32), event_ids=ev,
        source_kind=kind, event_plane_status=stat, payload_sha256="a" * 64)
    req = SimpleNamespace(floor_id=104, x1=0, y1=0, x2=1, y2=1, world_profile="recovered25")
    prov = dict(
        content_role="LATER_RECOVERED", evidence_role="LATER_RECOVERED",
        world_profile="recovered25", payload_sha256="a" * 64,
        payload_kind=kind, event_plane_status=stat, source_versions=("mixed25",))
    return SimpleNamespace(payload=area, request=req, provenance=prov)


class PrivateMapCellDiagnosticTests(unittest.TestCase):
    def test_client_event_preserved_and_png_synthetic(self):
        raw, report = build(sample())
        self.assertTrue(raw.startswith(b"\x89PNG"))
        self.assertIn(b"NOT ORIGINAL STONEAGE GAME PIXELS", raw)
        self.assertEqual(report["observed_nonzero_event_ids"], [[1, 1], [3, 1]])
        self.assertEqual(report["viewport_dimensions"], [2, 2])
        self.assertEqual(report["cell_count"], 4)
        self.assertFalse(report["source_artwork_rendered"])
        self.assertFalse(report["original_game_world_entered"])
        self.assertEqual(struct.unpack_from(">II", raw, 16), (24, 24))

    def test_server_event_stays_absent_not_zero(self):
        _, report = build(sample(server=True))
        self.assertIsNone(report["observed_nonzero_event_ids"])
        self.assertIsNone(report["cells"][0]["event_id"])
        self.assertEqual(report["event_marker"], "ABSENT_NOT_ZERO")

    def test_no_event_forgery(self):
        obj = sample(server=True)
        obj.payload.event_ids = (0, 0, 0, 0)
        with self.assertRaises(ValueError):
            build(obj)

    def test_wrong_sha(self):
        obj = sample()
        obj.provenance["payload_sha256"] = "b" * 64
        with self.assertRaises(ValueError):
            build(obj)

    def test_wrong_provenance(self):
        for field, value in [
            ("content_role", "TW1_DIRECT"),
            ("evidence_role", "TW1_DIRECT"),
            ("world_profile", "tw1"),
        ]:
            obj = sample()
            obj.provenance[field] = value
            with self.assertRaises(ValueError):
                build(obj)

    def test_region_request_mismatch(self):
        obj = sample()
        obj.request.x1 = 1
        with self.assertRaises(ValueError):
            build(obj)

    def test_overwide(self):
        obj = sample()
        obj.payload.x2 = 64
        obj.request.x2 = 64
        obj.payload.map_width = 65
        obj.payload.tile_ids = tuple(range(65)) * 2
        obj.payload.object_ids = (0,) * 130
        obj.payload.event_ids = (0,) * 130
        with self.assertRaises(ValueError):
            build(obj)

    def test_bad_ids(self):
        for invalid in (-1, 65536, "1"):
            obj = sample()
            obj.payload.tile_ids = (1, invalid, 1, 3)
            with self.assertRaises(ValueError):
                build(obj)

    def test_output_and_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)
            manifest = export_private(path, sample())
            meta = json.loads(manifest.read_text())
            self.assertEqual(meta["interface_language"], "zh-CN")
            self.assertTrue((path / "tile-id-diagnostic.png").exists())
            with self.assertRaises(ValueError):
                export_private(path, sample())
            self.assertTrue(manifest.exists())


if __name__ == "__main__":
    unittest.main()
