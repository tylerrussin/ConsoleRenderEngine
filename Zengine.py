from math import sqrt, floor, ceil
import os
import sys
import curses
from curses import textpad
import math
import time
import keyboard
import random
os.system('color')

nScreenWidth = 120
nScreenHeight = 40

fPlayerX = 8.0
fPlayerY = 8.0
fPlayerA = 0.0

nMapHeight = 16
nMapWidth = 16

fFOV = 3.14159 / 4.0
fDepth = 16.0


# Create Screen Buffer
os.system(f"mode con: cols={nScreenWidth} lines={nScreenHeight}")
screen = [[0 for x in range(nScreenWidth)] for y in range(nScreenHeight)]



# curses.start_color()
# curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)


map = []

map.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '#', '#', '#', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
map.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])



def getMarixString(m):
    x = ''
    for col in m:
        x += ''.join(str(item) for item in col)
    return x


tp1 = time.perf_counter()
tp2 = time.perf_counter()

# while True:
#     tp2 = time.perf_counter()
#     elapsedTime = tp2 - tp1
#     tp1 = tp2
#     fElapsedTime = float(elapsedTime)

#     if keyboard.is_pressed('W'):
#         fPlayerX += math.sin(fPlayerA) * 5.0 * fElapsedTime
#         fPlayerY += math.cos(fPlayerA) * 5.0 * fElapsedTime
#     view = curses.initscr()
#     view.addstr(0, 0, f"({fPlayerX},{fPlayerY})")
#     view.refresh()
    


