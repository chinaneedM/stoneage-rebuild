import tempfile
import unittest
from pathlib import Path

from tools.stoneage_local_filesystem_persistence import (
    LOCAL_FILESYSTEM_PERSISTENCE_PROFILE,
    LocalFilesystemPersistenceStore,
)
from tools.stoneage_local_runtime_core import LocalPersistenceStore


class LocalFilesystemPersistenceTests(unittest.TestCase):

    def _store(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "nested" / "saves"
        return temp, LocalFilesystemPersistenceStore(root)

    def test_store_satisfies_local_persistence_protocol_and_creates_root(self):
        _, store = self._store()
        self.assertIsInstance(store, LocalPersistenceStore)
        self.assertTrue(store.root.is_dir())
        self.assertEqual(
            store.profile_id,
            LOCAL_FILESYSTEM_PERSISTENCE_PROFILE,
        )

    def test_utf8_payload_round_trips_byte_exactly(self):
        _, store = self._store()
        payload = '{"schema":"stoneage.local-runtime-save.r1","note":"石器時代\\nA\\r\\nB"}'
        store.save("slot-1", payload)
        self.assertEqual(store.load("slot-1"), payload)

        files = tuple(store.root.iterdir())
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].name.endswith(".save.json"))
        self.assertNotIn("slot-1", files[0].name)
        self.assertEqual(files[0].read_bytes(), payload.encode("utf-8"))

    def test_save_replaces_existing_slot_and_leaves_no_temp_file(self):
        _, store = self._store()
        store.save("slot", "first")
        store.save("slot", "second")
        self.assertEqual(store.load("slot"), "second")
        files = tuple(store.root.iterdir())
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].name.endswith(".save.json"))

    def test_distinct_logical_keys_use_distinct_files(self):
        _, store = self._store()
        store.save("slot-a", "A")
        store.save("slot-b", "B")
        self.assertEqual(store.load("slot-a"), "A")
        self.assertEqual(store.load("slot-b"), "B")
        self.assertEqual(
            len(tuple(store.root.glob("*.save.json"))),
            2,
        )

    def test_path_like_key_cannot_escape_configured_root(self):
        temp, store = self._store()
        outside = Path(temp.name) / "escape.save.json"
        store.save("../../escape", "safe")
        self.assertEqual(store.load("../../escape"), "safe")
        self.assertFalse(outside.exists())
        self.assertEqual(
            len(tuple(store.root.glob("*.save.json"))),
            1,
        )

    def test_missing_slot_returns_none(self):
        _, store = self._store()
        self.assertIsNone(store.load("missing"))

    def test_blank_keys_and_non_text_payloads_fail_closed(self):
        _, store = self._store()
        with self.assertRaisesRegex(ValueError, "non-empty"):
            store.save("   ", "payload")
        with self.assertRaisesRegex(ValueError, "non-empty"):
            store.load("")
        with self.assertRaisesRegex(TypeError, "must be text"):
            store.save("slot", b"bytes")


if __name__ == "__main__":
    unittest.main()
