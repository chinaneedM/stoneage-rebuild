"""Private screenshot transport: public X25519 key, ephemeral DH + AES-256-GCM.

Only ciphertext may leave the temporary source runner. The session private key
stays in the researcher's local workspace; plaintext PNG stays outside Git.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA='stoneage.p3.private_frame.x25519_aesgcm.v1'
MAX_BYTES=8*1024*1024


def require(ok,message):
    if not ok:raise ValueError(message)


def private_output(path,suffix):
    p=path.resolve()
    require(p!=ROOT and ROOT not in p.parents,'private frame output must stay outside public Git')
    require(p.suffix==suffix and p.parent.is_dir() and not p.exists(),'private output must be new with an existing parent')
    return p


def seal(raw,public_pem):
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    require(raw.startswith(b'\x89PNG\r\n\x1a\n') and 0<len(raw)<=MAX_BYTES,'only bounded PNG evidence admitted')
    public=serialization.load_pem_public_key(public_pem);require(isinstance(public,X25519PublicKey),'X25519 recipient required')
    ephemeral=X25519PrivateKey.generate();salt=os.urandom(16);nonce=os.urandom(12)
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=SCHEMA.encode()).derive(ephemeral.exchange(public))
    aad={'schema':SCHEMA,'plaintext_sha256':hashlib.sha256(raw).hexdigest(),
         'plaintext_bytes':len(raw),'recipient_key_sha256':hashlib.sha256(public_pem).hexdigest()}
    encoded=json.dumps(aad,sort_keys=True,separators=(',',':')).encode()
    aad.update(ephemeral_public_b64=base64.b64encode(ephemeral.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)).decode(),
               salt_b64=base64.b64encode(salt).decode(),nonce_b64=base64.b64encode(nonce).decode(),
               ciphertext_b64=base64.b64encode(AESGCM(key).encrypt(nonce,raw,encoded)).decode())
    return aad


def unseal(envelope,private_pem):
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    require(envelope['schema']==SCHEMA and 0<envelope['plaintext_bytes']<=MAX_BYTES,'unqualified private-frame schema/size')
    private=serialization.load_pem_private_key(private_pem,password=None);require(isinstance(private,X25519PrivateKey),'X25519 private key required')
    public_pem=private.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
    require(hashlib.sha256(public_pem).hexdigest()==envelope['recipient_key_sha256'],'private-frame recipient mismatch')
    ephemeral=X25519PublicKey.from_public_bytes(base64.b64decode(envelope['ephemeral_public_b64'],validate=True))
    salt=base64.b64decode(envelope['salt_b64'],validate=True);nonce=base64.b64decode(envelope['nonce_b64'],validate=True)
    require(len(salt)==16 and len(nonce)==12,'invalid encryption parameters')
    aad={k:envelope[k] for k in ('schema','plaintext_sha256','plaintext_bytes','recipient_key_sha256')}
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=SCHEMA.encode()).derive(private.exchange(ephemeral))
    raw=AESGCM(key).decrypt(nonce,base64.b64decode(envelope['ciphertext_b64'],validate=True),
                           json.dumps(aad,sort_keys=True,separators=(',',':')).encode())
    require(len(raw)==envelope['plaintext_bytes'] and hashlib.sha256(raw).hexdigest()==envelope['plaintext_sha256'],
            'decrypted frame differs from authenticated metadata')
    require(raw.startswith(b'\x89PNG\r\n\x1a\n'),'decrypted evidence is not PNG')
    return raw


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True)
    p.add_argument('--key',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--decrypt',action='store_true');a=p.parse_args()
    if a.decrypt:
        out=private_output(a.output,'.png');raw=unseal(json.loads(a.input.read_bytes()),a.key.read_bytes())
        with out.open('xb') as f:f.write(raw)
    else:
        out=private_output(a.output,'.json');e=seal(a.input.read_bytes(),a.key.read_bytes())
        with out.open('x') as f:json.dump(e,f,sort_keys=True)
    print('PRIVATE_FRAME_AUTHENTICATED_TRANSPORT=PASS; PRIVATE_KEY_NOT_EMITTED')


if __name__=='__main__':main()
