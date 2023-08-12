import sys

import keyboard

# Path to console_render_engine.py
sys.path.append('../..')

import console_render_engine



if __name__ == '__main__':

    CMD_FONT = 5            # Console ASCII font size
    SCREEN_WIDTH = 256      # Console Screen Size X (columns)  #256#
    SCREEN_HEIGHT = 127     # Console Screen Size Y (rows)

    cmd_engine = console_render_engine.ConsoleRenderEngine(CMD_FONT, SCREEN_WIDTH, SCREEN_HEIGHT)
    cmd_engine.on_user_create()

    cmd_engine.reset_screen()

    # Simulation loop
    while 1:

        # Quit simulation
        if keyboard.is_pressed('P'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # cmd_engine.draw_circle(128, 63, 50, '\u2588', [0x000F, 0x00F0])
        cmd_engine.fill_circle(128, 63, 50, '\u2588', [0x000F, 0x00F0])

        # Render current screen to command
        cmd_engine.display_screen()
