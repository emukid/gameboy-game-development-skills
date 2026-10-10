#include <gb/gb.h>
#include <stdint.h>

/* Original 8x8 art: checker background, solid player, outlined target. */
static const uint8_t background[] = {
    0xAA,0,0x55,0,0xAA,0,0x55,0,0xAA,0,0x55,0,0xAA,0,0x55,0
};
static const uint8_t objects[] = {
    0x3C,0x3C,0x7E,0x7E,0xFF,0xFF,0xDB,0xDB,
    0xFF,0xFF,0x66,0x66,0x66,0x66,0x24,0x24,
    0xFF,0xFF,0x81,0x81,0x81,0x81,0x81,0x81,
    0x81,0x81,0x81,0x81,0x81,0x81,0xFF,0xFF
};
#define TITLE 0u
#define PLAY 1u
#define WIN 2u
/* Exported state symbols also support deterministic emulator assertions. */
uint8_t game_state;
uint8_t player_x;
uint8_t player_y;
uint8_t collected;
static const uint8_t target_x[] = {120u, 32u, 120u};
static const uint8_t target_y[] = {64u, 32u, 112u};
static uint8_t previous;

static void reset_game(void) {
    player_x = 24u;
    player_y = 64u;
    collected = 0u;
    game_state = PLAY;
    BGP_REG = 0xE4u;
}

static void render(void) {
    move_sprite(0, player_x + 8u, player_y + 16u);
    if (game_state == PLAY) {
        move_sprite(1, target_x[collected] + 8u, target_y[collected] + 16u);
    } else {
        hide_sprite(1);
    }
}

void main(void) {
    uint8_t i, keys, pressed;
    DISPLAY_OFF;
    BGP_REG = 0xE4u;
    OBP0_REG = 0xE4u;
    SCX_REG = 0u;
    SCY_REG = 0u;
    set_bkg_data(0, 1, background);
    fill_bkg_rect(0, 0, 32, 32, 0);
    set_sprite_data(0, 2, objects);
    for (i = 0u; i != 40u; ++i) hide_sprite(i);
    set_sprite_tile(0, 0);
    set_sprite_tile(1, 1);
    SPRITES_8x8;
    player_x = 24u;
    player_y = 64u;
    game_state = TITLE;
    previous = 0u;
    render();
    SHOW_BKG;
    SHOW_SPRITES;
    DISPLAY_ON;
    while (1) {
        vsync();
        keys = joypad();
        pressed = keys & (uint8_t)~previous;
        previous = keys;
        if (game_state != PLAY) {
            if (pressed & J_START) reset_game();
        } else {
            if ((keys & J_LEFT) && player_x > 0u) --player_x;
            if ((keys & J_RIGHT) && player_x < 152u) ++player_x;
            if ((keys & J_UP) && player_y > 0u) --player_y;
            if ((keys & J_DOWN) && player_y < 136u) ++player_y;
            if (player_x < target_x[collected] + 8u &&
                player_x + 8u > target_x[collected] &&
                player_y < target_y[collected] + 8u &&
                player_y + 8u > target_y[collected]) {
                ++collected;
                if (collected == 3u) {
                    game_state = WIN;
                    BGP_REG = 0x1Bu;
                }
            }
        }
        render();
    }
}
