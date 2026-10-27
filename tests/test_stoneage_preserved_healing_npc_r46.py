"""Synthetic parser and source-boundary guards for the limited R46 artifact."""
import hashlib
import unittest
from tools.stoneage_preserved_healing_npc_r46 import (
    parse_create_text, fingerprint, sha, EXPECTED_SHA256, EXPECTED_BYTES,
    SOURCE_SCOPE, derive_from_verified_bytes, decode_qualified
)

SAMPLE = """NPCCREATE
{
floorid: 100
borncenter: 2,3,1,1
name: 治療師
graphicname: 100012
functionset: NPCHealer
dialogue: 原文不应公开
}
{
floorid: 101
borncenter: 5,9,1,1
name: 第二人
healer: Healer|file:abc.arg
}
"""
class OriginalHealerParsing(unittest.TestCase):
    def test_header_and_two_complete_blocks(self):
        blocks,lines = parse_create_text(SAMPLE)
        self.assertEqual(len(blocks),2)
        self.assertEqual(blocks[0]["open_line"],2)
        self.assertEqual(blocks[1]["fields"][2]["original_name"],"第二人")
        self.assertEqual(blocks[0]["fields"][0]["integer_values"],[100])
        self.assertEqual(lines, SAMPLE.count("\n"))

    def test_original_name_retained_but_dialogue_redacted(self):
        blocks,_ = parse_create_text(SAMPLE)
        raw = str(blocks)
        self.assertIn("治療師",raw)
        self.assertIn("NPCHealer",raw)
        self.assertNotIn("原文不应公开",raw)

    def test_refs_only_whitelisted(self):
        blocks,_=parse_create_text(SAMPLE)
        fields={x["key"]:x for x in blocks[1]["fields"]}
        self.assertEqual(fields["healer"]["declared_reference_token"],"Healer|file:abc.arg")
        self.assertNotIn("declared_reference_token",fields["name"])

    def test_duplicate_field_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            parse_create_text("NPCCREATE\n{\nname:A\nname:B\n}\n")

    def test_nested_blocks_rejected(self):
        with self.assertRaisesRegex(ValueError,"nested"):
            parse_create_text("NPCCREATE\n{\n{\nname:A\n}\n}\n")

    def test_missing_header_rejected(self):
        with self.assertRaisesRegex(ValueError,"header"):
            parse_create_text("{\nname:A\n}\n")

    def test_stray_code_is_not_silently_skipped(self):
        with self.assertRaisesRegex(ValueError,"unclassified"):
            parse_create_text("NPCCREATE\n{\nname:A\nexecute(param)\n}\n")

    def test_no_unclosed_block(self):
        with self.assertRaisesRegex(ValueError,"unterminated"):
            parse_create_text("NPCCREATE\n{\nname:A\n")

    def test_source_pin_invariance(self):
        self.assertEqual(EXPECTED_BYTES,649)
        self.assertEqual(EXPECTED_SHA256,"1d7d71960958cc60c5e6ba686fede736b5d66ec15f5d58300041a8a2de893847")
        self.assertIn("NOT_OFFICIAL_TW10",SOURCE_SCOPE)
        with self.assertRaisesRegex(ValueError,"hash"):
            decode_qualified(b"NPCCREATE\n")

    def test_digest_protected_payload_not_returned(self):
        b="敏感对话".encode()
        self.assertEqual(fingerprint(b),{"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
        self.assertNotIn("敏感",str(fingerprint(b)))

if __name__=="__main__":
    unittest.main()
