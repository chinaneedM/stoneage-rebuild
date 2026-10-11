"""Source-only PET carried-item and unique-code call-path orientation.

Proves the presence and branch boundaries of operations in *pinned late
descendants*, not live configuration, natural user reachability, or JSS/TW v1.
Raw proprietary game sources stay transient in CI and are never published.
"""
from __future__ import annotations
import argparse
import hashlib
import re
import subprocess
from pathlib import Path
from tools.stoneage_enemy_creation_audit import definition

PROFILES = {
    "gavin": {
        "commit": "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56",
        "root": "gmsv/src",
        "files": {
            "base": "783b8803333bf3a63320b4379519a69b377e9037",
            "char": "6f1c35acb8ceb103e5501c88e49d8fe93aafcb70",
            "item": "ff3d18514367905c8dd72316908508dd60272018",
            "version": "af6c866fd609a39e2960236275f6bf39e7f47b2c",
        },
        "pet_gate": "NOT_SIMPLIFY_ITEMSTRING",
        "item_slots": "CHAR_MAXITEMHAVE",
    },
    "bismarck": {
        "commit": "999ffdf1d220ec6666eb65339180689c9caf1876",
        "root": "server/gmsv",
        "files": {
            "base": "5f646eba671b39f5e90f53e3a95cbcc70ff56975",
            "char": "970b7b3f975965c6c5e77352a2e0382adf943753",
            "item": "94b00b11d02cc775bab6fe72c9c2ba77d9618712",
            "version": "b3fc0c80705973bc8d088287c98a5d66171bb6c2",
        },
        "pet_gate": "PET_ITEM",
        "item_slots": "CHAR_MAXPETITEMHAVE",
    },
}
FUNCTIONS = {
    "base": ("_CHAR_getItemIndex", "_CHAR_setItemIndex",
             "CHAR_makePetStringFromPetIndex", "CHAR_makePetFromStringToArg",
             "ITEM_setItemUniCode"),
    "char": ("CHAR_addItemToChar", "CHAR_addItem",
             "CHAR_addItemSpecificItemIndex"),
    "item": ("_ITEM_initExistItemsOne", "_ITEM_endExistItemsOne",
             "ITEM_makeItemAndRegist"),
}
REQUIRED = (
    "add_direct_factory", "add_records_owner", "specific_add_calls_setter",
    "specific_add_records_owner", "generic_add_type_unrestricted",
    "specific_add_type_unrestricted", "setter_index_no_actor_type",
    "setter_unique_hook_conditional", "pet_serializer_has_item_path",
    "pet_parser_has_item_path", "pet_parser_direct_slot_write",
    "pet_parser_calls_original_initializer", "unique_uses_clock_counter",
    "allocator_owner_player_type_check", "release_scans_player_count",
    "factory_registers_unattached_template",
)
HEX = re.compile(r"^[a-f0-9]{64}$")


def demand(value, message):
    if not value:
        raise ValueError(message)


def git_blob_id(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def read_pinned(profile, root):
    spec = PROFILES[profile]
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    demand(sha == spec["commit"], "pinned source checkout mismatch: " + profile)
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True)
    demand(not dirty, "pinned source checkout dirty: " + profile)
    paths = {"base": "char/char_base.c", "char": "char/char_item.c",
             "item": "item/item.c", "version": "include/version.h"}
    data = {}
    for category, path in paths.items():
        raw = (root / spec["root"] / path).read_bytes()
        demand(git_blob_id(raw) == spec["files"][category],
               "pinned original file drift: " + profile + " " + path)
        data[category] = raw.decode("utf-8", errors="replace")
    return data


