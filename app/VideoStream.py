from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

# Can edit this file based on video source, e.g. for a USB webcam

class VideoStream():

    # Upon initialization, create a video stream
    def __init__(self):
        self.camera = PiCamera()
         # Can set other camera properties here, e.g. resolution and frame rate
        self.array_capture = PiRGBArray(self.camera)
        time.sleep(1)
    
    def capture_stream(self):
        # Call capture_continuous here
        return self.camera.capture_continuous(self.array_capture, format="bgr", use_video_port=True)