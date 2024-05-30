# -------------------------------------------------------------
# This is not production code but I am losing the will to live
# Provide the path to the module so that the tests can run
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------------------------------------------

from picamzero import Camera
from os.path import exists

# ============================================================
# WARNING - this script will take pictures with your picamera
# It should remove them again but you may want to check the
# /tests folder after running just in case, before committing
# to GitHub! :D
# ============================================================


# Set up camera 
camera = Camera()

def test_init():
	assert camera.pc2 is not None

def test_named_video():
	# Record a video with a specific filename
	camera.record_video("testvideo.mp4", 3)
	assert exists("testvideo.mp4")
	os.remove("testvideo.mp4") # Delete the file

def test_unnamed_video():
	# Record a video with no specified filename
	filename = camera.record_video()
	assert exists(filename)
	os.remove(filename)

# I don't know why but if you put the tests for the picture
# _before_ the video tests, the video tests fail. If they are 
# after, they pass. Weird.

def test_named_picture():
	# Take a picture with a specific filename
	camera.take_picture("testpic.jpg")
	assert exists("testpic.jpg")
	os.remove("testpic.jpg") # Delete the file
	
def test_unnamed_picture():
	# Take a pic with no specified filename
	filename = camera.take_picture()
	assert exists(filename)
	os.remove(filename)


