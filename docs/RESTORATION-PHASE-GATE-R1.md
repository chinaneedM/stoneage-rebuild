# Restoration-first stage gate R1

Status: **ADOPTED WORK ORDER; NOT A COMPLETION CERTIFICATE** (2026-10-12).

## Goal and sequence

First reconstruct and verify as much historically grounded StoneAge material
as can reasonably be recovered. **Only after an auditable historical recovery
review** shall the user and assistant decide how to design and produce their
new modern single-player StoneAge. Do not accelerate to engine/asset/gameplay
production simply because a technical milestone or a reported percentage rises.

## Baselines and historical boundaries

- **FOUNDATION:** accepted clean Taiwan Waei/JSS v1.0 disc and pinned
  evidence-derived metadata. It is not asserted byte-identical to JSS 1999.
- **ORIGIN:** JSS 1999 archaeology and original-design intent, including
  explicit differentiation between published concepts and shipping mechanics.
- **BRIDGES:** Mainland 1.82 and other independently proven early versions.
  Labels without verified client bytes are candidates, not accepted builds.
- **LATER COMPARISONS:** 2.5, 8.0/8.5 and other versioned materials are useful
  controls and a future content reference library, not automatic 1.0 facts.
- **SERVER LIMIT:** retail-client absence does not prove the absence of a
  server-authoritative mechanic; missing original server datasets remain OPEN.

## Completion register (evidence-based, no decorative aggregate percentage)

| Recovery family | Evidence required before closing the family | Current gate |
| --- | --- | --- |
| Original provenance and version lineage | Hash-pinned specimens, independent original identity, cross-version diffs | PARTIAL: TW1.0 foundation accepted; 1999 original and specific regional bridges have gaps |
| Executable/runtime and persistence | Static+dynamic attribution where possible, stack/object ownership, file IO, native save framing/checksum | OPEN: TW1.0 R14 exact register input and caller/global effects |
| World, maps, movement and encounters | Version-scoped maps, transitions, event triggers, geography, spawn and encounter data | PARTIAL: complete original world/server layer not accepted |
| Characters, pets, growth and capture | Deterministic formulas, authority/profile distinctions, client/server evidence | PARTIAL: substantial version-tagged recovery; unresolved authority/gaps |
| Battle, turns, skills and status | End-to-end reproducible scenarios with provenance and negative controls | PARTIAL: extensive battle evidence; outstanding profile/entry/reachability limits |
| Inventory, equipment, economy and drops | Identity, ownership, transaction/transfer, rewards, integrity and persistence | PARTIAL: extensive recovered and tested mechanics; full cross-system closure OPEN |
| Quests, NPC dialogue and progression | Versioned original scripts and server-dependent transitions or explicit gaps | OPEN: do not reconstruct missing original scripts as facts |
| Graphics, animation, sound and UI | Asset/format metadata, display and interaction rules, provenance, licensing boundaries | PARTIAL: engineering/source extraction exists; complete original coverage not accepted |
| Integration and reproducibility | Cross-system deterministic test matrices, version isolation, independent CI/artifact custody | PARTIAL: subsystem evidence exists; full historical acceptance pending |

PARTIAL means work exists, **not** that the listed family is nearly complete.
OPEN means evidentiary closure has not been demonstrated. Both categories
require concrete, version-scoped evidence before advancement.

## Acceptance requirements

1. Inventory every recoverable subsystem and evidence source, with baseline,
   file/build identity, source confidence, date, and what it does **not** prove.
2. Deliver reproducible extraction reports/specifications and bounded tests.
   No original proprietary binaries or assets enter the public repository.
3. Cross-check shared gameplay state and end-to-end dependencies (world ↔
   encounter ↔ combat ↔ reward ↔ roster/inventory ↔ save).
4. Distinguish FACT, HYPOTHESIS, DESIGN and OPEN. Permit explicit **evidence
   unavailable / original server authority unrecovered** closures, without
   misrepresenting them as fully restored facts.
5. Publish an evidence-backed acceptance matrix for all families, including
   unresolved limitations, regressions, historical-version scope, and the
   exact remaining production risks.
6. Obtain a separate joint user review of the restoration results **before**
   choosing a new engine, committing to new lore/era integrations or starting
   the full modern game build.

## Immediate work queue

- TW1.0 R14: determine conservative reaching definitions for EBX at 0x49dec,
  EAX/ESI at 0x4943c/0x4944a/0x49457/0x49463, graph bounds, CALL barriers,
  possible frame prologues and branch joins.
- Next: independently qualify original native persistence / handle / buffer
  semantics if the evidence permits; never silently collapse uncertainty.
- Continue the version-tagged inventory and original world/server gap closure
  without promoting later rules to the earlier baseline.
