"""Synthetic negative gates for a privately exported original-client observation kit."""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
from tools import stoneage_singleplayer_observation_kit as kit

class OfflineKit(unittest.TestCase):
    def test_landing_cannot_claim_original_gameplay(self):
        html=kit.landing_html(100000,0,6,3)
        self.assertIn("无需登录、服务器",html)
        self.assertIn("非原游戏可操作世界",html)
        self.assertIn("frame-*.png",html)
        self.assertNotIn("http://",html)
        self.assertNotIn("https://",html)
    def test_bad_selection(self):
        with self.assertRaises(ValueError):kit.landing_html(-1,0,0,1)
        with self.assertRaises(ValueError):kit.landing_html(1,0,0,0)
        with self.assertRaises(ValueError):kit.landing_html(1,0,0,513)
    def test_public_repo_out_rejected(self):
        with tempfile.TemporaryDirectory() as source:
            with self.assertRaises(ValueError):kit.safe_directories(pathlib.Path(source),kit.ROOT)
    def test_private_output_must_be_empty(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as target:
            (pathlib.Path(target)/"unrelated.txt").write_text("keep")
            with self.assertRaises(ValueError):kit.safe_directories(pathlib.Path(source),pathlib.Path(target))
            self.assertEqual((pathlib.Path(target)/"unrelated.txt").read_text(),"keep")
    def test_private_output_inside_source_rejected(self):
        with tempfile.TemporaryDirectory() as source:
            folder=pathlib.Path(source);(folder/"output").mkdir()
            with self.assertRaises(ValueError):kit.safe_directories(folder,folder/"output")
    def test_missing_original_directory_rejected(self):
        with tempfile.TemporaryDirectory() as target:
            with self.assertRaises(ValueError):kit.safe_directories(pathlib.Path(target)/"missing",pathlib.Path(target))
    def test_output_is_private_and_consumes_existing_real_exporters(self):
        with tempfile.TemporaryDirectory() as origin, tempfile.TemporaryDirectory() as target:
            source=pathlib.Path(origin);dest=pathlib.Path(target)
            frame=b"\x89PNG\r\n\x1a\nSYNTHETIC_TEST_BYTES"
            custody={"original_files":{"mock":{"sha256":"test-only"}},"source_status":"SYNTHETIC_TEST",
                     "timeline":{"frames":[{"bmp_no":1}]}}
            def fake_export(folder,frames,c):
                self.assertTrue(folder.is_dir())
                (folder/"frame-000.png").write_bytes(frames[0][1])
                (folder/"source-manifest.json").write_text('{"test":true}')
            def fake_write(path,html,c):
                path.write_text(html)
                path.with_suffix(".json").write_text("{}")
            with patch.object(kit,"timeline",return_value=custody["timeline"]), \
                 patch.object(kit,"preview",return_value=("<html>test</html>",custody)), \
                 patch.object(kit,"unpack",return_value=[("frame-000.png",frame)]), \
                 patch.object(kit,"export_private",side_effect=fake_export), \
                 patch.object(kit,"write_private",side_effect=fake_write):
                receipt=kit.emit_kit(source,dest,100000,0,6)
            self.assertEqual(receipt["derived_source_frame_positions"],1)
            self.assertIs(receipt["original_client_executable_launched"],False)
            self.assertIs(receipt["original_game_world_entered"],False)
            self.assertFalse(receipt["historical_server_required_or_contacted"])
            self.assertIn("animation-original.html",(dest/"index.html").read_text())
            self.assertEqual((dest/"frames/frame-000.png").read_bytes(),frame)
            self.assertEqual(json.loads((dest/"kit-receipt.json").read_text())["schema"],kit.SCHEMA)
    def test_rollback_on_export_failure(self):
        with tempfile.TemporaryDirectory() as origin, tempfile.TemporaryDirectory() as target:
            source=pathlib.Path(origin);dest=pathlib.Path(target)
            custody={"original_files":{},"source_status":"SYNTHETIC_TEST","timeline":{}}
            def crash(folder,frames,c):
                (folder/"partial.png").write_bytes(b"synthetic")
                raise ValueError("synthetic failure")
            with patch.object(kit,"timeline",return_value={}), \
                 patch.object(kit,"preview",return_value=("<html>test</html>",custody)), \
                 patch.object(kit,"unpack",return_value=[("frame-000.png",b"test")]), \
                 patch.object(kit,"export_private",side_effect=crash):
                with self.assertRaisesRegex(ValueError,"synthetic failure"):
                    kit.emit_kit(source,dest,100000,0,6)
            self.assertEqual(list(dest.iterdir()),[])
    def test_no_web_executable_or_original_server_in_path(self):
        src=pathlib.Path(kit.__file__).read_text(encoding="utf-8")
        self.assertNotIn("urllib.request",src)
        self.assertNotIn("subprocess",src)
        self.assertNotIn("socket.",src)

if __name__=="__main__":unittest.main()
