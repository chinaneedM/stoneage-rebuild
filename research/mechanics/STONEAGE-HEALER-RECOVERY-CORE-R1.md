# StoneAge Healer / Recovery Core R1

Status: **strong convergent descendant evidence; player revival remains separate**  
Scope: ordinary free healer, window healer, player/pet HP/MP restoration, party targeting, charge formulas and payment ordering.

## Why this seam matters

The battle/death models now describe how HP/MP and death state are lost. This recovery seam closes the ordinary post-battle loop without collapsing distinct mechanisms into one another.

The preserved source family contains two separate healer NPC designs:

1. **ordinary healer** — immediate free full HP/MP recovery;
2. **window healer** — selectable player HP/MP services with level-based pricing, while pet recovery is free.

A crucial reconstruction constraint is that neither healer should be mistaken for the player-resurrection subsystem.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/npc/npc_healer.c`
  - `server/gmsv/npc/npc_windowhealer.c`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src/npc` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv/npc` files

## Ordinary healer

### Interaction scope

`NPC_HealerTalked` responds only to players within distance 2.

Party behavior is stable:

- standalone player -> heal self;
- party client -> heal self;
- party leader -> iterate the leader-owned party roster and heal every valid member.

Thus a client cannot trigger free healing for the whole party; the leader can.

### Player restoration

`NPC_HealerAllHeal` sets:

```
player HP = WORKMAXHP
player MP = WORKMAXMP
```

It does **not** explicitly:

- clear the player's `CHAR_ISDIE`;
- invoke `CHAR_playerresurrect`;
- clear poison/paralysis/sleep/stone/drunk/confusion;
- move the player.

Therefore ordinary healer recovery must remain distinct from the reconstructed player revival state transition.

### Pet restoration

For every valid carried pet slot, the healer:

```
CHAR_ISDIE = 0
HP = WORKMAXHP
MP = WORKMAXMP
CHAR_complianceParameter(pet)
```

So the same healer that does not revive a player **does revive carried pets** by directly clearing the pet death flag.

This asymmetric player/pet behavior is a source fact.

## Window healer

The window healer exposes separate choices for:

- player HP;
- player MP;
- player HP + MP;
- pet recovery.

### NPC configuration

The argument fields are parsed into:

1. free-service level threshold;
2. HP rate;
3. MP rate;
4. interaction range.

The source uses `RATE = 1000`.

When the configured HP rate parses as zero, the default stored rate is:

```
500 / 1000 = 0.5
```

When the configured MP rate parses as zero, the default is:

```
2000 / 1000 = 2.0
```

A zero range is normalized to 1.

R1 models the cost semantics directly and keeps concrete NPC argument rows in the data layer.

## Free level threshold

`NPC_WindowHealerLevelCheck` returns free-service TRUE when:

```
configured_level > player_level
```

Therefore:

- player level strictly below the threshold -> free;
- player level equal to or above the threshold -> paid.

This is a strict comparison, not `<=`.

## HP and MP costs

For paid users:

```
hp_cost = int(player_level * hp_rate / 1000)
if hp_cost < 1:
    hp_cost = 1
```

The default HP rate therefore gives approximately:

```
floor(level * 0.5), minimum 1
```

MP uses:

```
mp_cost = int(player_level * mp_rate / 1000)
if mp_cost == 0:
    mp_cost = 1
