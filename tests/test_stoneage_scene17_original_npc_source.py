import unittest
from tools.stoneage_scene17_original_npc_source import (
    PREFIX, TARGETS, MAX_HTTP_BYTES, MAX_HTTP_REQUESTS, member_subset, need,
)
from tools.stoneage_scene16_nearby_npc import SOURCE_PATH, SOURCE_SIZE, SOURCE_SHA256


class Scene17OriginalSource(unittest.TestCase):
    def test_fixed_two_original_members_only(self):
        self.assertEqual(set(TARGETS), {
            SOURCE_PATH, "npc/genout/npcgen.template"})
        self.assertEqual(TARGETS[SOURCE_PATH], (SOURCE_SIZE, SOURCE_SHA256))
        self.assertEqual(TARGETS["npc/genout/npcgen.template"][0], 4950)

    def test_bounded_source_not_entire_archive(self):
        self.assertLessEqual(MAX_HTTP_BYTES, 32*1024*1024)
        self.assertLessEqual(MAX_HTTP_REQUESTS, 512)
        self.assertTrue(PREFIX.endswith("/gmsv/data/"))

    def test_original_member_byte_gate_cannot_be_bypassed(self):
        from tools.stoneage_scene16_nearby_npc import probe
        with self.assertRaisesRegex(ValueError, "size and sha256 mismatch"):
            probe(b"NPCCREATE\n{\n}\n")

    def test_unsupported_duplicate_archive_member_is_not_success(self):
        with self.assertRaises(ValueError):
            need(False, "duplicate original archive member")

    def test_source_not_supplied_stays_unresolved(self):
        from tools.stoneage_scene16_nearby_npc import probe
        self.assertEqual(probe(None)["source_status"], "SOURCE_NOT_SUPPLIED")


if __name__ == "__main__":
    unittest.main()
