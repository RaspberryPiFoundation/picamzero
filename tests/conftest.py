# -------------------------------------------------------------
# This is not production code but I am losing the will to live
# Provide the path to the module so that the tests can run
import os
import sys

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

    camera = Camera()
    yield camera
    camera.pc2.close()
