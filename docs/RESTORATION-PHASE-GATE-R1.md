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


## 2026-10-15 — R55 conditional writer/read gate update

R55 source Action38728999042/job116401820264 SUCCESS at HEAD230726474ed0ed9dae228f97da389401b7554b4f, branch agent/tw10-savedata-r55-writer-inverse-20261015. Authenticates immutable R51/R52/R53/R54 source runs/artifacts and exact canonical numeric bytes before extension. R54 source132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R53 spec104275-byte SHA25626bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5 pinned. R55 artifact11969477120 tw10-r55-conditional-writer-read-spec ZIP SHA256569d762983ff27fb19078b825f31d444ec6cee5152efc0fccd78613aa1b3933a; raw spec103165 bytes SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863. Independent Action38729256210/job116402678124 SUCCESS at HEAD05535ed2621690954c4cb7c6264a80f9065f5bc5 authenticates all five immutable source/run/head/branch/artifact chains, exact sizes/digests, prior canonical bytes, strict R54 inventories/independent201-site stack replay, exact R53 regeneration and exact R55 specification reproduction/equality. Source and independent734 tests PASS (688 inherited plus46 R55 controls). Local46 pure-model tests, syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/disc/executable or save payload downloaded or evaluated; only numeric metadata and invented arrays used.

Conditional writer byte-sum key, input mutation, capacity fallback and zero-seed read roundtrip accepted on invented arrays. Actual native persistence, schema and application frame/REP effects remain OPEN. No system-family promotion or new-game design decision.

Highest NEXT R56: bind conditional R55 writer output/count to the savedata application write request0x40090 using the exact R54 numeric inventory. Qualify the specific frame helper CALL0x40025->0x49160 (EAX literal4132), including its page-probe reads, ESP rewrite, saved ECX/return-address relocation and conditional near-return geometry on invented storage only. Then replay caller REP/MOVS copy127 candidate, six transform pushes, post-transform/open ADD ESP,32, load0x40080, write-buffer LEA0x40086, write physical suffix and post-write count comparison0x4009c. Keep direction flag/segments/address validity and opaque open/write/close preservation/alias effects explicit. Separate conditional output128/write-request correspondence from actual native write/flush/close/persistence success. Prefer pinned metadata; retrieve originals only for an identified missing scope. Do not expand generic CRT ownership work, evaluate original payloads, or promote field schema/tag/version/migration/checksum/server authority/cross-version equivalence. Stage A precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R56 conditional application write-request gate

R56 source Action38730761697/job116407664800 SUCCESS at HEAD453ff20ca9f30ca9f05b1b42551508c7053f9cb5, branch agent/tw10-savedata-r56-application-frame-20261015. Authenticates immutable R51/R52/R53/R54/R55 metadata custody and exact bytes; R54 raw132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R55 spec103165-byte SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863 pinned before extension. R56 artifact11969389801 tw10-r56-conditional-application-frame-spec ZIP SHA25695938cabdcd015aa3e273cc541bd38e1fbd7f8cdf91716b895c7b132abf2e028; canonical raw67492 bytes SHA256db5628403b366e706e212bd7627f40861097d78bfb3f3acb0d95598bce70981c. Independent Action38731138905/job116408925725 SUCCESS at HEAD601b5f63bf47c0c1d799ed9fd7b94a3d8d07af94 authenticates all six immutable source/run/head/branch/artifact chains, strict R54 inventory/stack replay, exact R55 regeneration and exact R56 reproduction/equality; a separate all-path caller ESP algebra agrees at55 sites and preserves unknown downstream states without opaque-call stack premises. Source780 tests PASS; independent788 tests PASS (734 inherited plus54 R56 controls). Local54 pure metadata/model/algebra tests plus syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/executable/save payload retrieved, evaluated, executed or published; only numeric metadata and generated invented storage/stubs used.

Conditional helper stack geometry and writer-buffer/count-to-write-request correspondence accepted on invented storage. Actual opaque-call preservation, returned-count/error meaning and native persistence remain OPEN. No system-family promotion or new-game design decision.

