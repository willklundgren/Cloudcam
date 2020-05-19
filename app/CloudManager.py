# Handle D2C here
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio

class CloudManager():

    def __init__(self):
        print("Created CloudManager")
        self.device_client = IoTHubDeviceClient.create_from_connection_string("HostName=test-projects-iot-hub.azure-devices.net;DeviceId=rpi3_cloudcam;SharedAccessKey=o6imCgVXSEixjxQ29+CPfz0ZTgtXOJxGsdLXWNxVcCw=")
        
    async def connect(self):
         await self.device_client.connect()
        
    async def send_message(self, message):
        await self.device_client.send_message(message)

    async def disconnect(self):
        await self.device_client.disconnect()