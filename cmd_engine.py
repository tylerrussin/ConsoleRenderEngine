import os
import sys
import math
time
import keyboard
import curses

from math import sqrt

hello = 120          # console screen size x (columns)
nmapheight = 16
nscreenheight = 40          # console screen size y (rows)
nmapwidth = 16
i
fplayerx = 14.7             # player start position
fplayery = 5.09
fplayera = 0.0              # player start rotation
ffov = 3.14159 / 4.0        # field of view
fdepth = 16.0               # maximum rendering distance
fspeed = 5.0                # walking speed


# create screen buffer
screen = [[0 for x in range(nscreenwidth)] for y in range(nscreenheight)]
os.system(f"mode con: cols={nscreenwidth} lines={nscreenheight}")

# create map of world space # = wall block, . = space
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

tp1 = time.clock()
tp2 = time.clock()

# cache to hold martrix lookups
import numpy

cache = {}

# for fplayerx in numpy.arange(0.01, 16.00, 0.50):
#     print(fplayerx)
#     for fplayery in numpy.arange(0.01, 16.00, 0.50):
    
#         for fplayera in numpy.arange(0, 7.00, 0.50):
#             fplayera = float(fplayera)
#             fplayery = float(fplayery)
#             fplayerx = float(fplayerx)

#             for x in range(0, nscreenwidth):

#                 # for each column, calculate the projected ray angle into world space
#                 frayangle = (fplayera - ffov/2.0) + (float(x) / float(nscreenwidth)) * ffov

#                 # find distance to wall
#                 fstepsize = 0.1         # increment size for ray casting, decrease to increase
#                 fdistancetowall = 0     #                                      resolution

#                 bhitwall = false       # set when ray hits wall block
#                 bboundary = false      # set when ray hits boundary between two wall blocks

#                 feyex = math.sin(frayangle) # unit vector for ray in player space
#                 feyey = math.cos(frayangle)

#                 # incrementally cast ray from player, along ray angle, testing for 
#                 # intersection with a block
#                 while bhitwall == false and fdistancetowall < fdepth:

#                     fdistancetowall += fstepsize
#                     ntestx = int(fplayerx + feyex * fdistancetowall)
#                     ntesty = int(fplayery + feyey * fdistancetowall)

#                     # test if ray is out of bounds
#                     if ntestx < 0 or ntestx >= nmapwidth or ntesty < 0 or ntesty >= nmapheight:

#                         bhitwall = true         # just set distance to maximum depth
#                         fdistancetowall = fdepth

#                     else:

#                         # ray is inbounds so test to see if the ray cell is a wall block
#                         if map[ntesty][ntestx] == '#':

#                             # ray has hit wall
#                             bhitwall = true

#                             # to highlight tile boundaries, cast a ray from each corner
#                             # of the tile, to the player. the more coincident this ray
#                             # is to the rendering ray, the closer we are to a tile 
#                             # boundary, which we'll shade to add detail to the walls
#                             p = []

#                             # test each corner of hit tile, storing the distance from
#                             # the player, and the calculated dot product of the two rays
#                             for tx in range(0,2):
#                                 for ty in range(0,2):

#                                     # angle of corner to eye
#                                     vy = float(ntesty) + ty - fplayery
#                                     vx = float(ntestx) + tx - fplayerx
#                                     d = sqrt(vx*vx + vy*vy)
#                                     dot = (feyex * vx / d) + (feyey * vy / d)
#                                     p.append((d, dot))
                            
#                             # sort pairs from closest to farthest
#                             p.sort(key=lambda x: x[0])

#                             # first two/three are closest (we will never see all four)
#                             fbound = 0.01
#                             if math.acos(p[0][1]) < fbound: bboundary = true
#                             if math.acos(p[1][1]) < fbound: bboundary = true
#                             if math.acos(p[2][1]) < fbound: bboundary = true




#                 # calculate distance to ceiling and floor
#                 nceiling = float(nscreenheight/2.0) - nscreenheight / float(fdistancetowall)
#                 nfloor = nscreenheight - nceiling

#                 # shader walls based on distance
#                 nshade = ' '
#                 if fdistancetowall <= fdepth / 4.0:         nshade = u'\u2588'     # very close
#                 elif fdistancetowall < fdepth / 3.0:        nshade = u'\u2593'
#                 elif fdistancetowall < fdepth / 2.0:        nshade = u'\u2592'
#                 elif fdistancetowall < fdepth:              nshade = u'\u2591'
#                 else:                                       nshade = ' '        # too far away

