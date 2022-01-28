# Ray Casting Algorithm

### Introduction

Ray Casting is a lightweight technique for 3D graphical rendering that when implemented correctly creates a compelling illusion of an explorable 3d space. This project explores the concepts of ray casting and allows the user to use various methods of rendering the environment. 

**Gallary**

![](img/gallery.png)

### Usage

This codebase is built to run on Windows computers and the virtual environment requires python 3.7 to be installed.

The following files:

- Ray_Casting_Classic.py
- Ray_Casting_Textured.py
- Ray_Casting_Hashed.py
- Ray_Casting_Hashed_color.py

Are all created to demonstrate different rendering methods of the Simulation Class within the repo. All rendering methods are built on top of the same ray casting algorithm. To test each method the associated file can be run directly.

There are limitations that should be noted:
All fills use ASCII characters from the extended set and may not be available with all command prompts
The Simulation Class uses colors when rendering text that not all command prompts support
Ray Casting Hashed and Ray Casting Hashed Color require JSON files of a pre-hashed map of the 3d environment. The user can create these files with the Make_Hashed_Map.py file. Alternatively, several of these pre-hashed files can be downloaded below as they are too large to store on GitHub and each requires at least 8 gigabytes of memory to run. Save these files in an extracted state in the hashed_map directory of this repo.


**Creating Maps**

Users can create maps that can be rendered with any of the above-listed methods. Maps exist as 2-dimensional arrays and consist of one ‘p’ ASCII character as well as a mix of ‘#’ characters representing walls and ‘.’ characters representing empty space.

An example of a constructed map:
```
map_two = []
map_two.append(list('################'))
map_two.append(list('#.#.....p......#'))
map_two.append(list('#.#............#'))
map_two.append(list('#.#............#'))
map_two.append(list('#.#............#'))
map_two.append(list('#..............#'))
map_two.append(list('#.#.....#....###'))
map_two.append(list('#.#.....#......#'))
map_two.append(list('#.#.....#....###'))
map_two.append(list('#.#.....#......#'))
map_two.append(list('#.##....#......#'))
map_two.append(list('#...#.......####'))
map_two.append(list('#.##...........#'))
map_two.append(list('#.#.........#..#'))
map_two.append(list('#...........#..#'))
map_two.append(list('################'))
```

Player spawns in at the location of p facing the southern direction.

**Hashing Maps**

Once a map is constructed the maps can be hashed by running the Make_Hashed_Map.py file and specifying which map to be hashed. Depending on the size of the map hashing can take 30 minutes to several hours. Several maps have been pre-hashed and saved to a personal google drive account.

