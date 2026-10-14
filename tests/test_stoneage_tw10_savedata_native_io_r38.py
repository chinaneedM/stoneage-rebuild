"""Invented ESP graphs, joins and call barriers; no original source bytes."""
import copy
import struct
import unittest
from functools import lru_cache
from unittest.mock import patch
from tools.stoneage_tw10_savedata_native_io_r38 import *
from tools.stoneage_tw10_savedata_native_io_r38_guard import validate
from tools.stoneage_tw10_savedata_native_io_r37 import derive as derive_r37
from tests import test_stoneage_tw10_savedata_native_io_r37 as r37

@lru_cache(maxsize=1)
def base_fixture():
    captured = {}
    def capture(dec, sections, imports, previous):
        raw = bytearray(dec.raw)
        def put(at, code):
            raw[at-dec.lo:at-dec.lo+len(code)] = code
        put(0x4ed47, b"\x56")
        put(0x4ed48, b"\x53")
        put(ROOT, bytes.fromhex("8b442404535657"))
        put(ROOT+7, b"\x90" * (STORE-ROOT-7+8))
        put(0x4e81a, bytes.fromhex("89c1"))
        put(SCALARS[0], bytes.fromhex("c1f905"))
        put(0x4e81f, bytes.fromhex("83e61f"))
        put(LEA, bytes.fromhex("8d3c8d") + struct.pack("<I", dec.base+0x1721760))
        put(SCALARS[1], bytes.fromhex("c1e603"))
        put(READS[1], bytes.fromhex("8b5c2414"))
        put(0x4e840, b"\x75\x1e")  # invented branch bypasses opaque CALL
        put(0x4e85a, bytes.fromhex("ff15") + struct.pack("<I", dec.base+0x5217c))
        put(0x4e860, bytes.fromhex("8b07"))
        put(STORE, bytes.fromhex("891c30c3"))
        dec = Decoder(bytes(raw), dec.lo, dec.base)
        imports = dict(imports)
        imports[dec.base+0x5217c] = ("SYNTHETIC.dll", "InventedStackBarrier")
        previous = derive_r37(dec, sections, imports, previous)
        captured["result"] = derive(dec, sections, imports, previous)
        return previous
    r37.base_fixture.cache_clear()
    try:
        with patch.object(r37, "derive", capture):
            r37.fixture()
    finally:
        r37.base_fixture.cache_clear()
    return captured["result"]

def fixture():
    return copy.deepcopy(base_fixture())

def effect(at, kind="neutral", delta=0, width=None):
    return {"site_rva":at,"syntax_class":kind,"esp_delta":delta,
            "operand_width_bytes":width,"conditional_32bit_stack_address_only":True}

