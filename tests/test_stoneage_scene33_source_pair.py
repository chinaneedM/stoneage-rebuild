"""Public derived receipts and synthetic malformed inputs; no historical assets."""
import copy
import json
import struct
import unittest

from tools import stoneage_scene33_source_pair as m


class SourcePairBoundaries(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(m.REPORT.read_text())

    def reject(self,mutate,message):
        r=copy.deepcopy(self.r);mutate(r)
        with self.assertRaisesRegex(ValueError,message):m.validate(r)

    def test_frozen_actual_static_receipt(self):
        self.assertEqual(m.validate(self.r)['source_members'],8)

    def test_every_runtime_and_official_promotion_rejected(self):
        for flag in m.FALSE:
            with self.subTest(flag=flag):
                self.reject(lambda r:r.update({flag:True}),'static is not runtime')

    def test_other_archive_rejected(self):
        self.reject(lambda r:r['parent_archive'].update(sha256='0'*64),'parent archive')

    def test_same_filename_other_member_rejected(self):
        self.reject(lambda r:r['source_inputs'][0].update(sha256='0'*64),'source identities')

    def test_duplicate_member_cannot_replace_missing_member(self):
        self.reject(lambda r:r['source_inputs'].__setitem__(1,r['source_inputs'][0]),'source identities')

    def test_static_ports_must_join(self):
        self.reject(lambda r:r['config_pair'].update(saac_listen_port=9201),'host/port join')

    def test_auth_equality_not_assumed(self):
        self.reject(lambda r:r['config_pair'].update(static_auth_token_bytes_equal=False),'credential equality')

    def test_auth_value_publication_rejected(self):
        self.reject(lambda r:r['config_pair'].update(auth_values_published=True),'credential equality')

    def test_blank_fields_cannot_be_silently_defaulted(self):
        self.reject(lambda r:r['config_pair'].update(blank_startup_values=[]),'blank fields')

    def test_import_descriptor_repetitions_not_deduplicated(self):
        self.reject(lambda r:r['binaries']['gmsv/gmsv.exe'].update(import_DLL_occurrences=['cygwin1.dll','KERNEL32.dll']),'duplicate import descriptor')

    def test_both_cygwin_occurrences_required(self):
        self.reject(lambda r:r['binaries'].pop('saac/cygwin1.dll'),'five original PE')

    def test_later_version_markers_not_erased(self):
        self.reject(lambda r:r.update(startup_config_comment_8_0_present=False),'lineage markers')

    def test_reference_presence_does_not_prove_validity(self):
        self.reject(lambda r:r['startup_file_references'][1].update(required_at_startup_proven=True),'presence is not startup')

    def test_missing_lockip_not_invented(self):
        self.reject(lambda r:r['startup_file_references'][0].update(archive_occurrences=1),'reference coverage')

    def test_header_crc_not_second_decompressor(self):
        self.reject(lambda r:r['extraction_witness'].update(successful_second_decompressor_for_all_eight=True),'one successful decompressor')

    def test_ci_not_original_source_action(self):
        self.reject(lambda r:r.update(source_action_run_id=123),'source/percent not invented')

    def test_unchecked_report_fact_cannot_drift(self):
        self.reject(lambda r:r.update(client_literal_IP_colon_marker_occurrences=1),'frozen actual')

    def test_actual_independent_audit(self):
        self.assertTrue(m.validate_audit(json.loads(m.AUDIT.read_text()),self.r))

    def test_audit_other_source_report_rejected(self):
        a=json.loads(m.AUDIT.read_text());a['source_report_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'audit/report binding'):m.validate_audit(a,self.r)

    def test_audit_cannot_drop_duplicate_dll_occurrence(self):
        a=json.loads(m.AUDIT.read_text());a['five_actual_PE_import_comparisons'].pop()
        with self.assertRaisesRegex(ValueError,'PE occurrence coverage'):m.validate_audit(a,self.r)


class SyntheticReaders(unittest.TestCase):
    def test_config_comments_opaque_and_blank_retained(self):
        rows,opaque=m.config_rows(b'# ignored=1\nport 9200\napport=\n=\n} config;\n')
        self.assertEqual(rows,[{'line':2,'key':'port','value':'9200'},{'line':3,'key':'apport','value':''}])
        self.assertEqual(opaque,[4,5])

    def test_duplicate_config_key_rejected_instead_of_last_wins(self):
        rows,_=m.config_rows(b'port 9200\nport=9201\n')
        with self.assertRaisesRegex(ValueError,'unique original config key'):m.one(rows,'port')

    def test_pe_header_extent_rejects_truncation(self):
        b=bytearray(160);b[:2]=b'MZ';struct.pack_into('<I',b,60,150)
        with self.assertRaisesRegex(ValueError,'PE signature'):m.pe_imports(b)

    def test_pe_section_raw_range_rejected(self):
        b=bytearray(400);b[:2]=b'MZ';struct.pack_into('<I',b,60,128);b[128:132]=b'PE\0\0'
        struct.pack_into('<HHIIIHH',b,132,0x14c,1,0,0,0,112,0)
        struct.pack_into('<H',b,152,0x10b);struct.pack_into('<IIII',b,272,10,0x1000,1000,380)
        with self.assertRaisesRegex(ValueError,'section raw range'):m.pe_imports(b)

    def test_rar_complete_parent_required_before_header_walk(self):
        with self.assertRaisesRegex(ValueError,'complete original archive'):m.rar_receipt(b'Rar!\x1a\x07\x00',{})


if __name__=='__main__':unittest.main()
