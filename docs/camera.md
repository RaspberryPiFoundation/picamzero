# Camera

The first thing you must do in any `picamzero` program is create a camera.

Add these two lines of code at the start of your program:

```
from picamzero import Camera
cam = Camera()
```

The `Camera` in the example is called `cam`, but you can call yours something different if you prefer.

The camera can do three basic things:

- show a **preview**
- take a **still** image (photo)
- record a **video**.

## Camera properties

The following properties of the camera can be set. There is no need to change any of these properties if you just want a standard image.

| Property      | Type    | Default  | Description |
| -----------   | ------- | -------- | ----------- |
| `brightness`    | float   | 0.0      | A value between between -1.0 and 1.0. |
| `contrast`      | float   | 1.0      | A value between 0.0 and 32.0. |
| `exposure`      | int     | None     | How long the exposure for a shot should be. The min and max values vary. |
| `gain`          | int     | None     | The analogue gain. The min and max values vary. |
| `greyscale`     | bool    | False    | Turn greyscale (black and white) mode on or off. Greyscale does **not** apply to video capture.|
| `white_balance` | str     | `"auto"`   | The white balance profile used. This can be `"auto"`, `"tungsten"`, `"fluorescent"`, `"indoor"`, `"daylight"` or `"cloudy"`. |

You can also change the size of the three modes (preview, still and video):

| Property          | Type    | Default  | Description |
| -----------       | ------- | -------- | ----------- |
| `preview_size`    | tuple   | Depends* | The width and height, in pixels, of the preview window, e.g. `(800, 600)`. Both the height and width must be even numbers and greater than 15.|
| `still_size`      | tuple   | Depends* | The width and height, in pixels, of any still images.  Both the height and width must be even numbers and greater than 15. |
| `video_size`      | tuple   | Depends* | The width and height, in pixels, of any video captured.  Both the height and width must be even numbers and greater than 15. |

*The default size will depend on which Raspberry Pi camera you are using.

Change a property by giving it a value, for example:

```
cam.brightness = 0.5
cam.greyscale = True
cam.video_size = (1920, 1080) # 1080p
```

---
## Camera methods

A method is something you can ask the camera to do.

### Flip the camera (`flip_camera`)

Flips the orientation of the camera. You can flip along the horizontal axis, the vertical axis or both. The flip will be applied to the preview, still images and videos.

```
flip_camera(
    vflip: bool,
    hflip: bool
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| vflip       | bool    | False     | No | Flips the image vertically. Setting this to True will provide an upside-down image. |
| hflip       | bool    | False     | No | Flips the image horizontally. Setting this to True will provide a mirror image. |

##### Example
```python
cam.flip_camera(vflip=True)
```

The camera image will be upside down.

Setting `flip_camera` more than once will mean earlier transforms are disregarded. For example:

```python
cam.flip_camera(vflip=True)
cam.flip_camera(hflip=True)
```
The camera will **only** be flipped horizontally. The previous `vflip` setting is reset by the second call to the method.



---

There are lots more camera methods for [previewing](preview_methods.md), [taking photos](photo_methods.md) and [recording videos](video_methods.md).
