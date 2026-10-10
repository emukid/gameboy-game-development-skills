# Game Boy Forge

Three Codex skills for designing, implementing, compiling, and testing original Game Boy homebrew ROMs.

| Skill | Use it for |
| --- | --- |
| [gameboy-design](skills/gameboy-design/SKILL.md) | Gameplay, controls, screen layout, assets, hardware budgets, acceptance cases |
| [gameboy-build](skills/gameboy-build/SKILL.md) | GBDK C implementation, tile conversion, scaffolding, reproducible ROM builds |
| [gameboy-verify](skills/gameboy-verify/SKILL.md) | Header checks, emulator input tests, screenshots, verification reports |

The default is DMG-compatible Game Boy with GBDK-2020 C. CGB, banking, audio, saves, and existing RGBDS projects have additional guidance. Game Boy Advance is a separate target. The included executable starter and automated gameplay tests cover DMG with a ROM-only cartridge.

## Use the skills

Copy each folder under `skills/` into `${CODEX_HOME:-$HOME/.codex}/skills/`, preserving scripts, references, and assets. Do not overwrite an existing customized skill without reviewing it. Start a new Codex session to discover newly installed skills. All three allow automatic selection, and can also be invoked explicitly:

```text
Use $gameboy-design to design a one-screen Game Boy arena game.
Use $gameboy-build to implement that design and compile the ROM.
Use $gameboy-verify to test the ROM against its acceptance cases.
```

For one request, ask the agent to use all three and deliver source plus the tested ROM. A design-only request stays design-only. The starter demonstrates a small collection game; agents should replace its mechanics and assets to match the actual request.

## Build and run the included game

Download and extract a host-matching [GBDK-2020 4.5.0 release](https://github.com/gbdk-2020/gbdk-2020/releases/tag/4.5.0). Python 3.9+ and Make are used below. Run from this repository:

```sh
python3 skills/gameboy-build/scripts/new_project.py /tmp/forge-demo
make -C /tmp/forge-demo GBDK_HOME=/absolute/path/to/gbdk
python3 skills/gameboy-verify/scripts/check_rom.py /tmp/forge-demo/build/game.gb
python3 -m venv /tmp/forge-verify
/tmp/forge-verify/bin/python -m pip install -r skills/gameboy-verify/scripts/requirements.txt
/tmp/forge-verify/bin/python skills/gameboy-verify/scripts/test_starter.py \
  /tmp/forge-demo/build/game.gb --symbols /tmp/forge-demo/build/game.noi \
  --screenshot /tmp/forge-play.png
```

Use new destination/screenshot paths when rerunning. On Windows use the virtual environment's `Scripts/python.exe` and the direct compilation command documented in the build skill if Make is unavailable.

Open [the compiled sample](artifacts/three-targets.gb) in a Game Boy emulator. Press Start, move with the D-pad, and collect three outlined targets. The background inverts on victory; Start restarts. The sample intentionally has no text, audio, saves, or lose state. Its complete source and design live in [the starter](skills/gameboy-build/assets/starter/).

## Evidence

See [VERIFICATION.md](VERIFICATION.md) for versions, hashes, commands, scope, and results. The suite includes actual compilation and emulator execution, malformed-ROM tests, pixel bitplane tests, and refusal to overwrite existing projects/assets. Run helper tests with:

```sh
python3 -m unittest discover -s tests -v
```

The toolchain and Python environment are local dependencies, not bundled skill content. No commercial game or proprietary boot ROM is needed.
