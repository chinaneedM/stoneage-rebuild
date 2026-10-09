import json
import unittest
from tools.stoneage_character_reuse_audit import Oracle, PIN_PATH, PINNED, template, vectors


class CharacterReuseTests(unittest.TestCase):
    def test_domain_has_all_partition_masks_cursors_callback_modes_and_lazy_start(self):
        cases=vectors()
        self.assertEqual(len(cases),4224)
        self.assertEqual(len(set(cases)),len(cases))
        for kind,size in ((1,2),(2,2),(3,3),(4,3)):
            self.assertEqual({v[2] for v in cases if v[0]==kind},set(range(1<<size)))
            self.assertEqual({v[1] for v in cases if v[0]==kind},set(range(size)))
        self.assertTrue(all(v[1]==0 for v in cases if v[7]))

    def test_fresh_default_does_not_copy_source_work_ticket_or_object(self):
        for p in PINNED:
            for payload in (0,1):
                ch=template(p,54 if p=='bismarck' else 24,payload)
                self.assertEqual(ch['work'][1:4],[0,0,0])
                self.assertEqual(ch['work'][4],-1)
                self.assertEqual(ch['work'][5],0 if p=='bismarck' else -1)
                self.assertEqual(ch['opaque'],0)

    def test_partition_wrap_skips_occupied_slots(self):
        o=Oracle('gavin',24,(3,2,6,0,0,1,0,0))
        self.assertEqual(o.allocate(0),4)
        self.assertEqual(o.cursors,[0,2,5])
        self.assertEqual(o.slots[4]['work'][1:4],[0,0,0])
        self.assertEqual(o.slots[5]['work'][1:4],[999,900,88])

    def test_full_partition_does_not_borrow_from_another_partition(self):
        o=Oracle('gavin',24,(2,0,3,3,2,1,0,0))
        o.slots[4]['use']=0
        self.assertEqual(o.allocate(3),-1)
        self.assertEqual(o.trace,[90,1])
        self.assertEqual(o.seq,0)

    def test_failed_callback_retains_copy_without_advancing_or_constructing(self):
        o=Oracle('gavin',24,(3,0,6,2,2,1,0,0))
        self.assertEqual(o.allocate(2),-1)
        self.assertEqual(o.slots[4]['use'],0)
        self.assertEqual(o.slots[4]['work'][1:4],[901,902,903])
        self.assertEqual(o.slots[4]['functions'],[0,0])
        self.assertEqual((o.cursors,o.seq),([0,2,4],0))
        self.assertEqual(o.allocate(0),4)
        self.assertEqual(o.slots[4]['sequence'],0)

    def test_callback_receives_copied_use_before_success_forces_live(self):
        o=Oracle('iris',24,(1,0,2,1,0,0,0,0))
        self.assertEqual(o.allocate(1),0)
        self.assertEqual(o.trace[:8],[10,1,20,0,0,0,0,0])
        self.assertEqual(o.slots[0]['use'],1)
        self.assertEqual(o.slots[0]['functions'],[1,0])

    def test_dirty_input_and_callback_can_supply_state_independently_of_old_slot(self):
        for payload,cb,expected in ((2,0,[901,902,903]),(0,3,[777,666,9])):
            o=Oracle('bismarck',54,(3,0,6,cb,payload,1,0,0))
            self.assertEqual(o.allocate(cb),4)
            self.assertEqual(o.slots[4]['work'][1:4],expected)

    def test_direct_release_reuse_assigns_new_sequence_and_replaces_callback_fields(self):
        o=Oracle('gavin',24,(3,0,6,3,0,1,1,0))
        o.run()
        self.assertEqual(o.slots[4]['work'][1:4],[0,0,0])
        self.assertEqual(o.slots[4]['sequence'],1)
        self.assertEqual(o.slots[4]['functions'],[0,0])

    def test_source_receipt_keeps_template_creator_callbacks_and_abi_boundaries(self):
        rows=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual(set(rows),set(PINNED))
        for p,row in rows.items():
            self.assertEqual(row['source_sha'],PINNED[p])
            self.assertEqual(set(row['functions']),{'CHAR_getDefaultChar','CHAR_initCharOneArray','CHAR_constructFunctable','ENEMY_createEnemy'})
            self.assertTrue(all(row['contracts'].values()))


if __name__=='__main__':unittest.main()