Highest NEXT R57: qualify actual savedata write-wrapper return/count/error syntax at CALL0x40090->0x48bbc and close-wrapper CALL0x400ac->0x4856c, separating the caller's unsigned JAE/literal1 from native write/close success. R42 retains a complete106-node/119-edge write-wrapper graph and106 numeric stack effects but only5 early operand shapes and1 frame definition; this is insufficient to reconstruct all returned EAX/count/control paths. Audit all existing R42-R49 metadata first, then retrieve authenticated originals only for missing complete write-wrapper/close-wrapper numeric inventories. Requalify exact prior original metadata, recover bounded complete instruction/branch/call/return shapes and preserve opaque nested calls, alias/frame and actual return/error-value gaps. Prioritize savedata-specific return/cleanup obligations, not generic CRT ownership exhaustion. Do not evaluate original payloads or promote a successful actual128-byte native write/close/flush, field schema/checksum/migration/persistence, original server authority or cross-version equivalence. Stage A restoration precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R57 bounded write/close return gate update

R57 original source Action38739896846/job116438533408 SUCCESS at HEAD1bb5924185c21a73d6e196f9764871b5b3593c08, branch agent/tw10-savedata-r57-write-close-returns-20261015. Original archive/disc/runtime/save identities authenticated transiently; accepted R54 report132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 rederived and strictly validated before extension. R42 write graph/effects and retained operand shapes match exactly. Derived-only artifact11976200967 tw10-r57-original-write-close-derived ZIP SHA256425595389a34ee483a855bd8669f404dd2c9b65695f54fddeb95b2510da4a042; raw203899 bytes SHA2563e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6. Independent Action38740708599/job116441358622 SUCCESS at HEAD6254425e4e1f8bc03515022c0a500faf97255359 authenticates all seven immutable R51-R57 source/run/head/branch/artifact chains, sizes/digests, exact canonical bytes, prior R56 reproduction, strict R57 report, independent reverse return sources and separately regenerated contract. Contract3654 bytes SHA2569c35c0d934b7d98503c62c210eb9f216b158ae727dadda7d8323545930cd17d7. Source796 tests PASS; independent826 tests PASS (788 inherited plus38 R57 controls). Local28 pure metadata/contract/reverse controls, syntax, ZIP/raw equality and historical-prefix checks PASS;10 additional primary-guard controls run remotely with capstone/pefile, which remain unavailable locally. Original client/save payload never executed/evaluated or published; transient original media purged.

Complete write/close inventories and20 independently audited return-source queries accepted. Full-count-shaped return has a structural memory-copy path without direct native write; actual persistence/close/flush remains OPEN. No subsystem-family promotion or new-game design decision.

Highest NEXT R58: qualify the shared write/close helper0x4a657 (write CALL0x48c38; close CALL0x48586) and close-path helper0x4a53e (CALL0x48596), focusing on return predicates, deferred/native output and close-result propagation needed by R57. Audit existing metadata first: mere rows in an overlapping address window are not a function inventory and no row at either target root was found in the R57 preflight. Retrieve authenticated originals only for missing bounded root/callee/entrygraph evidence. Keep other cleanup helpers0x4a5f1/0x4853d opaque unless their effects are required for a specific live value; avoid generic CRT/allocator ownership exhaustion. Separate conditional full-count/buffer-copy returns from actual native output, shared-helper result and close/flush success. Preserve frame/EDI/ESI/EBP/alias/callee barriers, no original payload evaluation or client execution. Actual persisted bytes, record/tag/version/checksum/migration/schema, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 queue supersession — R64 original-static native WriteFile TEST/Jcc accepted

R63 and R64 original-derived metadata have both been permanently archived in Git with source-run, ZIP and raw JSON digests. Two original-static WriteFile postcall continuations are confirmed as TEST EAX,EAX followed by JE, with conditional physical fourth argument/output-count position candidates but **without native execution evidence**. R64's bounded window contains only one of the first JE's candidate successors; preserve the other as OPEN. Stage A file-IO/persistence family remains OPEN; all other recovery-family PARTIAL/OPEN gates remain unchanged.

