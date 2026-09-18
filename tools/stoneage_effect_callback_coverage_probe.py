#!/usr/bin/env python3
"""Cross-check recovered StoneAge effect callback tokens against fixed source dispatch tables.

This probe intentionally emits only aggregate coverage counts and classification hashes.
It does not publish original item/magic/pet-skill names, callback tokens, or table rows.
"""

import argparse
import collections
import hashlib
import re
from pathlib import Path

ITEM_COMMON_FAMILY = {
    "ITEM_useRecovery": "battle_recovery",
    "ITEM_useStatusChange": "battle_status_apply",
    "ITEM_useStatusRecovery": "battle_status_recover",
    "ITEM_useMagicDef": "battle_defense",
    "ITEM_useParamChange": "battle_param",
    "ITEM_useFieldChange": "battle_field_attribute",
    "ITEM_useAttReverse": "battle_attribute_reverse",
    "ITEM_useRessurect": "battle_resurrection",
    "ITEM_useCaptureUp": "battle_capture",
    "ITEM_useWarp": "warp",
    "ITEM_petFollow": "pet_follow",
    "ITEM_useNoenemy": "encounter_suppress",
    "ITEM_equipNoenemy": "equipment_encounter_control",
    "ITEM_remNoenemy": "equipment_encounter_control",
    "ITEM_useEncounter": "encounter_force",
    "ITEM_useMic": "mic_toggle",
    "ITEM_dropMic": "mic_toggle",
    "ITEM_useRenameItem": "rename_ui",
    "ITEM_pickupDice": "dice_ui",
    "ITEM_dropDice": "dice_ui",
    "ITEM_initLottery": "lottery_ui",
    "ITEM_useLottery": "lottery_ui",
    "ITEM_useSkup": "skillup_point",
    "ITEM_AddPRSkillPoint": "profession_macro_shell",
    "ITEM_AddPRSkillPercent": "profession_macro_shell",
    "ITEM_changePetOwner": "pet_owner_release",
    "ITEM_useEffectTohelos": "tohelos_effect",
    "ITEM_DeleteByWatched": "lifecycle",
    "ITEM_DeleteTimeWatched": "lifecycle",
    "ITEM_WearEquip": "equipment_hook",
    "ITEM_ReWearEquip": "equipment_hook",
}

ITEM_CALLBACK_COLUMNS = {
    "initfunc": 6,
    "preoverfunc": 7,
    "postoverfunc": 8,
    "watchfunc": 9,
    "usefunc": 10,
    "attachfunc": 11,
    "detachfunc": 12,
    "dropfunc": 13,
    "pickupfunc": 14,
    "relifefunc": 15,
}


def clean_csv_rows(path):
    rows = []
    if not path or not path.exists():
        return rows
    for raw in path.read_bytes().splitlines():
        line = raw.strip()
        if not line or line.startswith(b"#"):
            continue
        rows.append([x.strip() for x in line.replace(b"\t", b" ").split(b",")])
    return rows


def setup_entries(path):
    out = {}
    if not path or not path.exists():
        return out
    for raw in path.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        k, v = line.split(b"=", 1)
        key = k.decode("ascii", "ignore").strip().lower()
        value = v.decode("utf-8", "replace").strip()
        out[key] = value
    return out


def basename(value):
    return Path(value.replace("\\", "/")).name if value else ""


def choose_active_file(data_dir, setup, *, kind):
    entries = setup_entries(setup)
    if kind == "item":
        names = [
            basename(v)
            for k, v in entries.items()
            if k.startswith("itemset") and basename(v).lower().startswith("itemset")
        ]
        default = "itemset.txt"
    elif kind == "magic":
        names = [basename(entries.get("magicfile", ""))]
        default = "magic.txt"
    elif kind == "petskill":
        names = [
            basename(v)
            for k, v in entries.items()
            if k in {"petskillfile1", "petskillfile2"}
        ]
        default = "petskill.txt"
    else:
        raise ValueError("unknown kind")

    names = [x for x in names if x]
    if names:
        chosen = collections.Counter(x.lower() for x in names).most_common(1)[0][0]
        for p in data_dir.iterdir():
            if p.is_file() and p.name.lower() == chosen:
                return p
    return data_dir / default


def token_text(raw):
    return raw.decode("utf-8", "replace").strip()


