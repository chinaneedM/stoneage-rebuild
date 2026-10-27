"""Synthetic negative/positive contracts; no copyrighted game assets in CI."""
from __future__ import annotations
import hashlib
import json
import struct
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from tools.stoneage_private_scene_graphic_join_r1 import (
    resolve_ids, join, export_private, requires_mapping, is_later_draw_candidate, authenticate, SCHEMA
)

def record(map_number, bitmapno, offset, size=18, width=1, height=2):
    row=bytearray(80)
    struct.pack_into("<IIIiiii",row,0,bitmapno,offset,size,0,0,width,height)
    struct.pack_into("<I",row,76,map_number)
    return bytes(row)

def region(events=(1,0), tile=(100,0), obj=(60,79), kind="CLIENT_DAT_THREE_PLANE"):
    status=("RECOVERED_CLIENT_DAT" if events is not None else
            "ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE")
    area=SimpleNamespace(floor_id=123,map_width=2,map_height=1,
        x1=0,y1=0,x2=1,y2=0,tile_ids=tile,object_ids=obj,event_ids=events,
        source_kind=kind,event_plane_status=status,payload_sha256="a"*64)
    req=SimpleNamespace(floor_id=123,x1=0,y1=0,x2=1,y2=0,world_profile="recovered25")
    prov={"world_profile":"recovered25","evidence_role":"LATER_RECOVERED",
        "content_role":"LATER_RECOVERED","payload_sha256":"a"*64,
        "payload_kind":kind,"event_plane_status":status}
    return SimpleNamespace(payload=area,request=req,provenance=prov)

def rd():
    return b"RD"+bytes([0,0])+struct.pack("<III",1,2,18)+bytes([8,9])

class PrivateSceneGraphicJoinTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        self.real=self.root/"real_15.bin"
        self.real.write_bytes(rd()*4)

    def checked(self,source,adrn):
        return join(source,adrn,self.real,
            expected_adrn=(len(adrn),hashlib.sha256(adrn).hexdigest()),
            expected_real=(self.real.stat().st_size,
                           hashlib.sha256(self.real.read_bytes()).hexdigest()))

    def test_source_bytes_and_private_indexed_preview(self):
        r,files=self.checked(region(),record(100,8,0)+record(60,9,18)+record(79,10,36))
        self.assertEqual(r["schema"],SCHEMA)
        self.assertEqual(r["map_ids_required"],[100])
        self.assertEqual(r["special_collision_ids_not_drawn"],[60,79])
        self.assertEqual(r["preview_count"],1)
        self.assertFalse(r["authentic_scene_rendered"])
        self.assertFalse(r["source_pins_match_preserved_bundle"])
        self.assertTrue(r["collision_lookup_not_draw_selection"])
        self.assertIn(b"NOT ORIGINAL SCENE COLORS",files[0][1])
        out=self.root/"private";out.mkdir()
        path=export_private(out,r,files)
        self.assertTrue(path.exists())
        self.assertFalse(json.loads(path.read_text())["original_world_entered"])
        with self.assertRaises(ValueError):export_private(out,r,files)

    def test_duplicate_map_number_is_not_last_wins(self):
        adrn=record(100,1,0)+record(100,2,18)+record(60,3,36)+record(79,4,54)
        mapping=resolve_ids(adrn,{60,100},self.real.stat().st_size)
        self.assertEqual([x["bitmapno"] for x in mapping[100]],[1,2])
        r,files=self.checked(region(),adrn)
        ambiguous=next(x for x in r["resources"] if x["map_id"]==100)
        self.assertEqual(ambiguous["status"],"DUPLICATE_ADRN_MAP_NUMBER_SELECT_RULE_OPEN")
        self.assertEqual(len(ambiguous["occurrences"]),2)
        self.assertEqual(len(files),0)

    def test_missing_mapping_is_never_filled_with_fake_art(self):
        r,files=self.checked(region(tile=(100,101)),record(100,9,0))
        self.assertEqual(len(files),1)
        self.assertEqual(sum(x["status"]=="SOURCE_ADRN_MAPPING_MISSING" for x in r["resources"]),1)

    def test_server_event_layer_absent_not_zero(self):
        a=region(events=None,kind="SERVER_LS2MAP_TWO_PLANE")
        r,_=self.checked(a,record(100,9,0))
        self.assertEqual(r["event_plane_status"],"ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE")
        a.payload.event_ids=(0,0)
        with self.assertRaises(ValueError):self.checked(a,record(100,9,0))

    def test_source_grade_cannot_be_silently_promoted(self):
        a=region()
        a.provenance["content_role"]="TW1_DIRECT"
        with self.assertRaises(ValueError):self.checked(a,record(100,9,0))

    def test_project_public_source_pins_must_reject_fake_bytes(self):
        with self.assertRaises(ValueError):join(region(),record(100,9,0),self.real)
        with self.assertRaises(ValueError):join(region(),record(100,9,0),self.real,
            expected_adrn=(80,"0"*64),
            expected_real=(self.real.stat().st_size,hashlib.sha256(self.real.read_bytes()).hexdigest()))

    def test_bad_raw_record_range(self):
        with self.assertRaises(ValueError):resolve_ids(record(100,9,100000),{100},72)

    def test_record_map_number_is_at_76_not_bitmap_id(self):
        self.assertEqual(resolve_ids(record(100,999,0),{100},72)[100][0]["bitmapno"],999)

    def test_read_hit_map_range_is_limited_candidate(self):
        self.assertFalse(requires_mapping(59))
        self.assertTrue(requires_mapping(60))
        self.assertFalse(requires_mapping(80))
        self.assertFalse(requires_mapping(99))
        self.assertTrue(requires_mapping(100))
        self.assertFalse(is_later_draw_candidate(60))
        self.assertTrue(is_later_draw_candidate(100))
        with self.assertRaises(ValueError):resolve_ids(b"",set(range(100,117)),72)

    def test_private_output_refuses_existing_destination(self):
        r,files=self.checked(region(),record(100,9,0))
        out=self.root/"private";out.mkdir()
        (out/"sentinel").write_text("preserve")
        with self.assertRaises(ValueError):export_private(out,r,files)
        self.assertEqual((out/"sentinel").read_text(),"preserve")

    def test_full_digest_authentication_refuses_byte_tampering(self):
        original=hashlib.sha256(self.real.read_bytes()).hexdigest()
        authenticate(self.real,self.real.stat().st_size,original)
        with self.assertRaises(ValueError):authenticate(self.real,self.real.stat().st_size,"0"*64)
        with self.assertRaises(ValueError):authenticate(self.real,4,original)

    def test_wrong_adnr_record_alignment(self):
        with self.assertRaises(ValueError):resolve_ids(b"\0"*79,{100},72)

if __name__=="__main__":
    unittest.main()
