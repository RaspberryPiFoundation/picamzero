from picamzero import Camera

# ----------------------------------
# Test started state retained
# ----------------------------------


def test_started_flip(cam: Camera):
    cam.flip_camera(hflip=True, vflip=True)
    assert cam.pc2.started is True


def test_started_preview_start(cam: Camera):
    cam.start_preview()
    assert cam.pc2.started is True


def test_started_preview_stop(cam: Camera):
    cam.stop_preview()
    assert cam.pc2.started is True


def test_started_annotate(cam: Camera):
    cam.annotate("text")
    assert cam.pc2.started is True


def test_started_video_and_still(cam: Camera):
    cam.take_video_and_still("vstill", duration=6, still_interval=2)
    assert cam.pc2.started is True


def test_started_take_photo(cam: Camera):
    cam.take_photo("single_photo")
    assert cam.pc2.started is True


def test_started_capture_image(cam: Camera):
    cam.capture_image("synonym")
    assert cam.pc2.started is True


def test_started_capture_sequence(cam: Camera):
    cam.capture_sequence("sequence", num_images=3)
    assert cam.pc2.started is True


def test_started_record_video(cam: Camera):
    cam.record_video("video")
    assert cam.pc2.started is True


def test_started_start_recording(cam: Camera):
    cam.start_recording("videostart")
    assert cam.pc2.started is True


def test_started_stop_recording(cam: Camera):
    cam.stop_recording()
    assert cam.pc2.started is True
