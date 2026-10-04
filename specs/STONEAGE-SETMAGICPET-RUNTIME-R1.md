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

## Open integration gates

Battle-round execution, persistent preparation ordering, coordinator selection,
confusion/combo/counter suppression, Weaken/Barrier/Nocast interaction,
dead-target retarget and end-to-end recovered enemy persistence remain OPEN
until the corresponding runtime branch tests and Actions pass.