def item_callback_counters(path):
    rows = clean_csv_rows(path)
    out = {name: collections.Counter() for name in ITEM_CALLBACK_COLUMNS}
    for row in rows:
        for name, idx in ITEM_CALLBACK_COLUMNS.items():
            if idx < len(row) and row[idx]:
                out[name][token_text(row[idx])] += 1
    return rows, out


def single_callback_counter(path, column=2):
    rows = clean_csv_rows(path)
    out = collections.Counter()
    for row in rows:
        if column < len(row) and row[column]:
            out[token_text(row[column])] += 1
    return rows, out


def strip_c_comments(text):
    """Remove C/C++ comments while preserving quoted string contents and newlines."""
    out = []
    i = 0
    state = "code"
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if state == "code":
            if ch == '"':
                out.append(ch)
                state = "string"
                i += 1
                continue
            if ch == "/" and nxt == "/":
                state = "line_comment"
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block_comment"
                i += 2
                continue
            out.append(ch)
            i += 1
            continue

        if state == "string":
            out.append(ch)
            if ch == "\\" and i + 1 < len(text):
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue

        if state == "line_comment":
            if ch == "\n":
                out.append("\n")
                state = "code"
            i += 1
            continue

        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                i += 2
                continue
            if ch == "\n":
                out.append("\n")
            i += 1
            continue

    return "".join(out)


def extract_table_region(text, marker):
    pos = text.find(marker)
    if pos < 0:
        raise ValueError(f"missing source table marker: {marker}")
    end = text.find("\n};", pos)
    if end < 0:
        end = text.find("\r\n};", pos)
    if end < 0:
        raise ValueError(f"unterminated source table: {marker}")
    return text[pos:end]


def parse_global_function_table(path):
    text = strip_c_comments(path.read_text(encoding="utf-8", errors="replace"))
    region = extract_table_region(text, "correspondStringAndFunctionTable[]")
    return set(re.findall(r'\{\s*\{\s*"([^"]+)"\s*\}', region))


def parse_named_function_table(path, marker):
    text = strip_c_comments(path.read_text(encoding="utf-8", errors="replace"))
    markers = (marker,) if isinstance(marker, str) else tuple(marker)
    last_error = None
    for candidate in markers:
        try:
            region = extract_table_region(text, candidate)
            return set(re.findall(r'\{\s*"([^"]+)"', region))
        except ValueError as exc:
            last_error = exc
    raise last_error or ValueError("no source table marker supplied")

def parse_global_function_guard_map(path):
    """Return token -> guarded(bool) for the global string/function registry."""
    text = strip_c_comments(path.read_text(encoding="utf-8", errors="replace"))
    region = extract_table_region(text, "correspondStringAndFunctionTable[]")
    stack = []
    out = {}
    for line in region.splitlines():
        stripped = line.strip()
        if re.match(r"^#\s*(if|ifdef|ifndef)\b", stripped):
            stack.append(stripped)
            continue
        if re.match(r"^#\s*(elif|else)\b", stripped):
            if stack:
                stack[-1] = stripped
            continue
        if re.match(r"^#\s*endif\b", stripped):
            if stack:
                stack.pop()
            continue
        m = re.search(r'\{\s*\{\s*"([^"]+)"', line)
        if m:
            out[m.group(1)] = bool(stack)
    return out


def parse_named_function_guard_map(path, marker):
    """Return token -> guarded(bool) for one named dispatch table."""
    text = strip_c_comments(path.read_text(encoding="utf-8", errors="replace"))
    markers = (marker,) if isinstance(marker, str) else tuple(marker)
    last_error = None
    region = None
    for candidate in markers:
        try:
            region = extract_table_region(text, candidate)
            break
        except ValueError as exc:
            last_error = exc
    if region is None:
        raise last_error or ValueError("no source table marker supplied")

    stack = []
    out = {}
    for line in region.splitlines():
        stripped = line.strip()
        if re.match(r"^#\s*(if|ifdef|ifndef)\b", stripped):
            stack.append(stripped)
            continue
        if re.match(r"^#\s*(elif|else)\b", stripped):
            if stack:
                stack[-1] = stripped
            continue
        if re.match(r"^#\s*endif\b", stripped):
            if stack:
                stack.pop()
            continue
        m = re.search(r'\{\s*"([^"]+)"', line)
        if m:
            out[m.group(1)] = bool(stack)
    return out


