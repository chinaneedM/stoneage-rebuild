import hashlib,unittest
from unittest.mock import patch
from tools import stoneage_party_pet_original_reward_item_audit as item

class RewardItemTests(unittest.TestCase):
    def test_complete_state_oracles_and_automatic_release_retained(self):
        for p in ('gavin','bismarck'):
            text=item.item_observations(p)
            for marker in ('whole original item array oracle','whole seven actor terminal oracle','whole arena terminal oracle','original terminal arena counter decremented','REAL_HEADER_PET_GROWTH','REAL_HEADER_PLAYER_LEVEL'):
                self.assertIn(marker,text)
            self.assertNotIn('memcpy(slots,round_baseline',text)

    def test_source_and_added_dependency_mutations_rejected(self):
        bodies={'_ITEM_endExistItemsOne':'original'}
        frozen={n:hashlib.sha256(b.encode()).hexdigest() for n,b in bodies.items()}
        for changed in ({'_ITEM_endExistItemsOne':'fake'},bodies|{'_CHAR_setItemIndex':'fake'}):
            with self.assertRaisesRegex(ValueError,'dependency drift'):
                item.pet.player.validate_bodies(changed,frozen)

    def test_inherited_growth_anchor_drift_rejected(self):
        with patch.object(item.pet,'pet_observations',return_value='drift'):
            with self.assertRaisesRegex(ValueError,'anchor drift'):item.item_observations('gavin')

    def test_versioned_stale_slot_and_capacity(self):
        g=item.substitutions('gavin',item.PREP)
        b=item.substitutions('bismarck',item.PREP)
        self.assertIn('reward_slot++;',g)
        self.assertNotIn('reward_slot++;',b)
        self.assertIn('reward_limit=CHAR_MAXITEMHAVE',g)
        self.assertIn('reward_limit=CheckCharMaxItem(0)',b)

    def test_recipient_packets_and_full_inventory_release(self):
        for p in ('gavin','bismarck'):
            text=item.item_observations(p)
            self.assertIn('mode==2?1:0',text)
            self.assertIn('mode==2?"Reward|||":"|||"',text)
            self.assertIn('mode==0||mode==3?"Reward|||":"|||"',text)
            self.assertIn('expected_item_count=',text)
            self.assertIn('expected_items[250].use=0',text)

if __name__=='__main__':unittest.main()
