import logging
import os
import sys
import tempfile
import traceback
from types import TracebackType
from typing import Optional

logger = logging.getLogger(__name__)


class PicameraZeroException(Exception):
    """
    Base class for exceptions thrown by the picamera-zero
    library.
    """

    def __init__(self, message: str, hint: Optional[str] = None, *args):
        """
        :param str message - The reason for the exception.
        :param Optional[str] hint - An optional hint to resolve the exception.
        """
        self.message: str = message
        self.hint: Optional[str] = hint
        super().__init__(*args)

    def _format_exception(self) -> str:
        """
        This function is called to 'render' the exception
        """
        lines: list[str] = [
            "******************************************",
            "An error occurred: ",
            f"\t{self.message}",
        ]
        if self.hint:
            lines.append("Hint: ")
            lines.append(f"\t{self.hint}")
        return os.linesep.join(lines)

    def __str__(self) -> str:
        return self._format_exception()


def override_sys_except_hook():
    """
    When called, this function overrides the default
    sys.except hook to control how exceptions are formatted to the
    user. It could be used, for example, to control how much of
    the stack trace is shown to the library user - beginner
    beginner programmers may find a full stack trace quite
    intimidating.

    This would be called either in picamera-zero's __init__.py or when
    instantiating picamera-zero's Camera object:

    """

    def on_exception(exctype, value, stacktrace: TracebackType):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            traceback.print_tb(stacktrace, file=f)

        # Extract the filename
        tb: traceback.StackSummary = traceback.extract_tb(stacktrace)
        err_filename: str = tb[0].filename

        # Add details
        error_msg = "\nTo fix this, look at: \n"
        error_msg += f"\tFile: {err_filename}\n"
        error_msg += f"\tLine: {stacktrace.tb_lineno}"

        logger.error(
            str(value)
            + error_msg
            + f"\nTo see the full stack trace, type this terminal command:\n"
            f"\t nano {f.name}"
            "\n*************************************************"
        )

    sys.excepthook = on_exception
