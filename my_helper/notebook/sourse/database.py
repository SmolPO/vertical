from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from my_helper.notebook.sourse.inserts import get_from_db
import psycopg2


class DataBase:
    def __init__(self):
        self.db = None
        self.conn = None
        self.cursor = None
        self.key_for_db = "host=95.163.249.246 dbname=Vertical_db user=office password=9024EgrGvz#m87Y1"

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(self.key_for_db)
            if not self.conn:
                return False
            self.cursor = self.conn.cursor()
            return True
        except:
            print("Внимание, нет соединения с базой данных по интернету")
            return False
            # QMessageBox.question(self, "Внимание", "Нет соединения с базой данных по интернету", QMessageBox.Ok)

    def get_data(self, fields, table):
        try:
            self.db.execute(get_from_db(fields, table))
        except:
            print("Разрыв соединения, пробуем переподключиться...")
            try:
                self.connect_to_db()
                self.db.execute(get_from_db(fields, table))
                return self.db.fetchall()
            except:
                print("Внимание, нет соединения с базой данных по интернету")
                return None
        return self.db.fetchall()

    def execute(self, text):
        try:
            self.conn.execute(text)
            return True
        except:
            print("Разрыв соединения, пробуем переподключиться...")
            try:
                self.connect_to_db()
                self.conn.execute(text)
                return True
            except:
                print("Внимание, нет соединения с базой данных по интернету")
                return False

    def my_commit(self, data, query):
        if data:
            print(data)
            try:
                self.db.execute(query)
                self.conn.commit()
            except:
                print("Разрыв соединения, пробуем переподключиться...")
                try:
                    self.connect_to_db()
                    self.db.execute(query)
                    self.conn.commit()
                except:
                    print("Внимание, нет соединения с базой данных по интернету")
            print("OK")

