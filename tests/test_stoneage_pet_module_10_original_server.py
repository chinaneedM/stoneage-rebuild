"""PET10 public derived-record replay. Does not read/provide copyrighted source data.
The original RAR was separately read in private local environment, checking 8 full-file hashes and RAR CRCs.
"""
import json, unittest, copy, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
SOURCE=ROOT/"STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"
def certify(x):
    assert x['schema']=='stoneage.pet10_original_mixed25_rar_same_archive_full_server_material_qualified.r1'
    assert x['preserved_original_rar']['bytes']==361255180
    assert x['preserved_original_rar']['sha256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
    assert x['original_spreadsheet_proprietary_names_and_row_bytes_published'] is False
    assert all(v is False for k,v in x['negative_evidence'].items() if k!='overall_restoration_percent')
    assert x['negative_evidence']['overall_restoration_percent'] is None
    files=x['verified_original_archive_members'];rows=x['source_rows'];s=x['table_summaries']
    assert len(files)==8
    assert files['enemybase.txt']['sha256']=='1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7'
    assert files['enemybase2.txt']['sha256']=='8ecb23231ae1aeb21fe943c7b459f0c0d10ef3599aedfeaeccca783b077f5fd4'
    assert files['spradrn_5.bin']['sha256']=='5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6'
    expected={'enemybase.txt':988,'enemybase2.txt':640,'enemy.txt':2087,'enemy2.txt':1494,'petskill.txt':147,'petskill1.txt':56,'spradrn_5.bin':847}
    for name,n in expected.items():
        assert len(rows[name])==n
        assert len({r[0] for r in rows[name]})==n
    assert files['enemybase.txt']['physical_lines']==995
    assert files['enemybase.txt']['blank_physical_lines']==[960,965,971,976,982,987,991]
    assert files['enemybase2.txt']['physical_lines']==640
    a=rows['enemybase.txt'];b=rows['enemybase2.txt'];spr=rows['spradrn_5.bin'];spr_keys={r[1] for r in spr}
    assert len(spr_keys)==841
    assert {r[1] for r in a}=={r[1] for r in a}|set()
    assert len({r[1] for r in a})==988
    assert len({r[1] for r in b})==640
    assert all(r[0]==i+1 and len(r)==17 and len(r[15])==7 and len(r[-1])==64 for i,r in enumerate(a))
    assert all(r[0]==i+1 and len(r)==17 and len(r[15])==7 and len(r[-1])==64 for i,r in enumerate(b))
    for filename,table,target_defs,totals in (
        ('enemybase.txt',a,rows['petskill.txt'],(495,493,424,234,302,1050,1050,0,15,2400)),
        ('enemybase2.txt',b,rows['petskill1.txt'],(316,324,291,227,252,661,649,12,11,1539))):
        pets=[r for r in table if r[3]==1];non=[r for r in table if r[3]==0]
        keys={r[2] for r in pets}
        defined={r[1] for r in target_defs}
        positive=[v for r in pets for v in r[15] if v is not None and v>0]
        neg=[v for r in pets for v in r[15] if v is not None and v<0]
        nulls=sum(v is None for r in pets for v in r[15])
        got=(len(pets),len(non),len(keys),len(keys&spr_keys),sum(r[2] in spr_keys for r in pets),len(positive),sum(v in defined for v in positive),sum(v not in defined for v in positive),len(neg),nulls)
        assert got==totals,(filename,got)
        assert s[filename]['flag_counts']=={'0':len(non),'1':len(pets)}
        assert s[filename]['PETFLG1_skill_slot_counts']['skill_positive_defined']==got[6]
        assert s[filename]['PETFLG1_skill_slot_counts']['skill_positive_missing']==got[7]
    for instfile,base in (('enemy.txt',a),('enemy2.txt',b)):
        valid={r[1] for r in base};actual=rows[instfile]
        assert len({r[1] for r in actual})==len(actual)
        assert all(r[3]==1 and r[2] in valid for r in actual)
        assert s[instfile]['matched_to_paired_template_id']==len(actual)
        assert s[instfile]['unmatched_to_paired_template_id']==0
    aids={r[1]:r for r in a};bids={r[1]:r for r in b};common=set(aids)&set(bids)
    assert len(common)==640
    assert x['source_relationship_scope']['base_pair_shared_template_ids']==640
    assert x['source_relationship_scope']['exact_56_fields_equal_in_common_ids']==365
    assert x['source_relationship_scope']['common_ids_with_any_field_difference']==275
    assert x['source_relationship_scope']['same_original_rar_member_paths_not_deployed_same_time'] is True
    return True
class PET10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.doc=json.loads(SOURCE.read_text(encoding='utf-8'))
    def test_replay_full_derived_source(self): self.assertTrue(certify(self.doc))
    def test_no_fake_clean_version(self):
        x=copy.deepcopy(self.doc);x['negative_evidence']['official_version_2_5_clean_release_proven']=True
        with self.assertRaises(AssertionError):certify(x)
    def test_no_fake_missing_skill_definition(self):
        x=copy.deepcopy(self.doc);x['source_rows']['petskill1.txt'][1][1]=99999
        with self.assertRaises(AssertionError):certify(x)
    def test_no_deleted_original_988_row(self):
        x=copy.deepcopy(self.doc);x['source_rows']['enemybase.txt'].pop()
        with self.assertRaises(AssertionError):certify(x)
    def test_no_graphic_number_as_species(self):
        x=copy.deepcopy(self.doc);x['negative_evidence']['original_species_count_verified']=True
        with self.assertRaises(AssertionError):certify(x)
if __name__=='__main__':unittest.main()