#                 if bboundary:       nshade = ' ' # black it out

#                 for y in range(0, nscreenheight):

#                     # each row
#                     if y < nceiling:
#                         screen[y][x] = ' '
#                     elif y > nceiling and y <= nfloor:
#                         screen[y][x] = nshade
#                     else: # floor

#                         # shade floor based on distance
#                         b = 1.0 - ((float(y) - nscreenheight/2.0) / (float(nscreenheight) / 2.0))
#                         if b < 0.25:        nshade2 = '#'
#                         elif b < 0.5:       nshade2 = 'x'
#                         elif b < 0.75:      nshade2 = '.'
#                         elif b < 0.9:       nshade2 = '-'
#                         else:               nshade2 = " "
#                         screen[y][x] = nshade2


#             # display map
#             for nx in range(0, nmapwidth):
#                 for ny in range(0, nmapwidth):

#                     screen[ny + 1][nx] = map[ny][nx]
                    
#             screen[int(fplayery)+1][int(fplayerx)] = 'p'

#             # display frame
#             screen[nscreenheight - 1][nscreenwidth - 1] = '\0'
#             string_screen = ''.join(ele for sub in screen for ele in sub)

#             # adding saved screen to cache
#             cache[("%.1f" % fplayera, "%.1f" % fplayerx, "%.1f" % fplayery)] = [string_screen]



# import pandas as pd

# df = pd.dataframe.from_dict(cache)

# df.to_csv('cmd_cache.csv')


# print('finished')


# fplayerx = 14.7             # player start position
# fplayery = 5.09
# fplayera = 0.0              # player start rotation






