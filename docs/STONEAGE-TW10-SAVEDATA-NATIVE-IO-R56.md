# TW1.0 R56 — conditional application frame and native write-request binding

Status: READY; exact R54/R55 metadata available.

Highest NEXT R56: bind conditional R55 writer output/count to the savedata application write request0x40090 using the exact R54 numeric inventory. Qualify the specific frame helper CALL0x40025->0x49160 (EAX literal4132), including its page-probe reads, ESP rewrite, saved ECX/return-address relocation and conditional near-return geometry on invented storage only. Then replay caller REP/MOVS copy127 candidate, six transform pushes, post-transform/open ADD ESP,32, load0x40080, write-buffer LEA0x40086, write physical suffix and post-write count comparison0x4009c. Keep direction flag/segments/address validity and opaque open/write/close preservation/alias effects explicit. Separate conditional output128/write-request correspondence from actual native write/flush/close/persistence success. Prefer pinned metadata; retrieve originals only for an identified missing scope. Do not expand generic CRT ownership work, evaluate original payloads, or promote field schema/tag/version/migration/checksum/server authority/cross-version equivalence. Stage A precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.

Specific existing evidence: helper17 rows at0x49160, literal4132 at0x40020, caller55 rows at0x40020 and transform129 rows. Treat hardware near-CALL/RET address movement separately from ordinary opaque-call assumptions. A valid result must preserve partial/unknown states when probe memory, REP DF/segments or opaque callees are unqualified. No generic allocator/CRT expansion is justified.

## Readiness worksheet — conditional hypotheses, not accepted R56 evidence

Let S denote writer0x40020 entry ESP. A candidate symbolic reading of the17 helper shapes is: near CALL enters at S-4, PUSH ECX adds a saved four-byte value at S-8, LEA ECX,[ESP+8] yields S, the4096-byte loop plus final remainder subtract the requested EAX amount, ESP is replaced with that coordinate, the saved ECX and original return-address marker are loaded from the old stack, and PUSH/RET relocates the marker. If all reads/addresses/flags and near-return conditions are valid, the candidate caller continuation ESP is S-4132. R56 must test this relation against the full numeric shape/edge inventory, including zero/page-boundary/multiple-page invented cases; no actual helper allocation is admitted here.

Under that still-unqualified helper effect, clear REP direction with compatible flat segments, valid memory and ordinary near-return stack effects for subsequent opaque calls, the candidate caller coordinates are:

| Candidate | Coordinate relative to S | Size or condition |
|---|---:|---|
| Length cell from LEA EAX0x4003a | -4132 | four bytes |
| Snapshot from LEA EDI0x40036 and LEA EDX0x40052 | -4128 | conditional127 bytes |
| Unused separation before output | -4001 | one byte |
| Transform output from LEA ECX0x40045 | -4000 | capacity4000, ending just before S |
| Pre-transform CALL0x4005a ESP | -4164 | six pushes plus saved ESI/EDI |
| Pre-open CALL0x40069 ESP | -4172 | two additional pushes |
| After ADD ESP,32 at0x40070 | -4140 | requires returned-call stack premise |
| Length load0x40080 from[ESP+8] | -4132 | candidate same length cell |
| Pre-write CALL0x40090 ESP | -4156 | four physical pushes |
| Write LEA0x40086 buffer | -4000 | candidate same output buffer |
| Post-write0x40095 load[ESP+24] | -4132 | candidate same length cell |

This is a worksheet for the next acceptance task, not proof of actual aliases, initialized values, a successful copy, returned count or persistence. In particular, arbitrary opaque callee writes could invalidate the length cell or buffer even if ESP geometry agrees. Preserve those memory/preservation conditions separately from the helper's hardware stack calculation. Do not infer a historical ABI or actual file-size promise from this table.


## Independent acceptance — 2026-10-15

Status: ACCEPTED for conditional helper/copy/caller/write-request geometry and invented control paths; actual native persistence remains OPEN. The earlier worksheet is superseded only within the explicit valid-storage/copy/opaque-preservation model premises.

R56 source Action38730761697/job116407664800 SUCCESS at HEAD453ff20ca9f30ca9f05b1b42551508c7053f9cb5, branch agent/tw10-savedata-r56-application-frame-20261015. Authenticates immutable R51/R52/R53/R54/R55 metadata custody and exact bytes; R54 raw132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R55 spec103165-byte SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863 pinned before extension. R56 artifact11969389801 tw10-r56-conditional-application-frame-spec ZIP SHA25695938cabdcd015aa3e273cc541bd38e1fbd7f8cdf91716b895c7b132abf2e028; canonical raw67492 bytes SHA256db5628403b366e706e212bd7627f40861097d78bfb3f3acb0d95598bce70981c. Independent Action38731138905/job116408925725 SUCCESS at HEAD601b5f63bf47c0c1d799ed9fd7b94a3d8d07af94 authenticates all six immutable source/run/head/branch/artifact chains, strict R54 inventory/stack replay, exact R55 regeneration and exact R56 reproduction/equality; a separate all-path caller ESP algebra agrees at55 sites and preserves unknown downstream states without opaque-call stack premises. Source780 tests PASS; independent788 tests PASS (734 inherited plus54 R56 controls). Local54 pure metadata/model/algebra tests plus syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/executable/save payload retrieved, evaluated, executed or published; only numeric metadata and generated invented storage/stubs used.

