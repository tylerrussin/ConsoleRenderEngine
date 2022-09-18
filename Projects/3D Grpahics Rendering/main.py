'''Graphical Rendering in The Command Line'''
import sys
import time
import keyboard

import vectors
import matrices
import meshes

# Path to console_render_engine.py
sys.path.append('../..')

import console_render_engine


def point_at(pos: vectors.Vector, target: vectors.Vector,
             up: vectors.Vector) -> matrices.ProjectionMatrix:
    '''Calculate the new projection matrix based on target and up vectors'''

    # Calculate forward direction
    new_forward = vectors.subtract(target, pos)
    new_forward = vectors.normalize(new_forward)

    # Calculate up direction
    a = vectors.multiply(new_forward, vectors.dot_product(up, new_forward))
    new_up = vectors.subtract(up, a)
    new_up = vectors.normalize(new_up)

    # Calculate right direction
    new_right = vectors.cross_product(new_up, new_forward)

    # Define dimensioning and translation matrix
    matrix = matrices.ProjectionMatrix()
    matrix.m[0][0] = new_right.x
    matrix.m[0][1] = new_right.y
    matrix.m[0][2] = new_right.z
    matrix.m[0][3] = 0

    matrix.m[1][0] = new_up.x
    matrix.m[1][1] = new_up.y
    matrix.m[1][2] = new_up.z
    matrix.m[1][3] = 0

    matrix.m[2][0] = new_forward.x
    matrix.m[2][1] = new_forward.y
    matrix.m[2][2] = new_forward.z
    matrix.m[2][3] = 0

    matrix.m[3][0] = pos.x
    matrix.m[3][1] = pos.y
    matrix.m[3][2] = pos.z
    matrix.m[3][3] = 1

    return matrix

def point_dist(point: vectors.Vector, plane_normal, plane_point) -> int:
    '''Calculates the distance of a point to the closest point on a plane'''

    return (plane_normal.x * point.x + plane_normal.y * point.y + plane_normal.z * point.z -
            vectors.dot_product(plane_normal, plane_point))


def triangle_clip(plane_point: vectors.Vector, plane_normal:vectors.Vector,
                  in_tri: meshes.Triangle, out_tris: list) -> int:
    '''Clip a given triangle against a given plane'''

    # Normalize plane norma;
    plane_normal = vectors.normalize(plane_normal)

    # Storage arrays to sort triangle points based on distance
    inside_points = []
    outside_points = []

    # Get signed distance of each point in triangle to plane
    dist_1 = point_dist(in_tri.vec_1, plane_normal, plane_point)
    dist_2 = point_dist(in_tri.vec_2, plane_normal, plane_point)
    dist_3 = point_dist(in_tri.vec_3, plane_normal, plane_point)

    if dist_1 >= 0:
        inside_points.append(in_tri.vec_1)
    else:
        outside_points.append(in_tri.vec_1)

    if dist_2 >= 0:
        inside_points.append(in_tri.vec_2)
    else:
        outside_points.append(in_tri.vec_2)

    if dist_3 >= 0:
        inside_points.append(in_tri.vec_3)
    else:
        outside_points.append(in_tri.vec_3)

    # All points outside the plane
    if len(inside_points) == 0:

        return 0

    # Populate output triangles with valid and clipped points

    # All points inside the plane
    if len(inside_points) == 3:

        out_tris[0].vec_1 = in_tri.vec_1
        out_tris[0].vec_2 = in_tri.vec_2
        out_tris[0].vec_3 = in_tri.vec_3

        out_tris[0].col =  in_tri.col
        out_tris[0].sym = in_tri.sym

        return 1

    # Two points lie outside the plane, clip into one new triangle
    if len(inside_points) == 1 and len(outside_points) == 2:

        out_tris[0].col = in_tri.col
        out_tris[0].sym = in_tri.sym

        # Inside point is valid
        out_tris[0].vec_1 = inside_points[0]

        # Calculate two new outside point positions
        out_tris[0].vec_2 = vectors.intersect_plane(plane_point, plane_normal,
                                                       inside_points[0], outside_points[0])
        out_tris[0].vec_3 = vectors.intersect_plane(plane_point, plane_normal,
                                                       inside_points[0], outside_points[1])

        return 1

    # One point lies outside the plane, clip into two new triangles
    if len(inside_points) == 2 and len(outside_points) == 1:

        out_tris[0].col = in_tri.col
        out_tris[0].sym = in_tri.sym

        out_tris[1].col =  in_tri.col
        out_tris[1].sym = in_tri.sym

        # meshes.Triangle one has two valid points
        out_tris[0].vec_1 = inside_points[0]
        out_tris[0].vec_2 = inside_points[1]

        # Calculate triangle one's new outside point postion
        out_tris[0].vec_3 = vectors.intersect_plane(plane_point, plane_normal,
                                                       inside_points[0], outside_points[0])

        # meshes.Triangle two has one valid point
        out_tris[1].vec_1 = inside_points[1]

        # Calculate triangle two's new outside point postions
        out_tris[1].vec_2 = out_tris[0].vec_3
        out_tris[1].vec_3 = vectors.intersect_plane(plane_point, plane_normal,
                                                       inside_points[1], outside_points[0])

        return 2


