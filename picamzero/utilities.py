import logging
import os
from pathlib import Path
from typing import Union

import cv2
import piexif
from libcamera import CameraConfiguration, controls

from .PicameraZeroException import PicameraZeroException

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.WARN)
logger = logging.getLogger(__name__)


def format_filename(filepath: Union[str, Path], ext: str) -> str:
    """
    Helper method: Generate suitable filename/extension

    :param str | Path filename:
            The filename the user entered, either as text or
            as a Path object

    :param str ext:
            The desired extension to be appended (e.g. ".jpg")

    :return str filename:
            The formatted filename
    """
    if filepath is None:
        raise PicameraZeroException(
            "No filename was specified",
            hint="A filename is required when taking a photo or recording a video",
        )
    else:
        formatted_name = ""
        if isinstance(filepath, Path):
            file_root, file_ext = os.path.splitext(filepath.name)
            formatted_name = f"{str(filepath.parent)}/{file_root}{ext}"

        else:
            file_root, file_ext = os.path.splitext(filepath)
            formatted_name = file_root + ext

    return formatted_name


# Return a dictionary of possible controls
def possible_controls(reverse_kv=False):
    poss_controls = {
        "auto": controls.AwbModeEnum.Auto,
        "tungsten": controls.AwbModeEnum.Tungsten,
        "fluorescent": controls.AwbModeEnum.Fluorescent,
        "indoor": controls.AwbModeEnum.Indoor,
        "daylight": controls.AwbModeEnum.Daylight,
        "cloudy": controls.AwbModeEnum.Cloudy,
    }
    if reverse_kv:
        return {v: k for k, v in poss_controls.items()}
    else:
        return poss_controls


def set_camera_size(
    config: CameraConfiguration,
    max_resolution: tuple[int, int],
    size: tuple[int, int],
    error_msg_type: str,
):
    """
    :param CameraConfiguration config:
        The camera configuration to mutate.
    :param tuple[int,int] max_resolution:
        A [width,height] two-tuple expressing the maximum width and height
        in pixels.
    :param tuple[int,int] size:
        A [width,height] two-tuple expressing the requested size in pixels.
    :param str error_msg_type:
        The name of the mode to use in the error message, should the size
        be greater than the max_resolution.

    :rtype None
    :return None
    """
    max_w, max_h = max_resolution
    if isinstance(size, tuple) and len(size) == 2:
        w, h = size
        if isinstance(h, int) and isinstance(w, int) and h > 15 and w > 15:
            if h > max_h or w > max_w:
                config.size = (max_w, max_h)
                logger.warning(
                    f"\nThe {error_msg_type} size couldn't be set to {size}"
                    f"\nReason: One or both of the values was too large."
                    f"\nThe size has been adjusted to ({max_w}, {max_h})."
                )
            else:
                # Make sure both are even
                if h % 2 or w % 2:
                    h = h - 1 if h % 2 else h
                    w = w - 1 if w % 2 else w
                    logger.warning(
                        f"\nThe {error_msg_type} size couldn't be set to {size}"
                        f"\nReason: Width and height must be even numbers."
                        f"\nThe size has been adjusted to ({w}, {h})."
                    )

                config.size = (w, h)
        else:
            config.size = (max_w, max_h)
            logger.warning(
                f"\nThe {error_msg_type} size couldn't be set to {size}"
                f"\nReason: Width and height must be integers greater than 15."
                f"\nThe size has been adjusted to ({max_w}, {max_h})."
            )
    else:
        config.size = (max_w, max_h)
        logger.warning(
            f"\nThe {error_msg_type} size couldn't be set to {size}"
            f"\nReason: The size provided was in the wrong format."
            f"The size has been adjusted to ({max_w}, {max_h})."
        )


