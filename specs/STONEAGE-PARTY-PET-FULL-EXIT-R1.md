# Real-header original player + party teammate + selected owned pet Exit R1

Status: **REMOTE ACCEPTED — bounded single-case native integration**, 2026-10-10.

Previously accepted full real-header original CreateVsEnemy populated party
entry is followed in this gate by **unmodified original descendant** BATTLE_Exit
for leader0 then teammate1, BATTLE_ExitAll and BATTLE_DeleteBattle. Gavin and
Bismarck exact source/header pins are recovered transiently in CI; original
source, binaries, headers and enemy master bytes are not redistributed.

## Test evidence

- Tested input `d063724a90a3def2528ff73c255db08d625d69ca`, tree
  `e01cf5ddfb30f108030f56ad279fab43d35112bc`.
- Workflow `38031083207`, job `114151987552`, **SUCCESS** with all
  ten steps completed and 18 Python structural/predecessor regression tests.
- Gavin and Bismarck each execute one eligible controlled encounter under
  `-O0` and `-O2` with nonrecovering undefined-behavior sanitizer. Within
  each profile the complete entry/exit trace is byte-identical at both
  optimization levels; profile traces are separately pinned in the receipt.
- Actual first-player front slot0 and teammate front slot1 enter battle; default
  owned healthy pet2 occupies rear slot5 and bid5. Original leader Exit clears
  own front and paired pet rear occupancy. Pet battle index resets -1 and mode
  NONE without deleting its owned roster slot or healthy pet object. Member
  Exit clears its front slot and sets member FINAL; original ExitAll and
  DeleteBattle clear the battle arena. World objects0/1 remain registered.

## Explicit adapter / provenance boundary

Source-profile differences are preserved. In the original `RIDEPET_getPETindex`
predicate an empty ride-license bitmask cannot select a ride code; our
controlled zero-license guard returns -1, aborting nonzero permissions. Gavin
uses its 2-argument and Bismarck its pinned 4-argument signature. Character
broadcast and K-status packets are bounded observation-only collectors, not
an original network stack. Teammate/pet status output and battle-time
guards admit only the named controlled actors and pinned constants. Original
GetProfit, Init, TaskLoop, server bootstrap, network, reclaimer and nonempty
skills/Lua/equipment are not tested.

This **does not yet demonstrate arena reuse under multiple fights**, arbitrary
roster status combinations, nonempty party variants, win/loss/profit, full
player progression or historical equivalence to JSS1999 / Taiwan-v1. It
creates no general runtime-pressure closure or promotion. Next: test repeated
real-header player/party/pet battle creation and Exit/Delete/reentry with a
complete state/ownership oracle before claiming full reuse; then Init/TaskLoop
and broader Finish/profit. Receipt:
`research/recovered/STONEAGE-PARTY-PET-FULL-EXIT-ACCEPTANCE-R1.json`.
