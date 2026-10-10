#!/usr/bin/env python3
"""Convert rectangular 0..3 pixel rows to row-major Game Boy 2-bpp C tiles."""
import argparse
import re
from pathlib import Path


def encode(text):
    rows = text.splitlines()
    if not rows or not rows[0]:
        raise ValueError("image is empty")
    width = len(rows[0])
    if width % 8 or len(rows) % 8:
        raise ValueError("width and height must be multiples of eight")
    if any(len(row) != width or re.fullmatch(r"[0-3]+", row) is None for row in rows):
        raise ValueError("use equal-width rows containing only digits 0, 1, 2, 3")
    output = []
    for top in range(0, len(rows), 8):
        for left in range(0, width, 8):
            for row in rows[top:top + 8]:
                pixels = [int(p) for p in row[left:left + 8]]
                output.extend(sum(((p >> plane) & 1) << (7 - x)
                                  for x, p in enumerate(pixels)) for plane in (0, 1))
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--symbol", default="tiles")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", args.symbol):
        parser.error("symbol must be a C identifier starting with a letter")
    try:
        data = encode(args.source.read_text(encoding="ascii"))
        lines = [", ".join(f"0x{b:02X}" for b in data[i:i + 16])
                 for i in range(0, len(data), 16)]
        with args.output.open("x", encoding="ascii") as output:
            output.write("#include <stdint.h>\n\n")
            output.write(f"const uint8_t {args.symbol}[{len(data)}] = {{\n    ")
            output.write(",\n    ".join(lines) + "\n};\n")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"{len(data) // 16} tiles, {len(data)} bytes")


if __name__ == "__main__":
    main()
