import copy
import io
import json
import unittest
from tools import stoneage_cn20_named_pet_visual_r104 as m
D=json.loads(m.SOURCE.read_text())
OLD=json.loads((m.ROOT/m.PARENT).read_text())

def fixture():
    text='<title>石器时代2.0</title>新 增 宠 物<table><tr><td><a href="new_pet.asp">1-40</a> <a href="new_pet1.asp">41-80</a> 81-104</td></tr></table><table>'
    for i,r in enumerate(OLD['records'][80:]):
        if i%5==0:text+='<tr>'
        im=r['image_reference'];dims=im['html_declared_dimensions'];attrs='' if dims is None else f' width="{dims[0]}" height="{dims[1]}"'
        text+='<td><img src="'+im['relative_src_as_written']+'"'+attrs+'>'+r['name_as_written']+'</td>'
        if i%5==4:text+='</tr>'
    return (text+'</table><span class="p12b">footer</span>').encode('gb18030')

class NamedPixelSupplements(unittest.TestCase):
    def test_valid_contract_and_original_parent_states(self):
        m.validate(D)
        self.assertEqual([r['name_as_written'] for r in D['records']],['裘里蛙','沙瓦列','砂鲨'])
        for r in D['records']:
            self.assertIsNone(r['game_ids'])
            self.assertFalse(r['same_instant_as_page_proven'])
            self.assertFalse(r['original_sprite_or_animation_verified'])
        self.assertTrue(all(OLD['records'][n-1]['image_reference']['pixels_requested'] is False for n in m.POSITIONS))

    def test_synthetic_metadata_grid_preserves_literal_cell_bindings(self):
        got=m.extract(fixture(),D,verify_page_bytes=False)
        self.assertEqual(got,D['selected_cells'])
        self.assertEqual([(r['ordinal'],r['relative_src_as_written']) for r in got],[(84,'img/newpet/104.JPG'),(88,'img/newpet/88.JPG'),(89,'img/newpet/87.JPG')])
        self.assertIsNone(got[1]['html_declared_dimensions'])

    def test_name_image_swap_case_or_normalized_filename_rejected(self):
        text=fixture().decode('gb18030')
        for old,new in [('104.JPG','84.JPG'),('87.JPG','89.JPG'),('88.JPG','87.JPG'),('104.JPG','104.jpg'),('裘里蛙','裘里娃'),('沙瓦列','砂鲨')]:
            with self.subTest(old=old),self.assertRaises(ValueError):m.extract(text.replace(old,new).encode('gb18030'),D,verify_page_bytes=False)

    def test_missing_row_or_added_blank_cell_is_not_invented(self):
        text=fixture().decode('gb18030')
        for modified in [text.replace('</table><span','<td>invented</td></table><span'),text.replace('81-104','81-105'),text.replace('</table><table><tr>','</table><table>',1)]:
            with self.assertRaises(ValueError):m.extract(modified.encode('gb18030'),D,verify_page_bytes=False)

    def test_archived_byte_pin_is_independent_of_semantic_grid(self):
        with self.assertRaisesRegex(ValueError,'Exact archived page'):m.extract(fixture(),D)
        self.assertEqual(m.extract(fixture()+b'<script>outer</script>',D,False),D['selected_cells'])

    def test_separate_capture_cannot_become_same_time_native_identity(self):
        for field in ['same_instant_or_exact_build_proven','web_ordinal_or_filename_is_game_id','original_sprite_animation_or_server_stats_recovered','asset_reuse_approved']:
            changed=copy.deepcopy(D);changed['boundaries'][field]=True
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'contract'):m.validate(changed)
        changed=copy.deepcopy(D);changed['images'][0]['capture']=D['page']['capture']
        with self.assertRaises(ValueError):m.validate(changed)

    def test_image_identity_and_decoding(self):
        from PIL import Image
        data=io.BytesIO();Image.new('RGB',(3,2)).save(data,'JPEG');raw=data.getvalue()
        expected={'bytes':len(raw),'sha256':m.sha(raw),'decoded':{'format':'JPEG','mode':'RGB','size':[3,2],'frames':1}}
        self.assertEqual(m.image_metadata(raw,expected)['size'],[3,2])
        with self.assertRaisesRegex(ValueError,'bytes'):m.image_metadata(raw+b'x',expected)
        expected['decoded']['size']=[2,3]
        with self.assertRaisesRegex(ValueError,'decoding'):m.image_metadata(raw,expected)

    def test_swapped_pixels_and_banner_name_join_cannot_be_accepted(self):
        changed=copy.deepcopy(D);changed['images'][0],changed['images'][1]=changed['images'][1],changed['images'][0]
        with self.assertRaises(ValueError):m.validate(changed)
        changed=copy.deepcopy(D);changed['discarded_probe']['named_species_pixel_join_accepted']=True
        with self.assertRaises(ValueError):m.validate(changed)

if __name__=='__main__':unittest.main()
