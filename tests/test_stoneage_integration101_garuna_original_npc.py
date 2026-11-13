"""Public derived-only regression tests for INTEGRATION101: no proprietary text required."""
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
REPORT=ROOT/'research/recovered/STONEAGE-INTEGRATION101-GARUNA-TWO-SETTLEMENTS-ORIGINAL-NPC-R1.json'

def gitsha(path):
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()

class TestGarunaOriginalNPC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=json.loads(INDEX.read_text(encoding='utf-8'))
        cls.m=json.loads(MAP.read_text(encoding='utf-8'))
        cls.r=json.loads(REPORT.read_text(encoding='utf-8'))
        cls.src=[x for x in cls.o['create_rows'] if x[0]=='genout/garunaev1.create']
        cls.out=cls.r['original_CREATE_source_bounded_rows']
        cls.files={x[0]:x for x in cls.o['source_files']}
        cls.maps={x[0]:x for x in cls.m['per_floor_source_rows']}

    def test_prior_public_git_blob_byte_integrity(self):
        self.assertEqual(gitsha(INDEX),'a088b61a3212f7049e7793f587123ffb29bebad7')
        self.assertEqual(gitsha(MAP),'1ef8c004179128ea44ffa4fb4259748bc8c83911')

    def test_different_same_basename_originals(self):
        a=self.files['genout/garunaev1.create']
        b=self.files['giiru/event/garunaev1.create']
        self.assertEqual(a[1],4992)
        self.assertEqual(b[1],1983)
        self.assertNotEqual(a[2],b[2])
        self.assertEqual(a[2],self.r['original_private_source']['original_CREATE_SHA256'])
        self.assertEqual(b[2],self.r['original_private_source']['different_original_full_SHA256'])

    def test_all_28_original_windows_anchored(self):
        self.assertEqual(len(self.src),len(self.out))
        self.assertEqual(len(self.out),28)
        for x,y in zip(self.src,self.out):
            with self.subTest(ordinal=x[1]):
                self.assertEqual(x[1],y['ordinal'])
                self.assertEqual([x[2],x[3]],y['original_CREATE_byte_halfopen'])
                self.assertEqual(x[4],y['original_CREATE_block_sha256'])
                self.assertEqual(x[5],y['source_floorid'])
                self.assertEqual(x[6],y['original_graphicname_alias'])
                self.assertEqual(x[7][:2],y['original_borncorner_xy'])
                self.assertEqual(x[10],y['original_direction'])
                self.assertEqual(x[14],y['original_name_field_utf8_sha256'])
                self.assertEqual(x[11],y['original_enemy_template'])

    def test_27_exact_original_handler_sha_and_one_inline(self):
        n=0
        for x,y in zip(self.src,self.out):
            h=y['original_handler']
            if x[15]:
                self.assertEqual(len(x[15]),1)
                s=x[15][0]
                self.assertEqual('npc/'+s[0],h['member'])
                self.assertEqual(s[1],'EXACT_SAME_NPC_SUBTREE_PATH')
                self.assertEqual(s[2],h['full_sha256'])
                self.assertEqual(self.files[s[0]][2],s[2])
                self.assertGreater(h['byte_size'],0)
                n+=1
            else:
                self.assertIsNone(h['member'])
                self.assertEqual(h['source_class'],'inline_literal_in_verified_original_CREATE_block')
                self.assertEqual(len(h['inline_literal_sha256']),64)
        self.assertEqual(n,27)
        self.assertEqual(sum(x['original_handler']['byte_size'] for x in self.out if x['original_handler']['member']),1941)

    def test_four_original_DAT_sources_and_28_coordinates(self):
        self.assertEqual(Counter(x['source_floorid'] for x in self.out),{31001:4,31002:10,31101:4,31102:10})
        for o in self.out:
            d=o['prior_original_MAP04_DAT']
            old=self.maps[str(o['source_floorid'])+'.dat']
            self.assertEqual(d['full_DAT_original_SHA256_from_prior_catalog'],old[2])
            self.assertEqual([d['width'],d['height']],old[3:5])
            self.assertEqual(old[3:5],[50,50])
            a,b=o['original_borncorner_xy']
            self.assertTrue(0<=a<50 and 0<=b<50)
            self.assertIs(d['spawn_header_in_bounds'],True)

    def test_not_28_species_or_26_verified_sprites(self):
        self.assertEqual({x['original_enemy_template'] for x in self.out},{'npcgen_man'})
        self.assertEqual(len(set(x['original_graphicname_alias'] for x in self.out)),26)
        self.assertEqual(len(set(x['original_name_field_utf8_sha256'] for x in self.out)),2)
        self.assertIs(self.r['limits']['numeric_graphicname_equals_qualified_TW1_original_pixels'],False)

    def test_negative_native_and_original_game_boundary(self):
        for key,value in self.r['limits'].items():
            self.assertIs(value,False,key)
        s=self.r['historical_preservation']
        self.assertEqual(s['CURRENT_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(s['CURRENT_bytes'],2709173)
        self.assertEqual(s['Stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertEqual(s['Stage_B'],'GATED')
        self.assertIsNone(s['overall_percent'])

if __name__=='__main__':unittest.main()
