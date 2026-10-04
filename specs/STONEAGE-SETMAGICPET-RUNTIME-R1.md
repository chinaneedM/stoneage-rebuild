# StoneAge SetMagicPet ordered runtime R1

## Scope

R1 execution is limited to the positively referenced recovered25 enemy skill
ID **601**. The closed but unreferenced family rows 602/603/604 remain data
evidence only.

The runtime preserves symbolic `BATTLE_COM_S_SETMAGICPET` identity. ATTACK may
be used internally as an action-order carrier, but no descendant numeric COM1
is promoted to the recovered25 binary.

## State model

SetDuck and STR/TGH/DEX turn counters are battle-local work state. Fixed pinned
source decrements all four in `BATTLE_StatusSeq`; expiration does not itself
rebuild character attributes.

ID 601 writes TGH turn=3/power=15 only when the target has no active SetDuck,
STR, TGH or DEX counter. The runtime keeps already prepared current-command
powers separate from the mutable counters so a counter can expire during
StatusSeq without retroactively changing the command that was prepared by the
preceding `BATTLE_PreCommandSeq`.

Post-round preparation reconstructs from immutable battle-session baseline
stats. In the admitted no-suit/no-profession/no-riding modifier domain,
baseline defense is also the source's saved pre-suit `mtgh` basis. Active
TGH therefore adds 15% of baseline defense before any later Weaken reduction.

## RNG

SetMagicPet owns no effect RNG. The only admitted random draws are descendant
`BATTLE_MultiList` dead-single retarget `rand()%10` draws. Live single
targets consume none.

## Runtime acceptance

**RECOVERED25_SETMAGICPET_RUNTIME_R1 =
CLOSED_BOUNDED_ID601_TGH_ENEMY_DOMAIN.**

The accepted branch proves exact ID-601 admission across the six positively
referenced recovered25 slots, typed enemy submission, source MultiList
dead-single retarget ownership, battle-local SetDuck/STR/TGH/DEX exclusion,
StatusSeq decrement, persistent expiry, confusion/combo/counter suppression,
Weaken/Barrier/Nocast interaction and coordinator persistence.

Code-level dedicated/coordinator/full-stack regressions pass at
`234cfb200ccff06bd97cb29009f81c7406e8f373`; the expiry/Weaken-order
supplement passes at `8b1cb0fd49f2708eecfe08b67bc97301fbf7e14f`.
Hash-verified pressure Action **37218864011 PASS** rewrote
`research/recovered/STONEAGE-25-PETSKILL-PRESSURE-R1.txt` at
`ec46a0248e6c64623096d03c14e5ffc156a1193c`, marking SetMagicPet
`closed_runtime`. Accepted executable slot coverage is therefore
**2434/2486 = 97.91%**.

## Remaining boundaries

Rows 602/603/604 remain data-only because they have no positive recovered25
slot use. Riding/drunk or other preparation domains not covered by the accepted
ID-601 fixture remain fail-closed. Historical numeric COM1, original-binary
identity, original compiler profile and Taiwan-v1 membership remain OPEN.

The pressure report mechanically selects **PETSKILL_BattleTimid, ID 606,
5 uses / 5 templates** as the next OPEN callback.