- Non-core 8.0 provenance tests must not be invoked solely by general
  TW1.0 `CURRENT-STATE.md` continuity updates.

See `docs/CURRENT-STATE.md` and `DD-021` for authoritative next tasks.

## 2026-10-12 queue supersession (R21 accepted)

The original immediate-work bullet retained above describes the historic
R14 entry point; the current authoritative latest CURRENT-STATE entry
supersedes it. R14–R21 bounded static evidence and independent custody
receipts are available; **R21 is conditional static acceptance only**.
Current highest NEXT is **TW1.0 R22**: CALL 0x499d4 effects/input
barriers, HeapReAlloc 0x4a0c4 pre-CALL source feasibility and
post-CALL opaque return, and cycle-aware EAX alias at 0x4a17d.
The original native-save persistence gate and all other system-family
PARTIAL/OPEN states remain unchanged. Engine/content production is
still deferred until joint review of Stage A.


## 2026-10-12 queue supersession (R22 accepted)

R22 original bounded static CALL/global/PUSH/cycle evidence is independently
accepted with hash-pinned original-source run, derivative artifact, guard,
negative controls and exact JSON custody. KERNEL32.dll!HeapCreate association
does **not** close original runtime heap ownership, native persistence,
file/handle/buffer linkage or effective write values. The original system
family gate status remains **OPEN/PARTIAL**, unchanged.

The latest CURRENT-STATE entry supersedes the earlier R21 queue. Highest
NEXT R23: correlate HeapCreate→HeapAlloc→HeapReAlloc *candidate* global/heap
sources with explicit CALL effects and path/stack boundaries, not an assumed
single heap or original SaveData model. Restoration before future-game
architecture remains binding.


## 2026-10-13 queue supersession (R23 accepted)

R23 original heap-call/global/PUSH geometry is independently accepted as
conditional static evidence only. All three EAX global stores retain opaque
CALL sources. Local pre-CALL stack offsets are not ABI/runtime argument proof.
Same-address dependencies do not establish common heap ownership or native save.

Highest NEXT R24: exact stopping prefixes before HeapCreate/HeapAlloc final
PUSH, caller-entry/stack boundaries, and HeapReAlloc EAX0x4a0b3 computation
and branch predicates. System-family PARTIAL/OPEN states remain unchanged;
Stage A restoration before joint future-game review remains binding.


## 2026-10-13 queue supersession (R24 accepted)

R24 competing candidate instruction spans, prefix barriers, EAX scalar and
pre-call comparison provenance are independently accepted as conditional
original static evidence only. Candidate anchors inside alternate decoded
instruction spans are not original function entries; no runtime size/ABI/heap
or native-save promotion is admitted. Prior conditional diagrams/counts remain
diagnostics, with explicit conflicting-prefix caveats.

Highest NEXT R25: coherent boundary/direct caller candidates near HeapAlloc
0x499ff and HeapReAlloc0x4a0a1, with SETE AL/upper-EAX and shifted ECX inputs
still OPEN; then use qualified context for native filename/IO tracing.
All system-family PARTIAL/OPEN statuses and restoration-first review remain.


## 2026-10-13 queue supersession (R25 accepted)

R25 full raw-text boundary/direct-transfer candidates and new-anchor input
sources are independently accepted as conditional original static evidence.
Direct CALL targets supply entry candidates, not complete/actual function or
caller proofs. Old SETE graph roots fail to reach the site; those empty sources
cannot support value/absence claims. Native persistence/heap/ABI remain OPEN.

Highest NEXT R26: use direct CALL-supported0x499c3/0x4a09c contexts for SETE
flags/full-EAX and ReAlloc EAX/ECX inputs, with bounded opaque-call/path gaps,
then resume qualified native filename/IO analysis. All system-family
PARTIAL/OPEN statuses and Stage A restoration-first review remain binding.


## 2026-10-13 queue supersession (R26 accepted)

R26 direct CALL-supported candidate contexts, SETE/zero/flag provenance,
separate global inputs and conditional32-bit affine expression are independently
accepted as original static evidence only. Actual functions/paths/stack frames,
ZF/globals/results, ABI roles, heap/CRT/alias ownership and native IO stay OPEN.

Highest NEXT R27 returns to the original native file-API boundary/direct-caller/
physical argument chain at CreateFileA0x4ed01 and ReadFile/WriteFile candidates.
Retain allocator gaps while auditing filename/returned handle/buffer/length128;
no native schema/persistence promotion until independently qualified. All
system-family PARTIAL/OPEN states and Stage A restoration-first review bind.


## 2026-10-13 queue supersession (R27 accepted)

