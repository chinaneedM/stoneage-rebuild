# Actual original default template, table and header layout R1

Status: LOCAL PASS; exact-input remote acceptance PENDING.
Evidence class: FACT bounded to the same three pinned descendant profiles and
current version.h configuration. No original executable/JSS/Taiwan-v1 equivalence,
no original build/ABI claim and zero runtime-pressure promotions.

This closes the earlier controlled-template limitation for the default getter.
The actual defaultPlayer.h, Char definition, enums, animation constants, feature
headers and complete 53-row default table are compiled without replacement.
The unchanged preprocessed CHAR_getDefaultChar functional body executes. Original
source remains transient outside this repository; receipts contain derived hashes,
ordinals, table identifiers and semantic findings only.

## Scope and checks

Each profile executes every 53-row table image plus unmatched image 31010, -1,
0 and INT_MAX, with destination bytes initially 0/0x5a/0xa5/0xff. Each case invokes
the getter twice. 228 cases per profile per optimization at GNU99 O0/O2 with
nonrecovering UBSan: 2,736 getter calls. Destination never aliases the original
static player template. Four semantic mutations per profile/optimization must
fail (remove memset, corrupt work reset, corrupt item sentinel, remove data copy):
24 rejected native mutations. 116 regressions and six predecessor complete reports
must pass unchanged.

The oracle independently parses the preprocessed positional initializer and enum
expressions. It derives the expected copied data prefix, work values and flags;
the native witness compares every data/work/flag element and the complete Char
object representation with a separately zero-initialized expected structure.
Inventory/title/pet/petskill sentinels are constructed using original capacities;
all remaining storage, optional pointers, callback strings/functions and padding
must match zero. LP64 host widths (pointer8/int4) are required; offsets/sizes are
host observations, never asserted to be original binary layout. The native
initializer values are also compared to independent parsing before getter calls.
Both optimization outputs must be identical; complete ordered output is hashed.
The concise native report contains these output digests, counts and layout records.

Source identity checks preserve clean exact Git pins, all source-header dependencies,
original file/getter hashes, preprocessed player/table hashes, active source macro
hashes and enum values. System header/compiler version is not a historical source
pin. No extra feature defines are injected. Other configurations remain OPEN.

## Findings

| Profile | Data ints / copy boundary | Work ints | Ticket / start / object ordinals | Extra data initializers |
| --- | --- | --- | --- | --- |
| gavin | 162 / 85 | 317 | 314 / 315 / 74 | 8 |
| iris | 159 / 84 | 316 | 313 / 314 / 74 | 10 |
| bismarck | 131 / 87 | 214 | 199 / 200 / 70 | 0 |

All actual table rows point to the same player and lvplayer00. Getter first writes
the row's image type, then overwrites that position while copying the player data
prefix: final image type is zero for every tested match and fallback. This ordering
is an observed source behavior, not a correction or desired modern behavior.
Image31010 is an unmatched fallback in this actual table; no enemy creation is
executed by that observation. Template strings and function tables are not copied.
Ticket/start/object work values are zero; FD is -1. gavin/iris also set chatroom -1;
Bismarck has no corresponding active enum and setter in this profile. Object0 alone
still establishes neither ownership nor a no-object sentinel.

Compiler diagnostics report 8/10 excess positional data initializers in gavin/iris;
they are counted, preserved and not silently suppressed. At the compiled enum
positions, gavin/iris static player has pig=-1/image100250; Bismarck static player
has pig100250/image0. Bismarck's comments label -1 and100250 as pig/image, but actual
positional initialization does not align with those labels under this configuration.
This is a bounded positional discrepancy; it is not proof of an original released
build defect or a complete cause analysis. All these fields lie after CHAR_INITDATA:
the getter outputs zero/zero for pig/image despite those static values. Comments
cannot substitute for compiled field positions. Preserve this distinction when
composing later creator/helper evidence.

## Remaining work

Execute full enemy creator/init/helper paths with their actual table/data/function
provenance and naturally reachable ticket/object states; then compose full Exit
with allocator reuse. This gate does not execute allocator using this exact template
or compose lifecycle helpers. Source string corruption, destination aliasing,
other feature/compile profiles, original build/ABI/maps/network/JSS/Taiwan-v1,
remaining actor ownership/stats/property/timer and matched-player/watch creation/
multi-actor/typed631/635 persistent/coordinator admission remain OPEN.
No engine/content-design transition. Pressure unchanged:
2486 = 2465 closed capability + 18 OPEN + 3 historical UB; zero promotions.