def _matching_brace_end(text, open_pos):
    depth = 0
    state = "code"
    i = int(open_pos)
    while i < len(text):
        ch = text[i]
        if state == "string":
            if ch == "\\" and i + 1 < len(text):
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue
        if state == "char":
            if ch == "\\" and i + 1 < len(text):
                i += 2
                continue
            if ch == "'":
                state = "code"
            i += 1
            continue
        if ch == '"':
            state = "string"
            i += 1
            continue
        if ch == "'":
            state = "char"
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def parse_item_function_body_map(path, tokens):
    """Classify whether item callback bodies contain unguarded substantive code."""
    text = strip_c_comments(path.read_text(encoding="utf-8", errors="replace"))
    out = {}
    for token in sorted(set(tokens)):
        pattern = re.compile(
            r"(?m)^[ \t]*(?:static[ \t]+)?(?:void|int|BOOL|char|long)[ \t\r\n*]+"
            + re.escape(token)
            + r"[ \t\r\n]*\("
        )
        m = pattern.search(text)
        if not m:
            out[token] = {"present": False, "unguarded_substantive": False}
            continue
        open_pos = text.find("{", m.end())
        if open_pos < 0:
            out[token] = {"present": False, "unguarded_substantive": False}
            continue
        end_pos = _matching_brace_end(text, open_pos)
        if end_pos is None:
            out[token] = {"present": False, "unguarded_substantive": False}
            continue
        body = text[open_pos + 1 : end_pos]
        stack = []
        unguarded_lines = 0
        guarded_lines = 0
        for raw in body.splitlines():
            stripped = raw.strip()
            if not stripped:
                continue
            if re.match(r"^#\s*(if|ifdef|ifndef)\b", stripped):
                stack.append(stripped)
                continue
            if re.match(r"^#\s*(elif|else)\b", stripped):
                if stack:
                    stack[-1] = stripped
                continue
            if re.match(r"^#\s*endif\b", stripped):
                if stack:
                    stack.pop()
                continue
            semantic = stripped.replace("{", "").replace("}", "").strip()
            if not semantic:
                continue
            if stack:
                guarded_lines += 1
            else:
                unguarded_lines += 1
        out[token] = {
            "present": True,
            "unguarded_substantive": unguarded_lines > 0,
            "unguarded_lines": unguarded_lines,
            "guarded_lines": guarded_lines,
        }
    return out


def merge_item_function_body_maps(paths, tokens):
    """Merge callback body evidence across the ordinary item source modules."""
    merged = {
        token: {
            "present": False,
            "unguarded_substantive": False,
            "unguarded_lines": 0,
            "guarded_lines": 0,
        }
        for token in set(tokens)
    }
    for path in paths:
        if path is None:
            continue
        current = parse_item_function_body_map(path, tokens)
        for token, state in current.items():
            if not state.get("present"):
                continue
            dst = merged[token]
            dst["present"] = True
            dst["unguarded_substantive"] = (
                dst["unguarded_substantive"] or state.get("unguarded_substantive", False)
            )
            dst["unguarded_lines"] += int(state.get("unguarded_lines", 0))
            dst["guarded_lines"] += int(state.get("guarded_lines", 0))
    return merged


def item_body_coverage(counter, dispatch_maps, body_maps):
    """Refine all-three unguarded item dispatch candidates by function-body evidence."""
    lineages = tuple(sorted(dispatch_maps))
    unique = collections.Counter()
    rows = collections.Counter()
    digest = hashlib.sha256()
    for token in sorted(counter):
        if not all(
            token in dispatch_maps[name] and not dispatch_maps[name][token]
            for name in lineages
        ):
            continue
        states = []
        for name in lineages:
            body = body_maps[name].get(token, {})
            if not body.get("present"):
                states.append("missing")
            elif body.get("unguarded_substantive"):
                states.append("stable")
            else:
                states.append("macro_shell")
        if all(s == "stable" for s in states):
            label = "stable_body_all3"
        elif all(s == "macro_shell" for s in states):
            label = "macro_shell_all3"
        elif "missing" in states:
            label = "partial_body_source"
        else:
            label = "mixed_body_guard"
        unique[label] += 1
        rows[label] += counter[token]
        digest.update((token + "|" + "|".join(states) + "\n").encode("utf-8"))
    return {
        "unique_counts": unique,
        "row_counts": rows,
        "classification_sha256": digest.hexdigest(),
    }


