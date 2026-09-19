import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_netpower_latin_token_probe import (
    analyze,
    classify,
    emit,
)


class NetPowerLatinTokenProbeTests(unittest.TestCase):
    def test_classify_sparse_tokens(self):
        text = (
            "StoneAge download www.stoneage.enium.co.kr/client/setup.exe "
            "setup.exe 123 MB Hananet CNET"
        )
        hits = classify(text)
        self.assertIn(("keyword", "StoneAge"), hits)
        self.assertTrue(any(k == "url" and "enium.co.kr" in v for k, v in hits))
        self.assertIn(("file", "setup.exe"), hits)
        self.assertIn(("size", "123 MB"), hits)

    def test_cross_psm_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "page87_psm6.txt").write_text(
                "www.stoneage.enium.co.kr client.exe",
                encoding="utf-8",
            )
            (root / "page87_psm11.txt").write_text(
                "www.stoneage.enium.co.kr client.exe",
                encoding="utf-8",
            )
            files, evidence = analyze(root)
            self.assertEqual(files, 2)
            self.assertEqual(
                evidence[(87, "file", "client.exe")],
                {6, 11},
            )

    def test_emit_does_not_include_unmatched_full_text(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            secret = "this-is-unrelated-long-ocr-prose"
            (root / "page88_psm6.txt").write_text(
                secret + " setup.exe",
                encoding="utf-8",
            )
            files, evidence = analyze(root)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(files, evidence)
            rendered = out.getvalue()
            self.assertNotIn(secret, rendered)
            self.assertIn("setup.exe", rendered)


if __name__ == "__main__":
    unittest.main()
