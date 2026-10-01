# StoneAge Stable Pet-Skill Core R1

Status: **active fixed-descendant stable subset reconstructed and regression-modeled**  
Scope: the 15 active pet-skill callbacks that are simultaneously:

1. present in the recovered active `petskill.txt`;
2. present in all three pinned descendant dispatch tables;
3. unguarded in all three dispatch tables;
4. implemented by substantive unguarded function bodies in all three pinned source lineages.

Pinned source revisions:

- gavinlinasd/StoneAge `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iriselia/StoneAge `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD/stoneage `999ffdf1d220ec6666eb65339180689c9caf1876`

This R1 layer is descendant-common evidence, **not proof that all 15 skills existed unchanged in the September/October 1999 launch build**.

## Active-table boundary

Recovered active `petskill.txt`:

- 147 rows;
- 69 unique callback tokens.

Textual fixed-source coverage:

- 65 tokens / 143 rows resolve in all three pinned source tables;
- 4 tokens / 4 rows resolve in none;
- no active token is only a one/two-lineage textual match.

That 65-token figure is **not** the common-core boundary.

Comment-aware guard classification gives:

- **15 unguarded-all-three tokens / 33 active rows**;
- **50 guarded-all-three tokens / 110 rows**;
- 0 mixed-guard;
- 0 partial-source;
- 4 all-source-missing / 4 rows.

Function-body refinement is unusually clean:

- **15 stable-body-all-three tokens / 33 rows**;
- 0 macro shells;
- 0 mixed body;
- 0 partial body source.

The four all-source-missing recovered rows remain quarantined as source/data skew. No behavior is invented for them.

## Stable active families

The 15 stable active callbacks are:

1. no action;
2. normal attack;
3. normal guard;
4. continuation attack;
5. charge attack;
6. guardian;
7. power balance;
8. mighty;
9. ordinary status-change attack;
10. earth round;
11. guard break;
12. abduct;
13. steal;
14. merge;
15. no-guard.

Active row counts by family:

- status change — 6;
- continuation attack — 4;
- charge — 3;
- power balance — 3;
- abduct — 3;
- no-guard — 3;
- mighty — 2;
- merge — 2;
- each remaining family — 1.

## Command-state architecture

Most ordinary pet skills do not execute their full effect inside `pet_skill.c`.

The handler writes battle command state:

- `CHAR_WORKBATTLECOM1` — command kind;
- `CHAR_WORKBATTLECOM2` — target slot;
- `CHAR_WORKBATTLECOM3` — packed skill parameters;
- `CHAR_WORKBATTLEMODE = BATTLE_CHARMODE_C_OK`.

The actual effect occurs later in battle command execution in `battle.c` / `battle_event.c`.

R1 therefore models both:

1. handler-side command encoding;
2. downstream stable execution behavior.

This avoids treating the callback function itself as the whole mechanic.

## PETSKILL_Use dispatch boundary

The fixed common dispatch wrapper was re-audited while connecting recovered
enemy AI skill execution.

Before calling a skill callback it:

1. reads the selected seven-slot pet-skill ID from the character;
2. resolves that ID to the pet-skill table row;
3. applies the base `ILLEGAL` check only when the actor is `CHAR_TYPEPET`;
4. resolves `FUNCNAME` and invokes the callback.

The common wrapper does **not** consume `FIELD`, `TARGET`, `COST` or MP
before dispatch. The optional `_PETSKILL_CHECKTYPE` gate is also restricted
to `CHAR_TYPEPET`; it does not add an enemy-side resource gate.

Therefore recovered enemy `wa` execution must preserve slot identity,
callback/OPTION semantics and callback-specific downstream battle state, but
must not invent an MP/COST deduction absent from this fixed enemy dispatch
path.

## None / attack / guard

The three simplest handlers only select ordinary battle commands:

