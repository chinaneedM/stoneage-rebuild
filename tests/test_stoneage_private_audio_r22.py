import copy
import io
from pathlib import Path
import tempfile
import unittest
import wave
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
from tools import stoneage_private_audio_r22 as a

def synthetic(rate=22050,width=1,channels=1):
    f=io.BytesIO()
    with wave.open(f,'wb') as w:
        w.setnchannels(channels);w.setsampwidth(width);w.setframerate(rate);w.writeframes(bytes([128,0,255,128])*width*channels)
    return f.getvalue()

class PrivateAudioTests(unittest.TestCase):
    def keys(self):
        k=X25519PrivateKey.generate();return k.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()),k.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
    def test_exact_synthetic_wave_roundtrip_and_no_private_key(self):
        private,public=self.keys();raw=synthetic();e=a.seal(raw,public)
        self.assertEqual(a.unseal(e,private),raw);self.assertNotIn('PRIVATE KEY',str(e));self.assertEqual(e['media_type'],'audio/wav')
    def test_wrong_recipient_rejected(self):
        private,public=self.keys();other,_=self.keys()
        with self.assertRaises(ValueError):a.unseal(a.seal(synthetic(),public),other)
    def test_authenticated_metadata_and_ciphertext_cannot_be_modified(self):
        private,public=self.keys();e=a.seal(synthetic(),public)
        for key in ('plaintext_sha256','ciphertext_b64','nonce_b64','schema','media_type'):
            d=copy.deepcopy(e);d[key]='invalid'
            with self.subTest(key=key),self.assertRaises(Exception):a.unseal(d,private)
    def test_truncated_outer_riff_rejected(self):
        with self.assertRaises(ValueError):a.wave_metadata(synthetic()[:-1])
    def test_non_pcm8_mono22050_formats_rejected(self):
        for raw in (synthetic(rate=11025),synthetic(width=2),synthetic(channels=2),b'not audio',b'\x89PNG\r\n\x1a\n'):
            with self.subTest(size=len(raw)),self.assertRaises(ValueError):a.wave_metadata(raw)
    def test_new_private_destination_required(self):
        with self.assertRaises(ValueError):a.outside_new(a.ROOT/'bad.json','.json')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'existing.json';p.write_text('x')
            with self.assertRaises(ValueError):a.outside_new(p,'.json')
    def test_pcm_duration_and_non_silence_are_measurements_not_hearing(self):
        m=a.wave_metadata(synthetic());self.assertEqual(m['frames'],4);self.assertEqual(m['non_midpoint_samples'],2)
        self.assertAlmostEqual(m['duration_seconds'],4/22050);self.assertNotIn('heard',m)

if __name__=='__main__':unittest.main()
