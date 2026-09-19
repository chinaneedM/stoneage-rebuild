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

The second reference for each protocol name is a `mov` and leads to a distinct small branch:

- ClientLogin -> `0x1a70b`
- CreateNewChar -> `0x1a787`
- CharDelete -> `0x1a82c`
- CharLogin -> `0x1a8d1`
- CharList -> `0x1a976`
- CharLogout -> `0x1aa1b`

This supports a per-protocol dispatch/receive path separate from the common send-side generator.

Exact handler semantics remain to be resolved from parameter extraction and downstream calls.

## Network handoff boundary

The exact direct-call graphs for these message builders do not reach a named WSOCK32 import.

The descendant `lssproto_Send` implementation explains a plausible architectural reason: it appends a newline and hands the encoded message to `lssproto.write_func(fd, encoded, len)`, an indirect function pointer rather than a direct `send()` call.

For Taiwan v1.0 this is currently a **lineage-consistent hypothesis**, not yet a binary-proven fact. The next binary task is therefore to inspect `0x1b3f0` for an indirect call and trace the backing function pointer's initialization to the actual socket/write wrapper.

## Evidence boundary

Established directly from Taiwan v1.0 bytes:

- exact protocol-name locations and xrefs;
- send-side versus dispatch-side reference forms;
- exact helper RVAs;
- exact helper call counts and order;
- the five helper semantic mappings above, because the six-message count/order constraints uniquely reproduce the preserved generator structure.

Still OPEN:

- exact identity of the indirect network write callback in Taiwan v1.0;
- exact mapping of receive/dispatch branch helpers;
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
