#!/usr/bin/env python3
"""Anonymous recovered25 enemybase-name encoding audit.

The report never emits original name bytes or decoded names. It only records
strict decoding counts/hashes needed to choose a reconstruction-safe text
decoder for the active enemybase table.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_enemybase_probe import clean_lines, setup_value


CANDIDATE_ENCODINGS = (
    "ascii",
    "cp950",
    "big5",
    "gbk",
    "gb18030",
    "shift_jis",
    "utf-8",
)


@dataclass(frozen=True)
class EnemybaseNameEncodingAudit:
    file_name: str
    row_count: int
    nonempty_name_count: int
    distinct_name_hash_count: int
    decodable_counts: tuple[tuple[str, int], ...]
    cp950_big5_both_decodable: int
    cp950_big5_same_text: int
    cp950_big5_different_text: int
    aggregate_name_sha256: str

    def count(self, encoding: str) -> int:
        return dict(self.decodable_counts)[str(encoding)]


def _active_enemybase_path(data_dir: Path, setup: Path | None) -> Path:
    configured = setup_value(setup, "enemybasefile")
    name = (
        Path(configured.replace("\\", "/")).name
        if configured
        else "enemybase.txt"
    )
    path = Path(data_dir) / name
    if not path.is_file():
        raise ValueError(f"active enemybase file not found: {name}")
    return path


def analyze(
    *,
    data_dir: Path,
    setup: Path | None = None,
) -> EnemybaseNameEncodingAudit:
    path = _active_enemybase_path(Path(data_dir), setup)
    names: list[bytes] = []
    for line in clean_lines(path):
        fields = line.split(b",")
        if len(fields) < 1:
            continue
        names.append(fields[0].strip())

    counts = {encoding: 0 for encoding in CANDIDATE_ENCODINGS}
    both = same = different = 0
    hashes: set[str] = set()
    aggregate = hashlib.sha256()

    for raw in names:
        if raw:
            hashes.add(hashlib.sha256(raw).hexdigest())
        aggregate.update(len(raw).to_bytes(4, "big"))
        aggregate.update(raw)

        decoded: dict[str, str] = {}
        for encoding in CANDIDATE_ENCODINGS:
            try:
                decoded[encoding] = raw.decode(encoding, errors="strict")
            except UnicodeDecodeError:
                continue
            counts[encoding] += 1

        if "cp950" in decoded and "big5" in decoded:
            both += 1
            if decoded["cp950"] == decoded["big5"]:
                same += 1
            else:
                different += 1

    return EnemybaseNameEncodingAudit(
        file_name=path.name,
        row_count=len(names),
        nonempty_name_count=sum(1 for raw in names if raw),
        distinct_name_hash_count=len(hashes),
        decodable_counts=tuple(
            (encoding, counts[encoding])
            for encoding in CANDIDATE_ENCODINGS
        ),
        cp950_big5_both_decodable=both,
        cp950_big5_same_text=same,
        cp950_big5_different_text=different,
        aggregate_name_sha256=aggregate.hexdigest(),
    )


def emit(audit: EnemybaseNameEncodingAudit) -> None:
    print("StoneAge recovered25 enemybase name encoding audit — R1")
    print(
        "SCOPE|active-enemybase-first-string-field|"
        "no-raw-name-bytes|no-decoded-names"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(f"ACTIVE_FILE|{audit.file_name}")
    print(f"COUNT|rows|{audit.row_count}")
    print(f"COUNT|nonempty_names|{audit.nonempty_name_count}")
    print(
        "COUNT|distinct_name_hashes|"
        f"{audit.distinct_name_hash_count}"
    )
    for encoding, count in audit.decodable_counts:
        print(f"COUNT|strict_decodable:{encoding}|{count}")
    print(
        "COUNT|cp950_big5_both_decodable|"
        f"{audit.cp950_big5_both_decodable}"
    )
    print(
        "COUNT|cp950_big5_same_text|"
        f"{audit.cp950_big5_same_text}"
    )
    print(
        "COUNT|cp950_big5_different_text|"
        f"{audit.cp950_big5_different_text}"
    )
    print(
        "AGGREGATE_NAME_SHA256|"
        f"{audit.aggregate_name_sha256}"
    )

    if (
        audit.row_count > 0
        and audit.count("cp950") == audit.row_count
        and audit.count("big5") == audit.row_count
        and audit.cp950_big5_different_text == 0
    ):
        print(
            "RUNTIME_TEXT_DECODER|cp950|"
            "all-active-names-strictly-decodable-and-big5-equivalent"
        )
        print("RESOLUTION|RECOVERED25_ENEMYBASE_NAME_ENCODING_CLOSED_CP950")
    else:
        print("RUNTIME_TEXT_DECODER|UNRESOLVED")
        print("RESOLUTION|RECOVERED25_ENEMYBASE_NAME_ENCODING_OPEN")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    a = ap.parse_args()
    emit(analyze(data_dir=a.data_dir, setup=a.setup))


if __name__ == "__main__":
    main()
