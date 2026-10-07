import json
import unittest
from tools.stoneage_becomepig_badstatus_audit import Witness, clear_fields, handles, vectors, PIN_PATH, FEATURES


def state(profile='gavin', action=2, kind=1, petpig=180, mask=3, owned=1, seed=73):
    features={key:False for key in FEATURES}
    for key in ('_OTHER_MAGICSTAUTS','_IMPRECATE_ITEM','_PETSKILL_SETDUCK','_MAGICPET_SKILL','_BATTLE_PROPERTY','_PETSKILL_BECOMEPIG'):
        features[key]=True
    features['_PROFESSION_SKILL']=profile!='bismarck'
    tables={'StatusTbl':['-1','CHAR_WORKPOISON','CHAR_WORKOBLIVION','CHAR_WORKNOCAST'],
            'MagicTbl':['-1','CHAR_DEFMAGICSTATUS','CHAR_MAGICSUPERWALL']}
    status=' '.join('CHAR_P_STRING_'+s for s in ('HP','EXP','MP','DUELPOINT','CHARM','EARTH','WATER','FIRE','WIND','RIDEPET','BASEBASEIMAGENUMBER'))
    c=handles([status+' CHAR_ISDIE CHAR_BATTLEPROPERTY CHAR_WHICHTYPE ITEM_FIST'], '',tables,features)
    v=(action,1,1,1,0,0,180,100250,100015,0,0,kind,1,-1,0)+(petpig,mask,owned,seed)
    return Witness(profile,c,v,tables,features)


class BadStatusCompositionTests(unittest.TestCase):
    def test_player_clears_owned_pet_counter_but_preserves_own_pig(self):
        w=state();self.assertEqual(w.execute(),0)
        self.assertEqual((w.i['CHAR_BECOMEPIG'],w.ints[1]['CHAR_BECOMEPIG']),(180,-1))
        self.assertEqual(w.properties,[0,ord('x')])
        self.assertEqual(w.flags[0]['CHAR_ISDIE'],0)

    def test_null_property_returns_after_early_status_and_death_before_late_and_pet(self):
        w=state(mask=2);w.execute()
        self.assertTrue(all(w.w[key]==0 for key in w.early))
        self.assertTrue(all(w.w[key]==73 for key in w.late))
        self.assertEqual((w.flags[0]['CHAR_ISDIE'],w.ints[1]['CHAR_BECOMEPIG']),(0,180))
        self.assertNotIn(34,w.trace[::3]);self.assertNotIn(36,w.trace[::3])

    def test_property_construct_precedes_late_profession_and_owned_pet_write(self):
        w=state();w.execute();events=list(zip(*[iter(w.trace)]*3))
        construct=events.index((34,0,0));late=events.index((35,0,w.c['CHAR_MYSKILLHIT']))
        self.assertLess(construct,late);self.assertLess(late,events.index((36,1,-1)))

    def test_pet_subject_does_not_reset_its_own_counter(self):
        for mask in range(4):
            w=state(action=3,mask=mask);w.execute()
            self.assertEqual(w.ints[1]['CHAR_BECOMEPIG'],180)
            self.assertNotIn(36,w.trace[::3])

    def test_nonplayer_or_absent_ownership_does_not_touch_pet_counter(self):
        for kind,owned in ((2,1),(3,1),(1,0)):
            w=state(kind=kind,owned=owned);w.execute()
            self.assertEqual(w.ints[1]['CHAR_BECOMEPIG'],180)

    def test_composed_exit_continues_after_null_clear(self):
        w=state(action=1,mask=0);w.execute()
        self.assertEqual((w.w['CHAR_WORKBATTLEMODE'],w.i['CHAR_BECOMEPIG']),(2,180))
        self.assertEqual(w.ints[1]['CHAR_BECOMEPIG'],180)
        self.assertIn(24,w.trace[::3]);self.assertIn(22,w.trace[::3]);self.assertIn(29,w.trace[::3])

    def test_versioned_profession_and_actual_loop_counts_are_not_flattened(self):
        self.assertTrue(state().late);self.assertEqual(state('bismarck').late,[])
        pins=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual({n:(p['status_count'],p['magic_count']) for n,p in pins.items()},
                         {'gavin':(44,6),'iris':(44,6),'bismarck':(12,6)})

    def test_bismarck_clears_nocast_before_unused_battle_error_but_not_invalid_battle(self):
        for profile in ('gavin','iris','bismarck'):
            for validbattle in (0,1):
                w=state(profile,action=1)
                v=list(w.v);v[2]=validbattle;v[3]=0;w.v=tuple(v)
                self.assertEqual(w.execute(),-103 if validbattle else -102)
                self.assertEqual(w.w['CHAR_WORKNOCAST'],0 if profile=='bismarck' and validbattle else 73)
                self.assertNotIn(25,w.trace[::3])

    def test_domain_excludes_invalid_rider_and_keeps_half_valid_pointers(self):
        vs=list(vectors())
        self.assertTrue(all(v[10]==0 for v in vs if not v[17]))
        self.assertEqual({v[16] for v in vs},set(range(4)))
        self.assertEqual({v[18] for v in vs},{-7,0,73})
        self.assertEqual(sum(v[0]>=2 for v in vs),1152)


if __name__=='__main__':unittest.main()
