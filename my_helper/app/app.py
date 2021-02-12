import kivy
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import socket
import pickle
import logging
import configparser
import threading

# команда App
app_connect_to_ser = 1
app_test_cmd = 2
to_app = "pc"
from_app = "app"
answ_pc_test_cmd = 5
app_on_music = 6
app_open_scan = 7

# команда Notebook
pc_connect_to_ser = 101
pc_test_cmd = 102
to_pc = 103
from_pc = 104
answ_app_test_cmd = 105
answ_pc_on_music = 106
answ_pc_open_scan = 107
answ_pc_errore = 404

# команда Server
answ_ser_connect_to_pc = 201
answ_ser_connect_to_app = 202
answ_ser_test_cmd = 203

red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]


class HBoxLayoutExample(App):
    def build(self):
        self.sock = socket.socket()
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.is_connect_to_pc = False
        layout = BoxLayout(padding=10)
        btn_test = Button(text="Test", color=blue)
        btn_test.bind(on_press=self.btn_test_cmd)
        btn_conn = Button(text="Server", color=blue)
        btn_conn.bind(on_press=self.btn_connect_cmd)
        layout.add_widget(btn_conn)
        layout.add_widget(btn_test)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        self.handler = threading.Thread(target=self.listen_server)

        return layout

    def btn_test_cmd(self, instance):
        self.send_message(app_test_cmd)

    def btn_connect_cmd(self, instance):
        self.connect_to_server()

    def btn_on_music(self, instance):
        self.send_message(app_on_music) if self.is_connect_to_pc else logging.info("pc is not connect")

    def btn_open_scan(self, instance):
        self.send_message(app_open_scan) if self.is_connect_to_pc else logging.info("pc is not connect")
        pass

    def btn_create_post_message(self, instance):
        email = input("input email")
        subject = input("input subject")
        text = input("input text")
        self.connect_to_email()
        self.send_post(email=email, sub=subject, text=text)
        pass

    def connect_to_email(self):

        pass

    def send_post(self, email, sub, text):

        pass

    def connect_to_server(self):
        self.sock.connect(('localhost', 9090))
        self.send_message(app_connect_to_ser)
        buffer = self.sock.recv(self.size_next_mess)
        answer = pickle.loads(buffer)
        if answer['cmd'] == answ_ser_connect_to_app:
            self.size_next_mess = answer['size_next_message']
            logging.info("Подключился к серверу")
            self.handler.start()
        else:
            logging.info("Сервер недоступен")

    def send_message(self, cmd, data=b"0"):
        message = dict(cmd=cmd, data=data, size_next_message=self.size_next_mess)
        zip_data = pickle.dumps(message)
        self.sock.send(zip_data)

    def listen_server(self):
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
            elif message['cmd'] == answ_pc_on_music or answ_pc_errore:
                print(message['data'])


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()