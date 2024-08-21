# Writing your first program

1. With your Raspberry Pi switched off, connect your Raspberry Pi Camera to a camera port.
    ![Connect the camera ribbon](images/connect-camera.gif)

2. Type this code into your code editor, then save and run it:

```python
from picamzero import Camera
cam = Camera()
cam.take_photo("helloworld.jpg")
```

Your camera will start up and take a photo.

The photo will be saved in the same directory as your Python file.

Now try out some of the other methods by following the [recipes](recipes.md).



