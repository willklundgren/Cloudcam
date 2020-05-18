from picamera import PiCamera
from time import sleep
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np

# Read label file and load labels into a variable
with open( "./Sample_TFLite_model/labelmap.txt" ) as file:
    labels = [ line.strip() for line in file.readlines() ]
    if labels[0] == '???':
        del(labels[0])

print("Taking a single picture...")

camera = PiCamera()
# camera.start_preview()
sleep(1)
camera.capture("./pi_camera_test_pic_debug.jpg")
sleep(1)
# camera.stop_preview()

print("Loading model into interpreter...")
interpreter = Interpreter(model_path = "./Sample_TFLite_model/detect.tflite")

# Getting useful information on the model for later use
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
model_input_height = input_details[0]["shape"][1]
model_input_width = input_details[0]["shape"][2]

interpreter.allocate_tensors()

print("Performing image pre-processing...")
image_path = "./BusinessWoman3.jpg" # Change accordingly
image = cv2.imread( image_path )
image_rgb = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )
imH, imW, _ = image.shape
image_resized = cv2.resize( image_rgb, ( model_input_width , model_input_height ) )
model_input_data = np.expand_dims( image_resized , axis=0 )

print("Performing inference...")
interpreter.set_tensor( input_details[0]["index"] , model_input_data )
interpreter.invoke() # Executes the inference
classes = interpreter.get_tensor(output_details[1]["index"])[0]
scores = interpreter.get_tensor(output_details[2]["index"])[0]

for i in range( len(scores) ):
    object_detected = labels[ int(classes[i]) ]
    print("Object:", object_detected)
    print("Confidence:", scores[i])
    print("")
