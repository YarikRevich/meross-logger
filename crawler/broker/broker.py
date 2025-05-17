import json
import os
import paho.mqtt.client as mqtt

__all__ = ["Broker"]

class Broker:
    """Represents MQTT broker wrapper."""
    
    def __init__(self):
        self.mqtt_client = mqtt.Client()

    def send(self, payload: object) -> None:
        """Sends payload to previously selected topic."""
        
        self.mqtt_client.publish(os.environ["MQTT_TOPIC"], json.dumps(payload))
        
    def start(self) -> None:
        """Starts MQTT broker."""
        
        self.mqtt_client.connect(os.environ["MQTT_BROKER"], int(os.environ["MQTT_PORT"]), 60)
        self.mqtt_client.loop_start()
        
    def stop(self) -> None:
        """Stops MQTT broker."""
        
        self.mqtt_client.loop_stop()