- None -> `BATTLE_COM_NONE`;
- NormalAttack -> `BATTLE_COM_ATTACK`;
- NormalGuard -> `BATTLE_COM_GUARD`.

They set the target and command-ready mode.

## Continuation attack

The handler parses a leading integer attack count:

- valid range: 1..10;
- invalid/missing/out-of-range: 1.

It writes the count to the **low half** of COM3.

The high half is not cleared by the handler, so stale high-half state can survive even though this execution path does not consume it.

Execution:

```
attack_max = LOW(COM3)
gDamageDiv = attack_max
```

The normal attack loop then performs up to that many attacks and uses the attack count as the damage divisor.

So this is not simply “N full-damage attacks”; the fixed old combat layer explicitly sets `gDamageDiv=N`.

### Recovered25 execution closure

Recovered25 closes ContinuationAttack for enemy AI with **4 referenced IDs /
139 positive enemybase skill-slot uses**. All four OPTION rows are ASCII,
contain a leading integer accepted by the fixed 1..10 handler grammar, and
recover the four distinct counts **2, 3, 4, 5**.

The executable round model preserves the fixed loop rather than multiplying a
single-hit result:

- `BATTLE_COM_S_RENZOKU=1001`;
- LOW(COM3) supplies both `attack_max` and `gDamageDiv`;
- the positive-damage division occurs after AttackSeq-shaped
  dodge/critical/GUARD/Guardian work and before DamageSub-shaped reactions and
  ride sharing;
- non-bow TargetListSet repeats the submitted original COM2, so once that
  original target is dead each later hit independently writes it back and can
  consume a fresh DefaultAttacker retarget roll;
- Guardian, reaction, ride/petfall, wakeup and death/ultimate consequences are
  applied per hit and therefore affect later hits;
- only the final BATTLE_Attack continuation state and final counter target feed
  the post-loop counter chain.

Recovered runtime admission uses explicit `ContinuationAttackRolls` with one
ordinary-attack RNG bundle per hit and rejects missing/extra actor mappings.
The historical LOW-only handler write remains documented; for recovered enemy
admission the otherwise inactive HIGH half is initialized to zero rather than
inventing previous COM3 residue.

Validation closes the full route through the ordinary resolver, persistent
battle state, recovered enemy `wa[n]` bridge and coordinator. The end-to-end
coordinator run is **36825205100 = PASS**, the full recovered25
region/runtime-stack run is **36825205097 = PASS**, and the final battle-core /
Taiwan gameplay regression runs are **36825541838 / 36825541884 = PASS**.

## Charge attack

The handler encodes:

- LOW(COM3): charge wait count N, range 1..10, default 1;
- HIGH(COM3): optional attack-percent parameter, default 0.

Each `BATTLE_Charge` execution step behaves as follows:

- while LOW > 0: decrement LOW by one and perform no action;
- when LOW <= 0:
  - rebuild attack power;
  - switch command to `BATTLE_COM_S_CHARGE_OK`.

Ready attack power is:

```
FIXSTR + FIXSTR * attack_percent * 0.01 + MODATTACK
```

The subsequent CHARGE_OK action enters the ordinary attack path and then resets the command.

N=1 therefore means one no-action charge turn before the ready attack.

Recovered25 execution closure adds:

- **3** enemy-referenced ChargeAttack IDs accounting for **90** positive enemybase skill-slot uses;
- strict CP950/Big5 agreement for all three OPTION rows;
- **3/3** valid leading wait counts, spanning **1..3**;
- **3/3** numeric `攻%` values, spanning **90..150**;
- persistent S_CHARGE command/countdown state across rounds;
- carry-aware enemy AI suppression so no fresh mode/target roll is consumed while charging;
- automatic S_CHARGE_OK promotion and ordinary physical execution when the countdown reaches zero.

Recovered enemy ready power uses the preserved birth FIXSTR-equivalent attack
projection with `MODATTACK=0`; an unproven enemy equipment/modifier layer is
not synthesized. Malformed or out-of-range recovered OPTION grammar fails
closed.

