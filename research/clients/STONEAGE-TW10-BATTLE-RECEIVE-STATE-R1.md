# StoneAge Taiwan v1.0 Battle Receive State — R1

Date: 2026-09-27

## Scope

This document reconstructs the **server -> client battle command receive boundary** in the accepted Taiwan/Waei v1.0 `sa_3.exe`.

It is deliberately separate from `tools/stoneage_battle_command_model.py`, which models **player -> server** submitted battle commands such as attack / guard / wait / escape / capture.

The modern single-player runtime may eventually unify both directions inside one deterministic battle state machine. The archaeology record must not conflate them.

## 1. Protocol envelope — V1_DIRECT

The generated v1 receive dispatcher proves:

```
B(string command)
  -> callback RVA 0x32c70
```

The `B` receive envelope has:

- integer fields: **0**
- string fields: **1**
- direct non-helper target: **0x32c70**

Primary evidence:

- `research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt`
- `research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`

## 2. Internal command discriminator — V1_DIRECT

The v1 callback at RVA `0x32c70` loads **byte 1** of the command and directly compares it against:

- `C` at RVA `0x32c7a`
- `P` at RVA `0x32cba`
- `A` at RVA `0x32ce2`
- `U` at RVA `0x32d25`

Every other value falls through to the default command-buffer path.

Therefore the following grammar skeleton is direct v1 fact:

```
B command
  second byte == C -> status-buffer path
  second byte == P -> 3-output parse path
  second byte == A -> 2-output parse + turn-sync path
  second byte == U -> single flag-set path
  otherwise        -> ordinary battle-command buffer
```

The semantic names attached below use pinned descendant source only where the original v1 binary does not itself carry symbol names.

## 3. BC/status queue — V1_DIRECT geometry; lineage semantic name

For second byte `C`, original v1 code:

- reads a write index from VA `0x46f270`;
- multiplies it by `0x1000` through a left shift of 12;
- adds buffer base VA `0x46a21c`;
- copies the entire NUL-terminated command;
- increments the write index;
- masks the index with `3`.

Directly recovered queue geometry:

```
slots     = 4
slot_size = 4096 bytes
ring_mask = 3
```

Pinned descendant `BismarckDD/stoneage@999ffdf1...` names the corresponding concepts:

- `BattleStatusBak`
- `BattleStatusWritePointer`

and performs the same copy / `(write + 1) & (BATTLE_BUF_SIZE - 1)` behavior for the `C` branch.

Classification:

- four-slot / 4096-byte ring behavior: **V1_DIRECT**
- human semantic label “battle status queue”: **V1_DIRECT + PINNED_DESCENDANT_CORROBORATION**

## 4. BP metadata branch — V1_DIRECT parse arity; lineage field names

For second byte `P`, v1:

- advances the command pointer by **3 bytes**;
- pushes one format-string pointer;
- supplies **three destination addresses**;
- invokes parser target `0x49120`;
- performs caller cleanup for **5 cdecl arguments**.

Therefore this is directly a **three-output parse** of the payload beginning at `command + 3`.

Pinned descendant source preserves:

```
sscanf_s(command + 3, "%X|%X|%X",
         &BattleMyNo, &BattleBpFlag, &BattleMyMp);
```

Evidence discipline:

- three-output parsing at command+3: **V1_DIRECT**
- exact semantic field names and expected hexadecimal interpretation: **PINNED_DESCENDANT_CORROBORATION** until the original v1 format-string bytes are independently emitted by the binary probe.

## 5. BA animation/turn branch — V1_DIRECT structure; lineage semantic names

For second byte `A`, v1:

- advances to `command + 3`;
- supplies **two destination addresses** to parser target `0x49120`;
- checks global VA `0x46f27c` against `1`;
- when equal:
  - copies the second parsed destination value into VA `0x46e248`;
  - clears VA `0x46f27c` to `0`.

