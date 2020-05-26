# Cloudcam
Basic cloud-enabled security camera for people detection. By default, the Raspberry Pi-based camera takes a picture every 2 seconds, and, if a person is detected, it draws a bounding box on the frame and the resulting image is sent to the cloud for storage, along with a message containing the model's associated confidence. It uses a pre-trained machine learning model from Google and is intended to show off functionality with Microsoft's Azure IoT services.

![RPi Setup](/images/cloudcam_setup.jpg)

## Prerequisites
- Raspberry Pi 3 Model B (Raspbian Buster)
- Raspberry Pi camera module. A USB webcam could instead be used, although VideoStream.py would need to be revised accordingly.
- An Azure subscription (can use Microsoft's free tier for testing)
- A USB power bank, e.g. from Anker
- A MicroUSB cable
- Some tape to mount the camera

## Getting Started

- Ensure the Raspberry Pi's camera module is properly attached
- Download and/or switch to Python 3.7 or higher on your Pi
- Get the TFLite interpreter by running "pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
"
- Get OpenCV, numpy, and the Azure IoT Python device SDK by running "pip3 install -r requirements.txt"; more information on Google's sample object detection model, which is included in this repository inside the "Sample_TFLite_model" folder, can be found [here](https://www.tensorflow.org/lite/models/object_detection/overview).
- Create an Azure IoT Hub
- Create a single device in Azure IoT Hub on the Azure portal. Copy the connection string and paste it into the "config_template.py" folder. Rename the folder to "config.py"
- Follow [these](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload) instructions to link an Azure Storage account to your newly created IoT Hub.
- Switch into the Cloudcam project folder
- Run "python3 main.py"

## Acknowledgements
Thank you to Adrian Rosebrook at PyImageSearch for starter code to integrate PiCamera with OpenCV - the relevant article can be found [here](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python).