FACT (conditional numeric metadata specification and invented-storage verification only):

- All17 helper0x49160 shapes/18edges and55 caller0x40020 shapes/54edges retained. Helper and caller numerical models dispatch only observed bounded shapes on fabricated storage. CALL observations dispatch explicit helper/transform model abstractions or invented open/write/close stubs; they do not execute original code or any OS/native API.
- Under valid32-bit memory/near-return geometry, the helper restores saved ECX and relocates the return marker so caller continuation ESP is S-requested_amount. Literal4132 gives conditional S-4132.305 invented helper amounts in0..65536 include0..256, page boundaries and literal4132; all17 shapes exercised. Whole-page probe offsets are followed by -amount, including a duplicate final address for exact page multiples. Failed invented probes stop qualification; actual page-probe/allocation success remains unknown.
- With clear DF, compatible flat source/ES segments, valid initialized/disjoint storage,31 repeated dword copies plus word/byte copies make a127-byte invented snapshot. Conditional S-relative regions are length cell[-4132,-4128), snapshot[-4128,-4001), one-byte padding[-4001,-4000), output capacity[-4000,0). REP validity/actual source values remain conditional.
- Six transform slots map to snapshot,count127,seed0,output,length-cell,capacity4000. With explicit opaque-call stack and live-memory preservation, post-open load0x40080[ESP+8] and post-write load0x40095[ESP+24] share S-4132. Write LEA0x40086 gives S-4000; CALL0x40090 physical slots are buffer(S-4000),literal1,count128,opaque-open-return shape.256 invented snapshots spanning every derived key byte verify requested bytes/count equal R55 model output. No file bytes are written.
- The five witness pre-instruction ESP coordinates at0x4005a/0x40069/0x40080/0x40090/0x40095 are -4164/-4172/-4140/-4156/-4156. Independent all-path ESP algebra checks all55 sites and three exit coordinates0. Without opaque-stack premises it retains the known prefix and marks post-open coordinates unknown, rather than assuming returning calls have zero actual effect.
- Two invented memory-clobber counterexamples preserve stack geometry but change request count128->127 or output content. Thus same address is not sufficient for count/content identity. Without opaque-memory preservation the report explicitly withholds content/count binding; unknown DF/segments/helper validity similarly prevent qualification.
- Seven invented open/write/close-return cases plus successful fixtures cover all55 caller shapes. Unsigned JAE0x4009e follows CMP0x4009c. Short-return path gives literal0 without close-call candidate in this bounded graph; >=count reaches CALL0x400ac then MOV EAX,1 at0x400b4 overwrites the close-return-shaped result. High-bit invented write returns also take the unsigned branch. These are syntax/model control facts, not native error conventions, successful close/flush/persistence or an actual resource-leak claim.

OPEN: actual helper/REP/alias/callee preservation, original wrapper returned-count/error meanings and native write/close/flush success, original payload/fields/tags/version/schema/checksum/migration/persistence, server authority and cross-version equivalence. Stage A system-family PARTIAL/OPEN gates unchanged.

No failed source or independent report admitted; both publication gates passed first run. Existing R54/R55 metadata was sufficient; original retrieval was not repeated.

Highest NEXT R57: qualify actual savedata write-wrapper return/count/error syntax at CALL0x40090->0x48bbc and close-wrapper CALL0x400ac->0x4856c, separating the caller's unsigned JAE/literal1 from native write/close success. R42 retains a complete106-node/119-edge write-wrapper graph and106 numeric stack effects but only5 early operand shapes and1 frame definition; this is insufficient to reconstruct all returned EAX/count/control paths. Audit all existing R42-R49 metadata first, then retrieve authenticated originals only for missing complete write-wrapper/close-wrapper numeric inventories. Requalify exact prior original metadata, recover bounded complete instruction/branch/call/return shapes and preserve opaque nested calls, alias/frame and actual return/error-value gaps. Prioritize savedata-specific return/cleanup obligations, not generic CRT ownership exhaustion. Do not evaluate original payloads or promote a successful actual128-byte native write/close/flush, field schema/checksum/migration/persistence, original server authority or cross-version equivalence. Stage A restoration precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


### R56 main integration verification and R57 inventory preflight

Accepted milestone integrated at821d1e2a5123e9effea74e9b8ea11027ea10cd49/treeb0cd778fbd2e8f6b867bfa379f8fd15ca802ff32. Main independent Action38731492812/job116410095677 SUCCESS:788 tests, immutable specification equality and independent55-site caller algebra. Main PET38731492980/late-provenance38731493104 SUCCESS; branch independent38731491551/PET38731492669/late-provenance38731491346 SUCCESS. Exact checkout, raw size/SHA and all earlier continuity prefixes verified.

R57 preflight searched all111 matching research/recovered/STONEAGE-TW10-SAVEDATA-*.json reports (largest284533 bytes; none exceeded the2000000-byte search bound). Their union contains30 operand-bearing mnemonic/site shapes at the106 R42 write-wrapper graph nodes, leaving76 without complete operand shapes in this search. The close range0x4856c<=site<0x48660 has zero such rows. This is an inventory search, not new semantic/row validation; it justifies fetching missing original write/close static inventories next. Highest NEXT remains R57, with no original payload evaluation or generic CRT ownership expansion.
