from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait
from pybricks.iodevices import PUPDevice
from PUPRemote.pupremote import PUPRemoteHub

SIDEWAYS = [Motor(Port.C), Motor(Port.E)]
FORWARDS = [Motor(Port.B), Motor(Port.D)]
COLOUR_SENSOR = ColorSensor(Port.F)
DISC_SENSOR = PUPDevice(Port.A)
CAMERA = PUPRemoteHub(Port.A)

CAMERA_CHANNEL_FORMAT:str = 'repr'
CAMERA_BALL_COMMAND = 'ball_position'
CAMERA_ENEMY_GOAL_COMMAND = 'enemy_goal'
CAMERA_SELF_GOAL_COMMAND = 'self_goal'
π = 3

CAMERA.add_command(CAMERA_BALL_COMMAND, CAMERA_CHANNEL_FORMAT, CAMERA_CHANNEL_FORMAT)
hub = PrimeHub()

DISTANCE_THRESHOLD = 0
def read_disc_angle() -> int:
    return DISC_SENSOR.read(5)[1]

def get_ball_position() -> tuple[float, float]:
    """Returns the position of the ball as a tuple of its angle and distance from the player."""

    return_value:tuple[float, float] = CAMERA.call(CAMERA_BALL_COMMAND)

    (angle, distance) = return_value

    return angle, distance

def get_own_goal_position() -> tuple[float, float]:
    """Returns the position of the home goal as a tuple of its angle and distance from the player."""

    return_value:tuple[float, float] = CAMERA.call(CAMERA_SELF_GOAL_COMMAND)

    (angle, distance) = return_value

    return angle, distance

def get_enemy_goal_position() -> tuple[float, float]:
    """Returns the position of the opponent's goal as a tuple of its angle and distance from the player."""

    return_value:tuple[float, float] = CAMERA.call(CAMERA_ENEMY_GOAL_COMMAND)

    (angle, distance) = return_value

    return angle, distance

def read_disc_distance() -> int:
    return DISC_SENSOR.read(5)[0]

SPEED = 500
def angle_to_movement_pair(angle: int) -> tuple[float, float]:
    horizontal_values = [0, 0.5, 0.86, 1.0, 0.86, 0.5, 0, -0.5, -0.86, -1.0, -0.86, -0.5, -0]
    horizontal_speed = horizontal_values[int(angle)]
    vertical_values = [0, 0.86,0.5,0.6,-0.5,-0.86,-1.0,-0.86,-0.5,-0.18,0.5,0.86,1.0]
    vertical_speed = vertical_values[int(angle)]
    # horizontal_speed = sin(angle*π/180)
    # vertical_speed = cos(angle*π/180)
    return horizontal_speed, vertical_speed

def move_vec(vec:tuple[float, float], rotation:int):
    SIDEWAYS[0].run( int( SPEED * -vec[0] ) + rotation )
    SIDEWAYS[1].run( int( SPEED *  vec[0] ) + rotation )
    FORWARDS[0].run( int( SPEED * -vec[1] ) + rotation )
    FORWARDS[1].run( int( SPEED *  vec[1] ) + rotation )

def main():
    cycles = 0
    while True:
        cycles += 1
        colour = cycles % 2
        hub.light.on([Color.BLACK, Color.RED][colour])
        # print(data)
        direction = read_disc_angle()
        distance = read_disc_distance()
        yaw = hub.imu.heading()
        movement_vector = angle_to_movement_pair(direction)

        rotation_value = yaw if distance < DISTANCE_THRESHOLD else direction * 15
        """The angle to which we want to rotate the robot. If the robot possesses the ball (assessed by distance from the ball), it wants to face forward. If not, the robot wants to face the ball. Direction is multiplied by 15 so that it operates on the same scale as yaw """
        if COLOUR_SENSOR.reflection() > 40:
            # print("backwards")
            correction_vector = (-movement_vector[0], -movement_vector[1])
            move_vec(correction_vector, rotation_value)
            wait(1)
            continue
        # print("Horizontal: ", movement_vector[0])
        # print("Vertical: ", movement_vector[1])
        move_vec(movement_vector, rotation_value)

main()

CAMERA.add_channel('gelb', to_hub_fmt = 'hhh')
CAMERA.add_channel('cyan', to_hub_fmt = 'hhh')