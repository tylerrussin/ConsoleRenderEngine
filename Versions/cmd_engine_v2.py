import os
import math
import time
import keyboard
import curses

from math import sqrt

nScreenWidth = 120          # Console Screen Size X (columns)
nScreenHeight = 40          # Console Screen Size Y (rows)
nMapHeight = 16
nMapWidth = 16

fPlayerX = 14.7             # Player Start Position
fPlayerY = 5.09
fPlayerA = 0.0              # Player Start Rotation
fFOV = 3.14159 / 4.0        # Field of View
fDepth = 16.0               # Maximum rendering distance
fSpeed = 5.0                # Walking Speed

# Create Screen Buffer
screen = [[0 for x in range(nScreenWidth)] for y in range(nScreenHeight)]
os.system(f"mode con: cols={nScreenWidth} lines={nScreenHeight}")

# Create Map of world space # = wall block, . = space
map = []
map.append(list('#########.......'))
map.append(list('#...............'))
map.append(list('#.......########'))
map.append(list('#..............#'))
map.append(list('#......##......#'))
map.append(list('#......##......#'))
map.append(list('#..............#'))
map.append(list('###............#'))
map.append(list('##.............#'))
map.append(list('#......####..###'))
map.append(list('#......#.......#'))
map.append(list('#......#.......#'))
map.append(list('#..............#'))
map.append(list('#......#########'))
map.append(list('#..............#'))
map.append(list('################'))

tp1 = time.perf_counter()
tp2 = time.perf_counter()

