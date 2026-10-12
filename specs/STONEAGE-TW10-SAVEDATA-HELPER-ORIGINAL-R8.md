# Taiwan 1.0 R8 original helper gate and strict derived report

This gate consumes only the independently SHA256-verified original sa_3.exe
and savedata.dat. It rederives the accepted R7 seed/call chain (136 states,
eight CALL rows) and requires CALL0x4879a target0x4b8a4 before analyzing that
helper with the bounded R8 effect model. It never executes the original PE.

Every analysis gap now includes exact RVA, enumerated reason, optional direct
CALL target and occurrence count. Aggregate reasons must equal those rows;
there are at most64 distinct gap sites. Return summaries/selected general
register intersections/stack effects remain independently bounded. The strict
JSON guard recomputes summary qualification from return-word/stack/cleanup,
cycle/cap/gap conditions and rejects ungrounded history/IO/caller-resumption
promotions, unknown fields, impossible totals, duplicate keys and payload text.
Format validation alone is not source-run custody or actual native behavior.

The original gate is branch-only with one bounded archive acquisition, complete
catalog MD5/SHA1 and embedded SHA256 checks, mandatory source cleanup and only
derived JSON upload. Independent review must pin source-run/head and validate
the tiny artifact without re-downloading original media. Synthetic CI performs
no original acquisition and cannot admit a historical helper summary.

A nonqualifying helper must not be skipped to resume filename propagation.
Nested calls, unknown aliases, caller-frame mutations or specialized effects
require exact independent summaries. The tool intentionally preserves all
native/format/publication admission flags as false even when a model-only
return-effect summary qualifies. No original bytes/operand listings/assets.