## Guardian

Guardian can immediately modify the pet’s attack and defense work powers using optional percent parameters:

```
new = FIXED + FIXED * percent / 100
```

It sets `CHAR_BATTLEFLG_GUARDIAN` and registers a guardian slot in the battle entry table.

Two modes exist.

### Guardian attack mode

Default mode uses `BATTLE_COM_S_GUARDIAN_ATTACK` and typically registers the pet as guardian for its paired owner position.

### Defensive guardian mode

When the option contains the defensive COM marker, the skill switches to ordinary guard and registers the selected target as the guarded entry.

### Guardian redirect checks

Attack redirection only succeeds when the registered guardian:

- exists;
- is alive;
- still has the guardian flag;
- is not the defended slot itself;
- is not sleeping;
- is not confused;
- is not paralyzed;
- is not petrified;
- is not under the ordinary barrier status;
- is not the attacker;
- is not trying to intercept a thrown-weapon attack.

Guardian entries and guardian flags are cleared during battle pre-command setup, so registration is turn-local rather than permanent state.

The fixed physical execution order is now connected end-to-end:

1. dodge is checked against the original target;
2. Guardian eligibility is checked;
3. successful interception replaces the physical defender before critical/damage;
4. wake-up and ordinary physical status application use that final defender;
5. a successful Guardian interception forces the attack continuation flag false, so the ordinary counter chain does not start from the intercepted hit.

The stable enum value `BATTLE_COM_S_GUARDIAN_GUARD=1004` is present in all three pinned headers but has no common executable occurrence. The actual defensive Guardian handler writes ordinary `BATTLE_COM_GUARD` and stores the guardian registration separately. R1 preserves that split rather than inventing an execution path for 1004.

## Power balance

The handler selects `BATTLE_COM_S_POWERBALANCE` and can immediately modify:

- attack power;
- defense power.

Optional attack/defense percentages use the same:

```
FIXED + FIXED * percent / 100
```

If the skill option pointer is null, the old handler returns FALSE **after** it has already written command/target/mode state.

When valid, PowerBalance later participates in the normal attack execution path.

Recovered25 runtime closure adds a narrower data-backed execution boundary:

- all **3** enemy-referenced PowerBalance skill IDs decode identically under strict CP950 and Big5;
- all **3/3** OPTION rows contain both the attack (`攻%`) and defense (`防%`) percentage markers;
- **0/3** rows contain the later/unclosed dexterity-extension marker (`敏%`);
- the recovered enemy birth projection supplies the FIXSTR/FIXTOUGH-equivalent attack/defense basis;
- `BATTLE_COM_S_POWERBALANCE=1007` is carried into the ordinary physical attack path with the handler's immediate work attack/defense mutations kept as explicit command-setup effects.

Recovered25 execution therefore fails closed if that proven marker grammar is not satisfied; no generalized PowerBalance extension parser is inferred.

## Mighty

The handler packs:

- LOW(COM3): damage multiplier ×100;
- HIGH(COM3): dodge modifier.

A significant old quirk is preserved.

The source initializes:

```
float fBai = 2.00;
int iBai = 0;
```

but only assigns `iBai = fBai * 100` when the multiplier marker is actually found.

Therefore an option missing the multiplier marker leaves LOW(COM3)=0, even though `fBai` had a nominal 2.00 default.

Execution then does:

```
gBattleDamageModyfy = LOW(COM3) * 0.01
gBattleDuckModyfy   = HIGH(COM3)
```

So missing the multiplier marker can produce a zero damage multiplier in this fixed implementation.

The fixed physical executor also pins the application order:

1. HIGH(COM3) is loaded into the action-local dodge modifier before target dodge is checked;
2. the dodge modifier is added in percentage points before the source converts the probability to its per-10000 scale;
3. LOW(COM3) becomes the action-local damage multiplier;
4. that multiplier is applied after critical/base damage, GUARD adjustment, minimum-damage handling and Guardian zero-damage correction;
5. it is applied before damage-reaction and later ride-pet sharing consume the resulting damage;
6. both Mighty globals are reset before the ordinary counter chain, so counters do not inherit the initiating Mighty modifiers.

This makes Mighty a single-hit ordinary physical specialization, not a multi-hit or persistent-status mechanic.

Recovered25 runtime closure further proves:

- **2** enemy-referenced Mighty skill IDs account for **120** positive enemybase skill-slot uses;
- both OPTION rows decode identically under strict CP950 and Big5;
- **2/2** contain the `倍` multiplier marker and **2/2** contain the `避` dodge marker;
- **2/2** pass strict numeric parsing for both values;
- recovered enemy execution rejects missing/malformed marker or numeric grammar rather than relying on the handler's old default quirk;
- `BATTLE_COM_S_MIGHTY=1006` is now carried end-to-end through the ordinary physical round without leaking its modifiers into counters.

## Ordinary status-change attack

The handler:

- selects `BATTLE_COM_S_STATUSCHANGE`;
- scans ordinary status tokens;
- defaults turn count to 3;
- optionally adjusts attack/defense work powers;
- packs status in LOW(COM3);
- packs turn in HIGH(COM3).

### Invalid-status sentinel quirk

The old handler stores the loop variable `i`, not the separate `status` variable.

If no status token matches, `i` reaches `BATTLE_ST_END` and that sentinel value is still packed into LOW(COM3).

The later status checker rejects statuses outside the valid ordinary range.

### Status application

Before attack execution, COM3 is copied into global status/turn state.

The status can only be applied when the physical attack actually causes positive damage.

The stable `BATTLE_StatusAttackCheck` rejects application when the target already has any ordinary status.

Paralysis uses its special base:

```
20 - status-specific resistance
```

Other ordinary statuses use the fixed-base relationship:

```
PerOffset
+ clamped level delta * multiplier
+ attacker fixed luck
- status-specific resistance
- vitality-ratio penalty
```

For ordinary pet StatusChange attacks, the enclosing `BATTLE_Attack()` path
initializes the common status-hit base (`suitpoison` / `PerOffset`) to **30**
before the command-specific status and turn are read from COM3. Therefore the
stable base pet path uses **PerOffset=30, Range=40, Bai=2.0**.

The earlier reference-model default of zero for this pet path was incorrect.
The implementation now delegates the arithmetic to the shared base-status core
in `tools/stoneage_battle_status_model.py`; a different offset is accepted
only when a separately proven versioned source explicitly supplies one.

where the vitality penalty is based on:

```
(VITAL / (VITAL + STR + TOUGH + DEX)) / 0.25 * 10
```

The normal non-PvP level term is clamped to ±40 in this call path and uses multiplier 2.0.

The stable core caps the final chance at 80 but does not add a corresponding lower clamp.

When application succeeds, the work timer is first written as:

```
requested_turn + 1
```

The physical attack path then has an additional stable DRUNK quirk: the
just-written drunk counter is immediately divided by two with integer
arithmetic. Ordinary magic/item StatusChange does not use this physical
post-write adjustment; those paths write their requested turn directly.

Selected immobilizing statuses also clear the target’s pending command.

Later suit/equipment resistance additions remain macro/version layers and are not part of this base probability model.

Shared-core correction validated at commit
`c06bff3e10610cb7b035ccb847bf235ecf620f37`: pet-skill run
**35672999246**, battle-core **35672998977**, ordinary-magic
**35672999058**, and item-effect **35672998940** all succeeded.

## Earth round

EarthRound is a two-phase state machine.

### Phase 1 — hide

The handler selects `BATTLE_COM_S_EARTHROUND1`.

The execution helper:

