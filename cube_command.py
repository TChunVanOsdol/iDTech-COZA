import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time


def rotate_lights(cube: cozmo.objects.LightCube, side):
    # Set the lights of the target cube to turn on only one side
    off = cozmo.lights.off_light
    if cube.cube_id == 1:
        color = cozmo.lights.red_light
    elif cube.cube_id == 2:
        color = cozmo.lights.green_light
    elif cube.cube_id == 3:
        color = cozmo.lights.blue_light
    lights = [off, off, off, off]
    lights[side] = color
    cube.set_light_corners(lights[0], lights[1], lights[2], lights[3])


def cube_com(robot: cozmo.robot.Robot):
    # Initialize light cubes
    cube = [None, None, None]
    cube[0] = robot.world.get_light_cube(LightCube1Id) # FWD cube
    cube[1] = robot.world.get_light_cube(LightCube2Id) # LEFT cube
    cube[2] = robot.world.get_light_cube(LightCube3Id) # RIGHT cube
    if cube[0] is not None:
        cube[0].set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")

    if cube[1] is not None:
        cube[1].set_lights(cozmo.lights.green_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube2Id cube - check the battery.")

    if cube[2] is not None:
        cube[2].set_lights(cozmo.lights.blue_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube3Id cube - check the battery.")
    # Robot setup
    timer = 0
    timestep = 0.01
    cube_side = 0 # Ranges 0-3 for cube lights
    state = "FWD" # State variable
    last_com = "FWD" # Event handler to update next state
    last_com_time = 0 # Last event received
    tap_tracker = [0, 0, 0] # Last time cube was tapped
    tap_com = ["FWD", "LEFT", "RIGHT"] # List of states
    # Robot loop
    while True:
        # Update cube tap times
        for n in range(3):
            if cube[n].last_tapped_time is not None:
                tap_tracker[n] = cube[n].last_tapped_time
        # Find most recent cube tap
        last_tap = max(tap_tracker)
        if last_tap > last_com_time:
            last_com_time = last_tap
            last_com = tap_com[tap_tracker.index(last_tap)]
        # State Machine
        timer += timestep
        if timer >= 0.25:
            timer = 0
            cube_side = (cube_side + 1) % 4
        # Forward State
        if state == "FWD" and last_com == "LEFT":
            state = "LEFT"
            cube[0].set_lights(cozmo.lights.red_light)
        elif state == "FWD" and last_com == "RIGHT":
            state = "RIGHT"
            cube[0].set_lights(cozmo.lights.red_light)
        elif state == "FWD":
            robot.drive_wheel_motors(50, 50, 200, 200)
            rotate_lights(cube[0], cube_side)
        # Left State
        elif state == "LEFT" and last_com == "FWD":
            state = "FWD"
            cube[1].set_lights(cozmo.lights.green_light)
        elif state == "LEFT" and last_com == "RIGHT":
            state = "RIGHT"
            cube[1].set_lights(cozmo.lights.green_light)
        elif state == "LEFT":
            robot.drive_wheel_motors(-50, 50, 200, 200)
            rotate_lights(cube[1], cube_side)
        # Right State
        elif state == "RIGHT" and last_com == "FWD":
            state = "FWD"
            cube[2].set_lights(cozmo.lights.blue_light)
        elif state == "RIGHT" and last_com == "LEFT":
            state = "LEFT"
            cube[2].set_lights(cozmo.lights.blue_light)
        elif state == "RIGHT":
            robot.drive_wheel_motors(50, -50, 200, 200)
            rotate_lights(cube[2], cube_side)

        time.sleep(timestep)


cozmo.run_program(cube_com)
