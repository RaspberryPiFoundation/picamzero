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


def set_camera_size(config, max_resolution, size, logger, error_msg_type, example_msg):
    if isinstance(size, tuple) and len(size) == 2:
        h, w = size
        max_h, max_w = max_resolution
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
            f"The size has been adjusted to {max_h}, {max_w}."
        )
