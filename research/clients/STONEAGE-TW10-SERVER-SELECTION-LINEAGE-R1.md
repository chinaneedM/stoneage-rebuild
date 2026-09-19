# StoneAge Taiwan v1.0 server-selection and launcher lineage — R1

Date: 2026-09-19  
Primary specimen: accepted Taiwan Waei/JSS StoneAge v1.0 retail disc, Redump 104630  
Primary runtime: `StoneAge/sa_3.exe`  
Launcher/updater: `StoneAge/StoneAge.exe`

## Result

The Taiwan v1.0 game runtime does not contain a file-backed fixed game-server table. Its selected game endpoint is populated from the process startup command line, parsed into a runtime table, then consumed by the sole game-server connection path. The retail-disc launcher independently constructs the same startup-parameter family and launches a versioned `sa_%d.exe` process through its unique `CreateProcessA` site.

The exact operator-era source that supplies the dynamic `IP:` fragment before the launcher assembles the final command line is not yet identified. That remaining upstream detail is not required to reproduce the client/game boundary.

## Binary facts — runtime command source

- Shared startup-source global: RVA `0x139b758`.
- WinMain-shaped initialization begins at RVA `0x1c4c0`.
- Before local stack allocation:
  - `0x1c4c0: mov eax,[esp+16]`
  - `0x1c4c4: mov ecx,[esp+12]`
  - `0x1c4cb: mov [0x139b95c],eax`
  - `0x1c4d0: mov [0x139b758],ecx`
- The same function immediately enters normal GUI-process startup using `CreateMutexA`, `GetLastError`, `MessageBoxA`, `LoadIconA`, and `LoadCursorA`; its early exits use `ret 0x10`, consistent with four incoming arguments.
- Therefore the third incoming argument is directly stored as the shared startup command source.
- Exact later references to `0x139b758` feed the token family:
  - `realbin:`
  - `adrnbin:`
  - `sprbin:`
  - `spradrnbin:`
  - `windowmode`
  - `nodelay`
  - `updated`

## Binary facts — server-table parser

Server-table writer RVA: `0x2e890`.

The writer receives the shared startup text, searches for literal `IP:`, decodes a decimal slot number and fills a runtime server record. The table starts at RVA `0x13f5e40` and contains 10 records of 193 bytes:

- offset 0: used byte
- offset 1: 128-byte host field
- offset 129: 64-byte port field

Observed writes include host bytes at `0x2e8eb`, host termination at `0x2e904`, port bytes at `0x2e924`, and ASCII `'1'` used marking at `0x2e938`. The table lies in virtual, non-file-backed `.data`, so it is runtime-populated rather than an embedded endpoint table.

The writer has one direct caller, RVA `0x1c7e4`; the caller pushes the value loaded from `0x139b758`.

## Binary facts — endpoint consumption

Selected-server index global: RVA `0x5c860`.

Getter RVA `0x2e950` resolves one of the ten records. The single game connection path then reaches:

- `socket`: callsite RVA `0x2eeaa`
- `htons`: `0x2ef2e`
- `inet_addr`: `0x2ef3d`
- DNS fallback `gethostbyname`: `0x2ef50`
- `connect`: `0x2efa4`

This sequence is the direct host/port-to-Winsock join.

## Binary facts — retail launcher

`StoneAge.exe` has exactly one `CreateProcessA` business call, RVA `0x43c3`.

Immediately before that call the launcher constructs a command line with a 17-string `%s` format. Static construction fragments in the same path include:

- `realbin:%d`
- `adrnbin:%d`
- `sprbin:%d`
- `spradrnbin:%d`
- `updated`
- `sa_%d.exe`
- `%ssa_%d.exe`

This independently matches the runtime startup-token family and establishes the updater/launcher -> process-command-line handoff architecture.

Literal `IP:` is not statically embedded in the launcher image. Its dynamic source before final launch-string assembly therefore remains open.

## waei.bin and WGS boundary

The runtime has a separate `waei.bin` string reference, but its exact bounded graph does not join the proven server-table or Winsock endpoint path, and the retail disc itself contains no `waei.bin`. It is not used as an explanation for the proven endpoint source.

The v1.0 runtime exposes only one business call each for `socket`, `htons`, `inet_addr`, `gethostbyname`, and `connect` in the recovered endpoint path. No separate pre-connect WGS server-list socket path has been observed in the accepted binary.

## Descendant control

Pinned descendant source `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876` later assigns WinMain `lpCmdLine` to `CmdLine` and parses the same resource/display token family. Its later `GameServer` and WGS implementations also provide semantic controls for server records. These sources are lineage controls only; the addresses, table dimensions and endpoint path above are independently recovered from the Taiwan v1.0 binaries.

## Reconstruction consequence

For the planned single-player rebuild, the historically meaningful result is the boundary:

`launcher/startup parameters -> runtime server table -> game connection`.

The exact historical billing/operator mechanism upstream of the dynamic endpoint string is not needed for the reconstructed single-player game. Game-owned data and mechanics that originally arrived over the game connection remain relevant and are handled separately through protocol/data archaeology.

Derived evidence: `research/recovered/STONEAGE-TW10-SERVER-SELECTION-R1.txt`.
