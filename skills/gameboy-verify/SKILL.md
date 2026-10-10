---
name: gameboy-verify
description: Validate compiled Game Boy ROM headers and test gameplay in an emulator. Use after building a .gb or .gbc file, diagnosing boot failures, or checking controls, state transitions, and release artifacts.
---

# Verify a Game Boy ROM

Separate build success, structural ROM validity, and gameplay evidence. None proves the others. Read the game design and derive concrete acceptance cases before testing.

## Structural checks

Run `python3 <skill>/scripts/check_rom.py path/to/game.gb`. It checks logo bytes, declared ROM length, header checksum, global checksum, and basic cartridge constraints for ROM-only, MBC1, MBC2, MBC3, and MBC5. It reports unsupported mapper types instead of claiming they are valid. A global checksum failure violates this suite's build-integrity gate even though ordinary Game Boy hardware does not enforce it.

Compare reported mapper, RAM, and CGB flag to the intended target. The checker cannot establish bank-access correctness, entry execution, save behavior, or graphics timing. For exotic mappers, use the documented mapper-specific rules and emulator support instead of weakening the standard checker silently.

## Boot and gameplay

Use a debugger-capable emulator such as Emulicious or SameBoy when available, or PyBoy for repeatable headless inputs. Read [emulator-testing.md](references/emulator-testing.md) for exact procedures and limits.

Install the dependencies with `python -m pip install -r <skill>/scripts/requirements.txt` in a virtual environment.

`python3 <skill>/scripts/smoke_rom.py game.gb --frames 180 --screenshot boot.png` runs a generic bounded boot/capture check with PyBoy. It reports screen diversity and a screen hash; it does **not** assert that a game works or that a title screen is correct. Use unique output paths; the script refuses to overwrite screenshots.

For the unchanged bundled `gameboy-build` starter, use:

```sh
python3 <skill>/scripts/test_starter.py project/build/game.gb --symbols project/build/game.noi --screenshot play.png
```

This starter-specific test drives real button input and asserts boot/title, Start edges, movement/clamping, collection, win, and restart using exported symbols. Do not apply those fixed expectations to a different game. Adapt scenarios from the actual design, resolve symbols from that build, and assert meaningful visible or state changes without patching RAM to bypass gameplay.

Test every claimed hardware mode and persistence feature. Inspect screenshots for layout and corruption; listen to audio when audio is present. Preserve exact commands, tool versions, emulator model, acceptance outcomes, ROM SHA-256, and limitations in a verification report. When no emulator is available, report “compiled and header-checked; gameplay unverified” and provide runnable checks. Do not claim successful play from a ROM's existence or a screenshot hash.
