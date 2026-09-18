# StoneAge Bus + Airplane Transport Core R1

Status: fixed-descendant common transport reconstruction. Recovered 2.5 key/route-shape measurement remains the next step.

## Fixed source set

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Primary files are npc_bus.c, npc_airplane.c and char_party.c.

## Shared initialization

Both classes require routenum and every routetoN from 1 through routenum. Missing route definitions fail initialization.

waittime defaults to 180 seconds. seflg defaults true. Both start in waiting mode 0, routepoint 2, roundtrip 0, with the current route chosen randomly from 1..routenum.

reverse=1 is not a simple direction flag: initialization sets routepoint to route_point_count - 1 and roundtrip to 1 before loading the target point.

Bus fast loop is 200 ms. Air fast loop is 100 ms. Waiting loop is 5000 ms.

Air additionally has WAVE default 77 and oneway default false.

## Route point formats

Bus routetoN points are x,y.

Air routetoN points are floor,x,y. When an Air route point changes floor, AirSetPoint immediately warps the transport NPC and every onboard party member to the new floor,x,y before continuing movement.

Both use semicolon-separated point lists. GetRoutePointNum iterates the old delimiter helper and returns the count.

## State machine

Mode 0 waits until current_time + waittime < now. Equality does not depart. On departure the mode becomes 1 and the fast loop interval is installed.

Mode 1 executes walking and intentionally falls through to the mode-2 case in the switch.

Mode 2 has a waittime/3 resume test, although the user-facing stop command that assigns mode 2 is compiled out with #if 0 in the inspected source.

When walking advances beyond the indexed route point list, the vehicle enters mode 3, records current time and sends end messages.

Mode 3 requires current_time + 3 < now. It then randomly selects a route, toggles roundtrip with XOR 1, chooses the next indexed point for the new direction, loads route/title, discharges the whole transport party, records current time and returns to waiting mode.

Air oneway has a special terminal rule: when oneway=1 and the toggled roundtrip becomes 1, Air immediately resumes mode 1 at the 100 ms loop instead of returning to mode 0.

## The actual boarding entry is shared

This is the most important source-call-graph result.

Both Bus and Air initialize CHAR_WHICHTYPE as CHAR_TYPEBUS.

The generic CHAR_JoinParty scan sees CHAR_TYPEBUS and calls NPC_BusCheckJoinParty. It does not dispatch to NPC_AirCheckJoinParty. After that check succeeds, the normal party path calls CHAR_JoinParty_Main and makes the transport NPC the party leader and the passenger a client.

NPC_AirCheckJoinParty exists in npc_airplane.c, but the inspected fixed source has no live generic-party call site for it; its Talked call is commented out, just like Bus Talked's direct check.

Therefore Air-only boarding extensions inside NPC_AirCheckJoinParty must not be promoted into the active generic boarding rules merely because their source functions exist.

## Common boarding gate order

The active generic Bus/Air boarding check is:

1. player must be exactly in front of the transport;
2. transport mode must be 0;
3. player must not already be in a party;
4. the transport party must have an empty slot;
5. denieditem must not match any carried/equipped item slot;
6. the compile-enabled _ITEM_CHECKWARES gate must allow the player;
7. every allowitem ID must be present;
8. needlevel must be satisfied when configured;
9. needstone must be affordable;
10. nonzero needstone is deducted immediately;
11. only after that does CHAR_JoinParty call CHAR_JoinParty_Main.

_ITEM_CHECKWARES is enabled in all three fixed descendants.

The event-state boarding check present in comments is disabled.

## Item-list semantics

denieditem scans all item slots and rejects if any configured ID is found.

allowitem performs a fresh full scan for every configured ID. During boarding preflight pickupmode is false, so duplicate configured IDs can reuse one physical item.

pickupitem only changes behavior when NPC_BusCheckAllowItem is later called with pickupmode=true. It then deletes the first matched item as each allowitem ID is processed. This is non-transactional: if an early item is deleted and a later required item is missing, the earlier deletion remains. Duplicate IDs require multiple physical copies in pickup mode.

## pickupitem is not ordinary arrival ticket consumption

CHAR_DischargeParty has two materially different paths.

When a passenger individually leaves as a party client and its leader is CHAR_TYPEBUS, source calls NPC_BusCheckAllowItem(..., TRUE). pickupitem can therefore delete allowitem entries in this client-leave path.

At a normal route terminal, however, Bus/Air calls CHAR_DischargeParty on the transport NPC itself. The transport is the party leader, so leader-side whole-party discharge runs. That branch does not call NPC_BusCheckAllowItem(..., TRUE) for passengers.

Therefore ordinary terminal arrival does not consume pickupitem through this path. This behavior should not be rewritten into a conventional ticket-consumption model during archaeology reconstruction.

## Stone and level quirks

Missing needlevel is represented by -1 and skips the minimum-level gate. Otherwise player level must be >= needlevel.

Missing needstone is represented by -1 and means free travel. Otherwise the checker returns the configured integer if current gold is >= it, or -1 on failure.

The caller subtracts every nonzero returned value. Consequently a malformed configured needstone less than -1 would add Stone rather than subtract it. R1 preserves this source arithmetic; recovered-data measurement will determine whether such values exist.

Stone is deducted before CHAR_JoinParty_Main, not after party mutation.

## Air-only source branches that are not active generic boarding rules

gavin and iriselia contain compile-disabled _NPC_AIRDELITEM and _NPC_AIRLEVEL definitions; Bismarck does not expose those flags in version.h.

Even if enabled, those checks live in NPC_AirCheckJoinParty, which the generic CHAR_TYPEBUS join path does not call in the inspected fixed source.

Accordingly delitem ticket deletion and maxlevel are source capabilities / later extensions, not part of the common active generic Bus/Air boarding core.

## Deterministic artifacts

- tools/stoneage_transport_core_model.py
- tests/test_stoneage_transport_core_model.py
- .github/workflows/validate-stoneage-transport-core.yml

Local validation: 26 deterministic tests passed.

## Evidence status

FACT: Bus and Air share CHAR_TYPEBUS generic party boarding through NPC_BusCheckJoinParty.

FACT: _ITEM_CHECKWARES is enabled in all three fixed descendants.

FACT: Bus uses x,y route points; Air uses floor,x,y and warps the whole onboard party on floor transition.

FACT: terminal whole-party discharge differs from individual passenger leave for pickupitem deletion.

SOURCE QUIRK: duplicate allowitem IDs can reuse one item during boarding preflight but require multiple copies when pickup deletion is active.

SOURCE QUIRK: pickup deletion is non-transactional.

SOURCE QUIRK: needstone values below -1 would increase gold.

VERSIONED / DORMANT: Air delitem/maxlevel boarding extensions are not on the active generic join path.

OPEN: which route/gate keys and route shapes are actually present in the verified recovered 2.5 Bus/Air argument files.

## Next seam

Run a payload-free recovered Bus/Air secondary-argument usage probe on the verified 2.5 bundle. Use it to distinguish active 2.5 route/economy configuration from dormant source capabilities, then close or narrow this transport seam.
