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
        self.conn = dict(sock_app=None, sock_pc=None, adr_app=None, adr_pc=None)
        logging.basicConfig(filename="log_file.log", level=logging.INFO)
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')
        self.size_next_mess = int(self.config.get("server", "size_first_mes"))
        logging.info("Сервер создан")

    def close(self):
        self.conn['sock_app'].close()
        self.conn['sock_pc'].close()

    def send_message(self, cmd, where, data=0, size_next=1024):
        message = dict(cmd=cmd, data=data, size_next_message=size_next)
        zip_message = pickle.dumps(message)
        key = 'sock_app' if where == to_app else to_pc
        self.conn[key].send(zip_message)

    def listener(self, source):
        key = 'sock_app' if source == from_app else from_pc
        conn, adr = self.conn[key], self.conn[key]
        while True:
            message = pickle.loads(conn.recv(self.size_next_mess))  # TODO проверка на успешное преобразование
            if not message:
                continue
            else:
                self.my_queue.append(message)
                threading.Thread(target=self.queue_worker()).start()

    def queue_worker(self):
        message = self.my_queue.pop()
        if message['cmd'] == app_connect_to_ser:
            self.send_message(answ_ser_connect_to_app, to_app)
        elif message['cmd'] == pc_connect_to_ser:
            self.send_message(answ_ser_connect_to_pc, to_pc)
        elif message['cmd'] == app_test_cmd:
            self.send_message(app_test_cmd, to_pc)
        elif message['cmd'] == pc_test_cmd:
            self.send_message(pc_test_cmd, to_app)
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
                self.my_queue.append(message)
                threading.Thread(target=self.listener, args="app").start()
                threading.Thread(target=self.queue_worker()).start()
            elif message['cmd'] == pc_connect_to_ser:
                self.conn['sock_pc'] = conn
                self.conn['adr_pc'] = adr
                threading.Thread(target=self.listener, args="pc").start()
                self.my_queue.append(message)
                threading.Thread(target=self.queue_worker()).start()
            else:
                conn.send(b'go to city Nachuy')
                logging.info("Левое подключение")
                conn.close()

if __name__ == '__main__':
    app = Server()
    app.run()