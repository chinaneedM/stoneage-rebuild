# BattleModel base DamageSub settlement audit R1

Date: 2026-10-06
Status: **CLOSED_BOUNDED_NO_RIDE_NATIVE_SETTLEMENT**

This audit supplements the accepted conditional reference. It directly compiles
the original DamageSub body transiently at all three established pins, with
only `_PETSKILL_BATTLE_MODEL` among later feature gates, a nonthrowing actor,
no ride pet, defined getters/setters and stubbed base reaction priority.
It does not identify an original build or reproduce all active descendant gates.

Each profile checks320 two-hit sequences, **640 native calls per profile,
1920 total**: ordinary/BattleModel marker, physical/nonphysical sentinel,
none/absorb/reflect/vanish/all-counter priority, zero/1/30/300 damage,
initial defender HP1/100 and1/2 charges. Both sequential HP/counter changes
and reported damage/reaction/ultimate values are checked. Direct DamageSub
calls after death isolate that function; they are not asserted to represent
reachable BattleModel helper calls, which recheck target life first.

## Remote acceptance — 2026-10-06

Action **37349075552 SUCCESS** on exact input
`33a8e76a988c441629e797defcc8095d77952e86`, tree
`1cb9731ed51d82c58e1e8da753afcddbc0d78af1`, reproduces640 native calls
per profile,1920 total. This closes only the reduced native contract stated
here. Full runtime, ride composition and flag-to-exit integration remain OPEN.

## Dated correction to earlier state interpretation

**FACT (bounded native descendant settlement):** marker-specific physical
reflection consumes its reflect charge, leaves both attacker and defender HP
unchanged, and reports the positive damage input unchanged. Therefore the
earlier state-audit sentence “damage remains on the defender” must not be read
as a defender HP subtraction. It is superseded by this correction. The native
settlement does not use ordinary reflected-return HP arithmetic.

Consequences for the separately accepted helper: reflected positive reported
damage can still wake the actual defender and reach the surviving-target status
check. The caller's HP loss and reported damage are distinct authoritative
values. Physical ABSORB heals and VANISH preserves HP while reporting positive
damage; both suppress wakeup but do not independently suppress status checks.
Nonphysical sentinel-1 bypasses selection and leaves all charges intact.

Raw damage >= maximum HP*1.2+20 can return ultimate2 even when reflection or
vanish preserves HP. The helper writes an ultimate entry flag independently
of its death presentation branch. Integration must reconcile this with the
accepted entry/exit lifecycle, rather than assuming every ultimate flag implies
HP0. Complete flag-to-exit integration remains OPEN.

## Source absent-ride read boundary

The marker reflection branch reads `CHAR_getInt(defpet,CHAR_HP)` even when
defpet=-1. The bounded native getter records that call and supplies a defined
zero witness; the value is unused in this no-ride HP settlement. Actual invalid
index behavior and original executable presentation are OPEN. A modern adapter
must avoid performing the invalid read, without claiming its value is restored.

Ride composition, throwing weapons, later reactions/transformations, real
reaction selection, AttackSeq/status probability, original integer command,
and full ordered/persistent/coordinator runtime are excluded from this audit.

Report: `research/recovered/STONEAGE-BATTLEMODEL-SETTLEMENT-SOURCE-AUDIT-R1.txt`.
Reproducer: `tools/stoneage_battlemodel_settlement_source_audit.py`.
Remote reproduction: `validate-stoneage-battlemodel-settlement.yml`.

**BATTLEMODEL_BASE_SETTLEMENT_AUDIT_R1 = CLOSED_BOUNDED_NO_RIDE_NATIVE_SETTLEMENT.**
