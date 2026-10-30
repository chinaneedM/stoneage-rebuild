import copy
import json
import unittest
from tools import stoneage_scene35_content_card as m


class SourceBoundaries(unittest.TestCase):
    def setUp(self):self.r=json.loads(m.REPORT.read_bytes())

    def reject(self,change,message):
        r=copy.deepcopy(self.r);change(r)
        with self.assertRaisesRegex(ValueError,message):m.validate(r)

    def test_actual_derived_report(self):
        self.assertEqual(m.validate(self.r)['static_NPC_arguments_observed'],1)

    def test_every_historical_promotion_rejected(self):
        for k in m.FALSE:
            with self.subTest(field=k):
                self.reject(lambda r:r.update({k:True}),'cannot become runtime')

    def test_other_parent_rejected(self):
        self.reject(lambda r:r['parent_archive'].update(sha256='0'*64),'parent identity')

    def test_same_filename_other_source_rejected(self):
        self.reject(lambda r:r['NPC_inputs'][2].update(sha256='0'*64),'NPC source identities')

    def test_duplicate_input_cannot_replace_missing_source(self):
        self.reject(lambda r:r['NPC_inputs'].__setitem__(2,r['NPC_inputs'][0]),'NPC source identities')

    def test_encounter_stop_not_silently_removed(self):
        self.reject(lambda r:r['encounter_stop'].update(status='BUILT'),'stop retained')

    def test_descendant_schema_cannot_become_original_header(self):
        self.reject(lambda r:r['encounter_stop']['originals'][0].update(source_field_names_authenticated=True),'layout evidence')

    def test_old_table_audit_not_rerun_as_content(self):
        self.reject(lambda r:r['encounter_stop'].update(old_encounter_audit_rerun=True),'stop retained')

    def test_NPC_reference_not_guessed_from_similar_filename(self):
        self.reject(lambda r:r['NPC'].update(exact_argument_file='npc/genout/msg_1000_63_103'),'point/reference')

    def test_other_same_name_NPC_not_substituted(self):
        self.reject(lambda r:r['NPC'].update(xy=[63,103]),'point/reference')

    def test_raw_direction_not_translated_to_bearing(self):
        self.reject(lambda r:r['NPC'].update(direction_raw='north'),'uninterpreted integers')

    def test_original_segments_keep_order_and_sizes(self):
        self.reject(lambda r:r['literal_comma_segments'].reverse(),'comma segments')

    def test_two_text_fragments_not_two_runtime_branches(self):
        self.reject(lambda r:r.update(runtime_branch_selection_verified=True),'cannot become runtime')

    def test_question_not_invented_quest(self):
        self.reject(lambda r:r.update(quest_origin='BASE_GAME_QUEST'),'invented quest')

    def test_source_action_not_derived_CI(self):
        self.reject(lambda r:r.update(source_action_run_id=123),'source Action/progress')

    def test_whole_actual_report_frozen(self):
        self.reject(lambda r:r.update(editorial_simplified_paraphrase='changed'),'frozen actual')

    def test_actual_private_card_audit(self):
        self.assertTrue(m.validate_audit(json.loads(m.AUDIT.read_bytes()),self.r))

    def test_other_private_source_audit_rejected(self):
        a=json.loads(m.AUDIT.read_bytes());a['source_report_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'audit/source report binding'):m.validate_audit(a,self.r)

    def test_save_acknowledgement_not_second_readback(self):
        a=json.loads(m.AUDIT.read_bytes());a['read_back_after_save']=True
        with self.assertRaisesRegex(ValueError,'not independent readback'):m.validate_audit(a,self.r)


class SyntheticPrivateReader(unittest.TestCase):
    def test_original_text_roundtrip_is_explicitly_synthetic_here(self):
        name='合成村民';text='合成甲,合成乙\n'
        self.assertTrue(m.audit_reader(m.reader(name,text),name,text)['exact_original_name_and_message_HTML_roundtrip'])

    def test_source_HTML_markup_cannot_inject_script_or_resource(self):
        name='<img src=x onerror=alert(1)>'
        text='<script>alert(1)</script>,&<>\"\n'
        r=m.audit_reader(m.reader(name,text),name,text)
        self.assertEqual((r['scripts'],r['external_resources']),(0,0))

    def test_empty_original_segment_positions_preserved(self):
        page=m.reader('合成','甲,,乙,\n')
        self.assertEqual(page.count('<article>'),4)

    def test_line_endings_and_ellipsis_preserved_in_source_field(self):
        name='合成';text='甲…,\n乙\r\n'
        self.assertTrue(m.audit_reader(m.reader(name,text),name,text)['exact_original_name_and_message_HTML_roundtrip'])

    def test_incorrect_original_text_rejected(self):
        with self.assertRaisesRegex(ValueError,'exact original decoded'):
            m.audit_reader(m.reader('甲','乙\n'),'甲','丙\n')

    def test_external_resource_rejected(self):
        with self.assertRaisesRegex(ValueError,'external resource'):
            m.audit_reader(m.reader('甲','乙\n')+'<img src="https://example.com/x">','甲','乙\n')

    def test_duplicate_source_ID_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate source text'):
            m.audit_reader(m.reader('甲','乙\n')+'<pre id="rawMessage">乙\n</pre>','甲','乙\n')

    def test_invalid_original_encoding_refused(self):
        with self.assertRaises(UnicodeDecodeError):m.text_shape(b'\x81')

    def test_synthetic_shape_counts_raw_delimiter_only(self):
        r=m.text_shape('甲，乙,丙\n'.encode('cp950'))
        self.assertEqual((r['ASCII_comma_count'],r['LF_count']),(1,1))


if __name__=='__main__':unittest.main()