class R38Synthetic(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(fixture()))
    def test_entry_and_three_pushes(self):
        qs = fixture()["stack_state_queries"]
        self.assertEqual(qs[0]["unique_conditional_esp_delta"], 0)
        self.assertEqual(qs[1]["unique_conditional_esp_delta"], -12)
    def test_two_physical_slots_not_values(self):
        bs = fixture()["conditional_slot_bridges"]
        self.assertEqual([b["caller_pre_call_esp_relative_offset"] for b in bs], [0,4])
        self.assertEqual([b["matching_suffix_push_rva"] for b in bs], [0x4ed48,0x4ed47])
        self.assertTrue(all(b["conditional_hardware_slot_candidate"] for b in bs))
        self.assertFalse(any(b["actual_argument_value_abi_owner_or_stack_alias_binding_proven"] for b in bs))
    def test_opaque_call_join_stays_unknown(self):
        q = fixture()["stack_state_queries"][2]
        self.assertEqual(q["known_conditional_esp_deltas"], [-12])
        self.assertIsNone(q["unique_conditional_esp_delta"])
        self.assertIn({"kind":"opaque_call","site_rva":0x4e85a}, q["unknown_barrier_candidates"])
    def test_exact_store_source_shape(self):
        s = fixture()["shared_store_shape"]
        self.assertEqual(s["operands"][1]["register"], "ebx")
        self.assertEqual(s["operands"][1]["width_bytes"], 4)
        self.assertFalse(s["actual_instruction_effect_or_value_known"])
    def test_delta_branch_join_disagrees(self):
        es=[effect(1),effect(2,"push",-4,4),effect(3),effect(4)]
        states,_,limit=stack_states(es,[[1,2],[1,3],[2,4],[3,4]],1)
        s=state_summary(states,4,limit)
        self.assertEqual(s["known_conditional_esp_deltas"],[-4,0])
        self.assertIsNone(s["unique_conditional_esp_delta"])
    def test_push_pop_geometry(self):
        es=[effect(1,"push",-4,4),effect(2,"pop",4,4),effect(3)]
        states,_,limit=stack_states(es,[[1,2],[2,3]],1)
        self.assertEqual(state_summary(states,3,limit)["unique_conditional_esp_delta"],0)
    def test_loop_widens_and_terminates(self):
        es=[effect(1,"push",-4,4),effect(2)]
        states,n,limit=stack_states(es,[[1,2],[2,1]],1)
        self.assertFalse(limit)
        self.assertLess(n,MAX_UPDATES)
        self.assertIsNone(state_summary(states,2)["unique_conditional_esp_delta"])
        self.assertTrue(state_summary(states,2)["state_limit_hit"])
    def test_unknown_esp_write(self):
        es=[effect(1,"unknown_esp_write",None),effect(2)]
        states,_,_=stack_states(es,[[1,2]],1)
        self.assertIsNone(state_summary(states,2)["unique_conditional_esp_delta"])
    def test_pop_esp_is_unknown(self):
        dec=Decoder(bytes.fromhex("5c"),0,0x400000)
        self.assertEqual(stack_effect(dec.at(0),dec.base)["syntax_class"],"unknown_esp_write")
    def test_explicit_esp_arithmetic_is_unknown(self):
        dec=Decoder(bytes.fromhex("83c404"),0,0x400000)
        self.assertEqual(stack_effect(dec.at(0),dec.base)["syntax_class"],"unknown_esp_write")
    def test_unreachable_query_is_not_entry(self):
        states,_,_=stack_states([effect(1),effect(2)],[],1)
        self.assertFalse(state_summary(states,2)["site_reached_in_stack_model"])
    def test_wrong_hash(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"bad",b"bad")

class R38Tamper(unittest.TestCase):
    def reject(self, mutator):
        d=fixture();mutator(d)
        with self.assertRaises(ValueError):validate(d)
    def test_promotions(self):
        for flag in FLAGS:
            with self.subTest(flag=flag):self.reject(lambda d,f=flag:d.update({f:True}))
    def test_prior(self):
        self.reject(lambda d:d.update(r37_exact_report_sha256="bad"))
    def test_delta(self):
        self.reject(lambda d:d["stack_state_queries"][1].update(unique_conditional_esp_delta=0))
    def test_call_barrier_omission(self):
        self.reject(lambda d:d.update(opaque_call_candidates=[]))
    def test_barrier_dropped(self):
        self.reject(lambda d:d["stack_state_queries"][2].update(unknown_barrier_candidates=[]))
    def test_stack_assumption(self):
        self.reject(lambda d:d["stack_model"].update(actual_stack_address_attribute_or_return_effects_proven=True))
    def test_hardware_slot(self):
        self.reject(lambda d:d["conditional_slot_bridges"][1].update(caller_pre_call_esp_relative_offset=0))
    def test_push_binding(self):
        self.reject(lambda d:d["conditional_slot_bridges"][0].update(actual_argument_value_abi_owner_or_stack_alias_binding_proven=True))
    def test_store_effect(self):
        self.reject(lambda d:d["shared_store_shape"].update(actual_instruction_effect_or_value_known=True))
    def test_scalar_evaluated(self):
        self.reject(lambda d:d["scalar_shapes"][0]["conditional_full_width_model"].update(evaluated_original_result=1))
    def test_wrong_effect_width(self):
        def mutate(d):
            e=next(e for e in d["stack_effect_candidates"] if e["syntax_class"]=="push")
            e["esp_delta"]=-2
        self.reject(mutate)
    def test_edge_count(self):
        self.reject(lambda d:d["bounded_edges"].pop())
    def test_state_model_cap(self):
        self.reject(lambda d:d["stack_model"].update(known_offset_limit=100))
    def test_payload(self):
        self.reject(lambda d:d.update(raw_bytes="forbidden"))

if __name__=="__main__":unittest.main()
