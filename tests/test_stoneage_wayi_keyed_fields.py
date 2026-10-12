"""Synthetic independent bitstream oracle, signed boundaries and mutations."""
import json
from pathlib import Path
import random
import struct
import unittest
from tools.stoneage_wayi_keyed_fields import (ALPHABET,keyed_pack,keyed_unpack,
    encode_int,decode_int,encode_string,decode_string,handshake_branch,
    probe,validate,source_selector)


def ref_pack(data,key,sign):
    out=[];acc=0
    for i,c in enumerate(data):
        acc |= c << ((i%3)*2)
        out.append(ALPHABET[((acc&63)+sign*key[len(out)%len(key)])%64]);acc >>= 6
        if i%3==2:
            out.append(ALPHABET[((acc&63)+sign*key[len(out)%len(key)])%64]);acc=0
    if acc:out.append(ALPHABET[(acc+sign*key[len(out)%len(key)])%64])
    return bytes(out)


def ref_int(value,key):
    a,b,c,d=struct.pack('<i',value)
    swapped=bytes((b,d,a,c))
    return ref_pack(bytes(255-x for x in swapped),key,1)


class KeyedFieldsTests(unittest.TestCase):
    def report(self):
        return json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-WAYI-KEYED-FIELDS-R1.json').read_text())

    def test_signed_boundaries_and_independent_integer_reference(self):
        for value in (-2147483648,-65536,-256,-2,-1,0,1,255,256,65535,0x01020304,2147483647):
            for key in (b'A',b'key',b'R1',bytes([255,128,65])):
                with self.subTest(value=value,key=key):
                    token=encode_int(value,key)
                    self.assertEqual(token,ref_int(value,key));self.assertEqual(decode_int(token,key),value)

    def test_deterministic_int32_sweep(self):
        rng=random.Random(127)
        for _ in range(256):
            n=rng.randint(-(1<<31),(1<<31)-1);k=b'R1-synthetic'
            self.assertEqual(decode_int(encode_int(n,k),k),n)

    def test_minus_one_has_five_symbols_terminating_zero_supplies_fourth_byte(self):
        self.assertEqual(encode_int(-1,b'A'),b'11111')
        self.assertEqual(keyed_unpack(b'11111',b'A',-1),b'\0\0\0')
        self.assertEqual(decode_int(b'11111',b'A'),-1)

    def test_string_direction_differs_from_integer(self):
        self.assertEqual(encode_string(b'abc',b'key'),ref_pack(b'abc',b'key',-1))
        self.assertNotEqual(encode_string(b'abc',b'A'),keyed_pack(b'abc',b'A',1))

    def test_all_nonzero_single_byte_strings(self):
        for c in range(1,256):
            v=bytes([c]);token=encode_string(v,b'R1')
            self.assertEqual(token,ref_pack(v,b'R1',-1));self.assertEqual(decode_string(token,b'R1'),v)

    def test_each_partial_group_boundary(self):
        for n in range(1,40):
            v=bytes(range(1,n+1));k=b'key'
            self.assertEqual(encode_string(v,k),ref_pack(v,k,-1))
            self.assertEqual(decode_string(encode_string(v,k),k),v)

    def test_key_cursor_resets_per_field(self):
        self.assertEqual(encode_string(b'a',b'key'),encode_string(b'a',b'key'))
        self.assertEqual(encode_string(b'b',b'key'),ref_pack(b'b',b'key',-1))
        self.assertNotEqual(encode_string(b'b',b'key'),ref_pack(b'b',b'eyk',-1))

    def test_high_bit_key_low_six_bit_alias(self):
        self.assertEqual(encode_int(123,b'A'),encode_int(123,bytes([129])))
        self.assertEqual(encode_string(b'xyz',b'A'),encode_string(b'xyz',bytes([129])))

    def test_wrong_key_has_no_authentication_guarantee(self):
        token=encode_int(123,b'A')
        self.assertNotEqual(decode_int(token,b'B'),123)
        self.assertEqual(decode_int(token,bytes([129])),123)

    def test_empty_string_valid_under_nonempty_key(self):
        self.assertEqual(encode_string(b'',b'key'),b'');self.assertEqual(decode_string(b'',b'key'),b'')

    def test_big5_checksum_is_byte_count(self):
        v=b'\xa4\xa4\xa4\xe5'
        self.assertEqual(len(v),4);self.assertEqual(len(v.decode('big5')),2)
        self.assertEqual(decode_string(encode_string(v,b'key'),b'key'),v)

    def test_integer_domain_rejects_overflow_and_boolean(self):
        for n in (-(1<<31)-1,1<<31,True,1.0):
            with self.assertRaises(ValueError):encode_int(n,b'A')

    def test_empty_nul_and_oversized_keys_rejected(self):
        for key in (b'',b'\0',b'x'*65,'key'):
            with self.assertRaises(ValueError):encode_string(b'a',key)

    def test_nul_string_and_oversize_rejected(self):
        for value in (b'\0',b'x'*4097,'x'):
            with self.assertRaises(ValueError):encode_string(value,b'A')

    def test_invalid_symbol_rejected_in_model_only(self):
        with self.assertRaises(ValueError):decode_string(b'!',b'A')

    def test_integer_token_wrong_size_rejected(self):
        for token in (b'1111',b'1111111'):
            with self.assertRaises(ValueError):decode_int(token,b'A')

    def test_handshake_f_not_later_n(self):
        self.assertEqual(handshake_branch(ord('F')),'set-mode-0x0f000001')
        self.assertEqual(handshake_branch(ord('E')),'error-message')
        self.assertEqual(handshake_branch(ord('N')),'version-error')

    def test_handshake_byte_domain(self):
        for c in (-1,256,True):
            with self.assertRaises(ValueError):handshake_branch(c)

    def test_accepted_evidence(self):validate(self.report())

    def test_wrong_specimen(self):
        with self.assertRaises(ValueError):probe(b'MZ')

    def test_integer_direction_mutation(self):
        r=self.report();r['probe']['anchors']['0x90105']['operation']='sub'
        with self.assertRaises(ValueError):validate(r)

    def test_handshake_identity_mutation(self):
        r=self.report();r['probe']['anchors']['0x5f809']['operands'][1]['value']=ord('N')
        with self.assertRaises(ValueError):validate(r)

    def test_vector_mutation(self):
        r=self.report();r['integer_vectors'][0]['value']=0
        with self.assertRaises(ValueError):validate(r)

    def test_native_promotion_rejected(self):
        r=self.report();r['probe']['matching_server_verified']=True
        with self.assertRaises(ValueError):validate(r)

    def test_source_default_not_forced_legacy(self):
        r=self.report();r['source_selector']['profiles']['default']['legacy_decoder_call_present']=True
        with self.assertRaises(ValueError):validate(r)

    def test_source_pin_mutation(self):
        r=self.report();r['source_selector']['source_blobs']['server/common/common.h']='0'*40
        with self.assertRaises(ValueError):validate(r)
