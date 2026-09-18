# StoneAge Charm NPC Core R1

Status: fixed-descendant common core; recovered 2.5 placement confirmed by the existing NPC secondary-argument census.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

All three npc_charm.c implementations converge on the same constants and state transitions.

The recovered 2.5 secondary-argument queue reports four Charm refs, all four without a secondary argument. There is therefore no per-instance configuration seam to resolve for this NPC class.

## Interaction

Charm reacts only to player characters and requires the player to be facing/near the NPC under the source face-to-face checks.

The normal UI sequence is:

1. choose the charm service;
2. source computes and displays the current price;
3. at charm >= 100 the UI gives an OK-only "already perfect" response;
4. otherwise the UI offers Yes/No;
5. on Yes, the source recomputes the price and checks carried Stone;
6. if affordable, it performs the charm upgrade.

The second cost computation means mutation uses current state at confirmation time rather than trusting the earlier displayed price.

## Cost formula

The common constants are:

- RATE = 10;
- CHARMHEAL = 5;
- WARU = 3.

Before the formula:

- charm >= 100 returns -1;
- charm <= 1 is replaced by 3.

The formula then uses C integer division:

cost = level * 10 * (charm / 3) * (transmigration + 1)

where charm / 3 truncates toward zero for the ordinary nonnegative game state.

This creates a non-monotonic edge:

- charm 0 or 1 is substituted to 3, so it costs one charm-division unit;
- charm 2 is not substituted, and 2 / 3 truncates to zero, so service is free;
- charm 3 begins charging again.

R1 preserves this rather than smoothing the price curve.

## Upgrade mutation

On success:

1. recompute cost;
2. subtract cost from CHAR_GOLD;
3. add 5 to CHAR_CHARM, capped at 100;
4. recompute player parameters;
5. send charm status;
6. recompute parameters for every carried pet and refresh each pet status.

The source does not mutate pet charm; pet recomputation is a dependent-parameter refresh after the player's charm change.

Exact carried Stone equal to cost is sufficient.

Insufficient Stone leaves charm and gold unchanged.

## Max-charm callback edge

The normal UI does not offer Yes at charm >= 100 because NPC_CharmCost returns -1 and the confirmation is replaced by an OK-only message.

However, the raw NPC_CharmUp function itself does not reject cost=-1. A forged or stale Yes callback that reaches the raw mutation path would calculate:

gold_after = gold - (-1)

and therefore add one Stone while keeping charm capped at 100.

R1 separates:

- normal UI flow, which rejects service at max charm;
- raw source mutation semantics, which preserve the cost=-1 arithmetic quirk.

This edge is not evidence of normal client behavior.

## Deterministic artifacts

- tools/stoneage_charm_core_model.py
- tests/test_stoneage_charm_core_model.py
- .github/workflows/validate-stoneage-charm-core.yml

Local validation: 14 deterministic tests passed.

## Evidence status

FACT: all three fixed descendants use RATE=10, CHARMHEAL=5 and WARU=3.

FACT: the recovered 2.5 census contains four Charm refs and no secondary argument for any of them.

FACT: normal service adds five charm, caps at 100, and deducts Stone before parameter refresh.

FACT: cost is multiplied by transmigration+1.

SOURCE QUIRK, ACTIVE FORMULA: charm 2 has zero cost because 2/3 truncates to zero, while charm 0/1 are substituted to 3 and therefore cost money.

SOURCE QUIRK, DEFENSIVE EDGE: raw max-charm mutation would add one Stone because cost=-1, although the normal UI does not expose a Yes button there.

OPEN: exact JSS-era placement and whether launch-era commercial data used the same Charm NPC.

## Next seam

Charm R1 is closed. Continue with Riderman because it changes persistent personal riding proficiency and Stone while remaining distinct from later family-bank and race packages.
