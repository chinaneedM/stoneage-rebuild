"""Public tests use only synthetic 1x1 PNGs, never original copyrighted data."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

from tools import stoneage_o6_private_export as o6


def fake_png():
    def chunk(tag,data):
        return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data))
    return (o6.PNG_SIG+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,6,0,0,0))
            +chunk(b'IDAT',zlib.compress(b'\x00\x00\x00\x00\xff'))+chunk(b'IEND',b''))


def fixture():
    raw=fake_png(); b64=base64.b64encode(raw).decode('ascii'); digest=o6.sha(raw)
    imgs={str(x):b64 for x in range(44)}
    for x in o6.ROOM_KEYS:imgs[x]=b64
    roommeta={k:{'PNG_sha256':digest,'width':1,'height':1} for k in imgs}
    views=[{'floor':1001,'source_DAT_sha256':o6.ROOM_DAT,'inclusive_viewport':o6.EXPECTED_BOUNDS[1001],
            'placements':[{'layer':'tile','source_xy':[7,12],'map_id':0} for _ in range(27)]},
           {'floor':1000,'source_DAT_sha256':o6.TOWN_DAT,
            'placements':[{'layer':'tile','source_xy':[60,96],'map_id':0} for _ in range(54)]}]
    warps=[{'source_floor':1001,'source_xy':[10,15],'destination_floor':1000,'destination_xy':[63,99]},
           {'source_floor':1000,'source_xy':[63,99],'destination_floor':1001,'destination_xy':[10,15]}]
    # 208 unique numeric bitmap IDs; 352 ordered occurrences; no assumed species identity.
    ids=list(range(95883,95883+208));
    groups=[]; idx=0
    for no,n in o6.EXPECTED_GROUP_COUNTS.items():
        positions=(ids[idx:idx+n] if n==208 else [ids[i%208] for i in range(n)])
        if n==208: idx=0
        per=n//8
        anims=[{'direction':i,'action':0,'frames':[[v,0,0,0] for v in positions[i*per:(i+1)*per]],
                'duration_word':1000} for i in range(8)]
        groups.append({'spr_no':no,'animations':anims})
    # Ensure bitmap membership exactly 208, via the third numeric group.
    source={'r15':{'views':views,'resources':roommeta,'images':imgs,'doorway_pair':warps,
                   'human_image':b64},
            'r21':{'bounds':o6.EXPECTED_BOUNDS[1000],'images':{key:b64 for key in (
                'old_parts0_npc0','old_parts1_npc0','old_parts0_npc1','old_parts1_npc1',
                'expanded_parts0_npc0','expanded_parts1_npc0','expanded_parts0_npc1','expanded_parts1_npc1')},
                'canvas_size':[1,1],'origin':[0,0],'source_map_sha256':o6.TOWN_DAT,
                'source_NPC_cell_original_three_u16':[187,0,49152]},
            'r22':{'position':[63,103],'graphic_key':16048,'text_sha256':'a'*64},
            'tw1':{'spr_no':100000,'direction':0,'action_code':6,'frames':[b64]*7,'frame_count':7},
            'limits':{'original_world_entered':False,'official_TW1_map_authenticated':False}}
    pet={'provenance':o6.SOURCE_SCOPE,'groups':groups,
         'images':{str(i):b64 for i in ids},'image_png_sha256':{str(i):digest for i in ids}}
    return source,pet


class SourceScopeGuard(unittest.TestCase):
    def test_synthetic_layout_is_valid(self):
        o6.validated_model(*fixture())

    def test_real_png_validation(self):
        raw=fake_png();self.assertEqual(o6.image_from_b64(base64.b64encode(raw).decode(),expected=o6.sha(raw))[1],[1,1])

    def test_tampered_png_hash_fails(self):
        with self.assertRaisesRegex(ValueError,'PNG SHA'):
            o6.image_from_b64(base64.b64encode(fake_png()).decode(),expected='0'*64)

    def test_non_png_rejected(self):
        with self.assertRaisesRegex(ValueError,'PNG'):
            o6.image_from_b64(base64.b64encode(b'not-a-PNG').decode())

    def test_oversized_png_dimensions_rejected(self):
        raw=bytearray(fake_png());raw[16:20]=struct.pack('>I',99999)
        with self.assertRaisesRegex(ValueError,'dimensions'):
            o6.png(bytes(raw))

    def test_unpinned_browser_html_rejected(self):
        with self.assertRaisesRegex(ValueError,'unrecognized original O5 HTML'):
            o6.parse_pinned_html(b'<script id="source">bad</script>')

    def test_wrong_map_version_is_rejected(self):
        src,pet=fixture();src['r15']['views'][0]['source_DAT_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'DAT provenance'):
            o6.validated_model(src,pet)

    def test_cross_version_official_claim_is_rejected(self):
        src,pet=fixture();src['limits']['official_TW1_map_authenticated']=True
        with self.assertRaisesRegex(ValueError,'native world'):
            o6.validated_model(src,pet)

    def test_directions_and_action_immutable(self):
        src,pet=fixture();pet['groups'][0]['animations'][0]['action']=5
        with self.assertRaisesRegex(ValueError,'direction/action'):
            o6.validated_model(src,pet)

    def test_352_frames_conserved(self):
        src,pet=fixture();pet['groups'][0]['animations'][0]['frames'].pop()
        with self.assertRaisesRegex(ValueError,'frame occurrence'):
            o6.validated_model(src,pet)

    def test_missing_original_pet_image_is_rejected(self):
        src,pet=fixture();pet['images'].pop(next(iter(pet['images'])))
        with self.assertRaisesRegex(ValueError,'payload count'):
            o6.validated_model(src,pet)

    def test_wrong_warp_coordinates_are_rejected(self):
        src,pet=fixture();src['r15']['doorway_pair'][1]['source_xy']=[63,100]
        with self.assertRaisesRegex(ValueError,'warp tuple'):
            o6.validated_model(src,pet)

    def test_untrusted_source_profile_is_rejected(self):
        src,pet=fixture();pet['provenance']='OFFICIAL_TW1'
        with self.assertRaisesRegex(ValueError,'profile'):
            o6.validated_model(src,pet)

    def test_duplicate_private_json_id_rejected(self):
        p=o6.EmbeddedJSON()
        with self.assertRaisesRegex(ValueError,'duplicate private JSON'):
            p.feed('<script type="application/json" id="source">{}</script>'*2)

    def test_full_synthetic_archive_to_275_PNGs_with_no_native_execution(self):
        src,pet=fixture()
        html=('<!doctype html><script type="application/json" id="source">'
             +json.dumps(src,separators=(',',':'))+'</script>'
             +'<script type="application/json" id="o5-data">'
             +json.dumps(pet,separators=(',',':'))+'</script>').encode()
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp); zpath=tmp/'synthetic.zip'; dest=tmp/'private';dest.mkdir();repo=tmp/'repo';repo.mkdir()
            with zipfile.ZipFile(zpath,'w') as z:z.writestr('index.html',html)
            with patch.object(o6,'O5_SHA',o6.sha(zpath.read_bytes())),patch.object(o6,'O5_HTML_SHA',o6.sha(html)):
                output=o6.export_private(zpath,dest,repo)
            self.assertEqual(output['original_PNGs_exported'],275)
            self.assertEqual(len(list(dest.rglob('*.png'))),275)
            self.assertEqual(len(json.loads((dest/'pet-numeric-timeline.json').read_text())['groups']),3)
            self.assertTrue(all(output['unproven'].values()))
            self.assertFalse(output['network_access_or_legacy_executable_used'])

    def test_refuse_existing_output_contents_and_repository_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);repo=tmp/'repo';repo.mkdir();dest=repo/'source-png';dest.mkdir();dummy=tmp/'input.zip';dummy.write_bytes(b'fake')
            with self.assertRaisesRegex(ValueError,'public repo'):
                o6.export_private(dummy,dest,repo)
            other=tmp/'other';other.mkdir();(other/'should-not-delete').write_bytes(b'keep')
            with self.assertRaisesRegex(ValueError,'not empty'):
                o6.export_private(dummy,other,repo)
            self.assertEqual((other/'should-not-delete').read_bytes(),b'keep')


if __name__=='__main__':unittest.main()