# StoneAge Refresh bounded source reference R1

## Evidence and scope

**FACT / LATER_RECOVERED:** independently audited clean pins:

| Profile | Commit | Compiled command | Source skill macro | Status END / labels | CONFUSION work enum |
|---|---|---:|---:|---:|---:|
| gavin | 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 | 2032 | 575 | 44 / 32 | 50 |
| iris | 9e6c8ce2cd8ed532a7157773acd1c61582c178b5 | 2032 | 575 | 44 / 32 | 50 |
| bismarck | 999ffdf1d220ec6666eb65339180689c9caf1876 | 2030 | 575 | 12 / 12 | 46 |

These are profile-specific compiled identifiers, not recovered IDs 583/592 or
recovered binary command assignments. No introduction date or Taiwan-v1
membership follows from later source comments.

Own model: `tools/stoneage_refresh_model.py`. Reproducible native audit:
`tools/stoneage_refresh_source_audit.py`. Original functions and actual LOW
macro compile only transiently; the repository keeps hashes and derived facts.

## Callback and dispatch

The callback writes REFRESH, the supplied target, C_OK and the skill array into
LOW(COM3), retaining the previous HIGH bits. It returns TRUE and neither reads
OPTION nor checks actor kind. Battle dispatch reads LOW and direct COM2 without
TargetAdjust. Executor return, command symbol, source macro, data skill ID and
skill-array identity remain separate namespaces.

## Parser and build boundaries

The executor compares the first **two bytes** at each candidate position with
status labels in order, stopping on the first match. Full-character equality is
not equivalent under UTF-8. The scan starts at status index zero, whose work
entry is -1. All audited work getters reject that element and return -1, so a
wildcard has a FALSE return and star receive effect.

Every profile dereferences a NULL OPTION. gavin/iris have 32 labels but scan to
END 44: a nonmatching first position can read outside the array before searching
later bytes. Only empty or immediate admitted baseline matches enter the own
reference for these profiles. Bismarck's complete 12-entry table can safely
search later positions or return no match. Embedded NUL and unknown/unproved
profiles/builds are rejected by the own API.

All profiles compile/test UTF-8 and GBK experiments; only iris has a wholly
CP950-encodable active label table. Replacing selected labels to force another
profile to compile would alter evidence. Original compiler execution charset
remains **OPEN**. The real-byte probe must retain source failures and profile
non-convergence; a conditional iris CP950 match is not binary provenance.

## Recovery behavior

Executor return and the receive effect depend on the **actor's** selected
counter, before recovery. A clean actor may clear a target while returning
FALSE; an affected actor may return TRUE even if no target is cleared. A no-match
OPTION returns FALSE before invoking effects or recovery.

Shared recovery emits MagicEffect before walking targets. For each target it
scans the whole active status-work table, retains the **highest index** with a
positive counter, then clears exactly that one counter if the requested status
matches it. A lower matching status remains unchanged when a higher positive
counter is present. Nonpositive counters are inactive.

Wildcard status zero compares that battle status index to the **CHAR work enum**
CONFUSION, rather than the battle CONFUSION index. All active indices fit that
bound in these three builds, including extended statuses. Wildcard therefore
clears the highest active counter, not every counter and not just the six base
statuses. Silence clearing also emits the profile's NC=0 notification; every
successful clear emits BadStatusString(target,0).

No random draw appears in the executor or shared recovery. This does not imply
an RNG-free full action: gavin/iris enable __ATTACK_MAGIC, whose original
MultiList can choose a different living target via rand() when a selected single
target dies. That path and its no-living-target/list-initialization behavior
require separate ordered runtime proof. Bismarck has that feature inactive.

## Verification and outstanding runtime

Local independent reference/probe/loader/pressure checks: **29 PASS**, including
13 semantic model tests. Original callback, actual LOW macro, executor and
shared recovery: **9083 defined witnesses** across seven builds, plus seven
expected NULL and five short-table diagnostics under ASan/UBSan. Accessor and
already-resolved target lists are audited witness seams, not native live
participant lookup/target selection.

The preservation probe verifies both bundle parts, concatenated archive and
full petskill hash, enumerates every exact callback row including unreferenced
rows, records full execution metadata/OPTION hashes and checks positive uses.
Full observed population and actual-byte native results require remote
acceptance and explicit hardening before being called CLOSED.

**OPEN:** typed enemy-AI admission, actor/target identity, direct-target and
MultiList RNG ordering, action suppression/continuation/counter/combo behavior,
persistent shared status removal, silence/magic eligibility restoration,
Weaken/Barrier prepared-power restoration, multi-target events, session
coordinator and following-round acceptance. No pressure CLOSED classification
or accepted-use increase is authorized by this source-reference milestone.
