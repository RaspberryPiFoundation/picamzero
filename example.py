from picamzero import Camera
from time import sleep

cam = Camera()

cam.preview.annotation = "Hello"
print(cam.preview.annotation)

cam.preview.start()

sleep(2)
cam.preview.stop()

"""
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
"""