# -------------------------------------------------------------
# This is not production code but I am losing the will to live
# Provide the path to the module so that the tests can run
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------------------------------------------

from picamzero import Camera
from os.path import exists
from time import sleep
import pytest

# ============================================================
# WARNING - this script will take pictures with your picamera
# It should remove them again but you may want to check the
# /tests folder after running just in case, before committing
# to GitHub! :D
# ============================================================


# Returns a camera to use in tests
@pytest.fixture
def cam():
	camera = Camera()
	yield camera
	camera.pc2.close()

# ----------------------------------
# Camera.py tests
# ----------------------------------

# Initialise a camera
def test_init(cam):
	assert cam.pc2 is not None
	
# Record a video with a specific filename
def test_named_video(cam):
	cam.record_video("testvideo.mp4", 3)
	assert exists("testvideo.mp4")
	os.remove("testvideo.mp4") # Delete the file

# Record a video with no specified filename
def test_unnamed_video(cam):
	filename = cam.record_video()
	assert exists(filename)
	os.remove(filename)

# Record a video with a filename but no extension
def test_unnamed_video(cam):
	assert True # To do!


# Take a picture with a specific filename
def test_named_picture(cam):
	cam.take_photo("testpic.jpg")
	cam.capture_image("testpic2.jpg")
	assert exists("testpic.jpg")
	assert exists("testpic2.jpg")
	os.remove("testpic.jpg") # Delete the file
	os.remove("testpic2.jpg")
	
# Take a pic with no specified filename
def test_unnamed_picture(cam):
	filename = cam.take_photo()
	filename2 = cam.capture_image()
	assert exists(filename)
	assert exists(filename2)
	os.remove(filename)
	os.remove(filename2)

# Take a pic with a filename but no extension
def test_named_picture_no_ext(cam):
	filename = cam.take_photo("test")
	filename2 = cam.capture_image("test2")
	assert exists("test.jpg")
	assert exists("test2.jpg")
	os.remove(filename)
	os.remove(filename2)
	
# Test a burst capture of 10 images at 0.01 sec interval
def test_unnamed_burst(cam):
	cam.capture_burst() # 10 images default
	assert exists("burst-0.jpg")
	assert exists("burst-9.jpg")
	# Clean up
	for i in range(10):
		os.remove(f"burst-{i}.jpg")
	
# Test a burst capture with a filename but no extension
def test_named_burst_no_extension(cam):
	cam.capture_burst("test") # 10 images default
	assert exists("test-0.jpg")
	assert exists("test-9.jpg")
	#Clean up
	for i in range(10):
		os.remove(f"test-{i}.jpg")
		
#def test_named_burst(cam):
	
#def test_burst_with_video(cam):

# ----------------------------------
# Preview.py tests
# ----------------------------------

# Does the preview exist?
def test_preview_exists(cam):
	assert cam.preview is not None
	assert cam.preview.pc2 is not None

# Can you start and stop the preview
def test_preview_starts_and_stops(cam):
	cam.preview.start()
	assert cam.preview._started == True
	cam.preview.stop()
	assert cam.preview._started == False

# Can you add an annotation
def test_annotation(cam):
	cam.preview.start()
	cam.preview.annotation = "test"
	assert cam.preview.annotation == "test" # property
	assert cam.preview._annotation == "test" # attribute


