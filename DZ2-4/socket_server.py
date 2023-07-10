import socket
from threading import Thread, Event
import logging
import json
import datetime
from time import sleep
import pathlib

MAIN_IP = '0.0.0.0'
HOST = '127.0.0.1'
PORT = 5000
STORAGE_DIR = pathlib.Path().joinpath('storage')
FILE_STORAGE = STORAGE_DIR / 'data.json'
# filename = './storage/data.json'

def recieve(sock, event_for_exit: Event):
    try:
        while True:
            data, address = sock.recvfrom(1024)
            msg = data.decode()
            data_dict = {key: value for key, value in [el.split('=') for el in msg.split('&')]}
            logging.debug(f'Socket_Server: Received data "{msg}" from {address}')

            sock.sendto(data, address)
            # logging.debug(f'Socket_Server: Send data "{msg}" to {address}')

            try:
                with open(FILE_STORAGE, "r", encoding='utf-8') as file:
                    data = json.load(file)
            except:
                data = {}

            dt = str(datetime.datetime.now())
            data.update({dt: data_dict})

            with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
                json.dump(data, fd, ensure_ascii=False, indent=4)

            if event_for_exit.is_set():
                break

    except Exception as e:
        logging.debug(f'Socket_Server: Error - '+str(e))
    finally:
        sock.close()
        logging.debug(f'Socket_Server: Stop')

def run_server(ip, port, event_for_exit: Event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    logging.debug('Socket_Server: Start')
    try:
        sock_server = Thread(target=recieve, args=(sock, event_for_exit))
        sock_server.start()

        while True:
            sleep(1)
            if event_for_exit.is_set():
                break

    except Exception as e:
        logging.debug(f'Socket_Server: Error - '+str(e))
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        logging.debug(f'Socket_Server: Shutdown')
        sock.close()
        logging.debug(f'Socket_Server: Stop')
    
def start_server(host, port, event_for_exit: Event):
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False)

    socket_server = Thread(target=run_server, args=(host, port, event_for_exit))
    socket_server.start()
    return socket_server


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s %(message)s')
    event = Event()
    socket_server = Thread(target=run_server, args=(HOST, PORT, event))
    socket_server.start()

    # run_server(HOST, PORT)

    sleep(1)
    while True:
        inp = input('Stop socket server (Y / N)? ').lower().strip()
        if inp == 'y':
            break

    event.set()
    socket_server.join()
    logging.debug('Done!')
