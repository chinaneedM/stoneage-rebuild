"""Synthetic-only guards for bounded archived-image acquisition and identity scope."""
import copy
from io import BytesIO
import json
import unittest
from PIL import Image
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from tools import stoneage_jp_pet_visual_r25_source as source
from tools.stoneage_p3_private_frame import unseal


def gif():
    out=BytesIO(); Image.new('RGB',(60,65),(12,34,56)).save(out,format='GIF'); return out.getvalue()


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parents=source.selected(source.PARENT.read_bytes(),source.PRIOR.read_bytes())
        key=X25519PrivateKey.generate()
        cls.private=key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption())
        cls.public=key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)

    def test_first12_unacquired_not_prior_sample_or_client_ids(self):
        self.assertEqual([x['web_ordinal'] for x in self.parents],[3,4,5,6,7,8,9,11,12,13,14,15])
        self.assertTrue(all(x['client_species_graphic_ids'] is None for x in self.parents))

    def test_parent_byte_drift_rejected(self):
        with self.assertRaises(ValueError): source.selected(source.PARENT.read_bytes()+b' ',source.PRIOR.read_bytes())

    def test_exact_gif_and_capture_independent_of_parent_epoch(self):
        p=self.parents[0];url='https://web.archive.org/web/20060604070000id_/'+p['image']['original_url']
        row,envelope=source.acquire_one(p,self.public,lambda _: (gif(),url,200,'image/gif'))
        self.assertEqual(row['image']['actual_capture'],'20060604070000')
        self.assertNotEqual(row['image']['actual_capture'],p['source_refs'][0]['actual_capture'])
        raw=unseal(envelope,self.private)
        self.assertEqual(source.sha(raw),row['image']['decoded_png_sha256'])
        with Image.open(BytesIO(raw)) as im:
            self.assertEqual(source.sha(im.convert('RGBA').tobytes()),row['image']['rgba_sha256'])
        self.assertFalse(row['visual_review_performed_at_source'])

    def test_html_placeholder_is_unacquired_and_only_one_attempt(self):
        calls=[];p=self.parents[0]
        def fetch(url): calls.append(url);return b'<html>rate limit</html>',url,200,'text/html'
        row,envelope=source.acquire_one(p,self.public,fetch)
        self.assertEqual(len(calls),1);self.assertIsNone(envelope);self.assertIsNone(row['image'])
        self.assertEqual(row['status'],'UNAVAILABLE_OR_UNQUALIFIED_THIS_SINGLE_ATTEMPT')

    def test_wrong_host_path_capture_and_rewrite_mode_rejected(self):
        original=self.parents[0]['image']['original_url']
        for url in ['https://example.com/x','https://web.archive.org/web/20060604070000/'+original,
                    'https://web.archive.org/web/20060604070000id_/'+original+'x',
                    'https://web.archive.org/web/latestid_/'+original]:
            with self.subTest(url=url),self.assertRaises(ValueError):source.inspect(gif(),url,original)

    def test_png_or_oversized_response_cannot_be_gif(self):
        p=self.parents[0];url='https://web.archive.org/web/20060604070000id_/'+p['image']['original_url']
        for raw in [b'\x89PNG\r\n\x1a\n',gif()+bytes(100001)]:
            with self.assertRaises(ValueError):source.inspect(raw,url,p['image']['original_url'])

    def test_wrong_dimensions_rejected(self):
        p=self.parents[0];url='https://web.archive.org/web/20060604070000id_/'+p['image']['original_url']
        out=BytesIO();Image.new('RGB',(1,1)).save(out,format='GIF')
        with self.assertRaises(ValueError):source.inspect(out.getvalue(),url,p['image']['original_url'])

    def test_animated_gif_not_silently_reduced_to_first_frame(self):
        p=self.parents[0];url='https://web.archive.org/web/20060604070000id_/'+p['image']['original_url']
        out=BytesIO();Image.new('RGB',(60,65),'red').save(out,format='GIF',save_all=True,append_images=[Image.new('RGB',(60,65),'blue')])
        with self.assertRaises(ValueError):source.inspect(out.getvalue(),url,p['image']['original_url'])

    def test_all_unavailable_do_not_become_coverage(self):
        def fetch(_): raise TimeoutError('synthetic timeout')
        report,envelopes=source.run(self.public,fetch)
        self.assertEqual(report['counts']['qualified_gifs'],0)
        self.assertEqual(report['counts']['qualified_reference_total'],13)
        self.assertEqual(report['counts']['unacquired_references'],111)
        self.assertEqual(envelopes,{})
        self.assertTrue(all(x['attempt_count']==1 and x['image'] is None for x in report['entries']))


class MaterialJoinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools import stoneage_jp_pet_visual_r25 as material
        cls.material=material
        cls.doc=json.loads(material.REPORT.read_bytes())
        cls.source=json.loads(material.SOURCE.read_bytes())
        cls.observations=json.loads(material.OBSERVATIONS.read_bytes())

    def test_actual_permanent_source_join_and_custody(self):
        self.material.validate(self.doc)
        self.assertEqual(self.doc['counts']['qualified_reference_total'],23)
        self.assertEqual(self.doc['new_image_capture_year_counts'],{'2003':2,'2006':8})

    def test_seven_required_record_fields_and_unproven_client_identity(self):
        for row in self.doc['records']:
            self.assertTrue({'record_id','record_revision','entity_type','version_profile',
                             'source_refs','verification_status','rights_status'} <= row.keys())
            self.assertIsNone(row['client_species_graphic_ids'])
            self.assertIsNone(row['cross_region_aliases'])
            self.assertIsNone(row['stats_growth_habitat_skills'])

    def test_name_reassignment_to_visually_similar_image_rejected(self):
        source=copy.deepcopy(self.source);source['entries'][0]['name_as_written']='invented'
        with self.assertRaises(ValueError):self.material.build(source,self.observations)

    def test_capture_era_not_promoted_to_parent_page(self):
        source=copy.deepcopy(self.source)
        source['entries'][1]['image']['actual_capture']='20031214055443'
        with self.assertRaises(ValueError):self.material.build(source,self.observations)

    def test_unseen_or_mismatched_decoded_pixels_rejected(self):
        for key,value in [('assistant_viewed',False),('decoded_png_sha256','0'*64),
                          ('identity_or_taxonomy_inferred',True)]:
            observations=copy.deepcopy(self.observations);observations['entries']['3'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.material.build(self.source,observations)

    def test_failed_14_15_have_no_image_or_invented_review(self):
        rows={r['web_ordinal']:r for r in self.doc['records']}
        for n in [14,15]:
            self.assertFalse(rows[n]['image']['pixels_acquired'])
            self.assertIsNone(rows[n]['visual_review'])
            self.assertIn('Connection refused',rows[n]['failure_this_attempt'])
        observations=copy.deepcopy(self.observations);observations['entries']['14']=observations['entries']['3']
        with self.assertRaises(ValueError):self.material.build(self.source,observations)

    def test_false_game_coverage_and_durable_delivery_refused(self):
        for key in ['original_world_entered','tw10_or_cross_region_species_identity_proven',
                    'source_pngs_durably_delivered_to_user']:
            doc=copy.deepcopy(self.doc);doc['boundaries'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):self.material.validate(doc)

    def test_prior_sample_not_double_counted(self):
        doc=copy.deepcopy(self.doc);doc['counts']['qualified_reference_total']=25
        with self.assertRaises(ValueError):self.material.validate(doc)


if __name__=='__main__':unittest.main()
