# StoneAge PETSKILL_BecomeFox ordered runtime R1

Status: **CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME**  
Date: 2026-10-06  
Scope: recovered25 positive enemy uses of `PETSKILL_BecomeFox` / ID 625 only.

## 1. Evidence boundary

This runtime is downstream of the accepted bounded BecomeFox reference:

- exact recovered25 callback population: ID **625** only;
- FIELD **1**, TARGET **1**, COST **2**, ILLEGAL **3000**;
- exact positive enemy references: **2 slot uses / 2 templates**;
- both positive references are enemybase **PETSKILL3**:
  TEMPNO 148 and 149;
- recovered OPTION length **0**, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- template 148: IMG 101743, base 32/40/26/30, MODAI 150;
- template 149: IMG 101744, base 28/45/22/32, MODAI 150;
- transformed fox image **101749**;
- the post-attack success threshold is `rand()%100 < 31`.

No recovered-original executable profile is inferred from the descendant sources.

## 2. Explicit descendant profiles

The caller must select one descendant source profile explicitly:
`gavin`, `iris`, or `bismarck`.

The profiles share the bounded transform/lifetime behavior used here but retain
two source divergences:

- gavin/iris reject ARRANGE before the BecomeFox draw;
- fixed Bismarck lacks that active ARRANGE rejection;
- gavin/iris PetIn reads FOXROUND through the ordinary-int accessor;
- Bismarck PetIn reads FOXROUND through the work-int accessor.

The PetIn divergence remains open and is not resolved by this runtime.

## 3. Exact post-attack gate

The exact descendant post-attack block was extracted and executed in a native
oracle against the model for **3840 vectors**: 1280 per pinned source profile.

The bounded gate preserves source ordering:

1. main physical AttackSeq result is observed;
2. MISS/DODGE/ALLGUARD reject before the BecomeFox draw;
3. gavin/iris also reject ARRANGE before the draw;
4. the one reduced draw is consumed only on the reached path;
5. the source threshold is strictly `draw < 31`;
6. target liveness is tested after the physical/counter chain;
7. player targets reject after draw consumption;
8. non-player success requires the explicit PETFLG witness;
9. the attacker pig marker remains an explicit witness;
10. success writes FOXROUND/current turn and the fox image.

`BATTLE_Counter()` calls `BATTLE_AttackSeq()` directly and does not overwrite
`Battle_Attack_ReturnData_x`. Therefore the BecomeFox result gate owns the main
attack result even when a counter chain ran. Guardian redirection settles damage
on the guardian but does not replace the original BecomeFox target identity.

## 4. Ordered action and FOXROUND lifetime

The historical numeric enum value of `BATTLE_COM_S_BECOMEFOX` is not proven.
R1 uses a reconstruction-only internal command token for scheduling identity and
never promotes that number as recovered historical data.

A fresh transform changes FOXROUND/image state only. It does **not** immediately
rewrite fixed work powers. At the transformed actor's own later action boundary:

- FIXSTR work attack becomes C-truncated 80 percent;
- FIXTOUGH work defense becomes C-truncated 80 percent;
- FIXDEX work quick becomes C-truncated 80 percent;
- ATTACK, GUARD and NONE remain admitted;
- other special commands are demoted to NONE in this bounded runtime.

Recovery is post-action and strict:
`currentTurn - foxRound > 2`. The expiring actor therefore still executes that
action with reduced work powers, then returns to its fixed baseline powers.

The source's earlier fox-specific DexCalc write is not treated as an additional
initiative penalty: exact pinned control flow showed ATTACK/GUARD/NONE fall
through to default DexCalc and overwrite that preliminary value.

## 5. Persistent multi-round state

`PersistentBattleState` carries only active FOXROUND entries in a
`BecomeFoxRuntimeOverlay`.

The overlay stores the **actual current work values**, not a derived
"is foxed => recompute 80 percent" flag. This preserves source chronology:

- if the target is transformed before its own action, that action writes and
  persists reduced work values;
- if the target already acted before it is transformed, its current work values
  remain unreduced until its next action boundary.

Normal dead entries may retain FOXROUND while they remain battle entries.
Ordinary/ultimate battle exits and session removal filter the overlay. Battle
termination and player escape clear it. An empty overlay is canonicalized to
`None` so unrelated runtime scopes cannot mistake an empty container for an
active transformation.

## 6. Recovered enemy-AI and coordinator admission

`resolve_enemy_ai_becomefox_submission` revalidates:

- exact callback population ID625;
- exact recovered row metadata and empty OPTION identity;
- actor TEMPNO 148 or 149;
- exact graphic/base-stat/MODAI identity;
- selected runtime index2/report slot3;
- enemy actor provenance;
- explicit descendant source profile.

The local runtime coordinator admits BecomeFox only when recovered common enemy
AI actually selects that `wa` slot. COM2 remains the selected source target.

The following runtime witnesses remain explicit and fail closed:

- one reduced `rand()%100` draw per selected caster;
- one attacker pig marker per selected caster;
- PETFLG provenance for each selected pet target;
- base-image provenance for each newly transformed pet target.

Surplus, missing or mis-keyed witnesses are rejected before round execution.

## 7. Fail-closed interaction boundary

The ordered runtime deliberately excludes unsupported composition rather than
inventing source order. In particular:

- active/selected actors are bounded to the admitted no-equipment-critical FIST
  physical profile;
- selected BecomeFox or an active FOXROUND overlay rejects any supplied ride
  runtime, mounted or unmounted; active overlay entries also reject a nonnegative
  ride selection marker;
- PetIn FOXROUND behavior is not integrated;
- wider equipment/critical interactions are not generalized;
- another semantic callback cannot own the same actor action;
- no original PRNG implementation is inferred from the reduced draw witness.

These are R1 boundaries, not claims that historical descendants could never
combine those systems.

## 8. Explicitly open boundaries

R1 does **not** establish:

- which descendant profile matches the recovered original executable;
- recovered-original numeric `BATTLE_COM_S_BECOMEFOX`;
- original PRNG implementation/sequence identity;
- gavin/iris versus Bismarck PetIn accessor as original truth;
- ride-bearing transform/restore lifecycle;
- wider weapon/equipment/critical composition;
- original JSS/Taiwan-v1 membership or introduction date;
- client presentation/name text outside the recovered server facts.

## 9. Acceptance gates

The runtime closure requires all of the following to remain successful:

- exact pinned source-order audit;
- exact native post-attack oracle: **3840 vectors**;
- exact ID625 recovered25 admission + FOXROUND unit gate;
- ordered ordinary-round integration gate;
- persistent multi-round FOXROUND gate;
- local session coordinator end-to-end ID625 enemy-AI gate;
- full local runtime coordinator regression;
- runtime golden contract;
- full recovered25 region/runtime-stack gate;
- complete verified pet-skill pressure reclassification.

Final pressure may promote only the exact two recovered25 positive ID625
placements. PetIn, ride/equipment composition and historical-origin questions
remain separate open axes.

**RECOVERED25_BECOMEFOX_ORDERED_RUNTIME_R1 =
CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.**
