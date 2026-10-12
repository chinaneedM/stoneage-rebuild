"""R15 synthetic: conditional provenance, exact calls, no ABI promotion."""
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_entrycalls_r15 import (
    register_origins,query_origins,call_surfaces,frame_sites,inspect_verified,FLAGS,
)
ROOT=0x1000
BASE=0x400000

def decoder(raw):return Decoder(raw,ROOT,BASE)

class R15Synthetic(unittest.TestCase):
    def test_register_copy_is_not_value(self):
        # mov eax,5; mov ebx,eax; mov ebp,esp; ret
        dec=decoder(bytes.fromhex("b80500000089c389e5c3"))
        nodes,edges,_,_=bounded_graph(dec,ROOT)
        p=query_origins(dec,nodes,edges,[],[(ROOT+5,"eax"),(ROOT+7,"ebp")],ROOT)
        self.assertEqual(p[0]["origins"][0]["kind"],"definition")
        self.assertFalse(p[0]["fully_known_value"])
        self.assertEqual(p[1]["origins"][0]["kind"],"entry")

    def test_esp_definitions_are_not_ownership(self):
        dec=decoder(bytes.fromhex("5589e590c3"))
        nodes,edges,_,_=bounded_graph(dec,ROOT)
        origins=register_origins(nodes,edges,ROOT,"esp")
        self.assertTrue(origins[ROOT+3])
        self.assertTrue(all(k[0] in ("definition","entry") for k in origins[ROOT+3]))
        f=frame_sites(nodes)
        self.assertTrue(any(x["writes_ebp"] for x in f))

    def test_indirect_call_not_named(self):
        # call eax; ret
        dec=decoder(bytes.fromhex("ffd0c3"))
        nodes,_,_,_=bounded_graph(dec,ROOT)
        v=call_surfaces(dec,[ROOT],{},[],nodes)[0]
        self.assertEqual(v["kind"],"register_indirect")
        self.assertFalse(v["callee_effect_summary_admitted"])
        self.assertIsNone(v["import_identity"])

    def test_direct_call_is_candidate_only(self):
        dec=decoder(bytes.fromhex("e800000000c3"))
        nodes,_,_,_=bounded_graph(dec,ROOT)
        v=call_surfaces(dec,[ROOT],{},[],nodes)[0]
        self.assertEqual(v["direct_target_rva"],ROOT+5)
        self.assertFalse(v["runtime_transfer_proven"])

    def test_non_call_rejected(self):
        dec=decoder(bytes.fromhex("90c3"))
        nodes,_,_,_=bounded_graph(dec,ROOT)
        with self.assertRaises(ValueError):
            call_surfaces(dec,[ROOT],{},[],nodes)

    def test_no_unknown_original_promotion(self):
        self.assertIn("native_io_executed",FLAGS)
        self.assertIn("frame_setup_ownership_proven",FLAGS)

    def test_hash_guard(self):
        with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
            inspect_verified(b"not-original",b"invalid")

if __name__=="__main__":
    unittest.main()
