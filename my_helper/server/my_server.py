import socket
import logging
import pickle
import configparser
from collections import deque
from commands import *
import threading


class Server:
    def __init__(self):
        self.my_queue = deque()
        self.sock = socket.socket()
        self.conn = dict(sock_app=None, sock_nb=None, adr_app=None, adr_nb=None, thr_app=None, thr_nb=None)
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        logging.info("Сервер создан")

    def close(self):
        self.conn['sock_app'].close()
        self.conn['sock_nb'].close()

    def send_message(self, cmd, data, where, size_next=1024):
        message = dict(cmd=cmd, data=data, size_next_message=size_next)
        zip_message = pickle.dumps(message)
        key = 'sock_app' if where == to_app else 'sock_nb'
        self.conn[key].send(zip_message)

    def listener(self, source):
        key = 'sock_app' if source == from_app else 'sock_nb'
        conn, adr = self.conn[key], self.conn[key]
        while True:
            message = pickle.loads(conn.recv(self.size_next_mess))
            if not message:
                continue
            else:
                self.my_queue.append(message)
                threading.Thread(target=self.queue_worker()).start()

    def queue_worker(self):
        message = self.my_queue.pop()
        if message['cmd'] == app_connect_to_ser:
            self.conn['sock_app'].send(ser_connect_to_app, self.size_next_mess)
        elif message['cmd'] == nb_connect_to_ser:
            self.conn['sock_nb'].send(ser_connect_to_nb, self.size_next_mess)
        elif message['cmd'] == app_test_cmd:
            self.conn['sock_nb'].send(ser_test_cmd, self.size_next_mess)
        elif message['cmd'] == nb_test_cmd:
            self.conn['sock_app'].send(ser_test_cmd, self.size_next_mess)
            pass

    def run(self):
        self.sock.bind(('', 9090))
        self.sock.listen(2)
        while True:
            conn, adr = self.sock.accept()
            message = pickle.loads(conn.recv(self.size_next_mess))
            if message['cmd'] == app_connect_to_ser:
                self.conn['sock_app'] = conn
                self.conn['adr_app'] = adr
                threading.Thread(target=self.listener, args="app").start()
                self.my_queue.append(message)
                threading.Thread(target=self.queue_worker()).start()
            elif message['cmd'] == nb_connect_to_ser:
                self.conn['sock_nb'] = conn
                self.conn['adr_nb'] = adr
                threading.Thread(target=self.listener).start()
            else:
                conn.close()


