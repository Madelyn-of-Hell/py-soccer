from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
import main
# SIDEWAYS = [Motor(Port.C), Motor(Port.E)]
# FORWARDS = [Motor(Port.B), Motor(Port.D)] # RIP PORT D # PORT D RETURNS BABEYYYYYYYYYY
# COLOUR_SENSOR = ColorSensor(Port.F)
# DISC_SENSOR = PUPDevice(Port.A)
HUB = main.HUB
# CAMERA_CHANNEL_FORMAT:str = 'repr'
# CAMERA_BALL_COMMAND = 'ball_position'
# CAMERA_ENEMY_GOAL_COMMAND = 'enemy_goal'
# CAMERA_SELF_GOAL_COMMAND = 'self_goal'
# ROTATION_SPEED = 150
# DISTANCE_THRESHOLD = 70
# π = 3

def get_raw_disc_data() -> list:
    return main.DISC_SENSOR.read(5)

def log_speed(name:str, code_snippet, *params) -> int:
    timer = StopWatch()
    for i in range(100):
        code_snippet(*params)
    time_taken = timer.time()
    print(f"TIME TAKEN TO RUN {name}: {time_taken*10}µs")
    return time_taken

print("Running on "+HUB.system.info()['name'])
battery_status:str = min(zip(["Maximum", "Ok", "Low", "Critical"],[8300, 7200, 6800, 6000]), key=lambda x: abs(x[1]-HUB.battery.voltage()))[0]
print(f"Battery level is {battery_status} ({HUB.battery.voltage()}mV)")
wait(1000)
time_elapsed = StopWatch()
while True:
    print(f"TIME TAKEN TO CYCLE LOOP: {time_elapsed.time()*1000}µs")
    print("Ground Reflectivity:", main.COLOUR_SENSOR.reflection())
    time_rdl = log_speed("read_disc_angle", main.get_disc_angle)
    time_atm = log_speed("angle_to_movement_pair", main.angle_to_movement_pair, 1)
    time_mv = log_speed("move_vec", main.move_vec, main.angle_to_movement_pair(1), 0)
    time_elapsed.reset()
    # print("data:",get_raw_disc_data())
