"""O23 mutation guards: no originals needed in public CI."""
import copy,json,unittest
from tools.stoneage_o23_three_consumables import REPORT,validate
class O23ConsumableSourceGuards(unittest.TestCase):
    def setUp(self):self.d=json.loads(REPORT.read_bytes())
    def test_actual_derived_source(self):
        self.assertEqual(validate(self.d)["actual_browser_canvas_states"],6)
    def test_source_and_era_mutations(self):
        cases=[
         ("full_current_original_blob",None,"bad"),("evidence_scope",None,"OFFICIAL_SAME_BUILD"),
         ("source_files","original_itemset.txt",{"bytes":0,"sha256":"0"*64,"parsed_item_rows":0}),
         ("actual_private_browser","real_original_pixel_PNG_canvas_states_verified",3),
         ("actual_private_browser","all_six_full_RGBA_equal_independent_Python",False),
         ("actual_private_browser","user_file_open_on_local_machine_verified",True),
         ("actual_private_browser","external_HTTP_requests",1),
         ("private_archive","sha256","0"*64),
         ("private_archive","original_client_binary_text_image_publicly_committed",True),
         ("limits","original_client_world_entered",True),
         ("limits","same_deployed_official_item_master_proven",True),
         ("limits","original_treatment_healing_poison_cure_or_resurrection_executed",True),
         ("limits","runtime_price_or_inventory_change_proven",True),
         ("limits","overall_percent",100),
         ("identity_controls","all_six_original_RD_blocks_actually_read",False)
        ]
        for group,key,val in cases:
            with self.subTest(group=group,key=key):
                item=copy.deepcopy(self.d)
                if key is None:item[group]=val
                else:item[group][key]=val
                with self.assertRaises(ValueError):validate(item)
    def test_item_and_image_mutation_controls(self):
        for rowno in range(3):
            for key,value in [
                ("original_imagenumber",12345),
                ("tw10_unique_alias_target_bitmap",9999),
                ("actual_alias_RD_sha256","0"*64),
                ("alias_candidate_canvas_RGBA_sha256","0"*64),
                ("literal_physical_control_bitmap",999),
                ("original_callback_string","ITEM_fake"),
                ("source_original_name","unproven"),
                ("source_row_sha256","0"*64),
            ]:
                with self.subTest(row=rowno,key=key):
                    item=copy.deepcopy(self.d);item["items"][rowno][key]=value
                    with self.assertRaises(ValueError):validate(item)
if __name__=="__main__":unittest.main()
