import unittest

from tools.stoneage_tw2000_preservation_probe import (
    EXPECTED_RAR_MD5,
    EXPECTED_RAR_SHA1,
    HTTPRangeFile,
    ITEM,
    RAR_NAME,
    REDUMP_URL,
)


class FakeRangeFile(HTTPRangeFile):
    def __init__(self, data):
        self.data = data
        self.url = "https://example.invalid/file.rar"
        self.size = len(data)
        self.pos = 0
        self.closed = False
        self.requests = 0
        self.bytes_read = 0
        self.final_url = self.url

    def read(self, size=-1):
        if self.closed:
            raise ValueError("closed")
        if self.pos >= self.size:
            return b""
        if size is None or size < 0:
            size = self.size - self.pos
        size = min(size, self.size - self.pos)
        out = self.data[self.pos:self.pos + size]
        self.pos += len(out)
        self.requests += 1
        self.bytes_read += len(out)
        return out


class TaiwanPreservationProbeTests(unittest.TestCase):
    def test_targets_are_exact(self):
        self.assertEqual(ITEM, "stoneage_tw_2000_win")
        self.assertEqual(RAR_NAME, "CD_DIC.rar")
        self.assertEqual(REDUMP_URL, "http://redump.org/disc/104630/")
        self.assertEqual(EXPECTED_RAR_MD5, "b37a4a47f4eb608cac67e4ddf7a1621a")
        self.assertEqual(EXPECTED_RAR_SHA1, "b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded")

    def test_seek_and_read_semantics(self):
        f = FakeRangeFile(b"0123456789")
        self.assertEqual(f.read(3), b"012")
        self.assertEqual(f.tell(), 3)
        self.assertEqual(f.seek(-2, 2), 8)
        self.assertEqual(f.read(2), b"89")
        self.assertEqual(f.seek(1, 0), 1)
        self.assertEqual(f.read(4), b"1234")


if __name__ == "__main__":
    unittest.main()
