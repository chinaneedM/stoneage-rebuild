# TW1.0 R62 — Retained R27–R58 post-WriteFile operand coverage census

**Status:** retained original-derived static report discovery, *not* binary analysis, API execution or persistence acceptance.

Scan one pinned report surface per version R27–R58, including ORIGINAL, DERIVED and SPEC forms. Collect each file's exact Git blob identity, count address-bearing metadata objects for `0x4c692` and `0x4c6f7`, and distinguish those address mentions from rows that provide **both** a decoded mnemonic and operand array. Structural graph nodes, stack-effect candidates, call-site metadata, and reaching EAX `unknown_call` probes do **not** count as full decoded instruction rows.

R28/R44/R45 already establish the bounded `0x4c5b4` native candidate graph, postcall EAX uncertainty, stack-effect candidates and first WriteFile precall definitions. These are necessary but insufficient for actual calling context, return value, bytes-written pointer alias, register/stack/callee preservation, conditional branch feasibility or persisted bytes. A complete retained-source scan takes priority over reacquiring the original binary.

The standalone tool `tools/stoneage_tw10_savedata_r62_source_coverage.py` hashes all 32 registered reports, requires immutable R28/R44/R45 blobs, and emits both positive and missing-evidence paths without preassuming that no usable operand row exists. Test fixtures intentionally inject *synthetic* full instruction operands as a positive classifier control; this **does not** change what the original client reports contain. CI derives and exactly replays a derived-only JSON census.

If complete target operand rows are absent from the retained sources, next obtain only a tightly bounded **non-executing, authenticated original-derived** instruction/CFG snapshot around `0x4c692` and `0x4c6f7` plus the caller/ABI preservation envelope; do not make broad download or native execution a prerequisite. The Stage A restoration matrix remains PARTIAL/OPEN, and Stage B new-game production remains deferred.
