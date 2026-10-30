"""O2: only public contract and synthetic denial tests; no proprietary pixels in CI."""
import json
import io
import base64
import zipfile
from unittest.mock import patch
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


    def test_synthetic_complete_private_bridge_and_corruption(self):
        """Exercise all O2 output edges with generated pixels, never a game sprite."""
        from PIL import Image
        rgb = b"\x19\x37\x55\xff"
        png_out = io.BytesIO()
        Image.new("RGBA", (2, 2), (25, 55, 85, 255)).save(png_out, format="PNG")
        png = png_out.getvalue()
        raw_image = Image.open(io.BytesIO(png)).convert("RGBA").tobytes()
        pixels = b"\x00"
        dat = b"D" * 153608
        palette = b"P" * 708
        rds = {i: ("RD" + str(i)).encode() for i in range(1, 57)}
        names = [f"expanded_parts{p}_npc{n}" for p in (0, 1) for n in (0, 1)]
        names += [f"old_parts{p}_npc{n}" for p in (0, 1) for n in (0, 1)]
        resources = {str(i): {
            "size": len(data), "width": 1, "height": 1,
            "RD_sha256": o2.digest(data),
            "index_sha256": o2.digest(pixels),
            "RGBA_candidate_sha256": o2.digest(rgb),
        } for i, data in rds.items()}
        manifest = {
            "resources": resources, "cells": [{"xy": [0, 0]}] * 77,
            "placements": [{"image_key": 1}] * 85,
            "NPC_cell_original_three_u16": [0, 0, 0],
            "origin": [0, 0], "canvas_size": [2, 2],
            "source_map_sha256": o2.digest(dat),
            "source_palette_sha256": o2.digest(palette),
            "frames": {n: {"PNG_sha256": o2.digest(png),
                            "RGBA_sha256": o2.digest(raw_image)} for n in names}
        }
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            src, dst = root / "evidence", root / "out"
            src.mkdir()
            dst.mkdir()
            (src / "source-derived-report.json").write_text(json.dumps(manifest))
            with zipfile.ZipFile(src / "private-original-subset.zip", "w") as z:
                z.writestr("1000.DAT", dat)
                z.writestr("Palet_1.sap", palette)
                for i, content in rds.items():
                    z.writestr(str(i) + ".rd", content)
            for n in names:
                (src / (n + ".png")).write_bytes(png)
            model = {"report": manifest, "frames": {
                n: base64.b64encode(png).decode("ascii") for n in names
            }}
            template = o2.VIEW_TEMPLATE.read_text(encoding="utf-8")
            viewer = template.replace("__PRIVATE_SCENE_JSON__",
                                      json.dumps(model, separators=(",", ":")))
            (src / o2.SCENE_HTML).write_text(viewer, encoding="utf-8")
            with patch.object(o2, "inspect_public", return_value=manifest), \
                 patch.object(o2.scene, "map_cells",
                              return_value=(manifest["cells"], manifest["placements"], [0, 0, 0])), \
                 patch.object(o2.scene, "render",
                              return_value=Image.new("RGBA", (2, 2), (25, 55, 85, 255))), \
                 patch("tools.stoneage_rd_codec.decode_rd_block",
                       return_value=({}, pixels)), \
                 patch("tools.stoneage_scene14_independent_replay.decode",
                       return_value=(1, 1, pixels)), \
                 patch("tools.stoneage_tw10_palette.initial_rgb", return_value=[]), \
                 patch("tools.stoneage_private_scene_palette_r3.candidate_rgba", return_value=rgb):
                receipt = o2.emit(src, dst)
                self.assertEqual(receipt["original_RD_images_independently_decoded"], 56)
                self.assertEqual(receipt["source_original_map_image_occurrences_verified"], 85)
                self.assertFalse(receipt["authentic_TW1_deployed_map_verified"])
                self.assertEqual(len(list((dst / "frames").glob("*.png"))), 8)
                self.assertIn("mixed25", (dst / "index.html").read_text())
                self.assertEqual((dst / o2.SCENE_HTML).read_bytes(), viewer.encode("utf-8"))
                (src / (names[0] + ".png")).write_bytes(b"forged")
                with self.assertRaisesRegex(ValueError, "private PNG digest mismatch"):
                    o2.verify_private(src)


if __name__ == "__main__":
    unittest.main()
