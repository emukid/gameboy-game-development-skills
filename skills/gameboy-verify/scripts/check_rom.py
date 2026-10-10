#!/usr/bin/env python3
"""Check standard Game Boy homebrew ROM structure; no runtime claims."""
import argparse
import hashlib
import json
from pathlib import Path

LOGO = bytes.fromhex(
    "CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D "
    "00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99 "
    "BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E")
ROM_SIZES = {i: 32768 << i for i in range(9)}
ROM_SIZES.update({0x52: 72 * 16384, 0x53: 80 * 16384, 0x54: 96 * 16384})
RAM_SIZES = {0: 0, 1: 2048, 2: 8192, 3: 32768, 4: 131072, 5: 65536}
# type: (family, maximum ROM bytes, external RAM allowed, maximum RAM bytes)
CARTS = {
    0x00: ("ROM", 32768, False, 0),
    0x08: ("ROM+RAM", 32768, True, 8192),
    0x09: ("ROM+RAM+BATTERY", 32768, True, 8192),
    0x01: ("MBC1", 2097152, False, 0),
    0x02: ("MBC1+RAM", 2097152, True, 32768),
    0x03: ("MBC1+RAM+BATTERY", 2097152, True, 32768),
    0x05: ("MBC2", 262144, False, 0),
    0x06: ("MBC2+BATTERY", 262144, False, 0),
    0x0F: ("MBC3+TIMER+BATTERY", 2097152, False, 0),
    0x10: ("MBC3+TIMER+RAM+BATTERY", 2097152, True, 32768),
    0x11: ("MBC3", 2097152, False, 0),
    0x12: ("MBC3+RAM", 2097152, True, 32768),
    0x13: ("MBC3+RAM+BATTERY", 2097152, True, 32768),
    0x19: ("MBC5", 8388608, False, 0),
    0x1A: ("MBC5+RAM", 8388608, True, 131072),
    0x1B: ("MBC5+RAM+BATTERY", 8388608, True, 131072),
    0x1C: ("MBC5+RUMBLE", 8388608, False, 0),
    0x1D: ("MBC5+RUMBLE+RAM", 8388608, True, 65536),
    0x1E: ("MBC5+RUMBLE+RAM+BATTERY", 8388608, True, 65536),
}


def inspect(data):
    result = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "errors": []}
    errors = result["errors"]
    if len(data) < 0x150:
        errors.append("file is shorter than the cartridge header")
        return result
    size, ram, cart = data[0x148], data[0x149], data[0x147]
    color = data[0x143]
    result.update(title=data[0x134:0x143 if color & 0x80 else 0x144].split(b"\0")[0].decode("ascii", "replace"),
                  cartridge_type=f"0x{cart:02X}", cgb_flag=f"0x{color:02X}",
                  declared_rom_bytes=ROM_SIZES.get(size), declared_ram_bytes=RAM_SIZES.get(ram))
    if data[0x104:0x134] != LOGO:
        errors.append("Nintendo logo mismatch")
    if ROM_SIZES.get(size) != len(data):
        errors.append("ROM size code is unknown or does not match file length")
    checksum = 0
    for value in data[0x134:0x14D]:
        checksum = (checksum - value - 1) & 0xFF
    if checksum != data[0x14D]:
        errors.append("header checksum mismatch")
    total = (sum(data) - data[0x14E] - data[0x14F]) & 0xFFFF
    if total != int.from_bytes(data[0x14E:0x150], "big"):
        errors.append("global checksum mismatch")
    if ram not in RAM_SIZES:
        errors.append("unknown RAM size code")
    if cart not in CARTS:
        errors.append("unsupported cartridge type; requires mapper-specific verification")
    else:
        family, max_rom, has_ram, max_ram = CARTS[cart]
        result["mapper"] = family
        if len(data) > max_rom:
            errors.append("ROM exceeds mapper capacity")
        if has_ram != (ram != 0):
            errors.append("external RAM size conflicts with cartridge type (MBC2 uses internal RAM)")
        if RAM_SIZES.get(ram, 0) > max_ram:
            errors.append("RAM exceeds mapper capacity")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.rom.read_bytes())
    except OSError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))


if __name__ == "__main__":
    main()
