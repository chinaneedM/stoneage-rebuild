"""Negative controls for default compiled PET equipment source gate."""
import hashlib
import unittest
from tools.stoneage_pet_item_build_gate_audit import EXTRA,validate

def fixture():
    rows=[]
    for p in ("gavin","bismarck"):
        arr=[("char/char_item.c",2655,1)] if p=="bismarck" else []
        h=hashlib.sha256()
        for path,n,d in arr:h.update(f"{path}:{n}:{d}\n".encode())
        d=dict(profile=p,make_blob=EXTRA[p]["make"][1],
               char_make_blob=EXTRA[p]["char_make"][1],
               macro_unique=1,macro_simplify=1,macro_pet=0,
               default_pet_equip=0,forced_pet_equip=int(p=="bismarck"),
               default_pet_send=0,raw_equip_definitions=int(p=="bismarck"),
               raw_equip_callers=0,raw_equip_occurrences=len(arr),
               site_sha256=h.hexdigest(),production_binary_verified=0,
               natural_pet_alias_proven=0,early_build_proven=0)
        rows.append("SOURCE_PET_BUILD_GATE|"+"|".join(f"{k}={v}" for k,v in d.items()))
        for path,n,z in arr:
            rows.append(f"SOURCE_PET_EQUIP_SITE|profile={p}|path={path}|line={n}|definition={z}")
    rows.append("RESOLUTION|PET_BUILD_DEFAULT_SOURCE_ONLY_PASS")
    return rows

class PetBuildGateTest(unittest.TestCase):
    def test_complete(self):
        summaries,sites=validate("\n".join(fixture()))
        self.assertEqual(len(summaries),2)
        self.assertEqual(len(sites["bismarck"]),1)
    def test_any_row_missing(self):
        lines=fixture()
        for i in range(len(lines)):
            with self.subTest(i=i),self.assertRaises(ValueError):
                validate("\n".join(lines[:i]+lines[i+1:]))
    def test_disable_gates_cannot_be_renamed_as_enabled(self):
        for old,new in (("default_pet_equip=0","default_pet_equip=1"),
                        ("default_pet_send=0","default_pet_send=1"),
                        ("macro_pet=0","macro_pet=1"),
                        ("forced_pet_equip=1","forced_pet_equip=0"),
                        ("production_binary_verified=0","production_binary_verified=1"),
                        ("natural_pet_alias_proven=0","natural_pet_alias_proven=1"),
                        ("early_build_proven=0","early_build_proven=1")):
            data=fixture()
            with self.subTest(field=old),self.assertRaises(ValueError):
                validate("\n".join(x.replace(old,new) for x in data))
    def test_raw_site_digest_count_and_definitions_enforced(self):
        for old,new in (("raw_equip_occurrences=1","raw_equip_occurrences=2"),
                        ("raw_equip_callers=0","raw_equip_callers=1"),
                        ("raw_equip_definitions=1","raw_equip_definitions=0"),
                        ("definition=1","definition=0"),
                        ("line=2655","line=9999"),
                        ("char/char_item.c","char/other_item.c")):
            rows=fixture()
            with self.subTest(old=old),self.assertRaises(ValueError):
                validate("\n".join(x.replace(old,new) for x in rows))
    def test_duplicate_fields_profile_unknown_and_resolution(self):
        data=fixture()
        for modified in (data+[data[0]],
                         [data[0]+"|extra=1"]+data[1:],
                         [data[0]+"|macro_pet=0"]+data[1:],
                         [data[0].replace("profile=gavin","profile=unknown")]+data[1:],
                         data[:-1]):
            with self.assertRaises(ValueError):
                validate("\n".join(modified))
    def test_gavin_cannot_have_pet_equip(self):
        data=fixture()
        data[0]=data[0].replace("raw_equip_definitions=0","raw_equip_definitions=1")
        with self.assertRaises(ValueError):validate("\n".join(data))
    def test_pinned_build_blob_required(self):
        data=fixture()
        data[0]=data[0].replace(EXTRA["gavin"]["make"][1],"f"*40)
        with self.assertRaises(ValueError):validate("\n".join(data))

if __name__=="__main__":unittest.main()
