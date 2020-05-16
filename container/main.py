from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(30)
camera.capture('./pi_camera_test_pic.jpg')
sleep(60)
camera.stop_preview()