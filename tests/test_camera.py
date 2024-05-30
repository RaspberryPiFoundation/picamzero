from picamzero import Camera

def test_init():
	camera = Camera()
	assert camera.picamera2 is not None