R27 original file-API inventory, five conditional pre-CALL PUSH suffixes and14 nearby direct caller candidates independently accepted. None establishes actual filename/handle/buffer/128-byte linkage, ABI role, true entry/frame/path, external-return or file/CRT/heap/alias ownership. Current heuristic graph at WriteFile0x4c6f1 does not reach that site; empty sources are not absence facts.

Highest NEXT R28: audit direct CALL-supported original contexts0x4eb55 (CreateFileA),0x4a8dc (ReadFile) and0x4c5b4 (WriteFile), with explicit span/path/entry bounds; trace EBP-frame inputs and [EBX]/[EAX+ESI] handle-like syntax as candidates, never actual handle ownership. Correct WriteFile0x4c6f1 unreachable heuristic root before using its sources; extend bounded analysis to third WriteFile0x4e42b if useful. Native savedata filename->returned handle->buffer/length128 remains OPEN. All system-family PARTIAL/OPEN states and Stage A restoration-first review remain binding.


## 2026-10-13 queue supersession (R28 accepted)

R28 CALL-supported file API graphs/inputs independently accepted as original conditional static syntax. All five target sites reached, including corrected WriteFile0x4c6f1 context; shared virtual .data0x1721760+4*EAX addressing candidates do not establish original index/table/handle/owner/initialization values. No returning-call/frame/ABI/native persistence promotion.

Highest NEXT R29: inspect exact original operand shapes and conditional scalar input provenance at ReadFile index definition0x4a8f9/ESI0x4a8fc and WriteFile index0x4c5d3/ESI0x4c5e0 plus EAX0x4c617. Qualify the shared0x1721760+4*EAX addressing candidates without evaluating original values or asserting a handle-table owner; audit bounded writes/references if useful. Continue filename/CreateFileA-return/handle/buffer/length128 linkage with explicit opaque-call, cycle, stack-frame and memory-alias gaps. Native schema/persistence remain OPEN. All system-family PARTIAL/OPEN states and Stage A restoration-first review remain binding.


## 2026-10-13 queue supersession (R29 accepted)

R29 five original scalar shapes and separate conditional u32 models plus25 shared-address operand candidates independently accepted. SAR EAX5/SHL ESI3/ADD EAX,ESI syntax does not prove actual indices/offsets/effective addresses or a native128-byte schema. Direct shared-global MOV0x4c9da is a writer candidate, not original initialization/alias completeness/CRT ownership proof.

Highest NEXT R30: inspect exact input definition shapes0x4a8f6/0x4c5d6 before SHL to qualify any conditional index/offset composition without asserting actual descriptor values, ranges or ownership. Audit direct MOV-to-shared-global candidate0x4c9da source and acquire coherent boundary/direct CALL support before using its context; immediate-address candidate0x4e77f may aid discovery. Continue native CreateFileA returned-handle capture and filename->handle->buffer/length128 with explicit call/stack/alias gaps; no CRT/table/native schema/persistence promotion. All system-family PARTIAL/OPEN states and Stage A restoration-first review remain binding.


## 2026-10-13 queue supersession (R30 accepted)

R30 original AND31/SHL3 composition, direct CALL/boundary discovery and shared-global writer inputs independently accepted as conditional static syntax. Root0x4c9ba reaches ESI store0x4c9da; root0x4c953 does not reach that global writer, but seven CALL candidates include CreateFileA numeric-continuation0x4ed26->0x4c953. No actual offsets/descriptor ranges, initialization/owner/aliases or native schema/persistence promotion.

Highest NEXT R31: return to original CreateFileA0x4ed01 conditional continuation from0x4ed07 and audit direct CALL0x4ed26->0x4c953 (exact R30 scan candidate). Recover physical PUSH/register sources and bounded callee memory-store candidates, with explicit entry/path/return/stack/alias uncertainty; no actual API EAX/handle success or CRT/FILE owner admission. Retain global writer0x4c9ba's opaque calls0x4c9c6/0x4c9d4 as independent initialization gaps, audit their identities only if useful, and do not block the whole native save chain on generic allocator exhaustion. Filename->returned handle->ReadFile/WriteFile buffer/length128/schema/persistence remain OPEN. All system-family PARTIAL/OPEN states and Stage A restoration-first review remain binding.


## 2026-10-13 queue supersession (R31 accepted)

R31 opaque CreateFileA EAX->ESI copy and distinct intervening CALL0x4ed1f->PUSH EAX->0x4c953 source evidence independently accepted. Five helper-global writes to0x172120c/0x1721208 are separate static candidates; helper's mapping-like role remains HYPOTHESIS until call/branch evidence. No actual native handle capture, caller parameter/ABI, global owner/aliases or schema/persistence promotion.

