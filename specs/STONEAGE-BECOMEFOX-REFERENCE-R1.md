# StoneAge PETSKILL_BecomeFox recovered25 source/data reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_SOURCE_DATA_REFERENCE**  
Date: 2026-10-06  
Scope: exact recovered25 callback population/placements plus three pinned descendant structural source profiles.

## 1. Exact recovered25 population

The hash-verified recovered25 preservation bundle closes the callback population
to exactly one row:

- callback: `PETSKILL_BecomeFox`
- skill ID: **625**
- FIELD: **1**
- TARGET: **1**
- COST: **2**
- ILLEGAL: **3000**
- positive enemybase slot uses: **2**
- positive templates: **2**
- OPTION bytes: **0**
- OPTION SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- exact active petskill file SHA-256:
  `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`

Both positive uses are report slot3/runtime index2:

| TEMPNO | IMGNUMBER | VIT | STR | TOUGH | DEX | AI |
|---:|---:|---:|---:|---:|---:|---:|
| 148 | 101743 | 32 | 40 | 26 | 30 | 150 |
| 149 | 101744 | 28 | 45 | 22 | 32 | 150 |

No sibling BecomeFox callback row exists in the verified active petskill file.

## 2. Pinned descendant source structure

The current-main gate independently replays three clean pinned descendants:
gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris
`9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, and Bismarck
`999ffdf1d220ec6666eb65339180689c9caf1876`. Each passes **21/21** bounded
structural gates.

Common source facts include:

- the callback writes symbolic `BATTLE_COM_S_BECOMEFOX`, COM2 target carrier,
  C_OK and the low skill-array carrier;
- the callback reads no OPTION and owns no RNG;
- the post-attack transform branch rejects MISS/DODGE/ALLGUARD and requires a
  still-live target before one `rand()%100 < 31` draw;
- that draw occurs before non-player and nonzero PETFLG eligibility checks;
- success records current battle turn in FOXROUND and sets image **101749**;
- the active fox state applies distinct action-time power and initiative rules;
- recovery requires `current_turn - fox_round > 2` and restores base image,
  fixed powers and FOXROUND;
- battle exit has an independent fox cleanup path;
- command/menu restriction keys on FOXROUND state rather than image alone.

## 3. Material descendant divergence

`BATTLE_PetIn` does not agree across the fixed descendants:

- gavin/iris access FOXROUND through ordinary integer accessors;
- Bismarck uses work-state accessors.

All three place the fox reset block before the NORETURN guard and restore attack
and quick but not defense in that reset block. This divergence is preserved as
versioned evidence; no descendant is silently selected as recovered-original
behavior.

## 4. Explicit boundary

This R1 closes **source/data reference only**. It does not yet establish:

- ordered ordinary-attack hit/retarget/Guardian composition;
- native equivalence for the transform branch;
- exact original PRNG implementation or probability quality;
- cross-round persistent FOXROUND integration in the modern runtime;
- which PetIn accessor profile matches the recovered executable;
- ride cleanup reachability;
- original numeric COM1 value, active build flags, JSS/Taiwan-v1 membership;
- pressure/runtime promotion.

Therefore complete pressure remains **2486=2463 closed capability+20 OPEN+3
historical UB** and BecomeFox's two placements remain OPEN for runtime pressure.

## 5. Acceptance

Discovery run `37467373346/112281727223` first exposed the exact data.
Exact pinning input `a0fed469ce621ce1dba53afd3d608074af144544`, tree `73c835d23d670f6d0bc39828fecc525b92d874d8`, then passed
`37467755344/112282980151`: 4 probe tests, all three 21-gate source profiles,
verified bundle recovery, exact callback population, exact row identity and exact
template identity. Derived report writeback `8dfa0a6313acb4a0b3e87e031663a8c4f09e1cb7`
changes only the recovered25 probe report.

Derived reports:

- `research/recovered/STONEAGE-BECOMEFOX-PREAUDIT-R1.txt`
- `research/recovered/STONEAGE-25-BECOMEFOX-PROBE-R1.txt`

Receipt:
`research/recovered/STONEAGE-BECOMEFOX-REFERENCE-ACCEPTANCE-R1.json`.

**BECOMEFOX_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_SOURCE_DATA_REFERENCE.**
