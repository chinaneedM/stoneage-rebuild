# Tools

Reproducible archaeology tools and later development utilities.

All archaeology probes are designed to emit derived metadata/statistics rather than copying proprietary client payload bytes into the repository.

Current tools:

- `stoneage_resource_probe.py` — validates StoneAge ADRN/REAL image-container structure and recovered MAP file geometry.
- `stoneage_rd_codec.py` — independently reconstructed legacy RD image decoder/codec primitives.
- `stoneage_rd_validate.py` — validates the RD decoder against selected recovered REAL/ADRN blocks.
- `stoneage_spr_probe.py` — parses SPRADRN/SPR animation streams and cross-checks frame image references against ADRN.
- `stoneage_map_pair_probe.py` — compares recovered one-layer MAP files with same-stem three-layer DAT caches.
- `stoneage_client_server_map_probe.py` — cross-checks recovered client-directory MAP data against the bundled SACH/server-related map corpus.
- `stoneage_dat_probe.py` — parses the case-insensitive recovered DAT cache corpus, profiles tile/parts/event layers, maps graphic references through ADRN, and isolates event-domain anomalies.
- `stoneage_dat_server_probe.py` — compares recovered numeric DAT tile/parts layers with same-ID LS2MAP server tile/object layers to identify exact matches, revision drift, and map-specific cache anomalies.
