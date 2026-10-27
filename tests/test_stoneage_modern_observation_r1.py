"""Source identity, Simplified Chinese UI and non-gameplay observer guards."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
import wave
import zlib

from tools.stoneage_modern_observation_manifest import (
    CLAIM, CUSTODY, SOURCE_PROFILES, UI_LANGUAGE,
    file_fingerprint, report, validate_report,
)

ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / "tools/modern-observation-viewer.html"


def png(width: int = 2, height: int = 2) -> bytes:
    def chunk(kind, payload):
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    head = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    scan = b"".join(b"\x00" + b"\x80" * width for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head) + chunk(b"IDAT", zlib.compress(scan)) + chunk(b"IEND", b"")


class ModernObservationR1(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        (self.root / "floor.png").write_bytes(png())
        (self.root / "figure.png").write_bytes(png(1, 3))
        with wave.open(str(self.root / "voice.wav"), "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(11025)
            f.writeframes(b"\0\0" * 100)

    def sample(self, region="CN_MAINLAND"):
        return report(region, [("map_png", self.root / "floor.png"),
                               ("character_png", self.root / "figure.png"),
                               ("wav", self.root / "voice.wav")])

    def test_all_source_regions_are_independent(self):
        self.assertEqual(set(SOURCE_PROFILES), {
            "TW_WAEI_1_0", "CN_MAINLAND", "JP_JSS", "KR_KOREA", "LATER_RECOVERED"})
        for name in SOURCE_PROFILES:
            r = self.sample(name)
            validate_report(r)
            self.assertEqual(r["source_profile"], name)
            self.assertEqual(r["display_language"], "zh-CN")
            self.assertFalse(r["original_world_entered"])

    def test_synthetic_files_have_sha_but_are_not_original_provenance(self):
        r = self.sample()
        self.assertEqual(r["observation_class"], CLAIM)
        self.assertEqual(len(r["files"]), 3)
        self.assertTrue(all(f["evidence_grade"] == CUSTODY for f in r["files"]))
        self.assertEqual(r["files"][0]["png"], {"width": 2, "height": 2})
        self.assertEqual(r["files"][2]["wav"]["hz"], 11025)
        self.assertTrue(all("path" not in f and "bytes" not in f for f in r["files"]))
        self.assertEqual(r["display_language"], UI_LANGUAGE)

    def test_region_cannot_be_silently_relabelled(self):
        r = self.sample("TW_WAEI_1_0")
        r["source_metadata"] = SOURCE_PROFILES["CN_MAINLAND"]
        with self.assertRaises(ValueError): validate_report(r)

    def test_modern_viewer_never_claims_original_world(self):
        for field in ("original_executable_launched", "original_world_entered",
                      "asset_version_provenance_authenticated", "original_server_data_authenticated",
                      "historical_NPC_pet_quest_binding_authenticated",
                      "region_text_production_translation_verified"):
            r = self.sample()
            r[field] = True
            with self.assertRaises(ValueError): validate_report(r)

    def test_reject_unsupported_movement_upgrade(self):
        r = self.sample()
        r["modern_rendered_movement"] = "AUTHENTIC_ORIGINAL_CLIENT_MOVEMENT"
        with self.assertRaises(ValueError): validate_report(r)

    def test_invalid_source_unknown_region(self):
        with self.assertRaises(ValueError):
            report("TW1_AS_CN", [("map_png", self.root / "floor.png")])

    def test_wrong_magic_and_oversized_pixels(self):
        f = self.root / "broken.png"
        f.write_bytes(b"BAD!" + b"\x00" * 30)
        with self.assertRaises(ValueError): file_fingerprint(f, "map_png")
        f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", 9000, 9000) + b"\x08\x00\x00\x00\x00" + b"\0" * 16)
        with self.assertRaises(ValueError): file_fingerprint(f, "map_png")

    def test_unsupported_suffix(self):
        f = self.root / "evil.exe"
        f.write_bytes(png())
        with self.assertRaises(ValueError): file_fingerprint(f, "map_png")

    def test_repeated_same_slot_fails(self):
        with self.assertRaises(ValueError):
            report("CN_MAINLAND", [("map_png", self.root / "floor.png")] * 2)

    def test_user_original_file_not_bundled_or_auto_published(self):
        html = VIEWER.read_text(encoding="utf-8")
        self.assertIn('lang="zh-CN"', html)
        self.assertIn("简体中文", html)
        self.assertIn("非原版游戏运行", html)
        self.assertIn("未进入历史服务器", html)
        self.assertIn("image-rendering:pixelated", html)
        self.assertIn("requestAnimationFrame(loop)", html)
        self.assertIn('id="actor"', html)
        self.assertIn('id="pet"', html)
        self.assertIn('id="floor"', html)
        self.assertIn('id="audio"', html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn("<img src=", html)
        self.assertNotIn("data:image/", html)
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("TW_WAEI_1_0", html)
        self.assertIn("CN_MAINLAND", html)
        self.assertIn("JP_JSS", html)
        self.assertIn("KR_KOREA", html)

    def test_source_bound_diagnostic_click_and_sha_guard_are_present(self):
        html = VIEWER.read_text(encoding="utf-8")
        self.assertIn('id="mapmeta"', html)
        self.assertIn('crypto.subtle.digest("SHA-256"', html)
        self.assertIn('m.source_version_role!=="LATER_RECOVERED"', html)
        self.assertIn('m.original_game_world_entered!==false', html)
        self.assertIn('server?c.event_id!==null', html)
        self.assertIn('mapDiagnostic.cells[y*w+x]', html)
        self.assertIn('mapDiagnostic&&selectedCell', html)
        self.assertNotIn('fetch(', html)

    def test_report_zero_files_rejected(self):
        with self.assertRaises(ValueError): report("TW_WAEI_1_0", [])

    def test_metadata_sha_tamper_detected(self):
        r = self.sample()
        r["files"][0]["sha256"] = "fake"
        with self.assertRaises(ValueError): validate_report(r)


if __name__ == "__main__":
    unittest.main()
