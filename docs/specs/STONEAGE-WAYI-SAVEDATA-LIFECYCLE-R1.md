# Wayi compiled settings lifecycle R1

## Identity and scope

FACT denotes static evidence from the exact accepted late archived client,
921600 bytes, SHA256
`4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63`.
Nine aligned windows cover full save/create/load, startup result handling,
parent-process setup, import thunks, snapshot close and wrappers. Original
binary/source/disassembly remain outside Git; no original program, process API,
actual settings file, real PID or credentials are used by the synthetic models.

## Declared initial backing and alias limits

Settings RVA `0x4319d28`, length127 lies in `.data`, whose RVA is663552,
VirtualSize78724564 and SizeOfRawData249856. The complete127-byte region is
beyond the raw-backed portion but inside the virtual size. Under Microsoft's
[PE section rule](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers),
the virtual remainder is zero-filled. Therefore this unpacked image declares
zero initial settings storage. This is an inference from its headers and the
PE rule, not an observed original loader/UPX/runtime memory dump or proof that
all pre-load writers preserve zeros.

A linear `.text` scan finds31 direct CALL/JMP edges to the seven named roots
and skips24 undecodable bytes. Raw-backed non-executable sections contain no
32-bit word equal to the backing address or five named settings entry addresses.
This bounds a direct discovery surface. It does not close pointer arithmetic,
indirect/callback aliases, initialization writes or executable/data ambiguity.
No fake file offset is used for a virtual-only address: the probe splits raw
bytes from virtual zeros and verifies both bounds.

## Factory, encoding and failure states

The previous factory model represents state before encoder mutation. Native
constructor `0x808c0` builds plain version6/default options, then passes the
GLOBAL backing to `0x8e050`. For key0 it complements every even index and
index divisible by5. Its backing starts `f9 00` after encoding: the plain
version6 WORD becomes249 in that mutated state. The generated128-byte file
encoding remains the reversible encoding of the original plain factory.

This mutation precedes fopen/fwrite. It occurs on both success and failure.
The ordinary save function instead copies127 backing bytes onto its stack and
encodes that copy, so its encoder leaves global backing unchanged.

| Synthetic/native bounded route | Backing after route | Outcome |
| --- | --- | --- |
| Create open failure or short write | Complemented factory | Create FALSE; loader error1 |
| Create success, loader reopen failure | Complemented factory | Loader FALSE/error2 |
| Created file read error | Complemented factory | Close read stream; FALSE/error3 |
| Created complete file, successful read/decode | Plain factory restored | Version6 accepted |
| Existing file read error | Prior backing unchanged | Close read stream; FALSE/error3 |
| v4/v5 migration, failed save | Migrated plain backing retained | Load TRUE; error remains0 |

Creation and ordinary save return FALSE on short fwrite without calling fclose
in those branches. Full writes attempt fclose and return TRUE without testing
its result. Closing is an attempt, not proof of successful flush or persistence.
No modern error cleanup or retry is silently added to the historical projection.

A subsequent57-byte v4 read can retain a tail from a prior failed creation:
bytes58..126 need not be plain zeros. Tests explicitly compose this hypothetical
sequence. It is not evidence that a real user experienced that sequence.
Malformed input/capacity/aliasing/native execution remain OPEN as in R1.

## Full save preamble and migration joins

Both migration calls target full `0x80600`, not the previously bounded file body
at `0x806ba`. The preamble reads pending process-ID storage RVA `0x41658e0`.
When nonzero it enumerates an existing process snapshot, matches the stored ID,
compares the entry's executable name with literal `explorer.exe`, and only on
that comparison's zero result attempts imported OpenProcess. A nonzero returned
handle leads to imported TerminateProcess(exit code0) and CloseHandle. The
preamble ignores those two return values, clears the pending ID, then continues
to the settings body. Enumeration failure, unmatched ID/name or open failure
also clear the pending ID and fall through; zero pending ID skips the preamble.

These are exact **conditional call attempts** in this specimen, not executed
process effects or proof that every save reaches them. The comparison routine
at `0x95880` is a CRT semantic label from source/argument matching. Purpose,
author attribution, original publisher build identity and actual execution
remain OPEN; this does not assign malware/anti-cheat intent.

Earlier setup `0x3f457..0x3f4cf` stores GetCurrentProcessId's result, creates a
process snapshot (flags2, second argument supplied by earlier ESI state), then
searches for that ID and replaces it with entry offset0x18. Win32 x86
[PROCESSENTRY32 layout](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32)
identifies that offset as th32ParentProcessID. The entry size is0x128;
process ID/name offsets are0x08/0x24. This connects the conditional save gate
with parent-ID setup. Enumeration failure can leave the original current ID;
no actual parent/name/handle is recovered. Snapshot close is independently
present at `0x3f6a4`; lifetime/reachability beyond those bounded joins remains OPEN.

The synthetic preamble projection returns event names from five booleans.
It accepts no actual PID, command or process object, and calls no OS function.
Settings bytes/file results are supplied by separate pure projections.

## Startup and source distinctions

Startup call `0x1e5e4` invokes load wrapper `0x805d0`, which calls load and
applies sound/chat/interface options only on its success. On FALSE, the bounded
startup path reads the error byte, formats a message, calls MessageBoxA and
returns0. On TRUE it branches beyond this window. This is not a complete
startup termination or window/session execution claim.

Fresh Bismarck master `2f736808ff4361f5429ee919b718c88fabb60346`:
main.cpp blob65b5d8501f6770aefe35d38c5d4c1c4c902259bd includes conditional
`__NEW_CLIENT` current→parent-ID snapshot setup. main.cpp and savedata.cpp
have no TerminateProcess token. This lexical absence is bounded to those two
pinned files, not the entire repository or a preprocessed build. The already
accepted source recursion/mute-bit differences remain. No source compiled
configuration proves an original build match.

## Validation and next gates

34 new checks cover raw/virtual split and invalid bounds, independent periodic
mutation masks, version249 post-encode state, all short-write lengths, copy-save
invariance, create/reopen/read failures, v4/v5 ignored-write outcomes, failed
creation→v4 tail retention, all32 boolean preamble combinations, startup/static
metadata mutations and refusal of native/indirect/publisher promotions.
Combined with262 adjacent tests,296 checks pass. CI rederives three exact Git
blob source profiles independently; probe and source reports have complete
canonical fingerprints. No original program/source execution is involved.

Highest NEXT: resolve baseline Taiwan v1.0 savedata instruction windows behind
four `.text` address-word hits; retain indirect initialization/lifetime closure,
full cross-profile framing/checksum and authentic14-field server/native-pair
gates. Official full package/manifest remains opportunistic. Pressure unchanged:
2486=2465 bounded closed+18 OPEN+3 historical UB; no early-era/engine promotion.
