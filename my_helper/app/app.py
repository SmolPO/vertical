import kivy
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import socket
import pickle
import logging
import configparser
from ..server.commands import *

red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]


class HBoxLayoutExample(App):
    def build(self):
        self.sock = socket.socket()
        logging.basicConfig(filename="log_file.log", level=logging.INFO)

        layout = BoxLayout(padding=10)
        btn_test = Button(text="Test", color=blue)
        btn_test.bind(on_press=self.btn_test_cmd)
        btn_conn = Button(text="Server", color=blue)
        btn_conn.bind(on_press=self.btn_connect_cmd)
        layout.add_widget(btn_conn)
        layout.add_widget(btn_test)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.connect_to_server()
        return layout

    def btn_test_cmd(self):
        self.send_message(app_test_cmd)

    def btn_connect_cmd(self):
        self.send_message(app_connect_to_ser)

    def connect_to_server(self):
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        self.sock.connect(('localhost', 9090))
        self.send_message(app_connect_to_ser)
        buffer = self.sock.recv(self.size_next_mess)
        answer = pickle.loads(buffer)
        if answer['cmd'] == answ_ser_connect_to_app:
            self.size_next_mess = answer['size_next_message']
            logging.info("Подключился к серверу")
        else:
            logging.info("Сервер недоступен")

    def send_message(self, cmd, data=b"0"):
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
            if message['cmd'] == answ_ser_connect_to_app:
                print('yes, connect')
                logging.info("Сервер подключился ко мне снова, зачем?")
            elif message['cmd'] == pc_test_cmd:
                self.send_message(answ_app_test_cmd, b"hello, I am app!")
                print(message['data'])
            elif message['cmd'] == answ_pc_test_cmd:
                print(message['data'])


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()