# Return a dictionary of fonts
def font_dict(reverse_kv=False):
    fonts = {
        "plain1": cv2.FONT_HERSHEY_SIMPLEX,
        "plain2": cv2.FONT_HERSHEY_DUPLEX,
        "plain-small": cv2.FONT_HERSHEY_PLAIN,
        "serif1": cv2.FONT_HERSHEY_COMPLEX,
        "serif2": cv2.FONT_HERSHEY_TRIPLEX,
        "serif-small": cv2.FONT_HERSHEY_COMPLEX_SMALL,
        "handwriting1": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        "handwriting2": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    }
    if reverse_kv:
        return {v: k for k, v in fonts.items()}
    else:
        return fonts


def check_font_in_dict(font):
    if isinstance(font, str):
        if font not in font_dict():
            # Font not found: return the list of available fonts with descriptions
            available_fonts = ", ".join([key for key in font_dict().keys()])
            logger.warning(
                f"The font '{font}' is not available. Available fonts are:"
                f"\n{available_fonts}."
            )
            logger.warning("Your font has been set to 'plain1'")
            font = cv2.FONT_HERSHEY_SIMPLEX
        else:
            font = font_dict()[font]
        return font


def convert_color(color):
    """
    Converts a color from a string (e.g., "#ffffff", "#ffffff00", "blue")
    or a tuple (255, 255, 255, 255) into a 4-tuple (R, G, B, A).
    """

    color_names = {
        "white": (255, 255, 255, 255),
        "silver": (192, 192, 192, 255),
        "gray": (128, 128, 128, 255),
        "black": (0, 0, 0, 255),
        "red": (255, 0, 0, 255),
        "maroon": (128, 0, 0, 255),
        "yellow": (255, 255, 0, 255),
        "olive": (128, 128, 0, 255),
        "lime": (0, 255, 0, 255),
        "green": (0, 128, 0, 255),
        "aqua": (0, 255, 255, 255),
        "teal": (0, 128, 128, 255),
        "blue": (0, 0, 255, 255),
        "navy": (0, 0, 128, 255),
        "fuchsia": (255, 0, 255, 255),
        "purple": (128, 0, 128, 255),
    }

    if color is not None:

        if isinstance(color, str):
            color = color.strip().lower()

            if color in color_names:
                return color_names[color]

            if color.startswith("#"):

                # Check length for RGB (#RRGGBB) or RGBA (#RRGGBBAA)
                if len(color) == 7:
                    color += "ff"  # Add alpha value if not provided
                elif len(color) != 9:
                    logger.warning(
                        f"""{color} is not a valid hex color.
                        It must be in the format #RRGGBB or #RRGGBBAA.
                        The font color has been set to black (#000000ff)"""
                    )
                    return None

                # Split the color into its hex values
                hex_colors = (
                    color[1:3],  # Red
                    color[3:5],  # Green
                    color[5:7],  # Blue
                    color[7:9],  # Alpha
                )

                # Convert hex to integers and validate
                rgba_values = []
                for hex_color in hex_colors:
                    try:
                        int_color = int(hex_color, 16)
                    except ValueError:
                        logger.warning(
                            f"""{color} contains an invalid hex value.
                            Each part must be a valid hex value
                            between 00 and ff.
                            The font color has been set to black (#000000ff)"""
                        )
                        return None
                    if not (0 <= int_color <= 255):
                        logger.warning(
                            f"""{color} contains a value out of range.
                            Each part must be between 00 and ff.
                            The font color has been set to black (#000000ff)"""
                        )
                        return None
                    rgba_values.append(int_color)

                return tuple(rgba_values)

        # If the color is not a string, treat it as an iterable (tuple or list)
        else:
            try:
                no_of_colors = len(color)
            except TypeError:
                logger.warning(
                    "A color must be a list or tuple of 3 or 4 values.",
                    "The font color has been set to black (0, 0, 0, 255)",
                )
                return None

            if no_of_colors not in (3, 4):
                logger.warning(
                    "A color must contain 3 or 4 values.",
                    "Example: (red, green, blue) or (red, green, blue, alpha)."
                    "The font color has been set to black (0, 0, 0, 255)",
                )
                return None

            # Default alpha value if not provided
            if no_of_colors == 3:
                color = (*color, 255)

            for c in color:
                if not (0 <= c <= 255):
                    logger.warning(
                        f"""{c} is not a valid color value.
                    The font color has been set to black (0, 0, 0, 255)"""
                    )
                    None
            return tuple(color)

    logger.warning(
        """
        The font color you specified was not in the expected format.
        It will be set to \"black\""""
    )
    return None


