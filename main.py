from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait, StopWatch, multitask, run_task
from pybricks.iodevices import PUPDevice
# from PUPRemote.pupremote import PUPRemoteHub REMOVED FROM CHAMPIONSHIP VERSION

SIDEWAYS = [Motor(Port.C), Motor(Port.E)]
FORWARDS = [Motor(Port.B), Motor(Port.D)] # RIP PORT D # PORT D RETURNS BABEYYYYYYYYYY
COLOUR_SENSOR = ColorSensor(Port.F)
DISC_SENSOR = PUPDevice(Port.A)
# CAMERA = PUPRemoteHub(Port.A)
HUB = PrimeHub()

"""take a guess."""
SPEED = 500

CAMERA_CHANNEL_FORMAT:str = 'hh'#Angle, Distance
"""The transfer format for communication via pupremote with the camera. hh means two half-integers, 
corresponding to the angle in degrees, and the distance from the centre."""
CAMERA_BALL_COMMAND = 'ball_position'
"""The name of the function on the other end of pupremote that returns the ball's position."""
CAMERA_ENEMY_GOAL_COMMAND = 'enemy_goal'
"""The name of the function on the other end of pupremote that returns the enemy team's goal position."""
CAMERA_SELF_GOAL_COMMAND = 'self_goal'
"""The name of the function on the other end of pupremote that returns the home team's goal position."""
ROTATION_SPEED = 2000
"""A constant to be used for calibration purposes determining the speed at which the robot rotates."""
DISTANCE_THRESHOLD = 70
"""PROBABLY DEPRECATED LOL: a value to compare the disc sensor's ``strength`` value against. 
Used to test whether or not the ball is close enough, but not really useful because strength is ridiculously 
inconsistent and honestly just evil tbh this is why we need THE FUCKING 
CAMERAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
π = 3
"""A surprise tool that's gonna help us later 😉"""

# REMOVED FROM CHAMPIONSHIP EDITION
# CAMERA.add_command('gelb', to_hub_fmt = CAMERA_CHANNEL_FORMAT)
# CAMERA.add_command('cyan', to_hub_fmt = CAMERA_CHANNEL_FORMAT)


async def read_disc_angle() -> int:
    """Reads the infrared disc sensor's angle and writes it to the shared file."""
    # while True:
    #     with open("disc_val_shared.dat", "w") as f:
    #         f.write(DISC_SENSOR.read(5)[1])
    val = await DISC_SENSOR.read(5)
    return val[1]

async def get_disc_angle() -> int:
    """Returns the infrared disc sensor's angle, taken from the shared file."""
    with open("disc_val_shared.dat", "r") as f:
        return int(f.read())


#  REMOVED FROM CHAMPIONSHIP VERSION
# def get_ball_position() -> tuple[float, float]:
#     """Returns the position of the ball as a tuple of its angle and distance from the player."""
#
#     return_value:tuple[float, float] = CAMERA.call(CAMERA_BALL_COMMAND)
#
#     (angle, distance) = return_value
#
#     return angle, distance

#  REMOVED FROM CHAMPIONSHIP VERSION
# def get_own_goal_position() -> tuple[float, float]:
#     """Returns the position of the home goal as a tuple of its angle and distance from the player."""
#
#     return_value:tuple[float, float] = CAMERA.call(CAMERA_SELF_GOAL_COMMAND)
#
#     (angle, distance) = return_value
#
#     return angle, distance

# REMOVED FROM CHAMPIONSHIP VERSION
# def get_enemy_goal_position() -> tuple[float, float]:
#     """Returns the position of the opponent's goal as a tuple of its angle and distance from the player."""
#
#     return_value:tuple[float, float] = CAMERA.call(CAMERA_ENEMY_GOAL_COMMAND)
#
#     (angle, distance) = return_value
#
#     return angle, distance

async def read_disc_distance() -> int:
    return DISC_SENSOR.read(5)[0]

async def angle_to_movement_pair(angle: int) -> tuple[float, float]:
    """Converts the angle of the ball to the vector taken by ``move_vec()``. Currently a table of values due to the 30 degree increments of the disc sensor making it faster to hard code than to do sin/cos calculations on the fly lol ;-; \n
    TODO: UPDATE THIS FOR THE CAMERA"""
    horizontal_values = [0, 0.5, 0.86, 1.0, 0.86, 0.5, 0, -0.5, -0.86, -1.0, -0.86, -0.5, -0]
    horizontal_speed = horizontal_values[int(angle)]
    vertical_values = [0, 0.86,0.5,0.6,-0.5,-0.86,-1.0,-0.86,-0.5,-0.18,0.5,0.86,1.0]
    vertical_speed = vertical_values[int(angle)]
    # horizontal_speed = sin(angle*π/180)
    # vertical_speed = cos(angle*π/180)
    return horizontal_speed, vertical_speed
