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
os.system(f"mode con: cols={nScreenWidth} lines={nScreenHeight}") # Font mechanic(y is always twice as big as x)
view = curses.initscr()

def draw(x, y):
    # Check screen boundry
    if x < nScreenWidth and y < nScreenHeight:
        screen[y][x] = '1'



def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dx1 = abs(dx)
    dy1 = abs(dy)
    px = 2 * dy1 - dx1
    py = 2 * dx1 - dy1

    if dy1 <= dx1:
        if dx >= 0:
            x = x1
            y = y1
            xe = x2

        else:
            x = x2
            y = y2
            xe = x1
        draw(x, y)
        for i in range(x, xe):
            x += 1
            if px < 0:
                px = px + 2 * dy1
            
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y = y + 1

                else:
                    y = y - 1
                px = px + 2 * (dy1 - dx1)
            draw(x, y)
    
    else:
        if dy >= 0:
            x = x1
            y = y1
            ye = y2
        
        else:
            x = x2
            y = y2
            ye = y1
        draw(x, y)
        for i in range(y, ye):
            y += 1
            if py <= 0:
                py = py + 2 * dx1
            
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x = x + 1
                
                else:
                    x = x - 1
                py = py + 2 * (dx1 - dy1)
            draw(x, y)

def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)


while 1:

    # Quit simulation
    if keyboard.is_pressed('Q'):
        curses.endwin()                                 # End curses instance
        os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
        command_line_font(16)                           # Reset default font size
        sys.exit()                                      # Exit Program

    # Initialize points
    x1 = 60
    x2 = 110
    x3 = 0
    y1 = 30
    y2 = 20
    y3 = 0

    # Draw line into matrix
    draw_triangle(x1, y1, x2, y2, x3, y3)


    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele for sub in screen for ele in sub))
    view.refresh()