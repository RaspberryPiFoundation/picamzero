from picamzero import Camera
from time import sleep

cam = Camera()

cam.preview.start()


cam.preview.annotation = "Hello"
print(cam.preview.annotation)

sleep(2)
cam.preview.stop()
