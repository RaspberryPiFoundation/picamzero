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
from datetime import datetime
import pytest

# ============================================================
# WARNING - this script will take pictures with your picamera
# It should remove them again but you may want to check the
# /tests folder after running just in case, before committing
# to GitHub! :D
# ============================================================

@pytest.fixture(autouse=True)
def cwd(tmpdir, monkeypatch):
    """
    This fixture changes the current working directory before
    each test in this file to to a temporary directory so that
    image / video clean up is taken care of by the OS.
    """
    monkeypatch.chdir(tmpdir)


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
	
# Record a video with a specific filename
def test_named_video_no_extension(cam):
	cam.record_video("testvid", 3)
	assert exists("testvid.mp4")

# Record a video with no specified filename
def test_unnamed_video(cam):
	filename = cam.record_video()
	assert exists(filename)

# Record a video with a filename but no extension
@pytest.mark.skip(reason="TODO")
def test_unnamed_video(cam):
	pass

# Take a picture with a specific filename
def test_named_picture(cam):
	cam.take_photo("testpic.jpg")
	cam.capture_image("testpic2.jpg")
	assert exists("testpic.jpg")
	assert exists("testpic2.jpg")
	
# Take a pic with no specified filename
def test_unnamed_picture(cam):
	filename = cam.take_photo()
	filename2 = cam.capture_image()
	assert exists(filename)
	assert exists(filename2)

# Take a pic with a filename but no extension
def test_named_picture_no_ext(cam):
	filename = cam.take_photo("test")
	filename2 = cam.capture_image("test2")
	assert exists("test.jpg")
	assert exists("test2.jpg")
	
# Test a burst capture of 10 images at 0.01 sec interval
def test_unnamed_burst(cam):
	cam.capture_burst() 
	assert exists("burst-0.jpg")
	assert exists("burst-9.jpg")
	
# Test a burst capture with a filename but no extension
def test_named_burst_no_extension(cam):
	cam.capture_burst("test") 
	assert exists("test-0.jpg")
	assert exists("test-9.jpg")

# Can you take a video and stills	
def test_video_with_stills(cam):
	cam.take_video_and_still(filename="abc", duration=12, still_interval=2)
	assert exists("abc.mp4")
	assert exists("abc-0.jpg")
	assert exists("abc-5.jpg")
	assert not exists("abc-6.jpg")
	
	cam.take_video_and_still() # no args
	assert exists("testvs.mp4")
	assert exists("testvs-0.jpg")
	assert exists("testvs-4.jpg")
	assert not exists("testvs-5.jpg")
	
# Test a named burst capture with extension	
def test_named_burst(cam):
	cam.capture_burst("testing.jpg") 
	assert exists("testing-0.jpg")
	assert exists("testing-9.jpg")

# Test whether you can change the number of pics
def test_burst_quantity(cam):
	cam.capture_burst(filename="fewer", num_images=2)
	assert exists("fewer-0.jpg")
	assert exists("fewer-1.jpg")
	assert not exists("fewer-2.jpg")

# Test the burst interval
def test_burst_interval(cam):
	start = datetime.now()
	cam.capture_burst(filename="longer", interval=1, num_images=3)
	stop = datetime.now()
	elapsed = stop - start
	start2 = datetime.now()
	# This one should be faster
	cam.capture_burst(filename="shorter", interval=0.5, num_images=3)
	stop2 = datetime.now()
	elapsed2 = stop2 - start2
	assert elapsed > elapsed2
	
# Test the video gets made when you do a burst
def test_burst_with_video(cam):
	cam.capture_burst(filename="with-vid", make_video=True)
	assert exists("with-vid-timelapse.mp4")

# Test burst synonym methods
def test_burst_synonyms(cam):
	start_seq = datetime.now()
	cam.take_sequence(filename="seq", num_images=4, interval=0.5, make_video=True)
	stop_seq = datetime.now()
	seq_total = stop_seq - start_seq
	assert exists("seq-0.jpg")
	assert exists("seq-3.jpg")
	assert not exists("seq-4.jpg")
	assert exists("seq-timelapse.mp4")
	
	start_cap = datetime.now()
	cam.capture_sequence(filename="cap", num_images=8, interval=1, make_video=True)
	stop_cap = datetime.now()
	cap_total = stop_cap - start_cap
	assert exists("cap-0.jpg")
	assert exists("cap-7.jpg")
	assert not exists("cap-8.jpg")
	assert exists("cap-timelapse.mp4")
	assert cap_total > seq_total

# Test that you can video and take stills
@pytest.mark.skip(reason="TODO")
def test_video_with_stills(cam):
	# Finish this when method updated 
	# - need to take out strftime from filename
	#cam.take_video_and_still(filename="abc", duration=12, still_interval=3)
	#assert exists("abc.mp4")
	pass
	
	

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



