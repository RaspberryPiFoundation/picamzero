from .PicameraZeroException import PicameraZeroException
import os
from libcamera import controls


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


def set_camera_size(config, size, max_resolution, logger, error_msg_type, example_msg):
    if isinstance(size, tuple) and len(size) == 2:
        h, w = size
        if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
            max_h, max_w = max_resolution
            if h > max_h or w > max_w:
                logger.error(
                    """Warning: The specified size exceeds the camera's
                    maximum allowed dimensions. The size has been adjusted to fit."""
                )
            h = min(h, max_h)
            w = min(w, max_w)

            config.size = (h, w)
        else:
            raise PicameraZeroException(
                f"""The height and width of the {error_msg_type} must
                be two positive integers.""",
                f"Example: {example_msg}",
            )
    else:
        raise PicameraZeroException(
            f"""The size of the {error_msg_type} must be two positive integers,
            separated by a comma and in brackets.""",
            f"Example: {example_msg}.",
        )