if __name__ == '__main__':

    CMD_FONT = 5            # Console ASCII font size
    SCREEN_WIDTH = 256      # Console Screen Size X (columns)  #256#
    SCREEN_HEIGHT = 127     # Console Screen Size Y (rows)

    cmd_engine = console_render_engine.ConsoleRenderEngine(CMD_FONT, SCREEN_WIDTH, SCREEN_HEIGHT)
    cmd_engine.on_user_create()

    tp1 = time.perf_counter()
    tp2 = time.perf_counter()
    THETA = 0

    v_camera = vectors.Vector()
    v_look_dir = vectors.Vector()
    yaw = 0

    mesh = meshes.LoadMesh('data/spaceship.obj')

    matrix_prog = matrices.make_projection(90, SCREEN_HEIGHT / SCREEN_WIDTH, 0.1, 1000)

    # Simulation loop
    while 1:

        cmd_engine.reset_screen()

        # Calculate time differential per frame
        tp2 = time.perf_counter()
        elapsed_time = tp2 - tp1
        tp1 = tp2
        THETA += 1 * elapsed_time


        # Quit simulation
        if keyboard.is_pressed('P'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # Move v_camera
        if keyboard.is_pressed('UP_ARROW'):
            v_camera.y += 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('DOWN_ARROW'):
            v_camera.y -= 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('LEFT_ARROW'):
            v_camera.x += 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('RIGHT_ARROW'):
            v_camera.x -= 8 * elapsed_time

        v_forward = vectors.multiply(v_look_dir, 8 * elapsed_time)

        # Move yaw
        if keyboard.is_pressed('W'):
            v_camera = vectors.add(v_camera, v_forward)
        # Move yaw
        if keyboard.is_pressed('S'):
            v_camera = vectors.subtract(v_camera, v_forward)

        # Move yaw
        if keyboard.is_pressed('A'):
            yaw -= 2 * elapsed_time
        # Move yaw
        if keyboard.is_pressed('D'):
            yaw += 2 * elapsed_time


        # Rotation Z and X projection matrices
        mat_rot_z = matrices.make_rotation_z(THETA)
        mat_rot_x = matrices.make_rotation_x(THETA * 0.5)

        mat_trans = matrices.make_translation(0, 0, 8)

        mat_world = matrices.make_identity()                            # Form World Matrix
        mat_world = matrices.multiply_matrix(mat_rot_z, mat_rot_x)      # Transform by rotation
        mat_world = matrices.multiply_matrix(mat_world, mat_trans)      # Transform by translation

        # Camera movement
        v_up = vectors.Vector(0, 1, 0)
        v_target = vectors.Vector(0, 0, 1)
        mat_camera_rot = matrices.make_rotation_y(yaw)
        v_look_dir = vectors.multiply_matrix_vector(mat_camera_rot, v_target)
        v_target = vectors.add(v_camera, v_look_dir)

        mat_camera = point_at(v_camera, v_target, v_up)
        mat_view = matrices.quick_inverse(mat_camera)


        vec_triangles_to_raster = []

        # Iterate through triangles
        for tri in mesh.tris:

            # Initiate triangles
            tri_projected = meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())
            tri_transformed = meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())
            tri_viewed = meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())

            # World matrix transform
            tri_transformed.vec_1 = vectors.multiply_matrix_vector(mat_world, tri.vec_1)
            tri_transformed.vec_2 = vectors.multiply_matrix_vector(mat_world, tri.vec_2)
            tri_transformed.vec_3 = vectors.multiply_matrix_vector(mat_world, tri.vec_3)

            # Get lines either side of triangle
            line1 = vectors.subtract(tri_transformed.vec_2, tri_transformed.vec_1)
            line2 = vectors.subtract(tri_transformed.vec_3, tri_transformed.vec_1)

            # Take cross product of lines to get normal to triangle surface
            normal = vectors.cross_product(line1, line2)
            normal = vectors.normalize(normal)

            # Get Ray from triangle to camera
            vCameraRay = vectors.subtract(tri_transformed.vec_1, v_camera)

            # If ray is aligned with normal, then triangle is visible
            if vectors.dot_product(normal, vCameraRay) < 0:

                # Illumination
                light_direction = vectors.Vector(0, 1, -1)
                light_direction = vectors.normalize(light_direction)

                # Calculate dot product of triangle normal and light direction
                # How "aligned" are light direction and triangle surface normal?
                dp = max(0.1, vectors.dot_product(light_direction, normal))

                # Set symbol in triangle
                col, sym = cmd_engine.get_shaded_color(dp)
                tri_transformed.col = col
                tri_transformed.sym = sym

                # Convert world space --> view space
                tri_viewed.vec_1 = vectors.multiply_matrix_vector(mat_view, tri_transformed.vec_1)
                tri_viewed.vec_2 = vectors.multiply_matrix_vector(mat_view, tri_transformed.vec_2)
                tri_viewed.vec_3 = vectors.multiply_matrix_vector(mat_view, tri_transformed.vec_3)
                tri_viewed.sym = tri_transformed.sym
                tri_viewed.col = tri_transformed.col

                # Clip triangles outside of view
                clipped = [meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector()),
                           meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())]
                clipped_triangles = triangle_clip(vectors.Vector(0,0,0.5), vectors.Vector(0,0,1),
                                                  tri_viewed, clipped)


                for n in range(0, clipped_triangles):

                    # Project triangles from 3D -> 2D
                    tri_projected.vec_1 = vectors.multiply_matrix_vector(matrix_prog,
                                                                         clipped[n].vec_1)
                    tri_projected.vec_2 = vectors.multiply_matrix_vector(matrix_prog,
                                                                         clipped[n].vec_2)
                    tri_projected.vec_3 = vectors.multiply_matrix_vector(matrix_prog,
                                                                         clipped[n].vec_3)
                    tri_projected.sym = clipped[n].sym
                    tri_projected.col = clipped[n].col

                    # Normilize
                    tri_projected.vec_1 = vectors.divide(tri_projected.vec_1, tri_projected.vec_1.w)
                    tri_projected.vec_2 = vectors.divide(tri_projected.vec_2, tri_projected.vec_2.w)
                    tri_projected.vec_3 = vectors.divide(tri_projected.vec_3, tri_projected.vec_3.w)

                    # X/Y are inverted so put them back
                    tri_projected.vec_1.x *= -1
                    tri_projected.vec_2.x *= -1
                    tri_projected.vec_3.x *= -1
                    tri_projected.vec_1.y *= -1
                    tri_projected.vec_2.y *= -1
                    tri_projected.vec_3.y *= -1

                    # Scale into view
                    vOffsetView = vectors.Vector(1, 1, 0)
                    tri_projected.vec_1 = vectors.add(tri_projected.vec_1, vOffsetView)
                    tri_projected.vec_2 = vectors.add(tri_projected.vec_2, vOffsetView)
                    tri_projected.vec_3 = vectors.add(tri_projected.vec_3, vOffsetView)
                    tri_projected.vec_1.x *= 0.5 * SCREEN_WIDTH
                    tri_projected.vec_1.y *= 0.5 * SCREEN_HEIGHT
                    tri_projected.vec_2.x *= 0.5 * SCREEN_WIDTH
                    tri_projected.vec_2.y *= 0.5 * SCREEN_HEIGHT
                    tri_projected.vec_3.x *= 0.5 * SCREEN_WIDTH
                    tri_projected.vec_3.y *= 0.5 * SCREEN_HEIGHT

                    # Copy values into new triangle
                    new_tri = meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())
                    new_tri.vec_1 = tri_projected.vec_1
                    new_tri.vec_2 = tri_projected.vec_2
                    new_tri.vec_3 = tri_projected.vec_3
                    new_tri.sym = tri_projected.sym
                    new_tri.col = tri_projected.col
                    vec_triangles_to_raster.append(new_tri)

        # Sort triangles from back to front "painters algorithm"
        vec_triangles_to_raster.sort(key=lambda tri:
                                    (tri.vec_1.z + tri.vec_2.z + tri.vec_3.z) / 3, reverse=True)

        for tri_to_rastor in vec_triangles_to_raster:

            # Clip triangles against all four screen edges
            clipped = [meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector()),
                       meshes.Triangle(vectors.Vector(), vectors.Vector(), vectors.Vector())]

            # Queue clipped triangles
            triangles_queue = []

            # Add initial triangle
            triangles_queue.append(tri_to_rastor)
            new_triangles = 1

            for p in range(0, 4):

                tris_to_add = 0

                while new_triangles > 0:

                    # Take triangle from front of queue
                    test = triangles_queue.pop(0)
                    new_triangles -= 1

                    # Clip against a plane
                    if p == 0:	
                        tris_to_add = triangle_clip(vectors.Vector(0, 0, 0),
                                                    vectors.Vector(0, 1, 0), test, clipped)
                    elif p == 1:
                        tris_to_add = triangle_clip(vectors.Vector(0, SCREEN_HEIGHT - 1, 0),
                                                    vectors.Vector(0, -1, 0), test, clipped)
                    elif p == 2:
                        tris_to_add = triangle_clip(vectors.Vector(0, 0, 0),
                                                    vectors.Vector(1, 0, 0), test, clipped)
                    elif p == 3:
                        tris_to_add = triangle_clip(vectors.Vector(SCREEN_WIDTH - 1, 0, 0),
                                                    vectors.Vector(-1, 0, 0), test, clipped)

                    # Add new triangles into queue
                    for w in range(0, tris_to_add):

                        # Copy values into new triangle
                        new_tri = meshes.Triangle(vectors.Vector(), vectors.Vector(),
                                                  vectors.Vector())
                        new_tri.vec_1 = clipped[w].vec_1
                        new_tri.vec_2 = clipped[w].vec_2
                        new_tri.vec_3 = clipped[w].vec_3
                        new_tri.sym = clipped[w].sym
                        new_tri.col = clipped[w].col
                        triangles_queue.append(new_tri)

                new_triangles = len(triangles_queue)


            # Draw the transformed, viewed, clipped, projected, sorted, clipped triangles
            for t in triangles_queue:

                # Fill in triangles to cmd engine screen
                cmd_engine.fill_triangle(int(t.vec_1.x), int(t.vec_1.y),
                                        int(t.vec_2.x), int(t.vec_2.y),
                                        int(t.vec_3.x), int(t.vec_3.y),
                                        t.sym, t.col)

                # # Draw wireframe lines to cmd engine screen
                # cmd_engine.draw_triangle(int(t.vec_1.x), int(t.vec_1.y),
                #                         int(t.vec_2.x), int(t.vec_2.y),
                #                         int(t.vec_3.x), int(t.vec_3.y),
                #                         PIXEL_SOLID, [FG_BLACK, BG_BLACK])

        # Render current screen to command
        cmd_engine.display_screen()
