from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

import random
import socket
import pickle
import logging
import configparser
import threading
import webbrowser
import os
import sys

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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('../designer_ui/main_menu.ui', self)
        self.b_pass_week.clicked.connect(self.ev_pass_week)
        self.b_pass_month.clicked.connect(self.ev_pass_month)
        self.b_pass_auto.clicked.connect(self.ev_pass_auto)
        self.b_pass_recover.clicked.connect(self.ev_pass_recover)
        self.b_pass_unlock.clicked.connect(self.ev_pass_unlock)
        self.b_pass_issue.clicked.connect(self.ev_pass_issue)
        self.b_new_person.clicked.connect(self.ev_new_person)
        self.b_new_bill.clicked.connect(self.ev_new_bill)
        self.b_new_build.clicked.connect(self.ev_new_build)
        self.b_new_boss.clicked.connect(self.ev_new_boss)
        self.b_create_act.clicked.connect(self.ev_create_act)
        self.b_get_material.clicked.connect(self.ev_get_material)
        self.b_pdf_check.clicked.connect(self.ev_pdf_check)
        self.b_send_covid.clicked.connect(self.ev_send_covid)

    def ev_pass_week(self):
        print("pass week")

    def ev_pass_month(self):
        print("pass month")

    def ev_pass_auto(self):
        print("pass auto")

    def ev_pass_recover(self):
        print("pass rec")

    def ev_pass_issue(self):
        print("pass issue")

    def ev_pass_unlock(self):
        print("pass unlock")

    def ev_new_boss(self):
        print("new boss")

    def ev_new_bill(self):
        print("new bill")

    def ev_new_build(self):
        print("new build")

    def ev_new_person(self):
        print("new person")

    def ev_create_act(self):
        print("create act")

    def ev_get_material(self):
        print("get mat")

    def ev_pdf_check(self):
        print("pdf check")

    def ev_send_covid(self):
        print("send covid")







class Notebook:
    def __init__(self):
        self.sock = socket.socket()
        self.config = configparser.ConfigParser()
        self.size_next_mess = 1024
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.handler = threading.Thread(target=self.listen_server)
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
            self.handler.start()
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
        while True:
            data = self.sock.recv(self.size_next_mess)
            if not data:
                continue
            message = pickle.loads(data)
            cmd = message['cmd']
            if cmd == answ_ser_connect_to_pc:
                print("yes, connect")
                logging.info("Сервер подключился ко мне снова, зачем?")
            elif cmd == app_test_cmd:
                print("Получил тестовую команду от приложения")
                self.send_message(answ_pc_test_cmd, b"Hello! I am notebook!")
            elif cmd == answ_app_test_cmd:
                print("Получил ответ на свою тестовую команду от приложения")
                print(message['data'])
            elif cmd == app_on_music:
                self.on_music()
                self.send_message(answ_pc_on_music, b"may be PC play music")
            elif cmd == app_open_scan:
                os.startfile(r'C:/Program Files/Pantum/ptm6500/PushScan/ptm6500app.exe')
                self.send_message(answ_pc_open_scan, b"may be PC start scan")

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

    def on_music(self):
        webbrowser.open('http://atmoradio.ru/')  # Go to example.com
        return True


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
