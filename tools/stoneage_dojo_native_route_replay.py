"""Run the preserved GMSV dojo instruction paths to the warp call boundary.

Install Unicorn 2.1.4 and pass the directory containing the private, CRC-verified
gmsv.exe and data/npc/doujyou. JSON output contains only numeric traces and hashes.
The harness supplies character, battle, equipment, map and CRT test doubles.
It stops before the actual warp function and does not start the server.
"""

import argparse
import hashlib
import json
import re
import struct
import sys
from collections import Counter
from pathlib import Path

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_32, Uc
from unicorn.x86_const import (
    UC_X86_REG_EAX,
    UC_X86_REG_EBP,
    UC_X86_REG_EIP,
    UC_X86_REG_ESP,
)

ROOT = Path(__file__).resolve().parents[1]
GMSV_SHA256 = "d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00"
CREATE_SHA256 = "ac3e46dc64d2e478cba4a115e15c2d32d3193c38e9de85f53ce8b06f3d99d925"

DATA = 0x3000000
FRAME = 0x3180000
RETURN = 0x3100000
NPC = 12
PLAYER = 24
WARP = 0x440730


def p32(*xs):
    return struct.pack("<" + "I" * len(xs), *(x & 0xFFFFFFFF for x in xs))


def create(pe):
    u = Uc(UC_ARCH_X86, UC_MODE_32)
    u.mem_map(0x400000, 0x1AC000)
    u.mem_map(0x2031000, 0x1000)
    u.mem_map(DATA, 0x200000)
    for va, offset, size in (
        (0x401000, 0x400, 0x15A598),
        (0x55C000, 0x15AA00, 0x3406C),
        (0x591000, 0x18EC00, 0x19D88),
    ):
        u.mem_write(va, pe[offset : offset + size])
    return u


def run(pe, kind, raw, target, center=(406, 126), mode="positive"):
    u = create(pe)
    eip = 0x492BAA if kind == "enemy" else 0x490EE0
    trace = []
    calls = Counter()
    work = {}
    if kind == "enemy":
        u.reg_write(UC_X86_REG_EBP, FRAME)
        u.reg_write(UC_X86_REG_ESP, FRAME - 0x10A00)
        u.mem_write(FRAME + 8, p32(NPC, NPC))
        u.mem_write(FRAME - 0x8018, raw + b"\0")
        u.mem_write(0x2031A90, p32(DATA + 0x2000))
        u.mem_write(DATA + 0x20AC, p32(PLAYER))
    else:
        previous = center if mode == "same_position" else (center[0] - 1, center[1])
        u.mem_write(DATA + 0x3000, p32(*previous))
        u.reg_write(UC_X86_REG_ESP, FRAME)
        u.mem_write(
            FRAME,
            p32(
                RETURN,
                2,
                3,
                0 if mode == "wrong_event" else 1,
                *center,
                0,
                DATA + 0x3000,
            ),
        )
    steps = 0
    stop = None
    dest = None
    raw_exit = None

    def cstr(ptr, limit=32768):
        return bytes(u.mem_read(ptr, limit)).split(b"\0", 1)[0]

    def num(p):
        m = re.match(rb"\s*[+-]?[0-9]+", cstr(p))
        return int(m.group()) if m else 0

    def intercept(_, address, size, data):
        nonlocal steps, stop, dest, raw_exit
        steps += 1
        if address in (
            0x492BC3,
            0x4930B6,
            0x492C96,
            0x495673,
            0x4956F0,
            0x495CF2,
            0x490F9D,
            0x490D2C,
            0x490A46,
            0x490C02,
        ):
            trace.append(hex(address))
        sp = u.reg_read(UC_X86_REG_ESP)
        if address in (0x4930B6, 0x492C96):
            expected = [None, None, None] if b"dieact:0" in raw else target
            assert [work.get((NPC, slot)) for slot in (0x55, 0x56, 0x57)] == expected
            u.mem_write(FRAME + 8, p32(0, NPC))
            u.reg_write(UC_X86_REG_EIP, 0x495600)
            return
        if address in (RETURN, 0x495D66, WARP):
            stop = hex(address)
            if address == WARP:
                args = struct.unpack("<7I", u.mem_read(sp, 28))
                raw_exit = [args[0] - 5, args[3]]
                dest = list(args[4:])
                assert args[3] == PLAYER
            u.emu_stop()
            return
        stubs = {
            0x55AFF0: "strlen",
            0x55B130: "strstr",
            0x55AE70: "strcpy",
            0x55B150: "memcpy",
            0x55AF60: "memset",
            0x55AFE0: "atoi",
            0x42DE30: "setWorkInt",
            0x42DDC0: "getWorkInt",
            0x42D960: "checkIndex",
            0x42C720: "dischargeParty",
            0x416D80: "getObjectType",
            0x416F50: "getObjectIndex",
            0x42DB90: "getCharInt",
            0x48F160: "loadArg",
            0x4F4ED0: "mapCoordinateBoundary",
            0x40E730: "equipmentState",
            0x55AD30: "getreent",
            0x55AF50: "fprintf",
        }
        name = stubs.get(address)
        if name is None:
            return
        calls[name] += 1
        ret, a, b, c, d, e = struct.unpack("<6I", u.mem_read(sp, 24))
        result = 0
        if name == "strlen":
            result = len(cstr(a))
        elif name == "strstr":
            i = cstr(a).find(cstr(b))
            result = a + i if i >= 0 else 0
        elif name == "strcpy":
            u.mem_write(a, cstr(b) + b"\0")
            result = a
        elif name == "memset":
            u.mem_write(a, bytes([b & 255]) * c)
            result = a
        elif name == "memcpy":
            u.mem_write(a, bytes(u.mem_read(b, c)))
            result = a
        elif name == "atoi":
            result = num(a)
        elif name == "setWorkInt":
            work[(c, d)] = e
        elif name == "getWorkInt":
            result = work.get((c, d), 0)
        elif name == "checkIndex":
            result = int(c == PLAYER)
        elif name == "getObjectType":
            result = 0 if mode == "wrong_object" else 1
        elif name == "getObjectIndex":
            result = {2: NPC, 3: PLAYER}[a]
        elif name == "getCharInt":
            values = {
                (PLAYER, 0x36): 1,
                (NPC, 5): center[0] + int(mode == "wrong_x"),
                (NPC, 6): center[1],
                (PLAYER, 4): 3021,
                (PLAYER, 0x6E): 0,
            }
            result = values.get((a, b), 0)
        elif name == "loadArg":
            assert a == NPC and len(raw) < c
            u.mem_write(b, raw + b"\0")
            result = 1
        elif name == "mapCoordinateBoundary":
            result = int(a == 3022 and 0 <= b < 15 and 0 <= c < 15)
        elif name == "getreent":
            result = DATA + 0x6000
        u.reg_write(UC_X86_REG_EAX, result)
        u.reg_write(UC_X86_REG_ESP, sp + 4)
        u.reg_write(UC_X86_REG_EIP, ret)

    u.hook_add(UC_HOOK_CODE, intercept)
    try:
        u.emu_start(eip, 0, count=50000)
    except Exception as e:
        raise RuntimeError((hex(u.reg_read(UC_X86_REG_EIP)), calls, trace)) from e
    assert stop is not None, (hex(u.reg_read(UC_X86_REG_EIP)), calls, trace)
    return dict(
        target=dest,
        stop=stop,
        native_instruction_hooks=steps,
        trace=trace,
        stub_calls=dict(calls),
        site_player=raw_exit,
    )


