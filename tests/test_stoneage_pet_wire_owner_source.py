"""Strict negative checks: source capability must not become executable history."""
import unittest
from tools.stoneage_pet_wire_owner_source_audit import COMMIT, MARK, validate_report

GATE={
  "source_commit":COMMIT,"source_blobs":9,"wire_integer_fields":5,
  "client_server_opcode":127,"decoder_checksum_guard":1,
  "authenticated_connection_gate":1,"trade_and_battle_restrictions":1,
  "menu_source_calls":3,"native_actor_slot_index_swaps":4,
  "native_slot_setter_unique_hook":1,"conditional_unique_code_regenerator":1,
  "effective_real_pair_verified":0,"emitted_live_packet_verified":0,
  "native_owner_lifecycle_executed":0,"early_version_verified":0,
}
NAMES=["client_serializer","server_decoder","server_callback","native_swap","slot_setter","unique_hook"]
def example():
    return "\n".join(
        ["SOURCE_PET_WIRE_OWNER_GATE|"+"|".join(f"{k}={v}" for k,v in GATE.items())]
        +[f"SOURCE_PET_CHAIN_BODY|name={name}|sha256={'a'*64}" for name in NAMES]
        +["BOUNDARY|Late pinned source-only optional PET wire-order and actor-slot-index changes; no deployed binary, live packet, item owner/unique-code runtime claim or JSS1999/Taiwan1.0 promotion",
          "OPEN|Build-compatible enabled client/server pair; runtime opcode127 dispatch; natural PET item ownership and persistent unique-code before/after move",
          MARK])+"\n"
class SourceOnlyPetWireOwnerTests(unittest.TestCase):
    def test_bounded_source_receipt(self):
        self.assertEqual(validate_report(example())["source_blobs"],"9")
    def test_runtime_or_original_promotion_rejected(self):
        for key in ("effective_real_pair_verified","emitted_live_packet_verified",
                    "native_owner_lifecycle_executed","early_version_verified"):
            with self.subTest(key=key),self.assertRaises(ValueError):
                validate_report(example().replace(key+"=0",key+"=1"))
    def test_wire_and_guard_mutations_rejected(self):
        for k,v in (("source_blobs","8"),("wire_integer_fields","6"),
                    ("client_server_opcode","128"),("decoder_checksum_guard","0"),
                    ("authenticated_connection_gate","0"),("trade_and_battle_restrictions","0"),
                    ("menu_source_calls","2"),("native_actor_slot_index_swaps","3"),
                    ("native_slot_setter_unique_hook","0"),("conditional_unique_code_regenerator","0")):
            with self.subTest(key=k),self.assertRaises(ValueError):
                validate_report(example().replace(k+"="+str(GATE[k]),k+"="+v))
    def test_body_metadata_not_missing_or_swapped(self):
        for name in NAMES:
            with self.subTest(name=name),self.assertRaises(ValueError):
                validate_report(example().replace("name="+name,"name=wrong"))
        with self.assertRaises(ValueError):
            validate_report(example().replace("sha256="+"a"*64,"sha256=wrong"))
    def test_duplicate_fields_missing_lines_and_boundary(self):
        src=example()
        with self.assertRaises(ValueError):
            validate_report(src.replace("|source_blobs=9","|source_blobs=9|source_blobs=9"))
        parts=src.splitlines()
        for i in range(len(parts)):
            with self.subTest(line=i),self.assertRaises(ValueError):
                validate_report("\n".join(parts[:i]+parts[i+1:])+"\n")
        with self.assertRaises(ValueError):
            validate_report(src.replace("source-only","deployed"))
        with self.assertRaises(ValueError):
            validate_report(src.replace("JSS1999/Taiwan1.0","proven"))
if __name__=="__main__":unittest.main()
