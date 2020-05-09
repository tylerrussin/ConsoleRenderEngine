import curses
import time
view = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
view.addstr(10,10,"Pretty text", curses.color_pair(1))
view.refresh()
time.sleep(10)

y = "\33[32m#\033[0m"
print(y)
