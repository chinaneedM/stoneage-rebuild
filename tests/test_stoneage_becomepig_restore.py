import unittest
from tools.stoneage_becomepig_restore_audit import Witness, vectors


def handles():
    keys=('HP','EXP','MP','DUELPOINT','CHARM','EARTH','WATER','FIRE','WIND','RIDEPET','BASEBASEIMAGENUMBER')
    return {'ITEM_FIST':0,**{'CHAR_P_STRING_'+key:1<<i for i,key in enumerate(keys)}}


def state(profile='gavin',**changes):
    names=('action','validchar','validbattle','use','side','pos','pig','old','eq','meta','ride','kind','dead','fox','fall')
    values=dict(zip(names,(1,1,1,1,0,0,180,100250,100015,0,0,1,0,-1,0)))
    values.update(changes)
    return Witness(profile,handles(),tuple(values[k] for k in names))


class WholeRestorationTests(unittest.TestCase):
    def test_invalid_battle_prevents_changes_but_unused_battle_has_prior_effects(self):
        blocked=state(validbattle=0,fox=2)
        self.assertEqual(blocked.execute(),-102)
        self.assertEqual(blocked.trace,[])
        self.assertEqual(blocked.i['CHAR_BASEIMAGENUMBER'],100250)
        unused=state(use=0,fox=2)
        self.assertEqual(unused.execute(),-103)
        self.assertEqual(unused.i['CHAR_BASEIMAGENUMBER'],100388)
        self.assertEqual(unused.w['CHAR_WORKFOXROUND'],-1)
        self.assertEqual(unused.w['CHAR_WORKBATTLEMODE'],1)
        self.assertIn((28,0,0),list(zip(*[iter(unused.trace)]*3)))

    def test_new_ride_lookup_can_replace_active_pig_image(self):
        for ride,image in ((1,300001),(2,300002),(3,100000)):
            w=state(action=0,ride=ride)
            self.assertEqual(w.execute(),1)
            self.assertEqual(w.i['CHAR_BECOMEPIG'],180)
            self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],image)
        b=state('bismarck',action=0,ride=1)
        self.assertEqual(b.execute(),1)
        self.assertEqual(b.i['CHAR_BASEIMAGENUMBER'],100250)
        self.assertNotIn(5,b.trace[::3])

    def test_item_or_npc_transform_early_return_keeps_ride_after_stat_rebuild(self):
        for meta in (2,3):
            w=state(action=0,meta=meta,ride=3)
            self.assertEqual(w.execute(),0)
            self.assertEqual((w.i['CHAR_RIDEPET'],w.i['CHAR_BASEIMAGENUMBER']),(0,100250))
            self.assertEqual((w.w['CHAR_WORKATTACKPOWER'],w.i['CHAR_HP']),(15,100))
            self.assertNotIn(5,w.trace[::3])

    def test_dead_compliance_still_rebuilds_and_caps_stats_before_appearance_guard(self):
        w=state(action=0,dead=1)
        self.assertEqual(w.execute(),1)
        self.assertEqual((w.i['CHAR_HP'],w.i['CHAR_MP']),(100,80))
        self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],100250)
        self.assertEqual(w.trace[::3],[1,2,3])

    def test_petfall_status_observes_minus_two_before_final_minus_one(self):
        w=state(fall=1)
        self.assertEqual(w.execute(),0)
        events=list(zip(*[iter(w.trace)]*3))
        negative=events.index((11,0,-2))
        self.assertEqual(events[negative+1][0:2],(21,0))
        self.assertEqual(events[negative+2],(11,0,-1))
        self.assertEqual((w.i['CHAR_BECOMEPIG'],w.i['CHAR_RIDEPET'],w.w['CHAR_WORKBATTLEMODE']),(180,-1,2))
        self.assertEqual((w.entries[0][0],w.entries[0][5]),(-1,-1))

    def test_additional_airplane_image_exception_is_versioned(self):
        for name,want in (('gavin',100015),('iris',100015),('bismarck',100362)):
            w=state(name,action=0,pig=-1,old=100362)
            self.assertEqual(w.execute(),1)
            self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],want)

    def test_corpus_retains_lower_player_entry_domain_and_inactive_hooks(self):
        vs=list(vectors())
        self.assertEqual(len(vs),27650)
        self.assertEqual(sum(v[0]==0 for v in vs),3074)
        self.assertEqual(sum(v[0]==1 for v in vs),24576)
        self.assertEqual({v[5] for v in vs if v[0] and v[4]>=0},{0,4})
        self.assertTrue(all(v[11]==1 for v in vs if v[0]))


if __name__=='__main__':unittest.main()
