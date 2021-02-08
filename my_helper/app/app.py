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
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        layout = BoxLayout(padding=10)
        for i in range(5):
            btn = Button(text="Button #%s" % (i + 1), color=blue)
            layout.add_widget(btn)
        self.connect_to_server()
        return layout

    def connect_to_server(self):
        sock = socket.socket()
        sock.connect(('localhost', 9090))
        zip_data = pickle.dumps(dict(cmd=1, )
        sock.send(zip_data)
        data = sock.recv(1024)
        answer = pickle.loads(data)
        if answer['cmd'] == 2:
            logging.info("Подключился к серверу")


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()