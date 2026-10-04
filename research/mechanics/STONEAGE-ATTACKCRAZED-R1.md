# AttackCrazed pinned descendant reference — R1

Audit date: 2026-10-04. Classification: **FACT for the pinned later-source
profiles**; **OPEN for recovered25 binary identity and Taiwan-v1 membership**.

## Evidence and numbering

Audited gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris
`9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, and Bismarck
`999ffdf1d220ec6666eb65339180689c9caf1876`. The reproducible audit checks
source HEAD/clean tree, active preprocessor features, actual compiled header
command value, callback work writes, target-list construction and dispatch.

All three enable `_BATTLE_ATTCRAZED`; their compiled command is 2010 and their
`PETSKILL_AttCrazed` macro is 608. The recovered preservation data identifies
callback row **613**. These numbering domains must not be conflated. No
recovered25 command number is assigned by this reference model.

## Callback and admitted OPTION domain

- Reject invalid actor indexes and PLAYER actors.
- Write symbolic command, submitted target, command-ready mode, attack work
  power `int(FIXSTR*0.8)` and defense work power `int(FIXTOUGH*0.7)` before
  reading OPTION. These are C double multiplication/truncation operations.
- LOW(COM3) stores the skill array; HIGH(COM3) stores the C `atoi` OPTION count.
- gavin/iris reject a NULL OPTION after the preceding work writes. Bismarck
  instead compares the pointer to a string-literal address; this is not a
  content-empty test or a NULL guard. Missing-pointer behavior is divergent
  and remains outside the reference admission domain.
- The reference admits non-NUL bytes whose `atoi` prefix yields **1..19**.
  The 20-entry target buffer writes its sentinel at index n, so n>=20 is
  unsafe. Zero, negative, overflow and pointer-missing cases remain OPEN;
  rejecting these inputs is a reconstruction gate, not a claim that the old
  callback validated them. Numeric-prefix trailing bytes are intentionally
  accepted as `atoi` would accept them.

## Target-list construction and RNG order

Before damage dispatch, the native list is filled with the original target.
The specialized branch then:

1. With `_SHOOTCHESTNUT` enabled, same-side targets change the command to NONE
   and return without selection RNG. gavin/iris enable this feature;
   Bismarck does not. Opposite-side behavior converges.
2. A target outside 0..19 sets list index 1 to -1 and returns.
3. A target in 0..9 scans **0..8**; a target in 10..19 scans **10..18**.
   Slots 9 and 19 are omitted by the strict upper-bound loop. Preserve this
   source quirk rather than silently repairing it.
4. Only slots accepted by `BATTLE_TargetCheck` enter the candidate list.
5. With no candidates, return the original 20-entry target-filled buffer;
   this does not manufacture a no-action or a terminator.
6. Otherwise consume n explicit `RAND(0,j-1)` draws, with replacement, and
   append -1. A single candidate still consumes n `(0,0)` draws.

## Physical dispatch boundary still awaiting runtime admission

- Count is HIGH(COM3), with **no AttackCrazed damage division**. It must not
  reuse ContinuationAttack's divided damage merely because both are multi-hit.
- List selection occurs before the first physical TargetAdjust and before
  dodge/critical/guard RNG.
- For non-bow actors the first hit uses TargetAdjust on the submitted target.
  **Preselected list[0] is unused as a hit target**, although its RNG draw has
  already been consumed. Later hits use list[++k] and TargetAdjust again.
- Work command becomes ordinary ATTACK before physical execution. The common
  ordinary attack path owns Guardian, dodge, critical, guard, damage reaction,
  ride splitting, death/exit/profit and minimum-damage behavior.
- Actor death, negative list sentinel and empty-side checks stop the loop at
  their existing ordered boundaries. Counter continuation is evaluated after
  the multi-hit sequence using its final ordinary BATTLE_Attack result.
- Bow and other weapon profiles are not admitted by this reference milestone.
  Complete runtime closure requires an explicit weapon domain and per-hit
  mutable state/RNG tests; static list construction alone is insufficient.

## Acceptance

`tools/stoneage_attack_crazed_model.py` is an independent callback/list
reference, not an executable enemy-AI bridge. `tools/stoneage_attack_crazed_source_audit.py`
reproduces source gates and emits derived hashes/flags only.
`tools/stoneage_recovered25_attack_crazed_probe.py` probes actual recovered
metadata, OPTION length/hash/safe count and the expected 9 uses/9 templates.

The preservation-bundle probe must verify both parts and combined archive
SHA-256 before decoding. Only derived reports may be committed. Until that
probe and enemy AI -> typed submission -> ordered physical round -> persistent
coordinator acceptance pass, `RECOVERED25_ATTACKCRAZED_RUNTIME_R1` stays **OPEN**
and executable slot-use coverage stays **2391/2486**, approximately **96.2%**.
