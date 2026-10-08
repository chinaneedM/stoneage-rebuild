"""Bounded player HP/death witnesses through complete original restoration callers.

Reuse accepted actual lookup/status maps and complete caller extraction. Only
the independent witness's initial player HP varies; original C stays transient.
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
from tools.stoneage_becomepig_native_audit import _assert_rows
from tools.stoneage_guard_break2_source_audit import PINNED

RESOLUTION = "BECOMEPIG_BOUNDED_PLAYER_HP_DEATH_FULL_CALLER_PASS_ZERO_RUNTIME_PROMOTIONS"


def exit_timing_extra_argument(profile: str, hp: int, dead: int) -> int:
    """CheckDefBTime final argument; HP is the caller's already capped HP."""
    return 10 if dead or (profile != "bismarck" and hp == 1) else 0


def vectors():
    for action, hp, dead, pig, mask, owned, meta, side, pos in itertools.product(
        (0, 1), (0, 1, 2, 150), (0, 1), (-1, 0, 180), range(4),
        (0, 1), range(4), (0, 1), (0, 4),
    ):
        yield (*lookup.fixture(
            action=action, dead=dead, pig=pig, pointermask=mask,
            owned=owned, meta=meta, side=side, pos=pos,
        ), hp)


def native_source(source: str) -> str:
    # Fail closed if any inherited harness seam changes.
    for old, new in (
        ('int main(void){int action,vc,vb,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall;',
         'int main(void){int playerhp;int action,vc,vb,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall;'),
        ('%d' * 25 + '"', '%d' * 26 + '"'),
        ('&learn,&belt)==25)', '&learn,&belt,&playerhp)==26)'),
        ('ints[i][CHAR_HP]=i==0?150:40;', 'ints[i][CHAR_HP]=i==0?playerhp:40;'),
    ):
        source = lookup.replace_once(source, old, new)
    return source


def verify_identity(actual, path: Path, profile: str, *, functions=False):
    expected = json.loads(path.read_text())['profiles'][profile]
    if functions:
        expected = expected['functions']
    if actual != expected:
        raise ValueError(profile + ': accepted source/default identity drift: ' + path.name)


def audit(profile: str, root: Path) -> dict:
    root = root.resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip()
    if head != PINNED[profile] or dirty:
        raise ValueError(profile + ': pinned source commit/tree drift')
    domain = lookup.source_domain(profile, root)
    verify_identity(domain['identity'], lookup.PIN_PATH, profile)
    body, tables, identity = badstatus.source_domain(profile, root)
    verify_identity(identity, badstatus.PIN_PATH, profile)
    functions, caller_identity = restore.original_functions(profile, root)
    verify_identity(caller_identity, lookup.PIN_PATH.parent / 'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json', profile, functions=True)
    c = lookup.handles(functions, body, tables, identity['features'], domain)
    cases = list(vectors())
    expected = []
    for case in cases:
        v, hp = case[:-1], case[-1]
        witness = lookup.Witness(profile, c, v, tables, identity['features'], domain)
        witness.i['CHAR_HP'] = hp
        result = witness.execute()
        # Independently certify the Exit branch's call argument, not only the
        # inherited full-state oracle. Every valid matched player Exit calls it.
        penalties = [witness.trace[i + 2] for i in range(0, len(witness.trace), 3)
                     if witness.trace[i] == 27]
        wanted = [exit_timing_extra_argument(profile, min(hp, 100), v[12])] if v[0] else []
        if penalties != wanted:
            raise ValueError(profile + ': independent HP/death timing oracle drift')
        expected.append(witness.row(result))
    source = native_source(lookup.native_composition(
        profile, functions, body, tables, identity['features'], c, domain,
    ))
    payload = ''.join(' '.join(map(str, case)) + '\n' for case in cases)
    for opt in ('-O0', '-O2'):
        _assert_rows(restore.run_native(source, payload, opt), expected, profile + ' HP/death complete callers')
    semantic_digest = hashlib.sha256(json.dumps(expected, separators=(',', ':')).encode()).hexdigest()
    return dict(profile=profile, source_sha=head, cases_per_optimization=len(cases),
                optimizations=2, native_comparisons=len(cases) * 2,
                hp1_without_death_exit_timing_extra_argument=exit_timing_extra_argument(profile, 1, 0),
                semantic_sha256=semantic_digest)


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
    print(f'TOTAL|player_hp_death_comparisons={total}|profiles=3')
    print('FACT|gavin_iris_HP1_without_death_flag_calls_exit_timing_extra_argument10_Bismarck_calls0')
    print('FACT|death_flag_calls_exit_timing_extra_argument10_then_player_death_clear_and_HP1_in_all_profiles')
    print('BOUNDARY|synthetic_player_HP0_1_2_150_and_death_flags_not_claimed_reachable_world_states')
    print('BOUNDARY|complete_original_compliance_exit_badstatus_actual_maps_helpers_controlled_stats_property_construct_timing_network_symbolic_ABI')
    print('OPEN|pet_death_follow_ownership_PvP_watch_enemy_invalid_rider_original_build_PRNG_and_runtime')
    print('RESOLUTION|' + RESOLUTION)


if __name__ == '__main__':
    main()
