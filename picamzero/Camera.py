from picamera2 import Picamera2

# from picamera2 import MappedArray

# from picamera2.encoders import H264Encoder
# from picamera2.outputs import FfmpegOutput
from time import sleep

# from time import strftime, localtime
from .PicameraZeroException import PicameraZeroException
import cv2
import logging
import os

import numpy as np
from libcamera import Transform

logger = logging.getLogger(__name__)


class Camera:
    def __init__(self):
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
            logger.error("Could not connect to the camera!")
            logger.error("Please check all connections")
            exit()

        # Camera
        self.resolution = (2592, 1944)
        self.hflip = False
        self.vflip = False

        # Set the current config as the preview config
        self.preview_config = self.pc2.create_preview_configuration(
            {"size": self.resolution}
        )
        self.pc2.configure(self.preview_config)
        self._started = False

        # Annotation
        self._text = None
        self._text_color = (255, 255, 255, 255)
        self._text_bgcolor = (0, 0, 0, 0)
        self._text_origin = (30, 30)
        self._text_font = cv2.FONT_HERSHEY_SIMPLEX
        self._text_scale = 5
        self._text_thickness = 5

    # METHODS
    # ----------------------------------

    def flip_camera(self, vflip=False, hflip=False):
        """
        Flip the image horizontally or vertically
        """
        self.vflip = vflip
        self.hflip = hflip
        self.preview_config["transform"] = Transform(vflip=self.vflip, hflip=self.hflip)

    def start_preview(self):
        """
        Show a preview of the camera
        """
        if not self._started:
            try:
                self.pc2.configure(self.preview_config)
                self.pc2.start(show_preview=True)
                self._started = True
            except RuntimeError:
                logger.error("Preview couldn't start")

    def stop_preview(self):
        """
        Stop the preview
        """
        if self._started:
            try:
                self.pc2.stop_preview()  # Pete to change to close() later?...
                self._started = False
            except RuntimeError:
                logger.error("Couldn't stop preview")

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

    def annotate(self, text="Default Text", video=False):
        """
        Text overlays - **need to implement to take note of the
        current mode (preview or capture)**
        """
        self._text = text
        overlay = np.zeros((self.resolution[0], self.resolution[1], 4), dtype=np.uint8)
        cv2.putText(
            overlay,
            self._text,
            self._text_origin,
            self._text_font,
            self._text_scale,
            self._text_color,
            self._text_thickness,
        )

        if not self._started:
            logger.error("Start the preview before adding an annotation")
            raise PicameraZeroException(
                "Cannot set annotation", "Start the preview before adding an annotation"
            )
            exit()

        try:
            self.pc2.set_overlay(overlay)
        except AttributeError:
            logger.error("Could not add overlay")

        """
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, text, self.origin, self.text_font, self.scale,
            self.text_color, self.thickness)

        """

    # Image overlay
    def add_image_overlay(self, image):
        """
        Image overlays
        """
        pass

    # Take video and take still
    def take_video_and_still(self, filename=None, duration=20, still_interval=4):
        """
        Take video for <duration> and take a still every <interval> seconds?
        """

        if filename is None:
            raise PicameraZeroException(
                "Filename not specified",
                hint="Check that you specified a name for the video",
            )
            exit()

        # Use inbuilt function for now
        if duration % still_interval == 0:
            for i in range(int(duration / still_interval)):
                self.pc2.start_and_record_video(f"{filename}.mp4")
                sleep(still_interval)
                request = self.pc2.capture_request()
                # Does this result in a flipped image if set above?
                request.save("main", f"{filename}-{str(i)}.jpg")
                request.release()

            self.pc2.stop_recording()
        else:
            logger.error("Duration must be equally divisible by interval")
            """
            Can also handle this differently using different division?
            """

    # Take a picture
    def take_photo(self, filename=None):
        """
        Takes a jpeg image using the camera
        """
        if filename is None:
            raise PicameraZeroException(
                "Filename not specified",
                hint="Check that you specified a name for the photo",
            )
            exit()

        file_root, file_ext = os.path.splitext(filename)

        # Check if the extension is valid, if not replace it with ".jpg"
        if file_ext.lower() != ".jpg":
            filename = file_root + ".jpg"

        # Use inbuilt function for now
        self.pc2.start_and_capture_file(filename)

        # Useful to know what the file is called
        return filename

    # Synonym method for take a picture
    def capture_image(self, filename=None):
        return self.take_photo(filename)

    # Take a sequence
    def capture_sequence(
        self, filename=None, num_images=10, interval=0.01, make_video=False
    ):
        """
        Take a series of <num_images> and save them as
        <filename> with auto-number, also set the interval between
        """
        if filename is None:
            raise PicameraZeroException(
                "Filename not specified",
                hint="Check that you specified a filename for the burst",
            )
            exit()
        else:
            file_root, file_ext = os.path.splitext(filename)
            # Check if the filename already has the ".jpg" extension
            if file_ext.lower() != ".jpg":
                filename = file_root + "-{:d}" + ".jpg"
            else:
                filename = filename[:-4] + "-{:d}.jpg"

        # Use inbuilt function for now
        self.pc2.start_and_capture_files(filename, num_files=num_images, delay=interval)

        if make_video:
            try:
                # Extract base name from filename pattern
                base_name = filename[:-8]  # Remove the "-{:d}.jpg" part
                video_name = base_name + "timelapse.mp4"
                frame = cv2.imread(filename.format(0))
                height, width, layers = frame.shape

                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video = cv2.VideoWriter(
                    video_name, fourcc, 1 / interval, (width, height)
                )

                for i in range(num_images):
                    img_path = filename.format(i)
                    if os.path.exists(img_path):
                        video.write(cv2.imread(img_path))
                    else:
                        logger.warning(
                            f"{img_path} does not exist and will be skipped."
                        )

                video.release()
                return video_name
            except Exception as e:
                return f"Error creating video: {e}"

    # Record a video
    def record_video(self, filename=None, duration=5):
        """
        Record a video
        """
        if filename is None:
            raise PicameraZeroException(
                "Filename not specified",
                hint="Check that you specified a name for the video",
            )
            exit()
        elif not filename.lower().endswith(".mp4"):
            # Check if the filename already has the ".mp4" extension
            filename = filename + ".mp4"

        # Use basic inbuilt function
        self.pc2.start_and_record_video(filename, duration=duration)

        return filename

    # Record a video with option to take a photo
    def start_recording(self, filename):
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