# Game Loop
while True:
    view = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    


    tp2 = time.perf_counter()
    elapsedTime = tp2 - tp1
    tp1 = tp2
    fElapsedTime = float(elapsedTime)

    # Controls
    # Handle CCW Rotation
    if keyboard.is_pressed('p'):
        sys.exit()

    if keyboard.is_pressed('A'): 
        fPlayerA -= (0.8) * fElapsedTime

    if keyboard.is_pressed('D'):
        fPlayerA += (0.8) * fElapsedTime

    if keyboard.is_pressed('W'):
        fPlayerX += math.sin(fPlayerA) * 5.0 * fElapsedTime
        fPlayerY += math.cos(fPlayerA) * 5.0 * fElapsedTime

        if map[int(fPlayerY)][int(fPlayerX)] == '#':
            fPlayerX -= math.sin(fPlayerA) * 5.0 * fElapsedTime
            fPlayerY -= math.cos(fPlayerA) * 5.0 * fElapsedTime

    if keyboard.is_pressed('S'):
        fPlayerX -= math.sin(fPlayerA) * 5.0 * fElapsedTime
        fPlayerY -= math.cos(fPlayerA) * 5.0 * fElapsedTime

        if map[int(fPlayerY)][int(fPlayerX)] == '#':
            fPlayerX += math.sin(fPlayerA) * 5.0 * fElapsedTime
            fPlayerY += math.cos(fPlayerA) * 5.0 * fElapsedTime

    for x in range(0, nScreenWidth):
        # For each column, calculate the projected ray angle into world space
        fRayAngle = float((fPlayerA - fFOV / 2.0) + float(x) / float(nScreenWidth) * fFOV)

        fDistanceToWall = float(0)
        bHitWall = False
        bBoundary = False

        fEyeX = float(math.sin(fRayAngle))
        fEyeY = float(math.cos(fRayAngle))

        while bHitWall == False and fDistanceToWall < fDepth:

            fDistanceToWall += 0.1

            nTestX = int(fPlayerX + fEyeX * fDistanceToWall)
            nTestY = int(fPlayerY + fEyeY * fDistanceToWall)

            # Test if ray is out of bounds
            if nTestX < 0 or nTestX >= nMapWidth or nTestY < 0 or nTestY >= nMapHeight:

                bHitWall = True     # Just set distance to maximum depth
                fDistanceToWall = fDepth
            else:
                # Ray is inbounds so test to see if the ray cell is a wall block
                if map[nTestY][nTestX] == '#':
                    bHitWall = True
                    p = []
                    for tx in range(0,2):
                        for ty in range(0,2):
                            vy = float(nTestY) + ty - fPlayerY
                            vx = float(nTestX) + tx - fPlayerX
                            d = sqrt(vx*vx + vy*vy)
                            dot = (fEyeX * vx / d) + (fEyeY * vy / d)
                            p.append((d, dot))
                    
                    # Sort Pairs from closest to farthest
                    p.sort(key=lambda x: x[0])

                    fBound = 0.01
                    if math.acos(p[0][1]) < fBound: bBoundary = True
                    if math.acos(p[1][1]) < fBound: bBoundary = True
                    if math.acos(p[2][1]) < fBound: bBoundary = True


        # Calculate distance to ceiling and floor
        nCeiling = int(float(nScreenHeight / 2.0) - nScreenHeight / float(fDistanceToWall))
        nFloor = int(nScreenHeight - nCeiling)

        nShade = ' '

        if fDistanceToWall <= fDepth / 4.0:         nShade = u'\u2588'     # Very Close
        elif fDistanceToWall < fDepth / 3.0:        nShade = u'\u2593'
        elif fDistanceToWall < fDepth / 2.0:        nShade = u'\u2592'
        elif fDistanceToWall < fDepth:              nShade = u'\u2591'
        else:                                       nShade = ' '        # Too far away

        if bBoundary:       #nShade = u'\u25A0' # Black it out
            if fDistanceToWall <= fDepth / 4.0:         nShade3 = u'\u2588'     # Very Close
            elif fDistanceToWall < fDepth / 3.0:        nShade3 = u'\u2593'
            elif fDistanceToWall < fDepth / 2.0:        nShade3 = u'\u2592'
            elif fDistanceToWall < fDepth:              nShade3 = u'\u2591'
            else:                                       nShade3 = ' '  
            

        for y in range(0, nScreenHeight):
            if y < nCeiling:
                screen[y][x] = nShade
                screen[nScreenHeight - 1][nScreenWidth - 1] = ''
                view.addstr(y, x, str(screen[y][x]), curses.color_pair(2))
            elif y > nCeiling and y <= nFloor:
                if bBoundary:
                    screen[y][x] = nShade2
                    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
                    view.addstr(y, x, str(screen[y][x]), curses.color_pair(3))
                else:
                    screen[y][x] = nShade
                    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
                    view.addstr(y, x, str(screen[y][x]), curses.color_pair(1))
            else:
                b = 1.0 - ((float(y) - nScreenHeight / 2.0) / (float(nScreenHeight) / 2.0))
                if b < 0.5:        nShade2 = u'\u2588'
                elif b < 0.6:       nShade2 = u'\u2593'
                elif b < 0.7:      nShade2 = u'\u2592'
                elif b < 0.8:       nShade2 = u'\u2591'
                else:               nShade2 = " "
                screen[y][x] = nShade2
                screen[nScreenHeight - 1][nScreenWidth - 1] = ''
                view.addstr(y, x, str(screen[y][x]), curses.color_pair(2))

    # screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    # map[nMapWidth - 1][nMapHeight - 1] = ''
    # view = curses.initscr()
    # view.addstr(0, 0, getMarixString(screen))
    # view.addstr(0, 0, getMarixString(map))
    # view.refresh()

    # For the screen
    for nx in range(0, nMapWidth):
        for ny in range(0, nMapWidth):
            # screen[ny + 1][nx] = map[ny][nx]
            # screen[int(fPlayerY)+1][int(fPlayerX)] = 'P'
            screen[nScreenHeight - 1][nScreenWidth - 1] = ''
            view.addstr(ny + 1, nx, str(map[ny][nx]), curses.color_pair(1))
            

    try:
        
        # screen[nScreenHeight - 1][nScreenWidth - 1] = ''
        # view = curses.initscr()
        # for index_c, col in enumerate(screen):
        #     for index_r, row in enumerate(col):
        #         view.addstr(index_c, index_r, str(screen[index_c][index_r][0]))#, screen[index_c][index_r][1])
        screen[nScreenHeight - 1][nScreenWidth - 1] = ''
        view.addstr(int(fPlayerY), int(fPlayerX), 'P', curses.color_pair(1))
        screen[nScreenHeight - 1][nScreenWidth - 1] = ''
        view.addstr(0,0, f'X={fPlayerX}, Y={fPlayerY}, A={fPlayerA}, FPS={1.0 / fElapsedTime}')

        view.addstr(nScreenHeight - 1, nScreenWidth -1 , '', curses.color_pair(1))
        view.refresh()
    except:
        pass




    # # for the map
    # map[nMapWidth - 1][nMapHeight - 1] = ''
    # curses.initscr()
    # my_window = curses.newwin(17, 16, 1, 0)
    # for index_c, col in enumerate(map):
    #     for index_r, row in enumerate(col):
    #         my_window.addstr(index_c, index_r, str(map[index_c][index_r]))

    # my_window.refresh()



