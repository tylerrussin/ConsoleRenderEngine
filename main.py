import os
import sys
import keyboard
import curses

from Command_Line_Font import command_line_font

command_line_font(16)        # Console ASCII font size
nScreenWidth = 120          # Console Screen Size X (columns)
nScreenHeight = 40          # Console Screen Size Y (rows)

# Create Screen Buffer
screen = [[' ' for x in range(nScreenWidth)] for y in range(nScreenHeight)]
os.system(f"mode con: cols={nScreenWidth} lines={nScreenHeight}")
view = curses.initscr()


while 1:

    # Quit simulation
    if keyboard.is_pressed('Q'):
        curses.endwin()                                 # End curses instance
        os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
        command_line_font(16)                           # Reset default font size
        sys.exit()                                      # Exit Program


    screen[20][40] = 'T'

    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele for sub in screen for ele in sub))
    view.refresh()
