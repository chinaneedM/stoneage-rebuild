#!/usr/bin/env python3
"""Aggregate recovered StoneAge ExChangeMan secondary-argument usage without payload text."""

import argparse
import collections
import hashlib
from pathlib import Path

TEMPLATE_MAGIC = b"NPCTEMPLATE"
CREATE_MAGIC = b"NPCCREATE"

KNOWN_KEYS = (
    b"EventNo",
    b"EVENT",
    b"TYPE",
    b"KeyWord",
    b"Pet_Name",
    b"GetItem",
    b"DelItem",
    b"GetRandItem",
    b"GetStone",
    b"DelStone",
    b"GetPet",
    b"GetEgg",
    b"DelPet",
    b"EndSetFlg",
    b"CleanFlg",
    b"NpcWarp",
    b"Break",
    b"NotDel",
    b"pet_skill",
)

CONDITION_FAMILIES = (
    b"PETEV",
    b"PET",
    b"ENDEV",
    b"NOWEV",
    b"ITEM",
    b"IMAGE",
    b"TIME",
    b"SP",
    b"LV",
)


def source_candidate(path):
    name = path.name
    return not (name.endswith("~") or name.startswith("#") or name.lower().endswith(".bak"))


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
            k, v = line.split(b"=", 1)
            block.append((k.strip().lower(), v.strip()))


def parse_templates(paths):
    out = collections.defaultdict(list)
    for path in paths:
        for entries in iter_blocks(path):
            fields = {}
            for k, v in entries:
                fields[k] = v
            name = fields.get(b"templatename", b"")
            if name:
                out[name].append(fields.get(b"functionset", b""))
    return out


def parse_create_refs(paths):
    for path in paths:
        for entries in iter_blocks(path):
            for k, v in entries:
                if k != b"enemy":
                    continue
                name, sep, arg = v.partition(b"|")
                yield name.strip(), (arg if sep else b"")


def assigned_file(arg):
    for token in arg.split(b"|"):
        if b"file" in token:
            parts = token.split(b":")
            if len(parts) >= 2:
                return parts[1].decode("utf-8", "replace")
    return None


def merge_arg_file(path):
    merged = b""
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if merged and not merged.endswith(b"|"):
                merged += b"|"
            merged += line
    return merged


def field_value(block, key):
    for token in block.split(b"|"):
        if key in token:
            parts = token.split(b":")
            if len(parts) >= 2:
                return parts[1]
    return None


def exact_key_tokens(block):
    for token in block.split(b"|"):
        if b":" not in token:
            continue
        key = token.split(b":", 1)[0].strip()
        if key:
            yield key


def condition_terms(event_value):
    for branch in event_value.split(b","):
        for term in branch.split(b"&"):
            term = term.strip()
            if term:
                yield branch, term


def classify_family(term):
    for family in CONDITION_FAMILIES:
        if family in term:
            return family.decode("ascii")
    return "OTHER"


