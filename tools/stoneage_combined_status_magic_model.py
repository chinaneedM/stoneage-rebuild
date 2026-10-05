"""Independent byte-level ordinary status-magic parser reference.

Only baseline-label matches are admitted for the two short-table profiles.
Build encodings are conditional experiments, not original compiler claims.
"""
from dataclasses import dataclass
import re

from tools.stoneage_refresh_model import _BASELINE, BUILD_CHARSETS, PROFILE_FACTS

STATUS_MAGIC_IDS = (61,139,159,169,179,189)
SUCCESS_MARKERS = {"gavin":"成", "iris":"Θ", "bismarck":"成功"}

# Independently pinned after verified-data Action 37266411923, report commit
# 7f50e1ae836485f2c46a5b2bc16e5a4cc2db9362. These do not derive from parsing.
EXPECTED_IRIS_CP950_STATUS = {61:0,139:1,159:4,169:6,179:5,189:3}


def expected_actual_outcomes():
    """The accepted 42-cell conditional actual-byte outcome matrix."""
    rows=[]
    for profile,charsets in BUILD_CHARSETS.items():
        for charset in charsets:
            for magic_id in STATUS_MAGIC_IDS:
                kind="recovery" if magic_id==61 else "change"
                if profile=="iris" and charset=="cp950":
                    rows.append((profile,charset,magic_id,kind,"defined",True,
                        EXPECTED_IRIS_CP950_STATUS[magic_id],
                        None if kind=="recovery" else 5,
                        None if kind=="recovery" else 15,"defined"))
                elif profile=="bismarck":
                    rows.append((profile,charset,magic_id,kind,"defined",False,None,None,None,"defined"))
                else:
                    rows.append((profile,charset,magic_id,kind,"unsafe",None,None,None,None,
                                 "short_status_table_scan_unsafe"))
    return tuple(sorted(rows))


def validate_actual_outcomes(rows):
    """Reject population, profile, classification or semantic drift."""
    rows=tuple(rows)
    if len(rows)!=42 or tuple(sorted(rows))!=expected_actual_outcomes():
        raise CombinedStatusMagicDomain("recovered_status_magic_exact_outcome_matrix_drift")


class CombinedStatusMagicDomain(ValueError):
    """Unsafe source parser or input outside the admitted build domain."""


@dataclass(frozen=True)
class ParsedStatusMagic:
    kind: str
    status: int | None
    turn: int | None = None
    success: int | None = None

    @property
    def accepted(self):
        return self.status is not None


def _scan(raw, *, profile, execution_charset, start):
    if profile not in PROFILE_FACTS or execution_charset not in BUILD_CHARSETS[profile]:
        raise CombinedStatusMagicDomain("unsupported_conditional_build")
    if raw is None:
        raise CombinedStatusMagicDomain("null_option_dereference")
    if type(raw) is not bytes or b"\0" in raw:
        raise CombinedStatusMagicDomain("requires_non_nul_option_bytes")
    end,count,_ = PROFILE_FACTS[profile]
    labels = tuple(word.encode(execution_charset)[:2] for word in _BASELINE[profile])
    for offset in range(len(raw)):
        for status in range(start,len(labels)):
            if raw[offset:offset+2] == labels[status]:
                # The body advances two bytes and the for-loop advances one
                # more even after a match. The next parser starts at +3.
                return status, offset+3
        if count < end:
            raise CombinedStatusMagicDomain("short_status_table_scan_unsafe")
    return None,None


def _sscanf_int(raw, offset, default):
    # Input is an exact NUL-terminated string witness; searching past its
    # terminator is not admitted merely because a larger legacy buffer exists.
    if offset > len(raw):
        raise CombinedStatusMagicDomain("cursor_past_option_terminator")
    match = re.match(rb"[ \t\n\r\v\f]*([+-]?[0-9]+)",raw[offset:])
    if match is None:
        return default
    value = int(match.group(1))
    if not -(2**31) <= value < 2**31:
        raise CombinedStatusMagicDomain("sscanf_integer_overflow")
    return value


def parse_status_magic_option(raw, *, kind, profile, execution_charset):
    if kind not in ("change","recovery"):
        raise CombinedStatusMagicDomain("unsupported_status_magic_kind")
    status,cursor = _scan(raw,profile=profile,execution_charset=execution_charset,
                          start=1 if kind=="change" else 0)
    if status is None:
        return ParsedStatusMagic(kind,None)
    if kind=="recovery":
        return ParsedStatusMagic(kind,status)
    if cursor > len(raw):
        raise CombinedStatusMagicDomain("cursor_past_option_terminator")
    turn_pos = raw.find(b"turn",cursor)
    if turn_pos < 0:
        # The original overwrites pszP with NULL, then calls strstr again.
        raise CombinedStatusMagicDomain("missing_turn_causes_null_success_search")
    cursor = turn_pos+len(b"turn")+1
    turn = _sscanf_int(raw,cursor,3)
    marker = SUCCESS_MARKERS[profile].encode(execution_charset)
    success_pos = raw.find(marker,cursor)
    success = 15 if success_pos<0 else _sscanf_int(raw,success_pos+len(marker)+1,15)
    return ParsedStatusMagic(kind,status,turn,success)
