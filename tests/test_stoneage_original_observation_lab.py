"""All synthetic: never stores or invents the original licensed art/audio."""
import hashlib
import io
import json
import struct
import tempfile
import unittest
import wave
import zlib
from pathlib import Path

from tools.stoneage_original_observation_lab import (
    ROOT, MODE, PINNED, get_record, gray_png, build_bitmap,
    inspect_wav, safe_output, check_original, git_blob_hash
)

def sample_record(bitmapno=17, off=0, size=18, w=2, h=2):
    return struct.pack("<IIIiiii",bitmapno,off,size,0,0,w,h)+bytes(52)

def rd_rle():
    return b"RD"+bytes([1,0])+struct.pack("<III",2,2,18)+bytes([0x84,0x5a])

class OriginalObservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)
        self.adrn=self.path/"adrn.bin"
        self.real=self.path/"real.bin"
        self.adrn.write_bytes(sample_record())
        self.real.write_bytes(rd_rle())
        self.expected={
            "adrn_1.bin":(80,hashlib.sha256(self.adrn.read_bytes()).hexdigest()),
            "real_1.bin":(18,hashlib.sha256(self.real.read_bytes()).hexdigest()),
        }
    def test_synthetic_flag1_gray_preview_and_custody(self):
        data,c=build_bitmap(self.adrn,self.real,bitmapno=17,expected=self.expected)
        self.assertEqual(c["preview_mode"],MODE)
        self.assertFalse(c["original_colors_reproduced"])
        self.assertFalse(c["historical_gameplay_screenshot"])
        self.assertFalse(c["server_entity_binding_verified"])
        self.assertEqual(c["decoded_palette_index_sha256"],hashlib.sha256(bytes([0x5a]*4)).hexdigest())
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(data[25],0) # grayscale PNG color type
        self.assertEqual(zlib.decompress(data[41:-16]),b"\x00\x5a\x5a\x00\x5a\x5a")
    def test_index_selector_exact(self):
        data,c=build_bitmap(self.adrn,self.real,index=0,expected=self.expected)
        self.assertEqual(c["record"]["bitmapno"],17)
        self.assertEqual(c["record"]["index"],0)
    def test_corrupted_binary_rejected(self):
        self.real.write_bytes(rd_rle()[:-1]+b"\x00")
        with self.assertRaises(ValueError):
            build_bitmap(self.adrn,self.real,index=0,expected=self.expected)
    def test_duplicate_identity_rejected(self):
        self.adrn.write_bytes(sample_record()+sample_record())
        with self.assertRaises(ValueError):
            get_record(self.adrn,bitmapno=17)
    def test_bad_bounds_and_unknown_rejected(self):
        with self.assertRaises(ValueError):
            get_record(self.adrn,index=1)
        with self.assertRaises(ValueError):
            get_record(self.adrn,bitmapno=20)
        with self.assertRaises(ValueError):
            get_record(self.adrn,index=0,bitmapno=17)
    def test_original_source_pins_present(self):
        self.assertEqual(PINNED["real_1.bin"][0],315842228)
        self.assertEqual(PINNED["adrn_1.bin"][0],10079680)
        self.assertEqual(len(PINNED["real_1.bin"][1]),64)
    def test_reject_public_repo_asset_and_overwrite(self):
        with self.assertRaises(ValueError):
            safe_output(ROOT/"forbidden.png")
        f=self.path/"already.png";f.write_bytes(b"png")
        with self.assertRaises(ValueError):
            safe_output(f)
        self.assertEqual(safe_output(self.path/"new.png"),(self.path/"new.png").resolve())
    def test_reject_invalid_png(self):
        with self.assertRaises(ValueError):
            gray_png(b"\x01",2,2)
    def test_readonly_wav_source_structure(self):
        path=self.path/"sound.wav"
        with wave.open(str(path),"wb") as w:
            w.setnchannels(1);w.setsampwidth(1);w.setframerate(8000)
            w.writeframes(bytes([128]*80))
        expected={"StoneAge/data/se/test.wav":(path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest())}
        row=inspect_wav(path,"StoneAge/data/se/test.wav",expected=expected)
        self.assertEqual(row["format"]["sample_rate_hz"],8000)
        self.assertEqual(row["format"]["duration_seconds"],0.01)
        self.assertFalse(row["audio_played_or_heard_by_assistant"])
        with self.assertRaises(ValueError):
            inspect_wav(path,"StoneAge/data/se/unproven.wav",expected=expected)
    def test_git_hash_uses_content_prefix(self):
        self.assertEqual(git_blob_hash(b"test"),"30d74d258442c7c65512eafab474568dd706c430")

if __name__=="__main__":
    unittest.main()
