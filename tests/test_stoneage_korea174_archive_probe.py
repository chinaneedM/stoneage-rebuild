import unittest

from tools.stoneage_korea174_archive_probe import (
    ARCHIVE_TIMEOUT_SECONDS,
    DOWNLOAD_EXT,
    INTEREST,
    REQUEST_TIMEOUT_SECONDS,
    ROOT_SNAPSHOT_LIMIT,
    LinkParser,
    classify_probe_result,
    decode_html,
    parse_availability_closest,
    parse_arquivo_cdx,
    safe,
    select_launch_snapshots,
)


class Korea174ArchiveProbeTests(unittest.TestCase):
    def test_download_extensions(self):
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/stoneage.exe"))
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client.zip?x=1"))
        self.assertIsNone(DOWNLOAD_EXT.search("http://x/index.asp"))

    def test_interest_terms(self):
        self.assertIsNotNone(INTEREST.search("스톤에이지 클라이언트 다운로드"))
        self.assertIsNotNone(INTEREST.search("StoneAge patch"))
        self.assertIsNone(INTEREST.search("generic portal"))

    def test_link_parser(self):
        parser=LinkParser()
        parser.feed('<a href="pds/client.exe">스톤에이지 다운로드</a>')
        self.assertEqual(
            parser.links,
            [("pds/client.exe","스톤에이지 다운로드")],
        )

    def test_decode_html_cp949(self):
        text="스톤에이지"
        self.assertEqual(decode_html(text.encode("cp949")),text)

    def test_launch_snapshot_selection_prefers_july_to_september_2003(self):
        rows=[
            {"timestamp":"20030601000000","original":"http://game3.netmarble.net/stoneage/"},
            {"timestamp":"20030728000000","original":"http://game3.netmarble.net/stoneage/"},
            {"timestamp":"20030901000000","original":"http://game3.netmarble.net/stoneage/"},
        ]
        selected=select_launch_snapshots(rows,limit=3)
        self.assertEqual(
            [row["timestamp"] for row in selected],
            ["20030728000000","20030901000000","20030601000000"],
        )

    def test_safe_caps_and_removes_controls(self):
        out=safe("a\x00b"+("x"*1000))
        self.assertNotIn("\x00",out)
        self.assertLessEqual(len(out),500)

    def test_archive_request_budget_is_bounded(self):
        self.assertLessEqual(REQUEST_TIMEOUT_SECONDS,15)
        self.assertLessEqual(ARCHIVE_TIMEOUT_SECONDS,20)
        self.assertLessEqual(ROOT_SNAPSHOT_LIMIT,3)

    def test_arquivo_ndjson_is_normalized(self):
        raw=(
            b'{"timestamp":"20030728000000",'
            b'"url":"http://stoneage.netmarble.net/client/sa.exe",'
            b'"status":"200","mime":"application/octet-stream",'
            b'"digest":"ABC","length":"123"}\n'
        )
        self.assertEqual(
            parse_arquivo_cdx(raw),
            [{
                "timestamp":"20030728000000",
                "original":"http://stoneage.netmarble.net/client/sa.exe",
                "statuscode":"200",
                "mimetype":"application/octet-stream",
                "digest":"ABC",
                "length":"123",
            }],
        )

    def test_availability_closest_is_normalized(self):
        self.assertEqual(
            parse_availability_closest(
                {
                    "archived_snapshots":{
                        "closest":{
                            "available":True,
                            "status":"200",
                            "timestamp":"20030728010203",
                            "url":"http://web.archive.org/web/20030728010203/http://x/",
                        }
                    }
                }
            ),
            {
                "timestamp":"20030728010203",
                "status":"200",
                "url":"http://web.archive.org/web/20030728010203/http://x/",
            },
        )
        self.assertIsNone(
            parse_availability_closest({"archived_snapshots":{}})
        )

    def test_probe_result_distinguishes_outage_from_no_hits(self):
        self.assertEqual(
            classify_probe_result(
                hit_count=0,successful_queries=0,failed_queries=12
            ),
            "INCONCLUSIVE",
        )
        self.assertEqual(
            classify_probe_result(
                hit_count=0,successful_queries=3,failed_queries=9
            ),
            "PARTIAL_NO_HITS",
        )
        self.assertEqual(
            classify_probe_result(
                hit_count=0,successful_queries=12,failed_queries=0
            ),
            "BOUNDED_NO_HITS",
        )
        self.assertEqual(
            classify_probe_result(
                hit_count=1,successful_queries=1,failed_queries=11
            ),
            "HITS",
        )


if __name__=="__main__":
    unittest.main()
