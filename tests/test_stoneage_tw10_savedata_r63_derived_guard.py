"""R63 independent negative controls; all sample mnemonics are synthetic fixtures."""
import copy
import unittest
from tools.stoneage_tw10_savedata_r63_derived_guard import validate

CALLS=((0x4C68C,0x4C692),(0x4C6F1,0x4C6F7))
def fixture():
    sites=[]
    for call,post in CALLS:
        def row(site,mn):
            return {"site_rva":site,"mnemonic":mn,"operands":[],
                    "actual_instruction_effect_or_value_known":False}
        a=row(call,"call")
        b=row(post,"test")
        sites.append({
            "call_rva":call,"postcall_rva":post,
            "window_address_lower":call-32,"window_address_upper":post+48,
            "decoded_instruction_rows":[a,b],"bounded_local_edges":[[call,post]],
            "postcall_instruction":b,
            "import_name":"WriteFile","import_slot_rva":0x520A4,
            "syntactic_call_continuation_edge":True,
            "actual_callee_return_or_native_effect_proven":False,
            "actual_eax_return_register_value_proven":False,
            "actual_flags_or_branch_feasibility_proven":False,
            "native_api_result_eax_or_bytecount_proven":False,
        })
    return {
        "schema":"tw10-r63-original-postwritefile-static-operand-window",
        "runtime_sha256":"cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a",
        "candidate_root_rva":0x4C5B4,"candidate_graph_nodes":139,"candidate_graph_edges":156,
        "bounded_call_return_assumption_only":True,"sites":sites,
        "original_executable_executed":False,
        "original_savedata_payload_read_or_published":False,
        "actual_abi_or_register_stack_memory_preservation_proven":False,
        "actual_native_writefile_return_count_or_success_proven":False,
        "actual_buffer_flush_close_or_disk_persistence_proven":False,
        "original_savedata_schema_migration_or_server_authority_proven":False,
    }
class DerivedGuard(unittest.TestCase):
    def reject(self,change):
        d=fixture()
        change(d)
        with self.assertRaises(ValueError):validate(d)
    def test_synthetic_valid_does_not_accept_source_provenance(self):
        r=validate(fixture())
        self.assertEqual(r["guard"],"STRUCTURE_ONLY")
        self.assertFalse(r["original_static_source_artifact_cryptographically_pinned"])
    def test_wrong_runtime_sha(self):
        self.reject(lambda d:d.__setitem__("runtime_sha256","0"*64))
    def test_wrong_import_slot(self):
        self.reject(lambda d:d["sites"][1].__setitem__("import_slot_rva",0))
    def test_missing_postcall(self):
        self.reject(lambda d:d["sites"][0]["decoded_instruction_rows"].pop())
    def test_fake_success(self):
        self.reject(lambda d:d.__setitem__("actual_native_writefile_return_count_or_success_proven",True))
    def test_fake_abi(self):
        self.reject(lambda d:d.__setitem__("actual_abi_or_register_stack_memory_preservation_proven",True))
    def test_missing_call_edge(self):
        self.reject(lambda d:d["sites"][0]["bounded_local_edges"].clear())
    def test_forged_postcall_copy(self):
        self.reject(lambda d:d["sites"][1].__setitem__("postcall_instruction",{"site_rva":0}))
    def test_raw_code_leak(self):
        self.reject(lambda d:d["sites"][0]["decoded_instruction_rows"][0].__setitem__("bytes","90"))
    def test_duplicate_local_edge(self):
        self.reject(lambda d:d["sites"][0]["bounded_local_edges"].append(d["sites"][0]["bounded_local_edges"][0][:]))
    def test_wrong_call_opcode(self):
        self.reject(lambda d:d["sites"][0]["decoded_instruction_rows"][0].__setitem__("mnemonic","push"))
    def test_mutated_native_effect_flag(self):
        self.reject(lambda d:d["sites"][1].__setitem__("actual_eax_return_register_value_proven",True))
    def test_bad_window_bounds(self):
        self.reject(lambda d:d["sites"][1].__setitem__("window_address_upper",0))
    def test_duplicate_row(self):
        self.reject(lambda d:d["sites"][0]["decoded_instruction_rows"].append(copy.deepcopy(d["sites"][0]["decoded_instruction_rows"][1])))

if __name__=="__main__":
    unittest.main()
