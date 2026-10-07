import unittest

from tools.stoneage_becomepig_clock_audit import step_expected, MAPS


class ClockOwnershipTests(unittest.TestCase):
    def test_duplicate_eligible_connections_visit_same_actor_in_slot_order(self):
        # Three distinct eligible connections reach actor2. Starting at2, the
        # second visit expires world state; the third sees the inactive marker.
        pigs,last,cycles,calls,reads=step_expected('gavin',[2]*4,[0]*4,15,15,MAPS[5],0,0,1,1,{1})
        self.assertEqual((pigs,last,cycles,reads),([2,2,-1,2],1,1,2))
        self.assertEqual(calls,[[0]*4,[0]*4,[1]*4,[0]*4])

    def test_default_service_exclusion_difference_changes_battle_count(self):
        for excluded,want in (({1},7),({1,2},8)):
            pigs,*_=step_expected('gavin',[10]*4,[1]*4,15,15,MAPS[5],0,0,1,1,excluded)
            self.assertEqual(pigs,[10,10,want,10])

    def test_player_array_owner_ignores_unusable_connection_topology(self):
        pigs,last,cycles,calls,_=step_expected('bismarck',[11]*4,[0]*4,5,0,MAPS[3],0,5,10,10,set())
        self.assertEqual((pigs,last,cycles),([0,11,0,11],10,6))
        self.assertEqual(calls,[[0,0,0,1],[0]*4,[0,0,0,1],[0]*4])

    def test_bismarck_world_subtraction_can_end_without_cleanup(self):
        pigs,_,_,calls,_=step_expected('bismarck',[0]*4,[0]*4,15,15,MAPS[0],0,0,10,10,set())
        self.assertEqual(pigs,[-1]*4)
        self.assertEqual(calls,[[0,0,0,1]]*4)

    def test_gap_does_not_catch_up_and_second_time_sample_controls_next_poll(self):
        pigs,last,cycles,_,reads=step_expected('bismarck',[60]*4,[1]*4,15,15,MAPS[0],0,5,1000,1002,set())
        self.assertEqual((pigs,last,cycles,reads),([50]*4,1002,6,2))
        after=step_expected('bismarck',pigs,[1]*4,15,15,MAPS[0],last,cycles,1001,1001,set())
        self.assertEqual((after[0],after[1],after[2],after[4]),([50]*4,1002,6,1))

    def test_cycle_wrap_and_battle_zero_to_world_cleanup_are_versioned(self):
        result=step_expected('bismarck',[1]*4,[1]*4,15,15,MAPS[0],0,10000,10,10,set())
        self.assertEqual((result[0],result[2]),([0]*4,0))
        after=step_expected('bismarck',result[0],[0]*4,15,15,MAPS[0],10,0,20,20,set())
        self.assertEqual(after[0],[-1]*4)
        self.assertEqual(after[3],[[0,0,0,1]]*4)
        clean=step_expected('iris',[0]*4,[0]*4,15,15,MAPS[0],1,0,2,2,{1,2})
        self.assertEqual(clean[0],[-1,0,0,-1])
        self.assertEqual(clean[3],[[1]*4,[0]*4,[0]*4,[1]*4])


if __name__=='__main__':unittest.main()
