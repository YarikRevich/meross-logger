from handler import Handler
from broker import Broker

def main():
    broker = Broker()
    broker.start()

    handler = Handler(broker)
    
    try:
        handler.start()
    except KeyboardInterrupt:
        pass    
        
    broker.stop()

if __name__ == "__main__":
    main()