Highest NEXT R32: identify original intervening CALL0x4ed1f and the predicate/branch reaching0x4ed26 to qualify the helper's mapping-like role. If justified, audit conditional physical PUSH EAX offset0 -> helper entry [ESP+4] hardware geometry separately from any API return/owner claim. Resume captured ESI0x4ed07 along other candidate parent paths and inspect parent memory-store/call inputs; do not mistake0x4c953's globals for the shared0x1721760 address candidates. Actual filename->CreateFileA result->ReadFile/WriteFile buffer/length128/schema/persistence, alias/frame/return effects and CRT/heap ownership remain OPEN. All system-family PARTIAL/OPEN states and Stage A restoration-first review remain binding.


## 2026-10-14 queue supersession (R36 accepted)

R32–R36 original conditional static CALL/flag/operand topology evidence and independent derivative custody are accepted. R36 structural branch routes, PUSH spelling, low-byte projections and address candidates do not establish actual handles, API/ABI effects, owner/alias identity or native schema/persistence. All system-family PARTIAL/OPEN states remain unchanged.

Highest NEXT R37: original continuation helpers0x4ed49->0x4e80a and0x4ed87->0x4c761, conditional PUSH/register/helper-memory geometry, partial-register definitions and three store address candidates. Native filename->CreateFileA-result->ReadFile/WriteFile buffer/length128/schema/persistence stays OPEN. Stage A restoration before joint future-engine/game review remains binding.


## 2026-10-14 queue supersession (R37 accepted)

R37 independently accepts two original CALL-supported helper contexts, shared-displacement/static import candidates and separately classified byte/full-width scalar operands. This does not demonstrate actual handle/descriptor/table ownership, caller/helper parameter binding, API/ABI results, file seek or native schema/persistence. All system-family PARTIAL/OPEN statuses remain unchanged.

Highest NEXT R38: first helper stack-prefix and caller PUSH geometry, exact shared-store source/width and scalar/address inputs, retaining opaque SetStdHandle/SetFilePointer effects and all alias/frame/return gaps. Stage A comprehensive restoration remains prior to joint future-engine/game review.


## 2026-10-14 queue supersession (R38 accepted)

R38 independently accepts conditional ESP slot geometry and exact shared-store source/width syntax with explicit32-bit stack/near-CALL requirements, opaque CALL barriers and memory-alias/content gaps. No actual parameter/handle binding, effective owner, original file IO/schema/persistence or system-family closure is admitted. All PARTIAL/OPEN gates remain unchanged.

Highest NEXT R39: exact mask and bounded symbolic stack-token correspondence if justified, then native parent ReadFile-context buffer/length candidates. Keep unknown API/return/frame/alias effects separate and avoid generic ownership exhaustion. Stage A restoration before joint future-engine/game review remains binding.


## 2026-10-14 queue supersession (R39 accepted)

R39 independently accepts mask/shift, conditional slot/register-symbol and native read-caller syntax with explicit bounded-prefix/stack assumptions. Actual values, ABI/frame/owner/alias effects and native save payload/persistence stay OPEN. The immediate1/local byte address/0x1A compare supports an end-check hypothesis only; no text/EOF/CRT or128-byte schema FACT admitted. All system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R40: native read-context entry stack/frame/parameter and post-call branch/address provenance, distinguish the candidate probe branch, then return to savedata-specific filename/buffer/length recovery. Avoid generic ownership exhaustion. Stage A restoration before joint future-engine/game review remains binding.


## 2026-10-14 queue supersession (R40 accepted)

R40 independently accepts bounded read-prolog/frame-slot geometry, API/PUSH syntax, equal address spellings and local flag-source candidates. Original contents, ABI/alias/owner/preservation, actual end-check/text/EOF role and native savedata payload/schema/persistence remain OPEN. All system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R41: return to savedata-specific original filename PUSH/CALL sites0x40064->0x40069,0x400e4->0x400e9,0x40115->0x4011a,0x402a0->0x402a5, all direct targets0x487ba from accepted R4–R7 evidence. Revalidate their exact immediate address0x63634 and physical pre-CALL suffix, then recover bounded caller continuation buffer/count/size operands and downstream direct CALL identities with coherent original boundary/entry support. These are independent conditional caller contexts; do not assume the0x487ba return or register/frame preservation. Seek savedata-specific payload read/write candidates, keeping generic open/end-check paths separate. No global/table/allocator ownership exhaustion; no literal128 schema promotion. All system-family PARTIAL/OPEN states and Stage A restoration before joint future-engine/game review remain binding.


## 2026-10-14 queue supersession (R41 accepted)

