import unittest

from tools.stoneage_cnet_exact_record_probe import (
    Parser,
    closest,
    decode,
    normalize,
    sparse_snippets,
)


class CnetExactRecordProbeTests(unittest.TestCase):
    def test_closest(self):
        payload = {"archived_snapshots":{"closest":{
            "available":True,"timestamp":"20001110044200","status":"200","url":"x"
        }}}
        self.assertEqual(closest(payload), ("20001110044200","200","x"))
        self.assertIsNone(closest({"archived_snapshots":{}}))

    def test_decode_korean(self):
        self.assertIn("스톤에이지", decode("스톤에이지 다운로드".encode("cp949")))

    def test_parser_and_normalize(self):
        p = Parser()
        p.feed('<a href="/files/stoneage.exe">Stoneage 다운로드</a>')
        self.assertEqual(len(p.links), 1)
        self.assertEqual(
            normalize("http://korea.cnet.com/downloads/File.asp", p.links[0][2]),
            "http://korea.cnet.com/files/stoneage.exe",
        )

    def test_sparse_snippets(self):
        rows = sparse_snippets(["hello world", "파일 용량 32MB", "Stoneage"])
        self.assertIn("파일 용량 32MB", rows)
        self.assertIn("Stoneage", rows)
        self.assertNotIn("hello world", rows)


if __name__ == "__main__":
    unittest.main()
