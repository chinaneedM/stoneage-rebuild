# PETSKILL_Weaken fixed-source safe reference — R1

Evidence date: 2026-10-04. This is later-descendant/recovered25 reconstruction,
not a Taiwan-v1 membership claim or a production redesign.

## Evidence and identity

FACT: exact callback `PETSKILL_Weaken` is active under `_SKILL_WEAKEN` with
`_MAGIC_WEAKEN` in all three pinned profiles:

| Profile | Commit | Source root | Compiled command | WEAKEN status/work | Source skill macro |
|---|---|---|---|---|---|
| gavin | `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` | `gmsv/src` | 2022 | 7 / 51 | 544 |
| iris | `9e6c8ce2cd8ed532a7157773acd1c61582c178b5` | `Source/gmsv` | 2022 | 7 / 51 | 544 |
| Bismarck | `999ffdf1d220ec6666eb65339180689c9caf1876` | `server/gmsv` | 2021 | 7 / 47 | 544 |

OPEN: none of those numeric commands or skill-array indices is an authenticated
recovered25 binary mapping. Actual recovered data IDs 575/576 must pass the
independent hash-verified preservation-bundle probe.

## Submission, dispatch and byte parser

FACT: callback writes symbolic COM1, COM2 target, C_OK and LOWCOM3 array, and
returns TRUE. It does not inspect OPTION/data, reject PLAYER or mutate attack,
defense or quickness. Dispatch uses COM2 directly and LOWCOM3; no preceding
physical TargetAdjust or ordinary counter loop is introduced.

FACT: executor fetches OPTION, scans bytes against the first TWO bytes of each
status label, then increments its pointer by two plus the for-loop's one byte.
It searches `turn`, advances by sizeof including NUL, and sscanf reads an integer.
Success-marker search starts from that advanced pointer, not OPTION start.
Weaken initializes turn=3 and Success=0: failed turn sscanf retains **3**, unlike
the uninitialized-turn Nocast/Barrier paths. Missing turn still passes NULL to
the later strstr; this remains outside the safe domain. Terminal markers can
advance past the string NUL and are rejected. Signed turn+1/scanf overflow is
also rejected.

FACT / encoding boundary: source literals are UTF-8; gavin uses simplified
shorthand, iris traditional shorthand, and Bismarck longer simplified status
labels. The admitted leading WEAKEN marker stops the native scan at status 7.
In CP950/Big5 the marker occupies two bytes and the scanner skips a following
byte; in UTF-8 it consumes the three-byte character. Full recovered OPTION
bytes are decoded strictly under CP950 and Big5, with equality required.
Encoding is explicit and is not an inferred recovered compile profile.

FACT / historical unsafe control: gavin/iris compile BATTLE_ST_END=44 while
aszStatus contains only 32 labels. Arbitrary/no-match scans can read beyond that
array. Bismarck's 12-status profile has 12 labels. Safe reference admits a
leading, verified WEAKEN marker only; it does not invent arbitrary scan results.
Bismarck's OPTION pointer comparison against an empty string literal is not a
NULL guard. Null input is never exercised or admitted there.

## Shared application

FACT: `BATTLE_MultiParamChangeTurn` resolves MultiList, emits magic-effect setup,
then checks each target with `BATTLE_StatusAttackCheck(status, Success,30,1.0)`.
Any positive entry in the complete compiled StatusTbl blocks before RNG.
Otherwise probability is level difference clamped to +/-30 (zero in PvP), plus
Success and attacker fixed luck, minus WEAKEN resistance, vital-share penalty
and active general suit resistance. C float boundaries and int truncation are
retained. Maximum probability is 80, without a lower clamp; success uses the
strict comparison RAND(1,100) < per.

FACT: equipment-specific branches compare status index against work-field
enums. WEAKEN index 7 differs from 51/47, so those branches do not execute.
Bismarck's extra Lua resistance feature is inactive in the pinned profile.
The safe implementation rejects signed intermediate overflow and undefined
stat totals rather than filling unavailable state with zero.

