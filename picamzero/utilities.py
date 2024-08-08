from .PicameraZeroException import PicameraZeroException
import os


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