def analyze(npc_dir):
    all_files = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    templates = [p for p in all_files if magic_kind(p) == "template"]
    creates = [p for p in all_files if magic_kind(p) == "create"]
    template_map = parse_templates(templates)

    exchange_names = {
        name for name, sets in template_map.items() if any(v == b"ExChangeMan" for v in sets)
    }
    ambiguous_names = {
        name
        for name in exchange_names
        if len(template_map[name]) > 1 or len(set(template_map[name])) > 1
    }

    counts = collections.Counter()
    key_blocks = collections.Counter()
    family_blocks = collections.Counter()
    family_terms = collections.Counter()
    op_terms = collections.Counter()
    type_blocks = collections.Counter()
    aggregate = hashlib.sha256()

    counts["template_names_exchangeman"] = len(exchange_names)
    counts["template_names_exchangeman_ambiguous"] = len(ambiguous_names)
    for key in (
        "create_refs_exchangeman_ambiguous",
        "quirk_live_lv_not_equal",
        "quirk_live_nowev_not_equal",
        "quirk_live_item_relational",
        "quirk_live_image_relational",
        "quirk_live_pet_not_equal",
        "quirk_capable_getstone_delstone_nonnet",
        "quirk_capable_evdel",
        "quirk_capable_evdel_nonstar_item_term",
        "quirk_capable_delitem_loop_index_truncation",
        "getpet_random_candidate_blocks",
        "getegg_random_candidate_blocks",
    ):
        counts[key] = 0

    for name, arg in parse_create_refs(creates):
        if name not in exchange_names:
            continue
        counts["create_refs_exchangeman"] += 1
        if name in ambiguous_names:
            counts["create_refs_exchangeman_ambiguous"] += 1
        if not arg:
            counts["create_refs_without_argument"] += 1
            continue

        fn = assigned_file(arg)
        if fn is not None:
            counts["create_refs_file_argument"] += 1
            path = npc_dir / fn
            if not path.is_file():
                counts["argument_files_missing"] += 1
                continue
            data = merge_arg_file(path)
            counts["argument_files_resolved"] += 1
            digest = hashlib.sha256(data).hexdigest().encode()
            aggregate.update(str(len(data)).encode() + b"|" + digest + b"\n")
        else:
            counts["create_refs_inline_argument"] += 1
            data = arg
            digest = hashlib.sha256(data).hexdigest().encode()
            aggregate.update(str(len(data)).encode() + b"|" + digest + b"\n")

        blocks = data.split(b"EventEnd")
        if len(blocks) <= 1:
            counts["arguments_without_eventend"] += 1
        counts["event_segments_total"] += len(blocks)

        for block in blocks:
            if not block.strip(b"| \t\r\n"):
                counts["event_segments_empty"] += 1
                continue
            counts["event_blocks_nonempty"] += 1

            known_present = set()
            for key in KNOWN_KEYS:
                if field_value(block, key) is not None or (key in (b"Break",) and key in block):
                    known_present.add(key.decode("ascii"))
            for key in known_present:
                key_blocks[key] += 1

            unknown = 0
            for key in exact_key_tokens(block):
                if key not in KNOWN_KEYS:
                    unknown += 1
            counts["unknown_key_tokens"] += unknown

            event = field_value(block, b"EVENT")
            if event is None:
                counts["event_blocks_without_event_condition"] += 1
            else:
                counts["event_blocks_with_event_condition"] += 1
                if b"," in event:
                    counts["event_blocks_with_or"] += 1
                block_families = set()
                for branch, term in condition_terms(event):
                    if b"&" in branch:
                        counts["condition_terms_in_and_branch"] += 1
                    fam = classify_family(term)
                    family_terms[fam] += 1
                    block_families.add(fam)
                    if b"!=" in term:
                        op_terms["!="] += 1
                        if fam == "LV":
                            counts["quirk_live_lv_not_equal"] += 1
                        elif fam == "NOWEV":
                            counts["quirk_live_nowev_not_equal"] += 1
                        elif fam in {"PET", "PETEV"}:
                            counts["quirk_live_pet_not_equal"] += 1
                    elif b"<" in term:
                        op_terms["<"] += 1
                        if fam == "ITEM":
                            counts["quirk_live_item_relational"] += 1
                        elif fam == "IMAGE":
                            counts["quirk_live_image_relational"] += 1
                    elif b">" in term:
                        op_terms[">"] += 1
                        if fam == "ITEM":
                            counts["quirk_live_item_relational"] += 1
                        elif fam == "IMAGE":
                            counts["quirk_live_image_relational"] += 1
                    elif b"=" in term:
                        op_terms["="] += 1
                    else:
                        op_terms["none"] += 1
                    if b"*" in term:
                        counts["condition_terms_with_star"] += 1
                for fam in block_families:
                    family_blocks[fam] += 1

            typ = field_value(block, b"TYPE")
            matched_types = []
            if typ is not None:
                for label in (b"REQUEST", b"ACCEPT", b"MESSAGE"):
                    if label in typ:
                        name = label.decode("ascii")
                        type_blocks[name] += 1
                        matched_types.append(name)
                if not matched_types:
                    type_blocks["OTHER"] += 1
                    matched_types.append("OTHER")

            if field_value(block, b"EndSetFlg") is not None:
                if matched_types:
                    for name in matched_types:
                        counts["endset_type_" + name.lower()] += 1
                else:
                    counts["endset_type_missing"] += 1

            delete = field_value(block, b"DelItem")
            if delete is not None:
                if b"EVDEL" in delete:
                    counts["quirk_capable_evdel"] += 1
                    if event is not None:
                        for _, term in condition_terms(event):
                            if b"ITEM" in term and b"=" in term:
                                rhs = term.split(b"=", 1)[1]
                                if b"*" not in rhs:
                                    counts["quirk_capable_evdel_nonstar_item_term"] += 1
                                    break
                else:
                    toks = delete.split(b",")
                    if len(toks) > 1 and any(b"*" not in t for t in toks[:-1]):
                        counts["quirk_capable_delitem_loop_index_truncation"] += 1

            if field_value(block, b"GetStone") is not None and field_value(block, b"DelStone") is not None:
                counts["quirk_capable_getstone_delstone_nonnet"] += 1
            if field_value(block, b"GetItem") is not None and field_value(block, b"GetRandItem") is not None:
                counts["blocks_getitem_and_random"] += 1

            getpet = field_value(block, b"GetPet")
            if getpet is not None and b"," in getpet:
                counts["getpet_random_candidate_blocks"] += 1
            getegg = field_value(block, b"GetEgg")
            if getegg is not None and b"," in getegg:
                counts["getegg_random_candidate_blocks"] += 1

    return {
        "counts": counts,
        "key_blocks": key_blocks,
        "family_blocks": family_blocks,
        "family_terms": family_terms,
        "op_terms": op_terms,
        "type_blocks": type_blocks,
        "arg_aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered ExChangeMan secondary-argument usage probe — R1")
    print("No NPC names, dialogue, paths, concrete item/pet IDs, coordinates, or argument rows are stored.")
    print("SCHEMA|ExChangeMan templates -> create refs -> inline/file arg merge -> EventEnd segments -> aggregate structural usage")
    print(f"ARG_CORPUS_AGGREGATE_SHA256|{result['arg_aggregate']}")
    for k in sorted(result["counts"]):
        print(f"COUNT|{k}|{result['counts'][k]}")
    for k, n in sorted(result["key_blocks"].items()):
        print(f"KEY_BLOCK|{k}|{n}")
    for k, n in sorted(result["type_blocks"].items()):
        print(f"TYPE_BLOCK|{k}|{n}")
    for k, n in sorted(result["family_blocks"].items()):
        print(f"CONDITION_FAMILY_BLOCK|{k}|{n}")
    for k, n in sorted(result["family_terms"].items()):
        print(f"CONDITION_FAMILY_TERM|{k}|{n}")
    for k, n in sorted(result["op_terms"].items()):
        print(f"CONDITION_OPERATOR_TERM|{k}|{n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    args = ap.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
