"""No source-count, face-art, palette or allocation identity by inference."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from tools.stoneage_jp2003_creation_reference_join import INPUTS, ROOT, REPORT, build, validate_report
from tools.stoneage_early_mail_venue_crosswalk import pointer


class CreationReferenceJoinTests(unittest.TestCase):
    def reject(self, i, key, value, message):
        o=json.loads(REPORT.read_text());o['records'][i]['source_facts'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_same_twelve_denominator_does_not_bind_type_palette_or_48_entities(self):
        self.reject(0,'forty_eight_new_character_entities',True,'Matching cardinality')
        o=json.loads(REPORT.read_text());o['records'][0]['source_facts']['position_reference_index'][0]['exact_appearance_type_or_color_ids']={'body':1}
        with self.assertRaisesRegex(ValueError,'model/color'):validate_report(o)

    def test_twelve_existing_references_cannot_duplicate_or_swap_positions(self):
        o=json.loads(REPORT.read_text());ix=o['records'][0]['source_facts']['position_reference_index'];ix[0]=deepcopy(ix[1])
        with self.assertRaisesRegex(ValueError,'duplicated or misbound'):validate_report(o)

    def test_player_named_positions_not_later_canonical_nicknames(self):
        self.reject(1,'canonical_names_or_later_nickname_aliases',['FAMILIAR_LATER_NAME'],'canonical identity')

    def test_static_art_and_uninspected_companion_not_face_editor_component(self):
        self.reject(2,'static_illustration_or_companion_is_face_editor_asset','charapicillust1.gif','Face editor')
        self.reject(2,'companion_reference_role','ORIGINAL_ANIMATED_SPRITE','Face editor')

    def test_one_2006_image_not_four_2003_color_sets_or_full_animation(self):
        self.reject(3,'reviewed_image_capture','20031214051427','Later illustration')
        self.reject(3,'four_colors_names_or_animation_sets',['ORANGE','RED','BLUE','GREEN'],'Later illustration')

    def test_2001_points_not_later_2003_allocation_values(self):
        self.reject(4,'same_allocation_values_or_same_build_proven',True,'Earlier allocation')

    def test_byte_pin_changes_and_missing_inputs_rejected(self):
        raw={k:(ROOT/v[0]).read_bytes() for k,v in INPUTS.items()}
        for key in raw:
            bad=dict(raw);bad[key]+=b'\n'
            with self.assertRaisesRegex(ValueError,'byte pin'):build(bad)
        raw.pop('features')
        with self.assertRaisesRegex(ValueError,'Exact three'):build(raw)

    def test_all_pointers_archive_fields_body_and_existing_image_counts(self):
        o=json.loads(REPORT.read_text());validate_report(o)
        self.assertEqual(build({k:(ROOT/v[0]).read_bytes() for k,v in INPUTS.items()}),o)
        c=json.loads((ROOT/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required'];bodies=set();images=set()
        for r in o['records']:
            self.assertLessEqual(set(c),r.keys())
            for ref in r['source_refs']:
                pointer(json.loads(Path(ref['derived_report']).read_bytes()),ref['json_pointer'])
                (images if ref['object_kind']=='EXISTING_REVIEWED_WEB_IMAGE' else bodies).add((ref['original_url'],ref['actual_capture'],ref['original_sha256']))
        self.assertEqual((len(bodies),len(images)),(3,1))
        o['coverage']['new_original_requests_images_or_entities']=1
        with self.assertRaisesRegex(ValueError,'counted as new'):validate_report(o)


if __name__=='__main__':unittest.main()