Highest NEXT R65: resolve precise local/out-of-window control predecessors and TEST/EFLAGS/JE scope, then qualify memory output-pointer and cross-function frame/ABI barriers separately. Actual native BOOL, transferred bytes, flush/close, persisted records, schema/version/checksum/migration and original server authority cannot be promoted from these static spellings. Do not initiate new engine or game-redesign Stage B.


## 2026-10-16 — R65/R66 retained control/count scope accepted; R67 tail operands next

Original-static cross-window branch/flag/count-pointer geometry and conditional count-consumer syntax are accepted within their explicit metadata scope. R65 branch/main38819955397/38820017473 and R66 branch/main38820370818/38820484845 SUCCESS. Permanent reports and exact34-source census remain in Git, with original binaries and save payload absent. Eleven native-tail operands remain missing; LEAVE/RET already retained.

Highest NEXT R67: narrowly obtain11 missing0x4c731..0x4c75e operands and required CFG edges after fresh source requalification; preserve all ABI/frame/memory/count/persistence boundaries. All Stage A families PARTIAL/OPEN; Stage B remains gated.


## 2026-10-16 — R67 native-tail operand closure / R68 explicit early-return gap

Eleven missing native-tail operand rows are recovered under authenticated original-static custody, with known LEAVE/RET requalified. Independent forward/reverse EAX-source algorithms preserve both decoded subtraction/all-ones candidates and the unqualified early0x4c5fe barrier. Canonical derived reports and source-custody receipt survive artifact expiry; no original program/API or savedata payload executed.

Highest NEXT R69: after refreshed corpus/custody, recover only the missing early-return instruction and necessary incoming context. Actual native returns/counts, call/frame/register/memory aliases, feasible paths, flush/close/disk persistence and original format/schema/checksum/migration/server authority remain OPEN. Stage A subsystem family statuses PARTIAL/OPEN; Stage B gated.


## 2026-10-16 — TW1.0 R69/R70 early-zero and three conditional return definitions

FACT (authenticated original-static syntax): R69 retains38 early-return neighborhood rows on the exact139-node/156-edge graph after reproducing R67/R63. The missing0x4c5fe instruction is XOR EAX,EAX, entered from early JNE fallthrough0x4c5fc and late byte26 JE0x4c72b. A133-report preflight bounds the prior absence claim. R70's independent forward/reverse algorithms agree on zero, SUB EAX,frame[-16], and OR EAX,0xffffffff direct return definitions;103 of139 nodes decoded. Conditional uint32 shapes agree across1011 invented-only arithmetic comparisons. Actual branches, inputs, count/ABI/frame/aliases, historical marker/error meanings and persistence are not established.

Source Action38851405164/job116813227130 and artifact12025561162 have independently verified ZIP/raw/canonical Git custody. R69 raw25466 bytes/SHA25626ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe/blobd5d4924803dc28de8be00f712eecd11cf9003c66; R70 raw2406 bytes/SHA256c59858b8d35be04c8f37efec8c297d346fd57d6df2496973c75424143881d621/blobcd2782a57c7c131bd938ca5fe29406a486cc6823. Permanent reports/custody/acceptance receipt remain in research/recovered. No proprietary code/assets/save payload archived or executed. Full local124 tests pass; exact remote acceptance anchors are recorded separately in STONEAGE-TW10-SAVEDATA-R69-R70-ACCEPTANCE-R1.json.

OPEN: actual native returns/counts, temporal frame/memory identity, feasible paths, flush/close/persistence, original record schema/checksum/migration/server authority. Stage A families PARTIAL/OPEN; Stage B gated. Highest NEXT R71: retained-first adjustment update/count-to-return relation, especially R44 INC frame[-16]0x4c653 and known count accumulation; no redundant original acquisition before proven gap.


