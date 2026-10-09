import json
import unittest
from tools.stoneage_exit_world_item_audit import Oracle,PIN_PATH,PINNED,vectors


def state(profile='gavin',kind=3,side=0,ptr=1,pattern=2,peer=0,active=1,layout=0,dest=2,ticket=999,per=17,otype=1):
    names=('CHAR_WORKBATTLEMODE','CHAR_WORKBATTLEINDEX','CHAR_WORKFOXROUND','CHAR_WORKTICKETTIME',
           'CHAR_WORKTICKETTIMESTART','CHAR_WORKENCOUNTPROBABILITY_MIN','CHAR_WORKENCOUNTPROBABILITY_MAX',
           'CHAR_ENCOUNT_FIX','CHAR_WORKOBJINDEX','CHAR_FLOOR','CHAR_X','CHAR_Y','CHAR_WHICHTYPE','CHAR_WORKPARTYMODE','CHAR_MAILMODE')
    c={n:i for i,n in enumerate(names)}
    o=Oracle(profile,c,{'items':54 if profile=='bismarck' else 24,'pool':30},
             (kind,side,ptr,pattern,peer,active,layout,dest,ticket,per,otype))
    row=o.run()
    return o,row


class ExitWorldItemTests(unittest.TestCase):
    def test_domain_preserves_nonplayer_partitions_and_ticket_boundaries(self):
        cases=vectors()
        self.assertEqual(len(cases),7056)
        self.assertEqual(len(set(cases)),len(cases))
        self.assertEqual({v[0] for v in cases},{2,3})
        self.assertEqual({v[1] for v in cases},{-1,0,1})
        self.assertEqual({v[8] for v in cases},{-1,0,999,1000,1001})

    def test_destroy_moves_retained_world_object_but_not_dead_actor_coordinates(self):
        for p in ('gavin','iris'):
            o,row=state(p)
            self.assertEqual(row[:3],(0,-101,0))
            self.assertEqual(o.coords,[7000,1,1])
            self.assertEqual(o.obj,[7001,41,6])
            self.assertEqual(o.cells[27],[0])
            self.assertEqual(o.cells[5],[])
            self.assertEqual(o.stale_write,8)
            self.assertEqual(o.work['CHAR_WORKTICKETTIME'],999)

    def test_bismarck_destroyed_subject_skips_actual_warp(self):
        o,row=state('bismarck')
        self.assertEqual(row[:3],(0,-101,0))
        self.assertEqual((o.warp_ret,o.move_ret),(-9,-9))
        self.assertEqual(o.obj,[7000,1,1])
        self.assertEqual(o.cells[5],[0])

    def test_live_player_carried_reference_prevents_item_death(self):
        for p in PINNED:
            for peer in (1,4):
                o,_=state(p,peer=peer)
                self.assertEqual((o.itemuse[100],o.owners[100],o.count),(1,7,1))
                self.assertFalse(o.itemuse[200])

    def test_pool_and_invalid_player_references_are_not_ownership_protection(self):
        for p in PINNED:
            for peer in (2,3):
                o,_=state(p,peer=peer)
                self.assertEqual((o.itemuse[100],o.owners[100],o.count),(0,-1,0))

    def test_unused_items_do_not_decrement_counter_or_change_owner(self):
        for p in PINNED:
            o,_=state(p,active=0)
            self.assertEqual(o.count,0)
            self.assertEqual(set(o.owners.values()),{7})

    def test_empty_slots_call_end_without_destroying_unrelated_live_items(self):
        for p in PINNED:
            o,_=state(p,pattern=0)
            self.assertEqual(o.ends,len(o.indices))
            self.assertEqual(o.count,len(o.indices))

    def test_warp_reports_success_after_missing_map_link(self):
        for p in PINNED:
            o,_=state(p,kind=2,layout=1)
            self.assertEqual((o.warp_ret,o.move_ret),(1,0))
            self.assertEqual(o.coords,o.obj)
            self.assertEqual(o.obj,[7001,41,6])
            self.assertFalse(any(0 in cell for cell in o.cells))

    def test_bismarck_recovers_misplaced_link_on_same_old_floor(self):
        for p in PINNED:
            o,_=state(p,kind=2,layout=2)
            self.assertEqual(o.move_ret,int(p=='bismarck'))
            self.assertEqual(o.cells[27],[0] if p=='bismarck' else [])
            self.assertEqual(o.cells[10],[] if p=='bismarck' else [0])

    def test_map_splice_retains_neighbors_and_appends_to_destination_tail(self):
        for p in PINNED:
            o,_=state(p,kind=2,layout=3)
            self.assertEqual(o.cells[5],[1,2])
            self.assertEqual(o.cells[27],[3,4,0])

    def test_invalid_destination_returns_false_after_live_ticket_consumption(self):
        for p in PINNED:
            o,_=state(p,kind=2,dest=0)
            self.assertEqual((o.warp_ret,o.move_ret),(0,-9))
            self.assertEqual(o.coords,o.obj)
            self.assertEqual(o.work['CHAR_WORKTICKETTIME'],0)

    def test_pointer_failure_avoids_destroy_and_same_floor_move_accepts_coordinates(self):
        for p in PINNED:
            o,row=state(p,ptr=0,dest=1,per=-1,otype=0)
            self.assertEqual(row[:4],(0,0,1,0))
            self.assertEqual(o.coords,[7000,41,6])
            self.assertEqual(o.cells[11],[0])
            self.assertEqual(o.work['CHAR_WORKENCOUNTPROBABILITY_MIN'],5)

    def test_source_receipt_keeps_static_allocator_and_runtime_boundaries_distinct(self):
        d=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual(set(d),set(PINNED))
        for p,row in d.items():
            self.assertEqual(row['source_sha'],PINNED[p])
            self.assertTrue(row['contracts']['allocator_body_static_inspection_only'])
            self.assertTrue(row['contracts']['allocator_replaces_slot_from_input_template'])
            self.assertEqual(row['contracts']['map_old_floor_misplaced_link_recovery'],p=='bismarck')


if __name__=='__main__':unittest.main()
