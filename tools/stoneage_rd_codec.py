#!/usr/bin/env python3
"""Legacy StoneAge/JSS RD image-block decoder.

Supports legacy RD flags 0 (raw indexed pixels) and 1
(JSS run-length/literal coding). Later color extensions are deliberately
rejected until independently specified.
"""

import hashlib
import struct

RD_HEADER_SIZE = 16


class RDDecodeError(ValueError):
    pass


def parse_rd_header(block: bytes):
    if len(block) < RD_HEADER_SIZE:
        raise RDDecodeError("RD block shorter than 16-byte header")
    if block[:2] != b"RD":
        raise RDDecodeError("missing RD magic")
    width_u, height_u, stored_size = struct.unpack_from("<III", block, 4)
    width_s, height_s = struct.unpack_from("<ii", block, 4)
    return {
        "flag": block[2],
        "unknown": block[3],
        "width_u": width_u,
        "height_u": height_u,
        "width_s": width_s,
        "height_s": height_s,
        "stored_size": stored_size,
    }


def _read_count(data: memoryview, pos: int, control: int, family_base: int):
    code = control & 0xF0
    if code == family_base:
        return control & 0x0F, pos
    if code == family_base + 0x10:
        if pos >= len(data):
            raise RDDecodeError("truncated 12-bit run length")
        return ((control & 0x0F) << 8) | data[pos], pos + 1
    if code == family_base + 0x20:
        if pos + 1 >= len(data):
            raise RDDecodeError("truncated 20-bit run length")
        count = ((control & 0x0F) << 16) | (data[pos] << 8) | data[pos + 1]
        return count, pos + 2
    raise RDDecodeError(f"invalid control byte 0x{control:02x}")


def decode_legacy_rle(encoded: bytes, expected_len: int | None = None) -> bytes:
    data = memoryview(encoded)
    out = bytearray()
    pos = 0

    while pos < len(data):
        control = data[pos]
        pos += 1
        family = control & 0xF0

        if family in (0x00, 0x10, 0x20):
            count, pos = _read_count(data, pos, control, 0x00)
            end = pos + count
            if end > len(data):
                raise RDDecodeError("truncated literal run")
            out.extend(data[pos:end])
            pos = end
        elif family in (0x80, 0x90, 0xA0):
            if pos >= len(data):
                raise RDDecodeError("truncated repeated-byte value")
            value = data[pos]
            pos += 1
            count, pos = _read_count(data, pos, control, 0x80)
            out.extend(bytes((value,)) * count)
        elif family in (0xC0, 0xD0, 0xE0):
            count, pos = _read_count(data, pos, control, 0xC0)
            out.extend(b"\x00" * count)
        else:
            raise RDDecodeError(f"invalid control byte 0x{control:02x}")

        if expected_len is not None and len(out) > expected_len:
            raise RDDecodeError(
                f"decoded output exceeds expected length: {len(out)} > {expected_len}"
            )

    if expected_len is not None and len(out) != expected_len:
        raise RDDecodeError(f"decoded length mismatch: {len(out)} != {expected_len}")
    return bytes(out)


def decode_rd_block(block: bytes, authoritative_block_size: int | None = None):
    header = parse_rd_header(block)
    width = header["width_s"]
    height = header["height_s"]
    if width <= 0 or height <= 0:
        raise RDDecodeError(
            f"special/non-image dimensions are not decodable: {width}x{height}"
        )

    pixel_count = width * height
    if authoritative_block_size is None:
        authoritative_block_size = len(block)
    if authoritative_block_size > len(block):
        raise RDDecodeError("authoritative block size exceeds available bytes")

    payload = block[RD_HEADER_SIZE:authoritative_block_size]
    if header["flag"] == 0:
        if len(payload) < pixel_count:
            raise RDDecodeError("raw RD payload shorter than pixel count")
        pixels = bytes(payload[:pixel_count])
    elif header["flag"] == 1:
        pixels = decode_legacy_rle(payload, pixel_count)
    else:
        raise RDDecodeError(
            f"unsupported RD flag {header['flag']}; only legacy 0/1 are supported"
        )
    return header, pixels


def decoded_sha256(pixels: bytes) -> str:
    return hashlib.sha256(pixels).hexdigest()