- emits the hide/backstep state;
- clears `CHAR_ISATTACKED`;
- changes the command to `BATTLE_COM_S_EARTHROUND0`;
- returns FALSE in the fixed helper because its local result flag is never changed.

### Phase 2 — attack

`BATTLE_COM_S_EARTHROUND0` enters the ordinary attack path with:

```
gBattleDamageModyfy = 1.0 + 0.01 * COM3
```

After the attack it resets the command to NONE.

### COM3 stale-state hazard

The EarthRound handler writes COM3 only if its attack-percent marker exists.

If the marker is absent, the entire previous COM3 value survives and becomes the later EarthRound damage percentage.

R1 preserves this historical state-residue behavior rather than clearing COM3 defensively.

### Recovered25 execution closure

Recovered25 closes EarthRound for enemy AI with **1 referenced ID / 14 positive
enemybase skill-slot uses**. Its OPTION is non-ASCII but strict CP950 and Big5
decoding agree exactly. The bundle-backed hard probe proves the only recovered
row contains one numeric `攻%` marker and that its value is exactly **90**.

That recovered row therefore always overwrites the full COM3 with **90** before
phase 1; the historical stale-COM3 branch remains part of the stable generic
model, but is not reachable from this recovered25 row.

The executable two-round path preserves the fixed command state:

- phase 1 selects `BATTLE_COM_S_EARTHROUND1=1010`, emits hide/no-action, and
  carries `BATTLE_COM_S_EARTHROUND0=1009` with the original COM2/COM3;
- `BATTLE_AllCharaCWaitSet`-shaped persistence prevents a new command/AI
  decision from replacing that carried phase-2 command;
- phase 2 enters the ordinary physical path, applies
  `1.0 + 0.01 * COM3 = 1.90` after guard/minimum-damage/Guardian zero-damage
  handling, and then clears the command to NONE;
- the multiplier is action-local and is reset before the ordinary counter
  chain, so counters do not inherit the EarthRound multiplier.

Recovered runtime admission fails closed if the callback population, codec
agreement, marker grammar, or the exact **90** percentage drifts.

## Guard break

GuardBreak selects `BATTLE_COM_S_GBREAK=1002` and can immediately raise/lower attack power via an optional attack-percent marker.

Execution target-adjusts and invokes `BATTLE_S_GBreak`. The fixed order is unusual:

1. `BATTLE_AttackSeq` performs dodge / Guardian / critical / base-damage work first;
2. GuardBreak bypasses ordinary GUARD damage reduction inside AttackSeq;
3. `BATTLE_S_GBreak` then checks the **original target**;
4. damage is kept only if that target is using ordinary GUARD and is not confused;
5. otherwise damage is forced to zero and the result becomes MISS.

A fixed-source Guardian quirk is preserved: AttackSeq can calculate damage
against the redirected Guardian, but `BATTLE_S_GBreak` still passes the
original guarded target into `BATTLE_DamageSub`, so HP/reaction settlement
belongs to that original target.

Recovered25 narrows this further:

- **1** enemy-referenced GuardBreak skill ID accounts for **60** skill-slot uses;
- the OPTION bytes are **1/1 ASCII-only**;
- the fixed handler's optional marker `攻%` is non-ASCII, so **0/1** recovered rows can activate the attack-percent rewrite;
- recovered execution therefore uses the preserved enemy birth FIXSTR-equivalent attack projection unchanged and fails closed outside this proven ASCII-only subset.

This makes the ordinary GuardBreak family a conditional anti-guard strike, not a general armor-piercing attack.

## Abduct

The handler stores the pet-skill array index in the low half of COM3 and leaves
the high half untouched.

A later audit corrected the earlier claim that `_BATTLE_ABDUCTII` was outside
the fixed common build. All three pinned descendant `version.h` files define
both **`_BATTLE_ABDUCTII`** and **`_PETSKILL_OPTIMUM`**, so the active fixed
semantics include the AI-threshold branch.

