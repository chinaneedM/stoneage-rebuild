import json
import unittest
from tools.stoneage_becomepig_lookup_audit import (
    PIN_PATH, Witness, array, equipment, numeric_initializer, pet_index,
    player_index, ride_number, fixture, handles, helper_vectors,
)
from tools.stoneage_becomepig_badstatus_audit import FEATURES


def domain(profile='gavin'):
    return {'identity':{'equipment_index_argument':profile=='bismarck','maxnoindex':2,'item_fist':0,
                       'features':{'_ITEM_EQUITSPACE':True,'_NEW_RIDEPETS':profile!='bismarck'}},
            'tables':{'CHAR_eqimagetbl':[[100,101,102,103,104],[100,201,202,203,204]],
                      'ridePetTable':[[300,100,800,9],[301,100,800,10],[0,0,0,0]],
                      'RideCodeMode':[[800,1],[800,2],[801,2]],
                      'RPlistMode':[[100,0,1],[100,1,1]],
                      'RideNoList':[[[400,401],0],[[500,501],0]]}}


def state(profile='gavin',**changes):
    features={key:False for key in FEATURES}
    features['_BATTLE_PROPERTY']=features['_PETSKILL_BECOMEPIG']=True
    tables={'StatusTbl':['-1','CHAR_WORKNOCAST'],'MagicTbl':['-1']}
    status=' '.join('CHAR_P_STRING_'+s for s in ('HP','EXP','MP','DUELPOINT','CHARM','EARTH','WATER','FIRE','WIND','RIDEPET','BASEBASEIMAGENUMBER'))
    d=domain(profile);c=handles([status+' CHAR_ISDIE CHAR_BATTLEPROPERTY CHAR_WHICHTYPE'], '',tables,features,d)
    v=fixture(**({'base':100,'pbase':800,'petold':800}|changes))
    return Witness(profile,c,v,tables,features,d)


class OriginalLookupTests(unittest.TestCase):
    def test_integer_parser_supports_nested_masks_and_rejects_code_and_overflow(self):
        self.assertEqual(numeric_initializer('{{1, (1 << 3)}, {-2, 0}}'),[[1,8],[-2,0]])
        for value in ('{x}','{f()}','{1.0}','{1 << 100}','{2147483648}','{True}'):
            with self.assertRaises(ValueError):numeric_initializer(value)

    def test_array_keeps_declared_bound_distinct_from_initializers(self):
        _,rows,dims=array('tagRidePetTable ridePetTable[8]={{1,2,3,4},{5,6,7,8}};','ridePetTable')
        self.assertEqual(dims,'[8]');self.assertEqual(len(rows),2)

    def test_equipment_first_duplicate_wins_and_category_boundary_is_excluded(self):
        d=domain();self.assertEqual(equipment(d,0,100,1,0,999),101)
        for cat in (-2,-1,6):self.assertEqual(equipment(d,0,100,cat,1,999),-1)
        with self.assertRaises(ValueError):equipment(d,0,100,5,1,999)
        self.assertEqual(equipment(d,0,900,5,0,999),-1)

    def test_only_bismarck_live_belt_bypasses_table_and_category_guard(self):
        d=domain('bismarck')
        for category in (-1,1,5,6):self.assertEqual(equipment(d,0,100,category,1,999),999)
        with self.assertRaises(ValueError):equipment(d,-1,100,5,1,999)
        self.assertEqual(equipment(domain(),0,100,1,1,999),101)

    def test_ride_first_match_mask_selection_and_bounded_coordinate(self):
        d=domain()
        self.assertEqual(player_index(d,100),0)
        self.assertEqual(pet_index(d,800,0),-1)
        self.assertEqual(pet_index(d,800,3),0)
        self.assertEqual(pet_index(d,800,2),1)
        self.assertEqual(pet_index(d,800,-1),0)
        self.assertEqual(ride_number(d,0,1),401)
        for index,ti in ((-1,0),(2,0),(0,-1),(0,2)):self.assertEqual(ride_number(d,index,ti),-1)

    def test_dynamic_ride_overwrites_static_match_and_preserved_pig_image(self):
        w=state(ride=1,learn=1);self.assertEqual(w.execute(),1)
        self.assertEqual((w.i['CHAR_BASEIMAGENUMBER'],w.i['CHAR_BECOMEPIG']),(400,180))
        images=[value for code,actor,value in zip(*[iter(w.trace)]*3) if code==10 and actor==0]
        self.assertEqual(images,[100250,300,400])

    def test_old_image_only_static_match_first_row_and_missing_player_dynamic_branch(self):
        w=state(base=900,old=100,ride=1,learn=1)
        w.execute();self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],300)
        self.assertIn(6,w.trace[::3]);self.assertNotIn(7,w.trace[::3])

    def test_item_transform_and_death_prevent_ride_calls(self):
        for changes in ({'meta':2},{'meta':3},{'dead':1}):
            w=state(ride=1,learn=1,**changes);w.execute()
            self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],100250)
            self.assertNotIn(5,w.trace[::3])

    def test_bismarck_default_rider_preservation_and_belt_differences(self):
        w=state('bismarck',ride=1,learn=1,pig=-1);w.execute()
        self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],100250);self.assertNotIn(5,w.trace[::3])
        for belt,want in ((0,101),(1,100250)):
            w=state('bismarck',pig=-1,belt=belt,category=1);w.execute()
            self.assertEqual(w.i['CHAR_BASEIMAGENUMBER'],want)

    def test_no_match_dismounts_and_source_zero_row_can_match_in_active_profile(self):
        w=state(base=900,pbase=901,ride=1);w.execute()
        self.assertEqual((w.i['CHAR_RIDEPET'],w.i['CHAR_BASEIMAGENUMBER']),(-1,900))
        w=state(base=0,pbase=0,ride=1);w.execute()
        self.assertEqual((w.i['CHAR_RIDEPET'],w.i['CHAR_BASEIMAGENUMBER']),(0,0))

    def test_helper_corpus_excludes_only_reaching_undefined_match_not_belt_bypass(self):
        for profile in ('gavin','bismarck'):
            d=domain(profile);vs=list(helper_vectors(d))
            for v,value in vs:
                if v[0]==0:self.assertEqual(equipment(d,*v[1:]),value)
            self.assertFalse(any(v[0]==0 and v[1]==-1 and v[2]==100 and v[3]==5 for v,_ in vs))
        self.assertTrue(any(v[0]==0 and v[1]==0 and v[2]==100 and v[3]==5 and v[4] for v,_ in helper_vectors(domain('bismarck'))))

    def test_actual_default_profile_receipt_retains_distinct_maps_and_zero_fill(self):
        pins=json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual([pins[n]['maxnoindex'] for n in ('gavin','iris','bismarck')],[12,10,0])
        self.assertEqual([pins[n]['static_zero_filled_rows'] for n in ('gavin','iris','bismarck')],[0,0,192])
        self.assertEqual([pins[n]['tables']['CHAR_eqimagetbl']['rows'] for n in ('gavin','iris','bismarck')],[67,67,76])


if __name__=='__main__':unittest.main()
