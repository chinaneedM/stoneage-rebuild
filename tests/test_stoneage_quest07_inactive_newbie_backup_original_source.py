"""QUEST07: source-bounded dormant newbie.create.bak, actual 9 DAT and 5 candidate scenes."""
from collections import Counter
from copy import deepcopy
import hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-QUEST07-INACTIVE-NEWBIE-BACKUP-26-CREATE-NINE-ORIGINAL-DAT-R1.json"
MAP=ROOT/"research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json"
SHA=lambda s: bool(re.fullmatch(r"[0-9a-f]{64}",s))
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def verify(a,m):
    assert a["schema"]=="stoneage.quest07.later_community_mixed25_newbie_backup_inactive_source_and_nine_original_DAT.r1"
    assert a["source_scope"]=="LATER_COMMUNITY_MIXED25_ORIGINAL_CREATE_BACKUP_NOT_VERIFIED_ACTIVE_OFFICIAL_GAME_OR_EARLY_ORIGIN"
    assert a["original_RAR"]=={"bytes":361255180,"sha256":"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5","member_count":7952}
    a1=a["source_original_CREATE_files"]
    assert a1["backup"]["sha256"]=="fa83b8f14e355c757a2a27d2173d34941713c14b853886ea4aeff976d431d06d"
    assert a1["active"]["sha256"]=="761dc3d1ed885fb76b22af446331e5a0db6cf3e59a27cf2ab136a62a88d81d0b"
    assert a1["backup"]["original_RAR_member_crc32"]=="1a6f79b2"
    assert a1["active"]["original_RAR_member_crc32"]=="3f411954"
    assert a1["backup"]["bytes"]==6190 and a1["active"]["bytes"]==1548
    assert a1["backup"]["original_block_count"]==34 and a1["active"]["original_block_count"]==8
    shared=a["shared_exact_original_blocks"]
    novel=a["backup_only_original_create_records"]
    assert len(shared)==8 and len(novel)==26 and len({x["source_backup_block_ordinal"] for x in shared} | {x["backup_block_ordinal"] for x in novel})==34
    assert {x["floor"] for x in shared}=={1000,2000,3000,4000,1003,2003,3003,4003}
    maps=a["source_nine_original_DAT_members"];byfloor={x["floor"]:x for x in maps}
    assert len(maps)==len(byfloor)==9
    assert set(byfloor)=={815,816,8018,8019,8020,8021,8022,8023,8024}
    assert a["source_prior_MAP09_archive"]["nested_955_DAT_zip_sha256"]==m["original_DAT_archive"]["sha256"]=="c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a"
    assert a["publication_pins"]=={"main_head":"468b2b7087ec81ab066a9545002254bb74500073","main_tree":"96e6cf86066484200994e949c4c6a848a340ff34","source_current_blob":"c89e0e33537990aa2132b47c40fef49a985a935c","map09_git_blob":"137580e7c25aadf3d679b6ebfb5080b79912cc4f","source_zip_original":"9b6da49d88c9e06f9128bc0b56de967301baaaf2c3a74400881298c4c84d0b77"}
    assert blob(MAP.read_bytes())==a["publication_pins"]["map09_git_blob"]
    v={8018,8019,8020,8022,8023}
    for x in maps:
        w,h=x["geometry"]; assert x["bytes"]==8+6*w*h
        assert x["u16_cells_per_plane"]==w*h
        assert len(x["crc32"])==8 and SHA(x["sha256"])
        assert x["map09_original_955_zip_crc_ok"] is True and x["map09_original_955_zip_sha_match"] is True
        assert x["modern_MAP09_scene_material_previously_qualified"]==(x["floor"] in v)
        if x["floor"] in v:assert m["maps"][str(x["floor"])]["source_sha256"]==x["sha256"]
    refcount=Counter(); func=Counter();floors=Counter()
    for x in novel:
        f=x["original_floorid"];coords=x["original_borncenter"];w,h=byfloor[f]["geometry"]
        assert 0<=coords[0]<w and 0<=coords[1]<h
        assert x["original_map_DAT_full_sha256"]==byfloor[f]["sha256"] and x["source_DAT_geometry"]==[w,h]
        assert len(x["original_three_u16_DAT_values_at_borncenter"])==3
        assert all(0<=n<=65535 for n in x["original_three_u16_DAT_values_at_borncenter"])
        assert SHA(x["source_block_sha256"])
        assert x["source_block_byte_end"]>x["source_block_byte_start"]
        assert x["original_graphicname"] is None or x["original_graphicname"]>=0
        assert x["modern_source_qualified_MAP09_scene_thumbnail_present"]==(f in v)
        assert "private_marked_scene_file" in x if f in v else "private_marked_scene_file" not in x
        func[x["source_template_function"]]+=1;floors[f]+=1
        ref=x["source_argument_reference"]
        if ref:refcount["ref"]+=1;refcount["present" if x["exact_referenced_source_member_present"] else "missing"]+=1
        else:assert x["exact_referenced_source_member_present"] is None
    assert dict(func)==a["counts"]["backup_only_template_function_counts"]
    assert len(floors)==9 and sum(floors.values())==26
    assert (refcount["ref"],refcount["present"],refcount["missing"])==(24,1,23)
    assert sum(floors[f] for f in v)==9
    c=a["counts"]
    assert [c[k] for k in ("backup_original_block_count","active_original_block_count","shared_canonical_exact_blocks","backup_only_CREATE_blocks","backup_only_distinct_floors","original_DAT_full_bytes_recovered_for_backup_only_floors","backup_only_original_coords_in_DAT_geometry","backup_only_argument_ref_count","backup_only_argument_ref_present","backup_only_argument_ref_missing","backup_only_original_source_MAP09_visible_floor_count","backup_only_original_CREATE_refs_on_previously_qualified_visual_floors","backup_only_DAT_non_MAP09_visual_floor_count")]==[34,8,8,26,9,9,26,24,1,23,5,9,4]
    assert a["private_images"]["marked_thumbnail_floor_ids"]==sorted(v)
    assert a["private_images"]["contact_sha256"]=="76b9e763da7fb72e457aa9ee0347046aa215f4f9730b643ded7480983de7962c"
    q=a["private_custody_verified"];assert q["zip_sha256"]=="9b6da49d88c9e06f9128bc0b56de967301baaaf2c3a74400881298c4c84d0b77"
    assert q["zip_member_count"]==18 and q["zip_bytes"]==220401
    assert all(q[k] for k in ("zip_CRC_all_passed","zip_Library_roundtrip_SHA_verified","contact_Library_roundtrip_SHA_verified","private_derived_report_Library_roundtrip_SHA_verified"))
    assert q["private_derived_report_sha256"]=="786e9a498f3019933f6f4da5b03b8aab8515843198a2fe45edb01d1f0385e666"
    assert all(x is False for x in a["boundaries"].values())
    assert a["status"]=={"stage_A":"7_PARTIAL_2_OPEN","stage_B_wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None}
class OriginalBackup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))
        cls.map=json.loads(MAP.read_text(encoding="utf-8"))
    def test_complete_derived_contract(self):verify(self.data,self.map)
    def reject(self,fn):
        d=deepcopy(self.data);fn(d)
        with self.assertRaises((AssertionError,KeyError,TypeError)):verify(d,self.map)
    def test_reject_forged_original_DAT(self):
        self.reject(lambda d:d["source_nine_original_DAT_members"][0].__setitem__("sha256","0"*64))
    def test_reject_wrong_actor_coordinate(self):
        self.reject(lambda d:d["backup_only_original_create_records"][0].__setitem__("original_borncenter",[999,999]))
    def test_reject_unearned_live_status(self):
        self.reject(lambda d:d["boundaries"].__setitem__("backup_is_verified_activated_source",True))
    def test_reject_fake_resolved_script(self):
        self.reject(lambda d:d["counts"].__setitem__("backup_only_argument_ref_missing",0))
    def test_reject_fake_visible_map(self):
        self.reject(lambda d:d["source_nine_original_DAT_members"][0].__setitem__("modern_MAP09_scene_material_previously_qualified",True))
    def test_reject_original_client_execution(self):
        self.reject(lambda d:d["boundaries"].__setitem__("original_quest_ran_natively",True))
if __name__=="__main__":unittest.main()
