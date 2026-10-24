import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "tools"))
from stoneage_cn2001_early_social_r112 import validate

D = json.loads((ROOT / "research/recovered/STONEAGE-CN2001-EARLY-SOCIAL-R112.json").read_text(encoding="utf-8"))

class R112Boundaries(unittest.TestCase):
    def test_reference_passes(self):
        self.assertTrue(validate(D))
    def reject(self, edit):
        v=copy.deepcopy(D)
        edit(v)
        with self.assertRaises(AssertionError):
            validate(v)
    def test_reject_false_primary_claim(self):
        self.reject(lambda x:x["sources"][0].update(source_rank="ORIGINAL_2001_OPERATOR_HTML"))
    def test_reject_invented_original_sha(self):
        self.reject(lambda x:x["sources"][0].update(original_2001_html_sha256="invented"))
    def test_reject_false_independent_confirmation(self):
        self.reject(lambda x:x["sources"][0].update(independent_2001_confirmation=True))
    def test_reject_tw10_identity(self):
        self.reject(lambda x:x["version"].update(tw10_or_jss1999_identity_proven=True))
    def test_reject_relabel_prize(self):
        self.reject(lambda x:x["valentine"]["reward_tiers"][0].update(source_label="金暴"))
    def test_reject_unsupported_reward_count(self):
        self.reject(lambda x:x["valentine"]["reward_tiers"][0].update(winners_per_server_listed=100))
    def test_reject_misdated_meeting_room(self):
        self.reject(lambda x:x["valentine"]["claimed_rooms"][0].update(time="12:00"))
    def test_reject_server_transaction(self):
        self.reject(lambda x:x["valentine"].update(server_reward_confirmation=True))
    def test_reject_npc_id(self):
        self.reject(lambda x:x["valentine"].update(npc_master_id=123))
    def test_reject_unsupported_high_level_bands(self):
        self.reject(lambda x:x["migration"].update(higher_bands_unspecified=False))
    def test_reject_migration_done(self):
        self.reject(lambda x:x["migration"].update(network_migration_log="SUCCESS"))
    def test_reject_friend_card_schema(self):
        self.reject(lambda x:x["migration"].update(friend_card_persistence_schema="known"))
    def test_reject_leaking_winner_names(self):
        self.reject(lambda x:x["valentine"].update(usernames_intentionally_not_copied=False))
    def test_reject_cross_version_runtime(self):
        self.reject(lambda x:x["acceptance"].update(runtime_implementation_restored=True))
    def test_reject_claimed_original_bytes(self):
        self.reject(lambda x:x["acceptance"].update(original_first_party_bytes_restored=True))
    def test_reject_duplicate_record(self):
        self.reject(lambda x:x["records"].append(copy.deepcopy(x["records"][0])))

if __name__ == "__main__":
    unittest.main()
