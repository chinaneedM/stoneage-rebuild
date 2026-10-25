import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from tools import stoneage_tw10_palette as p
from tools.stoneage_original_animation_lab import preview,sample_report
from tests.test_stoneage_original_animation_lab import AnimationObservationTests


class PaletteInitialTests(unittest.TestCase):
    def test_original_fixed_constants_and_bgr_positions(self):
        self.assertEqual(p.digest(bytes(v for c in p.FIXED_RGB for v in c)),
                         '6d145e46e9b7aeadaea6f45babaf4712869071c871314cac6c3fa22d8b4f084a')
        raw=bytes((i*17+3)%256 for i in range(708));rgb=p.initial_rgb(raw)
        self.assertEqual(len(rgb),768)
        self.assertEqual(rgb[:48],bytes(v for c in p.FIXED_RGB[:16] for v in c))
        self.assertEqual(rgb[720:],bytes(v for c in p.FIXED_RGB[16:] for v in c))
        self.assertEqual(rgb[48:51],raw[:3][::-1])
        self.assertEqual(rgb[717:720],raw[669:672][::-1])
        self.assertNotEqual(raw[456:459],b'\0'*3)
        self.assertEqual(rgb[504:507],b'\0'*3)  # forced logical index 168

    def test_unread_suffix_preserved_but_not_used_for_color(self):
        raw=bytes((i*17+3)%256 for i in range(708))
        self.assertEqual(p.initial_rgb(raw),p.initial_rgb(raw[:672]+bytes(36)))
        self.assertNotEqual(hashlib.sha256(raw).digest(),hashlib.sha256(raw[:672]+bytes(36)).digest())
        with self.assertRaises(ValueError):p.initial_rgb(raw[:672])

    def test_indexed_png_preserves_indices_and_rgb_not_alpha(self):
        raw=bytes((i*17+3)%256 for i in range(708));rgb=p.initial_rgb(raw)
        indices=bytes([0,16,168,255]);png=p.indexed_png(indices,2,2,rgb)
        offset=8;chunks={}
        while offset<len(png):
            size=struct.unpack_from('>I',png,offset)[0];tag=png[offset+4:offset+8]
            body=png[offset+8:offset+8+size]
            self.assertEqual(zlib.crc32(tag+body)&0xffffffff,struct.unpack_from('>I',png,offset+8+size)[0])
            chunks[tag]=body;offset+=12+size
        self.assertEqual(chunks[b'PLTE'],rgb);self.assertNotIn(b'tRNS',chunks)
        self.assertEqual(chunks[b'IHDR'][8:10],bytes([8,3]))
        self.assertEqual(zlib.decompress(chunks[b'IDAT']),b'\0\0\x10\0\xa8\xff')
        with self.assertRaises(ValueError):p.indexed_png(b'\0',1,1,rgb[:-1])
        with self.assertRaises(ValueError):p.indexed_png(b'\0',2,2,rgb)

    def test_fake_originals_rejected_before_emulation_or_color_export(self):
        with self.assertRaises(ValueError):p.emulate_initial(b'MZ'+bytes(425982),bytes(708))
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'Palet_0.sap';f.write_bytes(bytes(708))
            with self.assertRaises(ValueError):p.original_rgb(f)

    def test_color_preview_does_not_change_source_frames_or_claim_game_display(self):
        with tempfile.TemporaryDirectory() as d:
            helper=AnimationObservationTests();helper.report=sample_report()
            _,_,_,timeline,paths,pins=helper.fixture(Path(d))
            t=copy.deepcopy(timeline);t.update(preview_mode=p.MODE,original_palette_verified=True,
                                             source_palette_rgb_mapping_verified=True)
            rgb=p.initial_rgb(bytes((i*17+3)%256 for i in range(708)))
            html,c=preview(t,paths,pins,color_table=rgb)
            self.assertEqual(c['timeline']['frames'],timeline['frames'])
            self.assertEqual(c['rendered_rgb_table_sha256'],p.digest(rgb))
            self.assertIn('private_indexed_color_png_sha256',c['bitmap_witnesses'][0])
            self.assertNotIn('private_grayscale_png_sha256',c['bitmap_witnesses'][0])
            self.assertFalse(c['timeline']['original_client_executed'])
            self.assertFalse(c['timeline']['historical_gameplay_screenshot'])
            self.assertFalse(c['assistant_viewed_or_heard_original'])
            self.assertIn('Palet_0',html)


if __name__=='__main__':unittest.main()
