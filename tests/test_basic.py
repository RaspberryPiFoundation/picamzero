from datetime import datetime
from os.path import exists

import pytest
from picamzero import Camera, PicameraZeroException

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
# Initialise camera
# ----------------------------------

# Initialise a camera
def test_init(cam: Camera):
    assert cam.pc2 is not None

# ----------------------------------
# Preview
# ----------------------------------

# Can you start and stop the preview
def test_preview_starts_and_stops(cam):
    cam.start_preview()
    assert cam._started is True
    cam.stop_preview()
    assert cam._started is False

# ----------------------------------
# Camera orientation (hflip/vflip)
# ----------------------------------



# ----------------------------------
# Video
# ----------------------------------

# Record a video with a specific filename
def test_named_video(cam: Camera):
    cam.record_video("testvideo.mp4", 3)
    assert exists("testvideo.mp4")

# Record a video with a specific filename
def test_named_video_no_extension(cam):
    cam.record_video("testvid", 3)
    assert exists("testvid.mp4")

# Fail to specify a filename for a video
def test_unnamed_video(cam):
    with pytest.raises(PicameraZeroException):
        _ = cam.record_video()

# ----------------------------------
# Image
# ----------------------------------

# Take a picture with a specific filename
def test_named_picture(cam):
    cam.take_photo("testpic.jpg")
    cam.capture_image("testpic2.jpg")
    cam.take_photo("testpic.jpeg")
    cam.capture_image("testpic2.jpeg")
    cam.take_photo("testpicpng.png")
    cam.capture_image("testpic2png.png")
    assert exists("testpic.jpg")
    assert exists("testpic2.jpg")
    assert not exists("testpic.jpeg")
    assert not exists("testpic2.jpeg")
    assert not exists("testpicpng.png")
    assert not exists("testpic2png.png")
    assert exists("testpicpng.jpg")
    assert exists("testpic2png.jpg")


# Fail to specify a filename for a picture
def test_unnamed_picture(cam):
    with pytest.raises(PicameraZeroException):
        _ = cam.take_photo()
    with pytest.raises(PicameraZeroException):
        _ = cam.capture_image()


# Take a pic with a filename but no extension
def test_named_picture_no_ext(cam):
    filename = cam.take_photo("test")
    filename2 = cam.capture_image("test2")
    assert filename == "test.jpg"
    assert filename2 == "test2.jpg"
    assert exists(filename)
    assert exists(filename2)

# ----------------------------------
# Sequence
# ----------------------------------

# Fail to specify a filename for a sequence
def test_unnamed_sequence(cam):
    with pytest.raises(PicameraZeroException):
        cam.capture_sequence()

# Test a sequence capture with a filename but no extension
def test_named_sequence_no_extension(cam):
    cam.capture_sequence("test")
    assert exists("test-0.jpg")
    assert exists("test-9.jpg")

# Test a named sequence capture with extension
def test_named_sequence(cam):
    cam.capture_sequence("testing.jpg")
    assert exists("testing-0.jpg")
    assert exists("testing-9.jpg")

# Test whether you can change the number of pics
def test_sequence_quantity(cam):
    cam.capture_sequence(filename="fewer", num_images=2)
    assert exists("fewer-0.jpg")
    assert exists("fewer-1.jpg")
    assert not exists("fewer-2.jpg")

# Test the sequence interval
def test_sequence_interval(cam):
    start = datetime.now()
    cam.capture_sequence(filename="longer", interval=1, num_images=3)
    stop = datetime.now()
    elapsed = stop - start
    start2 = datetime.now()
    # This one should be faster
    cam.capture_sequence(filename="shorter", interval=0.5, num_images=3)
    stop2 = datetime.now()
    elapsed2 = stop2 - start2
    assert elapsed > elapsed2

# Test the video gets made when you do a sequence
def test_sequence_with_video(cam):
    cam.capture_sequence(filename="with-vid", make_video=True)
    assert exists("with-vid-timelapse.mp4")
    

# ----------------------------------
# Video and still
# ----------------------------------

# Can you take a video and stills
def test_video_with_stills(cam):
    cam.take_video_and_still(filename="abc", duration=12, still_interval=2)
    assert exists("abc.mp4")
    assert exists("abc-0.jpg")
    assert exists("abc-5.jpg")
    assert not exists("abc-6.jpg")

    cam.take_video_and_still(filename="testvs")
    assert exists("testvs.mp4")
    assert exists("testvs-0.jpg")
    assert exists("testvs-4.jpg")
    assert not exists("testvs-5.jpg")
