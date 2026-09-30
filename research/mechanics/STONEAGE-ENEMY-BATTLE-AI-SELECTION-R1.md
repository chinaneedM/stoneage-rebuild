# StoneAge enemy battle AI command selection — R1

Date: 2026-10-01

Status: **stable-descendant command-selection core closed; recovered25 common profile/runtime bridge partially enabled with fail-closed skill expansion**

## Purpose

This audit closes the evidence boundary that was deliberately deferred when the
local persistent ATTACK/WAIT coordinator was introduced. It answers one narrow
question:

> When may the local runtime stop requiring caller-supplied enemy commands and
> derive an enemy command from recovered data without inventing behavior?

The answer is: only after both the integer `TACTICS` mode and the text
`TACTICSOPTION` profile are preserved. The current recovered25 runtime had
retained the former and discarded the latter, so automatic enemy-command
generation was not yet evidence-complete.

## Fixed source anchors

Primary stable descendant:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/char/enemy.c`
  - `gmsv/src/include/enemy.h`
  - `gmsv/src/battle/battle_ai.c`
  - `gmsv/src/battle/battle.c`

Independent convergent comparison:

- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/battle/battle_ai.c`

Recovered runtime bridge:

- verified mixed-2.5 `enemy.txt` selected by `setup.cf`;
- `tools/stoneage_encount_chain_probe.py`;
- `tools/stoneage_recovered25_encounter_runtime.py`;
- `tools/stoneage_tw10_25_encounter_bridge.py`.

This remains descendant/recovered25 evidence. It is not promoted to an exact
JSS-1999 or Taiwan-v1 enemy-AI dataset.

## 1. Enemy-instance data owns AI configuration

The stable enemy loader has two distinct AI inputs:

- integer `ENEMY_TACTICS`;
- text `ENEMY_TACTICSOPTION`.

On concrete enemy creation they become:

- `CHAR_WORKTACTICS`;
- `CHAR_WORKBATTLE_TACTICSOPTION`.

Therefore the AI profile belongs to the concrete `enemy.txt` variant layer,
not the `enemybase.txt` pet/species template.

Keeping only `TACTICS` is insufficient.

## 2. Dispatch table

The fixed common dispatcher contains:

- mode 0 -> no function;
- mode 1 -> `BATTLE_ai_normal`.

In `BATTLE_ai_all()`, an out-of-range mode is repaired to mode 1 before
dispatch. `BATTLE_ai_one()` instead rejects an out-of-range mode. Ordinary
battle turn setup calls `BATTLE_ai_all(..., turn=0)` for both sides before
`BATTLE_Battling()`.

No reconstruction should silently merge those two entry-point behaviors.

## 3. Normal profile grammar

The convergent fixed sources parse the following tags from
`TACTICSOPTION`:

- `at:<weight>;<target-scope>;<target-selection>`
- `gu:<weight>`
- `ma:<weight>`
- `es:<weight>`
- `wa:<w0>;<w1>;<w2>;<w3>;<w4>;<w5>;<w6>`

The later compile-gated `_ENEMY_ATTACK_AI` profile also recognizes
`rn:<value>` and additional target/selection modes. Those additions must stay
separately versioned until the recovered25 build boundary is established.

The ordinary action-mode roll uses the sum of:

- attack weight;
- guard weight;
- magic weight;
- escape weight;
- seven skill-slot weights.

A single explicit random draw selects one weighted mode.

## 4. Attack target scope

For ATTACK and `wa` skill modes, the stable common target scopes are:

- 1 = all living opposing entries;
- 2 = players only;
- 3 = pets only.

Dead entries and RESCUE-mode entries are excluded.

If a player-only or pet-only filter yields no candidates, the source falls
back to the all-target scope and retries. If the all-target scope itself has no
candidate, selection fails.

The compile-gated leader target mode is not part of this common subset.

## 5. Attack target selection

The stable common selectors are:

- 1 = explicit random candidate;
- 2 = highest current HP;
- 3 = lowest current HP.

HP-max/min selection keeps the first encountered slot on ties.

The compile-gated strength/dexterity/attribute selectors and the `rn`
random-override branch are not promoted into the common profile.

## 6. Selected action result

The common branch returns:

- ATTACK -> `BATTLE_COM_ATTACK` plus selected target;
- GUARD -> `BATTLE_COM_GUARD`;
- ESCAPE -> `BATTLE_COM_ESCAPE`;
- `wa[n]` -> invokes pet-skill slot `n`; the resulting battle command comes
  from `PETSKILL_Use`.

Although `ma` participates in the weighted mode roll, the inspected normal
function has no terminal magic-result branch and therefore returns failure for
that selected mode. This behavior must not be “fixed” by inventing a magic
command.

Skill execution remains a separate surface because it depends on recovered
pet-skill runtime state and can rewrite the battle command.

## 7. Surprise / immobility boundaries

`BATTLE_ai_all()` also applies outer behavior that is distinct from profile
selection:

- a charging enemy is marked command-ready without selecting a new command;
- a surprised enemy side receives `BATTLE_COM_NONE`;
- after normal AI selection, `BATTLE_CanMoveCheck()==FALSE` rewrites the
  selected command to NONE.

These are battle-state gates, not `TACTICSOPTION` grammar.

