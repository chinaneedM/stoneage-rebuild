"""O24 strict mutation guards for original mixed25 two-town event evidence."""
import unittest,copy,json
from tools.stoneage_o24_two_town_event import REPORT,validate
class O24OriginalEventGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=json.loads(REPORT.read_text(encoding="utf-8"))
    def test_pinned_static_source(self):
        self.assertEqual(validate(self.data),{"actors":2,"original_event_branches":6,"item_source_rows":2,"source_paths":6})
    def test_source_identity_and_provenance_mutations(self):
        for group,key,bad in [
            ("baseline","current_state_blob","0"*40),("original_archive","sha256","0"*64),
            ("scene21_private_zip","crc_verified",False),("source_files",None,None)
        ]:
            with self.subTest(group=group,key=key):
                d=copy.deepcopy(self.data)
                if group=="source_files":d["source_files"][5]["verification"]="RAR_DIRECT_SHA_CRC"
                else:d[group][key]=bad
                with self.assertRaises(ValueError):validate(d)
    def test_actor_item_map_and_event_mutations(self):
        for kind in ("floor","xy","graphicname","script","name","cell","item_id","image_id","branch_event","branch_get","branch_sha","branch_predicate"):
            with self.subTest(kind=kind):
                d=copy.deepcopy(self.data)
                if kind=="floor":d["actors"][0]["floor"]=1000
                if kind=="xy":d["actors"][0]["xy"]=[155,92]
                if kind=="graphicname":d["actors"][0]["graphicname"]=16030
                if kind=="script":d["actors"][0]["script"]="event02_2"
                if kind=="name":d["actors"][1]["name"]="unknown"
                if kind=="cell":d["actors"][1]["raw_cell_u16"]=[373,0,0]
                if kind=="item_id":d["items"][0]["id"]=2415
                if kind=="image_id":d["items"][1]["image_number"]=24130
                if kind=="branch_event":d["event_branches"]["event02_1"][1][0]=3
                if kind=="branch_get":d["event_branches"]["event02_2"][1][3]=2414
                if kind=="branch_sha":d["event_branches"]["event02_2"][0][7]="0"*64
                if kind=="branch_predicate":d["event_branches"]["event02_1"][2][2]="LV>0"
                with self.assertRaises(ValueError):validate(d)
    def test_nonpromotion_guards(self):
        keys=["all_six_original_source_members_validated_in_one_library_archive",
              "tw10_same_deployed_build","jss1999_identity","original_client_world_entered",
              "original_server_script_executed","original_item_grant_or_removal_executed",
              "original_graphic_frames_rendered_this_unit","raw_plane_3_game_semantics_confirmed",
              "source_event_is_limited_time_activity"]
        for k in keys:
            with self.subTest(key=k):
                d=copy.deepcopy(self.data);d["read_limits"][k]=True
                with self.assertRaises(ValueError):validate(d)
        d=copy.deepcopy(self.data);d["read_limits"]["overall_completion_percent"]=1
        with self.assertRaises(ValueError):validate(d)
if __name__=="__main__":unittest.main()