## 2026-10-16 — TW1.0 R71 adjustment predicate and R72 conditional count-unit relation

FACT (authenticated original-static syntax): a138-report retained-first census reuses R44/R45 evidence and identifies11 missing rows in a25-node adjustment-loop focus/29-node one-hop neighborhood. R71 exactly rederives R69/R67/R63 and preserves the139/156 graph. CMP CL,10/JNE qualifies the equality-only frame[-16] increment and extra literal13 store before the shared original-byte store. Input bound uses unsigned JAE; post-store output bound uses signed JL after comparison1024. Decoded graph coverage is128/139, with11 mode/direct-count operand nodes still absent in the registered representations.

Source Action38853018146/original job116818258696 and artifact12026131224 have independent ZIP/raw/permanent-report custody: ZIP3148 bytes/SHA256036e7aa7778d4f8fa778847671ae3dbec57807c26abfa12cecd25c9e7d03d89b; raw21525 bytes/SHA256746c7e64a973b52ca5cf3412342eb68725fcf15dcb5ad4a1e71a8e638ae90af5/blobf2a946ffc93c6a32210f2ebaa9dc9191833aac37. R71 independent branch38853444099 and R72 branch38853447606 SUCCESS; accepted code mainf8138e759c4665427f9680ab83d1acf567e19fd8 has successful R71/R72/R69/R70 Actions. R72 report5600 bytes/SHA256aa21627e0018f2a7d9c01aaa36b6f70f38456f938de31713fee893402070265a/blob94656b8f6c2f830743a6257c1a8abf7aedb00c22. Full local156 tests pass; separate remote suite counts remain41 and110.

R72 invented-only3124 trace-threshold comparisons plus four long cases qualify conditional complete-transfer output-minus-insertions identity. Post-store threshold can produce1025 output units. Partial-write examples disprove a general logical-prefix-count interpretation; no historical native behavior, overflow or memory safety conclusion is claimed. Actual count/BOOL, temporal frame/ABI/aliases, feasible paths, persisted records/schema/checksum/migration/server authority remain OPEN. No original code/assets/payload archived or executed. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R73: refresh custody, reuse exact142-report/128-node next-gap census in STONEAGE-TW10-SAVEDATA-R73-PREFLIGHT.json, and narrowly resolve the remaining mode/direct-count predicate context. Permanent receipt: STONEAGE-TW10-SAVEDATA-R71-R72-ACCEPTANCE-R1.json; spec: docs/specs/STONEAGE-TW10-R71-R72-ADJUSTMENT-COUNTS.md.


## 2026-10-16 — TW1.0 R73/R74 complete bounded operand census and mode/call barriers

FACT (authenticated original-static syntax): refreshed144-report census retains the11 gaps; R73 recovers17 one-hop rows after exact R71/R69/R67/R63 reproduction. Seven-source R74 union now decodes139/139 bounded graph nodes/156 edges. This closes the operand inventory within that intraprocedural candidate, not callees/runtime. Mask32 skips/enters opaque direct helper0x4c761; later mask128 chooses direct-native-prefix versus the qualified byte-expansion prefix. Literal5 equality writes9 and EAX-shaped5 to globals, while inequality invokes opaque0x4c953 before all-ones return. Historical flag/error meanings remain unproven.

Source Action38885251848/job116921375490 and derived-only artifact12039068385 have independent ZIP/raw/permanent custody: ZIP2915 bytes/SHA2567005037bf04b1ff034b12996dd4fae4dd1c4d37750c7d0bfe808ed01a93b974e; raw14043 bytes/SHA2565cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d/blob2a90bf654a723da53f7d6a26008ca660cb89b290. R74 report7076 bytes/SHA256cc7b48b139f64a502eb26bc45fbd5754b1bba202484447b625e5f34a28c32c25/bloba29a6a9b38a86d2f33d9e327d73c9d08cc3fb5ad. Independent R73/R74 branch Actions38886167422/38886173283 and six relevant code main Actions SUCCESS atfb7cb654c1c702cb2400bcf224f60fdcff52e18a. Local192 savedata tests PASS; remote suites44/146 are separate.

