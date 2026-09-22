import unittest

from tools.stoneage_korea174_exact_download_probe import merge_snapshots


class Korea174ExactDownloadProbeTests(unittest.TestCase):
    def test_merge_keeps_early_exact_cdx_capture(self):
        rows=merge_snapshots(
            "http://x/down_load.asp",
            [
                {
                    "timestamp":"20030728010101",
                    "original":"http://x/down_load.asp",
                    "statuscode":"200",
                    "mimetype":"text/html",
                    "digest":"ABC",
                    "length":"123",
                }
            ],
            [],
        )
        self.assertEqual(rows[0]["timestamp"],"20030728010101")
        self.assertEqual(rows[0]["source"],"cdx")

    def test_merge_deduplicates_same_availability_capture(self):
        cap={
            "timestamp":"20060401000000",
            "status":"200",
            "url":"http://web.archive.org/web/20060401000000/http://x/",
        }
        rows=merge_snapshots("http://x/down_load.asp",[],[cap,cap])
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["source"],"availability")


if __name__=="__main__":
    unittest.main()
