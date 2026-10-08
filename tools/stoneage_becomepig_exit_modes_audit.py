"""Bounded whole Exit caller: PvE/PvP/WATCH type and player/pet/enemy.

Original C remains transient. WATCH means the typed Exit caller only, not the
watch-link/Finish coordinator. Enemy destruction is an observed retained-slot
hook, not an implementation of original memory lifetime.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

from tools import stoneage_becomepig_lookup_audit as lookup
from tools import stoneage_becomepig_badstatus_audit as badstatus
from tools import stoneage_becomepig_restore_audit as restore
from tools.stoneage_becomepig_hp_death_audit import verify_identity
from tools.stoneage_becomepig_native_audit import _assert_rows
from tools.stoneage_guard_break2_source_audit import PINNED

RESOLUTION = 'BECOMEPIG_BOUNDED_PVP_WATCH_TYPED_ENEMY_EXIT_PASS_ZERO_RUNTIME_PROMOTIONS'
FLAG_NAMES = ('ISDUEL', 'ISPARTY', 'ISPARTYCHAT', 'ISTRADECARD', 'ISTELL',
              'ISFM', 'ISOCC', 'ISCHAT', 'ISSAVE')
FS_NAMES = ('DUEL', 'PARTY', 'PARTYCHAT', 'TRADECARD', 'TELL', 'FM', 'OCC', 'CHAT', 'SAVE')


def fs_mask(profile, flagbits, c):
    # Exit clears DUEL before composing FS. Bismarck emits only the first four.
    return sum(c['CHAR_FS_' + FS_NAMES[j]] for j in range(1, 4 if profile == 'bismarck' else 9)
               if flagbits & (1 << j))


def vectors():
    rows = set()
    def add(kind, mode, side, pos, hp=150, dead=0, pig=180, fox=-1,
            mask=3, owned=1, flagbits=0, guards=(1, 1, 1)):
        # Build a valid base fixture before explicitly expanding actor kind.
        v = list(lookup.fixture(action=1, side=side, pos=min(pos, 4), pig=pig,
                                fox=fox, dead=dead, pointermask=mask, owned=owned))
        v[1:4] = guards
        v[5], v[11] = pos, kind
        rows.add((*v, mode, hp, flagbits))
    # All safe slots: player i+5 accesses require player slot0..4.
    for kind in (1, 2, 3):
        positions = [(-1, 0)] + list(itertools.product((0, 1), range(5 if kind == 1 else 10)))
        for mode, (side, pos), hp, dead, pig, fox, mask, owned in itertools.product(
            (1, 2, 3), positions, (0, 1, 2, 150), (0, 1), (-1, 180),
            (-1, 2), range(4), (0, 1),
        ):
            add(kind, mode, side, pos, hp, dead, pig, fox, mask, owned)
    # Exhaust all nine independent flags for all battle types and both sides.
    for mode, (side, pos), flags in itertools.product((1, 2, 3), ((0, 0), (1, 4)), range(512)):
        add(1, mode, side, pos, flagbits=flags)
    # Invalid actor/battle and unused-battle checks precede membership cleanup.
    for kind, mode, guards, pig, fox in itertools.product(
        (1, 2, 3), (1, 2, 3), ((0, 1, 1), (1, 0, 1), (1, 1, 0)), (-1, 180), (-1, 2),
    ):
        add(kind, mode, 1, 4, pig=pig, fox=fox, guards=guards)
    return sorted(rows)


class Witness(lookup.Witness):
    def __init__(self, profile, c, case, tables, features, domain):
        v = list(case[:25])
        pos = v[5]
        v[5] = min(pos, 4)
        super().__init__(profile, c, v, tables, features, domain)
        self.v = case[:25]
        self.mode, hp, self.flagbits = case[25:]
        self.i['CHAR_HP'] = hp
        for j, name in enumerate(FLAG_NAMES):
            self.f['CHAR_' + name] = (self.flagbits >> j) & 1
        if case[11] != 1:
            self.entries = [[-1]*10, [-1]*10]
            self.escapes = [[0]*10, [0]*10]
            if case[4] >= 0:
                self.entries[case[4]][pos] = 0
                self.escapes[case[4]][pos] = 7

    def event(self, code, actor, value=0):
        # Existing independent player oracle is shared only for player branch.
        # Inject the separate PvP oracle at the ordered pre-XYD boundary.
        if code == 29 and actor == 0 and self.mode == 2:
            self.f['CHAR_ISDUEL'] = 0
            super().event(30, 0, fs_mask(self.name, self.flagbits, self.c))
        super().event(code, actor, value)

    def execute(self):
        if self.i['CHAR_WHICHTYPE'] == 1:
            return super().execute()
        _, vc, vb, use, side, pos, *_ = self.v
        if not vc:
            return -101
        if not vb:
            return -102
        if self.i['CHAR_BASEIMAGENUMBER'] == 101749 or self.w['CHAR_WORKFOXROUND'] != -1:
            self.setint(0, 'CHAR_BASEIMAGENUMBER', self.i['CHAR_BASEBASEIMAGENUMBER'])
            self.w['CHAR_WORKFOXROUND'] = -1
        if not use:
            return -103
        if side >= 0:
            self.entries[side][pos] = -1
            self.escapes[side][pos] = 0
            self.w['CHAR_WORKBATTLEMODE'] = 2
            self.w['CHAR_WORKBATTLEINDEX'] = -1
            if self.i['CHAR_WHICHTYPE'] == 3:
                self.event(31, 0)
        self.event(26, 0)
        return 0

    def row(self, result):
        row = list(super().row(result))
        index = len(row) - len(self.trace) - 1
        return tuple(row[:index] + [self.f['CHAR_' + name] for name in FLAG_NAMES] + row[index:])


def native_source(source):
    for old, new in (
        ('int main(void){int action,vc,vb,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall;',
         'int main(void){int mode,hp,flagbits;int action,vc,vb,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall;'),
        ('%d'*25+'"', '%d'*28+'"'),
        ('&learn,&belt)==25)', '&learn,&belt,&mode,&hp,&flagbits)==28)'),
        ('BattleArray[0].type=1;', 'BattleArray[0].type=mode;'),
        ('ints[i][CHAR_HP]=i==0?150:40;', 'ints[i][CHAR_HP]=i==0?hp:40;'),
        ('BattleArray[0].Side[side].Entry[pos+5].charaindex=1;BattleArray[0].Side[side].Entry[pos+5].char_index=1;',
         'if(kind==CHAR_TYPEPLAYER){BattleArray[0].Side[side].Entry[pos+5].charaindex=1;BattleArray[0].Side[side].Entry[pos+5].char_index=1;}'),
        (' int result;if(action>=2)',
         '\n' + ''.join('flags[0][CHAR_'+name+']=(flagbits>>'+str(j)+')&1;' for j,name in enumerate(FLAG_NAMES)) + '\n int result;if(action>=2)'),
        (' printf(" %d",nt);',
         ''.join('printf(" %d",flags[0][CHAR_'+name+']);' for name in FLAG_NAMES) + ' printf(" %d",nt);'),
    ):
        source = lookup.replace_once(source, old, new)
    return source


def audit(profile, root):
    root = root.resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip()
    if head != PINNED[profile] or dirty:
        raise ValueError(profile + ': pinned source tree drift')
    domain = lookup.source_domain(profile, root)
    verify_identity(domain['identity'], lookup.PIN_PATH, profile)
    body, tables, identity = badstatus.source_domain(profile, root)
    verify_identity(identity, badstatus.PIN_PATH, profile)
    functions, callers = restore.original_functions(profile, root)
    verify_identity(callers, lookup.PIN_PATH.parent / 'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json', profile, functions=True)
    c = lookup.handles(functions, body, tables, identity['features'], domain)
    # Absent profile flags are harness-only state; no original ordinals inferred.
    for j, name in enumerate(FLAG_NAMES):
        c.setdefault('CHAR_' + name, 470 + j)
    cases = vectors()
    expected = []
    for case in cases:
        w = Witness(profile, c, case, tables, identity['features'], domain)
        result = w.execute()
        codes = w.trace[::3]
        matched = all(case[1:4]) and case[4] >= 0
        player = case[11] == 1
        if codes.count(31) != int(matched and case[11] == 3):
            raise ValueError('independent enemy destruction hook invariant drift')
        if codes.count(30) != int(matched and player and case[25] == 2):
            raise ValueError('independent PvP FS callback invariant drift')
        if not player and any(code in codes for code in (20, 21, 22, 24, 25, 27, 28, 29, 30)):
            raise ValueError('nonplayer incorrectly entered player cleanup')
        expected.append(w.row(result))
    source = native_source(lookup.native_composition(profile, functions, body, tables, identity['features'], c, domain))
    payload = ''.join(' '.join(map(str, v)) + '\n' for v in cases)
    for opt in ('-O0', '-O2'):
        _assert_rows(restore.run_native(source, payload, opt), expected, profile + ' exit modes')
    return dict(profile=profile, source_sha=head, cases_per_optimization=len(cases),
                native_comparisons=len(cases)*2,
                semantic_sha256=hashlib.sha256(json.dumps(expected, separators=(',', ':')).encode()).hexdigest())


def main():
    parser = argparse.ArgumentParser()
    for profile in PINNED:
        parser.add_argument('--'+profile+'-dir', type=Path, required=True)
    args = parser.parse_args()
    total = 0
    for profile in PINNED:
        row = audit(profile, getattr(args, profile+'_dir'))
        total += row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()), flush=True)
    print(f'TOTAL|exit_modes_comparisons={total}|profiles=3')
    print('FACT|matched_PvP_player_clears_DUEL_before_FS_then_XYD_Bismarck_four_flags_gavin_iris_nine')
    print('FACT|WATCH_typed_Exit_retains_player_cleanup_without_PvP_FS_not_watch_link_or_Finish_acceptance')
    print('FACT|matched_enemy_calls_destruction_hook_pet_does_not_neither_enters_player_cleanup')
    print('BOUNDARY|all_safe_entry_positions_single_membership_symbolic_ABI_controlled_retained_enemy_slot_stats_property_ownership_network_timing')
    print('OPEN|actual_enemy_deallocation_post_destroy_lifetime_watch_link_Finish_multi_pet_actual_ownership_stat_property_timer_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__ == '__main__':
    main()