FACT: on hit the shared writer stores **WORKWEAKEN = turn+1**, including PET
and ENEMY targets. It does not clear target COM1 or directly change work power.
Executor retains FALSE return even after a successful application. Unlike
Nocast, it has no PET exclusion or NC application notification.

The safe MultiList selector/retarget rules reuse the accepted Nocast primitive.
Unsafe TARGET_ALL and empty single-side domains remain excluded.

## Explicit attribute recalculation seam

FACT: `CHAR_complianceParameter` rebuilds base work values, applies equipment,
then calls `Other_DefcharWorkInt`. With WORKWEAKEN positive, this latter routine
multiplies fixed strength/toughness/dexterity by **double 0.8**, converts to int,
and decrements WEAKEN once. It also decrements positive BARRIER once. Finally
it copies the resulting fixed values into attack/defense/quick work fields.
Even a counter of one reduces powers before becoming zero. A later compliance
event rebuilds baseline first, so the weakening is not automatically a cumulative
0.8 multiplier on the previous weakened profile.

This is separate from command submission, status application and StatusSeq.
Do not substitute an automatic beginning/end-of-round recalculation without
closing the caller schedule. Existing direct application does not itself call
compliance. The standalone safe recalculation reference requires other suit,
profession, wolf and fear modifiers absent, but compiles the actual routine with
those active feature branches present and their explicit work inputs zero.

## Counter visits and overlay integration boundary

FACT: WEAKEN index 7 precedes DEEPPOISON 8, BARRIER 9 and NOCAST 10.
StatusSeq first decrements storage/local cnt, then tests the current WEAKEN and
BARRIER storage and may restore cnt+1. Expiry still uses decremented local cnt.
A WEAKEN counter above one self-freezes. One expires to zero unless BARRIER
restores storage; in that case expiry can fire with stored WEAKEN still one.
Mutual WEAKEN/BARRIER freeze may retain both counters while later NOCAST emits
NC(0) from its local expiry. This behavior is preserved rather than replaced
with an invented fixed duration. Earlier base status visits observe the
WEAKEN storage before its own visit; later statuses see the updated storage.

Reference tick uses the existing accepted Barrier decrement/self-freeze
primitive. Runtime integration must extend **NocastParticipantRuntime /
NocastRoundOverlay**, adding an explicit counter/resistance, an explicit recalculation boundary and typed submission
through enemy AI, ordered round, persistent adapter and coordinator. Existing
`weaken_active_at_visit` external input remains distinct from the new counter.
Do not create another parallel status overlay, change historical character save
fields, or claim these uses executable before ordered runtime/E2E acceptance.

## Reproducibility and limits

`tools/stoneage_weaken_source_audit.py` verifies clean pinned Git identities,
active features, actual header enums, callback/dispatch/status gates and hashes.
It compiles actual callback, executor, status checker, shared writer and Other_DefcharWorkInt only in
a temporary directory. Fixtures inject a single resolved MultiList target and
explicit RAND(1,100) witness; the legacy random generator and MultiList itself
are not part of this native oracle. UBSan/ASan run 8 parser/executor and 512
probability/writer plus 128 recalculation cases per profile (24 + 1536 + 384 total). Leak detection is disabled
because the execution host does not support LeakSanitizer's process inspection;
address and undefined-behavior instrumentation remain enabled.

The 17 dedicated model tests cover byte offsets/defaults, failed/strict hit
checks, PET admission, overflow, self/mutual freeze, visit-order effects and
retarget RNG. Six synthetic probe tests do not impersonate actual recovered
rows. Total local reference/related-regression acceptance is 126 tests, including
the existing Nocast and Barrier persistent coordinator E2Es.

OPEN: recovered data population/OPTION acceptance, compliance caller scheduling and typed ordered runtime.
No original source, raw skill rows or proprietary assets are stored.
Source registry: SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1.
