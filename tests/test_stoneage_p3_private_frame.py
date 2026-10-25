import copy
from pathlib import Path
import tempfile
import unittest

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
from tools import stoneage_p3_private_frame as p
from tools.stoneage_original_observation_lab import gray_png


class PrivateFrameTests(unittest.TestCase):
    def keys(self):
        k=X25519PrivateKey.generate()
        return k.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()),k.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)

    def test_authenticated_private_synthetic_frame_round_trip(self):
        private,public=self.keys();raw=gray_png(bytes([20,40,60,80]),2,2)
        e=p.seal(raw,public);self.assertEqual(p.unseal(e,private),raw)
        self.assertNotIn(raw.decode('latin1'),str(e));self.assertNotIn('PRIVATE KEY',str(e))

    def test_wrong_key_metadata_and_ciphertext_rejected(self):
        private,public=self.keys();e=p.seal(gray_png(bytes([20]),1,1),public)
        other,_=self.keys()
        with self.assertRaises(ValueError):p.unseal(e,other)
        for field in ('plaintext_sha256','ciphertext_b64','nonce_b64'):
            d=copy.deepcopy(e);d[field]=('0'*64 if field=='plaintext_sha256' else 'A'+d[field][1:])
            with self.subTest(field=field),self.assertRaises(Exception):p.unseal(d,private)

    def test_no_public_or_existing_plaintext_output(self):
        with self.assertRaises(ValueError):p.private_output(p.ROOT/'forbidden.png','.png')
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'existing.png';path.write_bytes(b'x')
            with self.assertRaises(ValueError):p.private_output(path,'.png')


if __name__=='__main__':unittest.main()
