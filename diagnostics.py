from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait
from pybricks.iodevices import PUPDevice
from PUPRemote.pupremote import PUPRemoteHub

SIDEWAYS = [Motor(Port.C), Motor(Port.E)]
FORWARDS = [Motor(Port.B), Motor(Port.D)] # RIP PORT D # PORT D RETURNS BABEYYYYYYYYYY
COLOUR_SENSOR = ColorSensor(Port.F)
DISC_SENSOR = PUPDevice(Port.A)
CAMERA = PUPRemoteHub(Port.A)
HUB = PrimeHub()

CAMERA_CHANNEL_FORMAT:str = 'repr'
CAMERA_BALL_COMMAND = 'ball_position'
CAMERA_ENEMY_GOAL_COMMAND = 'enemy_goal'
CAMERA_SELF_GOAL_COMMAND = 'self_goal'
ROTATION_SPEED = 150
DISTANCE_THRESHOLD = 70
π = 3

def get_raw_disc_data() -> list:
    return DISC_SENSOR.read(5)

print("Running on "+HUB.system.info()['name'])
wait(1000)

while True:
    print("data:",get_raw_disc_data())
