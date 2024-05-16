from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from time import sleep

class Camera():

    def __init__(
        self      
    ):
        
        """
        Creates a Camera object based on a Picamera2 object

        :param type name:
            Description of the parameter
        """    
        self.picamera2 = Picamera2()
        self.example = "example"
    
    # PROPERTIES
    # ----------------------------------
    @property
    def example(self):
        """
        An example 
        """
        return self.example
    
    @example.setter
    def example(self, value):
        self.example = value

    # METHODS
    # ----------------------------------

    # Record video 
    """
    Picam video methods:
    start_recording(type, format, filename, quality)
    wait_recording(duration)
    stop_recording()
    """           
    def record_video(self, filename, duration=5):
        
        if not filename.endswith('.mp4'):
            filename += '.mp4'  # Append '.mp4' extension if not present

        # Start recording the video
        video_config = self.picamera2.create_video_configuration()   # Add config options?
        self.picamera2.configure(video_config)
        self.picamera2.start(show_preview=True)
        encoder = H264Encoder(10000000)
        
        output = FfmpegOutput(filename)
        self.picamera2.start_recording(encoder, output)
        sleep(duration)
        self.picamera2.stop_recording()
        self.picamera2.stop_preview()


    """
    Picam image methods:
    capture(output, format, resize)
    capture_sequence(output, format, resize)
    """  


