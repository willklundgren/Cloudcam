# Handle D2C here
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import asyncio
import config

class CloudManager():

    def __init__(self):
        print("Created CloudManager")
        self.device_client = IoTHubDeviceClient.create_from_connection_string(config.azure["iot_hub_conn_str"])
        
    async def connect(self):
         await self.device_client.connect()
        
    async def send_message(self, confidence, message):
        
        # Give detection info: timestamp, confidence, message
        D2C_message = Message(message)
        D2C_message.custom_properties["Confidence"] = confidence

        await self.device_client.send_message(D2C_message)

    async def store_in_blob(self, filename, confidence):
        blob_storage_info = await self.device_client.get_storage_info_for_blob(filename)
        sas_url = "https://{}/{}/{}{}".format(
            blob_storage_info["hostName"],
            blob_storage_info["containerName"],
            blob_storage_info["blobName"],
            blob_storage_info["sasToken"]
        )
        print(f"Upload SAS token: {sas_url} \n")
        confidence_metadata = dict(confidence=confidence)
        print("Uploading picture to blob storage...")
        with BlobClient.from_blob_url(sas_url) as blob_storage_client:
            with open(filename, "rb") as picture:
                result = blob_storage_client.upload_blob(data=picture , metadata=confidence_metadata )
                return result

    async def disconnect(self):
        await self.device_client.disconnect()