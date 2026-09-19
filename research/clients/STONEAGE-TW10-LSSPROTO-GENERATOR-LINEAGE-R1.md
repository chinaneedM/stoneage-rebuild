# Taiwan v1.0 LSSPROTO Generator Lineage — R1

Date: 2026-09-19

## Scope

This record identifies the protocol-message generator helpers in the accepted Taiwan Waei/JSS StoneAge v1.0 retail client by combining:

1. exact raw string cross-references recovered from the verified `sa_3.exe` bytes;
2. direct call counts and call order from those exact xref roots;
3. a later preserved StoneAge client source tree used only as a lineage control.

The Taiwan retail binary remains the primary evidence. The descendant source is not treated as proof unless its predicted structure is independently reproduced by the v1.0 bytes.

## Primary artifact anchor

Accepted Taiwan v1.0 runtime:

- disc track SHA1: `d0f270163772eb587185a65e24a3f7e565263f2f`
- `StoneAge/sa_3.exe` SHA1: `f3999d1331374abe60c1a11a70c08bc9108d6873`
- image base: `0x400000`

Canonical exact-xref report:

- `research/recovered/STONEAGE-TW10-EXACT-XREF-R1.txt`

## Protocol sequence recovered from the v1.0 binary

The strings below each have two exact .text references in the Taiwan binary: a push-side reference used by the message builder and a mov-side reference in a distinct dispatch/receive branch.

| Protocol name | push-side instruction RVA | mov-side instruction RVA |
| --- | ---: | ---: |
| ClientLogin | `0x19365` | `0x1a6d5` |
| CreateNewChar | `0x193d5` | `0x1a751` |
| CharDelete | `0x195c5` | `0x1a7f6` |
| CharLogin | `0x19615` | `0x1a89b` |
| CharList | `0x19665` | `0x1a940` |
| CharLogout | `0x196a5` | `0x1a9e5` |

The push-side functions are contiguous in the same order later preserved by the LSSPROTO generator.

## Helper identification from exact counts and order

### `0x1b480 = lssproto_CreateHeader`

Every tested send-side function calls `0x1b480` first, immediately after the exact protocol-name reference.

This matches the later generator pattern:

`lssproto_CreateHeader(lssproto.work, "<ProtocolName>")`

### `0x1b060 = lssproto_strcatsafe`

Direct call counts from the six v1.0 message builders are:

- ClientLogin: 2
- CreateNewChar: 13
- CharDelete: 1
- CharLogin: 1
- CharList: 1
- CharLogout: 1

Those counts exactly reproduce the descendant generator's number of argument-appends for the same six messages.

### `0x1b0f0 = lssproto_mkstr_string`

Direct call counts are:

- ClientLogin: 2
- CreateNewChar: 1
- CharDelete: 1
- CharLogin: 1
- CharList: 0
- CharLogout: 0

This exactly matches the number of string parameters converted by `lssproto_mkstr_string`. CharList and CharLogout append a literal empty string and therefore do not call the string converter.

### `0x1b0b0 = lssproto_mkstr_int`

This helper appears 12 times in CreateNewChar and zero times in the other five tested messages.

The later CreateNewChar signature contains exactly twelve integer fields around one string field:

`dataplacenum, imgno, faceimgno, vital, str, tgh, dex, earth, water, fire, wind, hometown`

The v1.0 call order alternates `0x1b0b0 -> 0x1b060` for those integer fields, with one `0x1b0f0 -> 0x1b060` pair for `charname`.

### `0x1b3f0 = lssproto_Send`

Every tested send-side function calls `0x1b3f0` exactly once and always as the final direct helper call after all argument appends.

This matches the later generator pattern:

`lssproto_Send(fd, lssproto.work)`

## Strongest sequence check: CreateNewChar

The Taiwan v1.0 CreateNewChar builder has 28 direct helper calls from its exact protocol-name root:

1. `0x1b480` — header
2. twelve `0x1b0b0 -> 0x1b060` integer-conversion/append pairs, with
3. one `0x1b0f0 -> 0x1b060` string-conversion/append pair in the correct sequence position, then
4. `0x1b3f0` — final send

This exact count/order correspondence is substantially stronger than matching names alone and establishes direct protocol-generator lineage between the accepted v1.0 runtime and the later preserved source family for these message builders.

