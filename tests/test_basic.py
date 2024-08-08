from datetime import datetime
from os.path import exists

import pytest
from picamzero import Camera, PicameraZeroException


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
# Helper functions
# ----------------------------------


# Test that the filename formatter works properly
def test_filename_format(cam: Camera):
    assert cam._format_filename("blah.jpg", ".jpg") == "blah.jpg"
    assert cam._format_filename("blah", ".jpg") == "blah.jpg"
    assert cam._format_filename("blah.", ".jpg") == "blah.jpg"
    assert cam._format_filename("a", ".mp4") == "a.mp4"
    assert cam._format_filename("a.mp4", ".mp4") == "a.mp4"
    assert cam._format_filename("abc.jpg", ".mp4") == "abc.mp4"
    assert cam._format_filename("example", "") == "example"
    with pytest.raises(PicameraZeroException):
        _ = cam._format_filename(None, ".jpg")


# ----------------------------------
# Preview
# ----------------------------------


# Can you start and stop the preview
def test_preview_starts_and_stops(cam: Camera):
    cam.start_preview()
    assert cam._started_preview is True
    cam.stop_preview()
    assert cam._started_preview is False


# ----------------------------------
# Camera orientation (hflip/vflip)
# ----------------------------------


def test_cam_flip(cam: Camera):
    cam.flip_camera(hflip=True)
    assert cam.hflip is True
    assert cam.preview_config["transform"].hflip is True
    cam.flip_camera(vflip=True)
    assert cam.vflip is True
    assert cam.preview_config["transform"].vflip is True
    cam.flip_camera(hflip=False, vflip=False)
    assert cam.hflip is False
    assert cam.preview_config["transform"].hflip is False
    assert cam.vflip is False
    assert cam.preview_config["transform"].vflip is False


# ----------------------------------
# Annotation
# ----------------------------------


def test_annotation_properties(cam: Camera):
    text = "hello"
    text_color = (255, 255, 0, 255)
    text_origin = (100, 100)
    text_scale = 4
    text_thickness = 6
    cam.annotate(
        text=text,
        text_color=text_color,
        text_origin=text_origin,
        text_scale=text_scale,
        text_thickness=text_thickness,
    )
    assert cam._text == text
    assert cam._text_color == text_color
    assert cam._text_origin == text_origin
    assert cam._text_scale == text_scale
    assert cam._text_thickness == text_thickness


# ----------------------------------
# Video
# ----------------------------------


# Record a video with a specific filename
def test_named_video(cam: Camera):
    cam.record_video("testvideo.mp4", 3)
    assert exists("testvideo.mp4")


# Record a video with a specific filename
def test_named_video_no_extension(cam: Camera):
    cam.record_video("testvid", 3)
    assert exists("testvid.mp4")


# Fail to specify a filename for a video
def test_unnamed_video(cam: Camera):
    with pytest.raises(PicameraZeroException):
        _ = cam.record_video()
    with pytest.raises(PicameraZeroException):
        _ = cam.start_recording()


# Test recording an unspecified length video with start and stop
def test_video_unspecified_length(cam: Camera):
    assert len(cam.pc2.encoders) == 0
    cam.start_recording("testvideo.mp4")
    assert len(cam.pc2.encoders) > 0
    cam.stop_recording()
    assert len(cam.pc2.encoders) == 0


# ----------------------------------
# Image
# ----------------------------------


# Take a picture with a specific filename
def test_named_picture(cam: Camera):
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
def test_unnamed_picture(cam: Camera):
    with pytest.raises(PicameraZeroException):
        _ = cam.take_photo()
    with pytest.raises(PicameraZeroException):
        _ = cam.capture_image()


# Take a pic with a filename but no extension
def test_named_picture_no_ext(cam: Camera):
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
def test_unnamed_sequence(cam: Camera):
    with pytest.raises(PicameraZeroException):
        cam.capture_sequence()


# Test a sequence capture with a filename but no extension
def test_named_sequence_no_extension(cam: Camera):
    cam.capture_sequence("test")
    assert exists("test-0.jpg")
    assert exists("test-9.jpg")


# Test a named sequence capture with extension
def test_named_sequence(cam: Camera):
    cam.capture_sequence("testing.jpg")
    assert exists("testing-0.jpg")
    assert exists("testing-9.jpg")


# Test whether you can change the number of pics
def test_sequence_quantity(cam: Camera):
    cam.capture_sequence(filename="fewer", num_images=2)
    assert exists("fewer-0.jpg")
    assert exists("fewer-1.jpg")
    assert not exists("fewer-2.jpg")


# Test the sequence interval
def test_sequence_interval(cam: Camera):
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
def test_sequence_with_video(cam: Camera):
    cam.capture_sequence(filename="with-vid", make_video=True)
    assert exists("with-vid-timelapse.mp4")


# ----------------------------------
# Video and still
# ----------------------------------


# Can you take a video and stills
def test_video_with_stills(cam: Camera):
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


# Test whether the correct number of stills are taken
# if the interval is not exactly divisible by the duration
def test_video_with_stills_non_divisible(cam: Camera):
    cam.take_video_and_still(filename="xyz", duration=7, still_interval=3)
    assert exists("xyz-0.jpg")
    assert exists("xyz-1.jpg")
    assert not exists("xyz-2.jpg")
    assert exists("xyz.mp4")
