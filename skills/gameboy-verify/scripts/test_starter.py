#!/usr/bin/env python3
"""Exercise the unchanged gameboy-build starter using real emulator input."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--symbols", type=Path, required=True)
    parser.add_argument("--screenshot", type=Path, required=True)
    args = parser.parse_args()
    if args.screenshot.exists():
        parser.error("screenshot already exists")
    symbols = {}
    for line in args.symbols.read_text().splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0] == "DEF":
            symbols[parts[1]] = int(parts[2], 16)
    for name in ("game_state", "player_x", "player_y", "collected"):
        if not 0xC000 <= symbols.get("_" + name, 0) < 0xE000:
            parser.error(f"missing WRAM symbol: {name}")
    from pyboy import PyBoy
    boy = PyBoy(str(args.rom), window="null", sound_emulated=False, cgb=False)
    checks = []

    def read(name):
        return boy.memory[symbols["_" + name]]

    def tick(frames):
        if not boy.tick(frames, render=True):
            raise AssertionError("emulator stopped early")

    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    def hold(button, frames):
        boy.button_press(button)
        tick(frames)
        boy.button_release(button)
        tick(2)

    def travel(name, target, negative, positive):
        value = read(name)
        if value != target:
            hold(positive if value < target else negative, abs(target - value))
        check(read(name) == target, f"{name} reaches {target}")

    try:
        boy.set_emulation_speed(0)
        tick(180)
        check(read("game_state") == 0 and read("player_x") == 24, "boot enters title")
        hold("right", 10)
        check(read("player_x") == 24, "title ignores movement")
        hold("start", 1)
        check(read("game_state") == 1 and read("collected") == 0, "Start enters play")
        initial_screen = boy.screen.image.tobytes()
        boy.button_press("start")
        hold("right", 10)
        boy.button_release("start")
        tick(2)
        check(read("player_x") == 34, "held Start does not reset play")
        check(boy.screen.image.tobytes() != initial_screen, "movement changes rendered screen")
        hold("left", 200)
        check(read("player_x") == 0, "left boundary clamps without wrap")
        hold("up", 200)
        check(read("player_y") == 0, "upper boundary clamps without wrap")
        hold("right", 200)
        check(read("player_x") == 152, "right boundary clamps")
        hold("down", 200)
        check(read("player_y") == 136, "lower boundary clamps")
        for count, (x, y) in enumerate(((120, 64), (32, 32), (120, 112)), 1):
            travel("player_x", x, "left", "right")
            if count == 3:
                travel("player_y", y - 8, "up", "down")
                check(read("collected") == 2, "touching target edge does not collect")
                hold("down", 1)
            else:
                travel("player_y", y, "up", "down")
            check(read("collected") == count, f"target {count} collected exactly once")
        check(read("game_state") == 2, "third target enters win")
        check(boy.memory[0xFF47] == 0x1B, "win changes background palette")
        check(boy.memory[0xFE04] == 0, "win hides target in hardware OAM")
        hold("start", 1)
        check(read("game_state") == 1 and read("collected") == 0 and
              read("player_x") == 24 and read("player_y") == 64, "restart resets run")
        check(boy.memory[0xFF47] == 0xE4, "restart restores palette")
        check(boy.memory[0xFE04] == 80 and boy.memory[0xFE05] == 128,
              "restart renders first target at expected OAM position")
        with args.screenshot.open("xb") as output:
            boy.screen.image.save(output, format="PNG")
        print(json.dumps({"pyboy": importlib.metadata.version("pyboy"), "model": "DMG",
                          "rom_sha256": hashlib.sha256(args.rom.read_bytes()).hexdigest(),
                          "checks": checks, "passed": len(checks)}, indent=2))
    finally:
        boy.stop(save=False)


if __name__ == "__main__":
    main()
