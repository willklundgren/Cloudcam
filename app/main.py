from picamera import PiCamera
import time
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
from VideoStream import VideoStream
from CloudManager import CloudManager
import asyncio
import os

async def main():

    # Set minimum confidence level required to draw bounding box; default is 60%
    minimum_confidence = 0.60
    # Set image folder (folder will be mirrored on the cloud); should be determined before running; default is 0
    image_folder_number = 0
    path = f"./cloudcam_session{image_folder_number}"
    while os.path.isdir(path) or os.path.isfile(path):
        print("Incrementing folder number")
        image_folder_number += 1
        path = f"./cloudcam_session{image_folder_number}"
        print(image_folder_number)
        
    os.mkdir(f"./cloudcam_session{image_folder_number}")

    cloud_manager = CloudManager()
    await cloud_manager.connect()

    # Read label file and load labels into a variable
    with open( "./Sample_TFLite_model/labelmap.txt" ) as file:
        labels = [ line.strip() for line in file.readlines() ]
        if labels[0] == '???':
            del(labels[0])

    print("Loading model into interpreter...")
    interpreter = Interpreter(model_path = "./Sample_TFLite_model/detect.tflite")

    # Getting useful information on the model for later use
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    model_input_height = input_details[0]["shape"][1]
    model_input_width = input_details[0]["shape"][2]

    # Preparing model inside interpreter
    interpreter.allocate_tensors()

    # Getting the video stream
    video_handler = VideoStream()
    frame_counter = 0

    for frame in video_handler.capture_stream():

        image = frame.array
        print("Performing image pre-processing...")
        # image_path = "./<YOUR TEST IMAGE>.jpg" # Can change accordingly
        # image = cv2.imread( image_path )
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

            if confidence > minimum_confidence and object_detected == "person": # can omit section after "and" to detect multiple objects

                frame_counter += 1

                print("Object:", object_detected)
                print("Confidence:", scores[i])
                print("")

                # Get x and y coordinates of bounding box, correcting for inference results that lay off the original image
                y_lower = int( max(1, (boxes[i][0] * image_rows) ) )
                y_upper = int( max(image_rows , (boxes[i][2] * image_rows) ) )
                x_lower = int( max(1, (boxes[i][1] * image_columns) ) )
                x_upper = int( max(image_columns , (boxes[i][3] * image_columns) ) )

                # Draw bounding box on the image
                cv2.rectangle(image, (x_lower, y_lower), (x_upper, y_upper), (255, 0, 0), 3)
                # cv2.imshow("Inference Result", image)
                new_image_path = f"cloudcam_session{image_folder_number}/cloudcam_image{frame_counter}.jpg"
                
                print("Saving image locally to Pi...")
                cv2.imwrite(new_image_path, image) # Can disable if Pi's memory is constrained
                confidence_string = str(round(confidence * 100, 1)) + '%'

                # Create and send message to cloud
                D2C_message = f"Detected {object_detected}"
                await cloud_manager.send_message(confidence_string, D2C_message)
                await cloud_manager.store_in_blob(new_image_path, confidence_string)
                

        # Clear stream for next frame
        video_handler.array_capture.truncate(0)
        time.sleep(2)

if __name__ == '__main__':   
    asyncio.run(main())