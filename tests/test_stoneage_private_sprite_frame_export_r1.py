"""Offline synthetic privacy/claim gates for source-qualified TW1-to-modern frame export."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from tools.stoneage_private_sprite_frame_export_r1 import export_private, unpack


def png():
    def chunk(name, body):
        data = name + body
        return struct.pack(">I", len(body)) + data + struct.pack(">I", zlib.crc32(data) & 0xffffffff)
    header = struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(b"\0\x7f")) + chunk(b"IEND", b"")


def source():
    raw = png()
    frame = {"bmp_no": 100}
    t = {"frames": [frame, frame]}
    image = "data:image/png;base64," + base64.b64encode(raw).decode()
    c = {"timeline": t, "bitmap_witnesses": [{
        "bitmapno": 100, "private_grayscale_png_sha256": hashlib.sha256(raw).hexdigest()}],
        "original_files": {"spr_1.bin": {"sha256": "a" * 64}}, "source_status": "SYNTHETIC_TEST_NOT_ORIGINAL"}
    html = '<script id="pack" type="application/json">' + json.dumps({"timeline": t, "images": {"100": image}}) + '</script>'
    return html, c


class PrivateFrameExport(unittest.TestCase):
    def test_original_pack_becomes_ordered_local_png_frames(self):
        h, c = source()
        frames = unpack(h, c)
        self.assertEqual([name for name, raw in frames], ["frame-000.png", "frame-001.png"])
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            manifest = export_private(out, frames, c)
            self.assertTrue(manifest.exists())
            meta = json.loads(manifest.read_text())
            self.assertEqual(meta["interface_language"], "zh-CN")
            self.assertTrue(meta["synthetic_preview_only"])
            self.assertFalse(meta["original_game_world_entered"])
            self.assertEqual(meta["source"], "TW_WAEI_1_0")

    def test_change_png_without_witness_rejected(self):
        h, c = source()
        c["bitmap_witnesses"][0]["private_grayscale_png_sha256"] = "f" * 64
        with self.assertRaises(ValueError): unpack(h, c)

    def test_change_timeline_rejected(self):
        h, c = source()
        c["timeline"]["frames"].append({"bmp_no": 999})
        with self.assertRaises(ValueError): unpack(h, c)

    def test_html_code_or_ambiguous_pack_rejected(self):
        h, c = source()
        with self.assertRaises(ValueError): unpack(h + h, c)
        with self.assertRaises(ValueError): unpack("<div/>", c)

    def test_existing_output_kept_safe(self):
        h, c = source()
        frames = unpack(h, c)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "existing").write_text("untouched")
            with self.assertRaises(ValueError): export_private(target, frames, c)
            self.assertEqual((target / "existing").read_text(), "untouched")

    def test_bad_filename_rejected(self):
        h, c = source()
        f = unpack(h, c)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                export_private(Path(directory), [("../outside.png", f[0][1])], c)


if __name__ == "__main__":
    unittest.main()
