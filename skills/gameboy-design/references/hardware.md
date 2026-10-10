# Hardware decisions

## Baseline DMG

The display is 160×144 pixels (20×18 visible 8×8 tiles). Background maps are 32×32 tile IDs. Each 8×8, 2-bpp tile consumes 16 bytes. Plan tile IDs and address ranges; background and object tile storage partially overlap depending on addressing mode. There are 384 physical tile slots in DMG VRAM, but one background addressing mode selects 256 and objects address 256. Do not assume all 384 are independently available to both.

DMG has 8 KiB WRAM and 8 KiB VRAM. Leave room for stack, runtime, shadow OAM, and temporary buffers. A large `const` asset belongs in ROM. An unqualified writable array consumes scarce RAM. ROM-only cartridges provide 32 KiB; larger games need a compatible mapper and bank layout.

Objects are 8×8 or 8×16 pixels; the size mode applies to all objects. Limit: 40 objects total, 10 selected per scanline. In 8×16 mode, tile pairs use an even first tile. A 16×16 actor uses four 8×8 objects or two 8×16 objects. Budget peak shared scanlines with enemies, bullets, and HUD. Hide unused objects by their Y position so they do not consume scanline selection slots.

DMG provides four background shades and two object palettes, each with three visible shades; object color index zero is transparent. Keep silhouettes readable without color. Object coordinates stored in OAM have offsets: screen top-left is `(x - 8, y - 16)`.

At normal speed the display runs about 59.73 frames/second. Avoid assuming exactly 60 seconds per 3600 frames for real-time timing. Budget simulation separately from graphics transfers. VRAM and OAM access restrictions depend on LCD mode; use safe library transfers and shadow OAM. VBlank is finite, not permission for unlimited copies.

## Color, banking, and sound

CGB adds banks of VRAM/WRAM, per-tile attributes, and color palettes. Decide DMG-only, dual-compatible, or CGB-only deliberately; a `.gbc` extension does not set cartridge compatibility. Dual-mode games need a working DMG path and initialization of CGB palettes/attributes. Test both modes.

Choose an MBC based on ROM capacity, external RAM, battery, RTC, and target emulator support. MBC5 is a useful general choice for larger homebrew; avoid adding save hardware when no persistence is required. Plan bank ownership of code, maps, graphics, and music. Keep interrupt-critical code/data reachable across switches.

Audio has two pulse channels, a wave channel, and a noise channel. Define which effect may interrupt which music channel. Silence and restore channels predictably on pause/restart. Choose a tracker/driver only when music is needed.

## Authoritative references

Consult these when implementing details, especially timing, memory banking, or CGB support:

- [Pan Docs specifications](https://gbdev.io/pandocs/Specifications.html)
- [Tile data](https://gbdev.io/pandocs/Tile_Data.html), [tile maps](https://gbdev.io/pandocs/Tile_Maps.html), [OAM](https://gbdev.io/pandocs/OAM.html)
- [Memory map](https://gbdev.io/pandocs/Memory_Map.html), [access restrictions](https://gbdev.io/pandocs/Accessing_VRAM_and_OAM.html)
- [Cartridge header](https://gbdev.io/pandocs/The_Cartridge_Header.html)
- [GBDK banking](https://gbdk.org/docs/api/docs_rombanking_mbcs.html)
