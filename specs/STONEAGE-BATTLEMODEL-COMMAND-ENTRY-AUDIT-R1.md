# BattleModel command-entry audit R1

Date: 2026-10-06. Status: SOURCE_NATIVE_PASS / EXACT_HEAD_DATA_PENDING.

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

The C lexical census includes definitions and registrations. It is bounded
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
Actions and derived report review are required before accepting this audit.

## Reproduction

- `python -m unittest tests.test_stoneage_battlemodel_command_entry_audit`
- `python -m tools.stoneage_battlemodel_command_entry_source_audit` with three
  pinned source directories (see settlement workflow).
- `python -m tools.stoneage_recovered25_battlemodel_command_entry_probe` with
  exact preservation `--data-dir` and `--setup` (see full-region workflow).
