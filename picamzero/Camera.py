import logging
import math
import os
from functools import wraps
from time import sleep, time
from typing import Callable, TypeVar

import cv2
import numpy as np
from libcamera import Transform
from picamera2 import MappedArray, Picamera2

from . import utilities as utils
from .PicameraZeroException import PicameraZeroException

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.WARN)

# Suppress Libcamera and Picamera warnings
os.environ["LIBCAMERA_LOG_LEVELS"] = "4"
Picamera2.set_logging(level=logging.ERROR)

# Different camera and processor combinations
# support a different range of resolutions.
# This is the minimum 'maximum' for all combinations.
MAX_VIDEO_SIZE: tuple[int, int] = (1920, 1080)

# T = TypeVar("T", bound=Any)
T = TypeVar("T")


class Camera:

    _instance_count = 0

    def __init__(self):

        if Camera._instance_count > 0:
            raise PicameraZeroException(
                "Only one Camera instance is allowed.",
                "Ensure you are not trying to create multiple Camera objects.",
            )
        """
        Creates a Camera object based on a Picamera2 object

        :param Picamera2 pc2:
            An internal Picamera2 object. This can be accessed by
            advanced users who want to use methods we have not
            wrapped from the Picamera2 library.
        """
        try:
            self.pc2 = Picamera2()
            Camera._instance_count += 1

        except RuntimeError:
            logger.error("Could not connect to the camera!")
            logger.error("Please check all connections")
            exit()

        # Camera
        self.hflip = False
        self.vflip = False

        # Annotation
        self._text = None
        self._text_properties = {
            "font": utils.check_font_in_dict("plain1"),
            "color": (255, 255, 255, 255),
            "position": (0, 0),
            "scale": 3,
            "thickness": 3,
            "bgcolor": None,
            "position": (0, 0),
        }

        self.pc2.start()

    def __del__(self):
        """
        Cleanup the Camera instance when it is deleted
        """
        Camera._instance_count -= 1
        if hasattr(self, "pc2") and self.pc2 is not None:
            self.pc2.close()

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
        return self.pc2.preview_configuration.size

    @preview_size.setter
    def preview_size(self, size):
        utils.set_camera_size(
            self.pc2.preview_configuration,
            self.pc2.sensor_resolution,
            size,
            error_msg_type="preview",
        )

    @property
    def still_size(self):
        return self.pc2.still_configuration.size

    @still_size.setter
    def still_size(self, size):
        utils.set_camera_size(
            self.pc2.still_configuration,
            self.pc2.sensor_resolution,
            size,
            error_msg_type="image",
        )

    @property
    def video_size(self):
        return self.pc2.video_configuration.size

    @video_size.setter
    def video_size(self, size):
        utils.set_camera_size(
            self.pc2.video_configuration, MAX_VIDEO_SIZE, size, error_msg_type="video"
        )

    # Check that a control exists (it might not have been set yet)
    def _get_control_value(self, name: str):
        if name in self.pc2.controls.make_dict():
            return getattr(self.pc2.controls, name)
        else:
            minvalue, maxvalue, defaultvalue = self.pc2.camera_controls[name]
            return defaultvalue

    # Brightness
    @property
    def brightness(self) -> float:
        """
        Get the brightness

        :return float:
            Brightness value between -1.0 and 1.0
        """
        return self._get_control_value("Brightness")

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
        return self._get_control_value("Contrast")

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
        return self._get_control_value("ExposureTime")

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
        return self._get_control_value("AnalogueGain")

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
    def white_balance(self) -> str | None:
        """
        Get the white balance mode

        :return str:
            The selected white balance mode as a string
        """
        control = "AwbMode"
        if control in self.pc2.controls.make_dict():
            return utils.possible_controls(reverse_kv=True)[self.pc2.controls.AwbMode]
        else:
            return None

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

    @property
    def greyscale(self) -> bool:
        if (
            "Saturation" in self.pc2.controls.make_dict()
            and self.pc2.controls.Saturation == 0
        ):
            return True
        else:
            # Any saturation above 0 results in greyscale off?
            return False

    @greyscale.setter
    def greyscale(self, on: bool) -> None:
        """
        Apply greyscale to the preview and image
        You have to call this _after_ the preview has started or it wont apply
        Does NOT apply to video

        :param bool on:
            Whether greyscale should be on
        """
        if on:
            self.pc2.controls.Saturation = 0.0
        else:
            self.pc2.controls.Saturation = 1.0

    @staticmethod
    def retain_controls(method: Callable[..., T | None]) -> Callable[..., T | None]:
        """
        Decorator to note the controls status before a method
        and return to that state after the method ends.

        Apply by adding @retain_controls before method definition.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs) -> T | None:

            # Make a note of the old size and controls
            configs = [
                self.pc2.preview_configuration,
                self.pc2.still_configuration,
                self.pc2.video_configuration,
            ]
            old_sizes = [config.size for config in configs]
            old_controls = self.pc2.controls.make_dict()

            # Do whatever it is you're doing
            returnvalue = method(self, *args, **kwargs)

            # Reset the controls
            self.pc2.set_controls(old_controls)

            # Reapply the transform and size
            trans = {"transform": Transform(hflip=self.hflip, vflip=self.vflip)}
            for i, config in enumerate(configs):
                config.update(trans)
                config.size = old_sizes[i]

            return returnvalue

        return wrapper

    # ----------------------------------
    # METHODS
    # ----------------------------------

    def flip_camera(self, vflip=False, hflip=False):
        """
        Flip the image horizontally or vertically
        """
        self.vflip = vflip
        self.hflip = hflip

        trans = {"transform": Transform(hflip=hflip, vflip=vflip)}
        self.pc2.preview_configuration.update(trans)
        self.pc2.still_configuration.update(trans)
        self.pc2.video_configuration.update(trans)

    @retain_controls
    def start_preview(self):
        """
        Show a preview of the camera
        """

        # At this point, null preview is probably running still...
        # (but that is OK!)
        try:
            self.pc2.stop_preview()  # Stop null preview
            self.pc2.start_preview(preview=True)

        except RuntimeError as e:
            logger.error(f"Preview couldn't start: {e}")

    @retain_controls
    def stop_preview(self):
        """
        Stop the preview
        """
        try:
            # Picam2 method should handle whether there actually is one
            self.pc2.stop_preview()

        except RuntimeError:
            logger.error("Couldn't stop preview")

    def annotate(
        self,
        text="Default Text",
        font="plain1",
        color=(255, 255, 255, 255),
        scale=3,
        thickness=3,
        position=(0, 0),
        bgcolor=None,
    ):
        """
        Set a text overlay on the preview and on images
        """
        self._text = text

        font = utils.check_font_in_dict(font)
        color = utils.convert_color(color)

        self._text_properties = {
            "font": font,
            "color": color,
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
    def add_image_overlay(self, image_path, position=(0, 0), transparency=0.5):
        overlay_img, position, transparency = utils.check_image_overlay(
            image_path, position, transparency
        )

        # Ensure the image is in BGRA format (with alpha channel)
        if overlay_img.shape[2] == 3:  # If no alpha channel, add one
            overlay_img = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2BGRA)

        overlay_h, overlay_w = overlay_img.shape[:2]

        def overlay_callback(request):
            with MappedArray(request, "main") as m:
                frame_h, frame_w = m.array.shape[:2]

                x, y = position

                # Ensure the region we overlay onto matches the overlay image's size
                roi = m.array[y : y + overlay_h, x : x + overlay_w]

                # Combine the images
                overlay_img_resized = cv2.resize(
                    overlay_img, (roi.shape[1], roi.shape[0])
                )
                overlay_alpha = overlay_img_resized[:, :, 3] / 255.0 * transparency
                background_alpha = 1.0 - overlay_alpha

                for c in range(0, 3):
                    roi[:, :, c] = (
                        overlay_alpha * overlay_img_resized[:, :, c]
                        + background_alpha * roi[:, :, c]
                    )

        # Add the overlay as a callback when any pics are taken or preview is shown
        self.pc2.pre_callback = overlay_callback

    # Take video and take still
    @retain_controls
    def take_video_and_still(self, filename=None, duration=20, still_interval=4):
        """
        Take video for <duration> and take a still every <interval> seconds?
        """
        # Format the filename so that it has no extension
        filename = utils.format_filename(filename, ext="")

        # Calculate when to take stills
        still_times = [
            i * still_interval
            for i in range(1, math.ceil(duration / still_interval) + 1)
        ]
        # Remove any times that are greater than the duration
        # (they need to be generated otherwise for durations that are
        # exactly divisible the final still isn't included)
        result = list(filter(lambda x: x <= duration, still_times))

        # Start the video
        self.pc2.start_and_record_video(f"{filename}.mp4", config="video")
        start_time = time()

        padding_amount: str = str(math.ceil(math.log10(len(result) + 1)))
        ext: str = "-{:0" + padding_amount + "d}.jpg"

        for i, still_time in enumerate(result):
            sleep(max(0, still_time - (time() - start_time)))

            request = self.pc2.capture_request()
            img_filename = utils.format_filename(filename, ext=ext)
            request.save("main", img_filename.format(i + 1))
            request.release()

        remaining_time = duration - (time() - start_time)

        if remaining_time > 0:
            sleep(remaining_time)

        self.stop_recording()
        self.pc2.start()

    @retain_controls
    def capture_array(self) -> np.ndarray:
        """
        Takes a photo at full resolution and saves it as an
        (RGB) numpy array.

        This can be used in further processing using libraries
        like opencv.

        :return np.ndarray:
            A full resolution image as a raw RGB numpy array
        """
        # Switch to high quality mode temporarily for array capture
        return self.pc2.switch_mode_and_capture_array(self.pc2.still_configuration)

    # Take a picture
    @retain_controls
    def take_photo(self, filename=None, gps_coordinates=None) -> str:
        """
        Takes a jpeg image using the camera
        :param str filename: The name of the file to save the photo.
        If it doesn't end with '.jpg', the ending '.jpg' is added.
        :param tuple[tuple[float, float, float, float],
                     tuple[float, float, float, float]] gps_coordinate:
        The gps coordinates to be associated
        with the image, specified as a (latitude, longitude) tuple where
        both latitude and longitude are themselves tuples of the
        form (sign, degrees, minutes, seconds). This format
        can be generated from the skyfield library's signed_dms
        function.
        """
        filename = utils.format_filename(filename, ".jpg")

        if self.pc2.started:
            self.pc2.stop()
        self.pc2.start()

        # Capture the image
        kwargs: dict = {}
        if gps_coordinates is not None:
            kwargs["exif_data"] = utils.signed_dms_coordinates_to_exif_dict(
                gps_coordinates
            )

        # Use inbuilt function for now
        self.pc2.start_and_capture_file(name=filename, **kwargs)

        self.pc2.start()

        # Useful to know what the file is called
        return filename

    # Synonym method for take a picture
    capture_image = take_photo

    # Take a sequence
    @retain_controls
    def capture_sequence(
        self, filename=None, num_images=10, interval=1, make_video=False
    ):
        """
        Take a series of <num_images> and save them as
        <filename> with auto-number, also set the interval between
        """
        # Format the filename using appropriate zero-padded sequence
        padding_amount: str = str(math.ceil(math.log10(num_images + 1)))
        ext: str = "-{:0" + padding_amount + "d}.jpg"
        img_filename = utils.format_filename(filename, ext=ext)

        img_filename = utils.OneIndexedString(img_filename)

        if self.pc2.started:
            self.pc2.stop()
        self.pc2.start()

        # DON'T specify configs here, the defaults are fine
        self.pc2.start_and_capture_files(
            img_filename, num_files=num_images, delay=interval
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
                    img_path = img_filename.format(i + 1)
                    if os.path.exists(img_path):
                        video.write(cv2.imread(img_path))
                    else:
                        logger.warning(
                            f"{img_path} does not exist and will be skipped."
                        )

                video.release()

            except Exception as e:
                logger.error(f"Error creating video: {e}")
        self.pc2.start()  # Restart camera

    # Synonym method for capture_sequence
    take_sequence = capture_sequence

    # Record a video
    @retain_controls
    def record_video(self, filename=None, duration=5):
        """
        Record a video
        """
        filename = utils.format_filename(filename, ".mp4")
        self.pc2.start_and_record_video(
            filename, config=self.pc2.video_configuration, duration=duration
        )
        self.pc2.start()
        return filename

    # Synonym method for record_video
    take_video = record_video

    # Record a video with option to take a photo
    @retain_controls
    def start_recording(self, filename=None, preview=False):
        """
        Record a video of undefined length
        """
        filename = utils.format_filename(filename, ".mp4")

        self.pc2.start_and_record_video(
            filename, config=self.pc2.video_configuration, show_preview=preview
        )

    # Stop recording video
    @retain_controls
    def stop_recording(self):
        """
        Stop recording video
        """
        self.pc2.stop_recording()
        self.pc2.start()