`_PETSKILL_OPTIMUM` loads each row directly at its pet-skill ID table index.
`PETSKILL_getPetskillArray(id)` therefore resolves the active fixed
`array` to that ID, allowing the handler's LOW(COM3) value to be reconstructed
from recovered skill identity rather than guessed from file line order.

The active fixed `BATTLE_Abduct` accepts PET or ENEMY attackers and rejects a
PLAYER defender before any attempt. It obtains:

```
AiPer = atoi(PETSKILL_OPTION)
```

Probability then branches as follows:

- if `AiPer <= 0` **or** the defender is not PET, use the old level formula:
  `int((defender_level - attacker_level) * 0.6 + 30)`, clamped to a
  **minimum 50**;
- if the defender is PET and `AiPer > 0`, bypass that formula and set
  `per=200` only when `defender FIXAI < AiPer`; otherwise set `per=0`;
- a non-null battle WinFunc subsequently forces `per=0`.

For an otherwise valid non-player attempt, `RAND(1,100) < per` determines
success. A successful PET target causes `BATTLE_PetDefaultExit` for its owner;
a successful ENEMY target receives `BATTLE_Exit`. The attacker then exits
battle whether that valid roll succeeded or failed. A PLAYER target returns
before the attempt and therefore does **not** trigger attacker exit.

### Recovered25 execution closure

Recovered25 closes Abduct for enemy AI with **2 referenced IDs / 14 positive
enemybase skill-slot uses**. Both OPTION rows are ASCII. The hard bundle probe
finds exactly one leading integer, exactly one positive `atoi(OPTION)`, and
the exact threshold population **{0,80}**; runtime admission rejects any
population drift.

The executable command is **`BATTLE_COM_S_ABDUCT=1012`**. The stable round
bridge preserves the skill ID in LOW(COM3), initializes the inactive HIGH half
to zero for recovered enemy submission, and performs the fixed
`BATTLE_TargetAdjust`-shaped target check before the Abduct transition.

Battle participants now preserve recovered FIXAI where available. A valid
non-player attempt consumes explicit `RAND(1,100)`; PLAYER targets consume no
Abduct success roll. Non-death Abduct exits are persisted separately from
capture/escape removal and from death/ultimate exit: the affected pet/enemy
identity and HP remain in the battle session, but that entry is excluded from
later rounds and produces no kill EXP/drop profit.

The end-to-end recovered path is therefore:
`enemy wa[n] -> PETSKILL_Abduct -> S_ABDUCT -> explicit target/RNG -> persistent
battle-entry exit`. Special battles carrying a non-null WinFunc remain outside
the admitted ordinary local-group seam rather than being synthesized.

This supersedes the earlier R1 text that treated ABDUCTII as an inactive later
extension.

## Steal

The stable old `BATTLE_Steal` is narrower and stranger than its name suggests.

Target entry chance:

- player target: 50;
- non-player target: 0.

On a successful entry roll, a second 50% split chooses gold vs item mode.

### Gold mode

The target loses:

```
target_gold * RAND(8,12) * 0.01
```

If the result is <=0, the steal becomes failure.

The fixed implementation shown in all three lineages subtracts the gold from the target but does **not** credit matching gold to the stealing pet or owner in this function.

### Item mode

One occupied ordinary inventory slot is selected.

The target slot is cleared and the item instance is ended.

The fixed function does **not** transfer that item into the attacker’s inventory.

Thus the old “steal” implementation behaves as target asset removal/destruction, not a conventional transfer, at this source layer.

When steal remains successful, the stealing pet/enemy exits battle.

Bismarck uses a revised inventory upper-bound helper while preserving the same success/mode/removal semantics; that bound implementation is treated as descendant implementation drift rather than a different core action.

## Merge

Merge is unusual because it is an unguarded pet-skill callback that delegates to field/item logic rather than a battle command.

