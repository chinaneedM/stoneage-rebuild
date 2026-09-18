# JSS Baseline vs 2003 Revival Delta — R1

Date: 2026-09-18

Purpose: use the earliest Japanese revival reporting as a controlled near-descendant comparison surface for reconstructing the former JSS/Gamer's Dream StoneAge baseline.

This file does **not** treat the 2003 revival client as the 1999 client. It records only feature boundaries that contemporary specialist reporting explicitly attributes to the earlier Japanese service or to changes introduced for the revival.

## Evidence classes

- **B / RETROSPECTIVE BASELINE EVIDENCE** — a specialist reporter in 2003 describes the former Japanese StoneAge service only a few years after it ended.
- **A/B / DIRECT 2003 STAFF COMMENT** — 4Gamer reports a direct on-site answer from revival staff.
- **OPEN** — exact build/date/data implementation remains unresolved.

Primary sources registered in `docs/SOURCE-REGISTRY.md`:

- `SRC-JP-2003-4GAMER-OGF-REVIVAL-01`
- `SRC-JP-2003-4GAMER-TGS-REVIVAL-01`

## 1. Why the 2003 revival is archaeologically valuable

The 2003 Japanese revival is close enough to the original shutdown that:

- the former Japanese version was still within recent professional/player memory;
- the revival team was working with StoneAge rights/data rather than reconstructing the title decades later;
- 4Gamer explicitly asked how the revival differed from the former version;
- at least one report records an on-site staff answer that the immediate revival state was **basically the same**, with bug fixing/restoration first and larger additions planned later.

This makes the revival a valuable **near-descendant diff anchor**.

It is still not a substitute for an authenticated 1999 retail/beta client.

## 2. Baseline mechanic: monster capture / pets

The July 2003 4Gamer revival announcement retrospectively describes the former title as including:

- monster capture;
- use of captured monsters as pets;
- turn-based combat;
- parties of up to five players.

Classification: **B / retrospective baseline evidence**.

These features are consistent with other early evidence and can be used as search/validation targets when original client/server material is recovered.

## 3. Baseline boundary: normal-player riding was not part of the former Japanese service

The July 2003 report states that, during the former Japanese operation, **only GMs could ride dinosaurs**.

Classification: **B / retrospective baseline evidence**.

Research consequence:

- do not treat normal-player pet riding as an automatic JSS-1999/Japanese-original feature;
- if a later Taiwan/Mainland/Korean client exposes riding data, that data must be dated rather than projected backward;
- if a JSS retail/beta client contains mount graphics or code, distinguish **resource/code presence** from **normal-player availability**;
- determine separately whether the GM-only riding capability was client-side, server-authorized, event-specific, or present only in later JSS service states.

### What this closes

The project's earlier OPEN question “did normal players ride pets in the earliest Japanese StoneAge?” now has a strong working answer:

**Working baseline: no — the 2003 near-contemporary report says riding in the former Japanese operation was GM-only.**

This remains below first-party-primary certainty and can be superseded by direct JSS evidence.

## 4. Baseline boundary: no dedicated item-trade window

At TGS 2003, 4Gamer asked revival staff whether the new version was completely the same as the earlier game.

The staff answer was reported as:

- basically the same;
- restoration first;
- current work focused on bug fixing;
- several larger updates planned after open beta, including map expansion and characters.

The report then identifies one already-present minor change:

**the original did not have the dedicated item trade window.**

It describes the earlier exchange practice in terms of putting items on the ground, with the obvious risk that another player could take them.

Classification:

- direct “basically the same / restoration / bug-fixing” response: **A/B / direct 2003 staff comment**;
- absence of original trade window and ground-drop exchange description: **B / specialist retrospective comparison**.

Research consequence:

- a JSS-baseline reconstruction should not silently inherit a later dedicated trade UI;
- item ground-drop/pickup behavior becomes a high-value original-client/server reconstruction target;
- recover and test ownership rules, pickup eligibility, expiration, map persistence and whether any server-side exchange safeguards existed beyond the client UI.

## 5. Revival-delta caution

The July and September 2003 reports also say that the revival would contain or later receive:

- map additions/expansion;
- character additions;
- UI improvements;
- bug fixes.

Therefore a recovered 2003 Japanese revival client must be classified as a **near-descendant**, not an original binary proxy.

For every feature/data table found in a 2003 build, ask:

1. Is it directly attested in JSS-era evidence?
2. Is it explicitly identified as a 2003 addition?
3. Does it appear in Taiwan/Korea/Mainland descendants before the Japanese revival?
4. Can asset IDs, timestamps, update notes, or source history date it more narrowly?

## 6. Candidate baseline-delta matrix

| Feature | Former Japanese baseline working status | 2003 revival evidence | Confidence |
| --- | --- | --- | --- |
| Monster capture / pets | present | retrospective description | B |
| Turn-based combat | present | retrospective description | B |
| Party up to 5 | present | retrospective description | B |
| Normal-player dinosaur/pet riding | **not available**; GM-only riding reported | July 2003 retrospective | B |
| Dedicated item trade window | **absent** | explicitly described as revival minor change | B |
| Ground-drop item exchange | reported old practice/context | TGS 2003 comparison | B |
| Map/character additions | later revival changes planned | staff comments | A/B for plan |
| UI changes | revival modified/improved UI | July/September reports | B |

## 7. Next proof targets

1. Search surviving JSS manuals, support pages, screenshots and magazine scans for any normal-player riding command/UI.
2. Search JSS update history for riding-related changes or GM event references.
3. Recover early Taiwan/Korean evidence to date the first normal-player riding implementation by region.
4. Recover 2003 Japanese beta/client and diff its UI/data against any later or earlier preserved branch, specifically looking for the trade-window addition.
5. On an original JSS client, identify item drop/pickup code/data and determine whether exchange was merely an emergent ground-drop action or had server rules dedicated to transfer.
6. Do not infer feature availability solely from dormant graphics, animations, flags or GM-only code.
