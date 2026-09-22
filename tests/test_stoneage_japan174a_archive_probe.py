import unittest

from tools.stoneage_japan174a_archive_probe import (
    ARCHIVE_TIMEOUT_SECONDS,
    HANGAME_GAMANIA_STONEAGE_PATTERN,
    HANGAME_GAMANIA_STONEAGE_ROOT,
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
    snapshot_period,
)


class Japan174aArchiveProbeTests(unittest.TestCase):
    def test_download_extensions_include_period_formats(self):
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client/sa174a.exe"))
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client/stone.lzh?x=1"))
        self.assertIsNone(DOWNLOAD_EXT.search("http://x/index.html"))

    def test_interest_accepts_japanese_client_terms(self):
        self.assertIsNotNone(INTEREST.search("STONE AGE クライアント"))
        self.assertIsNotNone(INTEREST.search("ダウンロードはこちら"))
        self.assertIsNone(INTEREST.search("generic portal"))

    def test_link_parser_keeps_href_and_anchor(self):
        parser=LinkParser()
        parser.feed('<a href="files/client.exe">クライアント ダウンロード</a>')
        self.assertEqual(
            parser.links,
            [("files/client.exe","クライアント ダウンロード")],
        )

    def test_decode_html_supports_shift_jis(self):
        original="クライアント"
        self.assertEqual(decode_html(original.encode("cp932")),original)

    def test_launch_snapshot_selection_prefers_december_window(self):
        rows=[
            {"timestamp":"20040115000000","original":"http://stoneage.to/"},
            {"timestamp":"20030501000000","original":"http://stoneage.to/"},
            {"timestamp":"20031212000000","original":"http://stoneage.to/"},
        ]
        selected=select_launch_snapshots(rows,limit=3)
        self.assertEqual(
            [row["timestamp"] for row in selected],
            ["20031212000000","20040115000000","20030501000000"],
        )

    def test_snapshot_period_distinguishes_launch_from_other_pages(self):
        self.assertEqual(snapshot_period("20031214000000"),"launch")
        self.assertEqual(snapshot_period("20031125000000"),"prelaunch")
        self.assertEqual(snapshot_period("20040207000000"),"postlaunch")
        self.assertEqual(snapshot_period(""),"unknown")

    def test_safe_strips_controls_and_caps(self):
        value="a\x00b"+("x"*1000)
        out=safe(value)
        self.assertNotIn("\x00",out)
        self.assertLessEqual(len(out),500)

    def test_hangame_gamania_launch_directory_is_pinned(self):
        self.assertEqual(
            HANGAME_GAMANIA_STONEAGE_PATTERN,
            "hangame.gamania.co.jp/stoneage/*",
        )
        self.assertEqual(
            HANGAME_GAMANIA_STONEAGE_ROOT,
            "http://hangame.gamania.co.jp/stoneage/",
        )

    def test_archive_request_budget_is_bounded(self):
        self.assertLessEqual(REQUEST_TIMEOUT_SECONDS,15)
        self.assertLessEqual(ARCHIVE_TIMEOUT_SECONDS,20)
        self.assertLessEqual(ROOT_SNAPSHOT_LIMIT,3)

    def test_arquivo_ndjson_is_normalized(self):
        raw=(
            b'{"timestamp":"20031212000000",'
            b'"url":"http://stoneage.to/client/sa174a.exe",'
            b'"status":"200","mime":"application/octet-stream",'
            b'"digest":"ABC","length":"123"}\n'
        )
        self.assertEqual(
            parse_arquivo_cdx(raw),
            [{
                "timestamp":"20031212000000",
                "original":"http://stoneage.to/client/sa174a.exe",
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
                            "timestamp":"20031216010203",
                            "url":"http://web.archive.org/web/20031216010203/http://stoneage.to/",
                        }
                    }
                }
            ),
            {
                "timestamp":"20031216010203",
                "status":"200",
                "url":"http://web.archive.org/web/20031216010203/http://stoneage.to/",
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


if __name__ == "__main__":
    unittest.main()
