# StoneAge Taiwan v1.0 Audio Provenance — R1

Date: 2026-09-19

## Scope

This note fixes the reconstruction boundary among the accepted Taiwan v1.0 retail client's three audio surfaces:

1. indexed records inside `sound_1.bin`;
2. loose SFX WAV files under `StoneAge/data/se/`;
3. loose BGM WAV files under `StoneAge/data/bgm/`.

Primary derived evidence:

- `research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt`
- source blob: `094becbc92397ee8abf72a014deffffabc97a316`
- generating tool: `tools/stoneage_tw10_audio_metadata.py`
- successful GitHub Actions run: `35451761733`

No proprietary audio payload is committed by this record.

## FACT — indexed container boundary

`soundaddr_1.txt` defines 114 indexed records that partition `sound_1.bin` contiguously from byte 0 through byte 3,695,418.

The reconstruction crosswalk resolves every indexed name to a loose SFX filename on the same retail disc. There are no missing loose counterparts.

The indexed/loose comparison is:

| Relation | Count |
| --- | ---: |
| byte-identical full WAV file | 107 |
| different WAV bytes, identical PCM `data` payload | 1 |
| different PCM `data` payload | 6 |
| indexed record with no loose counterpart | 0 |

Therefore the indexed container and loose SFX directory are related but not interchangeable provenance surfaces.

## FACT — the one wrapper-only variant

Indexed record 45, `sak_09a.wav`, differs from its loose same-name WAV as a complete file but has the same PCM `data` payload.

Both sides have:

- PCM format;
- mono channel;
- 11,025 Hz sample rate;
- 8-bit samples;
- 30,080-byte PCM payload;
- PCM SHA-256 `ac02d3c8521a0a66417046a5e82046f89916fcb71e35835a702e857b1def1fb2`.

Their RIFF chunk ordering/metadata differs. Reconstruction must therefore preserve the distinction between historical container bytes and historical loose-file bytes even when the audible sample payload is identical.

## FACT — six genuine payload variants

Six indexed records differ from their loose same-name files at the PCM payload layer:

- index 37: `sak_01.wav`
- index 38: `sak_02.wav`
- index 40: `sak_04.wav`
- index 41: `sak_05.wav`
- index 47: `sak_10.wav`
- index 48: `sak_11.wav`

These are not mere RIFF-wrapper differences and must not be silently normalized to one file.

A particularly visible format change occurs for `sak_01.wav`: the indexed container version is mono 11,025 Hz / 8-bit, whereas the loose same-name version is mono 11,025 Hz / 16-bit and substantially larger.

## FACT — the two unindexed loose files are exact aliases of indexed payloads

The loose SFX directory has 116 WAV files while the address table names only 114.

The two unindexed files are:

- `sak_91.wav`, 18,480 bytes, SHA-256 `a52bc353b31b3383d5c7faa7b746db376be2ec92f84518f246a35c0031ffb352`
- `sak_92.wav`, 44,504 bytes, SHA-256 `fb71374f48a6f79ecd009b1d6b606d81b6c3d9ee124323797baf515406c4da74`

Direct hash comparison establishes:

- `sak_91.wav` is byte-for-byte identical to **indexed record 37**, whose address-table name is `sak_01.wav`;
- `sak_92.wav` is byte-for-byte identical to **indexed record 38**, whose address-table name is `sak_02.wav`.

Thus the same retail disc simultaneously contains:

- indexed container payloads named `sak_01.wav` / `sak_02.wav`;
- loose same-name `sak_01.wav` / `sak_02.wav` files with different audio payloads;
- loose `sak_91.wav` / `sak_92.wav` files whose bytes exactly reproduce the indexed container payloads for 01/02.

The byte identity is FACT. The historical editorial reason for the 91/92 names, and whether they represent renamed originals, compatibility copies, replacement staging or another production convention, remains OPEN.

## FACT — BGM is a separate disc-resident surface

The retail disc contains 11 BGM WAV files under `StoneAge/data/bgm/`.

They are not members of `soundaddr_1.txt` and are not part of `sound_1.bin`. The audio reconstruction layer must therefore preserve BGM as an independent file-indexed subsystem rather than assigning it synthetic sound-container indices.

## Reconstruction rule

For an exact historical reconstruction:

1. preserve `soundaddr_1.txt` record order, offsets, sizes and indexed names as the canonical indexed-SFX namespace;
2. preserve the container segment hash independently from any loose-file hash;
3. retain loose same-name SFX as a separate provenance surface even when byte-identical;
4. retain wrapper-only and PCM-different variants as distinct historical resources;
5. retain `sak_91.wav` and `sak_92.wav` as separate loose-file identities while recording their exact alias relation to indexed 01/02 payloads;
6. preserve the 11 BGM files as a separate BGM namespace.

A modern engine may later deduplicate identical payloads internally, but deduplication is a DESIGN/storage optimization and must not erase the historical identity/provenance graph.

## Operational consequence

The deterministic v1.0 audio boundary is complete enough to leave the reconstruction-data critical path.

The next highest-priority task is to correlate **protocol-visible v1.0 character/pet/item/skill/NPC state** with the already recovered 2.5 server/master-data bridge. The later tables may explain field meaning and relationships, but no later-only field is to be promoted to v1.0 FACT without independent original-client/protocol support.
