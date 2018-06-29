import cozmo
import random
from cozmo.util import distance_mm, degrees


# Expand for full code!
def cozmo_program(robot: cozmo.robot.Robot):
    state = "findcube1"
    cubefound = robot.world.get_light_cube(3)
    while True:
        if state == "findcube1" and cubefound.cube_id != cozmo.objects.LightCubeIDs[0]:
            robot.drive_wheels(40, 10)
            cubefound = robot.world.wait_for_observed_light_cube()
        elif state == "findcube1" and cubefound.cube_id == cozmo.objects.LightCubeIDs[0]:
            state = "gotocube1"
            robot.stop_all_motors()
        elif state == "gotocube1":
            skip_check = random.randrange(1, 3)
            if skip_check == 1:
                state = "findcube2"
            else:
                state = "findcube3"
            robot.go_to_object(cubefound, distance_mm(80)).wait_for_completed()
            robot.set_head_angle(degrees(0))

        elif state == "findcube2" and cubefound.cube_id != cozmo.objects.LightCubeIDs[1]:
            robot.drive_wheels(40, 10)
            cubefound = robot.world.wait_for_observed_light_cube()
        elif state == "findcube2" and cubefound.cube_id == cozmo.objects.LightCubeIDs[1]:
            state = "gotocube2"
            robot.stop_all_motors()
        elif state == "gotocube2":
            state = "findcube3"
            robot.go_to_object(cubefound, distance_mm(80)).wait_for_completed()
            robot.set_head_angle(degrees(0))

        elif state == "findcube3" and cubefound.cube_id != cozmo.objects.LightCubeIDs[2]:
            robot.drive_wheels(40, 10)
            cubefound = robot.world.wait_for_observed_light_cube()
        elif state == "findcube3" and cubefound.cube_id == cozmo.objects.LightCubeIDs[2]:
            state = "gotocube3"
            robot.stop_all_motors()
        elif state == "gotocube3":
            state = "findcube1"
            robot.go_to_object(cubefound, distance_mm(80)).wait_for_completed()
            robot.set_head_angle(degrees(0))


cozmo.run_program(cozmo_program)

