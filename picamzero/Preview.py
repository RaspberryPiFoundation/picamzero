from picamera2 import Preview as PC2Preview
import cv2
import numpy as np

class Preview():

    def __init__(self, pc2):
        self.pc2 = pc2
        self.config = pc2.create_preview_configuration()
        self.pc2.configure(self.config)
        
        self._annotation = None
        self._text_color = (255, 255, 255, 255)
        self._text_origin = (0, 30)
        self._text_font = cv2.FONT_HERSHEY_SIMPLEX
        
        self._started = False


    # METHODS
    # ----------------------------------

	# Start
    def start(self, width=800, height=600):
        """
        Show a preview of the camera
        """
        try:
            self.pc2.start_preview(PC2Preview.QTGL, width=width, height=height)
            self.pc2.start()
            self._started = True
        except RuntimeError:
            print("Preview couldn't start")

    # Stop
    def stop(self):
        """
        Stop the preview
        """
        try:
            self.pc2.stop_preview()
            self._started = False
        except RuntimeError:
            print("Couldn't stop preview")

    @property
    def annotation(self):
        """
        Return the current annotation
        """
        return self._annotation
    
    @annotation.setter
    def annotation(self, text):
        self._annotation = text
        overlay = np.zeros((640, 480, 4), dtype=np.uint8)
        cv2.putText(
                overlay,
                self._annotation,
                self._text_origin,
                self._text_font,
                1, # scale
                self._text_color,
                2 # thickness
        )
        try:
            self.pc2.set_overlay(overlay)
        except AttributeError:
            if not self._started:
                print("Start the preview before adding an annotation")
            else:
                print("Could not add overlay")


    # Image overlay
    def add_image_overlay(self, image):
        """
        Image overlays
        """
        pass


