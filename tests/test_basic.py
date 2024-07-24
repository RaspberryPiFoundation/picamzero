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

# Take a picture with a specific filename
def test_named_picture(cam):
	cam.take_photo("testpic.jpg")
	assert exists("testpic.jpg")
	os.remove("testpic.jpg") # Delete the file
	
# Take a pic with no specified filename
def test_unnamed_picture(cam):
	filename = cam.take_photo()
	assert exists(filename)
	os.remove(filename)

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