def replay(original):
    pe = (original / "gmsv.exe").read_bytes()
    if hashlib.sha256(pe).hexdigest() != GMSV_SHA256:
        raise ValueError("GMSV SHA-256 differs from the authenticated source")
    report = (
        ROOT
        / "research/recovered/STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json"
    )
    prior = json.loads(report.read_bytes())["floor3021"]["original_NPCEnemy_ARG_route"][
        "rows"
    ]
    cases = []
    args = sorted((original / "data/npc/doujyou").glob("jyajyadou*.arg"))
    assert len(args) == 100
    for i, p in enumerate(args, 1):
        raw = p.read_bytes()
        rows = dict(line.split(b":", 1) for line in raw.splitlines())
        assert int(rows[b"gym"]) == i
        if hashlib.sha256(raw).hexdigest() != prior[i - 1][6]:
            raise ValueError(f"ARG {i} SHA-256 differs from the authenticated source")
        target = [int(rows[k]) for k in (b"warpfl", b"warpx", b"warpy")]
        flat = b"|".join(raw.splitlines())
        replay = run(pe, "enemy", flat, target)
        assert replay["target"] == target, (i, replay)
        cases.append(
            dict(ordinal=i, source_sha256=hashlib.sha256(raw).hexdigest(), **replay)
        )
    create = (original / "data/npc/doujyou/jyajyadou.create").read_bytes()
    if hashlib.sha256(create).hexdigest() != CREATE_SHA256:
        raise ValueError("CREATE SHA-256 differs from the authenticated source")
    matches = re.findall(
        rb"\{\s*floorid=3021\s+borncenter=(\d+),(\d+),1,1\s+[^{}]*?enemy=npcgen_warp\|([^\r\n]+)\s*\}",
        create,
    )
    assert len(matches) == 200
    warp = []
    for x, y, source in matches:
        args = list(map(int, source.split(b"|")))
        assert args == [3022, 1, 7]
        center = (int(x), int(y))
        case = run(pe, "warp", source, args, center)
        assert case["target"] == args, case
        warp.append(dict(center=list(center), **case))
    negative = {}
    for mode in ("same_position", "wrong_event", "wrong_object", "wrong_x"):
        neg = run(pe, "warp", matches[0][2], [3022, 1, 7], mode=mode)
        assert neg["target"] is None, neg
        negative[mode] = neg
    neg = run(
        pe,
        "enemy",
        b"|".join(
            (original / "data/npc/doujyou/jyajyadou001.arg").read_bytes().splitlines()
        ).replace(b"dieact:1", b"dieact:0"),
        [3021, 400, 114],
    )
    assert neg["target"] is None and neg["stop"] == "0x495d66", neg
    negative["dieact_zero_synthetic"] = neg
    neg = run(pe, "warp", b"3022|15|7", [3022, 15, 7])
    assert neg["target"] is None and neg["stub_calls"]["mapCoordinateBoundary"] == 1, (
        neg
    )
    negative["out_of_bounds_synthetic"] = neg
    return {
        "gmsv_sha256": GMSV_SHA256,
        "create_sha256": CREATE_SHA256,
        "enemy": cases,
        "warp": warp,
        "negative": negative,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gmsv_directory", type=Path)
    args = parser.parse_args()
    json.dump(replay(args.gmsv_directory), sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