## Receive/dispatch side

The second reference for each protocol name is a `mov` and belongs to the v1.0 string-protocol dispatcher rooted at `0x19730`.

The six login/character branches are now resolved through their shared decode/copy helpers and terminal callbacks:

- ClientLogin branch -> `0x2f200`
- CreateNewChar -> `0x31e90`
- CharDelete -> `0x31f90`
- CharLogin -> `0x2f530`
- CharList -> `0x2f320`
- CharLogout -> `0x2f610`

Shared receive-side helpers are `0x1b140` (string de-escape/decoder equivalent) and `0x1b4c0` (string-address copy/wrapper equivalent). `0x1b120` is the integer decoder: the independently observed `MC` branch calls it eight times, and `M` five times, matching their field counts.

The incoming network join is also closed: the unique WSOCK32 `recv` business call at `0x2ea8a` occurs in the network path that calls dispatcher root `0x19730` at `0x2eae3`. The dispatcher root itself contains exact early protocol-name cases (`EV`, `EN`, `RS`, `RD`) and leads into the later login and map protocol cases.

Map receive lineage is recorded separately in `research/clients/STONEAGE-TW10-RECEIVE-MAP-LINEAGE-R1.md`.

## Network handoff boundary

Taiwan v1.0 now independently closes the generated-protocol -> socket-write chain from retail bytes.

- `0x1b3f0 = lssproto_Send` ends at `0x1b46e` with an indirect call through the `.data` function-pointer slot `0x598e0`.
- The initialization helper at `0x1ac10` loads its first argument, first installs default text target `0x1b3d0` into `0x598e0`, tests the caller-supplied pointer, and at `0x1ac22` overwrites `0x598e0` when that pointer is non-null. This independently reproduces the later `lssproto_InitClient(writefunc,...)` control shape.
- `0x1ac10` has one direct caller, `0x2ebe3`; every valid call-predecessor path identifies `0x2eca0` as the callback argument.
- Control-flow recovery of callback `0x2eca0` shows it reads the pending-length global `0x13ede20` at `0x2ecaf` and writes the updated value back at `0x2ece1`. It also references `0x13ede1c`; that second global's human-readable role remains unassigned.
- The WSOCK32 `send` import occupies IAT RVA `0x52254`. The exact linker thunk is `0x48466` (`jmp [IAT]`) and has exactly one direct caller, `0x2eb33`.
- Immediately before `0x2eb33`, the runtime loads length from `0x13ede20` and socket from `0x13ede24`, then supplies flags `0`, that length, buffer address `0x13f1e34`, and the socket to `send`.

The binary-proven handoff is therefore:

`lssproto_Send 0x1b3f0 -> [0x598e0] -> callback 0x2eca0 -> pending write state -> 0x2eb33 -> thunk 0x48466 -> WSOCK32 send (IAT 0x52254)`

The later source predicted this two-stage buffered-write architecture, but the addresses, shared state and final Winsock call above are independently recovered from the accepted Taiwan v1.0 binary.

Canonical derived evidence: `research/recovered/STONEAGE-TW10-PROTOCOL-HANDOFF-R1.txt`.

## Evidence boundary

Established directly from Taiwan v1.0 bytes:

- exact protocol-name locations and xrefs;
- send-side versus dispatch-side reference forms;
- exact protocol utility helper RVAs, call counts and call order;
- the `lssproto_Send` indirect callback slot and its initialization semantics;
- the sole non-null callback supplied by the runtime;
- callback mutation of the pending-length state;
- the unique WSOCK32 `send` thunk/caller and its socket/buffer/length/flags argument path.

Still OPEN:

- exact symbolic names for a subset of receive-side utility helpers beyond the roles proven by binary structure;
- exact symbolic names for runtime globals beyond roles proven by use;
- whether every later LSSPROTO message remained byte/semantics compatible;
- server-side validation and logic not present in the retail client.

## Descendant source control

Repository: `BismarckDD/stoneage`  
Pinned commit: `999ffdf1d220ec6666eb65339180689c9caf1876`

Relevant files:

- `client/stoneage/proto/protocol.h`
- `client/stoneage/proto/lssproto_cli.cpp`
- `client/stoneage/proto/lssproto_util.cpp`

The descendant source is used as a comparison/control corpus only. The v1.0 retail binary is the historical anchor.
