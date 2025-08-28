from pybricks import pupdevices
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait
from pybricks.iodevices import PUPDevice


π = 3
hub = PrimeHub()
SIDEWAYS = [Motor(Port.C), Motor(Port.E)]
FORWARDS = [Motor(Port.B), Motor(Port.D)]
COLOUR_SENSOR = ColorSensor(Port.F)
DISC_SENSOR = PUPDevice(Port.A)
CLOCKHAND = 1
DISTANCE = 0

def read_disc_angle() -> int:
    return DISC_SENSOR.read(5)[1]

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
    return (horizontal_speed, vertical_speed)

def move_vec(vec:tuple[float, float]):
    SIDEWAYS[0].run(int(SPEED * -vec[0]))
    SIDEWAYS[1].run(int(SPEED * vec[0]))
    FORWARDS[0].run(int(SPEED * -vec[1]))
    FORWARDS[1].run(int(SPEED * vec[1]))

def stabilise():
    while True:
        yaw = hub.imu.heading()
        if abs(yaw) < 1:
            # print("we good")
            SIDEWAYS[0].stop()
            SIDEWAYS[1].stop()
            FORWARDS[0].stop()
            FORWARDS[1].stop()
        else:
            SIDEWAYS[0].run(-yaw * 2)
            SIDEWAYS[1].run(-yaw * 2)
            FORWARDS[0].run(-yaw * 2)
            FORWARDS[1].run(-yaw * 2)
def main():

    cycles = 0
    while True:
        # runloop.run([stabilise])
            cycles += 1
            colour = cycles % 2
            hub.light.on([Color.BLACK, Color.RED][colour])
            # print(data)
            direction = read_disc_angle()
            distance = read_disc_distance()
            # print("\n"*20)
            # print("Angle: ", direction)
            movement_vector = angle_to_movement_pair(direction)
            if COLOUR_SENSOR.reflection() > 40:
                # print("backwards")
                correction_vector = (-movement_vector[0], -movement_vector[1])
                move_vec(correction_vector)
                wait(1)
                continue
            # print("Horizontal: ", movement_vector[0])
            # print("Vertical: ", movement_vector[1])
            move_vec(movement_vector)

main()

yellow = pupdevices.add_channel('gelb', to_hub_fmt = 'hhh')
cyan = pupdevices.add_channel('cyan', to_hub_fmt = 'hhh')