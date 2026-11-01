"""O55 checks only public historical receipts and a private-file gate template.

No original proprietary pixel, map or script payload is used by these tests.
"""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "tools/stoneage_o55_two_scene_observer.html"
O17 = ROOT / "research/recovered/STONEAGE-O17-MAP1003-ACTUAL-PIXEL-CANDIDATE-R1.json"
O54 = ROOT / "research/recovered/STONEAGE-O54-VILLAGE-TO-PETSHOP-SOURCE-CORRIDOR-R1.json"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "script":
            self.scripts += 1


class O55SourceGateTests(unittest.TestCase):
    def test_two_original_candidate_pngs_match_saved_receipts(self):
        page = HTML.read_text(encoding="utf-8")
        o17 = json.loads(O17.read_text(encoding="utf-8"))
        o54 = json.loads(O54.read_text(encoding="utf-8"))
        self.assertIn(o17["candidate"]["combined_PNG_sha256"], page)
        self.assertIn(o54["private_frames"]["world"]["png_sha256"], page)
        for dims in (o17["candidate"]["canvas_dimensions"], o54["private_frames"]["world"]["dimensions"]):
            self.assertIn(f"width: {dims[0]}, height: {dims[1]}", page)
        self.assertFalse(o17["candidate"]["original_world_entered"])
        self.assertFalse(o54["not_proven"]["native_game_world_entered"])
        self.assertEqual(o17["map"]["dimensions"], [30, 30])
        self.assertEqual(o54["source_map"]["original_door_xy"], [[68, 72], [69, 72]])

    def test_no_original_art_or_online_service_ships_with_observer(self):
        page = HTML.read_text(encoding="utf-8")
        parser = Parser()
        parser.feed(page)
        self.assertEqual(parser.scripts, 1)
        self.assertTrue({"file-1000", "file-1003", "show-1000", "show-1003", "zoom", "scene-image"} <= parser.ids)
        self.assertIn("crypto.subtle.digest('SHA-256'", page)
        self.assertIn("URL.createObjectURL(file)", page)
        self.assertIn("default-src 'none'", page)
        self.assertNotIn("data:image/", page)
        self.assertNotIn("fetch(", page)
        self.assertNotIn("<img src=", page)
        self.assertLess(HTML.stat().st_size, 15000)

    def test_source_warning_and_stale_read_guard(self):
        page = HTML.read_text(encoding="utf-8")
        self.assertIn("不是", page)
        self.assertIn("不执行原游戏", page)
        self.assertIn("官方同部署", page)
        self.assertIn("if (revisions[id] !== revision) return", page)
        self.assertIn("if (actual !== sources[id].sha256)", page)
        self.assertIn("clearScene(id)", page)


if __name__ == "__main__":
    unittest.main()