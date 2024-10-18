import time
import json
import random
import logging
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your actual device-specific connection string
connection_string = "HostName=KritsnamIoTHub1.azure-devices.net;DeviceId=KritsnamIoTDevice1;SharedAccessKey=fTuzWR37e8jBuhEHZLEujiPu4VRabsb3rDmGcC+0Sc0="

def generate_random_telemetry():
    base_timestamp = int(time.time() * 1000)
    tele_param = []
    for i in range(4):
        tele_param.append({
            "ts": base_timestamp + (i * 60000),
            "flowRate": round(random.uniform(0, 100), 2),
            "discharge": random.randint(36000, 38000),
            "workHour": random.randint(22000, 23000),
            "cummRevDisch": random.randint(-10, 10),
            "Data": random.randint(220000, 230000),
            "CycleSlips": random.randint(50000, 55000),
            "NoData": random.randint(600, 700),
            "USS": random.randint(50000000, 53000000)
        })
    return tele_param

def create_payload():
    return {
        "token": "FM1037",
        "status": "ok",
        "json-ver": "v1.2",
        "teleParam": generate_random_telemetry()
    }

def main():
    device_client = None
    try:
        # Create the IoT Hub client
        device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        if not device_client:
            logger.error("Failed to create IoT Hub Device Client")
            return

        # Connect to the IoT Hub
        logger.info("Connecting to IoT Hub...")
        device_client.connect()
        logger.info("Connected to IoT Hub")

        # Define callback for cloud-to-device (C2D) message acknowledgment
        def on_command_received(command_request):
            logger.info(f"Command received: {command_request.name} with payload: {command_request.payload}")
            
            if command_request.name == "AcknowledgeMessage":
                # Process the received command payload
                logger.info("Acknowledging the received command...")

                # Create an acknowledgment payload to send back to the cloud
                response_payload = {
                    "status": "acknowledged"
                }

                # Create a method response and send it back
                method_response = MethodResponse.create_from_method_request(command_request, 200, response_payload)
                device_client.send_method_response(method_response)
                logger.info("Acknowledgment sent back to IoT Hub")

        device_client.on_method_request_received = on_command_received

        # Create a payload with random telemetry data
        payload = create_payload()

        # Send telemetry data to IoT Hub (D2C)
        message = Message(json.dumps(payload))
        message.content_encoding = "utf-8"
        message.content_type = "application/json"

        logger.info(f"Sending message: {json.dumps(payload, indent=2)}")
        device_client.send_message(message)
        logger.info("Telemetry message successfully sent!")

    except Exception as e:
        logger.error(f"Error occurred: {e}")

    finally:
        # Disconnect the client
        if device_client:
            logger.info("Disconnecting from IoT Hub...")
            try:
                device_client.disconnect()
                logger.info("Disconnected from IoT Hub")
            except Exception as e:
                logger.error(f"Error disconnecting from IoT Hub: {e}")

if __name__ == "__main__":
    main()
