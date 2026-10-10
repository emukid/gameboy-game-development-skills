---
name: gameboy-design
description: Design implementable Game Boy or Game Boy Color homebrew games, including controls, game states, tile graphics, memory budgets, and emulator acceptance criteria. Use before implementing a new ROM or a substantial gameplay change.
---

# Game Boy design

Turn the user's game idea into a concrete buildable design. Preserve their genre, mechanics, and requested scale. For an unspecified target, choose DMG-compatible Game Boy, GBDK-2020 C, and a 32 KiB ROM-only cartridge for the first playable version. These are defaults, not limits: choose banking when the actual game needs it. Game Boy Advance is a separate platform.

Inspect existing design and source before replacing decisions. Ask only about choices that materially alter the game; otherwise state assumptions and proceed. For a request to build a game, continue into implementation after designing it.

Write `GAME_DESIGN.md` (or update the project's equivalent) with:

- Player goal and core loop; exact win, lose, and restart conditions.
- Controls including held versus newly pressed buttons; title, play, pause, and ending transitions where relevant.
- Screen layout in 160×144 pixels: world, camera, HUD, sprite bounds, and collision coordinate system.
- Concrete content: levels, opponents, scoring, pacing, and feedback. Choose an achievable first playable slice without silently dropping requested features.
- Asset plan: tile IDs, background map, sprite/metasprite dimensions, palettes, animation frames, text glyphs, sound effects, music channel ownership.
- Hardware budget and cartridge plan using [hardware.md](references/hardware.md). Distinguish estimates from linker/profiler measurements.
- Deterministic acceptance cases: boot, each control, collision and boundary cases, win/lose, restart, and save/reload if present. Specify expected visible results or game-state values, not just “runs.”

Use integer or fixed-point simulation with one deliberate tick cadence. Define diagonal speed, collision response, and camera behavior explicitly when relevant. Account for many objects sharing one scanline, not only the total sprite count.

Handoff should identify source modules, asset inputs, build target, emulator model, and test scenarios. If the companion `gameboy-build` skill is installed, use it for implementation; otherwise follow the selected toolchain's official instructions. Do not treat a design document as a compiled ROM.
