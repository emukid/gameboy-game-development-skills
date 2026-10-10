# Emulator verification

## Repeatable headless execution

Create a Python virtual environment and run `python -m pip install -r <skill>/scripts/requirements.txt` (PyBoy 2.7.0 and Pillow 11.3.0) for this suite's tested scripts. Its bundled boot ROM avoids a dependency on a proprietary boot ROM. Initialize with `PyBoy(path, window="null", sound_emulated=False, cgb=False)` for DMG; step with `tick(frames, render=True)`, use `button_press()` and `button_release()`, and capture `screen.image`. Always `stop(save=False)` for tests that must not write battery saves. Pin the version in the report.

Allow a bounded boot period before gameplay assertions. A fixed boot delay is appropriate for the supplied starter; other games may need to wait for a state predicate with a maximum frame count. Use the same ROM bytes and symbols. GBDK `.noi` files contain `DEF name address` symbols; do not hardcode WRAM addresses that may change after recompilation. Release buttons explicitly. Allow an extra rendered frame for shadow OAM transfers.

A useful test observes a specific predicate: X increases under Right and remains at a boundary; overlap changes score exactly once; losing a life changes the state; restart clears run state. Screen diversity alone cannot tell a title from a crash. Save screenshots at key states and inspect them.

## Interactive/debugger checks

Open the final ROM in an installed emulator. Record emulator version and DMG/CGB model. Confirm boot, title legibility, responsive controls, expected speed, sprite visibility at edges, collision response, every game state, and restart. Test simultaneous and held inputs. Inspect tile maps and OAM when visuals differ from game state. Use source/map/symbol output from the same build for breakpoints.

For CGB-enhanced ROMs test both DMG and CGB. CGB-only games need CGB tests; do not force DMG and then classify the expected incompatibility as a defect. For battery saves, use an isolated save directory, exit normally to flush, restart the emulator, and verify restored data. Test missing/corrupt saves separately. For sound, verify channel mixing, effect priority, pause and restart by listening.

Timing-sensitive raster effects merit a second accurate emulator and, when available, hardware testing. State which was actually performed; a headless DMG test is not proof of physical hardware correctness.

## Reproducibility

Clean-build twice with identical inputs and compare SHA-256 hashes. Inspect map usage and compiler warnings. Retain source, source art, conversion command, pinned toolchain, ROM hash, and the test report. Do not distribute a boot ROM or third-party game as a test fixture.

References: [PyBoy API](https://docs.pyboy.dk/), [SameBoy](https://sameboy.github.io/), [Emulicious](https://emulicious.net/), [Pan Docs header](https://gbdev.io/pandocs/The_Cartridge_Header.html).
