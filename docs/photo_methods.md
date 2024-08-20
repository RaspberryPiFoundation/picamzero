# Photo methods

---
## Take a photo
#### `take_photo`

Takes a photograph using the camera and saves it as a `.jpg` image.
Returns the filename of the image.

```
take_photo(
    filename: str,
    gps_coordinates: tuple[tuple[float, float, float, float],
                     tuple[float, float, float, float]]
) -> str
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str | None     |  Yes | A file name for a `.jpg` image. This can also be a path to a file. |
| gps_coordinates    | tuple | None     | No | GPS coordinates to be associated with the image, specified as a (latitude, longitude) tuple where both latitude and longitude are themselves tuples of the form (sign, degrees, minutes, seconds). This format can be generated from the [skyfield library](https://github.com/skyfielders/python-skyfield)'s `signed_dms` function. |

##### Example
```
cam.take_photo("mypic.jpg")
```

The image will be saved into the same folder as the Python script, unless a path is specified. In this example, the image will be saved into a `photos` folder.

```
cam.take_photo("photos/mypic.jpg")
```

This method can also be called as ```capture_image()``` and will behave in exactly the same way.

```
cam.capture_image("mypic.jpg")
```
---

## Capture a sequence of images (timelapse)
#### `capture_sequence`

Take a series of `num_images` with a gap of `interval` between each one, and save them as
`filename` with an auto-number. Optionally, `make_video` using all of the images. All images will be in `.jpg` format and video in `.mp4` format.

```
capture_sequence(
    filename: str,
    num_images: int,
    interval: float,
    make_video: bool
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str  | None     | Yes | A file name for a `.jpg` image. This can also be a file path. |
| num_images  | int     | `10`       | No | How many images to take.|
| interval    | float   | `0.01`     | No | How long to wait in between each image, in seconds. |
| make_video  | bool    | `False`    | No | Whether to make a `.mp4` video of the images. |


##### Example
```
cam.capture_sequence("mysequence.jpg", 12, 0.5, True)
```

This will take a sequence of 12 images, at an interval of half a second (0.5), and then make a timelapse video of the images. The video will be called `mysequence.mp4`.

---

## Add an image overlay
#### `add_image_overlay`

Add an image on top of the preview and to still images captured by the camera. Does _not_ overlay the image on video.

```
add_image_overlay(
    image_path: str,
    position: tuple,
    transparency: float
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| image_path   | str  | -    | Yes | The path to an image to use as the overlay. The image must be in `PNG`, `JPG`/`JPEG` or `BMP` format.  |
| position   | tuple  |  `(0,0)`   | No  | A tuple of x,y coordinates for the position of the top left corner of the image.  |
| transparency   | float  |  `0.5`   | No | How transparent the image should be. This can be any value between 0 (completely transparent) and 1 (completely opaque). |


#### Example
```
cam.add_image_overlay("logo.gif")
```

This will add an overlay to previews and images taken with the camera.

---

##  Add a text annotation
#### `annotate`

Adds a text annotation to the preview and to still images captured by the camera. Does _not_ annotate video.

```
annotate(
    text: str,
    font: str,
    color: str/tuple,
    scale: int,
    thickness: int,
    position: tuple,
    bgcolor: tuple,
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| text        | str     | `"Default Text"`     | No | The text to overlay on the image/preview.  |
| font        | str     | `"plain1"`          | No | The font to use. Available fonts are:  `plain1`, `plain2`, `plain-small`, `serif1`,`serif2`, `serif-small`, `handwriting1`, `handwriting2` |
| color       | str/tuple   | `"white"` | No | A colour in RGBA, hex or color string format. (See the [colors](colors.md) documentation for more details.) |
| scale       | int     | `3`  | No | The base size of the font will be multiplied by this number, for example a value of `2` will make it twice as large. |
| thickness   | int     | `3`  | No | The thickness of the lines used in the font, measured in px. The value must be between `1` and `10`. |
| position    | tuple   | `(0, 0)`  |  No |  A pair of x, y coordinates for the top left corner of the text. |
| bgcolor     | tuple   | None  |  No | A colour in RGBA, hex or color string format. (See the [colors](colors.md) documentation for more details.) |

##### Example
```
cam.add_image_overlay("logo.gif")
```

This will add an overlay to the preview and any images captured.

---