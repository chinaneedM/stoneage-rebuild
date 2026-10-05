#!/usr/bin/env python3
"""Recovered25 Combined selected-magic cross-link probe.

This is a derived-only bridge from the already pinned Combined OPTION magic IDs
into recovered magic.txt.  It stores code function tokens and numeric metadata,
never recovered names/comments/raw OPTION text.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_magic_probe import parse as parse_magic, sha256
from tools.stoneage_recovered25_combined_probe import EXPECTED_EXACT_ROWS

EXPECTED_MAGIC_IDS=(
    20,21,22,23,24,25,61,71,81,91,101,121,
    139,159,169,179,189,240,306,
)
EXPECTED_MAGIC_SHA256="b3a57b595bd60dfab571fe7af4dd6e2d43a5839c934eb644ba462897b1bcb6bb"
EXPECTED_EXACT_MAGIC_ROWS=(
    (20,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,2,"1a6562590ef19d1045d06c4055742d38288e9e6dcd71ccde5cee80f1d5a774eb",False),
    (21,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,3,"ad57366865126e55649ecb23ae1d48887544976efea46a48eb5d85a6eeb4d306",False),
    (22,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,3,"27badc983df1780b60c2b3fa9d3a19a00e46aac798451f0febdca52920faaddf",False),
    (23,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,3,"983bd614bb5afece5ab3b6023f71147cd7b6bc2314f9d27af7422541c6558389",False),
    (24,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,3,"0604cd3138feed202ef293e062da2f4720f77a05d25ee036a7a01c9cfcdd1f0a",False),
    (25,"MAGIC_Recovery","0b3af9808d0d5d77f9d093223c13425b8a5b07b5c1542271e90d8afbbe5a62b8",1,8,0,None,3,"284b7e6d788f363f910f7beb1910473e23ce9d6c871f1ce0f31f22a982d48ad4",False),
    (61,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"ac95b687bdf0d6fbcc9773bcc0eeeb1d57598e2034919156fd52b74ae193334e",False),
    (71,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"a4f518e1de9057497b0f539e9ac7a56b6fe8f3837f1552e658507fce836b63ea",False),
    (81,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"fc84ea411bd02914ae6224a2d2d9d791c441d9e22aa8d98fcc3cf86ca873f428",False),
    (91,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"24e11382846108112996d872d7e1615a2762babdef71418d691d66ce76f9edf9",False),
    (101,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"1c15054669a63438a3c7570c90c082a7b37b13c8a828125a1de100092ab74379",False),
    (121,"MAGIC_StatusRecovery","563ba971f2073415ac2fd0370498070737a8f831331b4516c500adaff2cc050d",1,8,0,None,2,"1e1072e994d2faba2c882ec838ea143ba57ce88cc5f0757f433cc28384e33e8b",False),
    (139,"MAGIC_StatusChange","cf577a259d8fa201c0311da5148f7ad8c52bbe6fc4796e5c1c8282f53a94e799",1,8,0,None,15,"b8c793be8f9dfdd1c27e7f0cfdf11144d1bcc9652dac62926b03c6cad01f5a95",False),
    (159,"MAGIC_StatusChange","cf577a259d8fa201c0311da5148f7ad8c52bbe6fc4796e5c1c8282f53a94e799",1,8,0,None,15,"8eb7bdfe4f29de0b6e433eb76e81e8ca2d33a3f86ad743a571fcd56f4bff17a1",False),
    (169,"MAGIC_StatusChange","cf577a259d8fa201c0311da5148f7ad8c52bbe6fc4796e5c1c8282f53a94e799",1,8,0,None,15,"296bde1ddf6cbdadfdbbe5f7d8859fb2565ddc344656fec5d79d5f32c4a36442",False),
    (179,"MAGIC_StatusChange","cf577a259d8fa201c0311da5148f7ad8c52bbe6fc4796e5c1c8282f53a94e799",1,8,0,None,15,"2d1dfbe7933c69f7a52141db899fee139b9ad970d83b115d8f0f1543a03f8e36",False),
    (189,"MAGIC_StatusChange","cf577a259d8fa201c0311da5148f7ad8c52bbe6fc4796e5c1c8282f53a94e799",1,8,0,None,15,"3457f9a963785728cf910ee3f20c82ca0651b3c916ff76c37b42fde650e6893a",False),
    (240,"MAGIC_AttReverse","8c2e6d0e960a00c086a3812027e4df6792eca99b6f21b3e3791e8cdeddd64b0f",1,1,0,None,0,"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",False),
    (306,"MAGIC_AttMagic","1825266675c7a6789c3ae9c34a3c64a812593cde870b35d09e42568e30323e60",1,11,0,13,8,"60c3583c265729a2c7233b5c303ef4542931ff3d5dbfa08f592504486691fcac",False),
)


def combined_magic_ids():
    if EXPECTED_EXACT_ROWS is None:
        raise ValueError("Combined exact-row reference must be pinned first")
    return tuple(sorted({
        int(magic_id)
        for row in EXPECTED_EXACT_ROWS
        for magic_id in row[12]
    }))


def _ascii_function(raw:bytes)->str:
    try:
        token=bytes(raw).decode("ascii","strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Combined selected magic function token is not ASCII") from exc
    if not token.startswith("MAGIC_"):
        raise ValueError("Combined selected magic function token lacks MAGIC_ prefix")
    return token


def analyze_parsed_rows(
    parsed,
    malformed,
    *,
    expected_exact_rows=EXPECTED_EXACT_MAGIC_ROWS,
):
    by_id={}
    for fields,values in parsed:
        magic_id=int(values["ID"])
        if magic_id in by_id:
            raise ValueError(f"duplicate recovered magic ID {magic_id}")
        by_id[magic_id]=(fields,values)

    source_ids=combined_magic_ids()
    ids_match=source_ids==EXPECTED_MAGIC_IDS
    rows=[]
    missing=[]
    for magic_id in EXPECTED_MAGIC_IDS:
        record=by_id.get(int(magic_id))
        if record is None:
            missing.append(int(magic_id))
            continue
        fields,values=record
        if len(fields)<4:
            raise ValueError(f"magic {magic_id} lacks function/option columns")
        function=_ascii_function(fields[2])
        option=bytes(fields[3])
        function_raw=bytes(fields[2])
        rows.append({
            "id":int(magic_id),
            "function":function,
            "function_sha256":hashlib.sha256(function_raw).hexdigest(),
            "field":int(values["FIELD"]),
            "target":int(values["TARGET"]),
            "target_deadflg":int(values["TARGET_DEADFLG"]),
            "idx":None if values.get("IDX") is None else int(values["IDX"]),
            "option_bytes":len(option),
            "option_sha256":hashlib.sha256(option).hexdigest(),
            "option_contains_nul":b"\0" in option,
        })

    exact_rows_closed=False
    if expected_exact_rows is not None:
        actual=tuple(
            (
                row["id"],row["function"],row["function_sha256"],
                row["field"],row["target"],row["target_deadflg"],row["idx"],
                row["option_bytes"],row["option_sha256"],
                row["option_contains_nul"],
            )
            for row in rows
        )
        exact_rows_closed=actual==tuple(expected_exact_rows)

    return {
        "combined_magic_ids":source_ids,
        "ids_match":ids_match,
        "rows":tuple(rows),
        "missing":tuple(missing),
        "malformed":int(malformed),
        "population_closed":bool(
            ids_match
            and not missing
            and len(rows)==len(EXPECTED_MAGIC_IDS)
            and int(malformed)==0
        ),
        "exact_rows_closed":exact_rows_closed,
    }


def analyze(data_dir:Path):
    data_dir=Path(data_dir)
    path=data_dir/"magic.txt"
    if not path.is_file():
        raise ValueError("recovered25 magic.txt not found")
    _,parsed,malformed,_,_=parse_magic(path)
    result=analyze_parsed_rows(parsed,malformed)
    digest=sha256(path)
    if (
        EXPECTED_MAGIC_SHA256 is not None
        and digest!=EXPECTED_MAGIC_SHA256
    ):
        raise ValueError("recovered25 magic.txt full-file hash drift")
    return result,digest


def emit(result,digest):
    print("StoneAge recovered25 Combined selected-magic cross-link — R1")
    print("No recovered names/comments/raw magic OPTION text or assets stored.")
    print(f"COUNT|combined_magic_ids|{len(result['combined_magic_ids'])}")
    print(f"COUNT|magic_rows_matched|{len(result['rows'])}")
    print(f"COUNT|magic_parse_malformed|{result['malformed']}")
    for row in result["rows"]:
        idx="NONE" if row["idx"] is None else str(row["idx"])
        print(
            "COMBINED_MAGIC_ROW|"
            f"id={row['id']}|function={row['function']}|"
            f"function_sha256={row['function_sha256']}|"
            f"field={row['field']}|target={row['target']}|"
            f"target_deadflg={row['target_deadflg']}|idx={idx}|"
            f"option_bytes={row['option_bytes']}|"
            f"option_sha256={row['option_sha256']}|"
            f"option_contains_nul={int(row['option_contains_nul'])}"
        )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_MAGIC_CROSSLINK_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_MAGIC_EXACT_ROWS_"
        +("CLOSED" if result["exact_rows_closed"] else "OPEN")
    )
    print("DATA_SHA256|file=magic|sha256="+digest)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    args=ap.parse_args()
    result,digest=analyze(args.data_dir)
    emit(result,digest)
    if not result["population_closed"]:
        raise SystemExit("Combined selected-magic cross-link drift")
    if (
        EXPECTED_EXACT_MAGIC_ROWS is not None
        and not result["exact_rows_closed"]
    ):
        raise SystemExit("Combined selected-magic exact row drift")


if __name__=="__main__":
    main()
