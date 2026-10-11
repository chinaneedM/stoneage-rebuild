"""Mutation controls for pinned full-client PET sender source-only acceptance."""
import unittest
from tools.stoneage_pet_client_full_callgraph_audit import (
    PINNED, CLIENT_TREE, BLOBS, validate, MARK
)

def accepted():
    return "\n".join([
        "SOURCE_PET_CLIENT_GATE|pinned_commit=" + PINNED
        + "|client_tree=" + CLIENT_TREE
        + "|client_project_blob=" + BLOBS["client/stoneage.vcxproj"]
        + "|tracked_client_source_files=237|lexical_sender_sites=5"
        + "|lexical_caller_candidates=3|header_default_pet=0|vs_special_pet=0"
        + "|counterfactual_80_pet=1|client_sender_opcode=127|server_receiver_opcode=127"
        + "|runtime_packet_verified=0|deployed_client_binary_verified=0"
        + "|early_build_verified=0|inventory_sha256=" + "1"*64,
        "SOURCE_PET_CLIENT_SITE|kind=definition|path=client/stoneage/proto/protocol.cpp|line=2280",
        "SOURCE_PET_CLIENT_SITE|kind=declaration|path=client/stoneage/proto/protocol.h|line=462",
        "SOURCE_PET_CLIENT_SITE|kind=lexical_call_candidate|path=client/stoneage/system/menu.cpp|line=14824",
        "SOURCE_PET_CLIENT_SITE|kind=lexical_call_candidate|path=client/stoneage/system/menu.cpp|line=14966",
        "SOURCE_PET_CLIENT_SITE|kind=lexical_call_candidate|path=client/stoneage/system/menu.cpp|line=15333",
        "BOUNDARY|Full pinned tracked client source lexical scan found three _PET_ITEM UI call sites; checked-in VS special default excludes PET; no executed packet or deployed binary; no JSS1999/Taiwan1.0 inference",
        "OPEN|external/generated runtime client dispatch, optional version8 build, matching enabled server binary, actual item-owner transitions, natural alias and unique codes",
        MARK,
    ]) + "\n"

class PetClientPinnedGateTests(unittest.TestCase):
    def test_accepted_source_only_fixture(self):
        got = validate(accepted())
        self.assertEqual(got["lexical_caller_candidates"], "3")
        self.assertEqual(got["vs_special_pet"], "0")
    def test_false_runtime_and_version_promotion_rejected(self):
        for original, alternate in [
            ("runtime_packet_verified=0", "runtime_packet_verified=1"),
            ("deployed_client_binary_verified=0", "deployed_client_binary_verified=1"),
            ("early_build_verified=0", "early_build_verified=1"),
            ("header_default_pet=0", "header_default_pet=1"),
            ("vs_special_pet=0", "vs_special_pet=1"),
            ("counterfactual_80_pet=1", "counterfactual_80_pet=0"),
            ("lexical_caller_candidates=3", "lexical_caller_candidates=0"),
        ]:
            with self.subTest(original=original), self.assertRaises(ValueError):
                validate(accepted().replace(original, alternate))
    def test_wrong_header_dispatch_and_source_anchors_rejected(self):
        for original, alternate in [
            ("client_sender_opcode=127", "client_sender_opcode=128"),
            ("server_receiver_opcode=127", "server_receiver_opcode=128"),
            ("client_tree=" + CLIENT_TREE, "client_tree=" + "0"*40),
            ("client_project_blob=" + BLOBS["client/stoneage.vcxproj"], "client_project_blob=" + "0"*40),
            ("path=client/stoneage/proto/protocol.cpp", "path=client/stoneage/system/field.cpp"),
            ("line=2280", "line=2281"),
            ("kind=declaration", "kind=lexical_call_candidate"),
        ]:
            with self.subTest(original=original), self.assertRaises(ValueError):
                validate(accepted().replace(original, alternate))
    def test_report_schema_and_full_client_inventory_required(self):
        for replacement in [
            accepted().replace("tracked_client_source_files=237", "tracked_client_source_files=3"),
            accepted().replace("inventory_sha256="+"1"*64, "inventory_sha256=x"),
            accepted().replace("lexical_sender_sites=5", "lexical_sender_sites=2"),
            accepted().replace("runtime_packet_verified=0", "runtime_packet_verified=0|runtime_packet_verified=0"),
            accepted().replace("SOURCE_PET_CLIENT_SITE|kind=definition", "SOURCE_PET_CLIENT_UNKNOWN|kind=definition"),
        ]:
            with self.assertRaises(ValueError): validate(replacement)
    def test_missing_and_extra_line_rejected(self):
        lines = accepted().splitlines()
        for i in range(len(lines)):
            with self.subTest(i=i), self.assertRaises(ValueError):
                validate("\n".join(lines[:i]+lines[i+1:])+"\n")
        with self.assertRaises(ValueError):validate(accepted()+"SOURCE_PET_CLIENT_SITE|kind=other|path=x|line=1\n")
    def test_nonpromotion_boundary_required(self):
        with self.assertRaises(ValueError):
            validate(accepted().replace("no JSS1999/Taiwan1.0 inference", "JSS1999 confirmed"))

if __name__ == "__main__":
    unittest.main()
