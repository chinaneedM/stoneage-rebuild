"""Independent synthetic codec vectors and evidence mutation controls."""
import copy
import json
from pathlib import Path
import struct
import unittest
from tools.stoneage_wayi_codec_profile import (
    ALPHABET, permute, sixbit, unsixbit_seed, encode_outer, decode_outer,
    field_key, validate, probe,
)


def reference_packet(message, seed):
    # Independent streaming six-bit construction and explicit seed byte mapping.
    raw = struct.pack('<I', seed)
    swapped = bytes((raw[2],raw[0],raw[3],raw[1]))
    acc = 0; out = bytearray()
    for i, c in enumerate(swapped):
        acc |= (c ^ 255) << ((i % 3)*2)
        out.append(ALPHABET[acc & 63]); acc >>= 6
        if i % 3 == 2:
            out.append(ALPHABET[acc & 63]); acc = 0
    if acc:
        out.append(ALPHABET[acc])
    offset = seed % len(message)
    rotated = bytes(message[(i+offset)%len(message)] for i in range(len(message)))
    return bytes(255-c for c in out+rotated)


class CodecProfileTests(unittest.TestCase):
    def report(self):
        return json.loads((Path(__file__).resolve().parents[1]/
            'research/recovered/STONEAGE-WAYI-CODEC-PROFILE-R1.json').read_text())

    def test_all_99_seeds_independent_reference(self):
        for seed in range(99):
            for message in (b'x',b'&;140;synthetic;#;',bytes(range(32,127))):
                with self.subTest(seed=seed,length=len(message)):
                    packet=encode_outer(message,seed)
                    self.assertEqual(packet,reference_packet(message,seed))
                    self.assertEqual(decode_outer(packet),message)
                    self.assertEqual(len(packet),len(message)+6)

    def test_big5_like_bytes_are_bytes_not_utf8(self):
        message=b'&;69;\xa4\xa4\xa4\xe5;#;'
        self.assertEqual(decode_outer(encode_outer(message,73)),message)

    def test_seed_zero_hand_calculated_header(self):
        self.assertEqual(sixbit(b'\xff'*4),b'}}}}}3')
        self.assertEqual(encode_outer(b'x',0),bytes(c^255 for c in b'}}}}}3x'))

    def test_zero_residual_is_not_padded(self):
        self.assertEqual(sixbit(b'\x00'),b'0')
        self.assertEqual(sixbit(b'\x00\x00'),b'00')
        self.assertEqual(sixbit(b'\x00\x00\x00'),b'0000')
        self.assertEqual(sixbit(b'\x01'),b'1')

    def test_permutation_inverse_all_byte_positions(self):
        self.assertEqual(permute(b'\x01\x02\x03\x04','2413'),b'\x03\x01\x04\x02')
        self.assertEqual(permute(permute(bytes(range(4)),'2413'),'3142'),bytes(range(4)))

    def test_not_standard_base64(self):
        import base64
        self.assertNotEqual(sixbit(b'abc'),base64.b64encode(b'abc'))

    def test_invalid_seed_inputs(self):
        for seed in (-1,99,True,1.0):
            with self.assertRaises(ValueError):encode_outer(b'x',seed)

    def test_unsafe_synthetic_message_rejected(self):
        for message in (b'',b'\0',b'\xff',b'\n',b'\r',b'x'*4097,'x'):
            with self.assertRaises(ValueError):encode_outer(message,0)

    def test_seed_decoder_bounds(self):
        for token in (b'',b'00000',b'!!!!!!',b'}}}}}}'):
            with self.assertRaises(ValueError):unsixbit_seed(token)

    def test_synthetic_packet_domain(self):
        for packet in (b'',b'123456',b'\0'*7,b'x'*4103):
            with self.assertRaises(ValueError):decode_outer(packet)

    def test_key_modes_and_unrelated_bits(self):
        self.assertEqual(field_key(b'synthetic',0),b'synthetic19761101')
        self.assertEqual(field_key(b'synthetic',0x0f000000),b'synthetic07062005')
        self.assertEqual(field_key(b'synthetic',0xffffffff),b'synthetic07062005')
        self.assertEqual(field_key(b'synthetic',0x01000000),b'synthetic19761101')

    def test_key_mode_bounds(self):
        for base,mode in ((b'',0),(b'\0',0),(b'x',-1),(b'x',0x100000000),(b'x',True)):
            with self.assertRaises(ValueError):field_key(base,mode)

    def test_accepted_evidence(self):
        self.assertEqual(validate(self.report())['key_buffer_rva'],0x4bb4694)

    def test_specimen_mutation(self):
        for key,value in [('input_bytes',1),('decompressed_input_sha256','0'*64)]:
            r=self.report();r['probe'][key]=value
            with self.assertRaises(ValueError):validate(r)

    def test_changed_window_or_missing_helper(self):
        for missing in (True,False):
            r=self.report()
            if missing:r['probe']['windows'].pop()
            else:r['probe']['windows'][0]['start_rva']+=1
            with self.assertRaises(ValueError):validate(r)

    def test_key_suffix_or_literal_mutation(self):
        r=self.report();r['probe']['literals']['0xc8514']='19761101'
        with self.assertRaises(ValueError):validate(r)

    def test_runtime_promotion(self):
        for key in ('file_executed','packets_captured','matching_server_verified','native_pet_runtime_verified'):
            r=self.report();r['probe'][key]=True
            with self.assertRaises(ValueError):validate(r)

    def test_vector_changed_seed(self):
        r=self.report();r['synthetic_vectors'][0]['seed']=1
        with self.assertRaises(ValueError):validate(r)

    def test_hash_gate_rejects_small_specimen(self):
        with self.assertRaises(ValueError):probe(b'MZ')
