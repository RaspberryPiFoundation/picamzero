from picamera2 import Picamera2, MappedArray

# from picamera2.encoders import H264Encoder
# from picamera2.outputs import FfmpegOutput
from time import sleep, strftime, localtime
from .PicameraZeroException import PicameraZeroException
import cv2, logging, os
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

        self.resolution = (2592, 1944)

        capture_config = self.pc2.create_still_configuration({"size": self.resolution})
        preview_config = self.pc2.create_preview_configuration({"size": self.resolution})

        # Set the current config as the preview config
        self.pc2.configure(preview_config)
        self._started = False
        self._annotation = None


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

    def start_preview(self):
        """
        Show a preview of the camera
        """
        if not self._started:
            try:
                self.pc2.start(show_preview=True)  # Can we mix and match?
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

    '''
    def set_annotation(self, request, text="Default Text"):
        """
        Text overlays - **need to implement to take note of the
        current mode (preview or capture)**
        """
        self.text_color = (255, 255, 255, 255)
        self.bg_color = (0, 0, 0, 0)
        self.origin = (0, 30)
        self.text_font = cv2.FONT_HERSHEY_SIMPLEX
        self.scale = 2
        self.thickness = 2
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, text , self.origin, self.text_font, self.scale, self.text_color, self.thickness)


    @property
    def annotation(self):
        """
        Return the current annotation
        """
        return self._annotation

    ### I think this is going to need implementing in each capture method - as a Boolean option?
    ### Leaving this here for now and we can put our heads together in the morning!
    @annotation.setter
    def annotation(self, text):
        self.pc2.pre_callback = set_annotation
        self._annotation = text
        overlay = np.zeros((self._overlay_size[0], self._overlay_size[1], 4), dtype=np.uint8)
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
                logger.error("Start the preview before adding an annotation")
            else:
                logger.error("Could not add overlay")

    '''

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
    def capture_image(self, filename):
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
            # Check if the filename already has the ".jpg" extension
            if not filename.lower().endswith(".jpg"):
                filename = filename + "-{:d}" + ".jpg"
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

        # Useful to know what the file is called
        return filename

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

