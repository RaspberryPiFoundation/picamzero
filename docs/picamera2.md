# Picamzero and Picamera2

The `picamzero` library is a simplified wrapper of the `Picamera2` library. This means that if you need to use more advanced features from `Picamera2` that are not available in `picamzero`, you can do this without having to alter the rest of your program.

To do this, access the `pc2` object inside the camera:

```python
from picamzero import Camera
cam = Camera()

# Use a Picamera2 method
cam.pc2.start_encoder()
```

