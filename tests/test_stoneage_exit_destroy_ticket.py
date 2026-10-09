import json
import unittest
from tools.stoneage_exit_destroy_ticket_audit import Oracle,handles,vectors,PIN_PATH,PINNED


def symbolic_handles():
    # Public oracle receives the same symbolic field names, never original ABI ordinals.
    names=('CHAR_WORKBATTLEMODE','CHAR_WORKBATTLEINDEX','CHAR_WORKFOXROUND',
           'CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKPARTYMODE')
    return {**{n:j for j,n in enumerate(names)},'CHAR_WORKPARTYINDEX1':610}


def witness(profile='gavin',kind=3,ptr=1,party=1,owner=1,ticket=999,start=900,
            pattern=2,side=0,pos=9,guards=(1,1,1)):
    limits={'items':54 if profile=='bismarck' else 24,'pool':30}
    return Oracle(profile,symbolic_handles(),limits,
        (kind,*guards,side,pos,ptr,party,owner,ticket,start,pattern,2,1)).run()


def trace(row):
    if row[54]!=len(row)-55:raise ValueError('trace cardinality')
    return list(zip(row[55::3],row[56::3],row[57::3]))


class ExitDestroyTicketTests(unittest.TestCase):
    def test_domain_all_nonplayer_positions_and_excluded_player_cleanup(self):
        cases=vectors()
        self.assertEqual(len(cases),32676)
        self.assertEqual(len(set(cases)),len(cases))
        for kind in (2,3):
            self.assertEqual({(v[4],v[5]) for v in cases if v[0]==kind},
                             {(-1,0),*((s,p) for s in (0,1) for p in range(10))})
        self.assertTrue(all(v[4]<0 or not all(v[1:4]) for v in cases if v[0]==1))

    def test_actual_destroy_rejects_second_exit_and_unlinks_items_before_hooks(self):
        for profile,size in (('gavin',54),('iris',54),('bismarck',84)):
            row=witness(profile)
            self.assertEqual(row[:5],(0,-101,0,size,size))
            self.assertEqual(row[7],0)
            item_events=[e for e in trace(row) if e[0]==40]
            self.assertEqual(len(item_events),size)
            self.assertEqual(trace(row).count((41,0,0)),1)

    def test_expired_stale_ticket_invokes_warp_hook_but_clear_is_rejected(self):
        for profile in ('gavin','iris'):
            row=witness(profile)
            self.assertEqual(row[5:7],(10,2))
            self.assertEqual(row[12:14],(999,900))
            self.assertIn((33,0,0),trace(row))
            self.assertEqual(sum(e[0]==32 for e in trace(row)),2)
        row=witness('bismarck')
        self.assertEqual(row[5:7],(0,0))
        self.assertFalse(any(e[0] in (32,33,42) for e in trace(row)))

    def test_ticket_boundary_requires_strict_positive_before_now(self):
        for ticket in (-1,0,1000,1001):
            for profile in PINNED:
                row=witness(profile,ticket=ticket)
                self.assertFalse(any(e[0] in (32,33) for e in trace(row)))
                self.assertEqual(row[12],ticket)

    def test_pointer_failure_preserves_live_slot_and_allows_ticket_clear(self):
        for profile in PINNED:
            row=witness(profile,ptr=0)
            self.assertEqual(row[:5],(0,0,1,0,0))
            self.assertEqual(row[12:14],(0,0))
            self.assertIn((33,0,1),trace(row))

    def test_pet_and_unmatched_player_do_not_destroy_character(self):
        for profile in PINNED:
            for kind,side in ((2,0),(1,-1)):
                row=witness(profile,kind=kind,side=side)
                self.assertEqual(row[:5],(0,0,1,0,0))
                self.assertFalse(any(e[0] in (31,40,41) for e in trace(row)))
                self.assertEqual(sum(e[0]==33 for e in trace(row)),1)

    def test_owner_guard_is_separate_from_subject_guard(self):
        for profile in PINNED:
            row=witness(profile,kind=2,party=2,owner=0)
            notifications=[e for e in trace(row) if e[0]==42]
            self.assertEqual(len(notifications),0 if profile=='bismarck' else 4)
            self.assertIn((33,0,1),trace(row))  # subject remains live

    def test_item_end_receives_empty_slots_too_without_claiming_item_destruction(self):
        for profile in PINNED:
            row=witness(profile,pattern=0)
            self.assertTrue(all(e[2]==-1 for e in trace(row) if e[0]==40))
            self.assertEqual(row[3],84 if profile=='bismarck' else 54)

    def test_actual_battle_guard_rejects_unused_bismarck_before_fox_restore(self):
        for profile in PINNED:
            row=witness(profile,guards=(1,1,0))
            self.assertEqual(row[:2],(-102,-102) if profile=='bismarck' else (-103,-103))
            self.assertEqual(row[8],100250 if profile=='bismarck' else 100000)

    def test_identity_preserves_guard_disagreement_and_live_setters(self):
        rows=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual(set(rows),set(PINNED))
        for profile,d in rows.items():
            self.assertEqual(d['source_sha'],PINNED[profile])
            self.assertEqual(d['contracts']['ticket_subject_guard'],profile=='bismarck')
            self.assertTrue(d['contracts']['integer_and_work_setters_guard_live_slot'])
            self.assertEqual(set(d['setters']),{'_CHAR_setInt','_CHAR_setWorkInt'})


if __name__=='__main__':unittest.main()