while 1:

    # We'll need time differential per frame to calculate modification
    # to movement speeds, to ensure consistant movement, as ray-tracing
    # is non-deterministic
    tp2 = time.perf_counter()
    elapsedTime = tp2 - tp1
    tp1 = tp2
    fElapsedTime = elapsedTime

    # Handle CCW Rotation
    if keyboard.is_pressed('A'):

        fPlayerA -= (fSpeed * 0.75) * fElapsedTime

    # Handle CW Rotation
    if keyboard.is_pressed('D'):

        fPlayerA += (fSpeed * 0.75) * fElapsedTime

    # Handle Forwards movement & collision
    if keyboard.is_pressed('W'):

        fPlayerX += math.sin(fPlayerA) * fSpeed * fElapsedTime
        fPlayerY += math.cos(fPlayerA) * fSpeed * fElapsedTime
        if map[int(fPlayerY)][int(fPlayerX)] == '#':

            fPlayerX -= math.sin(fPlayerA) * fSpeed * fElapsedTime
            fPlayerY -= math.cos(fPlayerA) * fSpeed * fElapsedTime

    # Handle backwards movement & collision
    if keyboard.is_pressed('S'):

        fPlayerX -= math.sin(fPlayerA) * fSpeed * fElapsedTime
        fPlayerY -= math.cos(fPlayerA) * fSpeed * fElapsedTime
        if map[int(fPlayerY)][int(fPlayerX)] == '#':

            fPlayerX += math.sin(fPlayerA) * fSpeed * fElapsedTime
            fPlayerY += math.cos(fPlayerA) * fSpeed * fElapsedTime

    for x in range(0, nScreenWidth):

        # For each column, calculate the projected ray angle into world space
        fRayAngle = (fPlayerA - fFOV/2.0) + (float(x) / float(nScreenWidth)) * fFOV

        # Find distance to wall
        fStepSize = 0.1         # Increment size for ray casting, decrease to increase
        fDistanceToWall = 0     #                                      resolution

        bHitWall = False       # Set when ray hits wall block
        bBoundary = False      # Set when ray hits boundary between two wall blocks

        fEyeX = math.sin(fRayAngle) # Unit vector for ray in player space
        fEyeY = math.cos(fRayAngle)

        # Incrementally cast ray from player, along ray angle, testing for 
	    # intersection with a block
        while bHitWall == False and fDistanceToWall < fDepth:

            fDistanceToWall += fStepSize
            nTestX = int(fPlayerX + fEyeX * fDistanceToWall)
            nTestY = int(fPlayerY + fEyeY * fDistanceToWall)

            # Test if ray is out of bounds
            if nTestX < 0 or nTestX >= nMapWidth or nTestY < 0 or nTestY >= nMapHeight:

                bHitWall = True         # Just set distance to maximum depth
                fDistanceToWall = fDepth

            else:

                # Ray is inbounds so test to see if the ray cell is a wall block
                if map[nTestY][nTestX] == '#':

                    # Ray has hit wall
                    bHitWall = True

                    # To highlight tile boundaries, cast a ray from each corner
                    # of the tile, to the player. The more coincident this ray
                    # is to the rendering ray, the closer we are to a tile 
                    # boundary, which we'll shade to add detail to the walls
                    p = []

                    # Test each corner of hit tile, storing the distance from
				    # the player, and the calculated dot product of the two rays
                    for tx in range(0,2):
                        for ty in range(0,2):

                            # Angle of corner to eye
                            vy = float(nTestY) + ty - fPlayerY
                            vx = float(nTestX) + tx - fPlayerX
                            d = sqrt(vx*vx + vy*vy)
                            dot = (fEyeX * vx / d) + (fEyeY * vy / d)
                            p.append((d, dot))
                    
                    # Sort Pairs from closest to farthest
                    p.sort(key=lambda x: x[0])

                    # First two/three are closest (we will never see all four)
                    fBound = 0.01
                    if math.acos(p[0][1]) < fBound: bBoundary = True
                    if math.acos(p[1][1]) < fBound: bBoundary = True
                    if math.acos(p[2][1]) < fBound: bBoundary = True




        # Calculate distance to ceiling and floor
        nCeiling = float(nScreenHeight/2.0) - nScreenHeight / float(fDistanceToWall)
        nFloor = nScreenHeight - nCeiling

        # Shader walls based on distance
        nShade = ' '
        if fDistanceToWall <= fDepth / 4.0:         nShade = u'\u2588'     # Very Close
        elif fDistanceToWall < fDepth / 3.0:        nShade = u'\u2593'
        elif fDistanceToWall < fDepth / 2.0:        nShade = u'\u2592'
        elif fDistanceToWall < fDepth:              nShade = u'\u2591'
        else:                                       nShade = ' '        # Too far away

        if bBoundary:       nShade = ' ' # Black it out

        for y in range(0, nScreenHeight):

            # Each Row
            if y < nCeiling:
                screen[y][x] = ' '
            elif y > nCeiling and y <= nFloor:
                screen[y][x] = nShade
            else: # Floor

                # Shade floor based on distance
                b = 1.0 - ((float(y) - nScreenHeight/2.0) / (float(nScreenHeight) / 2.0))
                if b < 0.25:        nShade2 = '#'
                elif b < 0.5:       nShade2 = 'x'
                elif b < 0.75:      nShade2 = '.'
                elif b < 0.9:       nShade2 = '-'
                else:               nShade2 = " "
                screen[y][x] = nShade2



    # Display Stats
    view = curses.initscr()
    curses.curs_set(0)
    stats = f'X={"%.2f" % fPlayerX}, Y={"%.2f" % fPlayerY}, A={"%.2f" % fPlayerA}, FPS={"%.2f" % (1.0 / fElapsedTime)}'
    stats_window = curses.newwin(1, len(stats) + 1, 0, 0)
    stats_window.addstr(0, 0, stats)
    stats_window.refresh()

    # Display Map
    for nx in range(0, nMapWidth):
        for ny in range(0, nMapWidth):

            screen[ny + 1][nx] = map[ny][nx]
            
    screen[int(fPlayerY)+1][int(fPlayerX)] = 'P'

    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele for sub in screen for ele in sub))
    view.refresh()
    

# That's It!! - Tyler
