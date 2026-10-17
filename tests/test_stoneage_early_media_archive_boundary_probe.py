"""Adversarial, network-free early archived media qualification gates."""
import unittest
from tools.stoneage_early_media_archive_boundary_probe import (
    TARGETS, qualify, build, origin_key)

BASE="http://stoneage.17173.com/jingyan/jingyan.shtml"
def archived(ts, origin=BASE):
    return "https://web.archive.org/web/"+ts+"id_/"+origin

class ArchiveBoundaryTest(unittest.TestCase):
    def test_early_archived_article_is_only_link_metadata(self):
        raw=b"<html><body>stoneage <a href='../chongwu/pet.htm'>Pets</a></body></html>"
        d=qualify(raw,archived("20010614082314"),BASE)
        self.assertEqual(d["status"],"EARLY_CAPTURE_LINK_METADATA_QUALIFIED")
        self.assertEqual(d["qualified_link_count"],1)
        self.assertTrue(d["sample_link_targets"][0].endswith("/chongwu/pet.htm"))
        self.assertFalse(d["original_tw10_server_gameplay_verified"])
        self.assertFalse(d["original_site_layout_verified"])
    def test_later_archive_is_not_backdated(self):
        d=qualify(b"<html>stoneage</html>",archived("20060205112723"),BASE)
        self.assertEqual(d["status"],"OUT_OF_WINDOW_NOT_EARLY_EVIDENCE")
        self.assertEqual(d["actual_capture"],"20060205112723")
    def test_non_identical_origins_and_fake_archive_rejected(self):
        with self.assertRaisesRegex(ValueError,"target URL changed"):
            qualify(b"<html>stoneage</html>",archived("20010614082314",
                  "http://stoneage.17173.com/jingyan/other.shtml"),BASE)
        with self.assertRaisesRegex(ValueError,"no independently observed"):
            qualify(b"<html>stoneage</html>",BASE,BASE)
    def test_early_unbranded_index_remains_unqualified(self):
        d=qualify(b"<html><body><a href='pet.htm'>pets</a></body></html>",
                  archived("20010614082314"),BASE)
        self.assertEqual(d["status"],"EARLY_HTML_BRAND_NOT_ESTABLISHED")
    def test_three_bounded_leads_and_late_provenance(self):
        self.assertEqual(len(TARGETS),3)
        self.assertEqual(TARGETS[0]["url"],TARGETS[1]["url"])
        self.assertIn("LATE_",TARGETS[2]["lead"])
        self.assertEqual(origin_key(TARGETS[0]["url"])[0],"stoneage.17173.com")

if __name__=="__main__":
    unittest.main()
