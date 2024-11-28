from pathlib import Path

import pytest
from picamzero import PicameraZeroException
from picamzero import utilities as utils

tests_dir: Path = Path(__file__).parent

blah_path: Path = tests_dir / "blah.jpg"

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
        (Path("../test"), ".mp4", "../test.mp4"),
        (Path("images/beep.jpg"), ".jpg", "images/beep.jpg"),
        (Path("whatever.jpg"), ".jpg", "./whatever.jpg"),
    ],
)
def test_filename_format(filename, ext, expected):
    assert utils.format_filename(filename, ext) == expected


# Test the color converter
@pytest.mark.parametrize(
    "color,expected",
    [
        ("black", (0, 0, 0, 255)),
        ("white", (255, 255, 255, 255)),
        ("#ffffff", (255, 255, 255, 255)),
        ((0, 0, 0, 0), (0, 0, 0, 0)),
        ((255, 255, 255, 255), (255, 255, 255, 255)),
        ("blu", None),
        ("fff333", None),
        ("", None),
    ],
)
def test_color_converter(color, expected):
    assert utils.convert_color(color) == expected


# Test the image overlay checker
@pytest.mark.parametrize(
    "image_path,position,transparency,expected_pos,expected_trans",
    [
        # position tests
        (blah_path, (0, 0), 1.0, (0, 0), 1.0),
        (blah_path, (0, 0, 0), 1.0, (0, 0), 1.0),
        (blah_path, "100, 100", 1.0, (0, 0), 1.0),
        # transparency tests
        (blah_path, (0, 0), 1.0, (0, 0), 1.0),
        (blah_path, (0, 0), 1.01, (0, 0), 0.5),
        (blah_path, (0, 0), -0.1, (0, 0), 0.5),
        (blah_path, (0, 0), 0, (0, 0), 0.5),
        (blah_path, (0, 0), -1, (0, 0), 0.5),
        (blah_path, (0, 0), -2, (0, 0), 0.5),
        (blah_path, (0, 0), 3, (0, 0), 0.5),
        (blah_path, (0, 0), -2.3, (0, 0), 0.5),
        (blah_path, (0, 0), 3.3, (0, 0), 0.5),
    ],
)
def test_image_overlay_position_and_transparency(
    image_path, position, transparency, expected_pos, expected_trans
):
    image, pos, trans = utils.check_image_overlay(
        str(image_path), position, transparency
    )
    assert pos == expected_pos
    assert trans == expected_trans


# Test that you can't specify no filename
def test_filename_none():
    with pytest.raises(PicameraZeroException):
        _ = utils.format_filename(None, ".jpg")  # type: ignore


def test_one_indexed_string():
    to_format = utils.OneIndexedString("image-{:03d}")
    assert [to_format.format(i) for i in range(3)] == [
        "image-001",
        "image-002",
        "image-003",
    ]
