import io
import unittest
from types import SimpleNamespace
from tools.stoneage_private_scene_source_r2 import bounded_copy, select_headers, SELECTED, PREFIX

class SourceStreamTests(unittest.TestCase):
    def test_exact_stream(self):
        import hashlib
        out = io.BytesIO()
        row = bounded_copy(io.BytesIO(b"abc"), out, 3, hashlib.sha256(b"abc").hexdigest())
        self.assertEqual(out.getvalue(), b"abc")
        self.assertEqual(row["bytes"], 3)

    def test_truncated_source(self):
        with self.assertRaisesRegex(ValueError, "short"):
            bounded_copy(io.BytesIO(b"ab"), io.BytesIO(), 3)

    def test_oversize_source(self):
        out = io.BytesIO()
        with self.assertRaisesRegex(ValueError, "budget"):
            bounded_copy(io.BytesIO(b"abcd"), out, 3)
        self.assertEqual(out.getvalue(), b"")

    def test_same_size_wrong_source(self):
        with self.assertRaisesRegex(ValueError, "SHA256"):
            bounded_copy(io.BytesIO(b"abc"), io.BytesIO(), 3, "0" * 64)

    def headers(self):
        return [SimpleNamespace(filename=PREFIX+name, file_size=pin[0], flags=0)
                for name, pin in SELECTED.items()]

    def test_case_preserves_exact_archive_name(self):
        entries = self.headers()
        entries[-1].filename = PREFIX + "map/1001.DAT"
        self.assertEqual(select_headers(entries)["map/1001.dat"], PREFIX + "map/1001.DAT")

    def test_duplicate_original_refused(self):
        entries = self.headers()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            select_headers(entries + entries[:1])

    def test_solid_or_encrypted_refused(self):
        for flag in (1, 2, 4, 16):
            entries = self.headers()
            entries[0].flags = flag
            with self.assertRaisesRegex(ValueError, "split/encrypted/solid"):
                select_headers(entries)

    def test_missing_member_refused(self):
        with self.assertRaisesRegex(ValueError, "absent"):
            select_headers(self.headers()[:-1])

    def test_wrong_extent_refused(self):
        entries = self.headers()
        entries[0].file_size += 1
        with self.assertRaisesRegex(ValueError, "extent"):
            select_headers(entries)

if __name__ == "__main__":
    unittest.main()
