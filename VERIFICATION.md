# Verification

Verified locally on 2026-10-10, macOS arm64. The objective is a reusable skill set that enables an agent to design, implement, and compile a Game Boy ROM. The delivered skills include executable helpers and a compiled, emulator-tested example.

## Requirement evidence

| Capability | Authoritative evidence | Result |
| --- | --- | --- |
| Design a buildable game | `gameboy-design/SKILL.md`, hardware reference, starter `GAME_DESIGN.md` | Defines goals, controls, transitions, layout, assets, budgets, cartridge choice, and acceptance cases |
| Implement a ROM | `gameboy-build/SKILL.md`, implementation reference, starter source | Working GBDK game with input, rendering, collision, title/play/win/restart |
| Create graphics | `tiles.py`, converter tests, compiled generated C asset | Correct two-plane pixel encoding and row-major tile order; rejects malformed input |
| Compile for Game Boy | Actual GBDK compilation of copied starter | 32,768-byte DMG ROM, mapper 0, no external RAM; map and symbols generated |
| Reproduce build | Two clean builds with GBDK 4.5.0 | Identical SHA-256 |
| Validate ROM integrity | `artifacts/header.json`; malformed-ROM helper tests and corrupted-ROM CLI execution | Valid shipped ROM; altered data rejected |
| Verify gameplay | `artifacts/gameplay.json`; `test_starter.py` | 25 passing assertions using actual button input and read-only state observations |
| Inspect rendered output | `artifacts/three-targets.png`, boot capture | Player and target appear at expected positions; title omits target |
| Package discoverable skills | Three `SKILL.md` files and `agents/openai.yaml` files; quick validator | All three valid; all relative skill links resolve |
| Install locally | Symlinks under `/Users/sandwich/.codex/skills/` | `gameboy-design`, `gameboy-build`, and `gameboy-verify` resolve to this workspace |

## Tool versions and artifact identity

- GBDK-2020: 4.5.0, official `gbdk-macos-arm64.tar.gz` release archive.
- Downloaded archive SHA-256: `289ee60e46c5a2785a21e35533f84a5131ed4a063b21b0dbdedc9a10af15bf78` (recorded locally, not an independently authenticated upstream checksum).
- Emulator: PyBoy 2.7.0, forced DMG mode, bundled boot ROM, headless rendering.
- Screenshot dependency: Pillow 11.3.0.
- ROM: [`artifacts/three-targets.gb`](artifacts/three-targets.gb).
- ROM SHA-256: `7aff0c68f90c27a0cfec85b9c2d2faab557d1dc1d861cbcaa563a442b9fe3200`.
- Debug files: `artifacts/three-targets.map` and `artifacts/three-targets.noi`, from the same clean build.
- Link map reports `_CODE` 480 bytes, `_HOME` 291 bytes, `_DATA` 22 bytes, and shadow OAM at `0xC000`. These are individual sections, not total memory use; stack and other runtime sections also consume memory.

## Executed checks

From the repository root, the starter was copied into `.validation/starter` and built with:

```sh
python3 skills/gameboy-build/scripts/new_project.py .validation/starter
make -C .validation/starter GBDK_HOME=/Users/sandwich/Develop/gameboy-forge/.tools/gbdk
python3 skills/gameboy-verify/scripts/check_rom.py .validation/starter/build/game.gb
.tools/venv/bin/python skills/gameboy-verify/scripts/test_starter.py \
  .validation/starter/build/game.gb --symbols .validation/starter/build/game.noi \
  --screenshot .validation/play.png
.tools/venv/bin/python skills/gameboy-verify/scripts/smoke_rom.py \
  .validation/starter/build/game.gb --screenshot .validation/boot.png
python3 -m unittest discover -s tests -v
```

All 11 helper tests passed. They cover pixel bitplanes and tile order, malformed pixel input, asset overwrite refusal, valid and invalid ROM headers/checksums, mapper/RAM inconsistencies, mapper capacity, supported MBC2/MBC5 fixtures, unknown mappers, and scaffold overwrite refusal. Fixture validity tests concern header structure only, not execution of synthetic ROM data.

Gameplay assertions cover title behavior, Start transition, held Start, rendered movement, all four boundaries, all three collections, edge-touch non-collision, victory, target hiding in actual hardware OAM, and restart of state, position, palette, and target OAM. The final collision occurs on first overlap, so the test correctly expects the win state before the player reaches the target's center.

The tile converter CLI generated a new C asset, which was successfully compiled with GBDK `lcc -c`. An altered ROM was also passed to the checker CLI and returned exit code 1 with a global checksum mismatch. Skill-creator's `quick_validate.py` passed for each of the three skill folders. All local Markdown references within the skills were resolved against the filesystem.

A second clean build produced the same ROM hash; the distributable artifact was copied from that build. Screenshot output was inspected visually. The installed skills are symlinks, so moving this workspace requires reinstalling or repairing those links. Start a new Codex session to discover them.

## Scope and limitations

The executable proof covers GBDK C, DMG mode, and a ROM-only cartridge. CGB, RGBDS, music, bank switching, battery saves, and physical hardware testing are documented extension paths; they were not executed or certified by this demonstration. The starter deliberately has no audio, text UI, save system, pause, or lose condition. Its three-target game is a reusable example, not a restriction on games the agent can build.

The generic smoke command captures frames and reports observations only. Gameplay evidence comes from the design-specific input assertions and image inspection. No independent agent evaluation or physical hardware testing was performed.
