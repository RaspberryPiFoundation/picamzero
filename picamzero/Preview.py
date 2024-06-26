from picamera2 import Preview as PC2Preview
class Preview():

    def __init__(self, pc2):
        self.pc2 = pc2
        self.pconfig = pc2.create_preview_configuration()
        self.pc2.configure(self.pconfig)

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
        except RuntimeError:
            print("Preview couldn't start")

    # Stop
    def stop(self):
        """
        Stop the preview
        """
        try:
            self.pc2.stop_preview()
        except RuntimeError:
            print("Couldn't stop preview")

    @property
    def annotation(self):
        pass
    """
    Other annotation properties...
    """

    # Text overlay
    def add_text_overlay(self, text):
        """
        Text overlays
        """
        pass

    # Image overlay
    def add_image_overlay(self, image):
        """
        Image overlays
        """
        pass


