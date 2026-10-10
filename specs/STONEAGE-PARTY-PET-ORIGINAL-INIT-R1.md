# Pinned descendant original populated party/pet Init R1

Status: **REMOTE ACCEPTED — bounded original native gate**, 2026-10-10.

Action [38033067497](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38033067497), job 114157832582: SUCCESS with 18 regressions.
Tested SHA `1c0c27de29862e56b0d89370069b3c34174954d6`, tree `b38771da8453e8040196c7edab84cfd0c6b89574`. Execute actual pinned source bodies and real
headers for `BATTLE_Init`, `BATTLE_SurpriseCheck`,
`BATTLE_PreCommandSeq`, `BATTLE_CharaBackUp`,
`BATTLE_IsCharge`, `BATTLE_AllCharaCWaitSet`,
`BATTLE_TurnParam`, and `BATTLE_AttReverse`.

Start with accepted exact original populated leader0, teammate1 and owned
selected pet2 CreateVsEnemy scenario, and run original Init before original
ExitAll/Delete. Assert arena mode INIT -> BATTLE, timer, free-DP flag, player
backup indexes, all three living actors set to C_WAIT, preserved pet
ownership, preserved original Exit closure, and arena reuse 0,1,2,0.

Strict scoped adapters are allowed **only** for BATTLE_CharSendAll and
BATTLE_ActSettingSend (outbound client packet producers, no payload or
transport claims). If the preprocessed Bismarck source includes
BattleStartFunction, record and count that Lua callback boundary with a
typed collector, never claim actual Lua execution. No original C/headers or
master files committed. Four controlled encounters × Gavin/Bismarck ×
O0/O2 (nonrecovering UBSan); compare exact output across optimizations.

The next distinct gate must address the actual `BATTLE_Loop` dispatcher
and `BATTLE_Command` rather than assuming Init implies full turns or
Finish/profit. JSS1999/Taiwan-v1 provenance remains unresolved.

## Actual execution outcome

Four real original-header initialized encounters per profile/optimization, 16 total. INIT→BATTLE, free-DP flag, timestamp, player backup 0/1 and leader/member/selected pet C_WAIT all asserted; Exit/Delete continues to pass. Three-slot cursor 0→1→2→0. O0/O2 byte-identical stdout per profile. Gavin trace SHA256 `362fcd9ee1d3c1536bc1950dd8b7121d53c089ffcd614bfc6ccc0ada5e08bcfe`, Bismarck `4e3acec05e99f92bdff7e606b90e050ced7833b1a495693f4f6be24ce9990807`.

Preprocessed Bismarck build does **not** enable the optional BattleStartFunction callback (`lua_boundary=0`), so real Lua was not executed. Two outbound network APIs, BATTLE_CharSendAll and BATTLE_ActSettingSend, are strictly bounded call collectors, not packet assembly or delivery. All other listed Init bodies are preserved originals, extracted from pinned original descendants with real headers. No original BATTLE_Loop, BATTLE_Command, full rounds, Finish, or profit. No JSS/Taiwan-v1 equivalence or global promotion.

Receipt: `research/recovered/STONEAGE-PARTY-PET-ORIGINAL-INIT-ACCEPTANCE-R1.json`. Derived artifact 11663147028, metadata sha256 `2b8ce42870686e0fba254f0db73734ff78d0fe21538d856c2d102f1683f7573a`, ZIP not independently verified.
