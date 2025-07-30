import logging

from .Camera import Camera
from .PicameraZeroException import PicameraZeroException, override_sys_except_hook

__version__ = "1.0.2"

# Configure log level
logging.basicConfig(level=logging.INFO)

# declare the library's public API
__all__ = ["Camera", "PicameraZeroException"]

# Use PicameraZeroExceptions
override_sys_except_hook()
