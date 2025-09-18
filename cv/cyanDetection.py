# cyanDetection - By: lilith - Thu Aug 21 2025

# standard imports
import sensor
import time
from math import atan2, sqrt, pi

# connect to spike
from pupremote import PUPRemoteSensor
p = PUPRemoteSensor(power=True)
p.add_channel('cyan', to_hub_fmt='hhh')


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=0)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

cyan_threshold = (25, 75, -40, -15, -27, 15)

def white_australia_policy(x:int, y:int):
    # img = sensor.snapshot()
    centre = (160, 120)
    # img.draw_cross(centre)
    (x, y) = (x - centre[0], y - centre[1])
    movement_angle = 180 * atan2(y, x)/pi
    distance = sqrt(x*x + y*y)
    return ((movement_angle + 270)%360, distance)

def cyan_detection() -> list:
    """Define funtion."""
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([cyan_threshold], pixels_threshold=10, area_threshold=10)
    largest_blob = None
    pixels = x = y = 0
    # cyan_list = []
    for blob in blobs:
        if blob.pixels() > pixels:
            largest_blob = blob
            pixels = blob.pixels()
        img.draw_rectangle(blob.rect(), color=(255, 255, 255))
    if pixels > 0:
        img.draw_rectangle(largest_blob.rect(), color=(0, 255, 0))
        x = largest_blob.cx()
        y = largest_blob.cy()
        img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=(255, 255, 255))
        #cyan_list.append((largest_blob.cx(), largest_blob.cy()))
    #return cyan_list
    return (x, y)
    print("blobs:", x, y,)

while True:
    values = cyan_detection()
    wap = white_australia_policy(values[0], values[1])
    p.update_channel('cyan', int(wap[0]), int(wap[1]))
    print(wap)




