import unittest,hashlib
from fractions import Fraction
from unittest.mock import patch
from tools import stoneage_party_pet_original_pet_growth_audit as pet
from tools import stoneage_party_pet_original_player_level_audit as player

class PetGrowthTests(unittest.TestCase):
    def test_rank_boundaries_and_growth_truncation(self):
        packed=(20,30,40,50);bins=(3,3,2,2)
        minimum=tuple(int((a+b)*Fraction(9,2)) for a,b in zip(packed,bins))
        maximum=tuple((a+b)*6 for a,b in zip(packed,bins))
        self.assertEqual(pet.GROWTH,(minimum,maximum,tuple(2*v for v in minimum),(0,0,0,0)))

    def test_derived_combat_stats_independently(self):
        for growth,derived in zip(pet.GROWTH,pet.DERIVED):
            v,s,t,d=(10000+x for x in growth)
            actual=(v//100,(20*s+2*t+2*v+d)//2000,(20*t+2*s+2*v+d)//2000,d//100,(4*v+s+t+d)//100)
            self.assertEqual(actual,derived)

    def test_growth_rand_stream_exact_indices_and_rank_endpoints(self):
        stream=(0,536870912,1073741824,1610612736)
        self.assertEqual(tuple(4*v//2147483648 for v in stream),(0,1,2,3))
        self.assertEqual(550+51*2147483647//2147483648,600)
        self.assertEqual(450+51*0//2147483648,450)

    def test_variable_ai_cap_once_and_repeated(self):
        self.assertEqual(tuple(min(10000,seed+up*500) for seed,up in zip(pet.VARIABLE_SEEDS,(1,1,2,0))),pet.VARIABLE_FINAL)

    def test_profile_pet_packet_does_not_change_teammate(self):
        for p in ('gavin','bismarck'):
            text=pet.pet_observations(p)
            code='4c92' if p=='bismarck' else '1'
            self.assertIn(f'"-2|1|{code},0|1|{code},,,,|||"',text)
            self.assertIn('whole seven actor terminal oracle',text)
            self.assertIn('whole arena terminal oracle',text)
            self.assertNotIn('memcpy(slots,round_baseline',text)
            self.assertIn('11*up',text)

    def test_inherited_player_fixture_drift_rejected(self):
        with patch.object(player,'level_observations',return_value='drift'):
            with self.assertRaisesRegex(ValueError,'anchor drift'):pet.pet_observations('gavin')

    def test_pet_growth_body_mutation_and_stub_rejected(self):
        bodies={'CHAR_PetLevelUp':'original'}
        frozen={n:hashlib.sha256(b.encode()).hexdigest() for n,b in bodies.items()}
        for changed in ({'CHAR_PetLevelUp':'fake'},bodies|{'CHAR_PetAddVariableAi':'fake'}):
            with self.assertRaisesRegex(ValueError,'dependency drift'):player.validate_bodies(changed,frozen)

if __name__=='__main__':unittest.main()
