from threading import Thread, Event
import os
import signal
import WebProxy

# def set_sig(signal, frame):
#     proxy.shutdown()

if __name__ == "__main__":
    event = Event()

    proxy = WebProxy.WebProxy()

    process = Thread(target=proxy.run)
    process.start()

    try:
        while True: pass
    except KeyboardInterrupt:
        proxy.shutdown()

    process.join()