import unittest

from tools.stoneage_wayback_snapshot_link_probe import (
    Link,
    classify_link,
    decode_html,
    extract_links,
    normalize_target,
    snapshot_url,
)


class WaybackSnapshotLinkProbeTests(unittest.TestCase):
    def test_decode_cp949_anchor(self):
        raw = '<a href="download/sa.exe">스톤에이지 다운로드</a>'.encode("cp949")
        text = decode_html(raw)
        self.assertIn("스톤에이지", text)

    def test_extract_and_classify_download(self):
        body = b'<html><a href="/files/stoneage.zip">StoneAge download</a></html>'
        links = extract_links(body, "http://example.test/downloads/")
        self.assertEqual(len(links), 1)
        kind, link, target = links[0]
        self.assertEqual(kind, "download")
        self.assertEqual(target, "http://example.test/files/stoneage.zip")
        self.assertEqual(link.label, "StoneAge download")

    def test_interest_non_download(self):
        link = Link("a", "href", "/stoneage/", "StoneAge")
        self.assertEqual(
            classify_link(link, "http://example.test/stoneage/"),
            "interest",
        )

    def test_normalize_ignores_script_and_unwraps_wayback(self):
        self.assertEqual(normalize_target("http://a/", "javascript:void(0)"), "")
        wrapped = "https://web.archive.org/web/20001109153100/http://a.test/path"
        self.assertEqual(normalize_target("http://a.test/", wrapped), "http://a.test/path")

    def test_snapshot_url(self):
        self.assertEqual(
            snapshot_url("20001109153100", "http://a.test/"),
            "https://web.archive.org/web/20001109153100id_/http://a.test/",
        )


if __name__ == "__main__":
    unittest.main()
