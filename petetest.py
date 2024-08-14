from picamzero import Camera, utilities

from time import sleep
import os
from pprint import *

os.chdir("test_output")

cam=Camera()

cam.take_photo("start test")

# cam.preview_size(1024, 780)
cam.start_preview()
cam.annotate("Pete is awesome", scale=7, font="triplex")
# # cam.take_photo("anntest")
# sleep(5)
# cam.stop_preview()
# print(cam._text_properties)
# print('pppppp')
# print(utilities.font_dict()["simplex"][0])





# pprint(cam.pc2.sensor_modes)
# print(picam2.sensor_resolution)
# sensor_mode = cam.sensor_mode
# print(f"Current sensor mode: {sensor_mode}")
# pprint(cam.get_res())
# pprint(cam.get_sensor())
# cam.flip_camera(vflip=True)
# cam.record_video("vid", 10)
# cam.take_video_and_still("vidstill5", duration=9, still_interval=2)
# cam.record_video("vid", 10)
# cam.start_preview()
# sleep(2)
# cam.take_photo("flipped2")
# cam.start_preview()
# sleep(2)
# cam.capture_sequence("flip_seq")
# cam.start_preview()
# cam.take_photo("flipped2")