# StoneAge TimeMan Core R1

Status: fixed-descendant common core plus verified recovered 2.5 active surface.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

The three npc_timeman.c implementations are behaviorally convergent.

Recovered specimen:

- source bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- TimeMan argument aggregate SHA-256 7a3dfbacbaba1137d10052959eb299b0e9c1e1cfa3bff86181b637e5c52aa457
- real-byte workflow 35384038054: success
- 34 TimeMan refs, all 34 resolved file-backed

## StoneAge time scale

TimeMan does not use real-world clock hours.

The fixed handletime core defines:

- 5400 real seconds per StoneAge day;
- 1024 StoneAge hour units per day;
- 100 StoneAge days per year.

So one StoneAge day lasts 90 real minutes, and TimeMan compares an integer hour in the 0..1023 cycle.

RealTimeToLSTime computes:

hour = (seconds_within_5400_second_day * 1024) / 5400

with integer truncation.

## Common TimeMan table

The fixed table is:

- ALLNIGHT -> born 301, dead 700
- ALLNOON -> born 701, dead 300
- AM -> born 501, dead 125
- PM -> born 126, dead 500
- FORE -> born 701, dead 125
- AFTER -> born 126, dead 300
- EVNING -> born 301, dead 500
- MORNING -> born 501, dead 700
- FREE -> born 0, dead 1024

The misspelling EVNING is source data and should not be normalized in archaeology parsing.

Initialization scans this table in order and accepts the first table label found as a substring of the configured time value. Unknown/missing time makes TimeMan initialization fail.

## Recovered 2.5 active distribution

Only three table modes are used by the 34 recovered configs:

- ALLNOON: 18
- ALLNIGHT: 9
- AFTER: 7

No recovered 2.5 TimeMan uses AM, PM, FORE, EVNING, MORNING or FREE.

All 34 have main_msg.

main_msg comma-separated variant counts are:

- 1 variant: 16 configs
- 2 variants: 12 configs
- 3 variants: 3 configs
- 4 variants: 3 configs

Only four configs contain change_msg; each contains one variant.

Thirty configs omit change_no, which source normalizes to graphic 9999.

Four configs use a numeric alternate graphic.

No recovered config uses an explicit CLS-containing change_no in this specimen.

The R1 aggregate reports the change-mode and change-message totals independently; it does not claim pairwise identity solely from equal counts.

## Alternate graphic initialization

TimeMan stores the NPC's current base graphic as the original graphic.

For the alternate graphic:

- missing change_no -> 9999;
- any change_no containing substring CLS -> 9999;
- otherwise atoi(change_no).

Graphic 9999 means the TimeMan is hidden for interaction purposes.

The source checks for substring CLS, not exact equality.

## Time-window semantics

TimeMan uses strict boundaries.

For a non-wrapping interval where born < dead:

active iff born < hour < dead

Both endpoints are excluded.

For a wrapping interval where born >= dead:

active iff
born < hour < 1024
or
0 < hour < dead

Hour zero is explicitly excluded by the second branch.

This creates edge behavior that should not be smoothed in reconstruction.

Example ALLNOON, 701 -> 300:

- 701 inactive
- 702..1023 active
- 0 inactive
- 1..299 active
- 300 inactive

FREE is also slightly non-total under the literal code: its 0 -> 1024 interval is active for 1..1023, while exact hour 0 is inactive.

## Event-driven update, not a timer loop

NPC_TimeManInit does not immediately evaluate current StoneAge time.

It stores:

- original graphic;
- alternate graphic;
- born/dead window.

It does not explicitly initialize E_INT_MODE or E_INT_NOWGRAPHIC and does not invoke the time-state transition.

NPC_TimeManWatch performs the actual RealTimeToLSTime check, and Watch first requires the triggering nearby object to be a player.

Therefore TimeMan is lazily/event-driven: its visual mode is corrected when a relevant player Watch event occurs, not by an autonomous per-NPC timer in this source.

## Watch transition

On an active time:

- target graphic = original;
- mode = 0.

On an inactive time:

- target graphic = alternate;
- mode = 1.

Before mutating, source compares E_INT_NOWGRAPHIC to the target graphic. If already equal, it returns without broadcast.

Otherwise it:

1. writes CHAR_BASEIMAGENUMBER;
2. broadcasts the character change around the NPC;
3. writes mode;
4. records the current graphic in E_INT_NOWGRAPHIC.

## Talk behavior

Talk requires the normal proximity/front/player checks.

Additionally, if current base graphic is 9999, TimeMan returns immediately and cannot talk.

Mode 0 selects main_msg.

Any nonzero mode selects change_msg.

The selected message string is split by comma and one token is chosen with rand()%tokennum.

The source does not validate the GetStr result before iterating the message buffer. Missing message configuration is therefore unsafe source behavior. The recovered corpus avoids missing main_msg, while 30 configs omit change_msg; those 30 also predominantly use hidden alternate behavior at the aggregate level, but the R1 probe does not encode pairwise config identity.

## Deterministic artifacts

- tools/stoneage_timeman_core_model.py
- tests/test_stoneage_timeman_core_model.py
- .github/workflows/validate-stoneage-timeman-core.yml
- research/recovered/STONEAGE-25-TIMEMAN-USAGE-R1.txt

Local reference validation: 18 deterministic tests passed.

## Evidence status

FACT: all three fixed descendants share the same TimeMan table and control flow.

FACT: StoneAge time uses a 5400-real-second day mapped to 1024 internal hour units.

FACT: all 34 recovered TimeMan refs are resolved file-backed configs.

FACT: recovered active time modes are only ALLNOON 18, ALLNIGHT 9 and AFTER 7.

FACT: 30 recovered configs omit change_no and therefore default to hidden graphic 9999; four use numeric alternate graphics.

FACT: every recovered config has main_msg; only four have change_msg.

SOURCE QUIRK: time interval endpoints are excluded.

SOURCE QUIRK: exact StoneAge hour 0 is excluded even in wrapping/FREE logic.

SOURCE QUIRK: initialization is lazy with respect to current time; mode correction happens on Watch events.

SOURCE QUIRK: missing message fields are not safely validated before message-buffer use.

OPEN: exact JSS-era TimeMan placement/configuration and whether earlier commercial data used additional time-table modes.

## Next seam

TimeMan R1 is closed. Advance to Windowman as the next deterministic conditional-window seam, beginning with a recovered conff-shape probe to verify whether its parsed-but-unexecuted takeitem/giveitem/warp/battle fields are present in 2.5 data.
