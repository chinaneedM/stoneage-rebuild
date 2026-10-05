# StoneAge PETSKILL_BatFly reference R1

Status: **CLOSED_BOUNDED_FIXED_DESCENDANT_REFERENCE**
Date: 2026-10-05

## Recovered25 population

Verified recovered25 data contains exactly one callback row:

- ID **633**
- callback `PETSKILL_BatFly`
- FIELD **1**
- TARGET **3**
- COST **2**
- ILLEGAL **5000**
- OPTION length **0**
- OPTION SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

TARGET 3 is independently recovered from fixed descendant `pet_skill.h` as
`PETSKILL_TARGET_ALLOTHERSIDE`.

The complete positive recovered25 placement is one template with two slots:

- TEMPNO **1160**
- graphic **101815**
- base V/S/T/D **300 / 1 / 1 / 30**
- AI **100**
- one-based skill slots **1 and 4**
- both slots carry ID633

The first verified discovery gate is Action **37324003345 PASS**. The
second-pass exact-pin gate is Action **37324573414 PASS**. The accepted
derived report is
`research/recovered/STONEAGE-25-BATFLY-PROBE-R1.txt` on this branch.

## Fixed descendant callback and dispatcher

Pinned source profiles:

- gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`

All three retain the same semantic callback:

- COM1 is set to symbolic `BATTLE_COM_S_BAT_FLY`;
- COM2 stores the selected target;
- battle mode becomes `BATTLE_CHARMODE_C_OK`;
- LOW(COM3) stores the skill array/index;
- callback code consumes no OPTION and no RNG.

The dispatcher first calls `BATTLE_TargetAdjust`. If no living target exists,
it performs `BATTLE_NoAction`; otherwise it calls
`BATTLE_BatFly(battleindex, attackNo, myside)`. The adjusted single target is
therefore only an execution-validity gate. The effect itself rebuilds the
entire opposing side and does not consume that adjusted target as the damage
recipient.

Numeric descendant command values are profile-dependent:

- gavin/iris fixed profiles enable `_PETSKILL_LER` and produce command 2108;
- the pinned Bismarck server profile leaves `_PETSKILL_LER` inactive; when
  conditionally compiled for the audit its enum position produces 2047.

Under DD-019 these numbers do not identify the unresolved original build COM1.

## Target set and target ordering

BatFly calls ordinary `BATTLE_MultiList` with the entire opposing side.
That side-list path calls `BATTLE_TargetCheck`, which rejects invalid
entries, dead actors and actors with HP <= 0. BatFly does not call
`BATTLE_MultiListDead`.

The side-list path itself owns no RNG. An unrelated single-target branch inside
`BATTLE_MultiList` can use `rand()%10` when retargeting, but BatFly's side
constant does not enter that branch.

With the attack-magic profile active, multi-target lists call `qsort` through
the shared `SortLoc`/position table. The preserved side-0 comparator contains
the anomalous expression `ele2basex - ele1basey`. Because that comparator is
not treated as a portable strict ordering contract across libc/qsort
implementations, **R1 does not claim an exact original presentation/BD event
order**. The gameplay state transform is order-independent for the admitted
BatFly domain.

## HP transfer semantics

For each living target-side battle entry:

### No living ride pet

If `BATTLE_getRidePet(target)` returns no valid living pet:

- if target HP / 10 truncates to zero, drain exactly **1 HP**;
- otherwise drain **floor(current HP / 10)**.

This can reduce a 1-HP target to 0.

### Living ride pet

The common ride lookup is player-only in the recovered battle model. A
player riding a living pet therefore splits BatFly into two independent
current-HP drains:

- rider: **floor(current HP / 20)**, minimum 1;
- ride pet: **floor(current HP / 20)**, minimum 1.

If the ride pet reaches HP <= 0, the source clears `CHAR_RIDEPET`, updates
the ride image and sets `CHAR_WORKPETFALL=1`.

An allied pet battle entry is not a player rider and therefore follows the
ordinary 10% branch. The separately mounted ride pet is not an active battle
entry; it receives only the paired 5% drain through its player rider.

### Attacker healing

Every drained rider/entry/ride-pet amount is summed into `addhp`. After all
targets have been processed:

- if attacker HP + total drain <= max HP, attacker gains the full sum and the
  reported heal is that sum;
- if attacker HP + total drain > max HP, attacker HP is capped at max HP and
  the source resets the *reported* `addhp` to **0**.

Thus overflow can produce a positive actual heal but a zero reported heal.
This quirk is preserved.

The effect owns no ordinary attack sequence, dodge, critical, defense,
attribute, reaction, counter or RNG path.

## Protocol/visual helper

`PROFESSION_MAGIC_ATTAIC_Effect` is called before the HP loop. In this path
the pinned helper only emits battle protocol/visual commands and target ids; it
does not mutate HP or work state.

Pinned source variants disagree on certain Ler visual ids
(`_FIX_LER_IMG`), but those visual differences do not change BatFly HP
semantics.

## Neighboring Ler lifecycle is not BatFly

The same compile feature also contains special handling for graphics 101813
and 101814:

- resistance to battle-fly/ultimate knock-out paths;
- death-time `BATTLE_LerChange` transformation.

The sole recovered25 BatFly-positive template is graphic **101815**, not
101813/101814. Therefore R1 does **not** import those transformation or
anti-knockout semantics into ID633 merely because they share
`_PETSKILL_LER`.

## Native equivalence evidence

Final source/native gate **37328006584 PASS**. Each of the three pinned source
profiles runs **249 native HP vectors**, for **747 native vectors total**,
against the Python reference model. The accepted report is
`research/recovered/STONEAGE-BATFLY-SOURCE-AUDIT-R1.txt`, most recently
derived by bot commit
`db9dbef799e4fc08a28d7db7e5b22c7a3ffc3c4b` before the final comparator
boundary rerun.

The reference tests cover callback setup, 10% and 5% boundaries, one-HP
behavior, ride-pet fall, whole-side drain accumulation and the overflow
reported-heal-zero quirk.

## Open boundaries

R1 deliberately does not claim:

- original JSS/Taiwan-v1 membership;
- original numeric COM1;
- a portable exact qsort/BD presentation order;
- visual sprite identity as gameplay semantics;
- the business meaning of recovered `ILLEGAL=5000`;
- Ler transformation behavior for graphic101815;
- runtime integration.

**RECOVERED25_BATFLY_REFERENCE_R1 =
CLOSED_BOUNDED_FIXED_DESCENDANT_REFERENCE.**
