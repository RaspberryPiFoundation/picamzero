import pytest
from picamzero import PicameraZeroException
from picamzero import utilities as utils

# --------------------------------------------------
# Tests for functions that don't require PiCamera2
# --------------------------------------------------


# Test that the filename formatter works properly
@pytest.mark.parametrize(
    "filename,ext,expected",
    [
        ("blah.jpg", ".jpg", "blah.jpg"),
        ("blah", ".jpg", "blah.jpg"),
        ("blah.", ".jpg", "blah.jpg"),
        ("a", ".mp4", "a.mp4"),
        ("a.mp4", ".mp4", "a.mp4"),
        ("abc.jpg", ".mp4", "abc.mp4"),
        ("example", "", "example"),
        ("example", "-{:d}.jpg", "example-{:d}.jpg"),
        ("/photos/test.jpg", ".jpg", "/photos/test.jpg"),
        ("/videos/test.mp4", ".mp4", "/videos/test.mp4"),
        ("../test", ".mp4", "../test.mp4"),
    ],
)
def test_filename_format(filename, ext, expected):
    assert utils.format_filename(filename, ext) == expected


# Test that the image overlay checker
@pytest.mark.parametrize(
    "image_path,position,transparency,expected_pos,expected_trans",
    [
        # position tests
        ("blah.jpg", (0, 0), 1.0, (0, 0), 1.0),
        ("blah.jpg", (0, 0, 0), 1.0, (0, 0), 1.0),
        ("blah.jpg", "100, 100", 1.0, (0, 0), 1.0),
        # transparency tests
        ("blah.jpg", (0, 0), 1.0, (0, 0), 1.0),
        ("blah.jpg", (0, 0), 1.01, (0, 0), 0.5),
        ("blah.jpg", (0, 0), -0.1, (0, 0), 0.5),
        ("blah.jpg", (0, 0), 0, (0, 0), 0.5),
        ("blah.jpg", (0, 0), -1, (0, 0), 0.5),
        ("blah.jpg", (0, 0), -2, (0, 0), 0.5),
        ("blah.jpg", (0, 0), 3, (0, 0), 0.5),
        ("blah.jpg", (0, 0), -2.3, (0, 0), 0.5),
        ("blah.jpg", (0, 0), 3.3, (0, 0), 0.5),
    ],
)
def test_image_overlay_transparency(
    image_path, position, transparency, expected_pos, expected_trans
):
    image, pos, trans = utils.check_image_overlay(image_path, position, transparency)
    assert pos == expected_pos
    assert trans == expected_trans


# Test that you can't specify no filename
def test_filename_none():
    with pytest.raises(PicameraZeroException):
        _ = utils.format_filename(None, ".jpg")
