from multiprocessing import Process
import socket
import signal
import sys
import select
import ssl

class WebProxy:
    def __init__(self, port):
        signal.signal(signal.SIGINT, self.shutdown)

        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.settimeout(0)
            self.serverSocket.bind(('localhost', port))
            self.serverSocket.listen()

            print("Socket Created")

        except socket.error as err:
            print("Socket Creation Failed")
            print(err)
            sys.exit(0)
    
    def shutdown(self, signal, frame):
        self.serverSocket.close()
        print("Shutting Down Proxy Server")
        sys.exit(0)
    
    def run(self):
        while True:
            read, write, err = select.select([self.serverSocket], [], [], 0)
            for s in read:
                browser, address = s.accept()
                
                # Forking process to service client
                client_process = Process(target=self.service_client, args=(browser, address))
                client_process.start()
    
    def service_client(self, browser, address):
        # Get Requested url from client
        req = browser.recv(1024).decode()
        line = req.split('\n')[0]
        url = line.split(' ')[1]

        print(f'Sending request Client:{address} req:{url}')

        webserver, port = self.parse_req(url)
        
        # Connect with web server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(60)
        server.connect((webserver, port))
        server.sendall(req.encode())

        while True:
            data = server.recv(1024)

            if len(data) > 0:
                browser.send(data)
            else:
                break
        
        print(f'Client:{address} req:{url} Serviced')

        browser.close()
    
    def parse_req(self, url):
        http_pos = url.find('://')
        if http_pos != -1:
            url = url[http_pos+3:]
        
        webserver = ''
        port = ''s

        port_pos = url.find(':')
        
        webserver_pos = url.find('/')
        if webserver_pos == -1:
            webserver_pos = len(url)

        if port_pos == -1:
            port = 80
            webserver = url[:webserver_pos]
        else:
            port = int(url[port_pos+1:webserver_pos])
            webserver = url[:port_pos]
        
        return webserver, port