Map One Hashed Download [Here](https://drive.google.com/file/d/1Ws2Q2WXOJVLGt2i_gu-BLtg3crU63zSK/view?usp=sharing)

Map Two Hashed Download [Here](https://drive.google.com/file/d/1BNAjFWH12K9ixtiiuNjB-0_zz1oh_Mxe/view?usp=sharing)

**Creating Sprites**

Sprite textures can be used to change the textures of the wall in the simulation. There is currently a designed brick wall texture. New textures can be created by making a 2-dimensional array of strings representing color information (It should be noted that structure has not yet been built in this repo to make new sprite creation user-friendly). The Simulation Class is currently wired to handle red and white colors. However, manual manipulation of these colors can be changed in the files. Please reference the [python-curses](https://docs.python.org/3/howto/curses.html) documentation for more information on coloring text in the command prompt.

**Executables**

For demonstration purposes, executable files have been created that run without the need to set up an environment.

Ray Casting Classic Executable [Here](https://drive.google.com/file/d/153Kjcn8uFgkFhVWm62GR0R6aivwlmxeR/view?usp=sharing)

Ray Casting Textured Executable [Here](https://drive.google.com/file/d/1R-rmk3PQfAUNCWO82qQgjGl1lbZbg5ZQ/view?usp=sharing)

# Overview of the Ray Casting Algorithm and it's implementation

**The Command Prompt**

The command prompt (cmd) is the default command-line interpreter for windows operating systems. It is a tool for interfacing with the computer through text-based commands in the form of ASCII characters. Due to this, the cmd offers two valuable features that will be used to construct the ray casting 3d simulation. Firstly, the cmd interacts with the hardware of the computer allowing for python scripts to be executed by the command line. Secondly, since the cmd has mechanics for rendering ASCII characters each character can be treated as a colored/shaded pixel and the cmd output screen can be used as the view of the 3d simulation. However, the standard print() function of python that is used for outputting text is unoptimized for rendering. The third-party python library curses will be used to efficiently render the text-based pixels.

**Curses**

Curses is a program written in C designed to communicate with text-based display terminals. The program creates a terminal independent screen painting that efficiently renders text. The python wrapper of Curses also gives full control over each text-character location and color on the independently painted screen. The Curses python library allows for the ray casting algorithm to be implemented in the python programming language. Without it, many C-based commands would have to be written to interface with the visual side of the command prompt.

**ASCII Characters**

ASCII (American Standard Code for Information Interchange) Characters are encoded values for electronic communication. ASCII characters are used in text-based display terminals such as the command prompt. These characters include the standard 0-127 character set as well as many extended sets for specialized purposes. For the purposes of the ray casting cmd implementation, the standard set and the 128-255 extended character set are utilized. From the standard ASCII character set the character used are  ```‘ ’, ‘.’, ‘-’, ‘x’, ‘#’, ‘p’, ‘R’, ‘W’, ‘C’, ‘G’```. From the extended character set the characters are ```u'\u2588', u'\u2593', u'\u2592', u'\u2591'``` (expressed in Unicode format). These characters are used for representing simulation elements on the output screen. 

**Font Manipulation**

To create a more detailed representation of the 3D simulation the cmd font sizes can be altered to a smaller scale. The change to a smaller font size forces each text cell to be closer to the size of a traditional pixel. A custom connection to interface with the command lines font size has been written with python c-types allowing for C commands to be integrated within the ray casting program.

### Ray Casting

**Defining the Map**

The simulation exists as a 2d array. The array is made up of arrays of strings representing the objects in the 3d space. The characters used in the 2d array are ‘p’ for player location, ‘#’ for wall location, ‘.’ for empty space. In this space, each character is defined as a one-by-one unit square. The implemented map is a 16 by 16 2d array. 

**Casting Rays Overview**

The number of rays cast out is dependent on the screen width. Each ray shot in the 2d map array space will translate to one column in the screen display array. The distance it takes each ray to reach a wall describes how many rows of each column are filled in with ceiling vs wall vs floor characters. The distance also has an effect on the shaded wall character used in the rendered screen.

**Field of View**

The field of view is defined in this implementation as how much of the two divided by pi radian space around the player will be displayed in the scene. Pi divided by four (making up one eighth of the total visual space information) will be the player’s seen field of view. 

**<img src="https://render.githubusercontent.com/render/math?math=FOV = \frac{\pi}{4.0}">**

**Ray Angle**

For each ray in the width of the screen, there is an associated angle that the ray is shooting out at in the 2d map array space. The goal is to have several rays (one for each column in the screen width) whose angles lay within the player’s field of view. This angle is calculated by taking the player’s current angle and subtracting half the field of view. We then add the current column divided by the width of the screen times the player’s field of view. The result is a ray with an angle that aligns with a given column slot within the player’s field of view.

**<img src="https://render.githubusercontent.com/render/math?math=RayAngle\theta = (PlayerAngle\theta - \frac{FOV}{2}) %2B \frac{ScreenColumn}{ScreenWidth} \times FOV">**

**Unit Vector**

To begin the process of solving the distance from the player to the wall a unit vector is calculated for each ray angle in the screen width. The vector is calculated by taking the sine() and cosine() of the ray angle

**<img src="https://render.githubusercontent.com/render/math?math=\vec{X} = cos(RayAngle\theta)">**

**<img src="https://render.githubusercontent.com/render/math?math=\vec{Y} = sin(RayAngle\theta)">**

The importance of the unit vector is it translates or current ray angle into a scalable direction with a length.

**Distance to the Wall**

To calculate the distance of each ray (from player to a wall) a step size variable is used. For each iteration until a wall is hit the step size is added to the current distance traveled. This value then becomes a scaler that is multiplied by the unit vector. The origin of the vector is set by adding the scaled vector to the player’s x and y coordinates.

**<img src="https://render.githubusercontent.com/render/math?math=\vec{PlayerX} = PlayerX %2B \vec{X} \times CurrentDistance">**

**<img src="https://render.githubusercontent.com/render/math?math=\vec{PlayerY} = PlayerY %2B \vec{Y} \times CurrentDistance">**


The test_x(PlayerX Vector) and test_y(PlayerY Vector) floating-point numbers are then converted to integers and are used as index positions in the 2d map array. If the current value at the given indices is equal to ‘.’ the ray currently exists in an empty space. However, if the current value at the given indices is equal to ‘#’ this represents a wall in 2d map array space and a boolean flag is raised.

To avoid infinite rays being cast out into empty space a max depth variable is set limiting the max distance a ray can travel without intercepting a block space.

**Vertical Calculations**

After the ray has been cast and the distance to the wall has been calculated. The goal then becomes to fill in each row of a given column with text-based information representing the ceiling, wall, and floor. The y-coordinate space runs from the top to the bottom of our screen display array. 0 represents the first row and the screen display array height - 1 represents the last row. 

**The Ceiling**

From the top of the screen display array to the beginning of the represented wall are index positions that need to be filled with text-based characters representing the ceiling. The ceiling region of space is determined by finding the last y index to represent ceiling characters. This is done by taking half the screen height subtracted by the screen height divided by the distance to the wall for the current column.

**<img src="https://render.githubusercontent.com/render/math?math=CeilingStopIndex = \frac{ScreenHeight}{2} - \frac{ScreenHeight}{DistanceToWall}">**

All rows until this calculated index will be filled with ceiling text-based characters.

**The Floor**

The floor is simply the opposite of the ceiling and can be calculated as screen display array height minus the ceiling index.

**<img src="https://render.githubusercontent.com/render/math?math=FloorStartIndex = ScreenHeight - CeilingStopIndex">**

All rows after the floor index will be filled with floor text-based characters.

**The Wall**

The wall is all index positions of the screen display array that exist between the ceiling stop index and the floor start index.

### Rendering

The Project is designed to render scenes in three distinct ways. Each method represents a milestone achieved in the project. For the purposes of demonstration as progress was made with the simulation the previous rendering techniques were kept despite them becoming obsolete. The methods of rendering are **classic**, **textured**, and **hashed** each accomplishing specific goals based on the current knowledge and resources had at the time.

**Classic Rendering**

This method involves creating the 3d environment fully with ASCII characters rendered in with the default command prompt color of white text and a black background. With this color limitation, the strategy became to use different ASCII characters of different sizes to create shading effects that reflected depth in the simulation. The classic rendering method also makes use of a boundary line texturing technique that fixes several visual issues.

**Shading**

For the ceiling objects, the space character ‘ ‘ was used as it shades in as black. For the floor objects, a combination of  ```‘.’, ‘-’, ‘x’, ‘#’``` characters are used. The closer a given floor object is to the player the larger of an ASCII character is used. Alternatively, the further a given floor object is to the player the smaller of an ASCII character is used. The difference in the shape of these characters helps to create the illusion of depth on the screen. For the wall characters, several ASCII extended set characters are used and exist in a Unicode format  ```u'\u2588', u'\u2593', u'\u2592', u'\u2591'```. Each character is a block shape with dots within it. For walls close to the player the fully shaded-in block character is used. For walls further away a less densely filled-in block character is used. Similar to the floor shading method, the wall shading method also helps in creating the illusion of depth on the player’s screen.

**Boundary Lines**

The 3d simulation is able to project the ceiling, wall, and floor. To remove the visual issue of not being able to distinguish each wall cell from one another in the 3d space a boundary line texture is added to the walls. The difficulty of adding boundary lines is each ray cast out only has information on if it has intercepted a block or not (boolean flag). There is no intelligent communication between rays. The purposed solution is a manipulation of the current hit block corners and their relation to the current cast ray that has intersected the wall.

Firstly, a vector is created for each corner of a hit block back to the player. This is done by taking the current ray vector adding the current corner of the block minus the player’s coordinate.

**<img src="https://render.githubusercontent.com/render/math?math=\vec{CornerX} = \vec{PlayerX} %2B CornerX - PlayerX">**

**<img src="https://render.githubusercontent.com/render/math?math=\vec{CornerY} = \vec{PlayerY} %2B CornerY - PlayerY">**


For each of these new vectors, a magnitude is set so that the vector’s length is that of the corner to the player location. This is done by taking the square root of CornerX Vector times CornerX Vector plus CornerY Vector times CornerY Vector.

**<img src="https://render.githubusercontent.com/render/math?math=Magnitude = \sqrt{\vec{CornerX} \times \vec{CornerX} %2B \vec{CornerY} \times \vec{CornerY}}">**

Secondly, the dot product is calculated for the unit vector of the current ray cast out and for each of the corners unit vectors just created.

**<img src="https://render.githubusercontent.com/render/math?math=DotProduct = (\vec{X} \times \vec{CornerX} \div Magnitude) %2B (\vec{Y} \times \vec{CornerY} \div Magnitude)">**

Lastly, each corner vector and dot product pair are sorted in order by distance (corner vector’s magnitude) from the corner to the player.

In the given 3d environment only three corners of a block can be seen at once due to perspective. The first three closest corners of the block will be used for boundary texturing. By taking the inverse cosine of the dot product a new angle is created that represents the angle between the current cast out ray and the corner to player ray. A boundary angle size limit is set ahead of time. If the new angle in question is smaller than the predetermined boundary angle size limit the current cast out ray is flagged as a boundary ray and will be textured accordingly. This process is repeated for each of the three closest corners to the player of the hit block.

**<img src="https://render.githubusercontent.com/render/math?math=Angle\theta = cos^{-1}(DotProduct)">**

**If angle < 0.05 #(boundary angle limit size) it is a boundary**

A negative effect of this texturing approach is for each hit block three boundary lines will always be textured in. If a player is only facing one side of a block the third boundary line will be shaded in appearing through the face of the wall affecting the quality of the simulation.

**Texture Rendering**

This method involves creating the 3d environment with the use of the space ```‘ ‘``` ASCII character and then shading in each blank space as a different color depending on if it is a ceiling, wall, or floor object. A texture mapping process is added to the screen to inform the program what color to shade in each space character during rendering. The texture mapping process returns ASCII character values ```‘C‘, ‘R’, ‘W’, ‘G’```. The character C represents the ceiling object and is colored in as black, R and W represent wall objects and are colored in as either red or white, and G represents the ground object and is colored in as green.

**Texture Mapping**

The 3d space visualizes the ceiling, wall, and floor. The results of this are compelling, but the rendered wall is in greyscale and is lacking any sort of detail. The mapping of textures on wall objects in the simulation provides a more vibrant and immersive experience. To accomplish this a sprite with color information needs to be created, the normalized sample coordinates x and y need to be calculated, and the sprite texture needs to be sampled for rendering.

**Sprites**

In this implementation, a sprite is treated as a 2-dimensional array where each value represents a color. The collection of colors in the array comes together to form an image. The sprite is designed in such a way that given an x and y index location the 2d array returns a value representing which color to shade in the current text-based pixel on the player’s screen. The sprite used in this project exists as a 32 by 32 value image.

**Sampling Coordinates**

A given block in the 3d simulation exists as a unit square from length zero to one. The goal is to map the 32 by 32 sized sprite to the face of a unit square in the simulation. This is done by finding a normalized coordinate x for the horizontal position of the image and a normalized coordinate y for the vertical position of the image. The x sample coordinate is found by finding the midpoint of the hit block. Finding where the current casted ray hit the wall (x, y coordinates).  Creating a vector based on the midpoint and where the ray hit the wall. Then determining which side of the block was hit (with the aid of the newfound vector) and taking the associated x or y value for that wall’s side. This value represents the normalized x position of what part of the block was hit by the casted ray. The y sample coordinate is found by returning a normalized y value relative to the known wall height in vertical space(The space between the ceiling stop index and the floor start index).

**X Sample Coordinate**

Firstly, the midpoint of the hit block needs to be calculated. This is found by taking the previously found test_x(PlayerX Vector) and test_y(PlayerY Vector) variables (which are currently the index locations of a the hit block in the 2d map array) and adding 0.5 to each since each block is a unit square of 1.

**<img src="https://render.githubusercontent.com/render/math?math=MidPointX = \vec{PlayerX} %2B 0.5">**

**<img src="https://render.githubusercontent.com/render/math?math=MidPointY = \vec{PlayerY} %2B 0.5">**

Secondly, the coordinates of where the block wall was hit need to be calculated. This is done by taking the player’s coordinates plus the ray’s unit vector times the calculated distance to the wall

**<img src="https://render.githubusercontent.com/render/math?math=HitPointX = PlayerX %2B \vec{X} \times DistanceToWall">**

**<img src="https://render.githubusercontent.com/render/math?math=HitPointY = PlayerY %2B \vec{Y} \times DistanceToWall">**

Lastly, the side of the hit block needs to be known. Depending on which side of the block is hit the sample x coordinate will equal either the - x, x, -y, y coordinate of where the ray hit the wall. To calculate this we can use a slightly rotated arctan 2 function that will map each quadrant of the unit block to a side.

**<img src="https://render.githubusercontent.com/render/math?math=Angle\theta = arctan^{2}((HitPointY - MidPointY), (HitPoinitX - MidPointX))">**

The arctan 2 function returns a one-dimensional variable within a negative pi to positive pi radian space. The value of the test_angle(Angle theta) represents which quadrant the ray hit. The normalized sample x value is then set based on which quadrant was hit. If in quadrant pi divided by two sample x is set as test_point_y(HitPointY)(y coordinate of where the ray hit the wall) minus test_y(Y Vector)(y integer location of the wall in 2d map array space). If in quadrant pi sample x is set as test_point_x(HitPointX)(x coordinate of where the ray hit the wall) minus test_x(X Vector)(x integer location of the wall in 2d map array space). If in quadrant negative pi sample x is set as test_point_x minus test_x. If in quadrant negative pi divided by two sample x is set as test_point_y minus test_y.

The resulting sample x value is a normalized horizontal coordinate that can be used for texture sampling

**Y Sample Coordinate**

To calculate the sample_y coordinate the current row of the screen is taken minus the ceiling stop index divided by the (floor_start_index minus ceiling_stop_index)

**<img src="https://render.githubusercontent.com/render/math?math=SampleY = (ScreenRow - CeilingStopIndex) \div (FloorStartIndex - CeilingStopIndex)">**

The resulting sample y value is a normalized vertical coordinate that can be used for texture sampling.

**Sampling the Sprite Texture**

The sample y and sample x values now represent where to sample a texture in a normalized space of zero to one. Where sample x and sample y are floating-point values.

Given the normalized coordinates, the coefficients are removed. The remaining floating-point values are then multiplied by the sprite width and height.

**<img src="https://render.githubusercontent.com/render/math?math=SpriteIndexX = SampleX \times SpriteWidth">**

**<img src="https://render.githubusercontent.com/render/math?math=SpriteIndexY = SampleY \times SpriteHeight">**

The resulting values are x and y index positions that can be used to grab a value in the 2d sprite array.

The result of the full texture mapping process is a fully mapped texture to the walls of the 3d simulation.


**Hashed Screen Rendering**

One limitation of building this project in the python programming language is speed. High-level programming languages such as python are slower at computation when compared to low-level languages such as c++. Python functions fine for the classic rendering method, however with the texturing method performance is limited. The main issue is the need for more detail to get the full effect of the textures. This requires more computation and ultimately lowers the frame rate of the simulation. Computation at runtime is no longer effective and the frame rate(iteration speed) of the simulation is far too slow. The proposed solution for demonstration purposes is to do all the calculations in the simulation ahead of time and store those values so that at runtime the values can be referenced from computer memory.

**Hashing**

The hashing method for every possible player position in the simulated map returns a string of values to be rendered to the screen. In this implementation, the string is made up of ```‘C, R, W, G‘``` and space ```‘ ‘``` characters to be converted to color at runtime.

**Keys**

The key to the hash is a tuple of the current position of the player in the simulation. This tuple consists of the player’s angle, y-coordinate, and x-coordinate in the 2d map array. As an optimization, the player angle is limited to four positions (0 radians, pi divided by 2 radians, pi radians, and pi plus pi divided by 2 radians) rather than the full radian space available in the classic and texture render methods. The angle limit is a compromise of limiting player mobility to reduce the time and memory needed to make the hashed map.

**Values**

The returned values of the hash are strings containing texture information for each text-based character to be displayed on the player’s screen given the player’s current location. The string length is the product of the player’s screen height times the player’s screen width. Hashed values are calculated through a similar process as the texture rendering method with the exception that values calculated are saved to a hash for use at a later rendering time.

**Hashed Results**

Once constructed the hashed rendering method achieves an experience that could not be observed with computation at runtime using python. However, the large JSON files that the maps are stored in are memory intensive and require storage in google drive to be downloaded before runtime rather than being stored as part of the project repo.
