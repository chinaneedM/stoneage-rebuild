"""Synthetic source-layout counterexamples; no original webpage fixture in Git."""
import copy
import json
import unittest
from tools import stoneage_scene37_newbie_quest as m


def row(cells):
    return '<tr>'+''.join('<td>'+x+'</td>' for x in cells)+'</tr>'


def synthetic_2004():
    rows=[row(['手骑宠跳级任务','','','']), row(['任务条件：３０级','以下新人','',''])]
    rows += [row([str(i)+'.合成','','','']) for i in range(1,10)]
    rows += [row(['１０．这个任务只','合成','',''])]
    return ''.join(rows).encode()


def section_2006():
    return '任务条件：刚出生的1级人'+''.join(str(i)+'.合成' for i in range(1,10))+'10.能力值约是野生的一半'


def synthetic_2006():
    s=section_2006()
    return ('<div id="news">'+s+'<div>重复语境</div>'+s+'</div>').encode()


class SourceLayout(unittest.TestCase):
    def test_line_major_reading_differs_from_DOM_cell_major(self):
        s=synthetic_2004().decode().replace('<td>1.合成</td><td></td>', '<td>1.甲<br>乙</td><td>丙<br>丁</td>')
        self.assertEqual(m.extract_2004(s.encode())['normalized_steps'][0], '1.甲丙乙丁')

    def test_2004_all_ten_rows(self):
        self.assertEqual(len(m.extract_2004(synthetic_2004())['normalized_steps']),10)

    def test_missing_column_rejected(self):
        with self.assertRaises(ValueError):m.extract_2004(synthetic_2004().replace(b'<td></td>',b'',1))

    def test_duplicate_heading_rejected(self):
        b=synthetic_2004()
        with self.assertRaises(ValueError):m.extract_2004(b+b)

    def test_repairing_missing_heading_character_rejected(self):
        with self.assertRaises(ValueError):m.extract_2004(synthetic_2004().replace('手骑宠'.encode(),'新手骑宠'.encode()))

    def test_extra_step_rejected(self):
        s=synthetic_2004().decode().replace('<td>１０．',row(['合成','','',''])+'<td>１０．')
        with self.assertRaises(ValueError):m.extract_2004(s.encode())

    def test_script_in_selected_source_rejected(self):
        s=synthetic_2004().replace(b'<td>1.',b'<td><script>0</script>1.')
        with self.assertRaises(ValueError):m.extract_2004(s)

    def test_hidden_font_requires_new_review(self):
        s=synthetic_2004().replace(b'<td>1.',b'<td><font color="white">0</font>1.')
        with self.assertRaises(ValueError):m.extract_2004(s)

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(UnicodeDecodeError):m.extract_2004(synthetic_2004()+b'\xff')

    def test_literal_replacement_character_rejected(self):
        with self.assertRaises(ValueError):m.extract_2004(synthetic_2004()+'\ufffd'.encode())

    def test_2006_keeps_two_internal_occurrences(self):
        self.assertEqual(m.extract_2006(synthetic_2006())['identical_selected_section_occurrences'],2)

    def test_2006_single_occurrence_is_not_silently_accepted(self):
        s='<div id="news">'+section_2006()+'</div>'
        with self.assertRaises(ValueError):m.extract_2006(s.encode())

    def test_2006_changed_second_occurrence_rejected(self):
        s='<div id="news">'+section_2006()+section_2006().replace('1.合成','1.变异')+'</div>'
        with self.assertRaises(ValueError):m.extract_2006(s.encode())

    def test_2006_footer_or_script_cannot_supply_duplicate(self):
        s='<div id="news">'+section_2006()+'<script>'+section_2006()+'</script></div>'+section_2006()
        with self.assertRaises(ValueError):m.extract_2006(s.encode())

    def test_duplicate_article_container_rejected(self):
        with self.assertRaises(ValueError):m.extract_2006(synthetic_2006()+synthetic_2006())

    def test_NFKC_does_not_rewrite_species_or_bad_heading(self):
        self.assertEqual(m.compact(' 布依　３０ '),'布依30')
        self.assertNotEqual(m.compact('布依'),'布伊')


class DocumentaryLimits(unittest.TestCase):
    def setUp(self):self.r=json.loads(m.REPORT.read_bytes())

    def bad(self, mutate):
        r=copy.deepcopy(self.r);mutate(r)
        with self.assertRaises(ValueError):m.validate(r)

    def test_current_source_pins_and_semantics(self):
        self.assertEqual(m.validate(self.r)['documentary_quest_chains'],1)

    def test_official_deployment_not_proven(self):
        self.bad(lambda r:r['unproven'].update(official_plan_deployment_proven=True))

    def test_task_cannot_be_promoted_to_base_or_permanent_or_event(self):
        for origin in ['BASE_GAME_QUEST','PERMANENT_VERSION_QUEST','OPERATOR_EVENT_QUEST']:
            with self.subTest(origin=origin):self.bad(lambda r:r['quest'].update(origin_class=origin))

    def test_31_is_destination_level_not_exact_XP(self):
        self.bad(lambda r:r['quest'].update(server_XP_amounts=[10,20,31]))

    def test_recipe_3_not_invented_quantity(self):
        self.bad(lambda r:r['quest']['flow'][1].update(recipe_numbers_are_quantities_or_grades='QUANTITY_3'))

    def test_pet_name_not_silently_corrected(self):
        self.bad(lambda r:r['quest']['flow'][2].update(source_pet_label='布伊'))

    def test_level30_boundary_remains_unresolved(self):
        self.bad(lambda r:r['quest']['qualification_disagreement'].update(level30_inclusive=True))

    def test_repeated_sources_not_independent_witnesses(self):
        self.bad(lambda r:r['novelty'].update(independent_server_witnesses=2))

    def test_prior_source_cannot_be_removed(self):
        self.bad(lambda r:r['prior_materials'].pop())

    def test_step_hash_mutation_rejected(self):
        self.bad(lambda r:r['source_projection']['player2004']['normalized_step_sha256'].__setitem__(0,'0'*64))

    def test_no_completion_percentage(self):
        self.bad(lambda r:r.update(overall_percent=95))

    def test_publication_labels_not_original_publication_bytes(self):
        self.bad(lambda r:r['unproven'].update(original_publication_bytes_verified=True))


if __name__=='__main__':unittest.main()