FACT (original bounded static): four exact savedata filename PUSH/CALL prefixes and their PE-entrypoint CFG boundary support reverified. Separate continuation graphs discover repeated target0x48bbc with four physical PUSH candidates and target0x48660 with literal4000/local address candidates. Open CALLs remain opaque; branch joins retain alternate source candidates. No parameter/handle/buffer/length/schema/persistence or actual runtime execution admitted. HYPOTHESIS: savedata-specific payload write/read wrappers; target bodies and native API links remain for R42.

Highest NEXT R42: inspect savedata-specific direct targets0x48bbc (CALL0x40090/0x402c9) and0x48660 (CALL0x40145) as independent original CALL-supported wrapper candidates. Revalidate their entrygraph/decoder boundaries, bounded branch/memory/PUSH sources and any structurally supported downstream CALL0x48c5e->0x4c5b4 / CALL0x486f0->0x4a8dc already known from native WriteFile/ReadFile contexts. Audit the four physical input slots and literal4000 separately from true ABI roles, actual count/product/buffer contents or fixed128-byte schema. Keep opaque open/API results, ESP/frame/return/alias ownership gaps and the0x400e4 conditional branch/alternate reopen distinct. Avoid generic CRT/allocator exhaustion. Native savedata payload/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 queue supersession (R42 accepted)

FACT (bounded original static): savedata-specific wrappers0x48bbc/0x48660 have coherent direct CFG support and conditional paths to native IO contexts via0x48c5e->0x4c5b4 /0x486f0->0x4a8dc. Four whole stack slots, two IMUL operands and three-slot native-call suffix syntax independently requalified. Opaque CALLs/loop joins block actual frame/owner/value binding; one write-definition shape0x48c93 remains outside the12-row sampler. HYPOTHESIS only: fwrite/fread roles and descriptor-like field. No actual IO/schema/persistence or historical system-family closure.

Highest NEXT R43: qualify early conditional caller-slot/token provenance and exact EDI multiplication source chain0x48bc3->0x48bc6 /0x48667->0x4866a, without evaluating original count/products or promoting literal4000 to an actual API byte count. Recover omitted write input definition0x48c93 and distinguish loop-carried/reentrant CALL barriers. Trace the three physical native-context input slots, especially [ESI+16] versus wrapper [EBP+20] source, and native callee buffer/count slot geometry only where bounded prefix evidence permits. Keep true FILE/CRT/descriptor/handle/alias ownership and return effects OPEN; no generic allocator/CRT exhaustion. Native savedata framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 queue supersession (R43 accepted)

FACT (original bounded static): the two IMUL instructions have unique early EDI-load sources; bounded prefix/slot audits preserve conditional operand symbols and explicitly record two mutable+8 frame slots. The missing write shape is DEC EBX0x48c93;13/10 native definition shapes are now fully sampled. Loop-region and opaque-CALL alternatives remain distinct from actual input values/effects. Native object/count/buffer/schema/persistence remain OPEN.

Highest NEXT R44: qualify the three physical native-context input slots against independent callee-entry frame/read geometry at0x4c5b4 (CALL0x48c5e) and0x4a8dc (CALL0x486f0), under explicit32-bit stack/near-CALL and bounded alias-prefix conditions. Recover the source/update meaning of mutable wrapper[EBP+8] stores0x48bd2/0x48678 and retain their temporal relationship to initial read0x48bca/0x4866e and later native pushes. Do not assume an entry symbol survives opaque calls, a literal1*4000 is an actual IO byte count, or[ESI+16] is a proven owner/handle. Keep generic end-check caller0x4edb0 distinct from savedata wrapper0x486f0 even though both target0x4a8dc. Native framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN; no generic allocator/CRT exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 queue supersession (R44 accepted)

FACT (bounded original static): native input slot geometry, literal ESP adjustment operands, delayed write buffer-shaped read with opaque CALL barrier, read count-slot DEC-before-PUSH overlap and two different wrapper slot-rewrite source chains independently recovered. Read wrapper EBX->native EDI has only a conditional prefix register-symbol candidate. Third write slot/frame preservation and actual count/descriptor/buffer values remain OPEN; no original IO/schema/persistence accepted.

Highest NEXT R45: qualify original read count-slot DEC0x4a93b->PUSH0x4a959 and its reaching predicate/branch/input sources before native ReadFile0x4a960, keeping requested count, modified candidate count and actual transferred bytes separate. Revalidate that ReadFile import/PUSH identity and recover buffer/descriptor input candidates without actual values. Bound delayed write[EBP+12]0x4c623 behind original CALL0x4c60d: identify that direct/import call syntax if useful, retain frame-preservation unknowns and then inspect physical native WriteFile0x4c68c inputs. Do not pursue generic allocator/CRT owner exhaustion or force the missing write slot closed. Original savedata framing/checksum/migration/schema/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 queue supersession (R45 accepted)

