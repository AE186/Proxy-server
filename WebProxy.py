from multiprocessing import Process
import socket
import signal
import sys
import select
import json
import ContentFilter
import Cache

class WebProxy:
    def __init__(self):
        signal.signal(signal.SIGINT, self.shutdown)

        with open('config.json') as f:
            self.config = json.load(f)

        self.content_filter = ContentFilter.Filter()
        self.cache = Cache.getCache(self.config['CACHING-ALGO'], self.config['CACHE-SIZE'])

        try:
            self.proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.proxySocket.settimeout(0)
            self.proxySocket.bind((self.config['IP'], self.config['PORT']))
            self.proxySocket.listen()

            # print("Socket Created")

        except socket.error as err:
            print("Socket Creation Failed")
            print(err)
            sys.exit(0)
    
    def shutdown(self, signal, frame):
        self.proxySocket.close()
        print("Shutting Down Proxy Server")
        sys.exit(0)
    
    def run(self):
        while True:
            read, write, err = select.select([self.proxySocket], [], [], 0)
            for s in read:
                browser, address = s.accept()
                
                # Forking process to service client
                client_process = Process(target=self.service_browser, args=(browser, address))
                client_process.daemon = True
                client_process.start()
            
    def service_browser(self, browser, address):
        # Get Request from browser
        req = browser.recv(self.config['MAX-RECV-BUFF']).decode()
        line = req.split('\n')[0]
        url = line.split(' ')[1]
        method = line.split(' ')[0]

        webserver, port = self.parse_url(url)

        if self.content_filter.block(url):
            browser.close()
            return

        # print(f'Client:{address} method:{method} url:{url}\n')
        
        # Connect with web server and serve data to browser
        if port == 80:
            self.serve_http(webserver, port, browser, req, method, url)
        else:
            self.serve_https(webserver, port, browser)
        
        # print(f'Client:{address} method:{method} url:{url} Serviced')

        browser.close()
    
    def parse_url(self, url):
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
        
        return webserver, port

    def serve_http(self, webserver, port, browser, req, method, url):
        # Only GET and HEAD requests can be cached
        if (method == 'GET' or method == 'HEAD'):
            content = self.cache.get(url)
            if content is not None:
                browser.sendall(content)
                browser.close()
                return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(self.config["MAX-TIMEOUT"])
        server.connect((webserver, port))
        server.sendall(req.encode())

        content = bytes()

        
        while True:
            try:
                data = server.recv(self.config['MAX-RECV-BUFF'])
            except socket.error as err:
                pass

            if len(data) > 0:
                content += data
            else:
                break
        
        browser.sendall(content)
        server.close()

        if method == 'GET' or method == 'HEAD':
            self.cache.put(url, content)
    
    def serve_https(self, webserver, port, browser):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((webserver, port))

        # Send Connection Established with server for CONNECT request
        browser.sendall('HTTP/1.1 200 Connection established\r\n\r\n'.encode())

        server.setblocking(0)
        browser.setblocking(0)

        # Tunneling HTTPS client and server
        while True:
            try:
                browser_data = None
                server_data = None

                read, write, err = select.select([browser], [], [], 0)
                for s in read:
                    browser_data = s.recv(self.config['MAX-RECV-BUFF'])
                    server.sendall(browser_data)
                
                read, write, err = select.select([server], [], [], 0)
                for s in read:
                    server_data = s.recv(self.config['MAX-RECV-BUFF'])
                    browser.sendall(server_data)
                
                if browser_data is not None and server_data is not None and len(browser_data) == 0 and len(server_data) == 0:
                    break
            except socket.error as e:
                print(e)
                break
        
        server.close()

    def block(self, url):
            self.content_filter.Add_url(url)
        
    def unblock(self, url):
            self.content_filter.remove_url(url)