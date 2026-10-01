#!/usr/bin/env python3
"""Inspect pinned descendant Nocast profiles without storing original source."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

PROFILES = {
    "gavin": ("1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56", "gmsv/src"),
    "iris": ("9e6c8ce2cd8ed532a7157773acd1c61582c178b5", "Source/gmsv"),
    "bismarck": ("999ffdf1d220ec6666eb65339180689c9caf1876", "server/gmsv"),
}
FEATURES = ("_SKILL_NOCAST", "_MAGIC_NOCAST", "__ATTACK_MAGIC", "_ATTACK_MAGIC",
            "_SUIT_ADDENDUM", "_EQUIT_RESIST", "_SUIT_ADDPART3", "_MO_LUA_RESIST")


def analyze_source(name: str, root: Path):
    expected, base = PROFILES[name]
    root = Path(root).resolve()
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if actual != expected:
        raise ValueError(f"{name} source HEAD does not match pinned commit")
    if subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip():
        raise ValueError(f"{name} source tree has uncommitted changes")
    source = root / base
    include = source / "include"
    includes = ["-I", str(include)]
    if name == "bismarck":
        includes += ["-I", str(root / "server/common"), "-I", str(root / "shared/lua51")]
    definitions = subprocess.check_output(["cpp", "-dM", *includes, str(include / "version.h")], text=True)
    active = set(re.findall(r"^#define\s+(\w+)\b", definitions, re.M))
    features = {feature: feature in active for feature in FEATURES}
    # Probe actual header enums, not a manually counted command sequence.
    code = ('#include <stdio.h>\n#include "char_base.h"\n#include "battle.h"\n'
            '#include "battle_event.h"\nint main(void){'
            'printf("%d %d %d %d", BATTLE_ST_NOCAST, CHAR_WORKNOCAST,'
            'CHAR_WORKWEAKEN, CHAR_WORKBARRIER);'
            '#ifdef _SKILL_NOCAST\n'
            'printf(" %d",BATTLE_COM_S_NOCAST);\n'
            '#endif\nreturn 0;}\n')
    code = code.replace(';#ifdef', ';\n#ifdef')
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)
        (path / "probe.c").write_text(code)
        subprocess.run(["cc", "-w", *includes, str(path / "probe.c"), "-o", str(path / "probe")],
                       check=True, capture_output=True)
        enums = tuple(map(int, subprocess.check_output([str(path / "probe")], text=True).split()))
    hashes = []
    for rel in ("include/version.h", "include/char_base.h", "include/battle.h",
                "include/battle_event.h", "battle/pet_skill.c", "battle/battle.c",
                "battle/battle_event.c", "magic/magic.c"):
        hashes.append((base + "/" + rel, hashlib.sha256((source / rel).read_bytes()).hexdigest()))
    return {"name": name, "sha": actual, "features": features, "enums": enums, "hashes": tuple(hashes)}


def emit(results):
    print("StoneAge pinned descendant Nocast profile audit — R1")
    print("Only source identity, feature presence, enum values and hashes are stored.")
    for result in results:
        print(f"PROFILE|name={result['name']}|sha={result['sha']}")
        for feature, active in result["features"].items():
            print(f"FEATURE|profile={result['name']}|name={feature}|active={int(active)}")
        st, work, weaken, barrier, *command = result["enums"]
        print(f"ENUM|profile={result['name']}|status_nocast={st}|work_nocast={work}|"
              f"work_weaken={weaken}|work_barrier={barrier}|"
              f"command_nocast={command[0] if command else 'not_compiled'}")
        for path, digest in result["hashes"]:
            print(f"SOURCE_HASH|profile={result['name']}|path={path}|sha256={digest}")


def main():
    parser = argparse.ArgumentParser()
    for name in PROFILES:
        parser.add_argument(f"--{name}-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(tuple(analyze_source(name, getattr(args, name + "_dir")) for name in PROFILES))


if __name__ == "__main__":
    main()
