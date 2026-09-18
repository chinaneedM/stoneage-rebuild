import unittest

from tools.stoneage_save_logout_model import (
    failed_logout_save_data_loss_risk,
    logout_ack_result,
    logout_drop_items,
    logout_sequence,
    normal_logout_uses_save,
    observed_normal_save_false_callsite,
    periodic_character_save_due,
    periodic_save_sweep_due,
    saac_save_sequence,
    save_request,
    save_send_return_value,
    serialization_surface,
)


class SaveLogoutModelTests(unittest.TestCase):
    def test_global_periodic_sweep_uses_strictly_more_than_ten_seconds(self):
        self.assertFalse(periodic_save_sweep_due(110, 100))
        self.assertTrue(periodic_save_sweep_due(111, 100))

    def test_periodic_character_save_requires_login_and_strict_interval(self):
        self.assertFalse(
            periodic_character_save_due(
                connected=True,
                login_state="LOGIN",
                now_sec=280,
                last_save_sec=100,
                interval_sec=180,
            )
        )
        self.assertTrue(
            periodic_character_save_due(
                connected=True,
                login_state="LOGIN",
                now_sec=281,
                last_save_sec=100,
                interval_sec=180,
            )
        )
        self.assertFalse(
            periodic_character_save_due(
                connected=True,
                login_state="NOTLOGIN",
                now_sec=999,
                last_save_sec=0,
                interval_sec=180,
            )
        )

    def test_periodic_and_savepoint_do_not_unlock_but_logout_does(self):
        self.assertFalse(save_request(trigger="periodic")["unlock"])
        self.assertFalse(save_request(trigger="savepoint")["unlock"])
        self.assertTrue(save_request(trigger="logout")["unlock"])

    def test_save_send_does_not_wait_for_ack(self):
        self.assertFalse(save_request(trigger="logout")["wait_for_ack_before_return"])
        self.assertTrue(save_send_return_value(serialization_ok=True))

    def test_core_serialization_excludes_work_runtime_fields(self):
        surface = serialization_surface()
        self.assertIn("char_data_ints", surface["persisted"])
        self.assertIn("items", surface["persisted"])
        self.assertIn("pool_items", surface["persisted"])
        self.assertIn("carried_pets", surface["persisted"])
        self.assertIn("pool_pets", surface["persisted"])
        self.assertIn("work_ints", surface["runtime_only"])
        self.assertNotIn("work_ints", surface["persisted"])

    def test_later_depot_surfaces_are_versioned(self):
        base = serialization_surface()
        extended = serialization_surface(
            include_depot_item=True,
            include_depot_pet=True,
        )
        self.assertNotIn("depot_items", base["persisted"])
        self.assertNotIn("depot_pets", base["persisted"])
        self.assertIn("depot_items", extended["persisted"])
        self.assertIn("depot_pets", extended["persisted"])

    def test_drop_at_logout_items_are_deleted_before_snapshot(self):
        items = (
            {"id": 1, "drop_at_logout": False},
            {"id": 2, "drop_at_logout": True},
            None,
        )
        out = logout_drop_items(items)
        self.assertEqual(out["items_after_cleanup"][0]["id"], 1)
        self.assertIsNone(out["items_after_cleanup"][1])
        self.assertEqual(out["deleted"][0]["id"], 2)

    def test_logout_exits_battle_before_drop_cleanup_and_save(self):
        seq = logout_sequence(in_battle=True, save=True)
        self.assertLess(seq.index("battle_exit"), seq.index("delete_drop_at_logout_items"))
        self.assertLess(
            seq.index("delete_drop_at_logout_items"),
            seq.index("send_async_save_unlock_true"),
        )

    def test_logout_deletes_runtime_character_after_send_not_ack(self):
        seq = logout_sequence(in_battle=False, save=True)
        self.assertLess(
            seq.index("send_async_save_unlock_true"),
            seq.index("delete_runtime_character"),
        )
        self.assertNotIn("wait_for_save_ack", seq)

    def test_saac_unlocks_before_disk_write_on_logout_save(self):
        seq = saac_save_sequence(unlock=True)
        self.assertLess(seq.index("unlock_account"), seq.index("write_character_file"))

    def test_periodic_save_does_not_unlock_account(self):
        seq = saac_save_sequence(unlock=False)
        self.assertNotIn("unlock_account", seq)

    def test_failed_logout_save_has_no_retry_or_runtime_rollback(self):
        result = logout_ack_result(False)
        self.assertEqual(result["client_message"], "Cannot save")
        self.assertEqual(result["connection_state_after"], "NOTLOGIN")
        self.assertEqual(result["character_index_after"], -1)
        self.assertFalse(result["retry"])
        self.assertFalse(result["rollback_runtime_character"])
        self.assertTrue(failed_logout_save_data_loss_risk())

    def test_fixed_normal_logout_paths_save(self):
        self.assertTrue(normal_logout_uses_save())
        self.assertFalse(observed_normal_save_false_callsite())


if __name__ == "__main__":
    unittest.main()
