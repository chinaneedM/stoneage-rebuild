"""R64 synthetic negative controls; no fake instruction is historical evidence."""
import copy
import json
import unittest
from tools.stoneage_tw10_savedata_r64_flag_count import trace,inspect_raw,R28_BLOB,R63_JSON_SHA
from tests.test_stoneage_tw10_savedata_r63_derived_guard import fixture
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/"research/recovered"
class R64Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r28=json.loads((BASE/"STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json").read_text())
    def fabricated(self):
        s=fixture()
        w=next(x for x in self.r28["contexts"] if x["api"]=="WriteFile")
        for item,source in zip(s["sites"],w["api_sites"]):
            call=item["call_rva"];post=item["postcall_rva"]
            rows=item["decoded_instruction_rows"]
            rows[1].update({"mnemonic":"test","operands":[
                {"kind":"register","register":"eax","width_bytes":4},
                {"kind":"register","register":"eax","width_bytes":4}],
                "decoder_read_registers":["eax"],"decoder_written_registers":["eflags"]})
            branch=post+2
            row={"site_rva":branch,"mnemonic":"jne","operands":[],
                 "actual_instruction_effect_or_value_known":False}
            # Branch outcomes must lie within 48 bytes of the postcall site.
            fall=branch+2;target=branch+8
            rows.extend([row,{"site_rva":fall,"mnemonic":"nop","operands":[],
                              "actual_instruction_effect_or_value_known":False},
                         {"site_rva":target,"mnemonic":"nop","operands":[],
                              "actual_instruction_effect_or_value_known":False}])
            for p in source["push_candidates"]:
                rows.append({"site_rva":p["site_rva"],"mnemonic":"push",
                             "operands":[copy.deepcopy(p["input"])],"actual_instruction_effect_or_value_known":False})
            rows.sort(key=lambda z:z["site_rva"])
            item["bounded_local_edges"]=[
                [call,post],[post,branch],[branch,fall],[branch,target]]
            item["bounded_local_edges"].sort()
            item["postcall_instruction"]=next(x for x in rows if x["site_rva"]==post)
        return s
    def reject(self,change):
        r=self.fabricated()
        change(r)
        with self.assertRaises(ValueError):trace(r,self.r28)
    def test_synthetic_two_sites_keep_native_unknown(self):
        d=trace(self.fabricated(),self.r28)
        self.assertEqual(len(d["postcall_contexts"]),2)
        self.assertTrue(all(x["postcall_test_has_explicit_eax_operand"] for x in d["postcall_contexts"]))
        self.assertTrue(all(len(x["physical_push_candidates"])==5 for x in d["postcall_contexts"]))
        self.assertTrue(all(x["immediate_successor_is_conditional_jump"] for x in d["postcall_contexts"]))
        self.assertFalse(d["original_native_writefile_executed"])
        self.assertFalse(d["actual_flush_close_or_disk_persistence_proven"])
    def test_synthetic_inputs_do_not_alias_pinned_r28_reference(self):
        d=self.fabricated()
        w=next(x for x in self.r28["contexts"] if x["api"]=="WriteFile")
        row=next(x for x in d["sites"][1]["decoded_instruction_rows"] if x["site_rva"]==313064)
        before=copy.deepcopy(w["api_sites"][1]["push_candidates"][3]["input"])
        row["operands"][0]["register"]="ebx"
        self.assertEqual(w["api_sites"][1]["push_candidates"][3]["input"],before)

    def test_r63_exact_hash_bitflip_fails(self):
        with self.assertRaises(ValueError):
            inspect_raw(b"{}",(BASE/"STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json").read_bytes())
    def test_r28_changed_blob_fails(self):
        with self.assertRaises(ValueError):
            inspect_raw(b"{}",b"{}")
    def test_forged_eax_value(self):
        r28=copy.deepcopy(self.r28)
        w=next(x for x in r28["contexts"] if x["api"]=="WriteFile")
        w["inputs"]["queries"][-1]["actual_register_value_known"]=True
        # All mutation-negative tests directly target checked source fields below.
        q=next(x for x in w["inputs"]["queries"] if x["site_rva"]==0x4C692 and x["register"]=="eax")
        q["actual_register_value_known"]=True
        with self.assertRaises(ValueError):trace(self.fabricated(),r28)
    def test_wrong_postcall_opcode(self):
        self.reject(lambda r:r["sites"][0]["postcall_instruction"].__setitem__("mnemonic","cmp"))
    def test_missing_structural_fallthrough(self):
        self.reject(lambda r:r["sites"][0]["bounded_local_edges"].remove([r["sites"][0]["postcall_rva"],r["sites"][0]["postcall_rva"]+2]))
    def test_invalid_push_operand_vs_original(self):
        self.reject(lambda r:next(x for x in r["sites"][1]["decoded_instruction_rows"] if x["site_rva"]==313064)["operands"][0].__setitem__("register","ebx"))
    def test_missing_bytes_written_slot(self):
        self.reject(lambda r:r["sites"][0]["decoded_instruction_rows"].remove(next(x for x in r["sites"][0]["decoded_instruction_rows"] if x["site_rva"]==312958)))
    def test_forged_root_graph(self):
        self.reject(lambda r:r.__setitem__("candidate_graph_nodes",100))
    def test_corrupt_source_truth(self):
        self.reject(lambda r:r.__setitem__("actual_native_writefile_return_count_or_success_proven",True))
    def test_missing_flags_write(self):
        self.reject(lambda r:r["sites"][0]["postcall_instruction"].__setitem__("decoder_written_registers",[]))
    def test_one_branch_target_outside_window_stays_conditional_partial(self):
        r=self.fabricated()
        x=r["sites"][0]
        x["bounded_local_edges"].remove([x["postcall_rva"]+2,x["postcall_rva"]+10])
        d=trace(r,self.r28)
        self.assertFalse(d["postcall_contexts"][0]["both_branch_successors_inside_r63_window"])
        self.assertEqual(len(d["postcall_contexts"][0]["immediate_branch_successors"]),1)
    def test_missing_all_branch_edges_fails(self):
        def tamper(r):
            x=r["sites"][0]
            x["bounded_local_edges"]=[e for e in x["bounded_local_edges"] if e[0]!=x["postcall_rva"]+2]
        self.reject(tamper)

if __name__=="__main__":
    unittest.main()