Forward/reverse reaching-syntax algorithms agree on eight register queries. All six calls remain register/memory barriers; early mode snapshots and table/frame state are not equated across the optional call. Invented65536 snapshot pairs qualify four conditional predicate combinations, without actual values/path/ABI/count/persistence admission. No original program/API or payload executed or archived. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R75: reuse R46's already retained0x4c761 entry/51-node55-edge helper graph/three decoded rows/native seek context and R37 boundary;48 helper rows lack registered operands, but only material missing effects should be acquired. R30 already records0x4c953 boundary; its decoded entry remains absent in the registered scope. Exact148-source helper preflight blob73d192eec12cd31e67b5b0fc298ab4c3bdb53189 and STONEAGE-TW10-SAVEDATA-R73-R74-ACCEPTANCE-R1.json preserve next-step evidence. Native BOOL/count/position, frame/alias/preservation, actual close/flush/persistence, original schema/checksum/migration/server authority remain OPEN. Legacy queued attempt37642417333 stays queued; separately accepted successor37643425686 and permanent report are requalified in docs/continuity/STONEAGE-STALE-QUEUED-RUN-AUDIT-20261016.json, without claiming the old attempt succeeded.


## 2026-10-16 — TW1.0 R75 helper effects and R76 conditional seek contracts

FACT (original-static): refreshed150-source census reuses R46/R37's retained helper entry,51/55 graph and three decoded operands;48 missing rows are recovered only to inventory all local caller-visible register/stack/memory/return effects. No descendant call graph or original savedata payload is opened. Runtime/R73 and exact R46/R37 helper surfaces are requalified. Source Action38888448211/job116931879732, artifact12040258731 ZIP2743 bytes/SHA2564cd9097e869802b8bd107f737ac68183c78f42f7a4b9b75a6a639adc3d6e069f; raw25435 bytes/SHA256bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85/blob757c22945d7e18263b154e88f52376d0ab58d42c. Independent download/canonical custody survives artifact expiry.

R76's seven structural paths have conditional EBX/ESI/EDI token restoration and balanced near-return stack under declared call-cleanup and nonaliasing premises; adverse cleanup/clobber controls preserve those limits. EBP, table pointers and intermediate EBX remain opaque across calls. Caller/helper physical argument tokens conditionally reconcile to an opaque handle,0,0,2 at imported SetFilePointer; modern Microsoft API/ABI references support an EOF-request interpretation, without original execution/position/success proof. Local AND253 clears bit2 while preserving masks32/128 on256 invented bytes; whole-table snapshot identity is unproven.

Permanent R76 report7662 bytes/SHA2562a57125d32c3889def89c90d2e99192d94a25bd30b9677d5bfd7b0fd10fa3ead/blob2cdbcb8b95649a0ce610ab93fde5edcd7ef0997b. Local226 savedata tests PASS; remote48/180 are separate. Independent R75/R76 branches38889189883/38889194294 and eight code main gates SUCCESS atcdbb41c9f9b2a25ab7aeb32fbf3eaa666c53f8e4. Receipt STONEAGE-TW10-SAVEDATA-R75-R76-ACCEPTANCE-R1.json and spec docs/specs/STONEAGE-TW10-R75-R76-SEEK-CONTRACTS.md preserve source/contract distinctions. No actual I/O/schema/server-authority admission; Stage A PARTIAL/OPEN, Stage B gated.

Highest NEXT R77: pinned154-report helper-entry census blob38cc620394f21e04ec96c14a883b0510082fca43 separates absent registered decoded entries0x4e8fb/0x4c953 from retained root/numeric references. Prioritize only0x4e8fb handle-source and material caller-visible effects, then0x4c953 where necessary. Preserve ABI/stack/nonaliasing, table/address, native handle/count/position, close/flush/persistence and original record/schema/checksum/migration boundaries.