def observe(profile, texts):
    parts = {}
    for category, names in FUNCTIONS.items():
        for name in names:
            parts[name] = definition(texts[category], name)
    grab = parts.__getitem__
    add_to_char = grab("CHAR_addItemToChar")
    add = grab("CHAR_addItem")
    specific = grab("CHAR_addItemSpecificItemIndex")
    setter = grab("_CHAR_setItemIndex")
    pet_to_string = grab("CHAR_makePetStringFromPetIndex")
    pet_from_string = grab("CHAR_makePetFromStringToArg")
    ucode = grab("ITEM_setItemUniCode")
    allocation = grab("_ITEM_initExistItemsOne")
    released = grab("_ITEM_endExistItemsOne")
    factory = grab("ITEM_makeItemAndRegist")
    conditions = {
        "add_direct_factory": "ITEM_makeItemAndRegist(" in add_to_char
            and re.search(r"indexOfExistItems\s*\[\s*itembox\s*\]\s*=", add_to_char) is not None,
        "add_records_owner": "CHAR_addItemToChar(" in add
            and "ITEM_WORKCHARAINDEX" in add and "ITEM_WORKOBJINDEX" in add,
        "specific_add_calls_setter": "CHAR_setItemIndex(" in specific
            and "CHAR_findEmptyItemBox(" in specific,
        "specific_add_records_owner": "ITEM_WORKCHARAINDEX" in specific
            and "ITEM_WORKOBJINDEX" in specific,
        "generic_add_type_unrestricted": "CHAR_TYPEPLAYER" not in add
            and "CHAR_TYPEPET" not in add and "CHAR_TYPEPLAYER" not in add_to_char
            and "CHAR_TYPEPET" not in add_to_char,
        "specific_add_type_unrestricted": "CHAR_TYPEPLAYER" not in specific
            and "CHAR_TYPEPET" not in specific,
        "setter_index_no_actor_type": re.search(
            r"indexOfExistItems\s*\[\s*iindex\s*\]\s*=\s*id", setter) is not None
            and "CHAR_TYPEPLAYER" not in setter and "CHAR_TYPEPET" not in setter,
        "setter_unique_hook_conditional": "#ifdef _UNIQUE_P_I" in setter
            and "ITEM_setItemUniCode(id)" in setter,
        "pet_serializer_has_item_path": "PETITEMRESERVESTRING" in pet_to_string
            and "ITEM_makeStringFromItemIndex(" in pet_to_string,
        "pet_parser_has_item_path": "PETITEMRESERVESTRING" in pet_from_string
            and "ITEM_makeExistItemsFromStringToArg(" in pet_from_string,
        "pet_parser_direct_slot_write": re.search(
            r"indexOfExistItems\s*\[\s*item_index\s*\]\s*=\s*existitem_index"
            if profile == "bismarck" else
            r"indexOfExistItems\s*\[\s*itemindex\s*\]\s*=\s*existitemindex",
            pet_from_string) is not None,
        "pet_parser_calls_original_initializer": "ITEM_initExistItemsOne(" in pet_from_string,
        "unique_uses_clock_counter": "time(&t1)" in ucode
            and "unique_i++" in ucode and "ITEM_UNIQUECODE" in ucode,
        "allocator_owner_player_type_check": "ITEM_WORKCHARAINDEX" in allocation
            and "CHAR_TYPEPLAYER" in allocation
            and "CHAR_getItemIndex(" in allocation,
        "release_scans_player_count": "CHAR_getPlayerMaxNum()" in released
            and "CHAR_getItemIndex(" in released
            and "hitcnt < 1" in released,
        "factory_registers_unattached_template": "ITEM_makeItem(" in factory
            and "ITEM_initExistItemsOne(" in factory
            and "ITEM_setItemUniCode(" not in factory,
    }
    gate = ("#ifdef _PET_ITEM" if profile == "bismarck"
            else "#ifndef _SIMPLIFY_ITEMSTRING")
    demand(pet_to_string.count(gate) >= 1 and pet_from_string.count(gate) >= 1,
           "pet item serialization gate no longer profile specific: " + profile)
    limit = PROFILES[profile]["item_slots"]
    demand(limit in pet_to_string and limit in pet_from_string,
           "pet item slot limit drift: " + profile)
    default_header = texts["version"]
    active = set(re.findall(r"(?m)^\s*#\s*define\s+(_SIMPLIFY_ITEMSTRING|_PET_ITEM|_UNIQUE_P_I)\b", default_header))
    demand("_UNIQUE_P_I" in active, "default unique-code feature setting drift")
    demand("_SIMPLIFY_ITEMSTRING" in active, "default simplified item-string setting drift")
    demand("_PET_ITEM" not in active, "default PET_ITEM feature setting drift")
    for name, passed in conditions.items():
        demand(passed, f"source-only call-path assertion failed: {profile}/{name}")
    return parts, conditions


def source_report(profile, texts):
    parts, checks = observe(profile, texts)
    s = PROFILES[profile]
    summary = {
        "profile": profile,
        "base_blob": s["files"]["base"],
        "char_blob": s["files"]["char"],
        "item_blob": s["files"]["item"],
        "version_blob": s["files"]["version"],
        "pet_gate": s["pet_gate"],
        "pet_slot_limit": s["item_slots"],
        **{key: int(checks[key]) for key in REQUIRED},
        "default_header_unique_macro": 1,
        "default_header_simplify_macro": 1,
        "default_header_pet_item_macro": 0,
        "default_header_pet_serialization_active": 0,
        "natural_reachability_proven": 0,
        "production_macro_configuration_verified": 0,
        "first_release_membership_proven": 0,
    }
    rows = ["SOURCE_ONLY_PET_ITEM_IDENTITY|" +
            "|".join(f"{key}={val}" for key, val in summary.items())]
    for name in sorted(parts):
        digest = hashlib.sha256(parts[name].encode()).hexdigest()
        rows.append(f"SOURCE_ONLY_PET_ITEM_FUNCTION|profile={profile}|name={name}|sha256={digest}")
    return rows


