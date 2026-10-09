import json
import unittest

from tools.stoneage_watch_cleanup_audit import Oracle, vectors, PIN_PATH, PINNED


def stages(row):
    result=[];offset=0
    for _ in range(3):
        size=46+row[offset+45]
        result.append(row[offset:offset+size]);offset+=size
    if offset != len(row):
        raise ValueError('unexpected snapshot tail')
    return result


class WatchCleanupTests(unittest.TestCase):
    def test_domain_covers_every_physical_order_without_duplicate_rows(self):
        cases=list(vectors())
        self.assertEqual(len(cases),9225)
        self.assertEqual(len(set(cases)),len(cases))
        for count,expected in enumerate((5,20,60,120)):
            orders={v[4:4+count+1] for v in cases if v[1] == count}
            self.assertEqual(len(orders),expected)
            self.assertTrue(all(len(set(o)) == count+1 for o in orders))

    def test_root_finish_late_in_array_needs_another_scan(self):
        r=stages(Oracle('gavin',(1,3,0,4,4,0,1,2)).run())
        self.assertEqual([s[1] for s in r],[4,2,0])
        self.assertEqual([s[0] for s in r],[-1,4,2])
        # Immediate residual slots 1,2 stay linked after slot0/root deletion.
        self.assertEqual(r[1][2+8:2+8+4],(1,5,-1,2))
        self.assertEqual(r[1][2+16:2+16+4],(1,5,1,-1))

    def test_root_finish_early_in_array_cleans_in_same_scan(self):
        r=stages(Oracle('iris',(1,3,0,9,0,1,2,3)).run())
        self.assertEqual([s[1] for s in r],[4,0,0])
        self.assertEqual([s[0] for s in r],[-1,3,0])

    def test_direct_finish_immediate_residual_is_not_permanent(self):
        for profile in PINNED:
            r=stages(Oracle(profile,(0,3,0,0,4,0,1,2)).run())
            self.assertEqual([s[1] for s in r],[2,0,0])
            self.assertEqual(r[0][42:45],(16,23,17))
            self.assertEqual(r[1][44],23)

    def test_stop_root_does_not_imply_watch_actor_exit(self):
        r=stages(Oracle('gavin',(2,3,0,0,4,0,1,2)).run())
        self.assertEqual([s[1] for s in r],[4,3,3])
        self.assertEqual(r[1][42:45],(16,16,16))
        for node in (0,1,2):
            self.assertEqual(r[2][2+8*node+4],node+1)

    def test_dead_or_pet_only_watch_nodes_are_empty_for_countalive(self):
        for kind in (1,2):
            r=stages(Oracle('gavin',(2,3,kind,0,4,0,1,2)).run())
            self.assertEqual([s[1] for s in r],[4,0,0])
        live=stages(Oracle('gavin',(2,3,0,0,4,0,1,2)).run())
        self.assertEqual(live[2][1],3)

    def test_watchstop_deferred_cleanup_and_profile_flag_difference(self):
        for profile in PINNED:
            r=stages(Oracle(profile,(4,3,0,4,4,0,1,2)).run())
            self.assertEqual([s[1] for s in r],[4,1,1])
            for node in (0,1,2):
                self.assertEqual(r[0][2+8*node+4],-1)
                self.assertEqual(r[0][2+8*node+7],0 if profile=='bismarck' else 9)
            self.assertEqual(r[0][42:45],(0,7,0))
            self.assertEqual(r[1][44],7)

    def test_source_identity_pins_default_original_task_bodies(self):
        rows=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual(set(rows),set(PINNED))
        for profile,d in rows.items():
            self.assertEqual(d['source_sha'],PINNED[profile])
            self.assertEqual(d['contracts']['watch_stop_clears_watch_type'],profile=='bismarck')
            self.assertEqual(set(d['functions']),{'BATTLE_Stop','BATTLE_StopSet','BATTLE_FinishSet',
                'BATTLE_CountAlive','BATTLE_WatchStop','BATTLE_Loop'})
            self.assertTrue(all(len(x)==64 for x in d['functions'].values()))
            self.assertTrue(d['prior_domain']['contracts']['watch_delete_loop_reads_current_next_after_unlink'])


if __name__=='__main__':
    unittest.main()
