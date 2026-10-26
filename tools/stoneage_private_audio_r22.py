"""Bounded private WAV transfer. Original waveforms and private keys stay out of Git."""
import base64
import hashlib
import io
import json
import os
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA='stoneage.r22.private_wave.x25519_aesgcm.v1'
MAX_BYTES=65536

def need(ok,message):
    if not ok:raise ValueError(message)

def wave_metadata(raw):
    need(44<=len(raw)<=MAX_BYTES and raw[:4]==b'RIFF' and raw[8:12]==b'WAVE','one bounded WAV required')
    need(int.from_bytes(raw[4:8],'little')+8==len(raw),'full RIFF extent required')
    with wave.open(io.BytesIO(raw),'rb') as w:
        need(w.getcomptype()=='NONE' and w.getnchannels()==1 and w.getsampwidth()==1 and w.getframerate()==22050,'PCM8 mono22050 required')
        pcm=w.readframes(w.getnframes());need(len(pcm)==w.getnframes(),'complete PCM frames required')
        return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'channels':1,'sample_width_bytes':1,
            'sample_rate':22050,'frames':w.getnframes(),'duration_seconds':w.getnframes()/22050,
            'pcm_bytes':len(pcm),'pcm_sha256':hashlib.sha256(pcm).hexdigest(),
            'sample_unsigned_minimum':min(pcm),'sample_unsigned_maximum':max(pcm),
            'non_midpoint_samples':sum(v!=128 for v in pcm)}

def outside_new(path,suffix):
    p=Path(path).resolve();need(p!=ROOT and ROOT not in p.parents,'private output must remain outside repository')
    need(p.suffix==suffix and p.parent.is_dir() and not p.exists(),'new private output required');return p

def seal(raw,public_pem):
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    meta=wave_metadata(raw);public=serialization.load_pem_public_key(public_pem);need(isinstance(public,X25519PublicKey),'X25519 recipient')
    ephemeral=X25519PrivateKey.generate();salt=os.urandom(16);nonce=os.urandom(12)
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=SCHEMA.encode()).derive(ephemeral.exchange(public))
    aad={'schema':SCHEMA,'plaintext_bytes':len(raw),'plaintext_sha256':meta['sha256'],
        'recipient_key_sha256':hashlib.sha256(public_pem).hexdigest(),'media_type':'audio/wav'}
    encoded=json.dumps(aad,sort_keys=True,separators=(',',':')).encode()
    return {**aad,'ephemeral_public_b64':base64.b64encode(ephemeral.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)).decode(),
        'salt_b64':base64.b64encode(salt).decode(),'nonce_b64':base64.b64encode(nonce).decode(),
        'ciphertext_b64':base64.b64encode(AESGCM(key).encrypt(nonce,raw,encoded)).decode()}

def unseal(e,private_pem):
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    need(e['schema']==SCHEMA and e['media_type']=='audio/wav' and 44<=e['plaintext_bytes']<=MAX_BYTES,'private WAV envelope')
    private=serialization.load_pem_private_key(private_pem,password=None);need(isinstance(private,X25519PrivateKey),'X25519 private key')
    public_pem=private.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
    need(hashlib.sha256(public_pem).hexdigest()==e['recipient_key_sha256'],'recipient mismatch')
    salt=base64.b64decode(e['salt_b64'],validate=True);nonce=base64.b64decode(e['nonce_b64'],validate=True)
    need(len(salt)==16 and len(nonce)==12,'encryption parameters')
    ephemeral=X25519PublicKey.from_public_bytes(base64.b64decode(e['ephemeral_public_b64'],validate=True))
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=SCHEMA.encode()).derive(private.exchange(ephemeral))
    aad={k:e[k] for k in ('schema','plaintext_bytes','plaintext_sha256','recipient_key_sha256','media_type')}
    raw=AESGCM(key).decrypt(nonce,base64.b64decode(e['ciphertext_b64'],validate=True),json.dumps(aad,sort_keys=True,separators=(',',':')).encode())
    need(len(raw)==e['plaintext_bytes'] and hashlib.sha256(raw).hexdigest()==e['plaintext_sha256'],'decrypted WAV integrity');wave_metadata(raw);return raw
