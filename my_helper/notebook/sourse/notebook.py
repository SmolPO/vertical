import kivy
import random

import socket
import pickle
import logging
import configparser
from ...server.commands import *


class HBoxLayoutExample:
    def __init__(self):
        self.sock = socket.socket()
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        print("hello, I am pc. Connecting to server...")
        if self.connect_to_server():
            print("yes, I connected to server")
        else:
            print("no, I did not connect to server")
        pass

    def connect_to_server(self):
        self.sock.connect(('localhost', 9090))
        zip_data = pickle.dumps(dict(cmd=pc_connect_to_ser, data=b"0", size_next_message=self.size_next_mess))
        self.sock.send(zip_data)
        buffer = self.sock.recv(self.size_next_mess)
        answer = pickle.loads(buffer)
        if answer['cmd'] == answ_ser_connect_to_pc:
            print("Подключился к серверу")
            logging.info("Подключился к серверу")
            return True
        else:
            print("Сервер недоступен")
            logging.info("Сервер недоступен")
            return False

    def send_message(self, cmd, data=b""):
        message = dict(cmd=cmd, data=data, size_next_message=self.size_next_mess)
        zip_data = pickle.dumps(message)
        self.sock.send(zip_data)

    def listen_server(self):
        self.sock.listen()
        while True:
            data = self.sock.recv(self.size_next_mess)
            if not data:
                continue
            message = pickle.loads(data)
            if message['cmd'] == answ_ser_connect_to_pc:
                print("yes, connect")
                logging.info("Сервер подключился ко мне снова, зачем?")
            elif message['cmd'] == app_test_cmd:
                print("Получил тестовую команду от приложения")
                self.send_message(answ_pc_test_cmd, b"Hello! I am notebook!")
            elif message['cmd'] == answ_app_test_cmd:
                print("Получил ответ на свою тестовую команду от приложения")
                print(message['data'])

    def run(self):
        while True:
            cmd = input()
            if cmd == 7:
                self.connect_to_server()
            elif cmd == pc_test_cmd:
                self.send_message(pc_connect_to_ser, b"Hello, I am PC")
            elif cmd == 9:
                self.sock.close()
            elif cmd == 8:
                exit()
        pass

if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()