### Camera

All programs which use picamzero first require you to create a camera object, which is as simple as adding these two lines of code at the start of your file:

```
from picamzero import Camera
cam = Camera()
```

The `Camera` object we have created in the example is called `cam`, but you can call yours something different if you prefer.

The camera can do three basic things: 

- show a **preview**
- take a **still** image (photo)
- record a **video**.

#### Camera properties

The following properties of the camera can be set. There is no need to change any of these properties if you just want a standard image.

| Property      | Type    | Default  | Description |
| -----------   | ------- | -------- | ----------- |
| `brightness`    | float   | 0.0      | A value between between -1.0 and 1.0. |
| `contrast`      | float   | 1.0      | A value between 0.0 and 32.0. |
| `exposure`      | int     | None     | How long the exposure for a shot should be. The min and max values vary. |
| `gain`          | int     | None     | The analogue gain. The min and max values vary. |
| `greyscale`     | bool    | False    | Turn greyscale (black and white) mode on or off. |
| `white_balance` | str     | `"auto"`   | The white balance profile used. This can be `"auto"`, `"tungsten"`, `"fluorescent"`, `"indoor"`, `"daylight"` or `"cloudy"`. |

You can also change the size of the three modes (preview, still and video):

| Property          | Type    | Default  | Description |
| -----------       | ------- | -------- | ----------- |
| `preview_size`    | tuple   | Depends* | The height and width, in pixels, of the preview window, e.g. `(800, 600)`. Both the height and width must be even numbers.|
| `still_size`      | tuple   | Depends* | The height and width, in pixels, of any still images. Both the height and width must be even numbers. |
| `video_size`      | tuple   | Depends* | The height and width, in pixels, of any video captured. Both the height and width must be even numbers. |

*The default size will depend on which Raspberry Pi camera you are using. 

The defaults will be set to make the best use of your camera, so there is no need to change them unless you want to do something specific. 

Change a property by giving it a value, for example:

```
cam.brightness = 0.5
cam.greyscale = True
```



---
#### Flip the camera (`flip_camera`)

Flips the orientation of the camera. You can flip along the horizontal axis, the vertical axis or both. The flip will be applied to the preview, still images and videos.

```
flip_camera(
    vflip: bool,
    hflip: bool
) -> None
```

| Parameter   | Type    | Default  | Description |
| ----------- | ------- | -------- | ----------- |
| vflip       | bool    | False     | Whether to flip along the vertical axis. |
| hflip       | bool    | False     | Whether to flip along the horizontal axis. |

###### Example
```
cam.flip_camera(vflip=True)
```

The camera image will be flipped along the vertical axis.

---
