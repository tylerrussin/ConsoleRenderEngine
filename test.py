import os
import sys
# import win32console, win32con
import keyboard
import curses
from curses.textpad import Textbox, rectangle

view = curses.initscr()
curses.curs_set(False)
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)





# Create Screen Buffer
screen = [[' ' for x in range(120)] for y in range(40)]
os.system(f"mode con: cols={120} lines={40}")

# myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
# myConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active


while True:
    # exits game loop
    if keyboard.is_pressed('P'):
        # Changing back to default font size
        sys.exit()
    # curses.color_pair(2)
    # string = ' ' + u'\u2588' + ' '
    string = ' ' + u'\u00A0' + ' '
    view.addstr(0, 0, string, curses.color_pair(2))
    view.refresh()

        

 #   myConsole.WriteConsoleOutputCharacter(Characters=output, WriteCoord=win32console.PyCOORDType(0, 0)) # Print at coordinates


