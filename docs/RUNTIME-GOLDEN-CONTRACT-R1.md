# Runtime Golden Contract R1

## Status

**IMPLEMENTED / PENDING REMOTE CI.**

Schema: `stoneage.runtime-golden.r1`.

Canonical artifacts:

- `game/STONEAGE-RUNTIME-GOLDEN-CONTRACT-R1.json`
- `tools/stoneage_runtime_golden_contract.py`
- `tests/test_stoneage_runtime_golden_contract.py`

## 1. Purpose

This contract is the first cross-language behavioral oracle for the future
standalone production core.

The committed JSON contains only synthetic project-owned test data. It contains
no recovered DAT/MAP/ADRN/BIN bytes, no original game assets, and no dependency
on a user-supplied recovered bundle.

A future C# test runner must be able to consume the same JSON without
translating it into a C#-specific fixture format.

## 2. Covered semantics

R1 pins:

- canonical `stoneage.local-runtime-session.r1` JSON serialization and
  decode round-trip, including UTF-8 text and sorted world flags;
- static collision denial;
- independent non-overable live-character denial;
- classic overlap-Warp transition after a successful walk;
- spatial discovery of a state-gated dialogue interaction after Warp arrival;
- dispatch of that semantic interaction id through the canonical gate path;
- save -> state change -> continue restoring the saved authoritative session;
- baseline-relative occupancy delta for a moved initial character plus a new
  non-overable item;
- fail-closed wrong-session-contract handling;
- fail-closed zero-length semantic movement intent.

## 3. Synthetic world

The fixture uses two tiny 4x4 maps, one classic Warp, one synthetic dialogue
gate, and one synthetic non-overable character.

The runtime profile still uses the existing engine-neutral `recovered25`
profile label because the R1 bootstrap type validation currently requires it.
That is a schema/profile compatibility label inside this test harness, not
recovered historical content.

## 4. Parity rule

The Python verifier is the current executable oracle.

A future standalone C# implementation must reproduce the fixture's semantic
outputs before the corresponding subsystem can be considered ported.

Parity is based on semantic JSON fields, not Python object reprs or
implementation-specific class layouts.

When intentional runtime behavior changes, update the golden schema/version or
fixture and Python verifier together, record the reason in
`docs/CURRENT-STATE.md`, and require every production implementation to move
in lockstep.

## 5. Copyright/provenance boundary

Golden fixtures must remain safe to commit publicly.

Do not add:

- original StoneAge images/audio;
- recovered binary file payloads;
- proprietary client/server data blobs;
- opaque large byte arrays copied from a recovered distribution.

Recovered evidence may motivate semantics, but cross-language fixtures should
express the resulting normalized rule using synthetic values wherever possible.
