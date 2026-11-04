"""Stage A original RAR block-read receipt: metadata-only CI; never treat CRC-failed bytes as source."""
import json,unittest
from pathlib import Path
from copy import deepcopy

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-STAGE-A-ORIGINAL-RAR-BLOCK-REPLAY-CN182-PROVENANCE-R1.json"
MAP01=ROOT/"research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json"
GAP=ROOT/"research/recovered/STONEAGE-STAGE-A-ORIGINAL-DAT-AND-SAME-BUILD-SOURCE-GAP-R1.json"

def validate(r,m,g):
    assert r["schema"]=="stoneage.stage_a_original_private_mixed25_RAR_direct_block_read_and_CN182_provenance.r1"
    assert r["source_git_blobs"]=={
        "map01":"03675ee98d391f9ef0246315b2426f2a8b721fd3",
        "prior_gap":"cf661b5eb7d438ed7ce6c1de6b7e07f4b14ffa92",
        "current_historical_state_unmodified":"c89e0e33537990aa2132b47c40fef49a985a935c"}
    a=r["source_original_private_archive"]
    assert a["original_RAR_bytes"]==m["original_rar_bytes"]==361255180
    assert a["original_RAR_SHA256"]==m["original_rar_sha256"]
    assert a["archive_member_headers_parsed"]==m["full_rar_header_entries_seen"]==7952
    assert a["re_read_this_unit"] is True and a["full_archive_SHA_verified_this_unit"] is True
    assert r["methods"]["independent_decompressor_successfully_executed"] is False
    entries=r["results"]
    assert len(entries)==8
    assert len(set((x["source_group"],x["member_basename"]) for x in entries))==8
    assert all(x["full_declared_length_emitted"]==(x["original_RAR_header_uncompressed_bytes"]==x["direct_block_API_decoded_bytes"]) for x in entries)
    assert all(x["full_member_CRC_verified"]==(x["full_declared_length_emitted"] and x["original_RAR_header_uncompressed_CRC32"]==x["direct_block_API_decoded_CRC32"] and not x["direct_block_API_terminal_error"]) for x in entries)
    assert all(x["source_qualified_original_DAT"]==(x["full_member_CRC_verified"] and x["member_basename"].lower().endswith(".dat")) for x in entries)
    find=lambda n,area="CLIENT_MAIN_SA25":next(x for x in entries if x["member_basename"].lower()==n.lower() and x["source_group"]==area)
    ctl=find("2000.DAT")
    qualified=next(x for x in m["original_decoded_source_rows"] if x[0]==0 and x[1].lower()=="2000.dat")
    assert ctl["full_member_CRC_verified"] is True
    assert ctl["direct_block_API_decoded_bytes"]==qualified[2]
    assert ctl["direct_block_API_decoded_SHA256"]==qualified[3]
    assert ctl["direct_block_API_decoded_CRC32"]==qualified[4]
    assert ctl["decoded_first_two_u32"]==[150,150]
    mp0=find("3021.MAP")
    mp1=find("3021.MAP","ADDON_SACH_MX_0_30")
    assert mp0["direct_block_API_decoded_SHA256"]==mp1["direct_block_API_decoded_SHA256"]=="57a230c56ab77c418101e296480f7a04ce653e0aaf0512e15050e22b335ab789"
    assert mp0["full_member_CRC_verified"] is True and mp1["full_member_CRC_verified"] is True
    assert mp0["decoded_first_two_u32"]==mp1["decoded_first_two_u32"]==[407,144]
    x=find("3021.DAT")
    assert x["original_RAR_header_uncompressed_bytes"]==351656
    assert x["direct_block_API_decoded_bytes"]==351656
    assert x["decoded_first_two_u32"]==[0,0]
    assert x["original_RAR_header_uncompressed_CRC32"]=="c0d8a645"
    assert x["direct_block_API_decoded_CRC32"]=="0eb2e1fd"
    assert x["full_member_CRC_verified"] is False and x["source_qualified_original_DAT"] is False
    assert x["direct_block_API_terminal_error"]=="File CRC error"
    assert r["critical_verification"]["source_3021_DAT_candidate_member_crc_matched"] is False
    assert r["critical_verification"]["source_3021_DAT_candidate_first8_dimensions"]==x["decoded_first_two_u32"]
    for n in ("100.DAT","200.dat","3000.dat","3021.DAT"):
        y=find(n)
        assert y["full_member_CRC_verified"] is False and y["source_qualified_original_DAT"] is False
        prior=next(z for z in g["priority_qualified_floor_gaps"] if z["floor_id"]==int(n.split(".")[0]))
        assert prior["source_archived_member_presence"]["group0_client_DAT_verified"]==[]
        assert prior["source_archived_member_presence"]["group0_client_DAT_read_failures"][0]["expected_member_bytes"]==y["original_RAR_header_uncompressed_bytes"]
    assert find("100.DAT")["direct_block_API_decoded_bytes"]==162560
    assert find("200.dat")["direct_block_API_decoded_bytes"]==2457600
    assert find("3000.dat")["full_declared_length_emitted"] is True
    assert find("3000.dat")["original_RAR_header_uncompressed_CRC32"]!=find("3000.dat")["direct_block_API_decoded_CRC32"]
    assert find("1000.DAT")["full_declared_length_emitted"] is True
    assert find("1000.DAT")["full_member_CRC_verified"] is False
    assert r["critical_verification"]["recovered_four_DATs_now_qualified_count"]==0
    assert r["critical_verification"]["stage_A_nine_family_counts"]=={"PARTIAL":7,"OPEN":2}
    assert r["critical_verification"]["historical_2001_CN182_same_server_execution_proven"] is False
    assert r["historical_2003_Mainland_182_service"]["initial_mainland_2001_182_claim"] is False
    assert len(r["historical_2003_Mainland_182_service"]["source_publications"])==4
    assert r["critical_verification"]["stage_B_started"] is False
    assert r["critical_verification"]["overall_percent"] is None
    assert all(v is True for v in r["bounds"].values())

class OriginalRarBlockReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf8"))
        cls.m=json.loads(MAP01.read_text(encoding="utf8"))
        cls.g=json.loads(GAP.read_text(encoding="utf8"))
    def runcheck(self,r):validate(r,self.m,self.g)
    def test_exact_public_metadata_replay(self):self.runcheck(self.r)
    def test_guard_no_full_length_promotion(self):
        r=deepcopy(self.r)
        next(x for x in r["results"] if x["member_basename"]=="3021.DAT")["source_qualified_original_DAT"]=True
        with self.assertRaises(AssertionError):self.runcheck(r)
    def test_guard_no_3000_false_CRC_pass(self):
        r=deepcopy(self.r)
        next(x for x in r["results"] if x["member_basename"]=="3000.dat")["full_member_CRC_verified"]=True
        with self.assertRaises(AssertionError):self.runcheck(r)
    def test_guard_dont_invent_2001_policy(self):
        r=deepcopy(self.r)
        r["historical_2003_Mainland_182_service"]["initial_mainland_2001_182_claim"]=True
        with self.assertRaises(AssertionError):self.runcheck(r)
    def test_guard_dont_rewrite_original_archive_SHA(self):
        r=deepcopy(self.r)
        r["source_original_private_archive"]["original_RAR_SHA256"]="0"*64
        with self.assertRaises(AssertionError):self.runcheck(r)
    def test_guard_dont_erase_existing_3021_failure(self):
        r=deepcopy(self.r)
        r["critical_verification"]["recovered_four_DATs_now_qualified_count"]=1
        with self.assertRaises(AssertionError):self.runcheck(r)

if __name__=="__main__":unittest.main()
