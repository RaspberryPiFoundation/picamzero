from .Camera import Camera
from .PicameraZeroException import PicameraZeroException, override_sys_except_hook
import logging

# Configure log level
logging.basicConfig(
    level=logging.INFO
)

# declare the library's public API
__all__ = [
    "Camera"
]

# Use PicameraZeroExceptions
override_sys_except_hook()
