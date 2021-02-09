import kivy
import random

import socket
import pickle
import logging
from ...server.commands import *


class HBoxLayoutExample:
    def __init__(self):
        self.sock = socket.socket()
        self.size_next_message = 1024
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        pass

    def connect_to_server(self):
        self.sock.connect(('localhost', 9090))
        zip_data = pickle.dumps(dict(cmd=nb_connect_to_ser, next_mes=0))
        self.sock.send(zip_data)
        data = self.sock.recv(1024)
        answer = pickle.loads(data)
        if answer['cmd'] == answ_ser_connect_nb:
            logging.info("Подключился к серверу")
        else:
            logging.info("Сервер недоступен")

    def send_message(self, cmd, data, size_next=1024):
        message = dict(cmd=cmd, data=data, from_=1, size_next_message=size_next)
        zip_data = pickle.dumps(message)
        self.sock.send(zip_data)

    def listen_server(self):
        self.sock.listen()
        while True:
            data = self.sock.recv(self.size_next_mess)
            if not data:
                continue
            receive_data = pickle.loads(data)
            if receive_data['cmd'] == answ_ser_connect_nb:
                print("yes, connect")
                logging.info("Сервер подключился ко мне снова, зачем?")
            elif receive_data['cmd'] == app_test_cmd:
                self.send_message(answ_nb_test_cmd, "привееет, тестовую команду получил!")
                print(receive_data['data'])


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()