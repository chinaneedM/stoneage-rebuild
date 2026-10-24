# Early official client original-byte acquisition: bounded live endpoint qualification R1

**2026-10-24 — EARLY-OFFICIAL-CLIENT-ORIGINAL-PAYLOAD-QUALIFICATION-02** (FACT / OPEN). This is an official-client **source access** experiment, not gameplay or pet/NPC completion.

## Newly executed research scope

Use original, independently pinned Korean Inium-era distribution leads, **not** unauthenticated modern private-server clients:

| Distribution evidence | Historical URL | Source scope |
|---|---|---|
| Hananet STAD 8119 formal/full | http://stoneage.hananet.net/down/sa.exe | Archived 2001-08-14 commented button, 260M catalog entry |
| Hananet STAD 8120 demo/trial | http://stoneage.hananet.net/down/sa_demo.exe | Archived commented button, 240M catalog entry |
| CNET Korea Software_Id 200009263856 | http://korea.cnet.com/pc/games/online/stoneage.zip | Inium official November 2000 mirror catalog |
| Gagamel mirror on Inium official download page | http://www.gagamel.com/web_data/download/stoneagebeta.zip | Inium 2001 formal-version mirror list; filename `beta` not trial proof |

Original provenance is already pinned in `research/clients/STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md` and `research/recovered/STONEAGE-CLIENT-NAMED-ENTITY-PRIMARY-SOURCE-GAP-R1.json`. Do **not** treat catalog names and size approximations as downloaded original bytes.

## Reproducible test

`python -m unittest tests.test_stoneage_early_official_payload_probe -v` runs without network. `python -m tools.stoneage_early_official_payload_probe --output result.json` attempts one bounded 4096-byte Range GET for each historical address. Each entry independently reports timestamp at batch level, HTTP result, final URL, type, content range, length and SHA256 of the **sample only**, and prefix magic. Redirects to a different host are rejected; local/private targets are blocked. A 200 error document, HTML page, modern redirected site or executable prefix is **not** original-client qualification.

The dedicated Actions workflow publishes **metadata JSON only**, never executable binaries, client sprites or server databases. Its attempt outcomes must be read from a real completed Actions run before changing any source status. The script sets `complete_original_sha256=null`, and **all** claims of a complete client, specific build, original publisher purity and named entity↔bitmap ID remain false until a separately verified full download and extraction.

## Gate and stop condition

If an actual binary prefix is found, acquire **complete original bytes** off-repository and calculate full SHA256, file tree, client resource containers, build identity, contamination signs, and original source chain before entering cross-version comparison. If all four original endpoints are unreachable/HTML, record their exact statuses; **do not** repeat old CNET Wayback 16 zero-hit requests or infer global unavailability. Switch to a distinct authentic physical carrier such as the attested Korean 2001 GameTime guide CD, or another material map/NPC source domain per the continuity protocol. Historic JSS 1999 remains an independent unacquired original disc.

The project retains DD-029 content-addressed file deduplication with per-version occurrences, DD-028 separate base/permanent/operator-event/unknown quest categories, and R79 savedata paused. No overall completion percentage is derivable.
