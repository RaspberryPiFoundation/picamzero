from picamera2 import Picamera2, MappedArray
from .PicameraZeroException import PicameraZeroException
from time import sleep, time
from . import utilities as utils
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
        self.hflip = False
        self.vflip = False

        self.preview_config = self._generate_config("PREVIEW")

        # Set the preview config by default
        self.pc2.preview_configuration = self.preview_config
        self._started_preview = False

        # Annotation
        self._text = None
        self._text_properties = {
            "font": utils.font_dict()["simplex"][0],
            "color": (255, 255, 255, 255),
            "origin": (50, 50),
            "scale": 3,
            "thickness": 3,
            "bgcolor": None,
            "position": (0, 0),
        }

        self.pc2.start()

    # ----------------------------------
    # PROPERTIES
    # ----------------------------------

    # Check that the value given for a control is allowed
    def _check_control_in_range(self, name: str, value: float | int) -> bool:
        try:
            minvalue, maxvalue, defaultvalue = self.pc2.camera_controls[name]
        except Exception as e:
            raise PicameraZeroException(
                f"The control {e} doesn't exist", "Check for spelling errors?"
            )

        if value > maxvalue or value < minvalue:
            raise PicameraZeroException(
                f"Invalid {name.lower()} value",
                f"{name} must be between {minvalue} and {maxvalue}",
            )
        return True

    @property
    def preview_size(self):
        return self.pc2.preview.configuration.size

    @preview_size.setter
    def preview_size(self, size):
        if isinstance(size, tuple) and len(size) == 2:
            h, w = size
            if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
                max_h, max_w = self.pc2.sensor_resolution
                if h > max_h or w > max_w:
                    logger.error(
                        """Warning: The specified size exceeds the camera's
                            maximum allowed dimensions.
                            The size has been adjusted to fit."""
                    )
                h = min(h, max_h)
                w = min(w, max_w)

                self.pc2.preview.configuration.size = (h, w)
            else:
                raise PicameraZeroException(
                    "The height and width of the preview must be positive integers.",
                    "Example: (640, 480)",
                )
        else:
            raise PicameraZeroException(
                """The size of the preview must be two positive integers,
                separated by a comma and in brackets.""",
                "Example: (640, 480).",
            )

    @property
    def still_size(self):
        return self.pc2.still.configuration.size

    @still_size.setter
    def still_size(self, size):
        if isinstance(size, tuple) and len(size) == 2:
            h, w = size
            if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
                max_h, max_w = self.pc2.sensor_resolution
                if h > max_h or w > max_w:
                    logger.error(
                        """Warning: The specified size exceeds the camera's
                            maximum allowed dimensions.
                            The size has been adjusted to fit."""
                    )
                h = min(h, max_h)
                w = min(w, max_w)

                self.pc2.still.configuration.size = (h, w)
            else:
                raise PicameraZeroException(
                    "The height and width of the image must be positive integers.",
                    "Example: (640, 480)",
                )
        else:
            raise PicameraZeroException(
                """The size of the image must be two positive integers,
                separated by a comma and in brackets.""",
                "Example: (3280, 2464).",
            )

    @property
    def video_size(self):
        return self.pc2.video.configuration.size

    @video_size.setter
    def video_size(self, size):
        if isinstance(size, tuple) and len(size) == 2:
            h, w = size
            if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
                max_h, max_w = self.pc2.sensor_resolution
                if h > max_h or w > max_w:
                    logger.error(
                        """Warning: The specified size exceeds the camera's
                            maximum allowed dimensions.
                            The size has been adjusted to fit."""
                    )
                h = min(h, max_h)
                w = min(w, max_w)

                self.pc2.video.configuration.size = (h, w)
            else:
                raise PicameraZeroException(
                    "The height and width of the video must be positive integers.",
                    "Example: (1920, 1080)",
                )
        else:
            raise PicameraZeroException(
                """The size of the video must be two positive integers,
                separated by a comma and in brackets.""",
                "Example: (640, 480).",
            )

    # Brightness
    @property
    def brightness(self) -> float:
        """
        Get the brightness

        :return float:
            Brightness value between -1.0 and 1.0
        """
        return self.pc2.controls.Brightness

    @brightness.setter
    def brightness(self, bvalue: float):
        """
        Set the brightness

        :param float bvalue:
            Floating point number between -1.0 and 1.0
        """
        if self._check_control_in_range("Brightness", bvalue):
            self.pc2.controls.Brightness = bvalue

    # Contrast
    @property
    def contrast(self) -> float:
        """
        Get the contrast

        :return float:
            Contrast value between 0.0 and 32.0
        """
        return self.pc2.controls.Contrast

    @contrast.setter
    def contrast(self, cvalue: float):
        """
        Set the contrast

        :param float cvalue:
            Floating point number between 0.0 and 32.0
            Normal value is 1.0
        """
        if self._check_control_in_range("Contrast", cvalue):
            self.pc2.controls.Contrast = cvalue

    # Exposure
    @property
    def exposure(self) -> int:
        """
        Get the exposure

        :returns int:
            Exposure value (max and min depend on mode)
        """
        return self.pc2.controls.ExposureTime

    @exposure.setter
    def exposure(self, etime: int):
        """
        Set the exposure

        :param int etime:
            The exposure time (max and min depend on mode)
        """
        if self._check_control_in_range("ExposureTime", etime):
            self.pc2.controls.ExposureTime = etime

    # Gain
    @property
    def gain(self) -> float:
        """
        Get the gain

        :returns float:
            Gain value (max and min depend on mode)
        """
        return self.pc2.controls.AnalogueGain

    @gain.setter
    def gain(self, gvalue: float):
        """
        Set the analogue gain

        :param float gvalue:
            The analogue gain (max and min depend on mode)
        """
        if self._check_control_in_range("AnalogueGain", gvalue):
            self.pc2.controls.AnalogueGain = gvalue

    # White balance
    @property
    def white_balance(self) -> str:
        """
        Get the white balance mode

        :return str:
            The selected white balance mode as a string
        """
        return utils.possible_controls(reverse_kv=True)[self.pc2.controls.AwbMode]

    @white_balance.setter
    def white_balance(self, wbmode: str):
        """
        Set the white balance mode

        :param str wbmode:
            A white balance mode from the allowed list
            (at present, Custom is not allowed)
        """

        if wbmode.lower() not in utils.possible_controls():
            if wbmode.lower() == "custom":
                raise PicameraZeroException(
                    "Custom white balance is not supported yet",
                    "White balance can be "
                    + ", ".join(utils.possible_controls().keys()),
                )
            else:
                raise PicameraZeroException(
                    "Invalid white balance mode",
                    "White balance can be "
                    + ", ".join(utils.possible_controls().keys()),
                )
        else:
            set_awb_mode = {
                "AwbEnable": 1,
                "AwbMode": utils.possible_controls()[wbmode.lower()],
            }
            self.pc2.set_controls(set_awb_mode)

    # ----------------------------------
    # METHODS
    # ----------------------------------

    def _generate_config(self, mode):
        """
        Helper method: Generate a suitable config to use
        """
        temp_config = None
        if mode == "STILL":
            temp_config = self.pc2.create_still_configuration(
                {"size": self.pc2.sensor_resolution},
                transform=Transform(hflip=self.hflip, vflip=self.vflip),
            )
        elif mode == "VIDEO":
            temp_config = self.pc2.create_video_configuration(
                {"size": self.pc2.sensor_resolution},
                transform=Transform(hflip=self.hflip, vflip=self.vflip),
            )

        elif mode == "PREVIEW":
            temp_config = self.pc2.create_preview_configuration(
                {"size": self.pc2.sensor_resolution},
                transform=Transform(hflip=self.hflip, vflip=self.vflip),
            )

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
        self.pc2.start()

    def start_preview(self):
        """
        Show a preview of the camera
        """

        # At this point, null preview is probably running still...
        # (but that is OK!)
        self.pc2.stop()

        try:
            config = self.pc2.create_preview_configuration(
                {"size": self.pc2.sensor_resolution},
                transform=Transform(hflip=self.hflip, vflip=self.vflip),
            )
            self.pc2.configure(config)
            self.pc2.start()
            self.pc2.stop_preview()  # Stop null preview
            self.pc2.start_preview(True)  # Start the not null preview

        except RuntimeError as e:
            logger.error(f"Preview couldn't start: {e}")

    def stop_preview(self):
        """
        Stop the preview
        """
        if self.pc2._preview:
            try:
                self.pc2.stop_preview()

            except RuntimeError:
                logger.error("Couldn't stop preview")

    # Add filter (add synonym method, e.g. set effect - [like sensehat library])
    def add_filter(self, effect):
        """
        Give choice of effects (greyscale, negative, sketch)
        """
        pass

    def annotate(
        self,
        text="Default Text",
        font="simplex",
        color=(255, 255, 255, 255),
        origin=(50, 50),
        scale=3,
        thickness=3,
        position=(0, 0),
        bgcolor=None,
        video=False,
    ):
        """
        Set a text overlay on the preview and on images
        TODO: video?
        """
        self._text = text

        font = utils.check_font_in_dict(font)

        self._text_properties = {
            "font": font,
            "color": color,
            "origin": origin,
            "scale": scale,
            "thickness": thickness,
            "bgcolor": bgcolor,
            "position": position,
        }

        def annotation_callback(request):
            """
            Annotate before taking a photo etc.
            """
            text_prop = self._text_properties
            # Create the background
            if text_prop["bgcolor"] is not None:
                x, y = text_prop["position"]
            text_size, _ = cv2.getTextSize(
                text, text_prop["font"], text_prop["scale"], text_prop["thickness"]
            )
            text_w, text_h = text_size

            with MappedArray(request, "main") as m:
                if text_prop["bgcolor"] is not None:
                    cv2.rectangle(
                        m.array,
                        text_prop["position"],
                        (x + text_w, y + text_h),
                        text_prop["bgcolor"],
                        -1,
                    )
                cv2.putText(
                    m.array,
                    self._text,
                    (x, y + text_h + text_prop["scale"] - 4),
                    text_prop["font"],
                    text_prop["scale"],
                    text_prop["color"],
                    text_prop["thickness"],
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
        # Format the filename so that it has no extension
        filename = utils.format_filename(filename, ext="")

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
        filename = utils.format_filename(filename, ".jpg")

        still_config = self._generate_config("STILL")
        if self.pc2.started:
            self.pc2.stop()
        self.pc2.still_configuration = still_config
        self.pc2.start()

        # Capture the image
        self.pc2.start_and_capture_file(name=filename)

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
        # Format the filename
        img_filename = utils.format_filename(filename, ext="-{:d}.jpg")

        # Use inbuilt function for now
        prev_config = self._generate_config("PREVIEW")
        seq_config = self._generate_config("STILL")
        # Auto starts
        self.pc2.start_and_capture_files(
            img_filename,
            num_files=num_images,
            delay=interval,
            capture_mode=seq_config,
            preview_mode=prev_config,
        )

        if make_video:
            try:
                video_name = utils.format_filename(filename, ext="-timelapse.mp4")
                frame = cv2.imread(img_filename.format(0))
                height, width, layers = frame.shape

                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video = cv2.VideoWriter(
                    video_name, fourcc, 1 / interval, (width, height)
                )

                for i in range(num_images):
                    img_path = img_filename.format(i)
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
        filename = utils.format_filename(filename, ".mp4")
        self.pc2.start_and_record_video(
            filename, config=self._generate_config("VIDEO"), duration=duration
        )

        return filename

    # Record a video with option to take a photo
    def start_recording(self, filename=None, preview=False):
        """
        Record a video of undefined length
        """
        filename = utils.format_filename(filename, ".mp4")

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
