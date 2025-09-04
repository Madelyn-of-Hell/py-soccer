# yellowDetection - By: lilith - Thu Aug 21 2025

# standard imports
import sensor
import time


# connect to spike
# from pupremote import PUPRemoteSensor, OPENMV
# p = PUPRemoteSensor(power=True)
# p.add_channel('yelow', to_hub_fmt='hhh')





sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=0)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

yellow_threshold = (45, 70, 0, 35, 40, 70)


def yellow_detection()->list:
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([yellow_threshold], pixels_threshold=125, area_threshold=125)
    largest_blob = None
    yellow_list = []
    for blob in blobs:
        largest_blob = blob
        img.draw_rectangle(largest_blob.rect(), color=(255, 255, 255))
        img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=(255, 255, 255))
        yellow_list.append((largest_blob.cx(), largest_blob.cy()))
    return yellow_list


while True:
    yellow_goal = yellow_detection()
    # print("blobs:", yellow_goal)
    # p.update_channel('yellow', yellow_goal)
