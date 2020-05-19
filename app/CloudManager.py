# Handle D2C here
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import asyncio

class CloudManager():

    def __init__(self):
        print("Created CloudManager")
        self.device_client = IoTHubDeviceClient.create_from_connection_string("HostName=test-projects-iot-hub.azure-devices.net;DeviceId=rpi3_cloudcam;SharedAccessKey=o6imCgVXSEixjxQ29+CPfz0ZTgtXOJxGsdLXWNxVcCw=")
        
    async def connect(self):
         await self.device_client.connect()
        
    async def send_message(self, confidence, message):
        
        confidence_percentage = str(round(confidence * 100, 1)) + '%'
        # Give detection info: timestamp, confidence, message
        D2C_message = Message(message)
        D2C_message.custom_properties["Confidence"] = confidence_percentage
        
        await self.device_client.send_message(D2C_message)

    async def disconnect(self):
        await self.device_client.disconnect()