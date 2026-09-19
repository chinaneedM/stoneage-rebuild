#!/usr/bin/env python3
"""Aggregate recovered Quiz NPC/config shapes without preserving payload text, IDs or coordinates."""

import argparse
import collections
import hashlib
from pathlib import Path

TEMPLATE_MAGIC = b"NPCTEMPLATE"
CREATE_MAGIC = b"NPCCREATE"
KEYS = (
    b"StartMsg", b"Quiznum", b"EntryItem", b"EntryStone", b"NoEntryMsg",
    b"ItemFullMsg", b"GetItem", b"Border", b"FailureMsg", b"Warp",
    b"Party", b"Type", b"Answer", b"Level", b"Scope",
)


def source_candidate(path):
    n = path.name.lower()
    return not (
        path.name.endswith("~") or path.name.startswith("#") or n.endswith(".bak")
    )


def magic_kind(path):
    if not source_candidate(path):
        return None
    try:
        with path.open("rb") as f:
            first = f.readline().rstrip(b"\r\n")
    except OSError:
        return None
    if first == TEMPLATE_MAGIC:
        return "template"
    if first == CREATE_MAGIC:
        return "create"
    return None


def iter_blocks(path):
    block = None
    with path.open("rb") as f:
        next(f, b"")
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            if line.startswith(b"{"):
                block = []
                continue
            if line.startswith(b"}"):
                if block is not None:
                    yield block
                block = None
                continue
            if block is None or b"=" not in line:
                continue
            key, value = line.split(b"=", 1)
            block.append((key.strip().lower(), value.strip()))


def template_names(files):
    """Return stable Quiz template names and mixed-definition ambiguities.

    The server resolves duplicate template names by the first loaded match.
    For a payload-free deterministic probe we can safely accept a duplicate
    name only when every surviving definition selects Quiz.  Mixed duplicate
    definitions remain explicit load-order ambiguity rather than being guessed.
    """
    mapping = collections.defaultdict(list)
    for path in files:
        for entries in iter_blocks(path):
            d = dict(entries)
            name = d.get(b"templatename")
            if name:
                mapping[name].append(d.get(b"functionset", b""))
    stable = {
        name
        for name, defs in mapping.items()
        if defs and all(functionset == b"Quiz" for functionset in defs)
    }
    ambiguous = {
        name
        for name, defs in mapping.items()
        if any(functionset == b"Quiz" for functionset in defs)
        and not all(functionset == b"Quiz" for functionset in defs)
    }
    duplicate_stable = {
        name for name in stable if len(mapping[name]) > 1
    }
    return stable, ambiguous, duplicate_stable


def refs(files):
    for path in files:
        for entries in iter_blocks(path):
            for key, value in entries:
                if key != b"enemy":
                    continue
                name, sep, arg = value.partition(b"|")
                yield name.strip(), arg if sep else b""


def assigned_file(arg):
    for token in arg.split(b"|"):
        if b"file" not in token.lower():
            continue
        parts = token.split(b":", 1)
        if len(parts) == 2:
            return parts[1].decode("utf-8", "replace").strip()
    return None


def merge_file(path):
    out = b""
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            if out and not out.endswith(b"|"):
                out += b"|"
            out += line
    return out


def field(data, key):
    target = key.lower()
    for token in data.split(b"|"):
        parts = token.split(b":", 1)
        if len(parts) == 2 and parts[0].strip().lower() == target:
            return parts[1].strip()
    return None


def csv(value):
    if value is None or value == b"":
        return []
    return [x.strip() for x in value.split(b",")]


def atoi(value):
    s = value.lstrip()
    sign = 1
    if s[:1] in (b"+", b"-"):
        sign = -1 if s[:1] == b"-" else 1
        s = s[1:]
    n = 0
    found = False
    for ch in s:
        if not 48 <= ch <= 57:
            break
        found = True
        n = n * 10 + ch - 48
    return sign * n if found else 0


def entry_item_shape(value):
    tokens = csv(value)
    plain = 0
    starred = 0
    quantities = []
    for token in tokens:
        if b"*" in token:
            starred += 1
            _item, count = token.split(b"*", 1)
            quantities.append(atoi(count))
        else:
            plain += 1
    return len(tokens), plain, starred, tuple(quantities)


def pair_shape(value):
    tokens = csv(value)
    return len(tokens) // 2, len(tokens) % 2


def analyze_questions(path):
    result = {
        "present": bool(path and path.is_file()),
        "aggregate": "",
        "rows": 0,
        "arity": collections.Counter(),
        "type": collections.Counter(),
        "level": collections.Counter(),
        "answer_type": collections.Counter(),
        "answer_no": collections.Counter(),
    }
    if not result["present"]:
        return result

    digest = hashlib.sha256()
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            digest.update(hashlib.sha256(line).digest())
            parts = [x.strip() for x in line.split(b",")]
            result["rows"] += 1
            result["arity"][len(parts)] += 1
            if len(parts) >= 5:
                result["type"][atoi(parts[1])] += 1
                result["level"][atoi(parts[2])] += 1
                result["answer_type"][atoi(parts[3])] += 1
                result["answer_no"][atoi(parts[4])] += 1
    result["aggregate"] = digest.hexdigest()
    return result


