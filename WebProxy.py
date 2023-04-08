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
                client, address = s.accept()
                
                # Forking process to service client
                client_process = Process(target=self.service_client, args=(client, address))
                client_process.start()
    
    def service_client(self, client, address):
        # Get Requested url from client
        req = client.recv(1024).decode()
        line = req.split('\n')[0]
        url = line.split(' ')[1]

        print(f'Sending request Client:{address} req:{url}')

        http_pos = url.find('://')
        if http_pos != -1:
            url = url[http_pos+3:]

        
        webserver = ''
        port = ''

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
        
        # Connect with web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
        s.connect((webserver, port))
        # s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
        s.sendall(req.encode())

        while True:
            data = s.recv(1024)

            if len(data) > 0:
                client.send(data)
            else:
                break

        
        print(f'Client:{address} req:{url} Serviced')

        client.shutdown(socket.SHUT_RDWR)
        client.close()