async def run_motor_wrapper(motor:Motor, val:int):
    motor.run(val)
async def move_vec(vec:tuple[float, float], rotation:int):
    """Moves the robot according to a vector ``vec`` corresponding to sides A & B of a right-angled triangle, while spinning the robot at a speed defined by ``rotation``."""
    await multitask(
        run_motor_wrapper(SIDEWAYS[0], int( SPEED * -vec[0] ) + rotation ),
        run_motor_wrapper(SIDEWAYS[1], int( SPEED *  vec[0] ) + rotation ),
        run_motor_wrapper(FORWARDS[0], int( SPEED * -vec[1] ) + rotation ),
        run_motor_wrapper(FORWARDS[1], int( SPEED *  vec[1] ) + rotation ) #RIP PORT D #WOOOOOOOOO PORT D BABEYYYYYYYYYYYYYYYYY
    )


async def main():
    time_elapsed = StopWatch()
    """It's ``main()``. What do you think it does?"""
    # log_speed(HUB.light.on,Color.GREEN)
    print("cooking")
    cycles = 0
    movement_vector0 = 0 
    """The movement vector we will be comparing to to make sure we aren't updating vector for no reason"""
    while True:
        # cycles += 1
        # colour = cycles % 2
        # HUB.light.on([Color.BLACK, Color.RED][colour])
        direction = await read_disc_angle()
        """The ball's angle, as a value 1-12 corresponding to a clock position."""
        # distance = read_disc_distance()
        """The ball's distance from the robot (in theory; it's basically useless but i'm keeping it here for now in case I find something to do with it."""
        # print("Direction: ", direction, "\tDistance: ", distance)
        yaw = HUB.imu.heading()
        """The robot's yaw, when compared to its rotation at initiation."""
        movement_vector = await angle_to_movement_pair(direction)
        """omfg why are you looking at this just read what ``angle_to_movement_pair()`` does you FOOL, you MORON."""
        rotation_intensity = (12-direction) if direction > 6 else -direction
        """A very clever little number that makes sure we're rotating the fastest when we're farthest away from the target rotation, and makes sure we rotate the fastest way to get there."""
        # print("rotation intensity:",rotation_intensity, "\tclock angle:", rotation_intensity)
        # rotation_value = (yaw) if (distance < DISTANCE_THRESHOLD) else ( ( rotation_intensity * ROTATION_SPEED) )
        rotation_value = yaw
        """The actual value we're going to just into ``move_vec()`` in order to rotate it. TODO: make it independent of distance because distance is stupid. Maybe check if the ball is directly ahead of us and then if so start turning back to the goal? maybe overcompensate a little bit and hope we get it right? idk seems like a decent strategy hope you get around to it future maddie baiiiiii love u <333"""

######################### QUARANTINED —— EVIL BAD CODE !! DON'T TRUST DISTANCE, IT WILL COME FOR YOU #############################
        # if distance > DISTANCE_THRESHOLD: # For some reason distance increases the closer you get to the robot. I might make a wrapper to fix that at some point but for now it can be.
        #     print("turning to goal")
        # else:
        #     print(f"Focusing on the ball - it's {distance} units away")
###################################################################################################################################
        refl = await COLOUR_SENSOR.reflection()
        """The reflectivity detected by the colour sensor tucked into the base. We use this to check for shiny tape I.E the boundaries."""
        if  refl > 40:
            print("REFLECTIVITY CRITICAL: ", refl)
            correction_vector = (-movement_vector[0], -movement_vector[1])
            #GoingBackwards = True
            """The opposite of our current movement. It's not pretty, but if the ball's out of bounds it keeps us in stasis long enough that the ref should replace it and save us."""
            await move_vec(correction_vector, rotation_value)  # do I need to explain?
            movement_vector0 = (0,0)
            wait(1000) # hold us in stasis for a bit so the ref has time to bring the ball back in bounds.
            continue
        """Ensuring movement vector doesn't update when it doesn't have to"""
        if movement_vector0 != movement_vector:
            await move_vec(movement_vector, rotation_value)  # You know the dealio
        movement_vector0 = movement_vector
async def run():
    await main()

        print(time_elapsed.time())
        time_elapsed.reset()
if __name__ == '__main__':
    # with open("disc_val_shared.dat", "w") as f: f.write("test")
    # with open("disc_val_shared.dat", "r") as f: print(f.read())
    print("made the file")
    print('running')
    run_task(run())
    print('ran')
# main() #Hey fun fact! __name__ is always gonna be fucken __main__ and it would be really stupid and embarrassing to NOT KNOW THAT and accidentally LEAVE IN CODE THAT CHECKS FOR IT ANYWAYS RIGHT GUYS?? THAT WOULD BE SUPER WEIRD, HUH???!?!
# I retract my aggressive comment; there is a reason to do it now 💔
# import random