```

With the default MP rate this is:

```
level * 2
```

For ordinary positive configuration the practical minimum is also 1. The source's MP guard is literally `== 0`, unlike HP's `< 1`; R1 preserves that difference rather than rewriting it.

## Combined-service charging

Mode 3 computes charges only for player resources actually below max:

- missing HP -> add HP cost;
- missing MP -> add MP cost;
- already-full component -> no charge for that component.

Thus an HP-full/MP-low player selecting "both" pays only the MP component.

Pet condition never adds a charge.

## Payment ordering

`NPC_WindowMoneyCheck` performs:

1. determine whether the player's level requires payment;
2. calculate the requested cost;
3. compare carried gold to cost;
4. if insufficient -> return FALSE with no deduction;
5. if sufficient -> `CHAR_DelGold` immediately;
6. caller then enters the healed-result path.

Therefore payment precedes restoration.

R1 transaction logic preserves the no-partial-heal behavior on insufficient funds.

## Window-healer restoration modes

`NPC_WindowHealerAllHeal(talker, mode)` uses:

- mode 0 -> player HP/MP unchanged;
- mode 1 -> player HP to max;
- mode 2 -> player MP to max;
- mode 3 -> player HP and MP to max.

But **all four modes** then iterate every valid carried pet and:

- clear pet death;
- set pet HP to max;
- set pet MP to max;
- recompute pet parameters.

Therefore buying only player HP still gives full free pet recovery as a side effect.

## Explicit pet-only service

The menu labels pet recovery as free.

Selecting it first calls `NPC_PetHealerCheck`.

That check considers a pet in need only when:

```
pet HP != pet WORKMAXHP
```

It does not check:

- pet MP;
- pet death flag;
- abnormal statuses.

If the check returns true, the service executes mode 0, leaving player HP/MP unchanged while fully restoring every valid carried pet.

This produces an important edge case: a pet at full HP but low MP does **not** trigger the explicit "pet needs healing" detector, even though any actual healer execution would refill pet MP.

## Player death remains unchanged

Neither `NPC_HealerAllHeal` nor `NPC_WindowHealerAllHeal` clears the player's death flag.

They also do not call the generic player resurrection helper.

Therefore:

```
player death
  != healer service
  != player resurrection
```

The earlier death/revival R1 separation is confirmed by this subsystem.

## Player abnormal statuses remain unchanged

The healer functions contain no explicit clearing of ordinary player poison/paralysis/sleep/stone/drunk/confusion flags.

The same applies to pet abnormalities except for the pet death flag.

R1 therefore models HP/MP/death effects only and does not invent status curing.

## Party behavior

The ordinary healer directly heals the full party only when the talker is leader.

The window healer behaves differently: when the leader talks, it opens the healer selection window separately for each valid party member.

That means each player receives an individual service flow based on:

- their own level;
- their own HP/MP deficits;
- their own carried gold;
- their own pets.

R1 keeps the target enumeration separate from each member's payment transaction.

## Deterministic model

Repository artifacts:

- `tools/stoneage_healer_recovery_model.py`
- `tests/test_stoneage_healer_recovery_model.py`
- `.github/workflows/validate-stoneage-healer-recovery.yml`

Regression coverage includes:

- self versus leader-party target scope;
- free healer full player HP/MP;
- free healer pet revival/full recovery;
- player death/status flags remaining untouched;
- strict free-level threshold;
- default HP/MP pricing;
- component-only charging for combined recovery;
- free pet-only mode;
- HP-only pet-need detector;
- all window-healer modes;
- payment-before-heal and insufficient-funds atomicity.

## Evidence status

- **FACT:** three descendant lineages agree on ordinary healer HP/MP restoration and full carried-pet recovery.
- **FACT:** ordinary healer leader interaction heals the party; standalone/client interaction heals only the talker.
- **FACT:** pet death is cleared by healer code while player death is not.
- **FACT:** window healer uses a strict level threshold for free service.
- **FACT:** default HP rate is 0.5 × level and default MP rate is 2.0 × level.
- **FACT:** combined healing only charges components below max.
- **FACT:** pet healing is free and occurs in every window-healer recovery mode.
- **FACT:** explicit pet-need detection checks HP only.
- **FACT:** healer code does not explicitly cure ordinary abnormal statuses.
- **OPEN:** exact launch-era placement/configuration of free-healer versus window-healer NPCs in commercial map data.
- **OPEN:** whether all historical commercial configurations used the default 0.5/2.0 rates or custom NPC arguments.
- **OPEN:** client-facing localization/text differences by commercial region/version.

## Next technical seam

The recovery loop is now explicit. The next high-value seam is **trading / economy transfer semantics**: item/gold/pet offer construction, confirmation/locking, capacity checks, atomic exchange ordering and cancellation behavior. That will connect the reconstructed inventory, pet roster and carried-gold systems into a complete player-to-player economy transfer model.
