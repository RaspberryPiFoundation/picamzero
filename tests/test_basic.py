from datetime import datetime
from os.path import exists

import numpy as np
import piexif
import pytest
from libcamera import Transform, controls
from picamzero import Camera, PicameraZeroException, utilities
from picamzero.Camera import MAX_VIDEO_SIZE


@pytest.fixture
def cam_with_controls(cam: Camera):
    cam.brightness = 0.7
    cam.contrast = 11.2
    cam.exposure = 600
    cam.gain = 2
    cam.white_balance = "indoor"
    cam.greyscale = True
    cam.preview_size = (800, 600)
    cam.still_size = (800, 600)
    cam.video_size = (800, 600)
    cam.flip_camera(vflip=True, hflip=True)
    yield cam


# ----------------------------------
# Initialise camera
# ----------------------------------


# Initialise a camera
def test_init(cam: Camera):
    assert cam.pc2 is not None


# ----------------------------------
# Properties
# ----------------------------------


def test_invalid_control(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam._check_control_in_range("ThisDoesntExist", 1)


def test_property_brightness(cam: Camera):
    cam.pc2.start()
    cam.brightness = 0.5
    assert cam.pc2.controls.Brightness == 0.5
    assert cam.brightness == 0.5


def test_property_invalid_brightness(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam.brightness = 500


def test_property_contrast(cam: Camera):
    cam.contrast = 12.5
    assert cam.pc2.controls.Contrast == 12.5
    assert cam.contrast == 12.5


def test_property_invalid_contrast(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam.contrast = 40.0


def test_property_exposure(cam: Camera):
    cam.pc2.start()
    cam.exposure = 500
    assert cam.pc2.controls.ExposureTime == 500
    assert cam.exposure == 500


def test_property_invalid_exposure(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam.exposure = cam.pc2.camera_controls["ExposureTime"][0] - 1


def test_property_gain(cam: Camera):
    cam.pc2.start()
    cam.gain = 5
    assert cam.pc2.controls.AnalogueGain == 5
    assert cam.gain == 5


def test_property_invalid_gain(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam.gain = 500


def test_property_white_balance(cam: Camera):
    cam.pc2.start()
    cam.white_balance = "tungsten"
    assert cam.pc2.controls.AwbMode == controls.AwbModeEnum.Tungsten
    assert cam.white_balance == "tungsten"


def test_property_invalid_white_balance(cam: Camera):
    cam.pc2.start()
    with pytest.raises(PicameraZeroException):
        cam.white_balance = "NotAThing"


def test_property_set_video_size(cam: Camera):
    cam.pc2.start()
    cam.video_size = (1280, 720)
    assert cam.pc2.video_configuration.size == (1280, 720)


def test_property_set_preview_size(cam: Camera):
    cam.pc2.start()
    cam.preview_size = (1280, 720)
    assert cam.pc2.preview_configuration.size == (1280, 720)


def test_property_set_still_size(cam: Camera):
    cam.pc2.start()
    cam.still_size = (1280, 720)
    assert cam.pc2.still_configuration.size == (1280, 720)


@pytest.mark.parametrize(
    "size", [(9000, 6000), (-9000, 6000), (9000, -6000), (-9000, -6000), (90.00, 6.000)]
)
def test_property_invalid_size(cam: Camera, size):
    cam.preview_size = size
    assert cam.preview_size == cam.pc2.sensor_resolution
    cam.still_size = size
    assert cam.still_size == cam.pc2.sensor_resolution
    cam.video_size = size
    assert cam.video_size == MAX_VIDEO_SIZE


# -------------------------------------
# Test controls and transform retained
# -------------------------------------


@pytest.mark.parametrize(
    "method_to_call", ["start_preview", "take_photo", "record_video"]
)
@pytest.mark.parametrize(
    "prop,expected",
    [
        ("brightness", 0.7),
        ("contrast", 11.2),
        ("exposure", 600),
        ("gain", 2),
        ("white_balance", "indoor"),
        ("greyscale", True),
        ("preview_size", (800, 600)),
        ("still_size", (800, 600)),
        ("video_size", (800, 600)),
        ("brightness", 0.7),
        ("contrast", 11.2),
        ("exposure", 600),
        ("gain", 2),
        ("white_balance", "indoor"),
        ("greyscale", True),
        ("preview_size", (800, 600)),
        ("still_size", (800, 600)),
        ("video_size", (800, 600)),
        ("brightness", 0.7),
        ("contrast", 11.2),
        ("exposure", 600),
        ("gain", 2),
        ("white_balance", "indoor"),
        ("greyscale", True),
        ("preview_size", (800, 600)),
        ("still_size", (800, 600)),
        ("video_size", (800, 600)),
    ],
)
def test_controls_retained(
    cam_with_controls: Camera, method_to_call: str, prop: str, expected
):

    cam = cam_with_controls

    # Get the method to call
    run_method = getattr(cam, method_to_call)

    # Add an arg if it's take photo or record video
    if method_to_call in ["take_photo", "record_video"]:
        run_method("example")
    else:
        run_method()

    assert getattr(cam, prop) == expected


@pytest.mark.parametrize(
    "method_to_call", ["start_preview", "take_photo", "record_video"]
)
@pytest.mark.parametrize(
    "mode", ["preview_configuration", "still_configuration", "video_configuration"]
)
def test_transforms_retained(cam_with_controls: Camera, method_to_call: str, mode: str):

    cam = cam_with_controls

    # Get the method to call
    run_method = getattr(cam, method_to_call)

    # Add an arg if it's take photo or record video
    if method_to_call in ["take_photo", "record_video"]:
        run_method("example")
    else:
        run_method()

    expected_orientation = Transform(hflip=1, vflip=1)
    assert getattr(cam.pc2, mode).make_dict()["transform"] == expected_orientation


# ----------------------------------
# Preview
# ----------------------------------


# Can you start and stop the preview
def test_preview_starts_and_stops(cam: Camera):
    cam.start_preview()
    assert cam.pc2._preview is not None
    cam.stop_preview()
    assert cam.pc2._preview is None


# ----------------------------------
# Camera orientation (hflip/vflip)
# ----------------------------------


def test_cam_flip_h(cam: Camera):
    cam.flip_camera(hflip=True)
    assert cam.hflip is True
    # The transform should be retained after starting the preview
    cam.start_preview()
    assert cam.pc2.preview_configuration.make_dict()["transform"] == Transform(hflip=1)
    cam.stop_preview()


def test_cam_flip_v(cam: Camera):
    cam.flip_camera(vflip=True)
    assert cam.vflip is True
    cam.start_preview()
    assert cam.pc2.preview_configuration.make_dict()["transform"] == Transform(vflip=1)
    cam.stop_preview()


def test_cam_flip_v_and_h(cam: Camera):
    cam.flip_camera(hflip=True, vflip=True)
    assert cam.hflip is True
    assert cam.vflip is True
    cam.start_preview()
    assert cam.pc2.preview_configuration.make_dict()["transform"] == Transform(
        hflip=1, vflip=1
    )
    cam.stop_preview()


def test_cam_flip_none(cam: Camera):
    cam.flip_camera(hflip=False, vflip=False)
    assert cam.vflip is False
    assert cam.hflip is False
    cam.start_preview()
    assert cam.pc2.preview_configuration.make_dict()["transform"] == Transform()
    cam.stop_preview()


# ----------------------------------
# Annotation
# ----------------------------------


def test_annotation_properties(cam: Camera):
    cam.annotate(
        text="hello",
        color=(255, 255, 0, 255),
        position=(100, 100),
        scale=4,
        thickness=6,
    )
    assert cam._text == "hello"
    assert cam._text_properties["color"] == (255, 255, 0, 255)
    assert cam._text_properties["position"] == (100, 100)
    assert cam._text_properties["scale"] == 4
    assert cam._text_properties["thickness"] == 6


def test_annotation_invalid_font(cam: Camera):
    text = "hello"
    font = "compl"
    cam.annotate(
        text=text,
        font=font,
    )
    assert cam._text_properties["font"] == 0


def test_annotation_valid_font(cam: Camera):
    text = "hello"
    font = "plain2"
    cam.annotate(
        text=text,
        font=font,
    )
    assert cam._text_properties["font"] == utilities.check_font_in_dict(font)


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


def test_capture_array(cam: Camera):
    arr = cam.capture_array()
    expected_width, expected_height = cam.pc2.sensor_resolution
    assert arr.shape == (expected_height, expected_width, 3)
    assert arr.dtype == np.uint8


# ----------------------------------
# Sequence
# ----------------------------------


def test_picture_with_gps_coordinates(cam):
    filename = "picture_with_gps.jpg"
    latitude = (1.0, 29.1, 29.0, 48.78250810956524)
    longitude = (-1.0, 79.0, 17.0, 53.33060722541995)
    cam.take_photo(filename, gps_coordinates=(latitude, longitude))
    assert exists(filename)
    exif_data = piexif.load(filename)
    assert "GPS" in exif_data
    gps_ifd = exif_data["GPS"]
    assert gps_ifd[piexif.GPSIFD.GPSLatitude] == ((29, 1), (29, 1), (488, 10))
    assert gps_ifd[piexif.GPSIFD.GPSLatitudeRef].decode() == "N"
    assert gps_ifd[piexif.GPSIFD.GPSLongitude] == ((79, 1), (17, 1), (533, 10))
    assert gps_ifd[piexif.GPSIFD.GPSLongitudeRef].decode() == "W"


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


# ----------------------------------
# Filters
# ----------------------------------


def test_greyscale_filter(cam: Camera):
    cam.start_preview()
    cam.greyscale = True
    assert cam.pc2.controls.Saturation == 0.0
    cam.greyscale = False
    assert cam.pc2.controls.Saturation == 1.0
