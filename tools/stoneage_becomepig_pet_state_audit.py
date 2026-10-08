"""Original pet death/mail/follow/owned-slot/battle-occupancy composition R1.

Original C and maps stay transient. The accepted full-caller witness is expanded
with independent input/state handles; no historical field ordinals are chosen.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools import stoneage_becomepig_lookup_audit as lookup
from tools import stoneage_becomepig_badstatus_audit as badstatus
from tools import stoneage_becomepig_restore_audit as restore
from tools.stoneage_becomepig_hp_death_audit import verify_identity
from tools.stoneage_becomepig_native_audit import _assert_rows, _features
from tools.stoneage_guard_break2_source_audit import PINNED

RESOLUTION = "BECOMEPIG_BOUNDED_PET_DEATH_MAIL_FOLLOW_OWNERSHIP_PASS_ZERO_RUNTIME_PROMOTIONS"


def follow_result(follow, owner):
    # Two valid actors: player0, pet1. The roster is an independent input.
    if follow == -1:
        return follow, owner, ()
    if follow not in (0, 1):
        return -1, owner, ((40, 0, -1),)
    if follow == 1 and owner not in (0, 1):
        return 1, 0, ((40, 0, 1), (41, 1, 0))
    return follow, owner, ()


def pet_return(hp, dead, mail, roster_slot):
    if roster_slot < 0 or mail != 0:
        return hp, dead
    return (1, 0) if dead or hp <= 0 else (min(hp, 100), 0)


def vectors():
    for hp, dead, mail, follow, owner, slot, occupied, mask, pig, (side, pos) in itertools.product(
        (-2, 0, 1, 40, 150), (0, 1), (0, 1), (-1, 1, 2), (-1, 0),
        (-1, 0, 1, 2, 3, 4), (0, 1), range(4), (-1, 180), ((0, 0), (1, 4)),
    ):
        v = lookup.fixture(action=1, side=side, pos=pos, pig=pig,
                           pointermask=mask, owned=int(slot >= 0))
        yield (*v, hp, dead, mail, follow, owner, slot, occupied)


class Witness(lookup.Witness):
    def __init__(self, name, c, case, tables, features, domain):
        super().__init__(name, c, case[:25], tables, features, domain)
        hp, dead, mail, follow, owner, self.slot, self.occupied = case[25:]
        self.ints[1]['CHAR_HP'] = hp
        self.flags[1]['CHAR_ISDIE'] = dead
        self.ints[1]['CHAR_MAILMODE'] = mail
        self.w['CHAR_WORKPETFOLLOW'] = follow
        self.works[1]['CHAR_WORKPLAYERINDEX'] = owner
        if not self.occupied:
            self.entries[case[4]][case[5] + 5] = -1

    def event(self, code, actor, value=0):
        super().event(code, actor, value)
        if code == 3 and actor == 0:
            follow, owner, events = follow_result(
                self.w['CHAR_WORKPETFOLLOW'], self.works[1]['CHAR_WORKPLAYERINDEX'])
            self.w['CHAR_WORKPETFOLLOW'] = follow
            self.works[1]['CHAR_WORKPLAYERINDEX'] = owner
            for event in events:
                super().event(*event)

    def execute(self):
        # Independent caller oracle. Full original C runs without projection.
        side, pos = self.v[4:6]
        base = self.i['CHAR_BASEBASEIMAGENUMBER']
        petbase = self.ints[1]['CHAR_BASEBASEIMAGENUMBER']
        if self.i['CHAR_BECOMEPIG'] > -1:
            self.setint(0, 'CHAR_BASEIMAGENUMBER', 100388)
            self.compliance(0)
            self.event(20, 0)
            self.event(21, 0, self.c['CHAR_P_STRING_BASEBASEIMAGENUMBER'])
        self.event(28, 0)
        if self.name == 'bismarck':
            self.w['CHAR_WORKNOCAST'] = 0
        self.entries[side][pos] = -1
        self.escapes[side][pos] = 0
        self.w['CHAR_WORKBATTLEMODE'] = 2
        self.w['CHAR_WORKBATTLEINDEX'] = -1
        self.event(27, 0, 0)
        if self.occupied:
            self.entries[side][pos + 5] = -1
            self.works[1]['CHAR_WORKBATTLEMODE'] = 0
            self.works[1]['CHAR_WORKBATTLEINDEX'] = -1
        self.event(25, 0)
        self.compliance(0)
        self.event(24, 0)
        status = 0
        for key in ('HP', 'EXP', 'MP', 'DUELPOINT', 'CHARM', 'EARTH', 'WATER', 'FIRE', 'WIND', 'RIDEPET'):
            status |= self.c['CHAR_P_STRING_' + key]
        self.event(21, 0, status)
        if self.owned and self.ints[1]['CHAR_MAILMODE'] == 0:
            pet = self.ints[1]
            if self.flags[1]['CHAR_ISDIE'] or pet['CHAR_HP'] <= 0:
                self.flags[1]['CHAR_ISDIE'] = 0
                pet['CHAR_HP'] = 1
            self.works[1]['CHAR_WORKBATTLEMODE'] = 0
            if pet['CHAR_BASEIMAGENUMBER'] != petbase:
                self.setint(1, 'CHAR_BASEIMAGENUMBER', petbase)
                self.event(23, 0, ord('K'))
            self.event(25, 1)
            self.compliance(1)
            self.event(22, 0, self.slot)
        self.event(29, 0)
        self.event(26, 0)
        return 0

    def row(self, result):
        row = list(super().row(result))
        # Insert extra state before trace length. Parent row ends in length/trace.
        index = len(row) - len(self.trace) - 1
        return tuple(row[:index] + [
            self.ints[1]['CHAR_MAILMODE'], self.w['CHAR_WORKPETFOLLOW'],
            self.works[1]['CHAR_WORKPLAYERINDEX'],
        ] + row[index:])


def native_source(source):
    for old, new in (
        ('static int clearing,petpig,pointermask,owned,seed,base,pbase,petold,category,learn,belt,mappingactor;',
         'static int clearing,petpig,pointermask,owned,seed,base,pbase,petold,category,learn,belt,mappingactor,pethp,petdead,mail,follow,petowner,rosterslot,occupied;'),
        ('%d' * 25 + '"', '%d' * 32 + '"'),
        ('&learn,&belt)==25)', '&learn,&belt,&pethp,&petdead,&mail,&follow,&petowner,&rosterslot,&occupied)==32)'),
        ('return owned&&i==0&&slot==0?1:-1;', 'return owned&&i==0&&slot==rosterslot?1:-1;'),
        ('i=checked(i);works[i][f]=v;if(clearing)event(35,i,f);',
         'i=checked(i);works[i][f]=v;if(clearing)event(35,i,f);else if(f==CHAR_WORKPETFOLLOW)event(40,i,v);else if(f==CHAR_WORKPLAYERINDEX)event(41,i,v);'),
        (' int result;if(action>=2)', '''
 ints[1][CHAR_HP]=pethp;flags[1][CHAR_ISDIE]=petdead;
 ints[1][CHAR_MAILMODE]=mail;
 works[0][CHAR_WORKPETFOLLOW]=follow;works[1][CHAR_WORKPLAYERINDEX]=petowner;
 if(!occupied){BattleArray[0].Side[side].Entry[pos+5].charaindex=-1;BattleArray[0].Side[side].Entry[pos+5].char_index=-1;}
 int result;if(action>=2)'''),
        (' printf(" %d",nt);', ' printf(" %d %d %d",ints[1][CHAR_MAILMODE],works[0][CHAR_WORKPETFOLLOW],works[1][CHAR_WORKPLAYERINDEX]); printf(" %d",nt);'),
    ):
        source = lookup.replace_once(source, old, new)
    return source


def audit(profile, root):
    root = root.resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip()
    if head != PINNED[profile] or dirty:
        raise ValueError(profile + ': pinned source tree drift')
    if '_PETFOLLOW_NEW_' in _features(profile, root):
        raise ValueError(profile + ': multiple-follow-pointer feature excluded')
    domain = lookup.source_domain(profile, root)
    verify_identity(domain['identity'], lookup.PIN_PATH, profile)
    body, tables, identity = badstatus.source_domain(profile, root)
    verify_identity(identity, badstatus.PIN_PATH, profile)
    functions, callers = restore.original_functions(profile, root)
    verify_identity(callers, lookup.PIN_PATH.parent / 'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json', profile, functions=True)
    if re.search(r'CHAR_WORKPETFOLLOW\s*\+', functions[0]):
        raise ValueError(profile + ': arithmetic follow topology excluded')
    c = lookup.handles(functions, body, tables, identity['features'], domain)
    cases = list(vectors())
    expected = []
    for case in cases:
        w = Witness(profile, c, case, tables, identity['features'], domain)
        result = w.execute()
        hp, dead, mail, follow, owner, slot, occupied = case[25:]
        wanted_hp, wanted_dead = pet_return(hp, dead, mail, slot)
        if (w.ints[1]['CHAR_HP'], w.flags[1]['CHAR_ISDIE']) != (wanted_hp, wanted_dead):
            raise ValueError('independent pet return invariant drift')
        wanted_follow, wanted_owner, _ = follow_result(follow, owner)
        if (w.w['CHAR_WORKPETFOLLOW'], w.works[1]['CHAR_WORKPLAYERINDEX']) != (wanted_follow, wanted_owner):
            raise ValueError('independent follow invariant drift')
        if w.ints[1]['CHAR_BECOMEPIG'] != (-1 if slot >= 0 and case[16] & 1 else case[15]):
            raise ValueError('owned-pet counter clearing does not respect property guard')
        expected.append(w.row(result))
    source = native_source(lookup.native_composition(profile, functions, body, tables, identity['features'], c, domain))
    payload = ''.join(' '.join(map(str, case)) + '\n' for case in cases)
    for opt in ('-O0', '-O2'):
        _assert_rows(restore.run_native(source, payload, opt), expected, profile + ' pet death/mail/follow/ownership')
    return dict(profile=profile, source_sha=head, cases_per_optimization=len(cases),
                native_comparisons=len(cases) * 2,
                semantic_sha256=hashlib.sha256(json.dumps(expected, separators=(',', ':')).encode()).hexdigest())


def main():
    parser = argparse.ArgumentParser()
    for profile in PINNED:
        parser.add_argument('--' + profile + '-dir', type=Path, required=True)
    args = parser.parse_args()
    total = 0
    for profile in PINNED:
        row = audit(profile, getattr(args, profile + '_dir'))
        total += row['native_comparisons']
        print('PROFILE|' + '|'.join(f'{k}={v}' for k, v in row.items()))
    print(f'TOTAL|pet_death_mail_follow_ownership_comparisons={total}|profiles=3')
    print('FACT|owned_nonmail_pet_death_flag_or_HP_nonpositive_normalizes_to_HP1_before_badstatus_compliance')
    print('FACT|mail_skips_owned_pet_restore_but_not_earlier_player_badstatus_owned_pet_pig_counter_clear')
    print('FACT|follow_pointer_invalid_cleared_valid_pet_invalid_owner_repaired_independently_from_roster')
    print('FACT|owned_slot_and_battle_occupancy_independent_no_default_selection_inferred')
    print('BOUNDARY|one_pet_two_valid_actors_single_follow_pointer_all_owned_slots_PvE_positions0_or4_controlled_stats_property_construct_network_timing_ABI')
    print('OPEN|actual_ownership_getter_follow_lifecycle_multi_pet_PvP_watch_enemy_invalid_rider_full_timer_original_build_PRNG_runtime')
    print('RESOLUTION|' + RESOLUTION)


if __name__ == '__main__':
    main()
