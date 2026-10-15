"""Invented numeric graphs and pinned derivative corruption controls."""
import copy,hashlib,json,random,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r52 import *
from tools.stoneage_tw10_savedata_native_io_r52_guard import reverse_sources,validate as strict_validate

def reg(r,width=4,read=True,write=False):return {'kind':'register','register':r,'width_bytes':width,'decoder_read':read,'decoder_write':write}
def imm(n):return {'kind':'immediate','constant':n,'width_bytes':4,'decoder_read':False,'decoder_write':False}
def row(a,m,read=(),write=(),ops=()):return {'site_rva':a,'mnemonic':m,'decoder_read_registers':sorted(read),'decoder_written_registers':sorted(write),'operands':list(ops)}
def graph():return [row(1,'mov',(),('eax',),(reg('eax',write=True,read=False),imm(9))),row(2,'cdq',('eax',),('eax','edx')),row(3,'idiv',('eax','edx','ecx'),('eax','edx'),(reg('ecx'),))],[[1,2],[2,3]]
class ArchitectureSources(unittest.TestCase):
    def test_eax_preserved(self):
        rows,es=graph();self.assertEqual(reaches(rows,es,1,'eax')[3],{('definition',1)})
    def test_decoder_observation_retained(self):
        rows,es=graph();before=copy.deepcopy(rows);self.assertEqual(reaches(rows,es,1,'eax',False)[3],{('definition',2)});self.assertEqual(rows,before)
    def test_edx_sign_extension_definition(self):
        rows,es=graph();self.assertEqual(reaches(rows,es,1,'edx')[3],{('definition',2)})
    def test_correct_decoder_cdq(self):self.assertTrue(cdq(row(1,'cdq',('eax',),('edx',))))
    def test_cwd_not_cdq(self):self.assertFalse(cdq(row(1,'cwd',('eax',),('eax','edx'))))
    def test_cqo_not_cdq(self):self.assertFalse(cdq(row(1,'cqo',('eax',),('eax','edx'))))
    def test_unexpected_cdq_operand(self):self.assertFalse(cdq(row(1,'cdq',('eax',),('eax','edx'),[imm(1)])))
    def test_cdq_extra_write(self):self.assertFalse(cdq(row(1,'cdq',('eax',),('eax','edx','ecx'))))
    def test_cdq_extra_read(self):self.assertFalse(cdq(row(1,'cdq',('eax','ebx'),('eax','edx'))))
    def test_partial_parent_dependency(self):self.assertEqual(reads(row(1,'mov',(),('al',),(reg('al',1,False,True),imm(1)))),['eax'])
    def test_literal_assignment_no_input(self):self.assertEqual(reads(graph()[0][0]),[])
    def test_opaque_call(self):
        rows,es=graph();rows[1]=row(2,'call');self.assertEqual(reaches(rows,es,1,'eax')[3],{('unknown_call',2)})
    def test_far_call(self):
        rows,es=graph();rows[1]=row(2,'lcall');self.assertEqual(reaches(rows,es,1,'eax')[3],{('unknown_call',2)})
    def test_partial_write_kills_whole_register_value(self):
        rows,es=graph();rows[1]=row(2,'mov',(),('al',));self.assertEqual(reaches(rows,es,1,'eax')[3],{('definition',2)})
    def test_branch_join(self):
        rows=[row(1,'jne'),row(2,'mov',(),('eax',)),row(3,'mov',(),('eax',)),row(4,'nop')];es=[[1,2],[1,3],[2,4],[3,4]]
        self.assertEqual(reaches(rows,es,1,'eax')[4],{('definition',2),('definition',3)})
    def test_loop_reaches_fixed_point(self):
        rows=[row(1,'nop'),row(2,'inc',('eax',),('eax',)),row(3,'jmp')];es=[[1,2],[2,3],[3,2]];self.assertEqual(reaches(rows,es,1,'eax')[2],{('entry',1),('definition',2)})
    def test_bad_root(self):
        rows,es=graph()
        with self.assertRaises(ValueError):reaches(rows,es,9,'eax')
    def test_bad_register(self):
        rows,es=graph()
        with self.assertRaises(ValueError):reaches(rows,es,1,'esp')
    def test_missing_edge_endpoint(self):
        rows,es=graph()
        with self.assertRaises(ValueError):reaches(rows,es+[[3,9]],1,'eax')
    def test_duplicate_site(self):
        rows,es=graph()
        with self.assertRaises(ValueError):reaches(rows+[rows[0]],es,1,'eax')
    def test_focus_cap_remains_explicit(self):
        rows,es=graph();maps={r:reaches(rows,es,1,r) for r in REGS};s=focus(rows,maps,[(3,'edx')],cap=1)
        self.assertTrue(s['query_limit_hit']);self.assertFalse(s['graph_local_dependency_queries_closed']);self.assertEqual(s['pending_queries'],[{'site_rva':2,'register':'eax'}])
    def test_closed_focus(self):
        rows,es=graph();maps={r:reaches(rows,es,1,r) for r in REGS};s=focus(rows,maps,[(3,'edx')]);self.assertFalse(s['query_limit_hit']);self.assertEqual([r['site_rva'] for r in s['definition_shapes']],[1,2])
    def test_invalid_focus_bound(self):
        for cap in (0,193,True):
            with self.assertRaises(ValueError):focus([],{},[],cap)
    def test_forward_reverse_random_graphs(self):
        rng=random.Random(52)
        choices=[('nop',(),()),('mov',(),('eax',)),('mov',(),('edx',)),('mov',(),('al',)),('cdq',('eax',),('eax','edx')),('call',(),()),('inc',('ecx',),('ecx',))]
        for _ in range(30):
            rows=[row(i+1,*rng.choice(choices)) for i in range(7)];es=[[i,i+1] for i in range(1,7)]+[[rng.randrange(1,8),rng.randrange(1,8)] for _ in range(8)]
            for arch in (True,False):
                for r in ('eax','edx','ecx'):
                    m=reaches(rows,es,1,r,arch)
                    for a in range(1,8):self.assertEqual(m.get(a,set()),reverse_sources(rows,es,1,a,r,arch))
class PinnedReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=Path('research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ORIGINAL.json').read_bytes();cls.report=derive(cls.raw)
    def reject(self,fn):
        d=copy.deepcopy(self.report);fn(d)
        with self.assertRaises(ValueError):strict_validate(d,self.raw)
    def test_valid_independent_reverse(self):self.assertEqual(strict_validate(self.report,self.raw),46)
    def test_wrong_digest(self):
        with self.assertRaises(ValueError):derive(self.raw+b' ')
    def test_source_schema(self):
        d=json.loads(self.raw);d['schema']='wrong';raw=json.dumps(d).encode()
        with self.assertRaises(ValueError):derive(raw,hashlib.sha256(raw).hexdigest())
    def test_source_promotion(self):
        d=json.loads(self.raw);d['native_io_executed']=True;raw=json.dumps(d).encode()
        with self.assertRaises(ValueError):derive(raw,hashlib.sha256(raw).hexdigest())
    def test_all_seven_dividend_shapes(self):self.assertTrue(all(c['conditional_sign_extended_eax_dividend_syntax_qualified'] for c in self.report['analysis']['signed_division_contexts']))
    def test_focused_groups_closed(self):self.assertTrue(all(not c['source_graph']['query_limit_hit'] and c['source_graph']['graph_local_dependency_queries_closed'] for c in self.report['analysis']['signed_division_contexts']))
    def test_legacy_sample_complete(self):self.assertEqual(len(self.report['analysis']['r51_legacy_definition_shapes_complete']),39)
    def test_pending_shapes_complete(self):self.assertEqual(len(self.report['analysis']['r51_pending_definition_shapes']),11)
    def test_promotion(self):
        for k in FLAGS:self.reject(lambda d,k=k:d.update({k:True}))
    def test_cdq_decoder_observation(self):self.reject(lambda d:d['analysis']['cdq_architecture_overlays'][0]['decoder_observation'].update(decoder_written_registers=['edx']))
    def test_quotient_remainder_swap(self):self.reject(lambda d:d['analysis']['signed_division_contexts'][0].update(architecture_quotient_register='edx'))
    def test_source_fabrication(self):self.reject(lambda d:d['analysis']['signed_division_contexts'][0]['qualified_eax_source_candidates'][0].update(site_rva=0))
    def test_pending_query_hidden(self):self.reject(lambda d:d['analysis']['signed_division_contexts'][0]['source_graph'].update(query_limit_hit=True))
    def test_false_closure(self):self.reject(lambda d:d['analysis']['signed_division_contexts'][0]['source_graph'].update(actual_memory_closure_or_values_proven=True))
    def test_legacy_row_missing(self):self.reject(lambda d:d['analysis']['r51_legacy_definition_shapes_complete'].pop())
    def test_flag_execution(self):self.reject(lambda d:d['analysis']['processor_predicate_contexts'][0].update(actual_flags_path_feasibility_or_loop_iterations_proven=True))
    def test_output_alias(self):self.reject(lambda d:d['analysis']['conditional_output_store_context'].update(actual_read_count_minus_one_length_output_contents_or_alias_proven=True))
    def test_type_confusion(self):self.reject(lambda d:d.update(static_only=1))
if __name__=='__main__':unittest.main()
