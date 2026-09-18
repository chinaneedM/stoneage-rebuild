import contextlib
import io
import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_resource_probe import analyze_maps, analyze_real_adrn, emit


class StoneAgeResourceProbeTests(unittest.TestCase):
    def test_real_adrn_and_map_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real.bin"
            adrn = root / "adrn.bin"
            map_dir = root / "map"
            map_dir.mkdir()

            blocks = []
            records = []
            offset = 0
            for bitmapno, width, height, flag in [
                (1, 2, 3, 0),
                (2, 5, 4, 1),
                (3, 10, 10, 2),
            ]:
                payload = bytes([bitmapno]) * (10 + bitmapno)
                size = 16 + len(payload)
                block = (
                    b"RD"
                    + bytes([flag, 0])
                    + struct.pack("<III", width, height, size)
                    + payload
                )
                blocks.append(block)
                records.append(
                    struct.pack(
                        "<IIIiiii",
                        bitmapno,
                        offset,
                        size,
                        0,
                        0,
                        width,
                        height,
                    )
                    + bytes(80 - 28)
                )
                offset += size

            real.write_bytes(b"".join(blocks))
            adrn.write_bytes(b"".join(records))
            (map_dir / "100.MAP").write_bytes(
                struct.pack("<II", 2, 3) + bytes(2 * 3 * 2)
            )
            (map_dir / "200.MAP").write_bytes(
                struct.pack("<II", 5, 4) + bytes(5 * 4 * 2)
            )
            nested = map_dir / "nested"
            nested.mkdir()
            (nested / "lower.map").write_bytes(
                struct.pack("<II", 3, 2) + bytes(3 * 2 * 2)
            )

            ra = analyze_real_adrn(adrn, real)
            mp = analyze_maps(map_dir)

            self.assertEqual(ra["record_count"], 3)
            self.assertEqual(ra["remainder"], 0)
            self.assertEqual(ra["counts"]["rd_magic"], 3)
            self.assertEqual(ra["counts"]["size_match"], 3)
            self.assertEqual(ra["counts"]["dimension_bits_match"], 3)
            self.assertEqual(ra["counts"]["signed_dimension_match"], 3)
            self.assertEqual(mp["file_count"], 3)
            self.assertEqual(mp["counts"]["exact_8_plus_whx2"], 3)
            self.assertEqual(ra["contiguous_active_offsets"], 2)
            self.assertEqual(ra["unreferenced_real_tail"], 0)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                emit(ra, mp)
            output = buf.getvalue()
            self.assertIn("ADRN_RECORD_SIZE|80", output)
            self.assertIn("MAP_EXACT_8_PLUS_WHX2|3", output)
            self.assertIn("CONTIGUOUS_ACTIVE_OFFSETS|2", output)


if __name__ == "__main__":
    unittest.main()
