# Taiwan1.0 R9 nested helper, store geometry and structural loop frontier

Original mode checks full original hashes, rederives R7 and accepted R8 helper
44 states/two return states/exact unresolved call and alias sites. It analyzes
nested helper0x4918f with unchanged conservative R8 semantics, classifies the
selected store0x4b903 and builds bounded intraprocedural topology for0x4b8a4.
No arbitrary helper is summarized or skipped in the argument tracer.

Store metadata includes write width, address base/index register names and
scale, displacement's PE section/RVA/raw-backed/header-writable geometry.
Displacement in .data does not prove an indexed effective address or table/
object/field ownership. Exact effective RVA is emitted only for unsegmented,
absolute addresses with no base/index. Unknown incoming index values remain
unknown. The store is recognized from an explicit integer-write allowlist,
not unreliable operand access bits alone. No original operand listing/bytes.

The address CFG follows direct branches, stops returns/indirect jumps and
marks every CALL fallthrough as a RETURN ASSUMPTION for topology only. Limits
256 nodes/1024 RVAs. SCCs expose possible loops and conditional-branch sites;
they are not executed loops, path-condition solutions or nontermination proof.
This structural graph NEVER resumes filename/handle argument dataflow.

No ownership, runtime loop conditions, caller resumption, native IO, fixed128
format or original data publication is admitted. The branch-only original
acquisition preserves catalog/full archive/embedded hash gates and mandatory
cleanup; subsequent custody verification must use the tiny derived artifact.
