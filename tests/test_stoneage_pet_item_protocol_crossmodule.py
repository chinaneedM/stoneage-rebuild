"""Negative controls: source-only optional protocol callback cannot imply runtime."""
import hashlib
import unittest
from tools.stoneage_pet_item_protocol_crossmodule_audit import ORIGINAL,validate_report
SITES=[
 ("GmsvServer_PETITEM_recv","common/gmsv_server_recv.c",985,1),
 ("CHAR_movePetItem","common/gmsv_server_recv.c",1010,0),
 ("CHAR_movePetItem","gmsv/char/char_item.c",2655,1),
]

def rows():
    h=hashlib.sha256()
    for s in SITES:h.update(("|".join(map(str,s))+"\n").encode())
    d=dict(profile="bismarck",handler_blob=ORIGINAL["handler"],common_make_blob=ORIGINAL["common_make"],
           equipment_blob=ORIGINAL["equipment"],gmsv_subtree_direct_callers=0,
           whole_server_pet_equip_definitions=1,whole_server_pet_equip_direct_callers=1,
           protocol_recv_definitions=1,default_protocol_compiled=0,default_equipment_compiled=0,
           forced_protocol_compiled=1,forced_equipment_compiled=1,default_MI_recv_present=1,
           caller_under_positive_macro=1,known_compiled_production_binary=0,
           natural_pet_item_path_proven=0,early_original_build_proven=0,site_sha256=h.hexdigest())
    return ["SOURCE_PET_PROTOCOL_GATE|"+"|".join(f"{k}={v}" for k,v in d.items()),
            *[f"SOURCE_PET_PROTOCOL_SITE|symbol={x}|path={path}|line={line}|definition={df}" for x,path,line,df in SITES],
            "RESOLUTION|PET_PROTOCOL_CROSS_MODULE_SOURCE_ONLY_PASS"]

class CrossModuleEvidence(unittest.TestCase):
    def test_full_chain(self):
        summary,sites=validate_report("\n".join(rows()))
        self.assertEqual(len(sites),3)
        self.assertEqual(summary["whole_server_pet_equip_direct_callers"],"1")
    def test_no_missing_or_duplicate_lines(self):
        raw=rows()
        for i in range(len(raw)):
            with self.subTest(i=i),self.assertRaises(ValueError):
                validate_report("\n".join(raw[:i]+raw[i+1:]))
        with self.assertRaises(ValueError):validate_report("\n".join(raw+[raw[1]]))
    def test_checked_in_default_must_remain_disabled(self):
        fields=["default_protocol_compiled","default_equipment_compiled",
                "known_compiled_production_binary","natural_pet_item_path_proven",
                "early_original_build_proven","gmsv_subtree_direct_callers"]
        for k in fields:
            raw=rows()
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_report("\n".join(x.replace(k+"=0",k+"=1") for x in raw))
    def test_nondefault_feature_requires_explicit_forced_macro(self):
        for k in ("forced_protocol_compiled","forced_equipment_compiled",
                  "caller_under_positive_macro","default_MI_recv_present"):
            raw=rows()
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_report("\n".join(x.replace(k+"=1",k+"=0") for x in raw))
    def test_original_cross_library_caller_cannot_be_omitted(self):
        raw=rows()
        for old,new in (("whole_server_pet_equip_direct_callers=1","whole_server_pet_equip_direct_callers=0"),
                        ("common/gmsv_server_recv.c","gmsv/net/net.c"),
                        ("line=1010","line=1111"),
                        ("definition=0","definition=1")):
            with self.subTest(old=old),self.assertRaises(ValueError):
                validate_report("\n".join(x.replace(old,new) for x in raw))
    def test_bad_original_sha_or_forged_extra_field(self):
        raw=rows()
        for alt in (raw[0].replace(ORIGINAL["handler"],"a"*40),raw[0]+"|extra=1",
                    raw[0]+"|profile=bismarck"):
            with self.assertRaises(ValueError):
                validate_report("\n".join([alt]+raw[1:]))
    def test_missing_resolution_rejected(self):
        with self.assertRaises(ValueError):validate_report("\n".join(rows()[:-1]))

if __name__=="__main__":unittest.main()
