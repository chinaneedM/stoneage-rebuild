import unittest
from unittest.mock import patch
from tools import stoneage_party_pet_reward_ownership_audit as own

class OwnershipTests(unittest.TestCase):
    def test_escape_oracle_exact_distinct_sequences(self):
        self.assertEqual(own.escape_oracle(own.NAME),own.ESCAPED)
        self.assertEqual(own.escape_oracle('plain'), 'plain')
        self.assertEqual(own.escape_oracle('\\n'),'\\yn')

    def test_complete_original_layout_oracles_retained(self):
        for p in ('gavin','bismarck'):
            text=own.ownership_observations(p)
            for phrase in ('whole original shared item array oracle','whole seven actor terminal oracle','whole arena terminal oracle','REAL_HEADER_PLAYER_LEVEL','REAL_HEADER_PET_GROWTH','original terminal arena counter decremented'):
                self.assertIn(phrase,text)
            self.assertNotIn('memcpy(slots,round_baseline',text)

    def test_exact_packets_use_literal_not_gameplay_escape(self):
        for p in ('gavin','bismarck'):
            text=own.ownership_observations(p)
            self.assertIn('Reward|Reward||',text)
            self.assertIn(r'R\\c\\z\\y\\n|Second||',text)
            self.assertNotIn('makeEscapeString',text)

    def test_source_drift_rejected_before_composition(self):
        with patch.object(own.item.pet,'pet_observations',return_value='drift'):
            with self.assertRaisesRegex(ValueError,'anchor drift'):own.ownership_observations('gavin')

    def test_pool_reference_and_original_item_lifetime_distinct(self):
        text=own.ownership_observations('gavin')
        self.assertIn('expected_items[250].use=0',text)
        self.assertIn('slots[1].indexOfExistPoolItems[0]=250',text)
        self.assertIn('pool reference retained independently of item lifetime',text)
        self.assertIn('expected_item_count=ITEM_UseItemnum-(mode==1)',text)

    def test_duplicate_add_and_carried_release_are_separate(self):
        text=own.ownership_observations('bismarck')
        self.assertIn('mode==2?250:251',text)
        self.assertIn('reward_warning_count==(mode==0?2:0)',text)
        self.assertIn('reward_duplicate_warning_count==(mode==0?1:0)',text)
        self.assertIn('reward_one_count==(mode>=2?2:0)',text)

if __name__=='__main__':unittest.main()
