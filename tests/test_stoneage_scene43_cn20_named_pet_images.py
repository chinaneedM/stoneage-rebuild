"""Tests preserve CN2.0 webpage name->real src vs native TW1 IDs."""
import io,unittest
from PIL import Image
from tools.stoneage_scene43_cn20_named_pet_images import originals,inspect_jpeg,archived_url,parse_original_page,MAX_JPEG,PAGE_SHA,PAGE_BYTES

class Scene43(unittest.TestCase):
    def test_frozen_actual_page_and_two_source_photo_bytes(self):
        from tools.stoneage_scene43_cn20_named_pet_images import FROZEN, validate_frozen
        import json
        d=validate_frozen(json.loads(FROZEN.read_text(encoding="utf-8")))
        self.assertEqual(d["qualified_image_count"],2)
        self.assertEqual([x["web_ordinal"] for x in d["entries"]],[85,86])
        self.assertEqual([x["image"]["bytes"] for x in d["entries"]],[3753,4494])
        self.assertEqual([x["image"]["sha256"] for x in d["entries"]],[
            "ba7b663a9445a0e32117eb768db33e991c566ddfac8ad1ae5d93bb7cf6372e31",
            "9951490cc47de15342fd88e671a8e54d1c6c33c7786655af4ffe4b93300f16b2"])
    def test_refuses_2001_same_instant_false_upgrade(self):
        from tools.stoneage_scene43_cn20_named_pet_images import FROZEN,validate_frozen
        import json
        d=json.loads(FROZEN.read_text(encoding="utf-8"))
        d["entries"][0]["image"]["native_client_bitmap_or_sprite_identity_proven"]=True
        with self.assertRaises(ValueError):validate_frozen(d)
    def test_image_capture_time_is_different_from_html_capture_time(self):
        from tools.stoneage_scene43_cn20_named_pet_images import FROZEN,validate_frozen
        import json
        d=validate_frozen(json.loads(FROZEN.read_text(encoding="utf-8")))
        self.assertEqual(d["page_capture"],"20011023181629")
        self.assertEqual([x["image"]["actual_capture"] for x in d["entries"]],
                         ["20011026013455","20011026013052"])
        self.assertTrue(all(x["same_instant_as_archive_page_proven"] is False for x in d["entries"]))

    def original(self):
        rows=originals()
        self.assertEqual([x["ordinal"] for x in rows],[85,86])
        self.assertEqual([x["name_as_written"] for x in rows],["瑞德宝","瑞里西尔"])
        self.assertEqual([x["src"] for x in rows],["img/newpet/84.JPG","img/newpet/85.JPG"])
        return rows
    def test_parent_not_confused_with_image_number(self):
        self.original()
    def test_jpeg_source_valid(self):
        p=self.original()[0];u="https://web.archive.org/web/20011026020304id_/"+p["original_url"]
        buf=io.BytesIO();Image.new("RGB",(83,90)).save(buf,format="JPEG")
        d=inspect_jpeg(buf.getvalue(),u,p["original_url"])
        self.assertEqual(d["size"],[83,90])
        self.assertIs(d["visual_review_by_assistant"],False)
        self.assertIs(d["native_client_bitmap_or_sprite_identity_proven"],False)
    def test_wrong_image_path_rejected(self):
        p=self.original()[0];u="https://web.archive.org/web/20011026020304id_/"+p["original_url"].replace("84.JPG","85.JPG")
        with self.assertRaises(ValueError):archived_url(u,p["original_url"])
    def test_wrong_archive_host_rejected(self):
        p=self.original()[0]
        with self.assertRaises(ValueError):archived_url("https://example.com/web/20011026020304id_/"+p["original_url"],p["original_url"])
    def test_missing_archive_timestamp_rejected(self):
        p=self.original()[0]
        with self.assertRaises(ValueError):archived_url("https://web.archive.org/web/2001id_/"+p["original_url"],p["original_url"])
    def test_html_payload_cannot_be_pet_jpeg(self):
        p=self.original()[0];u="https://web.archive.org/web/20011026020304id_/"+p["original_url"]
        with self.assertRaises(ValueError):inspect_jpeg(b"<html>"*120,u,p["original_url"])
    def test_wrong_pixel_dimensions_rejected(self):
        p=self.original()[0];u="https://web.archive.org/web/20011026020304id_/"+p["original_url"]
        buf=io.BytesIO();Image.new("RGB",(90,83)).save(buf,format="JPEG")
        with self.assertRaises(ValueError):inspect_jpeg(buf.getvalue(),u,p["original_url"])
    def test_page_bytes_cannot_be_changed(self):
        with self.assertRaises(ValueError):parse_original_page(b"0"*PAGE_BYTES)
