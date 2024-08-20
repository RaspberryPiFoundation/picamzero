# Video methods

---
## Record a video
#### `record_video`

Records a video for a specified `duration`, given in seconds. If no duration is specified, the video will record for 5 seconds. Returns the `filename` of the video that was recorded.

```
record_video(
    filename: str,
    duration: int
) -> str
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str     | None     | Yes | A file name for a `.mp4` video. This can also be a path to a file. |
| duration    | str     | `5`       | No | The length of time to record, in seconds. |

##### Example
```
cam.record_video("test_video.mp4", 10)
```

A 10 second video will be recorded and saved into the same folder as the Python script, unless a path is specified.

---

## Start recording
#### `start_recording`

Start recording a video. Use this method if you want to record for an unknown length of time.

```
start_recording(
    filename: str,
    preview: bool,
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename    | str     | None     | Yes | A file name for a `.mp4` video. This can also be a path to a file. |
| show_preview   | bool     | `False`     | No | Whether to show a preview. |




##### Example
```
cam.start_recording("new_video.mp4")
```

This code will start recording a video called `new_video.mp4`. The video will not finish recording until `stop_recording()` is called.

---

## Stop recording
#### `stop_recording`

Stops a recording that is currently in progress. This method has no parameters or return value.

```
stop_recording() -> None
```

##### Example
```
# Stops a previously started recording
cam.stop_recording()
```

---

## Record a video and take photos
#### `take_video_and_still`

Record a video for a fixed `duration`, and while the video is running also take a photo at a specified `still_interval`.

```
take_video_and_still(
    filename: str,
    duration: int,
    still_interval: int
) -> None
```

| Parameter   | Data type    | Default  | Compulsory? | Description |
| ----------- | ------- | -------- | -------- | ----------- |
| filename       | str     | None    | Yes | A file name for a `.mp4` video. This can also be a path to a file. |
| duration       | int     | 20         | No | The length of time to record, in seconds. |
| still_interval  | int  | 4  | No | How frequently to take a photo, in seconds. If the duration is not exactly divisible by the interval specified, the method will ignore any remaining time. |


##### Example
```
cam.take_video_and_still("example.mp4", duration=16, still_interval=3)
```

This will record a 16 second video called `example.mp4`. It will also take a still image at 3, 6, 9, 12 and 15 seconds and save them as `example-1.jpg`, `example-2.jpg` etc.

---