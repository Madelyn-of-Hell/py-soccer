# cyanDetection - By: lilith - Thu Aug 21 2025

# standard imports
import sensor
import time


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


def cyan_detection() -> list:
    """Define funtion."""
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([cyan_threshold], pixels_threshold=200, area_threshold=200)
    largest_blob = None
    pixels = x = y = 0
    # cyan_list = []
    for blob in blobs:
        if blob.pixels() > pixels:
            largest_blob = blob
            pixels = blob.pixels()
    if pixels > 0:
        img.draw_rectangle(largest_blob.rect(), color=(255, 255, 255))
        x = largest_blob.cx()
        y = largest_blob.cy()
        img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=(255, 255, 255))
        #cyan_list.append((largest_blob.cx(), largest_blob.cy()))
    #return cyan_list
    p.update_channel('cyan', x, y)
    print("blobs:", x, y,)

while True:
    cyan_detection()


