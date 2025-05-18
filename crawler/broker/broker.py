import os
from datetime import datetime, timezone
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

__all__ = ["Broker"]

class Broker:
    """Represents InfluxDB broker wrapper."""
    
    def __init__(self):
        self.client = InfluxDBClient(
            url=os.environ["INFLUXDB_HOST"], 
            token=os.environ["INFLUXDB_TOKEN"], 
            org=os.environ["INFLUXDB_ORG"], 
            debug=False)

    def send(self, device: str, value: str) -> None:
        """Sends payload to previously selected measurement."""
        
        p = Point("status").tag("device", device).field("value", value) \
            .time(datetime.now(tz=timezone.utc), WritePrecision.MS)
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        write_api.write(bucket=os.environ["INFLUXDB_BUCKET"], record=p) 
        
    def close(self) -> None:
        """Stops InfluxDB client."""
        
        self.client.close()