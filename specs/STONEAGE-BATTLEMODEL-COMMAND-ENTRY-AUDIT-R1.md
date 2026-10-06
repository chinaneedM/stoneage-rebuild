# BattleModel command-entry audit R1

Date: 2026-10-06. Status: CLOSED_BOUNDED_PINNED_SOURCE_AND_EXACT_DATA_ENTRY_AUDIT.

## Evidence and version boundary

FACT for the three pinned descendant source trees: `PETSKILL_Use` maps the
actor's skill slot to an ID and then a runtime array. With their default
preprocessed headers, a nonzero ILLEGAL on a PET actor returns before callback
lookup. Active IDs638/641/649/650 have nonzero ILLEGAL. The ordinary W command,
PS request where present and random-pet paths funnel through this guard; they
do not supply evidence of a bypass. Original active executable flags remain
OPEN. Bismarck's `_OPEN_E_PETSKILL` can remove this guard, but is absent from
all three default headers. Its864 native controls are counterfactual, separate
from2592 default-header original-function controls, and retain owner/battle
checks. Callback bodies are neutral trace seams; these are entry-admission
witnesses, not a re-test of the separately accepted hit/damage implementation.

FACT for pinned source: equipment J magic can use `MAGIC_AttSkill` to look up a
callback directly, bypassing `PETSKILL_Use`. `_ITEM_ATTSKILLMAGIC` is present in
gavin/iris default headers, absent in Bismarck's. The second semicolon token is
C atoi input passed directly as a callback **runtime array position**, with no ID lookup at that call site.
All three default headers enable `_PETSKILL_OPTIMUM`: the loader stores rows
at their numeric IDs, so the array may equal the ID. Legacy layout stores rows
in file order. The loader publishes last-row-ID+1 as the effective OPTIMUM
bound, rather than simply allocation maximum+1. The exact active magic file
and both explicitly tagged layouts/bounds must be checked before claiming
any configured ID638 magic path; the original active build layout stays OPEN. Equipment possession, MP and actor/gameplay prerequisites
are separate OPEN obligations even for a matching row.

FACT for pinned source: template AI150 is CHAR_MODAI. Enemy battle tactics and
wa option weights come from enemy variants separately. Both actual variants
2559/2560 retain TACTICS1, no rn extension and index2 weight0; neither can select
ID638 through the accepted common weighted normal-AI selector.

The C lexical call-site census includes definitions. Callback registrations
are separately inspected; a registered pointer is not itself a call site. It is bounded
call-site evidence, not whole-program pointer analysis or proof against opaque
scripts/NPC/build overrides. No original source/data bytes or OPTION text are
stored; reports contain derived hashes, flags, counters and identities only.

## Placement criterion review

The current pressure ledger counts positive **enemybase skill-slot placements**
and classifies callback implementation capability. Existing bounded BatFly and
Lighttakeed closures do not establish original executable membership or full
natural gameplay reachability. Keep these axes explicit: callback/placement
capability closure and actual configured command-entry reachability are separate
claims. The conditional ID638 seam and independently authored selected-AI
controls cannot be relabelled as recovered natural selection.

DESIGN for the next promotion gate: if conditional placement closure is adopted,
require an exact predicate over active whole-file hashes, template1178/1179,
ID638 index2/report-slot3, callback/OPTION identity, level/MODAI/current runtime
admission and the already accepted bounded execution/death/exit profile. Add
mutation controls and prove only those two static placements qualify. Do not
put the entire BattleModel callback into CLOSED_RUNTIME_CALLBACKS and do not
promote unreferenced IDs641/649/650. A pressure receipt must state conditional
capability separately from zero actual normal-AI selection. Any broader actor
or equipment-magic seam requires its own source/native/runtime gate first.

No promotion in this audit:2486=2461 closed+22 OPEN+3 historical UB, two
BattleModel uses OPEN. Exact-head source/data/coordinator/golden/full-region
Actions all PASS on c26dce336ba59eccc1aca82080c1982ab07ece08. The derived
writeback c2d3b5dee957060163c1465cc5aa0776e1b8d1bd adds only the audit JSON;
no code changes. This accepts the bounded audit, not a pressure promotion.

## Reproduction

- `python -m unittest tests.test_stoneage_battlemodel_command_entry_audit`
- `python -m tools.stoneage_battlemodel_command_entry_source_audit` with three
  pinned source directories (see settlement workflow).
- `python -m tools.stoneage_recovered25_battlemodel_command_entry_probe` with
  exact preservation `--data-dir` and `--setup` (see full-region workflow).

## Exact-data findings and acceptance

- Hash-verified active magic:181 parsed rows, no malformed rows, **zero literal
  BattleModel callback OPTION candidates**. Both legacy ordered and default
  OPTIMUM layouts resolve0 ID638 and0 sibling BattleModel rows. Ordered bound
 147, OPTIMUM allocation/effective bounds653. ID638 arrays are135 in legacy
  order and638 in default OPTIMUM;641/649/650 are138/144/145 versus their IDs.
  No configured equipment-magic entry is established in this active file.
- Both exact enemy variants2559/2560 have **zero positive group references
  and zero positive area rows** under loader-first group identity. Raw PETFLG1
  is recorded without inferring capture/ownership. Spawn/NPC/script overrides
  and original active executable flags remain OPEN. No universal unreachability
  claim follows from these negative configured-path results.
- Complete pressure was recomputed from all active positive slots, not copied
  from constants:2486=2461 closed+22 OPEN+3 historical UB; unresolved IDs0;
  BattleModel2 uses OPEN and0 promotions. Exact hashes must match before census.
- Local unique workflow-test union855 PASS; exact-head settlement679,
  coordinator249, golden20, region160 PASS;2592 original PETSKILL_Use guard
  controls +864 explicitly counterfactual controls.60 explicit-selected +60
  selected-AI control companions and12 identity rejects per suite, including
  concrete-stack repeats. Actual normal-AI selected cases0;826 floors.
- Receipt: `research/recovered/STONEAGE-BATTLEMODEL-COMMAND-ENTRY-ACCEPTANCE-R1.json`.
  Next: `specs/STONEAGE-BATTLEMODEL-CONDITIONAL-PLACEMENT-CLOSURE-PLAN-R1.md`.
  The initial ordered-only pending analysis is superseded by the two-layout
  audit. Conditional exact-placement capability is the next promotion gate;
  wider actor/equipment command paths are not admitted by this acceptance.
