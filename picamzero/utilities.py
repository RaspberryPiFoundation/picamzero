from .PicameraZeroException import PicameraZeroException
import os
from libcamera import controls
import cv2
import logging

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


# Return a dictionary of fonts
def font_dict(reverse_kv=False):
    fonts = {
        "simplex": (cv2.FONT_HERSHEY_SIMPLEX, "Normal size sans-serif font"),
        "plain": (cv2.FONT_HERSHEY_PLAIN, "Small size sans-serif font"),
        "duplex": (
            cv2.FONT_HERSHEY_DUPLEX,
            "Normal size sans-serif font (more complex)",
        ),
        "complex": (cv2.FONT_HERSHEY_COMPLEX, "Normal size serif font"),
        "triplex": (cv2.FONT_HERSHEY_TRIPLEX, "Larger size serif font"),
        "small": (cv2.FONT_HERSHEY_COMPLEX_SMALL, "Small size serif font"),
        "script_simplex": (
            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "Handwriting-style font",
        ),
        "script_complex": (
            cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
            "Complex handwriting-style font",
        ),
        "italic": (cv2.FONT_ITALIC, "Italic version of the current font"),
    }
    if reverse_kv:
        return {v: k for k, v in fonts.items()}
    else:
        return fonts


def check_font_in_dict(font):
    if isinstance(font, str):
        if font not in font_dict():
            # Font not found: return the list of available fonts with descriptions
            available_fonts = "\n".join(
                [f"{name}: {desc}" for name, (_, desc) in font_dict().items()]
            )
            logger.warning(
                f"""Invalid font '{font}'. Available fonts are:\n{available_fonts}
                Your font has been set to \'simplex\'"""
            )
            font = 0
        else:
            font = 2
        return font
    