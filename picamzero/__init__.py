from .Camera import Camera
import logging

__version__ = "0.0.1"

# Configure log level
logging.basicConfig(
    level=logging.INFO
)

# declare the library's public API
__all__ = [
    "Camera"
]