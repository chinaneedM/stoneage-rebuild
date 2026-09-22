# StoneAge Counter Ride-Pet Interaction R1

Status: **closed to the accepted stable-descendant base boundary**

Scope: base `BATTLE_Counter` physical damage when one of the two alternating
counter participants is an active rider. DamageReact branches remain outside
this specific seam because the stable caller only starts the alternating
counter chain when the main attack's continuation flag remains true, and base
DamageReact on either participant disables that continuation.

## Fixed descendant evidence

Pinned descendants agree that `BATTLE_Counter`:

1. resolves the counter attack;
2. scales positive counter damage to 75 percent;
3. calls the same `BATTLE_DamageSub(attackindex,defindex,...)` used by normal
   physical attacks;
4. receives both `damage` and `petdamage` back from that call;
5. writes both values into the non-`_NOTRIDE_` counter battle command.

Witnesses:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/battle/battle_event.c`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/battle/battle_event.c`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/battle/battle_event.c`

These are descendant witnesses rather than direct 1999 JSS proof.

## 1. No special counter ride formula

There is no independent counter-specific ride-sharing algorithm in the pinned
base path.

After the source computes the ordinary counter physical result it does:

- positive damage -> multiply by 0.75;
- clamp to at least 1;
- call `BATTLE_DamageSub`.

Therefore the already reconstructed ordinary ride split applies unchanged.

For an active ride pet on the counter **target**:

- rider/player share uses the source ordinary split formula;
- ride-pet share uses the same ordinary split formula;
- the counter event's reported `damage` is the post-`DamageSub` rider/player
  amount;
- `petdamage` is the separate ride-pet amount.

If the active rider is the counter **attacker** and there is no Reflect branch,
the attacker's ride pet is not part of the target damage transaction.

## 2. PETFALL timing

If the ride pet reaches HP <= 0 inside the counter's `BATTLE_DamageSub`:

- the rider is immediately unmounted;
- the ride image/state is changed by the source;
- `CHAR_WORKPETFALL` is set;
- subsequent alternating counter attempts in the same chain see no mounted
  ride pet and therefore do not share later damage.

The reconstruction mutates the battle-local `RidePetRuntime` immediately, so
the same chain observes the unmounted state.

## 3. Ultimate threshold and overkill quantities

The counter's `BATTLE_DamageSub` receives the already-75%-scaled counter
damage as its raw `damage`.

Consequently:

- direct ultimate threshold compares that raw counter damage against
  `maxHP * 1.2 + 20`;
- when a rider is sharing damage, overkill accumulation uses the actual
  rider/player HP subtraction;
- ride-pet HP subtraction does not become player `CHAR_WORKULTIMATE`
  overkill;
- the target player's max HP remains the ultimate threshold max-HP basis.

This is the same distinction already used by the ordinary ride path:
`damage_for_threshold` can differ from `hp_damage_applied`.

## 4. Why DamageReact is not newly inferred here

Pinned `BATTLE_Counter` itself can call `BATTLE_DamageSub` with reactions,
but the stable alternating chain is entered from the main attack only while its
continuation flag remains true.

The recovered base main-attack logic forces continuation false when either
participant has an active base DamageReact.

Therefore this R1 closure does not need to invent a new Counter+DamageReact
entry path merely to close Counter+ride. It connects the previously isolated
no-reaction counter chain to the already-proven ordinary ride-sharing portion
of `BATTLE_DamageSub`.

## 5. Reconstruction representation

`_resolve_counter_chain` now accepts and returns the battle-local
`RidePetRuntime`.

Each damaging counter event may expose:

- `ride_damage_split`;
- `ride_hp_resolution`;
- `ride_pet_fell_rider_id`.

After each counter attempt the updated ride runtime is immediately visible to
the next alternating attempt.

The previous blanket rejection of any active ride plus counter rolls has been
removed.

## Validation

Implementation:

- `ecdfcbb9404cc1593b0299fa50c47f720760aec0` — connect counter
  `BATTLE_DamageSub` to ordinary ride sharing, ride HP, unmount/PETFALL and
  counter ultimate input quantities.
- `80aad145d0a2945791c7480043bec71e4f137ca8` — migrate the old closed-seam
  rejection test and make the multi-chain counter RNG explicit.

Validation at `80aad145d0a2945791c7480043bec71e4f137ca8`:

- battle-core **35724103327** — success;
- gameplay **35724103367** — success.

Regression coverage proves:

- a counter against an active rider splits damage into rider and ride-pet
  portions;
- ride-pet HP is reduced in the counter transaction;
- ride-pet death immediately unmounts and sets PETFALL;
- later counter attempts in the same chain stop sharing damage after the fall.
