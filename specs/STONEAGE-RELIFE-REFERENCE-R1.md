# StoneAge ENEMYSKILL_ReLife bounded reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_REFERENCE**  
Date: 2026-10-05  
Scope: recovered25 positive enemy uses of `ENEMYSKILL_ReLife` only.

## 1. Recovered25 data boundary

Verified preservation-bundle evidence closes the callback population to exact
skill ID **500**:

- FIELD **1** = battle;
- TARGET **2** = `PETSKILL_TARGET_ALLMYSIDE`;
- COST **2**;
- ILLEGAL **0**;
- OPTION length **0**;
- OPTION SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

There are exactly **3 positive enemybase slot uses / 3 templates**:

- TEMPNO 39 / graphic 100370 / PETSKILL5;
- TEMPNO 909 / graphic 100071 / PETSKILL2;
- TEMPNO 1165 / graphic 101814 / PETSKILL4.

No display text or raw proprietary table row is stored by this reference.

## 2. Fixed descendant callback boundary

Pinned later descendants:

- gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`.

All three compile `_PRO_BATTLEENEMYSKILL` and register the exact callback.
The callback itself does not parse OPTION or use the skill-array index. It
writes symbolic `BATTLE_COM_S_ENEMYRELIFE`, copies the supplied target carrier
to COM2, marks `BATTLE_CHARMODE_C_OK`, and returns TRUE.

The guarded numeric command is not portable:

- gavin / iris: **2013**;
- fixed Bismarck: **2012**.

R1 therefore preserves the symbolic command only. It does not choose either
number as the recovered25 original COM1.

## 3. Dispatcher and fallback ordering

The fixed battle dispatcher runs `BATTLE_TargetAdjust` on COM2 before calling
the ReLife effect helper.

- If target adjustment cannot produce a valid ordinary opponent target, the
  dispatcher emits NoAction and never enters ReLife.
- If target adjustment succeeds, it calls `BATTLE_E_ENEMYREFILE`.
- If that helper returns FALSE, the actor is marked attacked and the dispatcher
  falls back to ordinary physical `BATTLE_Attack` against the already-adjusted
  COM2 target.

Thus a failed ReLife effect is not WAIT/NONE, and a runtime must not perform a
second fallback retarget after the helper has failed.

TARGET=ALLMYSIDE is pet-skill metadata/admission information. For an enemy
caster it is **not** the actual resurrection target selector; that selection is
owned by the effect helper described below.

## 4. Enemy-caster resurrection target domain

For an enemy actor, `BATTLE_E_ENEMYREFILE` ignores the callback's COM2 as the
resurrection target and independently scans enemy-side battle slots **10..19**
in ascending order.

A candidate must survive the source's dead-entry checks:

- the slot resolves to a valid battle character;
- it is not marked `BENT_FLG_ULTIMATE`;
- battle mode is nonzero;
- battle mode is not `BATTLE_CHARMODE_RESCUE`;
- `CHAR_ISATTACKED == TRUE`;
- `CHAR_ISDIE == TRUE`.

If there is no candidate, the helper returns FALSE and consumes no
ReLife-effect RNG. The dispatcher then uses the ordinary-attack fallback.

If one or more candidates exist, one
`RAND(0, candidate_count - 1)` draw selects the candidate by ascending-slot
list index. The source still owns this call when candidate_count is one.

The separate pet-caster branch uses the carried defNo instead of this enemy
scan. Other actor types are rejected. Recovered25 positive references are enemy
templates, so the enemy branch is the bounded runtime target.

## 5. Resurrection amount and state mutation

After the selected slot is revalidated, the helper computes:

`power = target.WORKMAXHP / 2`

using C integer division and calls `BATTLE_MultiRessurect` with percentage flag
zero.

`BATTLE_MultiRessurect` re-resolves the dead target list and emits the magic
effect before HP/death mutation. For a nonzero power it consumes one source
`RAND(power * 0.9, power * 1.1)` recovery-amount draw. The resulting amount is
clamped to at least one, target HP is capped at WORKMAXHP, and
`CHAR_ISDIE` is cleared.

The fixed Bismarck helper contains an unrelated `power == -1` extension under
`_MAGICPET_SKILL`; ReLife always supplies WORKMAXHP/2, so that descendant
difference does not alter this bounded ReLife path.

The common resurrection helper also refuses player resurrection in PvP. That
is retained as a shared helper boundary, not promoted into a recovered25 enemy
case.

## 6. RNG ownership

The ordered runtime must preserve these distinct RNG seams:

1. any RNG used by the ordinary `BATTLE_TargetAdjust` / default-opponent
   carrier path belongs to that existing caller seam;
2. only after successful target adjustment and at least one eligible dead enemy
   does ReLife consume `RAND(0, dead_count-1)`;
3. after target selection and successful revalidation, nonzero resurrection
   power consumes the `RAND(power*0.9, power*1.1)` amount draw;
4. no eligible dead entry consumes neither ReLife draw and activates the
   physical-attack fallback.

No exact libc PRNG-state identity is claimed.

## 7. Explicitly open boundaries before ordered runtime

This reference does **not** close:

- recovered original executable/compiler/profile identity;
- original numeric `BATTLE_COM_S_ENEMYRELIFE` value;
- original JSS/Taiwan-v1 membership or introduction date;
- exact recovered enemy-AI COM2 carrier generation beyond the source ordering
  needed for fallback;
- runtime retention of dead-but-revivable battle entries across action/round
  boundaries;
- composition with modeled forced-exit/ultimate removal and other persistent
  status overlays;
- exact modern integer witness API for the source floating endpoint expressions
  until the runtime model is written.

These are runtime/integration questions, not reasons to weaken the closed
source/data reference.

## 8. Acceptance

- First source + preservation-bundle probe: **37288674220 PASS**.
- Exact recovered row/template pin: **37288913119 PASS**.
- Full petskill table SHA-256:
  `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.

Derived reports:

- `research/recovered/STONEAGE-RELIFE-SOURCE-AUDIT-R1.txt`
- `research/recovered/STONEAGE-25-RELIFE-PROBE-R1.txt`

**RELIFE_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.**
