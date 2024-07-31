from .Camera import Camera
from .PicameraZeroException import PicameraZeroException, override_sys_except_hook
import logging

__version__ = "0.0.1"

# Configure log level
logging.basicConfig(level=logging.INFO)

# declare the library's public API
__all__ = ["Camera", "PicameraZeroException"]

# Use PicameraZeroExceptions
override_sys_except_hook()
