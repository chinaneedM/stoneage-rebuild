# BattleModel default selection and ultimate exit audit R1

Status: CLOSED_BOUNDED_DEFAULTPET_HELPER_AUDIT;
runtime correction and full cleanup/profit integration OPEN.

Exact input `b6ca59eb86d2e0d1462fcdf56939d2c1cd7e6f8b`, tree
`23f26db6cb082ec75b742ad48f5c5a9f1b633ca1`: run `37415958204`, job
`112114499031` SUCCESS. Logs reproduce486 native helper cases and all428
shared tests/696 physical/3420 ItemCrush/1920 settlement/480 marker/60 pet
gates. Derived artifact `11391295439` uploaded. Receipt:
`research/recovered/STONEAGE-DEFAULT-PET-EXIT-HELPER-ACCEPTANCE-R1.json`.

## Evidence and boundary

`tools/stoneage_default_pet_exit_source_audit.py` checks clean HEAD/tree at
the three existing fixed descendant pins, compiles the unmodified original
`BATTLE_PetDefaultExit` transiently, and executes 162 cases per pin, 486 total.
Controlled getter and `BATTLE_Exit` stubs expose lookup identity, call count,
return value and selection stability. No original source is retained here.
Constants in the harness represent symbolic branches, not historical enum or
command numbers. This is no original build or Taiwan-v1 membership certificate.

Cases cross invalid/valid owner, player/pet/other kind, no selection/slot0/slot4,
missing/different lookup identity, and successful/positive/negative exit result.
All three pins agree: invalid owner rejects; nonplayer or negative selection
performs no lookup/exit. A selected player passes that exact roster slot and
resolved identity to Exit, including a missing lookup for Exit to reject. Exit
success returns1; nonzero result is negated. The helper does not clear selection.
It does not count active pets or infer default selection from ownership.

Separate **static** source anchors identify:

- player UltimateExtra calls PetDefaultExit before its own Exit;
- pet UltimateExtra writes owner DEFAULTPET=-1;
- player `_BATTLE_Exit` independently reads/clears `Entry[i+5]`;
- existing recorded player exit also recovers/clears carried non-mail pets.

The two underscored Bismarck identifiers are normalized only for static token
checks; the compiled helper is unchanged. Static anchors are not native full
UltimateExtra/Exit/feature-profile acceptance. Stub Exit deliberately does not
certify occupancy changes, HP recovery, selection mutation or profit.

## Actual repository integration gaps

`selected_default_pet_participant_id(state)` already resolves nullable roster
selection independently of occupancy. Ordinary kill profit already reads that
explicit identity for loyalty. However, the ordinary `register_ultimate_exits`
closure and ContinuationAttack exit block still infer the sole active allied
pet. Their comments saying the session lacks a selector are superseded by
DD-020 and the current persistent state.

The state adapter passes explicit selection to recall/BattleTimid, but supplies
no general selection identity to ordinary/continuation ultimate exit. Its
`next_default_pet_slot` handlers clear selection for those recall events and
have no dedicated pet-ultimate selection transition. The profit-event walk
also clears its current selection only on recall, so a pet ultimate followed
by player death needs chronological review. This is an OPEN defect audit;
no runtime correction is claimed by this source helper certificate.

## Required integration contract

1. Pass an explicit nullable selected roster identity through the persistent
   adapter, ordinary driver and continuation path. Direct low-level callers
   must distinguish missing authority from an explicit no-selection value.
2. Keep selected-pet helper exit separate from player-slot paired occupancy
   cleanup. No-selection means no selected lookup; it does **not** prove that
   the later player Exit leaves `i+5` occupied. Conversely carried ownership
   cleanup does not authorize arbitrary same-side battle-entry removal.
3. Preserve per-owner/slot binding and actual Guardian victim. In the declared
   reduced layout, require evidenced player `i`/pet `i+5` occupancy identity or
   explicitly reject mismatches. Do not silently choose an unrelated sole pet.
4. A pet ultimate clears owner default selection chronologically, including
   before any later player-death loyalty scan; a player ultimate helper by
   itself does not clear DEFAULTPET. Preserve roster ownership and surviving HP.
5. Skip later actions for actually exited entries; process AddProfit/exit at
   source-defined trigger points. Do not use restored player HP1 to award final
   EXP/items. Existing explicit elder-return/terminal settlement remains binding.

Required witnesses: no selected pet with paired occupancy, selected/paired
matching, selected retained but absent from battle, unrelated sole pet,
multiple retained pets, already recalled/exited selected pet, pet ultimate then
player death, Guardian redirection, ordinary and continuation agreement,
failure immutability, save/return selection persistence and no erroneous final
profit. Full native exit/profit composition remains required; this helper audit
does not discharge these witnesses or enable lethal ID638.

## Acceptance sequence

Exact settlement CI must reproduce486 helper cases plus existing428 shared
tests/696 physical/3420 ItemCrush/1920 settlement/480 marker/60 pet gates.
Accept this audit separately from the runtime correction. Then isolate the
selection/occupancy correction and its ordinary/persistent/continuation tests
before lethal BattleModel integration. Keep automatic AI, equipped/wider
features and BattleModel-specific golden/region/hash-verified pressure OPEN;
no ID638 positive slot promotion. DD-018 and DD-020 remain in force.
