"""Replay only authenticated recovery callbacks under a bounded x86 emulator.

The caller supplies an exact-image reader. Engine helpers, state, inventory,
random numbers and libc operations are fixtures. No historical executable
startup, network, battle resolution, or native inventory mutation takes place.
"""
import re
import struct

CODE = ((0x4fe4d0, 0x500630), (0x559140, 0x5594b0))
DATA = ((0x588970, 0x588a10), (0x5a4e98, 0x5a4ee6), (0x5a5376, 0x5a54c0), (0x5aa896, 0x5aa8c0))
OPTIONS = 0x700000
STOP = 0x700fff
STACK = 0x800000
CASTER = 8
SLOT = 7
DEFAULT_TARGET = 9
FIELD = 0
BATTLE_INIT = 1
BATTLE = 2
X87_RESET_CONTROL = 0x037f


def trial(take, option, battle_mode, *, hp=100, mp=10, max_hp=1000, max_mp=100, target_kind=1,
          rand=0, can_cure=1, battle_position=2, target=DEFAULT_TARGET, caster_valid=True, item_valid=True):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_FPCW

    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.reg_write(UC_X86_REG_FPCW, X87_RESET_CONTROL)  # x87 reset control word fixture
    pages = set()

    def write(address, data):
        for page in range(address & ~0xfff, (address + len(data) + 0xfff) & ~0xfff, 0x1000):
            if page not in pages:
                uc.mem_map(page, 0x1000, UC_PROT_READ | UC_PROT_EXEC)
                pages.add(page)
        uc.mem_write(address, data)

    for first, end in CODE + DATA:
        write(first, take(first, end - first))
    write(OPTIONS, option.encode('cp950') + b'\0')
    write(STOP, b'\xcc')
    uc.mem_map(STACK, 0x4000, UC_PROT_READ | UC_PROT_WRITE)
    stack = STACK + 0x3f00
    uc.mem_write(stack, struct.pack('<4I', STOP, CASTER, target, SLOT))
    uc.reg_write(UC_X86_REG_ESP, stack)
    stats = {4: 0, 5: 0, 6: 0, 10: hp, 11: mp, 0x36: target_kind}
    work = {0: battle_mode, 1: 4, 13: max_hp, 14: max_mp, 0x46: 0, 0x3f: 0}
    changes, battle_requests, deleted, ran = [], [], [], []

    def cstring(address):
        raw = bytearray()
        for offset in range(256):
            value = uc.mem_read(address + offset, 1)
            if value == b'\0':
                return bytes(raw)
            raw.extend(value)
        raise ValueError('Unterminated fixture string')

    def args(count):
        addr = uc.reg_read(UC_X86_REG_ESP) + 4
        return struct.unpack('<' + 'i' * count, uc.mem_read(addr, 4 * count))

    def log_values(out, count):
        out.append(list(args(count)))

    def scan():
        ptr, fmt, out = args(3)
        if cstring(fmt) != b'%d':
            raise ValueError('Unexpected scanf format')
        match = re.match(rb'\s*[+-]?\d+', cstring(ptr))
        if match:
            uc.mem_write(out, struct.pack('<i', int(match[0])))
        return bool(match)

    def search():
        haystack, needle = args(2)
        found = cstring(haystack).find(cstring(needle))
        return haystack + found if found >= 0 else 0

    def read_stat():
        _, field = args(2)
        return stats[field]

    def set_stat():
        _, _, who, field, amount = args(5)
        changes.append([who, field, amount])
        stats[field] = amount
        return 1

    def roll():
        ran.append(rand)
        return rand

    # Only calls reached by the ordinary recovery and boundary fixtures.
    # Battle settling, messaging, logging and inventory writes stop at these stubs.
    callbacks = {
        0x42d960: lambda: caster_valid, 0x42ddc0: lambda: work[args(4)[3]], 0x42e2e0: lambda: 1,
        0x4f71b0: lambda: item_valid, 0x4f76e0: lambda: OPTIONS if args(2)[1] == 3 else 0,
        0x55b130: search, 0x55afd0: scan, 0x55b030: roll, 0x42db90: read_stat,
        0x42dcf0: set_stat, 0x4335f0: lambda: can_cure,
        0x5178c0: lambda: battle_position, 0x548eb0: lambda: log_values(battle_requests, 8),
        0x433ab0: lambda: log_values(deleted, 6),
        0x438840: lambda: None, 0x43af80: lambda: None, 0x43d9d0: lambda: None,
        0x471f90: lambda: None, 0x4f7500: lambda: 0, 0x42dc30: lambda: 0,
        0x417f40: lambda: None, 0x55ae20: lambda: 0,
        0x43f040: lambda: OPTIONS, 0x42ea10: lambda: -1, 0x55b000: lambda: None,
    }
    for address in callbacks:
        write(address, b'\xc3')

    def code_hook(cpu, address, _size, _):
        if address in callbacks:
            result = callbacks[address]()
            cpu.reg_write(UC_X86_REG_EAX, result or 0)
        elif not any(first <= address < end for first, end in CODE):
            cpu.emu_stop()
            raise RuntimeError(f'Unmapped executable path {address:#x}')

    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.emu_start(0x500590, STOP, count=6000)
    if uc.reg_read(UC_X86_REG_EIP) != STOP:
        raise RuntimeError('Instruction bound exceeded')
    return {'changes': changes, 'battle_requests': battle_requests, 'deleted': [x[2:6] for x in deleted],
            'rand_calls': len(ran)}
