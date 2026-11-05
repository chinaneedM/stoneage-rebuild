from hashlib import sha256
import json
from pathlib import Path
import unittest


DATA = Path(__file__).resolve().parents[1] / "research/recovered"
WORLD17 = DATA / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-17-MAP-BGM-SOURCE-R1.json"
WORLD18 = DATA / "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json"


class BattleEntryBgmSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(WORLD18.read_bytes())
        cls.parent_bytes = WORLD17.read_bytes()
        cls.parent = json.loads(cls.parent_bytes)

    def test_exact_parent_source_and_track_identity(self):
        report = self.report
        self.assertEqual(report["world17_sha256"], sha256(self.parent_bytes).hexdigest())
        self.assertEqual(report["client_message"], "EN")
        self.assertEqual(report["clients"]["taiwan10_retail"]["exe_sha256"],
                         self.parent["taiwan10"]["client_exe"]["sha256"])
        late = report["clients"]["mixed25_saved"]
        self.assertEqual(late["exe_sha256"], self.parent["mixed25_archive"]["client_exe"]["sha256"])
        self.assertEqual(late["netcom_exe_sha256"], self.parent["mixed25_archive"]["netcom_exe"]["sha256"])
        self.assertEqual(report["slots"], {
            str(i): self.parent["shared_table_rows"][i]["requested_path"] for i in (5, 6)
        })
        self.assertEqual(report["slots"], {"5": "data/bgm/sabgm_b0.wav", "6": "data/bgm/sabgm_b1.wav"})

    def test_both_clients_take_the_same_track_for_the_tested_positive_results(self):
        r = self.report
        rows = r["client_positive_result_witnesses"]
        self.assertEqual([a["result"] for a in rows], list(range(1, 7)))
        for row in rows:
            n = row["result"]
            early = [int(n == 2), int(n in {2, 6})]
            later = early + [int(n == 4)]
            self.assertEqual(row["taiwan10_flags"], early)
            self.assertEqual(row["mixed25_flags"], later)
            for profile, actual in (("taiwan10_retail", early), ("mixed25_saved", later)):
                self.assertEqual(row["entry_slot_after_this_update"],
                                 5 if actual != r["clients"][profile]["slot6_required_values"] else 6)
        self.assertEqual([a["entry_slot_after_this_update"] for a in rows], [5, 6, 5, 5, 5, 5])

    def test_server_types_join_to_the_en_results_in_the_same_saved_archive(self):
        server = self.report["mixed25_server"]
        self.assertEqual(server["send_symbol"], "lssproto_EN_send")
        self.assertEqual(server["type_field_offset"], 12)
        rows = server["positive_source_paths"]
        self.assertEqual([(a["symbol"], a["result"]) for a in rows],
                         [("BATTLE_CreateVsEnemy", 1), ("BATTLE_CreateVsPlayer", 2)])
        self.assertIn("NPC_NPCEnemy_BattleIn", rows[0]["named_incoming_paths"])
        self.assertEqual(rows[1]["named_incoming_paths"], ["lssproto_DU_recv", "ITEM_BattlePK"])
        self.assertEqual([len(a["send_calls_va"]) for a in rows], [1, 2])
        self.assertTrue(all(not value for value in self.report["bounds"].values()))


if __name__ == "__main__":
    unittest.main()
