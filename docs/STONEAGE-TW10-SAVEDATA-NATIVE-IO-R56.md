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
