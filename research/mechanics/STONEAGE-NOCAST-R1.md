# StoneAge PETSKILL_Nocast — R1 guarded reference and data gate

Date: 2026-10-01. Historical layer: fixed descendants / recovered25 bridge.
Taiwan-v1 membership is not established. This is a reference boundary, not a
closed persistent-round/coordinator implementation.

## Pinned source and compile profiles

| Profile | Commit | `_SKILL_NOCAST` | `_MAGIC_NOCAST` | NOCAST COM1 |
| --- | --- | --- | --- | --- |
| gavinlinasd/StoneAge | `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` | enabled | enabled | 2025 |
| iriselia/StoneAge | `9e6c8ce2cd8ed532a7157773acd1c61582c178b5` | enabled | enabled | 2025 |
| BismarckDD/stoneage | `999ffdf1d220ec6666eb65339180689c9caf1876` | disabled | enabled | not compiled |

FACT: callback/executor text is present in all three trees. The pinned Bismarck
profile does not compile the pet-skill callback, so source-text convergence
must not be described as three executable-profile confirmations. Its executor
also has a pointer-to-string-literal null-test anomaly. It is a textual control
only for this family.

`tools/stoneage_nocast_source_audit.py` verifies clean pinned source identities,
preprocesses the actual feature headers and compiles an enum probe. The derived
report records file SHA-256s without storing original source. These two known
2025 values are profile facts; they do not establish recovered25 numeric COM1.

## Callback and target list

FACT: the callback does not parse OPTION or exclude PLAYER. It writes symbolic
NOCAST, the submitted target, command-ready mode and LOW(COM3)=array, then
returns TRUE. No physical-power mutation is made.

FACT: the dispatcher reads COM2 directly and calls `BATTLE_S_Nocast`. It does
not first call `BATTLE_TargetAdjust`. The executor expands targets with
`BATTLE_MultiList`, emits the magic animation, then checks `IsBATTLING` before
applying status to each listed target. A FALSE return remains FALSE even after
successful status writes; no ordinary-attack fallback exists in this case.

The gavin/iris active `__ATTACK_MAGIC` MultiList profile repairs dead single
targets using same-side live slots in ascending order and a `rand()%10`
rejection loop. Area/row lists remain ascending, with opposite-row fallback.
This RNG is not interchangeable with physical TargetAdjust RNG.

OPEN / historical UB: an empty single-target side returns before initializing
the caller's ToList; Nocast ignores the return. The TARGET_ALL loop also writes
the terminator at the wrong index. The reference refuses these domains rather
than manufacturing a target list. It admits only explicit single/side/row
selectors with defined list construction.

## OPTION grammar

FACT: the parser searches `turn`, advances by `sizeof("turn")` (five bytes),
scans `%d`, then searches the success marker `成` from that advanced pointer.
The marker advance also includes its terminating-NUL size, skipping one byte
after the marker. It is not a flexible key/value parser.

Missing turn can cause `strstr(NULL, ...)`; failed turn scanning leaves an
uninitialized local. These are rejected. Missing/failed success scanning retains
the initialized Success=0. Numeric signs and ASCII decimal prefixes follow
`sscanf`, with int32 overflow rejected. The recovered25 probe parses actual
OPTION bytes independently under strict CP950 and Big5, records only derived
parameters, length/hash and metadata, and requires convergence.

## Application, resistance and timing

FACT: the shared status check first rejects any active compiled StatusTbl entry
without RNG. This includes later statuses, not only the six base statuses.
For NOCAST it uses Range=30, Bai=1.0 and:

1. defender VITAL share -> four-times share -> times ten penalty;
2. level difference clamped to [-30,30], or zero in PvP;
3. Success + level + attacker FIXLUCK - MODNOCAST - vital penalty;
4. the active `_SUIT_ADDENDUM` subtracts defender WORKRESIST;
5. convert to int, cap only the upper end at 80;
6. strict `RAND(1,100) < per`, not <=.

