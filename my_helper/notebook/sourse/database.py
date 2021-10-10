from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from my_helper.notebook.sourse.inserts import get_from_db, my_update
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
            print("Нет соединения с базой данных по интернету")
            return False
            # QMessageBox.question(self, "Внимание", "Нет соединения с базой данных по интернету", QMessageBox.Ok)

    def get_data(self, fields, table):
        """        except:
            print("Разрыв соединения, пробуем переподключиться...")
            try:
                self.connect_to_db()
                self.execute(get_from_db(fields, table))
                return self.db.fetchall()
            except:
                print("Внимание, нет соединения с базой данных по интернету")
                return None"""
        row = get_from_db(fields, table)
        try:
            self.execute(row)
            return self.cursor.fetchall()
        except:
            print(row)
            print("Не удалось получить данные из БД")
            return

    def execute(self, text):
        """except:
                   print("Разрыв соединения, пробуем переподключиться...")
                   try:
                       self.connect_to_db()
                       self.conn.execute(text)
                       return True
                   except:
                       print("Внимание, нет соединения с базой данных по интернету")
                       return False"""
        try:
            self.cursor.execute(text)
        except:
            print(text)
            print("Не удалось выполнить запрос")
            return False
        return True

    def get_next_id(self, table):
        rows = self.get_data("id", table)
        if not rows:
            return 1
        return int(max(rows)[0]) + 1

    def my_commit(self, data):
        if data:
            try:
                print(data)
                self.connect_to_db()
                self.cursor.execute(data)
                self.conn.commit()

            except:
                print("Не удалось сделать коммит.")
            print("OK")

    def init_list(self, item, fields, table, people=False):
        rows = self.get_data(fields, table)
        item.addItems(["(нет)"])
        if not rows and rows != []:
            return False
        if not people:
            for row in rows:
                item.addItems([row[0]])
            return rows
        else:
            for row in rows:
                item.addItems([row[0] + " " + ".".join([row[1][0], row[2][0]]) + "."])
            return rows

    def my_update(self, data, table):
        print(data)
        try:
            self.cursor.execute(my_update(data, table))
            self.conn.commit()
        except:
            print("Не удалось обновить данные")

    def kill_value(self, my_id, table):
        self.execute("DELETE FROM {0} WHERE id = '{1}'".format(table, my_id))
        self.conn.commit()
