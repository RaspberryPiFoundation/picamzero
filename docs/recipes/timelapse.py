from picamzero import Camera

cam = Camera()
cam.start_preview()
cam.capture_sequence(filename="sequence.jpg", num_images=5, interval=1)