It checks the pet owner’s battle mode.

If the owner is in battle, the call fails.

Otherwise it delegates to:

```
ITEM_mergeItem_merge(owner, pet_id, data, pet_index, 0)
```

and returns that result.

### Recovered enemy-AI hazard

The recovered25 enemybase references cannot be treated as a normal battle command.

The fixed common enemy `BATTLE_ai_normal` `wa[n]` path calls:

```
PETSKILL_Use(enemy, skill_slot, target, NULL)
```

directly. It does **not** filter on `PETSKILL_FIELD`. The active
`_PETSKILL_CHECKTYPE` guard also applies only to `CHAR_TYPEPET`, not
`CHAR_TYPEENEMY`.

Ordinary enemies are initialized with all work integers at zero and do not
replace `CHAR_WORKPLAYERINDEX`, so Merge reads global character index **0**
as its nominal owner.

With `data == NULL`, the delimiter helper is NULL-safe but yields at most one
empty/zero material token. Therefore `ITEM_mergeItem_merge` reaches
`cnt <= 1` and never enters the real merge transaction.

The two earlier fixed descendants (gavinlinasd and iriselia) then fall off the
end of this non-void `int` function without returning a value. The resulting
garbage return controls whether `BATTLE_ai_normal` leaves the enemy in
`C_WAIT` or promotes it to `C_OK + COM_NONE`; that distinction is observable
because `BATTLE_Battling` skips actors not in `C_OK`, including their later
per-actor status sequence.

Bismarck explicitly repairs the function by moving/adding a final
`return result;` outside `if (cnt > 1)`, making this same NULL-data path
deterministically FALSE. That is treated as descendant bug-fix evidence, not
retroactive proof that the earlier binaries had deterministic FALSE semantics.

Accordingly, recovered enemy Merge remains a **historical undefined-behavior
boundary** and is intentionally fail-closed in the modern runtime. We do not
replay global-character-index-0 side effects or invent one ABI/compiler's
garbage return value.

This stable descendant callback must not be conflated automatically with later
macro-gated pet-fusion/egg systems; historical introduction still requires
earlier evidence.

## NoGuard

The handler parses and packs:

- HIGH(COM3): dodge value;
- LOW(COM3): `(counter << 8) + critical`.

The counter token is a simplified/traditional text variant across lineages; the packing algorithm is the same.

### Own-turn NoAction, cross-action COM3 effects

The stable `battle.c` command switch for `BATTLE_COM_S_NOGUARD` does call:

```
BATTLE_NoAction(...)
```

for the actor's own command turn. However, that does **not** make the packed
parameters dead. All three pinned lineages also read the still-selected
`S_NOGUARD` command in `battle_event.c`:

- when the NoGuard actor is the defender, `HIGH(COM3)` is added to the dodge
  probability before the 1..10000 dodge roll;
- when the NoGuard actor participates in the counter path, the upper byte of
  `LOW(COM3)` is added to the counter probability;
- `BATTLE_Counter` explicitly admits both ordinary ATTACK and S_NOGUARD as
  counter-capable command states.

The byte modifier uses the fixed-source quirk:

```
if (value > 127) value *= -1;
```

rather than a conventional signed-byte conversion.

The lower byte of LOW(COM3), nominally the critical modifier, is read by a
`BATTLE_CriticalCheckPet` helper present identically in the pinned lineages,
but that helper is enclosed in `#if 0`; the active common critical path calls
`BATTLE_CriticalCheckPlayer` instead. R1 therefore records the packed critical
byte as a **disabled-path** value, not as an active modifier.

This corrects the earlier R1 statement that NoGuard COM3 parameters had no
other fixed common consumers.

### High-half residue

The handler only writes HIGH(COM3) when the dodge marker exists.

Without it, the previous high half remains and therefore can directly affect
the later defending dodge calculation.

