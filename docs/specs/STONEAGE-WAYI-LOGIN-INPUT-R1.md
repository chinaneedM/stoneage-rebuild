# Compiled login input DES and storage paths R1

The specimen is the already accepted operator-linked client archived in 2006:
921600 unpacked bytes, SHA256
4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63.
Its exact 2005 release identity remains OPEN. Original software is never run.
All calculations use synthetic keys and blocks; no real credentials are read.

## Compiled primitive and independently checked numeric profile

| Compiled RVA | Bounded role |
|---|---|
| 0x8ebe0 | Eight key bytes, seven bits each, 28-bit halves, 16 scheduled round keys |
| 0x8ed80 | Initial permutation, 16 forward/reverse rounds, final permutation |
| 0x8f150 | ECB wrapper, existing backing rounded up to eight-byte blocks |

All nine compiled numeric tables match both separately pinned descendant client
and server DES arrays: shift schedule, PC1, both PC2 halves, 512 fused S/P values,
and four 256-entry initial/final permutation tables. Ledger contains RVAs,
counts, widths and SHA256s, never original table bytes or disassembly.
The independently written scalar model explicitly uses 32-bit words and
28-bit key halves. It passes forward and inverse checks against all 121 public
DES vectors in PyCryptodome3.23.0's test_DES module, and separately against the
library's DES cipher. Source of the fixture:
https://github.com/Legrandin/pycryptodome/blob/v3.23.0/lib/Crypto/SelfTest/Cipher/test_DES.py
Its SHA256 is recorded and rederived in CI. It identifies NIST SP800-17 inputs.

This establishes numeric DES structure agreement and synthetic model behavior,
not a native execution of the specimen. Source typedef unsigned long remains
platform-dependent; synthetic32-bit success does not validate a Linux64-bit
whole-source build. Native undefined behavior and malformed input are separate.

The wrapper masks direction with1, rounds (length+7)&~7 and transforms existing
backing memory. It does not create zero padding or PKCS padding. Synthetic model
requires explicit backing bytes for the rounded region. After transformation,
mode bit2 determines return0 versus1; modes0/1 can transform and return1. UI
callers do not branch on that return in the bounded windows. Embedded literal
f;encor1c is nine bytes; the schedule consumes its first eight. It is a static
program constant, not a recovered user/session credential.

## Compiled editable buffers, encrypted globals and login projection

| Path | Source | Destination | Bytes / direction |
|---|---|---|---|
| UI restore0x2074c | globalRVA0x15d834 /0x15ca78 | buffers0x155ae0 /0x160a48 | 32 each, mode1 decrypt |
| UI save0x2097d | same editable buffers | same two globals | 32 each, EBX=0 encrypt |
| Connect state71 | first16 bytes of each global | stack local strings | 16 each, mode1 decrypt |

UI function prologue explicitly zeroes EBX. Both UI copies use eight DWORDs;
connect path uses four DWORDs. After UI save the editable descriptors have
count/cursor clearing and 65-DWORD clearing, separately recorded; do not infer
C array capacities from that clearing span. The login send and post-send
field-key switch remain the previously accepted independently observed order.
Synthetic 32-byte ECB storage recovers all32 bytes for UI, while independently
decrypting its first16-byte prefix recovers exactly the first plaintext half.
It does not attest termination or user behavior for any actual long input.

Initializer0x20ba0 passes12 for both input descriptors. Setter0x211c0 stores
that fourth argument as BYTE at descriptoroffset0x104. Current descendant
login.cpp passes18 and uses different UI coordinates. The compiled12 parameter
is not proof of an enforced12-byte keyboard limit: keyboard/IME handling,
byte-versus-character count and terminator rules remain NEXT.

Source names idKey.buffer/passwd.buffer/szUser/szPassword support semantic
comparison of these otherwise independently matched compiled paths. They do
not establish identical source/build. No usernames/passwords are supplied,
recovered, printed or sent, and no original client/server or login is executed.

## Admission limits and next work

Six fixed source blobs and exact table hashes are rechecked; the workflow
rederives the numeric model comparison without compiling original source.
Existing F-versus-N greeting, key defaults, default TEA-versus-legacy selector,
and 13-versus14 item-field differences remain distinct compatibility gates.
A matching authenticated original operator server and native owner/save/drop/
unique lifecycle have not been admitted. Pressure2486=2465+18+3 unchanged.

Next: compiled keyboard/IME input-length and terminator handling, persistence
and initial global writers, full framing/checksum profiles. Original2005 full
package/manifest remains opportunistic. No early-era or engine promotion.