def parse_fields(line):
    fields = [pair.split("=", 1) for pair in line.split("|")[1:]]
    if any(len(x) != 2 for x in fields):
        raise ValueError("malformed source-only row")
    d = dict(fields)
    if len(d) != len(fields):
        raise ValueError("duplicate field in source-only row")
    return d


def validate_report(report):
    profiles, bodies = {}, set()
    for line in report.splitlines():
        if line.startswith("SOURCE_ONLY_PET_ITEM_IDENTITY|"):
            data = parse_fields(line)
            p = data.get("profile")
            if p not in PROFILES or p in profiles:
                raise ValueError("duplicate or unexpected source-only profile")
            spec = PROFILES[p]
            required = {"profile", "base_blob", "char_blob", "item_blob",
                        "version_blob", "pet_gate", "pet_slot_limit", *REQUIRED,
                        "default_header_unique_macro",
                        "default_header_simplify_macro",
                        "default_header_pet_item_macro",
                        "default_header_pet_serialization_active",
                        "natural_reachability_proven",
                        "production_macro_configuration_verified",
                        "first_release_membership_proven"}
            if set(data) != required:
                raise ValueError("missing or unknown source-only field")
            expected = {"base_blob": spec["files"]["base"],
                        "char_blob": spec["files"]["char"],
                        "item_blob": spec["files"]["item"],
                        "version_blob": spec["files"]["version"],
                        "pet_gate": spec["pet_gate"],
                        "pet_slot_limit": spec["item_slots"]}
            expected.update({k: "1" for k in REQUIRED})
            expected.update({k: "1" for k in (
                "default_header_unique_macro", "default_header_simplify_macro")})
            expected.update({k: "0" for k in (
                "default_header_pet_item_macro", "default_header_pet_serialization_active",
                "natural_reachability_proven",
                "production_macro_configuration_verified",
                "first_release_membership_proven")})
            if any(data[key] != val for key, val in expected.items()):
                raise ValueError("incorrect source path flag or original raw blob ID")
            profiles[p] = data
        elif line.startswith("SOURCE_ONLY_PET_ITEM_FUNCTION|"):
            data = parse_fields(line)
            if set(data) != {"profile", "name", "sha256"}:
                raise ValueError("bad function fingerprint fields")
            p, name = data["profile"], data["name"]
            if p not in PROFILES or name not in sum((list(v) for v in FUNCTIONS.values()), []):
                raise ValueError("unknown source function identity")
            if (p, name) in bodies or not HEX.fullmatch(data["sha256"]):
                raise ValueError("duplicate or invalid function fingerprint")
            bodies.add((p, name))
    need = {(p, f) for p in PROFILES for fs in FUNCTIONS.values() for f in fs}
    if set(profiles) != set(PROFILES) or bodies != need:
        raise ValueError("incomplete pinned function-level source witness matrix")
    if "RESOLUTION|PET_ITEM_IDENTITY_SOURCE_ONLY_ORIENTATION_PASS" not in report.splitlines():
        raise ValueError("missing source-only boundary resolution")
    return profiles, bodies


def main():
    parser = argparse.ArgumentParser()
    for p in PROFILES:
        parser.add_argument(f"--{p}-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for p in PROFILES:
        root = getattr(args, p + "_dir")
        print(f"PROVENANCE|{p}|commit={PROFILES[p]['commit']}", flush=True)
        rows.extend(source_report(p, read_pinned(p, root)))
    rows.extend((
        "BOUNDARY|Source-only late-descendant function access and conditional PET persistence; pinned default version headers select disabled PET persistence paths, unique-code and simplify macros defined; actual produced-build flags, natural gameplay calls, early object identity and JSS/Taiwan1.0 remain unproved",
        "OPEN|real PET add/equip call sites; post-login owner rebinding; compile-time macros; original item unique-code regeneration and first-release membership; stale alias dereference",
        "RESOLUTION|PET_ITEM_IDENTITY_SOURCE_ONLY_ORIENTATION_PASS",
    ))
    for row in rows:
        print(row)
    validate_report("\n".join(rows))


if __name__ == "__main__":
    main()
