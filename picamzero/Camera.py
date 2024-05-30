from picamera2 import Picamera2
# from picamera2.encoders import H264Encoder
# from picamera2.outputs import FfmpegOutput
from time import sleep, strftime, localtime

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

	# Take a picture
    def take_picture(self, filename=None):
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


    # Record a video 
    def record_video(self, filename=None, duration=5):
        """
        Record a video using the camera
        """
        
        if filename is None:
            # Set a default filename of example + current date/time
            filename = "example" + strftime("%Y%m%d%H%M%S", localtime()) + ".mp4"
        
        # Use basic inbuilt function
        self.pc2.start_and_record_video(filename, duration=duration)
        
        return filename
        


