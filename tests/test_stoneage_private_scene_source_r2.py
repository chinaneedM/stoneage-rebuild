import io
import unittest
from tools.stoneage_private_scene_source_r2 import bounded_copy

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

if __name__ == "__main__":
    unittest.main()
