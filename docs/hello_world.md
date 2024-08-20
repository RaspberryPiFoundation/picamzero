# Writing your first program

1. With your Raspberry Pi switched off, connect your Raspberry Pi Camera to a camera port.
    ![Connect the camera ribbon](images/connect-camera.gif)

2. Switch on your Raspberry Pi, and open a terminal window.

    ![Open a terminal window](images/open-terminal.png)

3. Open a Python editor (e.g. Thonny) on your Raspberry Pi.

    ![Open a Python editor](images/open-editor.png)

4. Type in this code, save it and then run it:

```
from picamzero import Camera
cam = Camera()
cam.take_photo("helloworld.jpg")
```

Your camera will start up and take a photo.

The photo will be saved in the same directory as your Python file.

Now try out some of the other methods by following the [recipes](recipes.md).



