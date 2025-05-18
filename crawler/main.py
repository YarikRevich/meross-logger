from handler import Handler
from broker import Broker

def main():
    broker = Broker()
    handler = Handler(broker)
    
    try:
        handler.start()
    except KeyboardInterrupt:
        pass    
        
    broker.close()

if __name__ == "__main__":
    main()
