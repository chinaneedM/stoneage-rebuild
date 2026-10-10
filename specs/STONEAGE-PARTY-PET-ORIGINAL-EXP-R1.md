# Original real-header EXP transfer R1

Status: REMOTE ACCEPTED, Actions38061352391 at b770da490d073794f20cdd6a7bbab5362088948b. Late descendant bounded
capability only; not first-release JSS1999/Taiwan-v1 historical equivalence.

## Inputs and whole-state oracle

The dedicated gate extends the accepted populated original-header lethal-loop
fixture. It preserves original Create/Init/command/AI/guard/nonterminal/lethal
controls and restores that fixture before its inherited Exit/Delete control.
Direct calls execute unchanged original BATTLE_GetExp and CHAR_AddMaxExp against
player0 or owned pet2. This is not the next Loop/Finish/GetExpGold composition.

Nine independent cases run per arena cursor0,1,2,0 and each native profile at
O0/O2 with nonrecovering UBSan. Before each call the whole seven-actor array is
saved. Independent expected state permits only recipient CHAR_EXP and
CHAR_WORKGETEXP writes. The entire arena must remain byte-identical. Invalid
recipient -1 must return0 without changing any actor or arena. No equipment,
item EXPUP or leveling branch is claimed. All source bodies/declarations are
fingerprinted, including exact unsigned getter signatures.

| Case | Input/control | Gavin expected add | Bismarck expected add |
|---|---|---:|---:|
| 0 | player, raw13 | 13 | 1000000 |
| 1 | player, bonus50% | 19 | 1000000 |
| 2 | pet, owner bonus50%, pet-local99% | 19 | 1000000 |
| 3 | raw -1 | 0 | 0 |
| 4 | raw0 | 0 | 1000000 |
| 5 | existing EXP at profile cap minus5 | 13, stored total capped1224160000 | 1000000, stored total capped1073741824 |
| 6 | pet ID1163 | 0 | 0 |
| 7 | maximum upgrade level | 0 | 0 |
| 8 | Gavin configured test multiplier3 | 39 | 1000000 |

Gavin's active preprocessed unsigned getter reads the original complete Config
structure's battleexp field. Values1/3 are explicit fixtures, not recovered
operator configuration. Bismarck's active getter returns1. In unequipped
Bismarck GetExp that getter is not called: its usage is inside untaken item
branches. Therefore source presence of the getter does not establish executed
multiplier dependence in this bounded Bismarck payout. Its unchanged original
CHAR_GetLevelExp and complete LevelUpTbl are included for actual GetExp checks.
The one-million floor and ignored extraExp variable are source-profile facts,
not rules imposed on other versions or the future modern implementation.

## Open terminal composition

Second Loop/Finish/GetExpGold, CHAR_LevelUpCheck, reward packets, positive item
ownership, gold and automatic terminal Exit/Delete remain OPEN. A local
exploratory second-Loop candidate with original GetExp/AddMaxExp proceeded to
abort-on-call getBattleDebugMsg; it was not accepted or integrated. Guarded
untaken dependencies still abort rather than fabricate gameplay values.
Pressure remains2486=2465 closed capability+18 OPEN+3 historical UB;
zero promotions and no phase transition.

Acceptance:21 regression tests,10 successful workflow steps,16 native
encounters,144 direct EXP case calls plus16 invalid-recipient calls. Complete
O0/O2 output bytes agree per profile. Independently downloaded artifact
11673262164 ZIP/report SHA256 and local byte identity are in the acceptance
receipt. The frozen original source manifest is separate from runtime output.
