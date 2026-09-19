import os
import tempfile
import unittest

from tools.stoneage_tw2000_clean_client_acceptance import (
    EXPECTED_BIN_SIZE,
    EXPECTED_RAR_MD5,
    EXPECTED_RAR_SHA1,
    file_hashes,
    pe_header,
)


class TaiwanCleanClientAcceptanceTests(unittest.TestCase):
    def test_pinned_preservation_identity(self):
        self.assertEqual(EXPECTED_BIN_SIZE, 523_449_360)
        self.assertEqual(EXPECTED_RAR_MD5, "b37a4a47f4eb608cac67e4ddf7a1621a")
        self.assertEqual(EXPECTED_RAR_SHA1, "b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded")

    def test_file_hashes(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"abc")
            path = f.name
        try:
            size, md5, sha1, sha256 = file_hashes(path)
            self.assertEqual(size, 3)
            self.assertEqual(md5, "900150983cd24fb0d6963f7d28e17f72")
            self.assertEqual(sha1, "a9993e364706816aba3e25717850c26c9cd0d89d")
            self.assertEqual(
                sha256,
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )
        finally:
            os.unlink(path)

    def test_pe_header_non_pe(self):
        self.assertIsNone(pe_header(b"not a pe"))


if __name__ == "__main__":
    unittest.main()
