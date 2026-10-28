"""Negative controls: synthetic parsing never authenticates private original evidence."""
import copy
import unittest
from tools.stoneage_scene16_nearby_npc import (
    SOURCE_PATH, SOURCE_SIZE, SOURCE_SHA256, TARGET, public_index, probe,
    parse_blocks, inside_target, summarize_candidate,
)


def fixture(x="63,103,63,103", floor="1000", enemy="npcgen_test|1", name=b"private"):
    return (b"NPCCREATE\n{\nfloorid=" + floor.encode()
            + b"\nborncorner=" + x.encode()
            + b"\nname=" + name + b"\ncreatenum=1\ndir=6\ntime=0\n"
            + b"graphicname=16023\nenemy=" + enemy.encode() + b"\n}\n")


class Scene16Gate(unittest.TestCase):
    def test_real_public_manifest_pin_and_arrival(self):
        anchor = public_index()
        self.assertEqual((anchor["file"], anchor["bytes"], anchor["sha256"]),
                         (SOURCE_PATH, SOURCE_SIZE, SOURCE_SHA256))
        self.assertEqual(anchor["anchor_arrival"], [1000, 63, 99])
        self.assertEqual(anchor["investigation_target"], list(TARGET))
        self.assertFalse(anchor["target_is_npc_source_verified"])

    def test_no_private_source_does_not_invent_npc(self):
        r = probe(None)
        self.assertEqual(r["source_status"], "SOURCE_NOT_SUPPLIED")
        self.assertIsNone(r["matched_count"])
        self.assertEqual(r["matched_candidates"], [])
        self.assertIsNone(r["overall_completion_percent"])
        for k in ("original_world_entered", "same_deployed_build_authenticated",
                  "original_npc_interaction_verified", "official_tw10_npc_authenticated"):
            self.assertFalse(r[k], k)

    def test_source_presence_is_not_satisfied_by_synthetic_bytes(self):
        with self.assertRaisesRegex(ValueError, "size and sha256 mismatch"):
            probe(fixture())

    def test_length_only_same_as_original_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "size and sha256 mismatch"):
            probe(fixture().ljust(SOURCE_SIZE, b"#"))

    def test_template_only_rejected(self):
        with self.assertRaisesRegex(ValueError, "template without"):
            probe(None, b"any")

    def test_parse_exact_synthetic_bytes_and_no_plaintext_name_export(self):
        b = parse_blocks(fixture(name=b"do_not_publish"), b"NPCCREATE")
        self.assertEqual(len(b), 1)
        self.assertTrue(inside_target(b[0]["fields"]))
        public = summarize_candidate(b[0], None)
        self.assertNotIn("do_not_publish", repr(public))
        self.assertIsNone(public["original_dialogue"])
        self.assertEqual(public["template_binding"], "TEMPLATE_SOURCE_NOT_SUPPLIED")
        self.assertEqual(public["numeric_source_fields"]["graphicname"], 16023)
        self.assertEqual(public["name_original_raw_bytes"], len(b"do_not_publish"))

    def test_same_cell_wrong_floor_rejected(self):
        b = parse_blocks(fixture(floor="1001"), b"NPCCREATE")
        self.assertFalse(inside_target(b[0]["fields"]))

    def test_neighboring_cell_cannot_be_silently_assumed_same_npc(self):
        b = parse_blocks(fixture(x="63,102,63,102"), b"NPCCREATE")
        self.assertFalse(inside_target(b[0]["fields"]))

    def test_bounded_source_spawn_range_matches_only_when_containing_target(self):
        b = parse_blocks(fixture(x="62,102,64,104"), b"NPCCREATE")
        self.assertTrue(inside_target(b[0]["fields"]))

    def test_inverted_or_malformed_source_rectangle_rejected(self):
        for x in ("64,104,62,102", "63,103", "63,foo,63,103"):
            with self.subTest(x=x), self.assertRaises(ValueError):
                b = parse_blocks(fixture(x=x), b"NPCCREATE")
                inside_target(b[0]["fields"])

    def test_duplicate_field_refused(self):
        raw = fixture().replace(b"floorid=1000", b"floorid=1000\nfloorid=1001")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_blocks(raw, b"NPCCREATE")

    def test_truncated_file_refused(self):
        with self.assertRaises(ValueError):
            parse_blocks(fixture()[:-3], b"NPCCREATE")

    def test_wrong_magic_refused(self):
        with self.assertRaises(ValueError):
            parse_blocks(fixture().replace(b"NPCCREATE", b"NPCTEMPLATE", 1), b"NPCCREATE")

    def test_no_fake_template_binding_without_unique_matching_source(self):
        b = parse_blocks(fixture(), b"NPCCREATE")[0]
        tmpl = parse_blocks(
            b"NPCTEMPLATE\n{\ntemplatename=npcgen_test\nfunctionset=Unknown\n}\n",
            b"NPCTEMPLATE")
        p = summarize_candidate(b, tmpl)
        self.assertEqual(p["template_binding"], "EXACT_TEMPLATE_NAME_IN_PINNED_MEMBER")
        self.assertEqual(p["functionset_token"], "Unknown")
        p = summarize_candidate(b, tmpl + tmpl)
        self.assertEqual(p["template_binding"], "AMBIGUOUS_DUPLICATES")
        self.assertEqual(p["matching_template_blocks"], 2)

    def test_template_names_never_join_on_prefix(self):
        b = parse_blocks(fixture(), b"NPCCREATE")[0]
        tmpl = parse_blocks(
            b"NPCTEMPLATE\n{\ntemplatename=npcgen_test_alt\nfunctionset=Other\n}\n",
            b"NPCTEMPLATE")
        self.assertEqual(summarize_candidate(b, tmpl)["template_binding"], "MISSING_MATCH")


if __name__ == "__main__":
    unittest.main()
