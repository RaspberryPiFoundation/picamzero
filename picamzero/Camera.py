from picamera2 import Picamera2, Preview, MappedArray
from time import sleep, time
from .PicameraZeroException import PicameraZeroException
import cv2
import logging
import os
import math

from libcamera import Transform

logger = logging.getLogger(__name__)

# For dev only - suppress Libcamera and Picamera warnings
# os.environ["LIBCAMERA_LOG_LEVELS"] = "4"
# Picamera2.set_logging(level=Picamera2.ERROR)


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
        self.resolution = (800, 600)
        self.hflip = False
        self.vflip = False

        # Set up preview config
        self.preview_config = self._generate_config("PREVIEW")

        # Set the preview config by default
        self.pc2.preview_configuration = self.preview_config
        self._started_preview = False

        # Annotation
        self._text = None
        self._text_color = (255, 255, 255, 255)
        self._text_bgcolor = (0, 0, 0, 0)
        self._text_origin = (50, 50)
        self._text_font = cv2.FONT_HERSHEY_SIMPLEX
        self._text_scale = 3
        self._text_thickness = 3

    # ----------------------------------
    # PROPERTIES
    # ----------------------------------
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

    # ----------------------------------
    # METHODS
    # ----------------------------------

    def _generate_config(self, mode):
        """
        Generate a suitable config to use
        """
        temp_config = None
        if mode == "STILL":
            temp_config = self.pc2.create_still_configuration({"size": self.resolution})
        elif mode == "VIDEO":
            temp_config = self.pc2.create_video_configuration({"size": self.resolution})
        elif mode == "PREVIEW":
            temp_config = self.pc2.create_preview_configuration(
                {"size": self.resolution}
            )
        # Set any transforms
        temp_config["transform"] = Transform(hflip=self.hflip, vflip=self.vflip)

        return temp_config

    def flip_camera(self, vflip=False, hflip=False):
        """
        Flip the image horizontally or vertically
        """
        self.vflip = vflip
        self.hflip = hflip

        if self.pc2.started:
            self.pc2.stop()

        self.preview_config["transform"] = Transform(vflip=self.vflip, hflip=self.hflip)
        self.pc2.preview_configuration = self.preview_config

        # Restart
        self.pc2.start(show_preview=self._started_preview)

    def start_preview(self):
        """
        Show a preview of the camera
        """
        if not self._started_preview:
            try:
                self.pc2.start_preview(
                    Preview.QTGL,
                    width=self.resolution[0],
                    height=self.resolution[1],
                    transform=Transform(hflip=self.hflip, vflip=self.vflip),
                )
                self._started_preview = True
                self.pc2.start()
            except RuntimeError:
                logger.error("Preview couldn't start")

    def stop_preview(self):
        """
        Stop the preview
        """
        if self._started_preview:
            try:
                self.pc2.stop_preview()  # Pete to change to close() later?...
                self._started_preview = False
            except RuntimeError:
                logger.error("Couldn't stop preview")

    # Add filter (add synonym method, e.g. set effect - [like sensehat library])
    def add_filter(self, filter):
        """
        Give choice of effects (greyscale, negative, sketch)
        """
        pass

    def annotate(
        self,
        text="Default Text",
        text_color=(255, 255, 255, 255),
        text_origin=(50, 50),
        text_scale=3,
        text_thickness=3,
        video=False,
    ):
        """
        Set a text overlay on the preview and on images
        TODO: video, text bgcolor, font?
        """
        self._text = text
        self._text_color = text_color
        self._text_origin = text_origin
        self._text_scale = text_scale
        self._text_thickness = text_thickness

        def annotation_callback(request):
            """
            Annotate before taking a photo etc.
            """

            with MappedArray(request, "main") as m:
                cv2.putText(
                    m.array,
                    self._text,
                    self._text_origin,
                    self._text_font,
                    self._text_scale,
                    self._text_color,
                    self._text_thickness,
                )

        # Add the annotation as a callback when any pics are taken
        self.pc2.pre_callback = annotation_callback

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

        # Start the video
        self.pc2.start_and_record_video(
            f"{filename}.mp4",
            config=self._generate_config("VIDEO"),
            show_preview=True,
        )

        start_time = time()

        still_times = [
            i * still_interval
            for i in range(1, math.ceil(duration / still_interval) + 1)
        ]
        # Remove any times that are greater than the duration
        # (they need to be generated otherwise for durations that are
        # exactly divisible the final still isn't included)
        result = list(filter(lambda x: x <= duration, still_times))

        for i, still_time in enumerate(result):
            sleep(max(0, still_time - (time() - start_time)))
            current_time = time() - start_time
            print(f"Current time: {current_time}")
            request = self.pc2.capture_request()
            request.save("main", f"{filename}-{i}.jpg")
            request.release()

        remaining_time = duration - (time() - start_time)

        if remaining_time > 0:
            sleep(remaining_time)

        self.pc2.stop_recording()

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

        still_config = self._generate_config("STILL")
        if self.pc2.started:
            self.pc2.stop()
        self.pc2.still_configuration = still_config
        self.pc2.start()

        # Capture the image
        self.pc2.start_and_capture_file(
            name=filename,
            show_preview=self._started_preview,
        )

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
        prev_config = self._generate_config("PREVIEW")
        seq_config = self._generate_config("STILL")
        # Auto starts
        self.pc2.start_and_capture_files(
            filename,
            num_files=num_images,
            delay=interval,
            capture_mode=seq_config,
            preview_mode=prev_config,
        )
        print(f"-----------Config: {self.pc2.still_configuration}")

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
        self._generate_config("VIDEO")
        # Auto starts
        self.pc2.start_and_record_video(filename, duration=duration)

        return filename

    # Record a video with option to take a photo
    def start_recording(self, filename=None, preview=False):
        """
        Record a video of undefined length
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

        # Update the preview variable as the preview may be started
        self._preview_started = preview

        self.pc2.start_and_record_video(
            filename, config=self._generate_config("VIDEO"), show_preview=preview
        )

    # Stop recording video
    def stop_recording(self):
        """
        Stop recording video
        """
        self.pc2.stop_recording()
