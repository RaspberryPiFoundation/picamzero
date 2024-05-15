from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from time import sleep

class Camera():

    def __init__(
        self,
        demo_string="Something exciting"        
    ):
        
        """
        Creates a Camera object based on a Picamera2 object
        """    
        self._pc2 = Picamera2()
        self.demo_string = demo_string
        
    def record_video(self, filename, duration=5):
        
        if not filename.endswith('.mp4'):
            filename += '.mp4'  # Append '.mp4' extension if not present

        # Start recording the video
        video_config = self._pc2.create_video_configuration()   # Do we need a config option?
        self._pc2.configure(video_config)
        self._pc2.start(show_preview=True)
        encoder = H264Encoder(10000000)
        
        output = FfmpegOutput(filename)
        self._pc2.start_recording(encoder, output)
        sleep(duration)
        self._pc2.stop_recording()
        self._pc2.stop_preview()

cam = Camera()
cam.record_video('test', 10)
