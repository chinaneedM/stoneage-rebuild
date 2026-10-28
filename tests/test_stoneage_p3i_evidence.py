"""Synthetic adversarial tests; no original imagery or files."""
import copy
import unittest
from tools.stoneage_p3i_evidence_guard import qualify_p3i
def sample():
    return {'original_client_execution_attempted':True,'native_probe_attempted':True,
        'observations':[{'frame':{'rgb_sha256':'a'*64}},{'frame':{'rgb_sha256':'b'*64}},{'frame':{'rgb_sha256':'a'*64}}],
        'native_probe':{'returncode':0,'stdout':{
            'schema':'stoneage.p3i.native_ddraw_primary.v1','target_owned_window_verified':True,
            'original_private_surface_read':False,'sample_region':[640,480],
            'ddraw_create_hr':'0x00000000','cooperative_hr':'0x00000000',
            'primary_create_hr':'0x00000000','primary_lock_hr':'0x00000000',
            'surface_bpp':8,'surface_pitch':640,'pixel_sha256':'f'*64,
            'index_zero_pixels':307200,'index_nonzero_pixels':0,
            'index_distinct':1,'palette_read':False,'palette_sha256':''}}}
class Evidence(unittest.TestCase):
    def test_primary_read_not_game_art(self):
        self.assertEqual(qualify_p3i(sample()),'PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED')
    def test_unreadable_primary_is_not_black_game_proof(self):
        s=sample();p=s['native_probe']['stdout'];p['pixel_sha256']='';p['primary_lock_hr']='0x88760000'
        self.assertEqual(qualify_p3i(s),'PRIMARY_DISPLAY_READ_UNAVAILABLE_GAME_RENDER_UNKNOWN')
    def test_adversarial_provenance_rejected(self):
        modifications=[
            lambda s:s.update(native_probe_attempted=False),
            lambda s:s.update(original_client_execution_attempted=False),
            lambda s:s['native_probe'].update(returncode=4),
            lambda s:s['native_probe']['stdout'].update(target_owned_window_verified=False),
            lambda s:s['native_probe']['stdout'].update(original_private_surface_read=True),
            lambda s:s['native_probe']['stdout'].update(sample_region=[1024,768]),
            lambda s:s['native_probe']['stdout'].update(index_zero_pixels=307199),
            lambda s:s['native_probe']['stdout'].update(pixel_sha256='x'*64),
            lambda s:s['native_probe']['stdout'].update(surface_pitch=1),
            lambda s:s['native_probe']['stdout'].update(ddraw_create_hr='ok'),
            lambda s:s.update(observations=[])]
        for change in modifications:
            s=copy.deepcopy(sample());change(s)
            with self.subTest(change=repr(change)),self.assertRaises(ValueError):
                qualify_p3i(s)
if __name__=='__main__':unittest.main()
