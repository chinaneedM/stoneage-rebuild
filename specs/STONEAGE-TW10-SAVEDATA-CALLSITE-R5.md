# Taiwan 1.0 savedata R5 — bounded source-string callsite and file-API audit

Status: DESIGN / awaiting original-byte gate. R4 already confirmed that all
four alternative push-immediate instructions are observable in a bounded
PE-entrypoint direct-edge graph. This is **not runtime execution**.

R5 identifies upstream structural graph conditions and downstream imported
file-API neighborhoods without assuming that any candidate executes, that
its pushed string is a valid file name argument or that data/savedata.dat
is genuinely read or written.

For exact original SHA256-pinned sa_3.exe and savedata.dat only, R5 repeats
the R4 direct graph, checks the previously accepted 31665 nodes and 35092
edges and exact four push sites, then reports for each:
- shortest **potential** PE-entrypoint graph path length;
- graph incoming edge counts split between sequential and branch;
- at most 256 reachable local decoded starts within 2048 RVAs after the
  candidate, and their first 30 direct imported file-API occurrences;
- only accepted Win32 file API names present in the existing v1.0 research
  allowlist, with exact original RVA, DLL and duplicate-free bounded totals.

R5 does **not** perform stack argument recovery, dynamic branch feasibility,
import thunk alias analysis, register/memory taint flow, native file handle
linkage, actual I/O timing, checksum inference or data-buffer ownership.
A nearby CreateFileA import is not proof the filename was supplied as
lpFileName, and ReadFile/WriteFile appearances do not establish any actual
128-byte buffer. All such claims remain explicitly false.

An original-data probe requires the fixed archive catalog MD5/SHA1, the
original disc BIN length, original exact embedded runtime/save SHA256 and
bounded 16-worker download. Original bytes must be deleted after processing;
only a JSON containing derived offsets/counts and nonadmission flags may
be uploaded. The synthetic CI runs separately and does not access archived
proprietary bytes.

NEXT after a verified original R5 report: classify candidate-specific
CreateFileA proximity and branch edges, then design a *separate* x86 stack/
handle/buffer dataflow test only for actual positive signals. No automatic
retrojection of later Wayi settings behavior or engine implementation.


## 2026-10-12 — R5 full-original static report accepted

The exact catalog-pinned archive, STONEAGE.bin and embedded original
sa_3.exe/savedata.dat pass identity gates in Actions38223087375. Immutable
original-run derived-only report ID11735491592 was independently fetched and
strictly validated in branch Actions38223391602 and main38223493392.

Four existing push start RVAs 0x40064,0x400e4,0x40115,0x402a0 have
PE-entrypoint-graph minimum path lengths 226,216,226,259. Each has one
sequential incoming edge and zero incoming explicit branch edges. Bounded
forward neighborhoods visited 34,158,73,34 graph nodes (limit <=256,
RVA span <=2048); observed zero direct recognized file-API import calls.
R4 graph count 31665 nodes/35092 edges unchanged.

This proves **only the bounded negative local API search**, not absence of
file IO, not filename-to-CreateFileA argument flow, not actual runtime code
execution and not any read/write size or storage schema. R6 must examine
cross-function/indirect wrappers and dataflow without silently promoting
inference to original fact. Acceptance receipt:
research/recovered/STONEAGE-TW10-SAVEDATA-CALLSITE-R5-ORIGINAL-ACCEPTANCE-R1.json.
