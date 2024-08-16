from .PicameraZeroException import PicameraZeroException
import os
from libcamera import controls, CameraConfiguration
import cv2
import logging
import piexif

logger = logging.getLogger(__name__)


def format_filename(filename: str, ext: str) -> str:
    """
    Helper method: Generate suitable filename/extension

    :param str filename:
            The text filename the user entered

    :param str ext:
            The desired extension to be appended (e.g. ".jpg")

    :return str filename:
            The formatted filename
    """
    if filename is None:
        raise PicameraZeroException(
            "No filename was specified",
            hint="A filename is required when taking a photo or recording a video",
        )
    else:

        file_root, file_ext = os.path.splitext(filename)

        # Check if the extension is valid, if not replace it
        if file_ext.lower() != ext:
            filename = file_root + ext

    return filename


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
    example_msg: str,
):
    max_h, max_w = max_resolution
    if isinstance(size, tuple) and len(size) == 2:
        h, w = size
        if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
            if h > max_h or w > max_w:
                config.size = (max_h, max_w)
                logger.warning(
                    f"""You specified an invalid size for the camera.
                    The size has been adjusted to {max_h}, {max_w}."""
                )
            else:
                config.size = (h, w)
        else:
            config.size = (max_h, max_w)
            logger.warning(
                f"""The height and width of the {error_msg_type} must
                be two positive integers.
                Example: {example_msg}.
                The size has been adjusted to {max_h}, {max_w}."""
            )
    else:
        config.size = (max_h, max_w)
        logger.warning(
            f"""The size of the {error_msg_type} must be two positive integers,
            separated by a comma and in brackets.""",
            f"Example: {example_msg}.",
            f"The size has been adjusted to {max_h}, {max_w}.",
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