The model preserves the C float-assignment boundaries and is checked against a
compiled C arithmetic oracle. Resistance/work-state inputs are explicit.

FACT / enum bug: gavin/iris status NOCAST=10, but WORKWEAKEN=51,
WORKBARRIER=53 and WORKNOCAST=54. The equipment branches compare the status
index to work IDs; their supposed extra NOCAST equipment/suit-part3 deductions
therefore do not execute. General WORKRESIST does execute. These are separate
fields and must not be conflated.

FACT: `StatusAttackCheck` executes before the PET-type exclusion. An otherwise
eligible pet consumes its hit RNG even though a successful check cannot apply
Nocast. A successful non-pet check sends NC(1), writes exactly `turn` (no +1),
and emits the bad-status marker. The executor still returns FALSE.

FACT: positive WORKNOCAST blocks `MAGIC_DirectUse` before item/MP handling.
It does not globally suppress physical commands or prove that the distinct
AttackMagic pet-skill path is blocked.

At the actor's status visit, the counter is decremented before expiry/effect.
Ordinary count 1 expires to 0 and sends NC(0); larger counts send NC(1).
Active weaken/barrier at this later visit can restore the stored counter while
the expiry test still uses the decremented local counter. Thus stored count 1
plus NC(0) is a real edge; direct-magic gating still sees positive storage.
The isolated reference requires the earlier-status visit results explicitly.

## Admission and next seam

The authoritative callback-pressure report selects ID 580, **18 positive slot
uses across 16 templates**, as the next OPEN family. The dedicated bundle
workflow must establish the real row parameters before runtime admission.

Reference tests cover grammar/UB boundaries, exact target-list RNG, PET immunity
ordering, full-status blocking, strict hit thresholds, C float arithmetic,
counter/notification divergence and direct-magic gating.

OPEN: connect the evidence-closed OPTION row to enemy AI, a typed semantic
submission, round-local full-status/resistance overlays, ordered per-actor
expiry and persistent coordinator carry-forward. Keep missing late-status and
work-resistance state fail-closed; do not inject it into Taiwan-v1 save fields
or mark the 18 slot uses executable until that path has passed.


## Accepted recovered data and validation

The verified preservation-bundle probe **36881045423 = PASS** at
`02b443d618d3ed10c617e33d46c26cf309a0e0d9` closes the real OPTION/metadata gate:

| ID | FIELD | TARGET | COST | ILLEGAL | OPTION bytes | turn | Success offset |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 580 | 1 | 3 | 2 | 1000 | 15 | 3 | 50 |

OPTION SHA-256:
`28c465f3106af23dafc91aa2c54c7c7c8ff147dd26d8ee92382ecd4862dd871f`.
Strict CP950/Big5 interpretations converge. Success=50 is the formula offset,
not an unconditional 50% chance. Actual positive references are 18 across 16
templates. Report write-back is `2f461c0a36af906b6514cedd6a1c1fa6c247f47c`.

Reference/source-profile workflow **36881045171 = PASS**: 30 dedicated tests and
reproduction of the three clean pinned header audits. Local base-status/pressure
regressions bring the targeted set to 52 passing tests.

The code-page result closes the data grammar; it does not establish the original
recovered executable's compiled string-literal bytes. The currently preserved
source repositories use their own encodings. Runtime admission must explicitly
declare a semantic bridge decoding/profile instead of claiming that compiling
these modern descendant trees reproduces the recovered25 binary.

`PETSKILL_NOCAST_GUARDED_REFERENCE_R1 = CLOSED_REFERENCE_MODEL_ONLY`.
`RECOVERED25_NOCAST_OPTION_DOMAIN_R1 = CLOSED_OPTION_GRAMMAR_AND_METADATA`.
`RECOVERED25_NOCAST_RUNTIME_R1 = OPEN`.
The 18 references remain outside executable coverage until the ordered
full-status/resistance/persistence integration passes.
