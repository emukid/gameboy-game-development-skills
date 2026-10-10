# Three targets

This original demonstration targets DMG, GBDK-2020 4.5.0, and a 32 KiB ROM-only cartridge. It has no audio, saves, or CGB enhancements.

Press Start to begin. Move the solid character with the D-pad, one pixel per simulation frame per axis. Diagonal movement changes both axes; opposite directions cancel except at a clamped boundary. Touch each of three outlined targets in sequence to win. The final target disappears and the background palette inverts. Press Start again to restart. There is no lose state or pause in this demonstration.

The title state shows the character and checker background with no target. During play a target appears at (120,64), then (32,32), then (120,112). The player starts at (24,64). Coordinates identify 8×8 top-left corners. The arena spans the entire 160×144 display; clamp player X to 0–152 and Y to 0–136. Collision is strict AABB overlap; touching edges alone does not count.

Budget: one background tile in the default background tile range, two object tiles at IDs 0–1, two 8×8 objects maximum on any scanline, one map filled with tile zero. Three tiles consume 48 bytes. Runtime and code usage must be checked in linker output. No external RAM or mapper is required.

Acceptance: boot to title; Start shows target; each direction moves the player; movement clamps at all four edges; each overlap advances one target; collecting all three enters win; releasing and pressing Start resets position and target count. Hold Start across frames to verify it does not repeatedly reset play. Test scripts must use frame stepping and symbols, not write game state directly.