def common_unguarded_family_counts(counter, lineage_maps, family_map=ITEM_COMMON_FAMILY):
    """Aggregate active tokens that are unguarded in every fixed source lineage."""
    lineages = tuple(sorted(lineage_maps))
    unique = collections.Counter()
    rows = collections.Counter()
    covered_tokens = set()
    for token, count in counter.items():
        if all(
            token in lineage_maps[name] and not lineage_maps[name][token]
            for name in lineages
        ):
            family = family_map.get(token, "unclassified")
            unique[family] += 1
            rows[family] += count
            covered_tokens.add(token)
    return {
        "unique": unique,
        "rows": rows,
        "covered_unique": len(covered_tokens),
        "covered_rows": sum(counter[t] for t in covered_tokens),
    }


def guard_coverage(counter, lineage_maps):
    lineages = tuple(sorted(lineage_maps))
    unique_counts = collections.Counter()
    row_counts = collections.Counter()
    digest = hashlib.sha256()

    for token in sorted(counter):
        states = []
        for lineage in lineages:
            mapping = lineage_maps[lineage]
            if token not in mapping:
                states.append("missing")
            else:
                states.append("guarded" if mapping[token] else "unguarded")

        if all(s == "unguarded" for s in states):
            label = "unguarded_all3"
        elif all(s == "guarded" for s in states):
            label = "guarded_all3"
        elif all(s != "missing" for s in states):
            label = "mixed_guard"
        elif all(s == "missing" for s in states):
            label = "missing_all3"
        else:
            label = "partial_source"

        unique_counts[label] += 1
        row_counts[label] += counter[token]
        digest.update((token + "|" + "|".join(states) + "\n").encode("utf-8"))

    return {
        "unique_counts": unique_counts,
        "row_counts": row_counts,
        "classification_sha256": digest.hexdigest(),
    }


def source_dispatch_sets(args):
    return {
        "gavin": {
            "item": parse_global_function_table(args.gavin_function),
            "magic": parse_named_function_table(args.gavin_magic, "MAGIC_functbl[]"),
            "petskill": parse_named_function_table(args.gavin_petskill, "PETSKILL_functbl[]"),
        },
        "iris": {
            "item": parse_global_function_table(args.iris_function),
            "magic": parse_named_function_table(args.iris_magic, "MAGIC_functbl[]"),
            "petskill": parse_named_function_table(args.iris_petskill, "PETSKILL_functbl[]"),
        },
        "bismarck": {
            "item": parse_global_function_table(args.bismarck_function),
            "magic": parse_named_function_table(args.bismarck_magic, ("sMageicFunctionTable[]", "MAGIC_functbl[]")),
            "petskill": parse_named_function_table(args.bismarck_petskill, "PETSKILL_functbl[]"),
        },
    }


def coverage(counter, lineage_sets):
    tokens = set(counter)
    lineages = tuple(sorted(lineage_sets))
    cls = collections.Counter()
    row_cls = collections.Counter()
    per = {}
    digest = hashlib.sha256()

    for token in sorted(tokens):
        mask = tuple(int(token in lineage_sets[name]) for name in lineages)
        matched = sum(mask)
        label = "all" if matched == len(lineages) else ("none" if matched == 0 else "some")
        cls[label] += 1
        row_cls[label] += counter[token]
        digest.update((token + "|" + "".join(map(str, mask)) + "\n").encode("utf-8"))

    for name in lineages:
        matched_tokens = [t for t in tokens if t in lineage_sets[name]]
        per[name] = {
            "unique_matched": len(matched_tokens),
            "row_uses_matched": sum(counter[t] for t in matched_tokens),
            "declared_dispatch_tokens": len(lineage_sets[name]),
        }

    return {
        "unique": len(tokens),
        "row_uses": sum(counter.values()),
        "classes": cls,
        "row_classes": row_cls,
        "per": per,
        "classification_sha256": digest.hexdigest(),
    }


