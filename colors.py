'''
Script testing out color rendering in the command prompt
'''
import curses
import time

from curses import has_colors, can_change_color

# Initiate classes
view = curses.initscr()
curses.start_color()

# Does command prompt support color?
print(has_colors())

# Can we change colors?
print(can_change_color())

# color integer is 0 - 767
# zero reserved for black
curses.init_color(42, 66, 182, 245)

# All color pallets
curses.init_pair(1, 42, curses.COLOR_BLACK)
view.addstr(10,10,"Pretty text", curses.color_pair(1))
view.refresh()
time.sleep(4)

