# Recipes

We have put together some example programs for common things people would like to do with their camera.

## Start a preview and take a photo

The preview will display for 2 seconds, and then the camera will take a photo called `test.jpg`.

```python
--8<-- "docs/recipes/preview_and_photo.py"
```

## Start a preview and record a video

The preview will display while the camera records a 5 second video called `test.mp4`.

```python
--8<-- "docs/recipes/preview_and_video.py"
```

## Take a timelapse sequence

The preview will display and the camera will take 5 photos with a 1 second interval between each photo.

The images will automatically be numbered `sequence-0.jpg`, `sequence-1.jpg` etc.

```python
--8<-- "docs/recipes/timelapse.py"
```

## Take a black and white image

The camera will take one black and white image. (No preview is started in this example).

```python
--8<-- "docs/recipes/bnw.py"
```