def analyze(args):
    sources = source_dispatch_sets(args)
    item_path = choose_active_file(args.data_dir, args.setup, kind="item")
    magic_path = choose_active_file(args.data_dir, args.setup, kind="magic")
    petskill_path = choose_active_file(args.data_dir, args.setup, kind="petskill")

    item_rows, item_slots = item_callback_counters(item_path)
    magic_rows, magic_tokens = single_callback_counter(magic_path, 2)
    petskill_rows, petskill_tokens = single_callback_counter(petskill_path, 2)

    item_sets = {name: s["item"] for name, s in sources.items()}
    magic_sets = {name: s["magic"] for name, s in sources.items()}
    petskill_sets = {name: s["petskill"] for name, s in sources.items()}
    item_guard_maps = {
        "gavin": parse_global_function_guard_map(args.gavin_function),
        "iris": parse_global_function_guard_map(args.iris_function),
        "bismarck": parse_global_function_guard_map(args.bismarck_function),
    }
    item_body_maps = None
    if all(
        getattr(args, name, None)
        for name in ("gavin_item_body", "iris_item_body", "bismarck_item_body")
    ):
        active_item_tokens = set().union(*(set(counter) for counter in item_slots.values()))
        item_body_maps = {
            "gavin": merge_item_function_body_maps(
                (args.gavin_item_body, getattr(args, "gavin_item_battle_body", None)),
                active_item_tokens,
            ),
            "iris": merge_item_function_body_maps(
                (args.iris_item_body, getattr(args, "iris_item_battle_body", None)),
                active_item_tokens,
            ),
            "bismarck": merge_item_function_body_maps(
                (args.bismarck_item_body, getattr(args, "bismarck_item_battle_body", None)),
                active_item_tokens,
            ),
        }

    magic_guard_maps = {
        "gavin": parse_named_function_guard_map(args.gavin_magic, "MAGIC_functbl[]"),
        "iris": parse_named_function_guard_map(args.iris_magic, "MAGIC_functbl[]"),
        "bismarck": parse_named_function_guard_map(
            args.bismarck_magic,
            ("sMageicFunctionTable[]", "MAGIC_functbl[]"),
        ),
    }

    return {
        "paths": {
            "item": item_path,
            "magic": magic_path,
            "petskill": petskill_path,
        },
        "row_counts": {
            "item": len(item_rows),
            "magic": len(magic_rows),
            "petskill": len(petskill_rows),
        },
        "item_slots": {
            slot: coverage(counter, item_sets)
            for slot, counter in item_slots.items()
        },
        "item_slot_guards": {
            slot: guard_coverage(counter, item_guard_maps)
            for slot, counter in item_slots.items()
        },
        "item_slot_common_families": {
            slot: common_unguarded_family_counts(counter, item_guard_maps)
            for slot, counter in item_slots.items()
        },
        "item_slot_bodies": (
            {
                slot: item_body_coverage(counter, item_guard_maps, item_body_maps)
                for slot, counter in item_slots.items()
            }
            if item_body_maps is not None else None
        ),
        "item_use_guard": guard_coverage(item_slots["usefunc"], item_guard_maps),
        "item_use_common_families": common_unguarded_family_counts(
            item_slots["usefunc"], item_guard_maps
        ),
        "item_use_body": (
            item_body_coverage(item_slots["usefunc"], item_guard_maps, item_body_maps)
            if item_body_maps is not None else None
        ),
        "magic": coverage(magic_tokens, magic_sets),
        "magic_guard": guard_coverage(magic_tokens, magic_guard_maps),
        "petskill": coverage(petskill_tokens, petskill_sets),
    }


def emit_coverage(prefix, result):
    print(f"{prefix}|unique_tokens={result['unique']}|row_uses={result['row_uses']}|"
          f"all3_unique={result['classes'].get('all',0)}|"
          f"some_unique={result['classes'].get('some',0)}|"
          f"none_unique={result['classes'].get('none',0)}|"
          f"all3_rows={result['row_classes'].get('all',0)}|"
          f"some_rows={result['row_classes'].get('some',0)}|"
          f"none_rows={result['row_classes'].get('none',0)}|"
          f"classification_sha256={result['classification_sha256']}")
    for lineage, p in sorted(result["per"].items()):
        print(f"{prefix}_LINEAGE|{lineage}|declared_dispatch_tokens={p['declared_dispatch_tokens']}|"
              f"unique_matched={p['unique_matched']}|row_uses_matched={p['row_uses_matched']}")


