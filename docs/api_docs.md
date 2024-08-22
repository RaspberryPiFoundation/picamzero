# API docs

API docs or "Application Programming Interface Documentation" is a fancy name for a list of all the things a piece of software can do, and how to use them.

The docs list all of the **methods** available.


## Method signature

You will see a block of code like this:

```python
record_video(
    filename: str,
    duration: int
) -> str
```

This tells you:

- the name of the method (`record_video`)
- the parameters it can accept (`filename` and `duration`)
- the type of data accepted by each parameter
    - `filename` needs a `str` (string)
    - `duration` needs an `int` (integer)
- what the method returns (`-> str`)

## Parameter list
This is a list of all parameters, their data type, their default value, whether it is compulsory for you to provide a value and a description of what each one does.

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str     | None     | Yes | A file name for a `.mp4` video. This can also be a path to a file. |
| duration    | int     | `5`       | No | The length of time to record, in seconds. |

## Example

An example of how to call the method is provided.

```python
cam.record_video("test_video.mp4", 10)
```

The example will always assume you have already imported the `picamzero` library, and created a camera. The full code to run this example would be:

```python
from picamzero import Camera
cam = Camera()
cam.record_video("test_video.mp4", 10)
```

Now that you know how to read API docs, have a look at the [photo methods](photo_methods.md), [video methods](video_methods.md) and [preview methods](preview_methods.md).