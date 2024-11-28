# Preview methods

---
## Start the preview

- Starts a preview window so that you can see what the camera sees.

```python
start_preview() -> None
```
##### Example
```python
cam.start_preview()
```

Note that if you start a preview but then the program ends, there will not be enough time to see the preview window. If you only want to see a preview, use python's built in `sleep()` method once you have started the preview to keep it open.

```python
from picamzero import Camera
from time import sleep

cam = Camera()
cam.start_preview()
# Keep the preview window open for 5 seconds
sleep(5)

```

---

## Stop the preview

- Stops a currently running preview.

```python
stop_preview() -> None
```

##### Example
```python
cam.stop_preview()
```

---
