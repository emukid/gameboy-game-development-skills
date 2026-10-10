#!/usr/bin/env python3
"""Capture a bounded emulator run. This does not prove gameplay correctness."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--frames", type=int, default=180)
    parser.add_argument("--model", choices=("dmg", "cgb"), default="dmg")
    parser.add_argument("--screenshot", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.frames <= 36000:
        parser.error("frames must be in 1..36000")
    if args.screenshot.exists():
        parser.error("screenshot already exists")
    from pyboy import PyBoy
    boy = PyBoy(str(args.rom), window="null", sound_emulated=False, cgb=args.model == "cgb")
    try:
        boy.set_emulation_speed(0)
        if not boy.tick(args.frames, render=True):
            raise RuntimeError("emulator stopped early")
        screen = boy.screen.image
        with args.screenshot.open("xb") as output:
            screen.save(output, format="PNG")
        print(json.dumps({"pyboy": importlib.metadata.version("pyboy"),
                          "model": args.model, "frames": args.frames,
                          "rom_sha256": hashlib.sha256(args.rom.read_bytes()).hexdigest(),
                          "screen_sha256": hashlib.sha256(screen.tobytes()).hexdigest(),
                          "distinct_colors": len(set(screen.getdata())),
                          "gameplay_verified": False}, indent=2))
    finally:
        boy.stop(save=False)


if __name__ == "__main__":
    main()