while 1:

    # we'll need time differential per frame to calculate modification
    # to movement speeds, to ensure consistant movement, as ray-tracing
    # is non-deterministic
    tp2 = time.clock()
    elapsedtime = tp2 - tp1
    tp1 = tp2
    felapsedtime = elapsedtime

    if keyboard.key_down == 'down':

        # exits game loop
        if keyboard.is_pressed('p'):
            sys.exit()


        # handle ccw rotation
        if keyboard.is_pressed('a'):

            fplayera -= (fspeed * 0.75) * felapsedtime

        # handle cw rotation
        if keyboard.is_pressed('d'):

            fplayera += (fspeed * 0.75) * felapsedtime

        # handle forwards movement & collision
        if keyboard.is_pressed('w'):

            fplayerx += math.sin(fplayera) * fspeed * felapsedtime
            fplayery += math.cos(fplayera) * fspeed * felapsedtime
            if map[int(fplayery)][int(fplayerx)] == '#':

                fplayerx -= math.sin(fplayera) * fspeed * felapsedtime
                fplayery -= math.cos(fplayera) * fspeed * felapsedtime

        # handle backwards movement & collision
        if keyboard.is_pressed('s'):

            fplayerx -= math.sin(fplayera) * fspeed * felapsedtime
            fplayery -= math.cos(fplayera) * fspeed * felapsedtime
            if map[int(fplayery)][int(fplayerx)] == '#':

                fplayerx += math.sin(fplayera) * fspeed * felapsedtime
                fplayery += math.cos(fplayera) * fspeed * felapsedtime

    # how angle is saved in cahce
    fplayera = fplayera % 6

    # checking if screen has already been solved
    if ("%.1f" % fplayera, "%.1f" % fplayerx, "%.1f" % fplayery) in cache:
        string_screen = cache[("%.1f" % fplayera, "%.1f" % fplayerx, "%.1f" % fplayery)][0]


    # if not solved, then solve
    else:
        for x in range(0, nscreenwidth):

            # for each column, calculate the projected ray angle into world space
            frayangle = (fplayera - ffov/2.0) + (float(x) / float(nscreenwidth)) * ffov

            # find distance to wall
            fstepsize = 0.1         # increment size for ray casting, decrease to increase
            fdistancetowall = 0     #                                      resolution

            bhitwall = false       # set when ray hits wall block
            bboundary = false      # set when ray hits boundary between two wall blocks

            feyex = math.sin(frayangle) # unit vector for ray in player space
            feyey = math.cos(frayangle)

            # incrementally cast ray from player, along ray angle, testing for 
            # intersection with a block
            while bhitwall == false and fdistancetowall < fdepth:

                fdistancetowall += fstepsize
                ntestx = int(fplayerx + feyex * fdistancetowall)
                ntesty = int(fplayery + feyey * fdistancetowall)

                # test if ray is out of bounds
                if ntestx < 0 or ntestx >= nmapwidth or ntesty < 0 or ntesty >= nmapheight:

                    bhitwall = true         # just set distance to maximum depth
                    fdistancetowall = fdepth

                else:

                    # ray is inbounds so test to see if the ray cell is a wall block
                    if map[ntesty][ntestx] == '#':

                        # ray has hit wall
                        bhitwall = true

                        # to highlight tile boundaries, cast a ray from each corner
                        # of the tile, to the player. the more coincident this ray
                        # is to the rendering ray, the closer we are to a tile 
                        # boundary, which we'll shade to add detail to the walls
                        p = []

                        # test each corner of hit tile, storing the distance from
                        # the player, and the calculated dot product of the two rays
                        for tx in range(0,2):
                            for ty in range(0,2):

                                # angle of corner to eye
                                vy = float(ntesty) + ty - fplayery
                                vx = float(ntestx) + tx - fplayerx
                                d = sqrt(vx*vx + vy*vy)
                                dot = (feyex * vx / d) + (feyey * vy / d)
                                p.append((d, dot))
                        
                        # sort pairs from closest to farthest
                        p.sort(key=lambda x: x[0])

                        # first two/three are closest (we will never see all four)
                        fbound = 0.01
                        if math.acos(p[0][1]) < fbound: bboundary = true
                        if math.acos(p[1][1]) < fbound: bboundary = true
                        if math.acos(p[2][1]) < fbound: bboundary = true




            # calculate distance to ceiling and floor
            nceiling = float(nscreenheight/2.0) - nscreenheight / float(fdistancetowall)
            nfloor = nscreenheight - nceiling

            # shader walls based on distance
            nshade = ' '
            if fdistancetowall <= fdepth / 4.0:         nshade = u'\u2588'     # very close
            elif fdistancetowall < fdepth / 3.0:        nshade = u'\u2593'
            elif fdistancetowall < fdepth / 2.0:        nshade = u'\u2592'
            elif fdistancetowall < fdepth:              nshade = u'\u2591'
            else:                                       nshade = ' '        # too far away

            if bboundary:       nshade = ' ' # black it out

            for y in range(0, nscreenheight):

                # each row
                if y < nceiling:
                    screen[y][x] = ' '
                elif y > nceiling and y <= nfloor:
                    screen[y][x] = nshade
                else: # floor

                    # shade floor based on distance
                    b = 1.0 - ((float(y) - nscreenheight/2.0) / (float(nscreenheight) / 2.0))
                    if b < 0.25:        nshade2 = '#'
                    elif b < 0.5:       nshade2 = 'x'
                    elif b < 0.75:      nshade2 = '.'
                    elif b < 0.9:       nshade2 = '-'
                    else:               nshade2 = " "
                    screen[y][x] = nshade2


        # display map
        for nx in range(0, nmapwidth):
            for ny in range(0, nmapwidth):

                screen[ny + 1][nx] = map[ny][nx]
                
        screen[int(fplayery)+1][int(fplayerx)] = 'p'

        # display frame
        screen[nscreenheight - 1][nscreenwidth - 1] = '\0'
        string_screen = ''.join(ele for sub in screen for ele in sub)

        # adding saved screen to cache
        cache[("%.1f" % fplayera, "%.1f" % fplayerx, "%.1f" % fplayery)] = [string_screen]



    # display stats
    view = curses.initscr()
    curses.curs_set(0)
    stats = f'x={"%.2f" % fplayerx}, y={"%.2f" % fplayery}, a={"%.2f" % fplayera}, fps={"%.2f" % (1.0 / felapsedtime)}'
    stats_window = curses.newwin(1, len(stats) + 1, 0, 0)
    stats_window.addstr(0, 0, stats)
    stats_window.refresh()

    # display frame
    view.addstr(0, 0, string_screen)
    view.refresh()
    

# that's it!! - tyler
