import hashlib
import struct
import unittest

from tools.stoneage_tw10_audio_metadata import parse_wave, sanitize


def make_wave(payload: bytes, *, channels=1, rate=11025, bits=8):
    block_align = channels * bits // 8
    byte_rate = rate * block_align
    fmt = struct.pack("<HHIIHH", 1, channels, rate, byte_rate, block_align, bits)
    body = (
        b"fmt " + struct.pack("<I", len(fmt)) + fmt
        + b"data" + struct.pack("<I", len(payload)) + payload
    )
    if len(payload) & 1:
        body += b"\x00"
    return b"RIFF" + struct.pack("<I", 4 + len(body)) + b"WAVE" + body


class TaiwanV10AudioMetadataTests(unittest.TestCase):
    def test_parse_wave(self):
        payload = b"\x01\x02\x03\x04"
        wave = parse_wave(make_wave(payload))
        self.assertEqual(wave["riff"], 1)
        self.assertEqual(wave["wave"], 1)
        self.assertEqual(wave["audio_format"], 1)
        self.assertEqual(wave["channels"], 1)
        self.assertEqual(wave["sample_rate"], 11025)
        self.assertEqual(wave["bits_per_sample"], 8)
        self.assertEqual(wave["data_size"], 4)
        self.assertEqual(wave["data_sha256"], hashlib.sha256(payload).hexdigest())
        self.assertIn("fmt :16", wave["chunk_signature"])
        self.assertIn("data:4", wave["chunk_signature"])

    def test_non_wave_is_explicit(self):
        wave = parse_wave(b"not a wave")
        self.assertEqual(wave["riff"], 0)
        self.assertEqual(wave["wave"], 0)
        self.assertEqual(wave["data_sha256"], "")

    def test_sanitize_report_delimiters(self):
        self.assertEqual(sanitize("a|b\nc"), "a%7Cb c")


if __name__ == "__main__":
    unittest.main()
