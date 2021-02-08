import kivy
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import socket
import pickle
import logging
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
        for i in range(5):
            btn = Button(text="Button #%s" % (i + 1), color=blue)
            layout.add_widget(btn)
        self.connect_to_server()
        return layout

    def connect_to_server(self):
        self.size_next_mess = 0
        self.sock.connect(('localhost', 9090))
        zip_data = pickle.dumps(dict(cmd=app_connect_to_ser, next_mes=0))
        self.sock.send(zip_data)
        data = self.sock.recv(1024)
        answer = pickle.loads(data)
        if answer['cmd'] == ser_connect_to_app:
            self.size_next_mess = answer['next_mess']
            logging.info("Подключился к серверу")
        else:
            logging.info("Сервер недоступен")

    def send_message(self, cmd, data):
        message = dict(cmd=cmd, data=data, from_=1, size_next_message=10)
        zip_data = pickle.dumps(message)
        self.sock.send(zip_data)

    def listen_server(self):
        self.sock.listen()
        while True:
            data = self.sock.recv(self.size_next_mess)
            if not data:
                continue
            receive_data = pickle.loads(data)
            if receive_data['cmd'] == ser_connect_to_app:
                self.send_message(ser_connect_to_app, self.size_next_mess)
                logging.info("Сервер подключился ко мне снова, зачем?")

            elif receive_data['cmd'] == ser_test_cmd:
                print(receive_data['data'])


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()