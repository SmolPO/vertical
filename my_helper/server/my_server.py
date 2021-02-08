import socket
import logging
import pickle
import configparser
from commands import *

class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        logging.info("Сервер запущен")

    def close(self):
        self.conn.close()

    def send_message(self, cmd, data):
        message = dict(cmd=cmd, data=data, size_next_message=10)
        zip_data = pickle.dumps(message)
        self.conn.send(zip_data)

    def run(self):
        first_message = dict(cmd=0, next_mes=0)
        while True:
            receive_data = pickle.loads(self.conn.recv(self.size_next_mess))
            if receive_data['cmd'] == app_connect_to_app:
                self.send_message(ser_connect_to_app, self.size_next_mess)
                logging.info("Подключено App к серверу")

            elif receive_data['cmd'] == 2:
                self.conn.send(receive_data.upper())



