"""Adversarial R30 original-pixel and private-output contracts, no game assets."""
from pathlib import Path
import json
import tempfile
import unittest

from tools.stoneage_tw85_r30_preview import candidate,require,sha,sealed_zip

class R30OriginalEvidenceTests(unittest.TestCase):
    @staticmethod
    def fixture():
        a={"frame_count":"8"}
        f=[{"bmp_no":str(10000+i),"sentinel":"0"} for i in range(8)]
        n={10000+i:[{"index":str(i),"width":"16","height":"16","size":"192",
                      "rd_flag":"1","rd_status":"HEADER_MATCH"}] for i in range(8)}
        return f,a,n

    def test_select_only_unique_actual_rd_id(self):
        f,a,n=self.fixture()
        self.assertTrue(candidate(f,a,{},n))
        n[10000].append(dict(n[10000][0],index="88"))
        self.assertFalse(candidate(f,a,{},n))

    def test_missing_rd_and_sentinel_must_fail(self):
        f,a,n=self.fixture()
        del n[10000]
        self.assertFalse(candidate(f,a,{},n))
        f,a,n=self.fixture()
        f[0]["bmp_no"]=str(0xffffffff);f[0]["sentinel"]="1"
        self.assertFalse(candidate(f,a,{},n))

    def test_too_large_or_ineligible_pixel_safeguard(self):
        f,a,n=self.fixture()
        n[10000][0]["width"]="100000"
        self.assertFalse(candidate(f,a,{},n))
        f,a,n=self.fixture()
        n[10000][0]["rd_flag"]="5"
        self.assertFalse(candidate(f,a,{},n))
        f,a,n=self.fixture()
        n[10000][0]["rd_status"]="OUT_OF_BOUNDS"
        self.assertFalse(candidate(f,a,{},n))

    def test_source_derived_not_paletted_original_picture(self):
        f,a,n=self.fixture()
        self.assertTrue(candidate(f,a,{},n))
        with self.assertRaises(ValueError):
            require(False,"refuse")

    def test_aes_gcm_rsa_session_capsule_never_includes_plain_png(self):
        from cryptography.hazmat.primitives.asymmetric import rsa,padding
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import base64
        import io
        import zipfile
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp)
            source=temp/"private";source.mkdir()
            (source/"frame_00_bmp_1.png").write_bytes(b"\x89PNG\r\n\x1a\n"+b"synthetic-test-pixels")
            (source/"PRIVATE-R30.json").write_text(json.dumps({"kind":"synthetic"}))
            key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
            pub=temp/"pub.pem";pub.write_bytes(key.public_key().public_bytes(
                serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
            path=temp/"private.r30.enc";envelope=temp/"envelope.json"
            sealed=sealed_zip(source,pub,path,envelope)
            blob=path.read_bytes()
            self.assertEqual(sha(blob),sealed["ciphertext_sha256"])
            self.assertNotIn(b"synthetic-test-pixels",blob)
            meta=json.loads(envelope.read_text())
            material=key.decrypt(base64.b64decode(meta["wrapped_key_base64"]),padding.OAEP(
                  mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            decoded=AESGCM(material).decrypt(
                base64.b64decode(meta["nonce_base64"]),blob,
                meta["associated_data_utf8"].encode("utf-8"))
            with zipfile.ZipFile(io.BytesIO(decoded)) as z:
                self.assertEqual(z.read("frame_00_bmp_1.png"),(source/"frame_00_bmp_1.png").read_bytes())
            self.assertFalse(meta["private_key_written_to_ci"])
            self.assertFalse(meta["public_source_files_or_unencrypted_original_art_in_artifact"])

if __name__=="__main__":unittest.main()
