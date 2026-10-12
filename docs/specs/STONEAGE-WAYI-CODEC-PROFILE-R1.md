# Wayi compiled outer codec, key binding and framing R1

Evidence: exact operator-linked archived client captured 2006-09-15, decompressed
SHA256 `4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63`.
Its 2005 original release equivalence remains OPEN. The original game is never
executed. Decoder Capstone5.0.7 only reads bounded instruction windows.

## FACT — compiled outer codec

Encoder0x8fc10 takes rand remainder99, destination-permutes four little-endian
seed bytes by2413 at0x90590, complements all bits, and packs with alphabet
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{} at0x8fed0.
This is low-bit-first packing, not standard Base64. Each byte emits one symbol;
every third byte emits an extra symbol. Nonzero residual is emitted, zero
residual is omitted. Valid seed0..98 after complement always has six symbols.
Rotate message left by seed modulo byte length (0x906c0); prepend seed header;
complement each byte (0x905c0). Decoder0x8fcd0 removes a terminal LF if present,
complements, decodes the first6symbols (0x8ff70), complements seed, applies3142,
and rotates the remaining message right (0x90620). The outer layer does not
reference the field-key buffer. Integer/string field wrappers independently do.

Synthetic model tests every99seeds against a second streaming construction on
one-byte, ASCII and long printable inputs, plus Big5-like bytes. Four stored
vectors are synthetic examples, not captured wire and not original execution.
Malformed input behavior is deliberately outside the model. Original decoder's
invalid-symbol retained-pointer behavior is not reproduced as validation.

## FACT — key binding, conditional suffix and framing

Field wrappers0x90740/0x907a0/0x90860/0x908a0 pass keybufferRVA0x4bb4694.
Connect bounded route0x5f539 copies literal at0xc8548 through lstrcpyA.
Post-login window0x5f979 tests (modeglobalRVA0x4205070 &0x0f000000)==0x0f000000;
both branches copy the same stack-supplied base, then append different literals:
0xc8514 versus0xc8508. Their exact strings and import identities are recorded in
the ledger. Base username identity requires upstream definition; suffix text
that resembles a date does not prove a build date, release date or credential.
Default/suffix literals differ from the pinned descendant server's
_DEFAULT_PKEY/ _RUNNING_KEY defaults. Neither selected live mode nor negotiated
session key has been observed.

Send hub format remains `&;%d%s;#;` with logicalID+13. Handoff appendsLF only
when encoded length<3*configuredsize, otherwise bounded branch skipsappend;
callback still receives resulting length. LF linehelper scans buffered bytes
and has CR stripping, then consumes line. Its backward CR scan starts beyond
copied prefix; do not infer universally safe/canonical CRLF handling from it.
ClientreceiveID-23 and serversend+23 are different directions from clientsend+13
and serverreceive-13. Directional biases alone do not establish compatibility.

## SOURCE — independently pinned descendant comparison

Fresh BismarckDD/Stoneage master/dev both resolve
2f736808ff4361f5429ee919b718c88fabb60346. Seven source blob hashes recorded,
including clientautil369f2b35a812535557d55496626ff6a2cac1c56b and serverautil
c1f4886c879d6d847017cc53373e9e6ead28ae28. Source legacy outer helpers match this
mathematical envelope. Server version.h defines_NEW_FUNC_DECRYPT and autil.c
has an alternative TEA/hex decoder under that gate. This is source membership,
not an executed whole-build profile; exact inbound wrapper/build must be checked
before asserting active deployment. Client_NEWNET_ condition is also separate.
Key defaults differ. Previous13fieldserver versus14fieldclient mismatch persists.
No candidate authenticated operator server or native paired runtime is admitted.

## NEXT

Recover keyed integer/string helper arithmetic, upstream stack base and mode
assignments; establish exact selected source preprocessing/receive wrapper
rather than macro presence alone. Add independent directional synthetic field
vectors with explicit nonempty key profiles and bounded framing domains.
Nativeowner/save/drop/unique lifecycle, full installer/original publisher hash,
and historical early-version membership remain OPEN. Pressure2486=2465+18+3
unchanged; no modern engine transition.
