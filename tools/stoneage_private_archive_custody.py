"""Private, local archive copy/readback for lawfully held StoneAge research carriers.

No downloads, no proprietary files in Git, and no proof of long-term storage.
Use only with a storage target independently verified to be private and durable.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

SCHEMA = "stoneage.private_original_archive_input_r1"
RECEIPT_SCHEMA = "stoneage.private_original_archive_receipt_r1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$")
DEFAULT_CHUNK_BYTES = 8 * 1024 * 1024


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest_file(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as handle:
        for part in iter(lambda: handle.read(1024 * 1024), b""):
            n += len(part)
            h.update(part)
    return n, h.hexdigest()


def load_manifest(path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    require(obj.get("schema") == SCHEMA, "manifest schema")
    require(isinstance(obj.get("archive_id"), str) and ID.fullmatch(obj["archive_id"]), "archive id")
    files = obj.get("files")
    require(isinstance(files, list) and files, "nonempty files")
    names = set()
    for entry in files:
        require(isinstance(entry, dict), "file object")
        name = entry.get("asset_id")
        require(isinstance(name, str) and ID.fullmatch(name) and name not in names, "unique asset id")
        names.add(name)
        src = entry.get("source_path")
        require(isinstance(src, str) and src and Path(src).is_absolute(), "absolute source path")
        require(not Path(src).is_symlink(), "source symlink forbidden")
        if Path(src).exists():
            require(stat.S_ISREG(Path(src).stat().st_mode), "not regular source")
        require(type(entry.get("expected_bytes")) is int and entry["expected_bytes"] >= 0, "expected bytes")
        require(isinstance(entry.get("expected_sha256"), str) and HEX64.fullmatch(entry["expected_sha256"]), "expected sha256")
        occ = entry.get("occurrences")
        require(isinstance(occ, list) and occ, "source occurrences required")
        seen = set()
        for item in occ:
            require(isinstance(item, dict) and set(item) == {"sample_id", "relative_path"}, "occurrence fields")
            sid, rel = item["sample_id"], item["relative_path"]
            require(isinstance(sid, str) and ID.fullmatch(sid), "sample id")
            require(isinstance(rel, str) and rel and not rel.startswith(("/", "\\")), "relative path")
            parts = rel.replace("\\", "/").split("/")
            require(all(p and p not in (".", "..") for p in parts), "unsafe occurrence path")
            require((sid, rel) not in seen, "duplicate occurrence")
            seen.add((sid, rel))
    return obj


def store_object(root, content):
    digest = hashlib.sha256(content).hexdigest()
    folder = root / "objects" / digest[:2]
    folder.mkdir(parents=True, exist_ok=True)
    final = folder / digest
    if final.exists():
        require(not final.is_symlink(), "symlink object")
        require(digest_file(final) == (len(content), digest), "existing object collision or corruption")
    else:
        fd, tmp = tempfile.mkstemp(prefix=".stage-", dir=folder)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            # A link, unlike replace, cannot overwrite another writer's object.
            try:
                os.link(tmp, final)
            except FileExistsError:
                require(digest_file(final) == (len(content), digest), "concurrent object mismatch")
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    require(digest_file(final) == (len(content), digest), "object readback failed")
    return {"sha256": digest, "bytes": len(content)}


def verify_receipt(root, receipt):
    require(receipt.get("schema") == RECEIPT_SCHEMA, "receipt schema")
    require(receipt.get("status") == "COPIED_AND_IMMEDIATE_READBACK_VERIFIED", "unqualified receipt status")
    require(isinstance(receipt.get("files"), list) and receipt["files"], "receipt files")
    for entry in receipt["files"]:
        require(HEX64.fullmatch(entry["expected_sha256"]) is not None, "receipt digest")
        reconstructed = hashlib.sha256()
        total = 0
        for part in entry["parts"]:
            require(HEX64.fullmatch(part["sha256"]) is not None, "part digest")
            path = root / "objects" / part["sha256"][:2] / part["sha256"]
            require(path.is_file() and not path.is_symlink(), "missing or symlink part")
            n, h = digest_file(path)
            require((n, h) == (part["bytes"], part["sha256"]), "part readback mismatch")
            with path.open("rb") as f:
                for buf in iter(lambda: f.read(1024 * 1024), b""):
                    reconstructed.update(buf)
            total += n
        require((total, reconstructed.hexdigest()) == (entry["expected_bytes"], entry["expected_sha256"]), "archive reassembly mismatch")
    return {"status": "FULL_READBACK_VERIFIED", "files": len(receipt["files"]),
            "provider_retention_verified": False, "commercial_runtime_executed": False}


def archive(manifest, root, chunk_bytes=DEFAULT_CHUNK_BYTES, confirmed=False, max_object_bytes=None):
    require(confirmed, "explicit private durable target acknowledgement required")
    require(type(chunk_bytes) is int and 0 < chunk_bytes <= 256 * 1024 * 1024, "chunk size")
    if max_object_bytes is not None:
        require(type(max_object_bytes) is int and max_object_bytes > 0 and chunk_bytes <= max_object_bytes, "object limit")
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "preexisting private target directory required")
    require(not (root / "objects").is_symlink() and not (root / "receipts").is_symlink(), "target symlink")
    receipt_dir = root / "receipts"
    receipt_dir.mkdir(exist_ok=True)
    receipt_path = receipt_dir / (manifest["archive_id"] + ".json")
    require(not receipt_path.exists(), "receipt already exists; preserve old evidence")
    budget = sum(e["expected_bytes"] for e in manifest["files"])
    require(shutil.disk_usage(root).free >= budget, "insufficient free space for conservative copy")
    entries = []
    for e in manifest["files"]:
        require(Path(e["source_path"]).is_file(), "source unavailable")
        chunks = []
        full = hashlib.sha256()
        total = 0
        with open(e["source_path"], "rb") as stream:
            while True:
                data = stream.read(chunk_bytes)
                if not data:
                    break
                full.update(data)
                total += len(data)
                chunks.append(store_object(root, data))
        require((total, full.hexdigest()) == (e["expected_bytes"], e["expected_sha256"]), "original source hash/size mismatch")
        entries.append({"asset_id": e["asset_id"], "expected_bytes": e["expected_bytes"],
                        "expected_sha256": e["expected_sha256"], "occurrences": e["occurrences"],
                        "parts": chunks})
    receipt = {"schema": RECEIPT_SCHEMA, "archive_id": manifest["archive_id"],
               "status": "COPIED_AND_IMMEDIATE_READBACK_VERIFIED",
               "files": entries, "private_target_operator_attested": True,
               "provider_retention_verified": False, "original_cleanliness_inferred": False,
               "named_pet_npc_quest_inferred": False}
    verify_receipt(root, receipt)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=receipt_dir,
                                     prefix=".receipt-", delete=False) as tmp:
        temp_name = tmp.name
        json.dump(receipt, tmp, ensure_ascii=False, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
    try:
        os.link(temp_name, receipt_path)
    finally:
        os.unlink(temp_name)
    return receipt_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="command", required=True)
    copy = commands.add_parser("archive", help="copy to already provisioned private target")
    copy.add_argument("--manifest", required=True)
    copy.add_argument("--root", required=True)
    copy.add_argument("--chunk-bytes", type=int, default=DEFAULT_CHUNK_BYTES)
    copy.add_argument("--max-object-bytes", type=int)
    copy.add_argument("--private-target-confirmed", action="store_true")
    check = commands.add_parser("verify", help="independent full readback from private archive")
    check.add_argument("--receipt", required=True)
    check.add_argument("--root", required=True)
    args = p.parse_args()
    if args.command == "archive":
        report = archive(load_manifest(args.manifest), args.root, args.chunk_bytes,
                         args.private_target_confirmed, args.max_object_bytes)
        print(json.dumps({"receipt": str(report), "status": "LOCAL_READBACK_ONLY"}, ensure_ascii=False))
    else:
        result = verify_receipt(Path(args.root), json.loads(Path(args.receipt).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
