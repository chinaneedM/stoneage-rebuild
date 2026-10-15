"""R61 adversarial guards: never promote inherited static evidence to execution."""
import copy
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_r61_gap_ledger import derive, inspect, SITES

BASE=Path(__file__).resolve().parents[1]/"research/recovered"
def source(n):
    return (BASE/f"STONEAGE-TW10-SAVEDATA-NATIVE-IO-R{n}-ORIGINAL.json").read_bytes()

class R61Gaps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={n:source(n) for n in (28,44,45)}
        cls.original=[json.loads(cls.raw[n]) for n in (28,44,45)]
    def reject(self, fn):
        arr=copy.deepcopy(self.original)
        fn(*arr)
        with self.assertRaises(ValueError):
            derive(*arr)
    def test_source_custody_and_exact_gaps(self):
        c=inspect(self.raw)
        self.assertEqual(len(c["postcall_sites"]),2)
        self.assertEqual([x["postcall_eax_source"] for x in c["postcall_sites"]],["unknown_call"]*2)
        self.assertEqual([x["prior_graph_site_reached"] for x in c["postcall_sites"]],[True,False])
        self.assertEqual(len(c["precise_missing_evidence"]),5)
        self.assertFalse(c["actual_savedata_written_bytes_flush_close_or_persistence_proven"])
    def test_mutated_blob_rejected(self):
        raw=dict(self.raw)
        b=bytearray(raw[44]);b[9]^=1;raw[44]=bytes(b)
        with self.assertRaises(ValueError): inspect(raw)
    def test_r28_postcall_forged_value(self):
        def f(a,b,c):
            w=next(x for x in a["contexts"] if x["api"]=="WriteFile")
            q=next(x for x in w["inputs"]["queries"] if x["site_rva"]==SITES[0][1] and x["register"]=="eax")
            q["actual_register_value_known"]=True
        self.reject(f)
    def test_r28_forged_source(self):
        def f(a,b,c):
            w=next(x for x in a["contexts"] if x["api"]=="WriteFile")
            q=next(x for x in w["inputs"]["queries"] if x["site_rva"]==SITES[1][1] and x["register"]=="eax")
            q["reaching_candidates"][0]["origin"]="definition"
        self.reject(f)
    def test_r28_fake_prior_reachability(self):
        self.reject(lambda a,b,c:next(x for x in a["contexts"] if x["api"]=="WriteFile")["api_sites"][1].__setitem__("prior_graph_site_reached",True))
    def test_r44_fake_stack_frame_proof(self):
        self.reject(lambda a,b,c:b.__setitem__("actual_esp_stack_contents_or_frame_preservation_proven",True))
    def test_r44_stack_inventory_mutation(self):
        self.reject(lambda a,b,c:next(x for x in b["native_contexts"] if x["native_root_candidate_rva"]==0x4c5b4)["inherited_stack_effect_candidates"].pop())
    def test_r45_fake_write_count(self):
        self.reject(lambda a,b,c:c.__setitem__("actual_entry_count_or_api_transferred_bytes_proven",True))
    def test_r45_fake_frame_preservation(self):
        self.reject(lambda a,b,c:c.__setitem__("actual_write_frame_preservation_or_callee_effects_proven",True))
    def test_r45_fake_import(self):
        self.reject(lambda a,b,c:next(x for x in c["native_api_contexts"] if x["site_rva"]==0x4c68c)["identity"]["import_identity"].__setitem__("iat_rva",0))
    def test_r45_forged_postcall_definition(self):
        def f(a,b,c):
            w=next(x for x in c["native_api_contexts"] if x["site_rva"]==0x4c68c)
            w["direct_definition_shapes"].append({"site_rva":0x4c692})
            w["direct_definition_count"]+=1
        self.reject(f)
    def test_source_noncustody_promotion(self):
        self.reject(lambda a,b,c:a.__setitem__("native_io_executed",True))
    def test_graph_limit_tamper(self):
        self.reject(lambda a,b,c:next(x for x in a["contexts"] if x["api"]=="WriteFile")["graph"].__setitem__("frontier",[1]))

if __name__=="__main__":
    unittest.main()
