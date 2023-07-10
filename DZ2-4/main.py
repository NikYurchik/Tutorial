from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
import socket
from threading import Thread, Event
import logging
from time import sleep
import socket_server


HTTP_HOST = '0.0.0.0'
LOCAL_HOST = '127.0.0.1'
HTTP_PORT = 3000
UDP_PORT = 5000

BUFFER = 1024
OK = 200
FOUND = 302
NOT_FOUND = 404


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', NOT_FOUND)

    def send_html_file(self, filename, status=OK):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(OK)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        send_socket(data_parse)

        self.send_response(FOUND)
        self.send_header('Location', '/')
        self.end_headers()


def send_socket(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = LOCAL_HOST, UDP_PORT
    data = msg.encode()
    sock.sendto(data, server)
    response, address = sock.recvfrom(BUFFER)
    sock.close()

def run_http(event_for_exit: Event):
    server_address = (HTTP_HOST, HTTP_PORT)
    http = HTTPServer(server_address, HttpHandler)
    logging.debug('HTTP_Server: Start')
    try:
        server = Thread(target=http.serve_forever)
        server.start()
        while True:
            sleep(1)
            if not server.is_alive():
                raise Exception('Abnormal HTTP_Server shutdown!')
            if event_for_exit.is_set():
                break
    except Exception as e:
        logging.error(f'HTTP_Server: Error - '+str(e))
    finally:
        http.shutdown()
        logging.debug(f'HTTP_Server: Shutdown')
        http.server_close()
        logging.debug(f'HTTP_Server: Stop')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s %(message)s')
    event = Event()
    
    # socket_server = Thread(target=run_server, args=(LOCAL_HOST, UDP_PORT, event))
    # socket_server.start()
    sock_server = socket_server.start_server(LOCAL_HOST, UDP_PORT, event)

    http_server = Thread(target=run_http, args=(event,))
    http_server.start()

    sleep(1)
    while True:
        inp = input('Stop all servers (Y / N)? ').lower().strip()
        if inp == 'y':
            break

    event.set()
    [el.join() for el in [socket_server, http_server]]
    logging.debug('Done!')
    