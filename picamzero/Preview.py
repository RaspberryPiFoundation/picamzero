from picamera2 import Preview as PC2Preview
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Preview:
    def __init__(self, pc2):
        self.pc2 = pc2
        self.config = pc2.create_preview_configuration()
        self.pc2.configure(self.config)

        self._annotation = None
        self._text_color = (255, 255, 255, 255)
        self._text_origin = (0, 30)
        self._text_font = cv2.FONT_HERSHEY_SIMPLEX
        self._overlay_size = (640, 480)
        self._started = False

    # METHODS
    # ----------------------------------

    def start(self, width=800, height=600):
        """
        Show a preview of the camera
        """
        if not self._started:
            try:
                self.pc2.start_preview(PC2Preview.QTGL, width=width, height=height)
                self.pc2.start()
                self._started = True
            except RuntimeError:
                logger.error("Preview couldn't start")

    def stop(self):
        """
        Stop the preview
        """
        if self._started:
            try:
                self.pc2.stop_preview()
                self._started = False
            except RuntimeError:
                logger.error("Couldn't stop preview")

    @property
    def annotation(self):
        """
        Return the current annotation
        """
        return self._annotation

    @annotation.setter
    def annotation(self, text):
        self._annotation = text
        overlay = np.zeros(
            (self._overlay_size[0], self._overlay_size[1], 4), dtype=np.uint8
        )
        cv2.putText(
            overlay,
            self._annotation,
            self._text_origin,
            self._text_font,
            1,  # scale
            self._text_color,
            2,  # thickness
        )
        try:
            self.pc2.set_overlay(overlay)
        except AttributeError:
            if not self._started:
                logger.error("Start the preview before adding an annotation")
            else:
                logger.error("Could not add overlay")

    # Image overlay
    def add_image_overlay(self, image):
        """
        Image overlays
        """
        pass
