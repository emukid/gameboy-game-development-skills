---
name: gameboy-build
description: Implement and compile Game Boy homebrew ROMs with GBDK-2020 C, including tile assets, input, gameplay, and reproducible builds. Use for creating a playable .gb file or extending an existing Game Boy project.
---

# Build a Game Boy ROM

Deliver source, generated assets, a repeatable build command, and the actual ROM. Preserve an existing engine/toolchain. Default new projects to GBDK-2020 C and DMG compatibility; if the user requests RGBDS assembly, use [toolchains.md](references/toolchains.md) instead of substituting C.

Read the project's design. If absent, establish controls, target hardware, core loop, terminal states, and restart behavior; use `gameboy-design` when available. Build the requested game, not merely the bundled demonstration.

## Start and compile

1. Locate the installed GBDK toolchain or obtain a host-matching archive from the [official releases](https://github.com/gbdk-2020/gbdk-2020/releases). Pin and record the version. The bundled starter is tested with 4.5.0. Use a project-local tool directory when no shared installation exists; do not silently replace system compilers.
2. For a new C project, scaffold with `python3 <skill>/scripts/new_project.py <destination>`. It refuses existing destinations. The copied starter is a complete small target-collection game that demonstrates title/play/win/restart, held movement, clamping, collision, tiles, and OAM. For an existing project, adapt its files directly.
3. Run `make -C <destination> GBDK_HOME=/absolute/path/to/gbdk`. The toolchain root contains `bin/lcc`; this is GBDK's driver, not an unrelated system `lcc`. `LCC=/absolute/path/to/lcc` is an alternative. On Windows use a make-capable shell or the direct command in [toolchains.md](references/toolchains.md).
4. Inspect diagnostics and map output. A successful host C compilation is not a Game Boy build. The deliverable is `build/game.gb` plus matching map/symbol files, not `.o` or `.ihx` alone.

## Implement the game

Use [implementation.md](references/implementation.md) for frame timing, graphics, input, collisions, sound, banking, and saves. Keep generated art reproducible from source. Start with a small playable vertical slice, then complete requested mechanics/content. Check each added state transition in an emulator.

For custom pixel art, `python3 <skill>/scripts/tiles.py art.txt tiles.c --symbol game_tiles` converts 0–3 digit rows into GBDK 2-bpp tile data. Width and height must be multiples of eight. Tiles are emitted left-to-right, top-to-bottom; no deduplication occurs, so map IDs remain predictable. PNG workflows can use GBDK `png2asset`; inspect its installed help for version-specific flags. Raster concept art must be reduced to the target palette and tile grid before it is a ROM asset.

Keep ROM constants `const`; avoid heap allocation and floating point in the frame loop. Use bounded arithmetic for movement and collision. Inspect ROM/WRAM usage before expanding assets. Do not “fix” overflow by changing header size without actually adding banks and correct bank access.

## Finish

Clean-build with the recorded toolchain. Validate header and cartridge configuration; boot and exercise the game using `gameboy-verify` if installed or an equivalent emulator procedure. Preserve a test report with emulator version/model, controls tested, expected versus observed outcomes, and artifact hash. Report untested audio, saves, CGB paths, or hardware timing honestly. A compiled file alone does not establish playability.
