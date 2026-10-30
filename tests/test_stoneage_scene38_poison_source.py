"""Synthetic markup/cross-source counterexamples; no original page fixture."""
import copy
import json
import unittest
from tools import stoneage_scene38_poison_source as m


def synthetic(reduction=50,turns=5,price='4000'):
    return ('<title>石器时代2.0</title><table><tr><td>技能名称</td><td>技能说明</td><td>技能价格</td></tr>'
            '<tr><td>猛毒攻击</td><td>攻击力降低'+str(reduction)+'%，造成敌方'+str(turns)+'回合中毒状态</td>'
            '<td><img src="unread-unit.gif">'+price+'</td></tr></table>').encode('gb18030')


class SelectedRowParsing(unittest.TestCase):
    def test_numeric_fields_actually_come_from_synthetic_row(self):
        x=m.extract_skill(synthetic(27,8,'1357'))
        self.assertEqual((x['attack_reduction_percent_as_text'],x['poison_turns_as_text'],x['listed_price']),(27,8,1357))

    def test_price_icon_filename_does_not_prove_currency(self):
        self.assertIsNone(m.extract_skill(synthetic())['price_currency'])

    def test_target_must_be_unique(self):
        s=synthetic().decode('gb18030');row=s[s.index('<tr><td>猛毒'):s.index('</table>')]
        with self.assertRaises(ValueError):m.extract_skill(s.replace('</table>',row+'</table>').encode('gb18030'))

    def test_price_cannot_be_borrowed_from_next_row(self):
        s=synthetic().decode('gb18030').replace('<td><img src="unread-unit.gif">4000</td>','')
        s=s.replace('</table>','<tr><td>别行</td><td>4000</td></tr></table>')
        with self.assertRaises(ValueError):m.extract_skill(s.encode('gb18030'))

    def test_blank_price_remains_missing_not_zero(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic(price=''))

    def test_header_order_cannot_be_reversed(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic().replace('技能价格'.encode('gb18030'),'另列'.encode('gb18030')))

    def test_duplicate_header_is_ambiguous(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic()+synthetic())

    def test_changed_skill_name_not_alias_merged(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic().replace('猛毒攻击'.encode('gb18030'),'毒攻击'.encode('gb18030')))

    def test_script_cannot_supply_effect(self):
        s=synthetic().decode('gb18030').replace('攻击力降低50%，造成敌方5回合中毒状态','<script>攻击力降低50%，造成敌方5回合中毒状态</script>')
        with self.assertRaises(ValueError):m.extract_skill(s.encode('gb18030'))

    def test_target_outside_skill_table_cannot_supply_row(self):
        s=synthetic().decode('gb18030');a=s.index('<tr><td>猛毒');row=s[a:s.index('</table>')];s=s[:a]+'</table><table>'+row+'</table>'
        with self.assertRaises(ValueError):m.extract_skill(s.encode('gb18030'))

    def test_percent_must_be_within_source_field_domain(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic(150))

    def test_turn_count_cannot_be_zero(self):
        with self.assertRaises(ValueError):m.extract_skill(synthetic(turns=0))

    def test_unclosed_selected_cell_rejected(self):
        s=synthetic().decode('gb18030').replace('4000</td>','4000')
        with self.assertRaises(ValueError):m.extract_skill(s.encode('gb18030'))

    def test_nonselected_legacy_bad_cells_are_not_repaired_or_exported(self):
        s=synthetic().decode('gb18030').replace('</table>','<tr><td>其它旧行</tr></table>')
        self.assertEqual(m.extract_skill(s.encode('gb18030'))['listed_price'],4000)

    def test_entry_links_require_literal_pair(self):
        h=('<a href="'+m.HREF+'">宠物技能</a>').encode('gb18030')
        self.assertEqual(m.extract_entry(h)['href'],m.HREF)
        with self.assertRaises(ValueError):m.extract_entry(h.replace(b'skill.asp',b'other.asp'))

    def test_duplicate_entry_link_rejected(self):
        h=('<a href="'+m.HREF+'">宠物技能</a>').encode('gb18030')
        with self.assertRaises(ValueError):m.extract_entry(h+h)

    def test_synthetic_HTML_cannot_pass_original_source_SHA_gate(self):
        with self.assertRaises(ValueError):m.source_projection({'facility':b'', 'skill':synthetic()})


class AttributionBoundaries(unittest.TestCase):
    def setUp(self):self.r=json.loads(m.REPORT.read_bytes())
    def bad(self,f):
        r=copy.deepcopy(self.r);f(r)
        with self.assertRaises(ValueError):m.validate(r)

    def test_prior_bytes_and_current_attribution(self):
        self.assertEqual(m.validate(self.r)['new_webpages'],0)

    def test_existing_page_not_recounted_as_new_discovery(self):
        self.bad(lambda r:r['novelty'].update(new_webpages_discovered=1))

    def test_currency_not_filled_from_later_page(self):
        self.bad(lambda r:r['source_projection']['skill'].update(price_currency='STONE'))

    def test_SBC_location_not_backfilled(self):
        self.bad(lambda r:r['source_projection']['skill'].update(trainer_location='SBC'))

    def test_price_not_MP_or_native_debit(self):
        for key in ['price_verified_as_combat_MP_cost','price_verified_as_training_debit']:
            with self.subTest(key=key):self.bad(lambda r:r['unproven'].update({key:True}))

    def test_later_conflict_not_silently_resolved(self):
        self.bad(lambda r:r['comparison_to_existing_R56_only_not_reacquired_portal_HTML'].update(old_conflict_is_resolved=True))

    def test_capture_does_not_date_another_page(self):
        self.bad(lambda r:r['comparison_to_existing_R56_only_not_reacquired_portal_HTML'].update(undated_S2_publication_date_inherited_from_S0='2001-12-04'))

    def test_earlier_capture_not_balance_patch_proof(self):
        self.bad(lambda r:r['unproven'].update(balance_patch_history_recovered=True))

    def test_no_prior_input_removed(self):
        self.bad(lambda r:r['prior_materials'].pop())

    def test_no_runtime_or_restoration_percentage(self):
        self.bad(lambda r:r['unproven'].update(original_world_entered=True))
        self.bad(lambda r:r.update(overall_percent=99))


if __name__=='__main__':unittest.main()
