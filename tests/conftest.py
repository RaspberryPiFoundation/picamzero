# -------------------------------------------------------------
# Provide the path to the module so that the tests can run
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# --------------------------------------------------------------


@pytest.fixture(autouse=True)
def cwd(tmpdir, monkeypatch):
    """
    This fixture changes the current working directory before
    each test in this file to to a temporary directory so that
    image / video clean up is taken care of by the OS.
    """
    monkeypatch.chdir(tmpdir)


# Returns a camera to use in tests
@pytest.fixture
def cam():
    from picamzero import Camera

    Camera._instance_count = 0

    camera = Camera()

    # Override picamera2's start_preview method to ensure
    # that the NULL preview is always used during testing
    # by saving a reference to the original function and
    # calling it with preview always set to False
    original_start_preview_function = camera.pc2.start_preview

    def overridden_start_preview(self, preview=False, **kwargs):
        preview = False
        return original_start_preview_function(preview, **kwargs)

    camera.pc2.start_preview = types.MethodType(overridden_start_preview, camera.pc2)

    try:
        yield camera
    finally:
        camera.pc2.close()
