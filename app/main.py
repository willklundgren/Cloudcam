from picamera import PiCamera
import time
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
from VideoStream import VideoStream

# Set minimum confidence level required to draw bounding box; default is 70%
minimum_confidence = 0.70

# Read label file and load labels into a variable
with open( "./Sample_TFLite_model/labelmap.txt" ) as file:
    labels = [ line.strip() for line in file.readlines() ]
    if labels[0] == '???':
        del(labels[0])

######################################################

# Getting the video stream
video_handler = VideoStream()

for frame in video_handler.capture_stream():

    image = frame.array
    cv2.imwrite("./video_stream_test.jpg", image)

    # Clear stream for next frame
    video_handler.array_capture.truncate(0)
    time.sleep(3)

#######################################################

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
image_rows, image_columns, image_color_channels = image.shape # Get original image height / width information
image_resized = cv2.resize( image_rgb, ( model_input_width , model_input_height ) ) # Resize image to fit model's required input shape
model_input_data = np.expand_dims( image_resized , axis=0 )

print("Performing inference...")
interpreter.set_tensor( input_details[0]["index"] , model_input_data )
interpreter.invoke() # Executes the inference

boxes = interpreter.get_tensor(output_details[0]['index'])[0]
classes = interpreter.get_tensor(output_details[1]["index"])[0]
scores = interpreter.get_tensor(output_details[2]["index"])[0]

for i in range( len(scores) ):
    object_detected = labels[ int(classes[i]) ]
    confidence = scores[i]

    if confidence > minimum_confidence:

        print("Object:", object_detected)
        print("Confidence:", scores[i])
        print("")

        # Get x and y coordinates of bounding box, correcting for inference results that lay off the original image
        y_lower = int( max(1, (boxes[i][0] * image_rows) ) )
        y_upper = int( max(image_rows , (boxes[i][2] * image_rows) ) )
        x_lower = int( max(1, (boxes[i][1] * image_columns) ) )
        x_upper = int( max(image_columns , (boxes[i][3] * image_columns) ) )

        # Draw bounding box on the image
        cv2.rectangle(image, (x_lower, y_lower), (x_upper, y_upper), (255, 0, 0), 2)
        # cv2.imshow("Inference Result", image)
        cv2.imwrite("./cv2_test_image.jpg", image) # for saving the image