FACT (original bounded static): the DEC has a bounded root-to-PUSH bypass; five ZF-source candidates and both first native API imports/five-slot suffixes independently recovered. Read buffer sources include copy and+1 address forms; write uses a local-frame address candidate. Delayed write CALL targets previously accepted helper0x4c761, but its actual effects and post-CALL frame preservation remain unknown. No actual requested/transferred count, file/handle/buffer/schema/persistence proof.

Highest NEXT R46: relate native read DEC0x4a93b, MOV ECX,EDI0x4a926 / LEA ECX,[EDI+1]0x4a942 and any intervening byte-store candidates to the bypass branches0x4a932/0x4a939 and first ReadFile0x4a960, using bounded path/input evidence without original byte/count evaluation. Recover the conditional count/buffer adjustment pairing, not a fictional unconditional decrement or text/pending-byte role. For native write, correlate CALL0x4c60d->0x4c761 caller suffix with the separately accepted R37 helper entry/SetFilePointer syntax only where slot evidence permits; retain opaque callee/seek/frame/alias effects. Keep generic end-check caller0x4edb0 and savedata wrapper0x486f0 distinct. Original savedata framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN; no generic allocator/CRT owner exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 queue supersession (R46 accepted)

FACT (bounded original static): optional count decrement, byte store and buffer+1 appear together on first-ReadFile structural paths or are jointly bypassed. The two bypass branch arms and shared local EDI source independently reproduced. Reused write helper entry matches only conditional caller slot0; later SetFilePointer stack reads remain behind an opaque CALL and unbound. No runtime byte/count/text/seek/frame/owner/schema/persistence FACT admitted.

Highest NEXT R47: qualify the one-byte source MOV AL,[EAX+5]0x4a934 and later MOV byte[EAX+ESI+5],10 at0x4a94c using bounded source/partial-register geometry; retain distinct EAX-before-load and EAX-after-reload0x4a940, no displacement-only alias or pending-byte/text-mode FACT. Relate local marker MOV dword[EBP-8],1 at0x4a945 and its earlier initialization to the first ReadFile0x4a960 continuation and local[EBP-12] result candidates, then bound count/return handoff toward the savedata read wrapper. Requested count, prefix adjustment and transferred count remain separate; do not execute or evaluate originals, infer successful IO/ABI/frame preservation, or pursue generic CRT/allocator ownership exhaustion. Native savedata framing/checksum/migration/schema/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R47 accepted)

FACT (original bounded static): the byte load affects only AL and reaches the byte store; later reset-shaped+5 store uses a separate EAX reload. Native local initialization/marker/result-addition and wrapper zero/-1/remaining-slot/buffer-advance shapes independently recovered. Cross-call EBP/EAX sources remain UNKNOWN_CALL, preventing actual alias, transferred-count, total-return or savedata schema/persistence promotion.

Highest NEXT R48: recover bounded native count/return exits around MOV EDX,[EBP-12]0x4a9a6 -> ADD[EBP-8],EDX0x4a9a9 and MOV EAX,[EBP-8]0x4aab4, with exact register sources, branch routes, memory-write/opaque-call barriers and no original arithmetic or frame-preservation assumption. Connect only the conditional native return syntax to savedata wrapper TEST0x486f8/CMP-1 at0x486fc, SUB[EBP+8],EAX0x48701 and ADD EBX,EAX0x48704; qualify loop/exit or element-count division candidates only where bounded evidence permits. Requested input product, native transferred-count-shaped result, prefix adjustment and wrapper element/remaining count must stay distinct. Do not infer actual byte totals/text/EOF/CRT/ABI/owner/schema/persistence or pursue generic allocator ownership exhaustion. Original server authority/cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R48 accepted)

FACT (bounded original static): local count-load/add syntax reaches the local return-load region, whose nearest write candidates also include a distinct EDI overwrite. Native and wrapper RET EAX alternatives are enumerated; wrapper remaining-slot/buffer-advance paths loop structurally to the native CALL. Both distinct DIV input sources and EDX:EAX operand geometry are qualified. Actual byte/count/alias/frame/ABI/quotient/return/schema/persistence remain OPEN.

