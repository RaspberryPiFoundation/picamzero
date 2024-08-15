### Photo methods

---
#### Take a photo (`take_photo`)

Takes a photograph using the camera and saves it as a `.jpg` image.
Returns the filename of the image.

```
take_photo(filename: str) -> str
```

| Parameter   | Type    | Default  | Description |
| ----------- | ------- | -------- | ----------- |
| filename    | str | None     | A file name for a .jpg image. This can also be a path to a file. |

###### Example
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

#### Capture a sequence of images (timelapse) (`capture_sequence`)

Take a series of `num_images` with a gap of `interval` between each one, and save them as
`filename` with an auto-number. Optionally, `make_video` using all of the images.

```
capture_sequence(
    filename: str,
    num_images: int,
    interval: float,
    make_video: bool
) -> None
```

| Parameter   | Type    | Default  | Description |
| ----------- | ------- | -------- | ----------- |
| filename    | str  | None     | A file name for a .jpg image. This can also be a file path. |
| num_images  | int     | 10       | How many images to take.|
| interval    | float   | 0.01     | How long to wait in between each image, in seconds. |
| make_video  | bool    | False    | Whether to make a `.mp4` video of the images. |


###### Example
```
cam.capture_sequence("mysequence.jpg", 12, 0.5, True)
```

This will take a sequence of 12 images, at an interval of half a second (0.5), and then make a timelapse video of the images. The video will be called `mysequence.mp4`.

---

#### Add an image overlay (`add_image_overlay`)

Add an image on top of the preview and to still images captured by the camera. Does _not_ overlay the image on video.

```
add_image_overlay(PARAMETER_NAME: str) -> None
```

| Parameter   | Type    | Default  | Description |
| ----------- | ------- | -------- | ----------- |
| PARAMETER_NAME    | str  | None     | A GIF image.  |



###### Example
```
cam.add_image_overlay("logo.gif")
```

This will add an overlay to [INSERT DESCRIPTION]

---

####  Add a text annotation (`annotate`)

Adds a text annotation to the preview and to still images captured by the camera. Does _not_ annotate video.

```
annotate(
    text: str,
    font: str,
    color: tuple,
    origin: tuple,
    scale: int,
    thickness: int,
    position: tuple,
    bgcolor: tuple,
    video: bool,
) -> None
```

| Parameter   | Type    | Default            | Description                   |
| ----------- | ------- | ------------------ | ----------------------------- |
| text        | str     | "Default Text"     | The text to overlay on the image/preview.  |
| font        | str     | "simplex"          | The font to use. Available fonts are: [TO DO] |
| color       | tuple   | (255, 255, 255, 255)  | A colour as a RGBA value. The first three values are Red, Green and Blue, and the final one is the Alpha (transparency). All values must be between 0 and 255. |
| origin      | tuple   | (50, 50)  | [TO DO: CAN WE REMOVE THIS?] |
| scale       | int     | 3  | How large the text is. [TO DO - WHAT CAN IT BE?] |
| thickness   | int     | 3  | How thick the text is. [TO DO - WHAT CAN IT BE?] |
| position    | tuple   | (0, 0)  |  A pair of x, y coordinates for the top left corner of the text. |
| bgcolor     | tuple   | None  |  A colour as a RGBA value. The first three values are Red, Green and Blue, and the final one is the Alpha (transparency). All values must be between 0 and 255. |
| video       | bool   | False |  [TO DO - CAN WE REMOVE THIS?] |

###### Example
```
cam.add_image_overlay("logo.gif")
```

This will add an overlay to [INSERT DESCRIPTION]

---