Pinned descendant source maps the same structure to:

```
sscanf_s(command + 3, "%X|%X",
         &BattleAnimFlag, &BattleSvTurnNo);

if (BattleTurnReceiveFlag == TRUE) {
    BattleCliTurnNo = BattleSvTurnNo;
    BattleTurnReceiveFlag = FALSE;
}
```

Classification:

- two-output parse + conditional second-value copy + one-shot flag clear: **V1_DIRECT**
- `BattleAnimFlag / BattleSvTurnNo / BattleTurnReceiveFlag / BattleCliTurnNo` names: **PINNED_DESCENDANT_CORROBORATION**

## 6. BU escape flag — V1_DIRECT write; lineage semantic name

For second byte `U`, v1 performs one material state mutation:

```
[VA 0x46f29c] = 1
```

and returns.

Pinned descendant source names the same concept:

```
BattleEscFlag = TRUE;
```

Classification:

- exact flag write: **V1_DIRECT**
- “battle escape flag” semantic name: **PINNED_DESCENDANT_CORROBORATION**

## 7. Default battle-command ring — V1_DIRECT geometry

Commands whose second byte is not `C/P/A/U` fall into a second ring:

- write index VA: `0x46f250`
- buffer base VA: `0x466214`
- slot stride: `0x1000` = **4096 bytes**
- post-write index: `(index + 1) & 3`

Direct geometry:

```
slots     = 4
slot_size = 4096 bytes
ring_mask = 3
```

Pinned descendant source names this surface:

- `BattleCmdBak`
- `BattleCmdWritePointer`

Classification: **V1_DIRECT + PINNED_DESCENDANT_CORROBORATION**.

## 8. Architectural consequence for the modern single-player game

The original online client used two distinct layers:

1. player submits a battle action to the authoritative server;
2. server sends battle-state / execution command strings back through `B`;
3. the client buffers status frames separately from ordinary battle execution commands;
4. small control messages update battle identity, animation/turn synchronization and escape state.

The modern single-player implementation does **not** need to preserve this network serialization internally.

Instead, reconstruct the same conceptual boundaries as typed state:

```
BattleIntent
  -> deterministic battle resolver
  -> BattleStateSnapshot / BattleEvent stream
  -> presentation queue
```

Recommended mapping:

- historical BC/status ring -> typed `BattleStateSnapshot` queue;
- historical default command ring -> typed `BattleEvent` / animation-event queue;
- BP metadata -> battle-local actor/control metadata;
- BA metadata -> animation/turn synchronization state;
- BU -> escape/termination event.

This preserves original behavior while removing network/string parsing from the single-player core.

## 9. Evidence boundary

Do not infer that every descendant battle subcommand or later battle feature existed in Taiwan v1 merely because later source has it.

Current v1 direct discriminator is specifically:

```
C / P / A / U / default
```

Later `Z/F/O` branches seen under descendant conditional compilation are **not** promoted to v1 fact because the accepted v1 callback directly returns through its recovered C/P/A/U/default structure and does not expose those additional discriminator comparisons.

## Final classification

**TW10_BATTLE_RECEIVE_ENVELOPE = V1_DIRECT**

**TW10_BATTLE_C_P_A_U_DISCRIMINATOR = V1_DIRECT**

**TW10_BATTLE_STATUS_RING_4x4096 = V1_DIRECT**

**TW10_BATTLE_COMMAND_RING_4x4096 = V1_DIRECT**

**TW10_BP_PARSE_ARITY_3 = V1_DIRECT**

**TW10_BA_PARSE_ARITY_2_AND_TURN_FLAG_SYNC = V1_DIRECT**

**TW10_BU_FLAG_WRITE = V1_DIRECT**

**DESCENDANT_SYMBOL_NAMES = CORROBORATION_ONLY**

Next closure seam: recover the two original v1 parser format strings and then bind the receive-state concepts into the engine-neutral gameplay schema.