Highest NEXT R49: qualify the native local overwrite MOV[EBP-8],EDI0x4aab1 using exact EDI definitions and bounded predecessor/branch/memory barriers; distinguish it from ADD[EBP-8],EDX0x4a9a9 and other native return-source alternatives without evaluating byte conversion/counts. For the savedata wrapper, recover temporal DIV0x486e4 versus DIV0x48743 numerator/divisor provenance, especially mutable[EBP+20] and store0x4871d, initial product versus remaining-slot[EBP+8], and visible MOV EAX,EDI0x4873c->SUB0x48740. Do not infer permanent ABI roles from frame offsets, merge the two division operations or promote original quotient/return/transferred byte values. Keep unknown CALL/frame/alias effects explicit; native savedata schema/framing/checksum/migration/persistence, server authority and cross-version equivalence remain OPEN. No generic allocator/CRT ownership exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R49 accepted)

FACT (bounded original static): native EDI overwrite is sourced by a final SUB whose inputs retain INC and opaque-CALL alternatives. A TEST/JE branch can bypass that overwrite. The same wrapper[EBP+20] slot is read then overwritten from two field-load sites or literal4096 before comparison/division candidates; final numerator cannot be bound to the initial product across opaque calls. Actual byte/count/ABI/alias/division/schema/persistence remain OPEN. Helper scope is bounded; next work returns to savedata-specific caller consumers.

Highest NEXT R50: return to original savedata-specific CALL0x40145->0x48660. Requalify its exact caller/decoder/entrygraph support and physical buffer/product inputs against accepted R41/R42 evidence, then inspect a bounded post-wrapper continuation, returned-value predicates and first buffer consumers for application-level field/record/framing checks. Keep opaque wrapper/open results and caller register/frame/alias barriers explicit; do not convert literal4000, a multiplication, a return candidate or historical128-byte observation into a proven read size/schema. Keep the separate write callers0x40090/0x402c9 as distinct contexts if needed for a later read/write correspondence. Native conversion/ABI/owner gaps from R49 remain documented OPEN and off the critical path unless needed for a specific savedata consumer. No generic allocator/CRT ownership exhaustion. Savedata payload/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R50 accepted)

FACT (bounded original static): savedata-specific read caller and processing entry requalified. Postprocessor comparisons57/127, register literals4/5, word checks and byte stores at global base/base+57 are recorded with exact widths. Actual length/tag/migration/alias remain unknown. Processor36 memory/control shapes are sampled to32; the omitted4 are explicit next work. Stage A gates unchanged.

Highest NEXT R51: qualify savedata application CMP EAX,57 at0x40195 and CMP EAX,127 at0x401c9 using exact stack-load/processor-output sources and bounded flag/control routes; separately qualify word comparisons at0x4019f/0x401e4, register literal4/5 definitions, byte stores at0x401a8/0x401af and their relation to global RVA0x13fbdac. Revisit processor0x47160 with all36 memory/control shapes, including the4 excluded by the R50 sample, and bound its input/output/algorithm structure. Do not assume decoded lengths, tag versions, migration, endianness, buffer alias or executed paths from these literals. Keep read/write callers distinct and opaque CALL/frame barriers explicit. Savedata schema/framing/checksum/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration precedes joint future-engine/game review; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R51 accepted)

FACT (bounded original static): processor115-node full instruction inventory and all36 memory/control shapes recovered. Normal RET0x47268 yields conditional net near-CALL ESP change0; the caller ECX/pre-CALL+32 coordinate matches post-CALL load[ESP+32] under that bounded model. All seven signed divisions and final byte NOT/subtraction syntax recorded. Source dependencies remain bounded:39 definitions,19 retained,11 pending expansion; schema/algorithm/value/alias/persistence remain OPEN.

Highest NEXT R52: qualify the seven processor IDIV sites0x47170/0x4719f/0x471b7/0x471d6/0x471ee/0x4721e/0x4722a with exact CDQ EAX-preservation/EDX-sign-extension syntax and bounded register-source expansion, keeping signed dividend, divisor, quotient and remainder distinct. Resolve the11 source-expansion pending definitions and19-of39 source-definition sample limitation using focused groups rather than suppressing caps. Bind only conditional caller ECX/pre-CALL+32 -> processor entry+20 -> ESI store0x4717c and post-CALL load0x4018e, with stack-slot mutation and memory-alias barriers explicit; qualify LEA EAX-1 -> ECX/store syntax and application57/127 checks without evaluating original bytes. Recover subtractive/NOT byte operations and loop predicates as syntax before assigning a historical algorithm/version/schema meaning. Native schema/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN; Stage A restoration precedes joint future-engine/game design. System-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R52 accepted)

FACT (conditional architecture/source metadata):10 CDQ observations preserved with a separate EAX-preservation/EDX-sign-extension overlay; all7 signed-division source groups and11 legacy-pending register groups close without query caps. All39 legacy definition shapes recovered. Forward/reverse algorithms agree on60 queries; output-store sources, five explicit alias-write barriers and10 processor predicates recorded. Actual memory/arithmetic results, algorithm/schema/tag/migration/persistence remain OPEN.

