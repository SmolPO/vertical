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
        self.sock.listen(2)
        self.conn = dict(sock_app=0, sock_nb=0, adr_app=0, adr_nb=0, thr_app=0, thr_nb=0)
        self.thr_queue = 0
        self.new_mess = False
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        logging.info("Сервер запущен")

    def close(self):
        self.conn['sock_app'].close()
        self.conn['sock_nb'].close()

    def send_message(self, cmd, data, where):
        message = dict(cmd=cmd, data=data, size_next_message=10)
        zip_data = pickle.dumps(message)
        #self.conn.send(zip_data)

    def listener(self, source):
        if source == "app":
            conn, adr = self.conn['sock_app'], self.conn['adr_nb']
        elif source == "nb":
            conn, adr = self.conn['sock_nb'], self.conn['adr_nb']

        while True:
            receive_data = pickle.loads(conn.recv(self.size_next_mess))
            if not receive_data:
                continue
            else:
                self.my_queue.append(receive_data)
                self.queue_worker()

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
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.thr_queue = threading.Thread(target=self.queue_worker())
        self.thr_queue.start()
        while True:
            conn, adr = self.sock.accept()
            receive_data = pickle.loads(conn.recv(self.size_next_mess))
            if receive_data['cmd'] == app_connect_to_ser:
                self.conn['sock_app'] = conn
                self.conn['adr_app'] = adr
                self.conn['thr_app'] = threading.Thread(target=self.listener, args="app")
                self.my_queue.append(receive_data)
            elif receive_data['cmd'] == nb_connect_to_ser:
                self.conn['sock_nb'] = conn
                self.conn['adr_nb'] = adr
                self.conn['thr_nb'] = threading.Thread(target=self.listener)
            else:
                conn.close()