def check_image_overlay(image_path, position, transparency):
    if not os.path.exists(image_path):
        raise PicameraZeroException(f"The file does not exist: {image_path}")

    if not os.path.isfile(image_path):
        raise PicameraZeroException(f"The path is not a file: {image_path}")

    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
    if not image_path.lower().endswith(valid_extensions):
        raise PicameraZeroException(
            f"Invalid file extension: {image_path}",
            hint=f"Supported extensions are: {valid_extensions}",
        )

    # Attempt to read the image
    overlay_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if overlay_img is None:
        raise PicameraZeroException(
            f"Could not load the overlay image from {image_path}"
        )

    if not isinstance(position, tuple) or not len(position) == 2:
        position = (0, 0)
        logger.warning(
            """You have specified an invalid position for the overlay image.
            The position must be two positive integers, separated by a comma
            and in brackets.
            The position has been set to (0, 0) - the top left."""
        )

    if not isinstance(transparency, float) or not (0.0 <= transparency <= 1.0):
        transparency = 0.5
        logger.warning(
            """You have specified an invalid transparency for the overlay image.
            The transparency must be a float between 0.0 and 1.0.
            The transparency has been set to 0.5"""
        )

    return overlay_img, position, transparency


def signed_dms_coordinates_to_exif_dict(gps_coordinates) -> dict:
    """
    :param gps_coordinates: A (latitude, longitude) tuple where
        both latitude and longitude are themselves tuples of the
        form (sign, degrees, minutes, seconds). This format
        can be generated from the skyfield library's signed_dms
        function.
    """
    try:
        latitude, longitude = gps_coordinates
        exif_gps_coordinates = []
        for coordinate in gps_coordinates:
            degrees, minutes, seconds = coordinate[1:]
            degrees = (int(degrees), 1)
            minutes = (int(minutes), 1)
            seconds = (round(seconds * 10), 10)
            exif_gps_coordinates.append((degrees, minutes, seconds))
        exif_latitude, exif_longitude = exif_gps_coordinates

        gps_ifd: dict = {
            piexif.GPSIFD.GPSLatitude: exif_latitude,
            piexif.GPSIFD.GPSLatitudeRef: "S" if latitude[0] < 0 else "N",
            piexif.GPSIFD.GPSLongitude: exif_longitude,
            piexif.GPSIFD.GPSLongitudeRef: "W" if longitude[0] < 0 else "E",
        }
        return {"GPS": gps_ifd}

    except ValueError:
        raise PicameraZeroException(
            "gps_coordinates should be a (latitude, longitude) "
            + "tuple where both latitude and longitude are tuples "
            + "of the form (sign, degrees, minutes, seconds). "
            + "This format can be generated by using the "
            + "skyfield library's signed_dms function, for example."
        )


class OneIndexedString(str):
    """
    A string with a custom format function
    to be used where 1-indexing is required
    in third-party code that calls the format
    function, as in the loop below:

        to_format = OneIndexedString("image-{:03d}")
        print([to_format.format(i) for i in range(3)])

    This will output:
        ["image-001","image-002","image-003"]

    A normal string, by contrast, would output:
        ["image-000","image-000","image-000"]

    """

    def format(self, *args, **kwargs) -> str:
        if args:
            args_copy = list(args)
            args_copy[0] = int(args_copy[0]) + 1
            args = tuple(args_copy)
        return super().format(*args, **kwargs)
