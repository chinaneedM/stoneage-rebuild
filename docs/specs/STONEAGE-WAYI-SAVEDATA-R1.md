# Wayi compiled local settings R1

FACT here means hash-pinned static instructions, not original execution. Scope:
accepted late archived client SHA256
`4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63`,
921600 decompressed bytes; sixteen aligned windows and44 direct backing
references. This is not Taiwan v1.0/early-era admission or an authenticated
operator/server pair. Original binary, source and raw disassembly stay outside Git.

## Settings encoding

Backing RVA `0x4319d28` is127 bytes. Named settings writers pass key0,
length127 and output capacity4000 to encoder `0x8e050`. This is a separate
primitive from login DES and network keyed-field/outer encoding.

For a nonempty bounded payload P, S is the sum of the **original** bytes modulo256.
Complement P[i] when i is even or divisible by5. Set E[0]=S; for n=i+1,
E[n]=(transformed P[i]+S*(n*n modulo7)) modulo256. The native encoder mutates its
source; the save writer supplies a127-byte stack copy, whereas the constructor
passes the global backing directly. Decoder `0x8e1a0` reverses the byte addition
and complement using E[0]. It does not recompute/validate the sum. This is not
an integrity/authentication check; generated tampering can retain valid version6
and length127 and still pass the bounded load decision.

The independent model implements key0/sufficient capacity/distinct buffers,
length1..127. The native encoder's insufficient-capacity raw-copy branch and
arbitrary-key/signed-square overflow/aliasing are outside that model. Native
decode divides by input length minus1 before validation. Loader reads up to4000
bytes and calls the decoder without an output capacity, then checks length.
The model rejects empty/one-byte/oversized encodings. Those guards are model
bounds, not recovered native guards; malformed-input memory behavior remains OPEN.

## Original load and migrations

Function `0x80760..0x808b4` resets the error byte at RVA `0x4319dac`, opens
`data\savedata.dat` with `rb+`, reads at most4000 bytes, tests CRT stream-error
bit0x20 and closes before decode. CRT routine labels derive from argument and
source comparison; they are not named Win32 imports.

| Condition | Compiled outcome |
| --- | --- |
| Missing file; creation fails | FALSE, error1 |
| Creation succeeds; reopen fails | FALSE, error2 |
| Stream read error | Close, FALSE, error3 |
| Decoded57 bytes; little-endian version4 | Low version byte=6; byte57=3; request save; TRUE |
| Decoded127 bytes; version5 | Low version byte=6; byte58=0; request save; TRUE |
| Other length, including57 with another version | FALSE, error4 |
| Decoded127 bytes; version6 | TRUE, no save |
| Decoded127 bytes; another version | FALSE, error5 |

The two migration calls to `0x80600` ignore its return. Success does not certify
successful persistence. No deletion or recursive load call exists in the entire
bounded original load function. The pinned descendant source has two remove
and recursive recovery branches instead. Its behavior cannot replace these
compiled outcomes.

A57-byte decode overwrites only backing[0:57]. Migration writes byte57 but does
not clear bytes58..126. Explicit prior backing therefore matters: initial
zero storage and reused/nonzero backing are different cases. No captured
savedata file or memory dump establishes a real user's tail. Version comparisons
are WORD-wide; migration writes only the low BYTE after that comparison.

## Named per-byte settings paths

| Backing offset | Bounded compiled use |
| --- | --- |
| 0..1 | Version WORD; migration low BYTE |
| 2..25 | No named field writer; copied/decoded/encoded as ordinary bytes |
| 26..35 | Two character slots, five pet slots each |
| 36,37,38 | Stereo, SE volume, BGM volume low bytes |
| 39..54 | Sixteen pitch bytes copied as four DWORDs |
| 55,56,57 | Chat color, line count, area |
| 58 | Cursor selection |
| 59..126 | No named field writer; copied/decoded/encoded as ordinary bytes |

Pet writer `0x809c0` accepts character0 or1, sets each byte to selection mask0x01
(value1) or0 and ORs value4 when its index matches the mail pet. Clear `0x80ad0`
zeros exactly five selected-character bytes. Reader `0x80a80` sets battle pet
WORD to-1, projects selection mask0x01 and applies each mail mask0x04 in increasing index
order. Last marked slot wins; no marked slot leaves the prior mail pet unchanged.
Conditional network sends and their return/runtime effects remain separate.

Sound `0x80b00/0x80b50` copies BGM as the full unsigned BYTE. Pinned descendant
source adds a mute bit0x80 and masks reads with0x7f; that source semantics is
absent from these compiled windows. Chat `0x80bb0/0x80be0` and cursor
`0x80c10/0x80c20` transfer their named bytes. Factory clears127 bytes and sets
version6/sound/pitch/line10/area3, but native constructor encoding subsequently
mutates the same backing. The factory model denotes **pre-encoding** state.

Source enum names CDKEY/PASSWORD reserve2..25 and are not active accessors.
Loaded legacy bytes survive named writers and migrations; constructor zeroing
alone cannot establish universal zero reserved bytes or credential persistence.
The44-reference sweep is a direct displacement/immediate surface in `.text`;
it does not prove absence of indirect aliases or other memory writers. The
bounded save body begins at `0x806ba`; preceding process-related control flow
at `0x80600` is not modeled as ordinary file IO.

## Reproducible acceptance

Derived ledger records window hashes, calls/branches/writes, selected operands,
and complete profile fingerprints. Exact-byte probe rejects another specimen.
Two descendant blobs at fresh observed master
`2f736808ff4361f5429ee919b718c88fabb60346` are Git-blob pinned. CI rederives their
lexical arithmetic/recovery/mute/reserved-slot distinctions without executing or
compiling original source.

34 new checks include all256 single-byte values, four deterministic samples for
each length1..127 against an independent periodic-mask/coefficient oracle,
hand-calculated byte vectors, full factory encoding, nonzero migration tails,
wrong lengths/versions, tampering without checksum validation, exact writer
slices, mail-state ordering and metadata/promotion mutations. Six stored vectors
are generated synthetic bytes, not archived files or wire captures.

OPEN: indirect writer/initial backing lifecycle; native malformed/capacity/
arbitrary-key behavior; save preamble and migration IO result effects; baseline
TW1.0 savedata indirection; complete cross-profile framing/checksum; authentic
14-field server/native pair and original publisher package/hash. Pressure stays
2486=2465 bounded closed+18 OPEN+3 historical UB; no engine promotion.
