# BattleModel ID638 normal-death persistent/coordinator bridge R1

Status: CLOSED_BOUNDED_ID638_NORMAL_DEATH_PERSISTENT_COORDINATOR.

## Purpose

Bind the already accepted recovered ID638/template admission to the canonical
persistent battle and local runtime coordinator **for normal death only**.

This checkpoint is deliberately narrower than full lethal638. It proves that
an explicitly admitted ID638 BattleModel action may create a normal death at
the source-shaped command-tail profit boundary and that the existing immutable
whole-scan settlement owns the resulting ISDIE/death accounting.

## Explicit scopes

The existing nonlethal scope remains unchanged:

`nonlethal_base_round_empty_equipment_ID638_R1`

A second, explicit scope is admitted:

`lethal_normal_profit_base_round_empty_equipment_ID638_R1`

The new scope permits only a **normal** BattleModel death. It does not admit an
ultimate flag, BATTLE_UltimateExtra, BATTLE_Exit, ride/equipment, unrelated
semantic callbacks or a death created by a later non-BattleModel action in the
same round.

## Runtime chronology

For the admitted normal-death path:

1. the coordinator re-admits the typed BattleModel submission against the
   current spawned template, selected runtime skill slot and loaded skill row;
2. the existing BattleModel physical/hit loop executes ID638;
3. the command driver records one
   `PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL` snapshot after all BattleModel
   hits;
4. the persistent layer resolves that boundary through the accepted immutable
   `ProfitExitSnapshot` whole scan;
5. only the scan's `processed_death_ids` becomes persistent death authority;
6. the pre-round persistent/context objects remain immutable.

The new scope does not bypass the existing fail-closed identity checks.

## Fail-closed boundaries

- The original nonlethal scope still rejects any BattleModel death.
- Both scopes still reject any BattleModel ultimate flag.
- Both scopes reject a death caused outside the explicit ID638 BattleModel
  command-tail action.
- Automatic BattleModel AI selection remains outside this checkpoint.
- Historical packet/presentation behavior remains outside this checkpoint.
- No recovered positive slot is promoted by this milestone.

## Remote acceptance — 2026-10-06

Implementation head:
`6c4032a4d6f3c3ab12b2e2c0c9830033809ba33b`,
tree `ec14ccbe881f6065ac1afc73466a702758a6eba4`.

Final tested input:
`89848f2ed92c4aa4c21c70d68356fe52b951ab40`,
tree `312a842d8d093fa57bb1b4a4200186dcaa63ce1a`.

BattleModel settlement:
`37443593822 / 112202958318` — SUCCESS, **655 tests**.
Artifact `11401694955`,
`sha256:d9bae433e4e06df60f2f18f7c6b11a697aff04377be8619fe6862e9ec6b1b41e`.

The same settlement also preserves:

- 19656 original PvE profit/exit cases;
- 19656 immutable scan/model-native comparisons;
- full original BATTLE_Battling BattleModel profit-tail 9/9;
- same-harness exact DamageSub 9/9;
- same-harness original Guardian 9/9;
- dispatch-tail splice 9/9;
- 384 bounded Weaken recalculation vectors.

Implementation-head integration pressure:

- local runtime session coordinator
  `37443283037 / 112201941097` — SUCCESS, **231 tests**;
- runtime golden contract
  `37443283236 / 112201941937` — SUCCESS;
- recovered25 region/runtime-stack
  `37443283255 / 112201946517` — SUCCESS.

## Next gate

Full lethal638 remains open.

The next gate must carry BattleModel `ultimate_kind` into the command-tail
boundary and reproduce source AddProfit scan ordering for multi-victim
ultimate/Exit composition. In particular, a Guardian pet may be hit before its
owner while AddProfit scans owner slot0 before pet slot5. Default-pet clearing,
player/pet Exit and duplicate suppression must follow the source scan order,
not hit order.

Only after that stronger ultimate/Exit path agrees with the exact full
BATTLE_Battling evidence and canonical persistent/coordinator runtime may the
two recovered positive BattleModel slots be evaluated for promotion.
