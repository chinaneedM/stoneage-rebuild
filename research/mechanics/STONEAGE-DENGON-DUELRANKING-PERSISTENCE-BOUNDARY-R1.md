# StoneAge Dengon / Duelranking Persistence Boundary R1

Status: **common fixed-descendant persistence/display boundary closed**

## Scope

This pass resolves the first item in the current persistence/display-boundary triage:

- whether `Dengon` is only presentation or owns durable state;
- whether ordinary `Duelranking` only displays server state or introduces an unmodeled persistent mutation.

Evidence controls:

- `gavinlinasd/StoneAge` @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- `iriselia/StoneAge` @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- `BismarckDD/stoneage` @ `999ffdf1d220ec6666eb65339180689c9caf1876`;
- recovered 2.5 bundle SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`;
- recovered Dengon runtime aggregate SHA-256 `cd107a9e86276ede4078bee722bb6b8fb051e9fc72947b2524c7d343e54ace10`.

## Dengon — persistent world-message state

`Dengon` is not merely a presentation NPC.

The three inspected descendants converge on a server-local bulletin-board implementation. The board file is addressed from the NPC's floor/X/Y position and stored beneath the server `Dengon` directory.

The common fixed format is:

- 1000 fixed slots;
- 11-byte decimal-ID prefix (`10 digits + :`);
- 256-byte message area;
- one newline byte;
- 268 bytes per slot;
- 268,000 bytes for a normally initialized empty board;
- seven displayed records per page.

When the file is absent, init creates all 1000 blank records, scans the ID prefix of each slot and recovers the maximum message ID.

Posting a non-empty message increments the board max ID and writes to `id % 1000`, making the file a fixed ring buffer. The payload also includes server-formatted time and player attribution. These payload fields are not retained in derived project reports.

### Persistence classification

**FACT:** Dengon mutates durable server-local board data.

**FACT:** this is world/message persistence, not ordinary player progression persistence. The common path does not alter inventory, Gold, pet state, location, save/progression fields, or similar character state.

### Recovered 2.5 runtime snapshot

The recovered 2.5 specimen contains 40 Dengon files. Every one is exactly 11 bytes and contains only a zero counter stub. No full 268-byte record is recoverable.

This is a significant shape mismatch with the literal common runtime initializer, which creates 268,000-byte files when a board is missing.

Therefore:

- the 40 stubs are not evidence for an 11-byte live board format;
- the snapshot contains no recoverable historical board messages;
- the stubs are classified as reset/preparation/runtime-residue artifacts unless another source proves their creation path;
- the fixed reader's unchecked short reads mean such a stub must not be treated as a valid populated board image.

## Duelranking — read/display adapter over persistent duel state

The ordinary common `Duelranking` path is read-only with respect to persistent duel ranking.

Interaction opens a ranking-choice window for a player within one tile. The common path then uses SAAC database queries against `DB_DUELPOINT`:

- top ranking: `DBGetEntryByCount(... start=0, count=10 ...)`;
- own ranking: build the player's DB key and call `DBGetEntryRank`;
- page navigation: query ten-row windows;
- own-rank context: query a ten-row window beginning five rows before the returned rank count, clamped at zero.

The display callback formats returned rows and updates `CHAR_WORKSHOPRELEVANT` as a transient page offset. It does not write duel points.

### Persistence classification

**FACT:** ordinary Duelranking reads persistent duel ranking through SAAC database queries.

**FACT:** the common NPC code does not write `DB_DUELPOINT`.

**FACT:** its ordinary per-player mutation is transient pagination state only.

**RESEARCH CONSEQUENCE:** the subsystem that awards or persists duel points is elsewhere in the duel/combat/account pipeline. Duelranking must not be reconstructed as that mutation source.

## Later compile-gated branches

The gavinlinasd/iriselia source family also carries compile-gated tournament and family-contend branches. Depending on feature flags, those branches can schedule tournament activity, maintain separate family-contend lists and write family participation state.

Those branches are strongly coupled to later tournament/family packages and are not part of the stable ordinary Duelranking core. They remain deferred with Raceman / ManorSman / FMPK / FMWarp and related later-scope systems.

## Evidence status

**FACT:** Dengon owns durable local bulletin-board files.

**FACT:** the recovered 2.5 Dengon files are 40 zero-counter 11-byte stubs, not valid full runtime board images.

**FACT:** ordinary Duelranking is a persistent-state reader/display adapter, not a duel-score writer.

**VERSIONED/LATER:** family/tournament extensions can add separate mutation paths behind compile-time feature switches.

**OPEN:** the exact historical subsystem that awards/writes duel points; trace it only if detailed duel scoring becomes a concrete core-combat gap.

## Priority consequence

The persistence/display-boundary triage now advances to the personal bank path: trace `CHAR_BANKGOLD` deposit/withdraw persistence separately from later family-account coupling before opening the broader family Bankman package.