from picamzero import Camera

cam = Camera()
cam.start_preview()
cam.record_video("test.mp4", duration=5)
