# Toolchain choices and commands

## GBDK-2020

Use the archive matching host OS and CPU from the official release page. Extract it, then confirm `bin/lcc` runs. Record the release and archive SHA-256. Do not substitute the host C compiler or standalone SDCC for the complete GBDK runtime/toolchain.

The starter uses this direct equivalent from the project root (create `build` first):

```sh
"/absolute/path/to/gbdk/bin/lcc" -Wm-ynFORGE -Wm-yt0 -Wm-yo2 -Wl-m -Wl-j -o build/game.gb src/main.c
```

These options set title FORGE, ROM-only type 0, two 16 KiB ROM banks, and map/debug output. Adapt title and mapper to the actual design. The starter is DMG-compatible; GBDK's `-Wm-yc` enables CGB support, while `-Wm-yC` marks CGB-only. Adding a flag does not implement a color rendering path. Consult installed `lcc`/`makebin` help when changing cartridge options.

`make clean` removes the generated build directory. The starter rebuilds all sources in one invocation so small projects avoid stale header/object dependencies; larger projects may adopt GBDK's official object-based templates.

Use a path without spaces if the installed compiler's nested subprocesses cannot handle them. On Windows the direct command also works with `lcc.exe` and native paths. Diagnose macOS quarantine on the downloaded tool directory only; do not disable system security globally.

References: [getting started](https://gbdk.org/docs/api/docs_getting_started.html), [toolchain](https://gbdk.org/docs/api/docs_toolchain.html), [release 4.5.0](https://github.com/gbdk-2020/gbdk-2020/releases/tag/4.5.0).

## Existing RGBDS assembly projects

Keep RGBDS if already used or explicitly requested. Pin an installed version and consult its matching [manuals](https://rgbds.gbdev.io/docs/). RGBDS syntax is not interchangeable with SDCC's assembler. The usual sequence is:

```sh
rgbasm -o build/main.o src/main.asm
rgblink -m build/game.map -n build/game.sym -o build/game.gb build/main.o
rgbfix -v -p 0xFF build/game.gb
```

Source must define a valid entry/header reservation, stack initialization, interrupt vectors and handling, safe LCD initialization, and a non-returning main loop. Set mapper, RAM, ROM size, and CGB compatibility intentionally using source/header or version-matching `rgbfix` flags. `rgbfix` repairs metadata, not runtime bugs or wrong bank placement. Use a maintained `hardware.inc` matched to source symbols. Assemble a tiny bootable baseline before adding game logic. This suite includes a tested C starter; these assembly commands describe the alternative workflow, not a tested assembly starter.
