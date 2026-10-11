# Operator-linked StoneAge2 manifest route R1

The accepted operator-linked updater response was captured September8 **2006**, not2005. Packed SHA256a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f; static UPX output253952 bytes/SHA256d0d9c33acc7eb47c2f625b827d5e30daccd29cb9782ff6c302b730e0a5406b2f. This work consumes only that pinned local decompressed file. Original game is never executed; no live server contacted.

## Static route evidence

Image base0x400000. The following are derived operand/control-flow observations of this exact specimen; roles are analytical names, not source symbols.

| Code RVA | Observation | Implication |
|---|---|---|
| 0x19ae–0x19d6 | stoneage.wayi.com.tw literal copied to global RVA0x856c0 | Default host buffer |
| 0x19df | WORD global RVA0x85840 receives0x1f90 | Default port8080, not80 |
| 0x1a03,0x1a0d | HKLM Software\Wayi\石器時代\5.00.000 passed to RegOpenKeyExA via ESI | Primary installation-key check |
| 0x1a11→0x1a63 | Primary open success jumps to newest7x default | Folder/resource generation label is not commercial release number |
| 0x1a1f,0x1a29 | Old HKLM Software\Waei\石器時代\5.00.000 fallback check | Separate old-key branch |
| 0x1a2f–0x1a5b | Secondary success copies /saupdate/newest6.txt, then returns | This branch skips path-file override |
| 0x1a5e→0x18a0 | Both opens fail, call primary RegCreateKeyExA/RegSetValueExA helper | Setup attempt, then fall through to newest7x; not proven setup success |
| 0x1a63–0x1a8b | /saupdate/sa70a/newest7x.txt copied to global RVA0x85740 | Primary/default manifest path |
| 0x19c7,0x1a95,0x1abf | Format %s/data/path.txt, open/read first line | Local override may change path; file itself missing |
| 0x1ad4–0x1ad9 | Decrement length and overwrite last byte with NUL | Do not model as unconditional newline trimming; final non-newline byte also removed |
| 0x1af1,0x1b07 | Helper0xf170 scans substring and returns pointer or zero | Requires both saupdate and newest substrings; not exact string comparison |
| 0x1b26 | Valid nonempty candidate copied to path buffer | Path string not necessarily one of default filenames |
| 0x1b41 | Failed nonempty/substring condition calls DeleteFileA | Invalid local override file removed by original historical code, never by our tool |
| 0x3d4e,0x3d69,0x3d73,0x3d7a | Load shared port word, pass path and host to helper0x3eb0 | Default address and port reach download-call argument preparation |
| 0x3fa4–0x3fb7,0x6370–0x638e | Port argument passed into socket setup, external WSOCK32 ordinal9 result stored as sockaddr WORD | Additional port-flow evidence; no live-connect claim |
| 0x4009–0x400f | GET %s\r\n literal passed to wsprintfA | Historical GET-line format, not proof of a full HTTP/1.x request |

An empty read/zero length reaches decrement/write-before-buffer risk; no natural occurrence or broad historical-UB accounting change is asserted. Runtime selected key state, contents of path.txt, and selected live route remain OPEN. It would be wrong to treat both default manifests as always fetched, infer version7 from newest7x, or certify original2005 release bytes from2006 capture plus mutable header.

## Corrected archive acquisition

Default-port80 manifest replay queries from the previous round remain true **request-specific**404 outcomes, but are insufficient to test the updater's default8080 route. New exact-port8080 replay requests for both filenames returned **archive404**, and bounded2004–2007 prefix CDX query returned `[]`. Exact FTP Stoneage80.exe CDX now returned `[]`, superseding previous503 only for this new request. No result proves global absence or historical unavailability.

A bounded download.wayi.com.tw prefix index produced22 data rows, including a **404-captured**2006 `/download/STONEAGE20060616.exe` path. That is an archived error record, not a recovered installer or authenticated8.0 package identity; unrelated3P/A3/mahjong binaries must not be treated as StoneAge. CDX archive-record lengths are not raw executable sizes. No manifest or full installer bytes obtained.

## Reproduction and acceptance

`python -m tools.stoneage_wayi_saupdate_route_probe /path/to/StoneAge2-unpacked.exe` rejects wrong length/hash, validates PE32 and bounds all selected executable windows. Uses Capstone5.0.7. Emits literal locations, instruction counts, selected operand shapes/control destinations/import identities only; no program bytes or disassembly text. Ten synthetic decoder/bounds tests plus47 adjacent PE/archive tests run offline; CI never fetches or executes an original program. Derived ledger `STONEAGE-WAYI-SAUPDATE-MANIFEST-ROUTE-R1.json` preserves source, query URLs/outcomes and exact code RVAs.

Highest NEXT: recover official package or its local data/path.txt/manifest with publisher hash/custody; use correct8080 defaults as version-labelled archive hypotheses. Bounded static sa.exe PET protocol analysis is possible using the independently acquired game specimen, but cannot yet count as natural PET owner/save/unique-code/opcode127 runtime. Pressure2486=2465+18+3 unchanged; no modern engine or JSS1999/TW1 promotion.