def emit(args):
    r = analyze(args)
    print("StoneAge recovered effect-callback coverage probe — R1")
    print("No original names, callback tokens, descriptions, options, or data rows are stored in this report.")
    print("COVERAGE_BOUNDARY|declared fixed-source dispatch tables; preprocessor presence is not compiled-active proof")
    for kind in ("item", "magic", "petskill"):
        print(f"ACTIVE_FILE|{kind}|{r['paths'][kind].name}|rows={r['row_counts'][kind]}")
    for slot, result in r["item_slots"].items():
        emit_coverage(f"ITEM_SLOT|{slot}", result)
    for slot in ("attachfunc", "detachfunc", "dropfunc", "pickupfunc", "relifefunc"):
        sg = r["item_slot_guards"][slot]
        for label in (
            "unguarded_all3",
            "guarded_all3",
            "mixed_guard",
            "partial_source",
            "missing_all3",
        ):
            print(
                f"ITEM_SLOT_GUARD_CLASS|{slot}|{label}|"
                f"unique_tokens={sg['unique_counts'].get(label,0)}|"
                f"row_uses={sg['row_counts'].get(label,0)}"
            )
        sb_all = r.get("item_slot_bodies")
        if sb_all is not None:
            sb = sb_all[slot]
            for label in (
                "stable_body_all3",
                "macro_shell_all3",
                "mixed_body_guard",
                "partial_body_source",
            ):
                print(
                    f"ITEM_SLOT_BODY_CLASS|{slot}|{label}|"
                    f"unique_tokens={sb['unique_counts'].get(label,0)}|"
                    f"row_uses={sb['row_counts'].get(label,0)}"
                )
        sf = r["item_slot_common_families"][slot]
        print(
            f"ITEM_SLOT_COMMON_FAMILY_TOTAL|{slot}|"
            f"unique_tokens={sf['covered_unique']}|row_uses={sf['covered_rows']}"
        )
        for family in sorted(set(sf["unique"]) | set(sf["rows"])):
            print(
                f"ITEM_SLOT_COMMON_FAMILY|{slot}|{family}|"
                f"unique_tokens={sf['unique'].get(family,0)}|"
                f"row_uses={sf['rows'].get(family,0)}"
            )
    ig = r["item_use_guard"]
    labels = (
        "unguarded_all3",
        "guarded_all3",
        "mixed_guard",
        "partial_source",
        "missing_all3",
    )
    for label in labels:
        print(
            f"ITEM_USE_GUARD_CLASS|{label}|"
            f"unique_tokens={ig['unique_counts'].get(label,0)}|"
            f"row_uses={ig['row_counts'].get(label,0)}"
        )
    print(f"ITEM_USE_GUARD_CLASSIFICATION_SHA256|{ig['classification_sha256']}")
    fam = r["item_use_common_families"]
    print(
        f"ITEM_USE_COMMON_FAMILY_TOTAL|unique_tokens={fam['covered_unique']}|"
        f"row_uses={fam['covered_rows']}"
    )
    for family in sorted(set(fam["unique"]) | set(fam["rows"])):
        print(
            f"ITEM_USE_COMMON_FAMILY|{family}|"
            f"unique_tokens={fam['unique'].get(family,0)}|"
            f"row_uses={fam['rows'].get(family,0)}"
        )
    ib = r.get("item_use_body")
    if ib is not None:
        for label in (
            "stable_body_all3",
            "macro_shell_all3",
            "mixed_body_guard",
            "partial_body_source",
        ):
            print(
                f"ITEM_USE_BODY_CLASS|{label}|"
                f"unique_tokens={ib['unique_counts'].get(label,0)}|"
                f"row_uses={ib['row_counts'].get(label,0)}"
            )
        print(f"ITEM_USE_BODY_CLASSIFICATION_SHA256|{ib['classification_sha256']}")
    emit_coverage("MAGIC", r["magic"])
    g = r["magic_guard"]
    labels = (
        "unguarded_all3",
        "guarded_all3",
        "mixed_guard",
        "partial_source",
        "missing_all3",
    )
    for label in labels:
        print(
            f"MAGIC_GUARD_CLASS|{label}|"
            f"unique_tokens={g['unique_counts'].get(label,0)}|"
            f"row_uses={g['row_counts'].get(label,0)}"
        )
    print(f"MAGIC_GUARD_CLASSIFICATION_SHA256|{g['classification_sha256']}")
    emit_coverage("PETSKILL", r["petskill"])


def add_source_args(ap, prefix):
    ap.add_argument(f"--{prefix}-function", type=Path, required=True)
    ap.add_argument(f"--{prefix}-item-body", type=Path)
    ap.add_argument(f"--{prefix}-item-battle-body", type=Path)
    ap.add_argument(f"--{prefix}-magic", type=Path, required=True)
    ap.add_argument(f"--{prefix}-petskill", type=Path, required=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    for prefix in ("gavin", "iris", "bismarck"):
        add_source_args(ap, prefix)
    args = ap.parse_args()
    emit(args)


if __name__ == "__main__":
    main()
