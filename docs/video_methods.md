# Video methods

---
## Record a video

- Records a video for a specified `duration`, given in seconds. If no duration is specified, the video will record for 5 seconds.
- **Returns** the `filename` of the video that was recorded.

```python
record_video(
    filename: str | Path,
    duration: int
) -> str
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str or Path     | None     | Yes | A filename for a `.mp4` video. This can also be a path to a file as either a string or a `Path` object. |
| duration    | int     | `5`       | No | The length of time to record, in seconds. |

##### Example
A 10 second video called `test_video.mp4` will be recorded and saved into the same folder as the Python script.

```python
cam.record_video("test_video.mp4", 10)
```

This method can also be called as ```take_video()``` and will behave in exactly the same way.

```python
cam.take_video("test_video.mp4", 10)
```

---

## Start recording

- Start recording a video. Use this method if you want to record for an unknown length of time.

```python
start_recording(
    filename: str | Path,
    preview: bool,
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str or Path     | None     | Yes | A file name for a `.mp4` video. This can also be a path to a file as either a string or a `Path` object. |
| show_preview   | bool     | `False`     | No | Whether to show a preview. |

##### Example

```python
cam.start_recording("new_video.mp4")
```

This code will start recording a video called `new_video.mp4`. The video will not finish recording until `stop_recording()` is called.

---

## Stop recording

- Stops a recording that is currently in progress.

```python
stop_recording() -> None
```

##### Example

```python
# Stops a previously started recording
cam.stop_recording()
```

---

## Record a video and take photos

- Record a video for a fixed `duration`, and while the video is running also take a photo at a specified `still_interval`.

```python
take_video_and_still(
    filename: str | Path,
    duration: int,
    still_interval: int
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename       | str or Path     | None    | Yes | A file name for a `.mp4` video.  This can also be a path to a file as either a string or a `Path` object. |
| duration       | int     | 20         | No | The length of time to record, in seconds. |
| still_interval  | int  | 4  | No | How frequently to take a photo, in seconds. If the duration is not exactly divisible by the interval specified, the method will ignore any remaining time. The first image will be taken after waiting for the specified interval. |

It may not be possible for the Raspberry Pi to capture images at the exact interval specified, particularly if the interval value is small.

##### Example

```python
cam.take_video_and_still("example.mp4", duration=16, still_interval=3)
```

This will record a 16 second video called `example.mp4`. It will also take a still image at 3, 6, 9, 12 and 15 seconds and save them as `example-1.jpg`, `example-2.jpg` etc.

