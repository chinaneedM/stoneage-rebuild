import copy
import json
import unittest
from tools import stoneage_tw10_palette_guard as guard


class PaletteSourceGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pointer=json.loads(guard.POINTER.read_bytes())
        cls.source=json.loads(guard.SOURCE.read_bytes())
        cls.old=json.loads((guard.DIRECTORY/'STONEAGE-TW10-ANIMATION-OBSERVATION-P2A-ACTUAL-SOURCE-R1.json').read_bytes())

    def test_actual_source_and_independent_initializer(self):
        self.assertTrue(guard.validate(self.pointer,self.source,self.old))

    def test_original_pivots_and_reserved_constants_mutations(self):
        for change in ('blue','slot','constant'):
            p=copy.deepcopy(self.pointer)
            if change=='slot':p['static_literal_pointer_slots'][0]['slot_rva']+=4
            else:
                w=next(w for w in p['windows'] if w['start_rva']==0x96c0)
                i=next(i for i in w['instructions'] if i['rva']==(0x99f5 if change=='blue' else 0x96c6))
                i['operands']='byte ptr [esi], al' if change=='blue' else 'al, 0xc1'
            with self.subTest(change=change),self.assertRaises(ValueError):guard.validate(p,self.source,self.old)

    def test_native_rgb_budget_cache_and_effect_promotions(self):
        for change in ('rgb','reads','cache','scene','com'):
            s=copy.deepcopy(self.source)
            if change=='rgb':s['original_actual_palette']['rgb_sha256']='0'*64
            elif change=='reads':s['original_actual_palette']['reads']=708
            elif change=='cache':s['synthetic_cached_state_with_original_code']['reads']=672
            elif change=='scene':s['actual_scene_palette_selection_proven']=True
            else:s['original_actual_palette']['original_com_palette_creation_executed']=True
            with self.subTest(change=change),self.assertRaises(ValueError):guard.validate(self.pointer,s,self.old)

    def test_color_export_must_retain_same_original_indexed_pixels(self):
        for field in ('palette_index_sha256','rd_block_sha256','bitmapno'):
            s=copy.deepcopy(self.source);w=s['color_animation_previews'][0]['bitmap_witnesses'][0]
            w[field]=99999 if field=='bitmapno' else '0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):guard.validate(self.pointer,s,self.old)


if __name__=='__main__':unittest.main()
