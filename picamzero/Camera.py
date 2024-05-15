from picamera2 import Picamera2

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



cam = Camera()
