import os
import re
import time
from broker import Broker

MEROSS_PATTERN = re.compile(r"\[Meross\]*[a-zA-Z\s\^\[\]0-9]*\[(.*?)\][a-zA-Z\s\^\[\]0-9]*\[(.*?)\]")
COLOR_ESCAPE_PATTERN = re.compile(r"\x1b\[([0-9;]*[mGKHF])")

__all__ = ["Handler"]

class Handler():
    """Represents handler used to watch changes in the log file."""
    
    def __init__(self, broker: Broker):
        self.broker = broker

    def start(self) -> None:
        """Starts handler observer."""
        
        with open(os.path.expanduser(os.environ["LOG_PATH"]), 'r') as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                    
                line = COLOR_ESCAPE_PATTERN.sub('', line)
                
                match = MEROSS_PATTERN.match(line)
                if match:
                    device, value = match.groups()
                    
                    print("Saved new value!")
                    
                    self.broker.send(device, value)
        
    