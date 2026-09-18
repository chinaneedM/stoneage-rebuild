import unittest

from tools.stoneage_pet_growth_model import (
    allocation_counts,
    individualize_growth_base,
    pack_growth_base,
    pet_level_increments,
    pet_rank_from_template_base,
    unpack_growth_base,
)


class PetGrowthModelTests(unittest.TestCase):
    def test_rank_thresholds(self):
        self.assertEqual(pet_rank_from_template_base(25,25,25,25),0)
        self.assertEqual(pet_rank_from_template_base(24,24,24,23),1)
        self.assertEqual(pet_rank_from_template_base(23,23,22,22),2)
        self.assertEqual(pet_rank_from_template_base(22,21,21,21),3)
        self.assertEqual(pet_rank_from_template_base(20,20,20,20),4)
        self.assertEqual(pet_rank_from_template_base(10,10,10,10),5)

    def test_pack_roundtrip(self):
        base=(21,22,23,24)
        self.assertEqual(unpack_growth_base(pack_growth_base(*base)),base)

    def test_birth_offsets(self):
        self.assertEqual(
            individualize_growth_base((20,20,20,20),(-2,-1,1,2)),
            (18,19,21,22),
        )
        with self.assertRaises(ValueError):
            individualize_growth_base((20,20,20,20),(-3,0,0,0))

    def test_ten_rolls_always_sum_to_ten(self):
        counts=allocation_counts([0,0,0,1,1,2,2,2,3,3])
        self.assertEqual(counts,(3,2,3,2))
        self.assertEqual(sum(counts),10)

    def test_level_increment_uses_base_plus_allocations_times_rank_roll(self):
        increments=pet_level_increments(
            growth_base=(20,20,20,20),
            rank=0,
            allocation_rolls=[0,0,0,1,1,2,2,2,3,3],
            rank_roll=500,
        )
        self.assertEqual(increments,(115,110,115,110))

    def test_rank_range_validation(self):
        with self.assertRaises(ValueError):
            pet_level_increments((20,20,20,20),5,[0]*10,549)
        self.assertEqual(
            pet_level_increments((20,20,20,20),5,[0]*10,550)[0],
            165,
        )


if __name__=="__main__":
    unittest.main()
