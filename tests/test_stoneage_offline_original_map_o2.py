"""O2: only public contract and synthetic denial tests; no proprietary pixels in CI."""
import json
from pathlib import Path
import tempfile
import unittest

from tools import stoneage_offline_original_map_o2 as o2


class PrivateO2(unittest.TestCase):
    def test_historical_source_contract_and_finite_map(self):
        report = o2.inspect_public()
        self.assertEqual(report["schema"], "stoneage.scene21.original_town1000_common_prefix_observer.r1")
        self.assertEqual((len(report["cells"]), len(report["placements"]), len(report["resources"]),
                          len(report["frames"])), (77, 85, 56, 8))
        self.assertEqual(report["remaining_unresolved_map_image_keys"], [])
        self.assertFalse(report["original_world_entered"])
        self.assertFalse(report["same_official_deployed_build_authenticated"])
        self.assertFalse(report["native_palette_selection_verified"])

    def test_empty_output_and_disjoint_private_paths_required(self):
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            source = folder / "evidence"
            out = folder / "private-output"
            source.mkdir()
            out.mkdir()
            self.assertEqual(o2.safe_directories(source, out), (source.resolve(), out.resolve()))
            with self.assertRaises(ValueError):
                o2.safe_directories(source, source)
            (out / "old").write_bytes(b"keep")
            with self.assertRaisesRegex(ValueError, "empty"):
                o2.safe_directories(source, out)
            self.assertEqual((out / "old").read_bytes(), b"keep")

    def test_nested_and_public_source_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            source = Path(root) / "source"
            source.mkdir()
            nested = source / "inside"
            nested.mkdir()
            with self.assertRaises(ValueError):
                o2.safe_directories(source, nested)
            with self.assertRaises(ValueError):
                o2.safe_directories(o2.ROOT, source)

    def test_missing_or_forged_private_bundle_not_accepted(self):
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            with self.assertRaises(ValueError):
                o2.verify_private(folder)
            (folder / "source-derived-report.json").write_text(
                '{"schema":"stoneage.scene21.original_town1000_common_prefix_observer.r1"}')
            with self.assertRaisesRegex(ValueError, "differs"):
                o2.verify_private(folder)
            (folder / "source-derived-report.json").write_bytes(o2.scene.REPORT.read_bytes())
            with self.assertRaisesRegex(ValueError, "private-original-subset.zip"):
                o2.verify_private(folder)

    def test_landing_version_boundary(self):
        receipt = {"schema": o2.SCHEMA}
        html = o2.landing_html(receipt)
        for required in ("mixed25", "不能标成官方台湾1.0", "不是原游戏世界",
                         "56个解码原图", "zh-CN", "map-o2-receipt.json"):
            self.assertIn(required, html)
        self.assertNotIn('href="https:', html)
        with self.assertRaises(ValueError):
            o2.landing_html({"schema": "forged"})

    def test_no_original_exe_server_or_network_path(self):
        code = Path(o2.__file__).read_text(encoding="utf-8")
        for forbidden in ("subprocess", "urllib.request", "requests.get", "socket.", "http.client"):
            self.assertNotIn(forbidden, code)
        self.assertIn('"original_game_world_entered": False', code)
        self.assertIn('"authentic_TW1_deployed_map_verified": False', code)


if __name__ == "__main__":
    unittest.main()
