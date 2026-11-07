"""Quarry narrative controls: source redirection, old variant and conflicting item."""
import hashlib
import json
import unittest
from tools.stoneage_quest10_quarry_spirits_source import ROOT,REPORT,SOURCE,source_events


class QuarrySource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(REPORT.read_text())

    def test_original_members_and_seven_creates(self):
        d=self.data;old=json.loads(SOURCE.read_text());manifest={r[0]:r for r in old['source_files']}
        self.assertEqual(d['verified_original_NPC_members'],2205)
        self.assertEqual(len(d['source_files']),12)
        for r in d['source_files']:
            self.assertEqual([r['bytes'],r['sha256'],r['crc32']],manifest[r['path']][1:4])
        originals=[r for r in old['create_rows'] if r[0]=='giiru/event/event30.create']
        self.assertEqual(len(d['source_creates']),7)
        for x,y in zip(d['source_creates'],originals):
            self.assertEqual([x['file'],x['ordinal'],x['start_byte'],x['end_byte'],x['block_sha256'],x['floor'],x['graphic_alias'],x['borncorner_raw']],y[:8])
            self.assertEqual(x['parameter_references'],y[15])
            self.assertEqual(x['template_bindings'],y[13])

    def test_current_Kui_reference_is_not_the_unreferenced_old_script(self):
        creates=self.data['source_creates'];kui=creates[4]
        self.assertEqual((kui['floor'],kui['borncorner_raw']),(30600,[15,10,15,10]))
        self.assertEqual(kui['parameter_references'][0][0],'king/event69_1')
        refs={ref[0] for c in creates for ref in c['parameter_references']}
        self.assertNotIn('giiru/event/event30_5',refs)
        self.assertNotIn('giiru/event/event30_5.old',refs)
        scripts={s['path']:s for s in self.data['source_event_scripts']}
        current=scripts['giiru/event/event30_5']['events'][1]
        older=scripts['giiru/event/event30_5.old']['events'][1]
        self.assertEqual(current['event'],'ENDEV=29&NOWEV=54&ITEM=2532')
        self.assertEqual(older['event'],'ENDEV=30&ENDEV=54&ITEM=2532')
        self.assertEqual(current['other_numeric_controls'],[{'name':'EndSetFlg','value':54}])
        self.assertEqual(older['other_numeric_controls'],[])
        reward=scripts['king/event69_1']['events'][2]
        self.assertEqual(reward['event'],'ENDEV=4&ENDEV=29&ENDEV=30&NOWEV=54&ITEM=2547')
        self.assertEqual(reward['other_numeric_controls'],[{'name':'GetPet','value':355},{'name':'EndSetFlg','value':54}])

    def test_literal_conditions_missing_separator_and_Charm_preserved(self):
        scripts=self.data['source_event_scripts']
        self.assertEqual([len(s['events']) for s in scripts],[8,5,6,3,6,2,6,8])
        self.assertEqual(scripts[0]['events'][2]['event'],'LV>79&ENDEV=4ENDEV=29&ENDEV=30&ITEM=2392')
        transfer=scripts[0]['events'][1]
        self.assertEqual([(x['name'],x['item_id'],x['explicit_quantity']) for x in transfer['commands']],
                         [('DelItem',2391,1),('GetItem',2392,1)])
        end=scripts[5]['events'][1]
        self.assertEqual(end['other_numeric_controls'],[{'name':'EndSetFlg','value':29},{'name':'Charm','value':1}])
        self.assertEqual(end['commands'][0]['item_id'],2551)
        self.assertIsNone(end['commands'][0]['explicit_quantity'])
        self.assertEqual(self.data['source_warp_controls'],[{'name':'FREE','raw':'LV>0'},
            {'name':'WARP','raw':'31910,10,14'},{'name':'FREE','raw':'ENDEV=4&NOWEV=29&ENDEV=30&NOWEV=54&ITEM=2548'}])

    def test_item_2391_conflict_and_complete_original_row_identities(self):
        items={r['item_id']:r for r in self.data['source_item_evidence']}
        self.assertEqual(len(items),11)
        self.assertEqual(sum(len(r['source_row_reconstructions']) for r in items.values()),21)
        self.assertEqual(items[2391]['source_name_sha256'],hashlib.sha256('三墀蛇牙'.encode()).hexdigest())
        self.assertIsNone(items[2391]['source_item01_numeric_row'][1])
        self.assertFalse(items[2391]['qualified_icon_present'])
        for item in items.values():
            for row in item['source_row_reconstructions']:
                column=1 if row['table']=='itemset.txt' else 2
                self.assertEqual(row['sha256'],item['source_item01_numeric_row'][column])
        self.assertEqual(items[2532]['source_image_alias'],items[2547]['source_image_alias'])
        self.assertEqual([items[k]['source_item01_numeric_row'][5] for k in [2532,2547]],['0','50000'])
        self.assertNotEqual(items[2532]['source_item01_numeric_row'][1],items[2547]['source_item01_numeric_row'][1])
        self.assertEqual(sum(r['qualified_icon_present'] for r in items.values()),9)

    def test_source_positions_and_prior_map_identity(self):
        prior=json.loads((ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text())
        maps=self.data['source_map_observations']
        self.assertEqual([r['floor'] for r in maps],[5005,5106,30600,31902,31909,31910,31911])
        self.assertEqual(sum(len(r['source_points']) for r in maps),8)
        creates={r['ordinal']:r for r in self.data['source_creates']}
        for row in maps:
            self.assertEqual(row['source_DAT_sha256'],prior['maps'][str(row['floor'])]['source_sha256'])
            for point in row['source_points']:
                key=point['source_create_ordinal_or_target']
                if key=='WARP_TARGET':self.assertEqual((row['floor'],point['xy']),(31910,[10,14]))
                else:self.assertEqual((row['floor'],point['xy']),(creates[key]['floor'],creates[key]['borncorner_raw'][:2]))
                self.assertEqual(len(point['original_three_u16_values']),3)

    def test_preserved_dependencies_and_no_duplicate_or_runtime_promotion(self):
        self.assertTrue(self.data['prior_delivery_NEXT_was_already_completed_by_O24_O32'])
        for path,expected in self.data['derived_input_blobs'].items():
            raw=(ROOT/path).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),expected)
        self.assertEqual(self.data['origin_class'],'ORIGIN_UNRESOLVED')
        self.assertTrue(all(v is False for v in self.data['boundaries'].values()))
        self.assertIsNone(self.data['status']['overall_percent'])
        raw=b'EventNo:54\nTYPE:ACCEPT\nEVENT:ITEM=1\nGetPet:355\nCharm:1\nEndSetFlg:54\nEventEnd\n'
        self.assertEqual(source_events(raw)[0]['other_numeric_controls'],[{'name':'GetPet','value':355},{'name':'Charm','value':1},{'name':'EndSetFlg','value':54}])


if __name__=='__main__':unittest.main()
