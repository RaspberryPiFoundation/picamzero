# Methods

All programs which use picamzero first require you to create a camera object, which is as simple as these two lines of code:

```
from picamzero import Camera
cam = Camera()
```

The `Camera` object we have created in the example is called `cam`, but you can call yours something different if you prefer.

You can call **methods** to perform particular tasks with your camera.

### Photo methods

#### capture_image()

Takes a photograph using the camera and saves it as a `.jpg` image. 
Returns the filename of the image.

```
capture_image(
    filename: string
) -> string
```

| Parameter   | Type    | Default  | Description | 
| ----------- | ------- | -------- | ----------- | 
| filename    | string  | None     | A file name for a .jpg image. This can also be a file path. | 

###### Example
```
cam.capture_image("mypic.jpg")
```

This method can also be called as ```take_photo()```.

```
cam.take_photo("mypic.jpg")
```


#### capture_sequence()

Take a series of `num_images` with a gap of `interval` between each one, and save them as
`filename` with an auto-number. Optionally, create a video using all of the images.
Returns **TODO SORT THIS OUT**


```
capture_sequence(
    filename: string,
    num_images: int, 
    interval: float, 
    make_video: bool
) -> string
```

| Parameter   | Type    | Default  | Description | 
| ----------- | ------- | -------- | ----------- | 
| filename    | string  | None     | A file name for a .jpg image. This can also be a file path. | 
| num_images  | int     | 10       | How many images to take.| 
| interval    | float   | 0.01     | How long to wait in between each image, in seconds. | 
| make_video  | bool    | False    | Whether to make a `.mp4` video of the images. | 


###### Example
```
cam.capture_sequence("mysequence.jpg", 12, 0.5, True)
```
