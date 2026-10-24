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

## Verified execution result — 2026-10-24

Candidate CI run [40102349701](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40102349701), head `770b948a89aaaa4b3d6a122264d8c8511fc1b9ba`, job `120896914256`: completed/success for offline gate, bounded network probe and derived JSON upload. Its actual log prints one report with timestamp `2026-10-24T14:24:37.717228+00:00`. Results: STAD 8119 formal `URLError` and no HTTP status; STAD 8120 trial `URLError` and no HTTP status; CNET exact `URLError` and no HTTP status; Gagamel exact `HTTP 441`, zero sample. All four downloaded zero sample bytes and had no full payload or original SHA. Do not infer HTTP status for the three request-level errors, nor blame them on historical site removal without DNS/TLS evidence. A 441 response is not a client nor necessarily an origin server status.

Derived metadata-only Actions artifact `12562948821` is 1,075-byte ZIP, upload-log/API digest `53715dbd672bdb058c12420492053146355bcbc5879f959af42f470b120af021`, not independently downloaded and rehashed in this milestone. The logged JSON is now archived in `research/recovered/STONEAGE-EARLY-OFFICIAL-PAYLOAD-PROBE-R1.json`, alongside the provenance and interpretation. The original proprietary installers were **not recovered or committed**.

**Finite stop:** Retire repeated live-HTTP requests to these same four historical URLs without a new independently verified mirror or preservation snapshot. Next priority is `CLIENT-ORIGINAL-PHYSICAL-CARRIER-RECOVERY-03`: source actual Korean 2001 GameTime guide bonus CD, Korean Inium retail CD or 1999 JSS original retail game CD as *lossless original bytes*, then SHA/tree/build/clean-room provenance and cross-version dedup. The source record for the first specifically attests a game installer and demo disc, but its physical existence and online availability are separate from actual acquisition. If none can be obtained in a bounded unit, stop search-only churn and switch to a concrete map/NPC master-content domain under continuity §13. No overall restoration progress percent is justified.