LOW is always overwritten by the packed counter/critical value.

### Recovered25 execution closure

Recovered25 closes NoGuard for enemy AI with **3 referenced IDs / 74 positive
enemybase skill-slot uses**. All three OPTION rows have strict CP950/Big5
agreement and use the traditional numeric `避% / 擊% / 心%` grammar. The
recovered value ranges are dodge **30..50**, counter **50..70**, and critical
**20..40**; no recovered row uses simplified `击%`.

The round core preserves S_NOGUARD as the selected same-round command after its
own NoAction event. HIGH(COM3) is therefore still visible to later defending
dodge checks, and the upper byte of LOW(COM3) is still visible when the actor
enters the non-player counter path. The disabled critical byte remains packed
but has no active consumer. This closure adds no cross-round state.

## COM3 residue as a historical implementation property

Several stable handlers use halfword setters rather than resetting the full field:

- ContinuationAttack overwrites LOW only;
- Abduct overwrites LOW only;
- NoGuard conditionally overwrites HIGH;
- EarthRound can leave the entire COM3 untouched.

These stale values are usually irrelevant to the immediate command, but EarthRound can consume stale full COM3 as a damage percentage.

A modern implementation should almost certainly use typed per-command state rather than a reused packed integer, but that is a redesign decision, not a historical reconstruction.

## Excluded pet-skill layer

Active recovered rows outside this R1 core include 50 all-three guarded callback families / 110 rows.

Examples include later feature-macro families for:

- attack magic;
- super-wall/magic status;
- guard-break variants;
- alchemy/fixing;
- mount/fall-ground;
- explosion;
- steal-money revision;
- extended enemy skills;
- timid/property/tear/light-take/crazed/shoot attacks;
- MP damage;
- deep poison;
- barrier;
- silence/no-cast;
- roar/SARS/sonic;
- transformations;
- combined/divide/bat-fly/battle-model families.

Their presence in the mixed recovered 2.5 table is valid content evidence, but they are not flattened into the stable common layer.

The four active all-source-missing callback rows remain quarantined.

## Reference model and validation

Artifacts:

- `tools/stoneage_petskill_core_model.py`
- `tools/stoneage_petskill_round_bridge.py`
- `tests/test_stoneage_petskill_core_model.py`
- `tests/test_stoneage_petskill_round_bridge.py`
- `.github/workflows/validate-stoneage-petskill-core.yml`
- `tools/stoneage_effect_callback_coverage_probe.py`
- `research/recovered/STONEAGE-25-EFFECT-CALLBACK-COVERAGE-R1.txt`

The model separates:

- handler-side command encoding;
- stable battle-execution transitions;
- injected random outcomes;
- later/macro extensions.

Initial dedicated CI run `35374550333` passed 44 tests.

After edge corrections for invalid-status sentinel, steal destruction semantics, and COM3 residue, run `35374921866` passed **50 deterministic tests**. Report-trigger rerun `35375022224` also completed successfully.

The round bridge and shared Guardian/status integration were subsequently validated by pet-skill run **35689840680** and battle-core run **35689840660** at `2fa7c2bde4ca882a2275f507d6f2a0e6f3a3d514`. The later Combo/status integration remained compatible in pet-skill run **35690533578**.

## Evidence boundary

- **FACT:** 15 active callback tokens / 33 rows are unguarded and substantive in all three fixed descendant lineages.
- **FACT:** 50 active tokens / 110 rows are guarded in all three.
- **FACT:** four active rows use callbacks absent from all three fixed source tables.
- **FACT:** the core handler formulas and key execution formulas above converge across the three pinned lineages, with text/format variants such as simplified/traditional option markers and Bismarck inventory-bound refactoring.
- **VERSIONED:** macro-gated pet skills remain explicit version layers.
- **OPEN:** which of the 15 stable-descendant skills existed in exactly this form in 1999/JSS and early 1.x.
