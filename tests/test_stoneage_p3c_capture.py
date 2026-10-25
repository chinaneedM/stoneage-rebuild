import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
from tools import stoneage_p3c_capture as c


class CaptureTests(unittest.TestCase):
    def fixture(self,args,*,env,text,capture_output,timeout,check,corrupt=False):
        d=Path(args[1]);stem=d/'window-77'
        im=Image.new('RGB',(320,160),(222,0,0))
        im.paste((0,0,0) if corrupt else (0,200,80),(160,0,320,160))
        im.save(str(stem)+'-map.ppm')
        Image.new('RGB',(320,160),(0,0,0)).save(str(stem)+'-rootmap.ppm')
        Path(str(stem)+'-indices.bin').write_bytes(b'\x2a'*25600+b'\x63'*25600)
        Path(str(stem)+'-palette.bin').write_bytes(bytes(768))
        return SimpleNamespace(stdout=json.dumps({'schema':'stoneage.p3c.x11_own_colormap.v1','x_errors':0,
            'windows':[{'window':77,'colormap':11,'default_colormap':2,'depth':8,'visual_class':3,'width':320,'height':160}]}))

    def test_known_colors_and_same_index_wrong_palette_negative_control(self):
        with tempfile.TemporaryDirectory() as d,patch.object(c.subprocess,'run',side_effect=self.fixture):
            r=c.capture(Path('/synthetic-helper'),Path(d)/'new',{},selftest=True)
        self.assertTrue(r['synthetic_known_rgb_passed'])
        self.assertFalse(r['original_client_executed'])
        self.assertEqual(r['windows'][0]['map']['synthetic_control_green_pixels'],25600)
        self.assertTrue(r['windows'][0]['same_indices_different_colormap_rgb'])

    def test_nonuniform_capture_without_known_green_is_not_color_acceptance(self):
        def broken(*args,**kwargs):return self.fixture(*args,**kwargs,corrupt=True)
        with tempfile.TemporaryDirectory() as d,patch.object(c.subprocess,'run',side_effect=broken),self.assertRaises(ValueError):
            c.capture(Path('/synthetic-helper'),Path(d)/'new',{},selftest=True)

    def test_original_capture_refuses_public_tree_and_existing_directory(self):
        for path in (c.ROOT,c.ROOT/'forbidden-frame'):
            with self.subTest(path=path),self.assertRaises(ValueError):c.capture(Path('/missing'),path,{})
        with tempfile.TemporaryDirectory() as d,self.assertRaises(ValueError):c.capture(Path('/missing'),Path(d),{})


if __name__=='__main__':unittest.main()
