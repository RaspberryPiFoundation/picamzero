from .Camera import Camera
import logging

# Configure log level
logging.basicConfig(
    level=logging.INFO
)

# declare the library's public API
__all__ = [
    "Camera"
]
