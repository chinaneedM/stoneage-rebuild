# Original real-header party/pet command admission R1

FACT is restricted to pinned late descendant source profiles and the bounded
synthetic live arena. This gate extends the accepted original Command WAIT gate;
it does not establish historical JSS1999/Taiwan-v1 behavior or execute a combat round.

## Native composition

- Gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` and Bismarck
  `999ffdf1d220ec6666eb65339180689c9caf1876`, original headers, GNU99,
  O0/O2 and nonrecovering UBSan. Iris pinned identity is checked as inherited.
- Preserve the complete original preprocessed bodies of `BattleCommandDispach`,
  `checkErrorStatus`, `BATTLE_MpDown`, `BATTLE_PetDefaultCommand` and original
  `CHAR_CHECKCHARDATAINDEX`, `_CHAR_getChar`, `CHAR_getUseName`. Inclusion does
  not claim every branch/function executes. Command source and four command
  function body hashes are emitted separately for each profile.
- Retain accepted original Create/party/pet Init, Loop/Command wait,
  Exit/Delete/pool reuse. Four encounters per optimization reuse arena slots
  0,1,2,0; all seven actor slots and complete BATTLE snapshots are available.
- Original `pet_skill.h` precedes `pet_skillinfo.h` numeric macros to preserve
  original declarations. New unresolved typed symbols abort on invocation;
  no missing AI/combat dependency is replaced with successful behavior.

## Inputs and assertions

Each encounter executes six complete parser calls: invalid descriptor -1,
non-player pet descriptor 9, unknown command `?`, leader command, member guard
`G`, and out-of-range pet skill `W|FFFF`. Original default-pet command is also
called with invalid -1 and valid pet2.

| Encounter mode | Leader input | Expected command / target |
| --- | --- | --- |
| 0 | `H|F` | Attack / 15 (hex F) |
| 1 | `H|oops` | Attack / invalid target -1 |
| 2 | `H|14` | Attack / out-of-range20 (hex14) becomes -1 |
| 3 | `G` | Guard / prior COM2 retained |

Allied actor0/1 are synthetic live players; pet2 is selected and owned by actor0.
Descriptor adapter7/8/9 resolves actor0/1/2; inherited WORKFD7 for both players
is deliberately retained. This is bounded admission, not actual network routing.

Invalid descriptor and non-player source return without state/output changes.
Unknown input leaves full actors/arena unchanged but acknowledges status.
Leader submission has an exact complete Char delta; turn-zero arena is unchanged.
Two original Loop dispatches (leader ready, then leader+pet ready) retain turn0
and complete seven-actor snapshots while member1 still waits. Original pet default
sets attack, target -1 and C_OK. Member guard has an exact complete Char delta;
`W|FFFF` retains the already prepared pet intent. It does not demonstrate a valid
pet skill or an unprepared-pet packet fallback.

Gavin partial input arms PartTime1120 (fixed original `time` adapter1000 +120);
Bismarck retains its previously armed1099. Exact status acknowledgements per
encounter are4, receive-time callback delta3 for Gavin and0 for Bismarck.
Original `BATTLE_CommandWait` reports both sides ready, and TimeOutCheck is false.
The all-ready `BATTLE_Loop` is intentionally not called: original enemy AI and
Battling remain aborting dependencies. No turn advance/action/round is accepted.

## Acceptance and next gate

The Python structural suite has27 checks including accepted predecessors.
Native runs execute16 Create/Init/input/wait/Exit/Delete encounters and96 parser
calls across two profiles and two optimizations. Complete per-profile trace bytes
must match O0/O2; derived evidence is accepted only after remote Actions success.

NEXT: original enemy AI/decision dependency closure in this same real-header
populated arena, then all-ready original Command/action round, Finish and profit.
Timeout-positive/PartTime expiration, valid pet skills, real transport/Lua,
full server bootstrap and historical original executable ABI remain OPEN.
Pressure2486=2465 capability closed+18 OPEN+3 historical UB, zero promotions;
no engine/content phase transition.
