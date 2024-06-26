from picamera2 import Picamera2
# from picamera2.encoders import H264Encoder
# from picamera2.outputs import FfmpegOutput
from time import sleep, strftime, localtime
from .Preview import Preview

class Camera():

    def __init__(
        self
    ):

        """
        Creates a Camera object based on a Picamera2 object

        :param Picamera2 pc2:
            An internal Picamera2 object. This can be accessed by
            advanced users who want to use methods we have not
            wrapped from the Picamera2 library.
        """
        try:
            self.pc2 = Picamera2()
        except RuntimeError:
            print("Could not connect to the camera!")
            print("Please check all connections")
            exit()

        self.preview = Preview(self.pc2)
     

    # PROPERTIES
    # ----------------------------------
    @property
    def example(self):
        """
        An example
        """
        return self.eg

    @example.setter
    def example(self, value):
        self.eg = value

     # METHODS
    # ----------------------------------

    def flip_camera(self, direction):
        """
        Flip the image H or V
        """
        pass

    @property
    def brightness(self):
        """
        Set the brightness
        """
        pass

    @property
    def contrast(self):
        """
        Set the contrast
        """
        pass

    # Set exposure
    @property
    def exposure(self):
        """
        Set the exposure
        """
        pass

    # Set gain
    @property
    def gain(self):
        """
        Set the gain
        """
        pass

    # Set white balance
    @property
    def white_balance(self):
        """
        Set the white balance
        """
        pass

    # Add filter (add synonym method, e.g. set effect - [like sensehat library])
    def add_filter(self, filter):
        """
        Give choice of effects (greyscale, negative, sketch)
        """
        pass

    @property
    def annotation(self):
        pass
    @property
    def annotation_size(self):
        pass
    @property
    def annotation_color(self):
        pass
    @property
    def annotation_background_color(self):
        pass

    def set_annotation(self, text, size, colour, bgcolour,
                       on_preview=True, on_image=True):
        """
        Text overlays - **need to implement to take note of the current mode (preview or capture)**
        """
        pass

    # Image overlay
    def add_image_overlay(self, image):
        """
        Image overlays
        """
        pass

    # Take video and take still
    def take_video_and_still(self):
        """
        Take video and take a still at certain times?
        """
        pass

    # Take a picture
    def take_photo(self, filename=None):
        """
        Takes a jpeg image using the camera
        """
        if filename is None:
            # Set a default filename of example + current date/time
            filename = "example" + strftime("%Y%m%d%H%M%S", localtime()) + ".jpg"

        # Use inbuilt function for now
        self.pc2.start_and_capture_file(filename)

        # Useful to know what the file is called
        return filename

    # Synonym method for take a picture
    def capture_image(self):
        return self.take_photo()

    # Take a sequence
    def capture_burst(self, filename=None, num_images = 10, interval=0.01):
        """
        Take a series of <num_images> and save them as <filename> with auto number, also set the delay betweeen
        """
        pass

    # Synonym method
    def take_sequence(self):
        pass

    # Synonym methods for burst (from picamera1)
    def capture_sequence(self):
        return self.capture_burst()

    # def take_pictures(self):
    #     return self.capture_burst()

    # Take timelapse (optional video from result)
    def take_timelapse(self, filename=None, make_video=False):
        """
        Time-lapse mode (continual photo taking after <delay>)
        """
        pass

    # Record a video
    def record_video(self, filename=None, duration=5):
        """
        Record a video
        """
        if filename is None:
            # Set a default filename of example + current date/time
            filename = "example" + strftime("%Y%m%d%H%M%S", localtime()) + ".mp4"

        # Use basic inbuilt function
        self.pc2.start_and_record_video(filename, duration=duration)

        return filename

    # Record a video with option to take a photo
    def start_recording(self, filename=None):
        """
        Record a video with option to take a photo (9.3. Multiple outputs)
        """
        pass

    # Stop recording video
    def stop_recording(self):
        """
        Stop recording video
        """
        pass

