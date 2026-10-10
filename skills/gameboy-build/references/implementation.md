# GBDK implementation notes

## Frame and state model

Represent title, play, pause, win, and lose as explicit states as needed. Poll `joypad()` once per simulation frame. `pressed = current & ~previous` detects new presses for menus; held bits drive movement. Save `previous` after processing. Reset all run-specific timers, actors, score, and state on restart. Do not let a held Start retrigger transitions every frame.

Use `vsync()` once per frame in current GBDK (older examples use `wait_vbl_done()`). Keep interrupts enabled for it. GBDK updates hardware OAM from shadow OAM during VBlank; `move_sprite()` edits the shadow data, so visible results can lag one frame. Use small bounded graphics updates with safe GBDK routines. Do not assume all logic after `vsync()` finishes inside VBlank. Avoid nested waits in entity functions.

Use world coordinates for collision and camera-independent rules. Convert to screen coordinates only when drawing. For a sprite of width `w`, keep its top-left X in `[0, 160-w]` if the arena is the whole screen. Clamp before unsigned subtraction or use a signed intermediate. Axis-aligned overlap uses strict comparisons for touching edges unless the design says otherwise. Test both directions and corners; fast objects may need swept collision or smaller steps.

## Graphics

At initialization call `DISPLAY_OFF` (GBDK's safe helper), upload static tiles/maps, initialize palettes and scroll, hide unused sprites, then enable required layers and `DISPLAY_ON`. Never disable the LCD by raw register write during an active scanline.

Load object data with `set_sprite_data()`, choose tile with `set_sprite_tile()`, and display it with `move_sprite(id, screen_x + 8, screen_y + 16)`. Hide unused objects with `hide_sprite()`. Set `SPRITES_8x8` or `SPRITES_8x16` intentionally. In 8×16 mode, reserve consecutive tile pairs and use even base IDs.

Keep tile allocation explicit. Default GBDK background addressing and sprite addressing can share part of VRAM. Reserving low object IDs and a small background set in its separate range works for the starter; inspect overlap before growing beyond it. Text libraries also allocate/upload tiles: do not mix them into a custom map without reserving their tile range. Generate map data and palette indices consistently with the converter. For CGB, initialize attribute maps and VRAM bank selection along with color palettes.

## Sound

For simple effects, use the documented `NRxx_REG` registers, enabling audio in NR52 before configuring NR50/NR51 and channels. A pulse effect sets duty/length, envelope, frequency, then trigger. Avoid retriggering on every held frame unless intended. For music, use a supported driver such as hUGEdriver and its matching export; budget its interrupt time and ROM bank. Allocate effect channels so music and effects do not fight. Test by listening; a screenshot cannot verify sound.

## ROM banking and saves

If the 32 KiB starter no longer fits, use the installed GBDK `banks_autobank` example and [banking guide](https://gbdk.org/docs/api/docs_rombanking_mbcs.html). Configure mapper/ROM banks in the build, bank code/data deliberately, and inspect placement in the map. A CPU pointer alone does not identify a banked asset. Use `BANKREF`/`BANK`, matching `BANKED` function declarations and definitions, and appropriate bank switches. Restore the previous data bank after temporary switches; never switch away from currently executing banked code manually. Interrupt handlers must not depend on whichever data bank happened to be selected.

Persistent saves need external RAM and a matching battery-capable cartridge type. Enable RAM before access and disable after. Define a format with magic/version, bounds checks, checksum, and sensible defaults for missing/corrupt saves. Serialize fields rather than writing a compiler-dependent struct layout. Test a cold emulator restart with the saved file and a corrupt save. In-process RAM survival is not proof of persistence.

## Debugging

- Blank screen: check LCD/layer flags, palettes, tile/map data, camera coordinates, and entry execution.
- Invisible objects: check OAM coordinate offsets, transparency, object mode, tile IDs, priority, and ten-object scanline limit.
- Flickering/corrupt graphics: inspect unsafe VRAM writes and exceeded transfer budgets.
- Freeze at frame wait: inspect disabled interrupts or a handler that never returns.
- Crash after content growth: inspect bank access, stack/WRAM overlap, integer wrap, and linker warnings.

Use [GBDK API](https://gbdk.org/docs/api/gb_8h.html), [coding guidelines](https://gbdk.org/docs/api/docs_coding_guidelines.html), and the installed headers for exact signatures. Old GBDK tutorials can use obsolete types, includes, or linker flags.
