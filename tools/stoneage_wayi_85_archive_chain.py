"""Offline metadata validation and read-only local hashing. No downloads or execution."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json"
IDS = ("l5i274801ov19w7", "g9b3g3hjmwwttg3", "e859n1nm1tk12j8",
       "69vrzm3nox8f0v9", "clbwjkcqqhxq6k9", "42uy5b9abbcu4qr")
FALSE_FIELDS = (
    "parts_payload_downloaded", "original_publisher_binary_equivalence_verified",
    "installer_version_verified_from_bytes", "authentic_pet_runtime_verified",
    "early_jss_or_taiwan_v1_equivalence_verified",
)


def validate(data):
    if data.get("schema") != "stoneage_wayi_85_sixpart_metadata_r1":
        raise ValueError("Unknown archive manifest")
    if data.get("classification") != "UNVERIFIED_SPLIT_MIRROR_METADATA_ONLY":
        raise ValueError("Unverified mirror promoted")
    if data.get("claimed_original_url") != "http://download.wayi.com.tw/download/STONEAGE20060616.exe":
        raise ValueError("Wrong operator URL")
    if any(data.get(k) is not False for k in FALSE_FIELDS):
        raise ValueError("Unsupported authenticity or runtime promotion")
    if data.get("part_sha256") is not None or data.get("assembled_sha256") is not None:
        raise ValueError("No actual bytes observed; hashes not allowed in metadata")
    if len(data.get("parts", [])) != 6:
        raise ValueError("Exactly six candidate parts required")
    if len(data.get("historical_url_sources", [])) != 2 or not data.get("mirror_post"):
        raise ValueError("Historical sources missing")
    for n, (part, key) in enumerate(zip(data["parts"], IDS), 1):
        filename = "STONEAGE20060616.exe." + str(n).zfill(3)
        if part.get("part") != n or part.get("filename") != filename or part.get("key") != key:
            raise ValueError("Part identity or sequence changed")
        if part.get("size_label") != ("92.4MB" if n == 6 else "200MB"):
            raise ValueError("Rounded displayed size mismatch")
        if not part.get("upload_display", "").startswith("2012-04-14 "):
            raise ValueError("Upload date provenance mismatch")
        if "byte_size" in part or "sha256" in part:
            raise ValueError("Fabricated exact-size or hash data")
    return data["parts"]


def hash_local_candidate(data, directory):
    parts = validate(data)
    root = Path(directory)
    if not root.is_dir():
        raise ValueError("Local part directory missing")
    combined = hashlib.sha256()
    file_receipts = []
    for item in parts:
        path = root / item["filename"]
        if not path.is_file() or path.is_symlink():
            raise ValueError("Missing or unsafe split part " + item["filename"])
        filehash = hashlib.sha256()
        nbytes = 0
        with path.open("rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                filehash.update(chunk)
                combined.update(chunk)
                nbytes += len(chunk)
        if not nbytes:
            raise ValueError("Empty split part")
        file_receipts.append({"filename": item["filename"], "bytes": nbytes, "sha256": filehash.hexdigest()})
    return {
        "classification": "LOCAL_HASH_ONLY_NOT_ORIGINAL_AUTHENTICATION",
        "original_binary_equivalence_verified": False,
        "runtime_verified": False,
        "file_digests": file_receipts,
        "concatenation_sha256": combined.hexdigest(),
        "concatenation_bytes": sum(e["bytes"] for e in file_receipts),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--local-dir", type=Path)
    args = p.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    validate(data)
    if args.local_dir:
        print(json.dumps(hash_local_candidate(data, args.local_dir), indent=2))
    else:
        print("WAYI85_ARCHIVE_METADATA_ONLY_PASS_NO_BYTES")


if __name__ == "__main__":
    main()