def analyze(npc_dir, question_file=None):
    files = sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p: str(p).lower(),
    )
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    names, ambiguous_names, duplicate_stable_names = template_names(templates)

    counts = collections.Counter()
    counts["stable_quiz_template_names"] = len(names)
    counts["duplicate_stable_quiz_template_names"] = len(duplicate_stable_names)
    counts["ambiguous_mixed_quiz_template_names"] = len(ambiguous_names)
    keys = collections.Counter()
    item_shapes = collections.Counter()
    quantities = collections.Counter()
    pair_shapes = collections.Counter()
    reward_candidate_arity = collections.Counter()
    warp_destination_arity = collections.Counter()
    scalar_shapes = collections.Counter()
    aggregate = hashlib.sha256()

    for name, arg in refs(creates):
        if name in ambiguous_names:
            counts["ambiguous_mixed_template_refs"] += 1
            continue
        if name not in names:
            continue
        counts["refs"] += 1
        filename = assigned_file(arg)
        if filename is not None:
            path = npc_dir / filename
            if not path.is_file():
                counts["missing_files"] += 1
                continue
            data = merge_file(path)
            counts["resolved_files"] += 1
        else:
            data = arg
            counts["inline"] += 1

        aggregate.update(
            str(len(data)).encode()
            + b"|"
            + hashlib.sha256(data).hexdigest().encode()
            + b"\n"
        )

        for key in KEYS:
            value = field(data, key)
            if value is not None:
                keys[key.decode("ascii")] += 1

        entry_item = field(data, b"EntryItem")
        if entry_item is not None:
            total, plain, starred, qs = entry_item_shape(entry_item)
            item_shapes[("tokens", total)] += 1
            item_shapes[("plain_tokens", plain)] += 1
            item_shapes[("star_tokens", starred)] += 1
            for q in qs:
                quantities[q] += 1

        entry_stone = field(data, b"EntryStone")
        if entry_stone is not None:
            v = atoi(entry_stone)
            scalar_shapes[("EntryStone", "negative" if v < 0 else "nonnegative")] += 1

        quiznum = field(data, b"Quiznum")
        if quiznum is not None:
            v = atoi(quiznum)
            scalar_shapes[("Quiznum", "positive" if v > 0 else "nonpositive")] += 1

        for key in (b"GetItem", b"Border", b"Warp"):
            value = field(data, key)
            if value is None:
                continue
            pairs, remainder = pair_shape(value)
            label = key.decode("ascii")
            pair_shapes[(label, pairs, remainder)] += 1

            vals = csv(value)
            if key == b"GetItem":
                for i in range(1, len(vals), 2):
                    reward_candidate_arity[len([x for x in vals[i].split(b".") if x])] += 1
            elif key == b"Warp":
                for i in range(1, len(vals), 2):
                    warp_destination_arity[len([x for x in vals[i].split(b".") if x])] += 1

    return {
        "counts": counts,
        "keys": keys,
        "item_shapes": item_shapes,
        "quantities": quantities,
        "pair_shapes": pair_shapes,
        "reward_candidate_arity": reward_candidate_arity,
        "warp_destination_arity": warp_destination_arity,
        "scalar_shapes": scalar_shapes,
        "aggregate": aggregate.hexdigest(),
        "questions": analyze_questions(question_file),
    }


def emit(result):
    print("StoneAge recovered Quiz usage probe — R1")
    print(
        "No NPC/template names, paths, dialogue, questions, answer text, "
        "coordinates, concrete item IDs, or original argument rows are stored."
    )
    print(
        "SCHEMA|Quiz refs -> secondary args + global question table -> "
        "key/state-mutation shape aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for key, n in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{n}")
    for key, n in sorted(result["keys"].items()):
        print(f"KEY_BLOCK|{key}|{n}")
    for (metric, value), n in sorted(result["item_shapes"].items()):
        print(f"ENTRY_ITEM_SHAPE|{metric}={value}|blocks={n}")
    for quantity, n in sorted(result["quantities"].items()):
        print(f"ENTRY_ITEM_QUANTITY|quantity={quantity}|tokens={n}")
    for (key, pairs, remainder), n in sorted(result["pair_shapes"].items()):
        print(f"PAIR_SHAPE|{key}|pairs={pairs}|remainder={remainder}|blocks={n}")
    for arity, n in sorted(result["reward_candidate_arity"].items()):
        print(f"GETITEM_CANDIDATE_ARITY|arity={arity}|pairs={n}")
    for arity, n in sorted(result["warp_destination_arity"].items()):
        print(f"WARP_DESTINATION_ARITY|arity={arity}|pairs={n}")
    for (key, shape), n in sorted(result["scalar_shapes"].items()):
        print(f"SCALAR_SHAPE|{key}|{shape}|blocks={n}")

    q = result["questions"]
    print(f"QUESTION_FILE|present={int(q['present'])}|rows={q['rows']}")
    if q["present"]:
        print("QUESTION_AGGREGATE_SHA256|" + q["aggregate"])
        for arity, n in sorted(q["arity"].items()):
            print(f"QUESTION_ARITY|fields={arity}|rows={n}")
        for label in ("type", "level", "answer_type", "answer_no"):
            for value, n in sorted(q[label].items()):
                print(f"QUESTION_META|{label}|value={value}|rows={n}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--question-file", type=Path)
    args = parser.parse_args()
    emit(analyze(args.npc_dir, args.question_file))


if __name__ == "__main__":
    main()
