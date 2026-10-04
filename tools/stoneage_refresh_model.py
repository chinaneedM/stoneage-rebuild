"""Independent bounded Refresh reference; no ordered runtime admission yet.

Targets are an explicitly supplied, already resolved MultiList witness. Build
charsets are conditional source experiments, never recovered binary facts.
"""
from dataclasses import dataclass

CALLBACK_NAME = 'PETSKILL_Refresh'
COMMAND_NAME = 'BATTLE_COM_S_REFRESH'
FEATURE_NAME = '_SKILL_REFRESH'
SOURCE_PETSKILL_SYMBOL_NAME = 'PETSKILL_REFRESH'


class RefreshSourceDomain(ValueError):
    """Unproved source build, invalid witness, or unsafe original scan."""


# Independently named baseline status vocabulary. Only matches before the
# extended labels are admitted in the two profiles whose tables are short.
_BASELINE = {
    'gavin': ('全','毒','麻','眠','石','醉','乱','虚','剧','障','默'),
    'iris': ('全','毒','麻','眠','石','醉','亂','虛','劇','障','默'),
    'bismarck': ('NULL','中毒','麻痹','睡眠','石化','醉酒','混乱','虚弱','剧毒','障碍','沉默','瘟疫'),
}
PROFILE_FACTS = {
    'gavin': (44,32,50), 'iris': (44,32,50), 'bismarck': (12,12,46),
}
BUILD_CHARSETS = {
    'gavin': ('utf-8','gbk'), 'iris': ('utf-8','gbk','cp950'),
    'bismarck': ('utf-8','gbk'),
}


def _profile(profile):
    if profile not in PROFILE_FACTS:
        raise RefreshSourceDomain('unknown pinned profile')
    return PROFILE_FACTS[profile]


def parse_refresh_option(option, *, profile, execution_charset):
    """Match actual first two execution bytes, retaining UTF-8 collisions.

For short tables only an immediate baseline match is safe: a nonmatch scans
past the actual label array before moving to the next byte. Empty strings
return before the scan; NULL is dereferenced in every source profile.
"""
    end, count, _ = _profile(profile)
    if execution_charset not in BUILD_CHARSETS[profile]:
        raise RefreshSourceDomain('whole active label table cannot use this charset')
    if option is None:
        raise RefreshSourceDomain('source dereferences NULL OPTION')
    if not isinstance(option, bytes) or b'\0' in option:
        raise RefreshSourceDomain('requires non-NUL raw OPTION bytes')
    if not option:
        return None
    labels = tuple(label.encode(execution_charset)[:2] for label in _BASELINE[profile])
    for offset in range(len(option)):
        prefix = option[offset:offset+2]
        for status, label in enumerate(labels):
            if prefix == label:
                return status
        if count < end:
            raise RefreshSourceDomain('no admitted leading marker; original short-table scan unsafe')
    return None


def _int32(value):
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise RefreshSourceDomain('requires signed int32 witness')
    return value


@dataclass(frozen=True)
class RefreshSetup:
    target_slot: int
    packed_com3: int
    command_name: str = COMMAND_NAME
    mode_name: str = 'BATTLE_CHARMODE_C_OK'
    source_return_value: bool = True


def resolve_refresh_setup(*, target_slot, skill_array, packed_com3_before):
    _int32(target_slot); _int32(skill_array); _int32(packed_com3_before)
    packed = (packed_com3_before & 0xffff0000) | (skill_array & 0xffff)
    if packed >= 2**31:
        packed -= 2**32
    return RefreshSetup(target_slot, packed)


@dataclass(frozen=True)
class RefreshResolution:
    source_return_value: bool
    receive_effect_name: str | None
    target_counters: tuple[tuple[int, ...], ...]
    cleared_statuses: tuple[int | None, ...]
    silence_clear_targets: tuple[int, ...]


def resolve_refresh_recovery(status, *, profile, actor_counters, target_counters):
    """Preserve highest-status-only recovery and actor-dependent return.

Wildcard compares a battle status index with a CHAR work enum, as the original
does. It clears one highest active counter, including extended states, rather
than clearing six base states or every positive state.
"""
    end, _, confusion_work = _profile(profile)
    actor = tuple(actor_counters)
    targets = tuple(tuple(row) for row in target_counters)
    for row in (actor, *targets):
        if len(row) != end or row[0] != 0:
            raise RefreshSourceDomain('requires full status vector with sentinel zero')
        for value in row:
            _int32(value)
    if status is None:
        return RefreshResolution(False, None, targets, (None,)*len(targets), ())
    if type(status) is not int or not 0 <= status < end:
        raise RefreshSourceDomain('invalid battle status index')
    active_actor = status != 0 and actor[status] > 0
    cleared = []
    updated = []
    silence = []
    for index, row in enumerate(targets):
        highest = next((j for j in range(end-1, 0, -1) if row[j] > 0), 0)
        clear = highest != 0 and (status == highest or status == 0 and highest <= confusion_work)
        output = list(row)
        if clear:
            output[highest] = 0
            if highest == 10:
                silence.append(index)
        updated.append(tuple(output))
        cleared.append(highest if clear else None)
    return RefreshResolution(active_actor, 'SPR_tyusya' if active_actor else 'SPR_hoshi',
                             tuple(updated), tuple(cleared), tuple(silence))