## 8. Recovered25 bridge gap and correction

Before this audit, `parse_enemy()` intentionally skipped all enemy text
prefix fields and the engine-facing `EnemyVariantBridge` retained only the
integer `TACTICS`. That was sufficient for spawn/stat restoration but not for
AI reconstruction.

The runtime bridge now preserves the second enemy text field as
`EnemyVariantBridge.tactics_option` while retaining the default empty value
for older synthetic callers.

The encounter-chain probe now performs a privacy/copyright-safe aggregate AI
profile audit. It reports only:

- integer tactics-mode counts;
- recognized tag presence counts;
- structurally invalid profile count;
- unknown tag counts;
- positive-action tag signatures;
- non-empty action-condition count.

It does **not** emit enemy names, raw tactics strings, action-condition strings
or original rows.

Implementation chain:

- `44675601c0c2c63149225b0e29e3f00b1bf3fbf7` — aggregate profile audit;
- `cb03b55f35a1edfd20fb1baea65c261235f44076` — parser regression;
- `9f4a7f812659b2a415762340205c6066299e9b10` — bridge field;
- `ac2892b44db2b1fd8f8523c69ddec185cd8753b2` — recovered25 loader propagation;
- `4052042d9b7634c7d44882925056b6abbb1be915` — bridge regression.

## 9. Recovered25 runtime integration status

The deferred runtime boundary is now partially closed without changing the
explicit-RNG rule.

- `tools/stoneage_enemy_ai_model.py` implements the common normal selector
  with explicit mode and target rolls.
- Only `TACTICS == 1` is admitted by the local coordinator. Other tactics
  modes remain fail-closed.
- ATTACK and GUARD are generated directly from the recovered profile and
  execute through the persistent ordinary-round runtime.
- ESCAPE is generated only through the dedicated escape seam using recovered
  `enemybase.RARE` plus explicit escape RAND and opponent-ABIO inputs.
- `wa[0..6]` is interpreted as the exact seven-slot pet-skill index. This is
  materially important because recovered25 `enemybase.txt` contains sparse
  skill-slot layouts; positive skill IDs cannot be compacted safely.
- The recovered25 pet-skill runtime resolves every positive enemybase skill
  reference: 147 active skill rows, 111 referenced skill IDs, 0 unresolved.
- The first executable `wa` subset admitted `PETSKILL_None`,
  `PETSKILL_NormalAttack` and `PETSKILL_NormalGuard`.
- `PETSKILL_StatusChange` is admitted after hash-pinned recovered25 proof that
  all six referenced OPTION rows have CP950/Big5 decode consensus and match
  the fixed ordinary-status grammar.
- `PETSKILL_PowerBalance` is admitted for the recovered25 subset whose three
  referenced OPTION rows decode identically under CP950/Big5, all contain both
  `攻%` and `防%`, and contain no unclosed `敏%` extension marker.
- `PETSKILL_Mighty` is admitted after bundle-backed proof that both referenced
  OPTION rows decode identically under CP950/Big5, both contain `倍` and `避`,
  and both pass strict multiplier/dodge numeric grammar.
- StatusChange carries recovered command-setup effects and uses only explicit
  target status profiles / status RNG. PowerBalance carries handler-side work
  attack/defense mutations into the ordinary physical attack path. Mighty
  preserves its packed damage multiplier and dodge modifier at their fixed
  execution points. Neither PowerBalance nor Mighty introduces hidden RNG.
- Empty slots, unresolved IDs and every other callback continue to fail closed.
- `BATTLE_COM_NONE` is preserved as its own source-shaped no-action command;
  it is not rewritten to WAIT.
- Recovered25 aggregate runtime validation remains
  `RESOLUTION|RECOVERED25_LOCAL_RUNTIME_STACK_CLOSED`.

The common AI source uses the same opposing-target selection path for ATTACK
and `wa` skill modes. The runtime therefore preserves that behavior instead
of attempting to infer skill-specific friendly-target policy.

## Reconstruction rule

Current rule:

- caller-supplied enemy commands remain valid at the low-level explicit-command
  coordinator seam;
- automatic common-normal generation is permitted only for the evidence-closed
  ATTACK/GUARD/ESCAPE/basic-`wa`/StatusChange/PowerBalance/Mighty subset described above;
- an unsupported selected `wa` callback is an error, never an implicit ATTACK,
  GUARD, NONE or WAIT fallback;
- a selected `ma` path still resolves to no common decision, matching the
  inspected source branch;
- no compile-gated `_ENEMY_ATTACK_AI` behavior may be assumed for recovered25.

## Next seam

Use hash-pinned recovered25 aggregate callback/slot-use coverage to prioritize
the remaining stable-common `wa` callbacks. PowerBalance and Mighty are now
closed. Audit GuardBreak next: recovered25 has one referenced GuardBreak ID with
60 slot uses and an ASCII-only OPTION, while the fixed handler's only optional
data marker is non-ASCII `攻%`, so no recovered attack-percent rewrite can
apply. The remaining work is its dedicated command-1002 guard-only execution
gate and downstream damage/reaction ordering. Keep ChargeAttack and
ContinuationAttack deferred until their cross-turn/multi-hit contracts are
explicitly reconstructed. Add new state/RNG inputs when required; do not
generalize a pet-skill executor ahead of evidence.