Highest NEXT R53: reconstruct a conditional savedata-specific transform specification from the complete pinned R51/R52 numeric metadata. Follow the caller literal0 seed/mode physical slot only under explicit entry/frame/non-alias/normal-return conditions. Qualify the source-byte selection, possible omitted-byte/output-index shift, signed remainder and low-byte IMUL/subtraction paths, final NOT predicates and output-length-shaped LEA/count-minus-one store; connect only conditional results to the application57/127 and word4/5 checks. Prefer bounded symbolic relations and invented-input counterexamples before any algorithm label or engine-neutral reference model is admitted. Keep generic nonzero-seed branches separate, retain divide-error/invalid-count/overflow and memory-alias preconditions, and do not evaluate original save bytes or claim a proven payload schema/version/migration/persistence. Original server authority/cross-version equivalence remain OPEN. Stage A restoration precedes joint future-engine/game design; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession (R53 accepted)

FACT (conditional reference only): zero-seed key selection/removal, shifted output-index subtraction and final NOT relation reconstructed from pinned metadata and verified with1029 invented fixtures plus10 generic-seed numerical fixtures. Both models agree;112 observed instructions exercised and3 negative-index repairs explicitly excluded by the model domain. Actual input/output bytes, schema/tag/migration/writer/persistence remain OPEN; invented inverse is not historical writer evidence.

Highest NEXT R54: qualify the savedata application read/write correspondence around conditional57/word4 normalization stores0x401a8/0x401af and direct CALL0x401b6->0x40020. Audit the write-side prefix0x40020 before the already accepted filename-push0x40064/write CALL0x40090, recover its processing-call identity, physical slots, frame/count/buffer sources and bounded entrygraph/control support, then compare any historical write transform with R53 only under explicit preconditions. The invented inverse fixture generator is not historical writer evidence. Existing R51/R52 instruction shapes are sufficient for the read processor but do not contain this write prefix: verify existing metadata first and retrieve authenticated originals only for that identified missing scope. Keep word4/5, lengths57/127, new byte at+57 and possible writer128-byte framing as separate candidates until linked. Do not evaluate original save contents or promote actual ABI/alias, field schema/checksum/migration/persistence, original server authority or cross-version equivalence. Stage A restoration precedes joint future-engine/game design; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R54 writer correspondence gate update

Original source Action38724589059/job116387179386 SUCCESS at HEAD660a051f9b58ef596fb2fdf8f27bfc9fd321a7a0, branch agent/tw10-savedata-r54-writer-prefix-20261015. Archive/disc/runtime/save identities authenticated transiently; exact accepted R51 report SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052 rederived and validated before extension. Derived-only artifact11967805220 ZIP SHA256a857094d202033ea378406fc3c5dae5580c984416181a80f497a6540466ffa5c; raw JSON132329 bytes SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387. Independent Action38725044477/job116388679063 SUCCESS at HEADd064e83ae3e14f4b6fede56b0f52f7ba2e7c8215 authenticates immutable source/run/head/branch/artifact, exact raw size/digest, canonical byte equality, strict inventories and separately regenerated pure writer contract. Legacy R38/R44/R50 and R51 stack algorithms agree at all201 instruction sites. Source664 tests PASS; independent688 tests PASS (656 inherited plus32 R54 controls). Local20 pure metadata tests and syntax/custody checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original executable/save payload never executed/evaluated or published; transient original media purged.

Historical writer prefix and complete129-row transform inventory recovered. Six physical inputs and conditional stack coordinates qualified. Arithmetic inverse, original values/native persistence/schema remain OPEN. No subsystem family promotion; Stage A continues.

Highest NEXT R55: derive a conditional historical writer0x47010 reference specification from the exact R54 complete129-row numeric inventory and R51/R52 read metadata. Recover the byte accumulator/key relation before the in-place NOT pass, seed-dependent insertion/index arithmetic, count+1/capacity branches, signed division and byte ADD/IMUL semantics. Qualify the zero-seed127->128 candidate against the read128->127 relation on invented inputs only, with a separately authored formula and bounded numerical instruction-shape model. Preserve writer input mutation, key derived from input rather than arbitrary R53 inverse keys, partial-register rules, aliased/out-of-capacity/error preconditions, and generic seed paths. No original payload evaluation or binary execution. Existing metadata is now sufficient for this arithmetic task; do not retrieve the original archive again without a specific missing-evidence reason. Stack helper0x49160 actual frame effect, REP direction/segments/count validity, opaque open/write/close, native output-length-to-write binding, word4/5 semantics, normalization/migration/schema/checksum/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint new-game design; system-family PARTIAL/OPEN gates unchanged.
