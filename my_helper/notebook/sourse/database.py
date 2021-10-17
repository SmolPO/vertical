from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
from my_helper.notebook.sourse.inserts import get_from_db, my_update, add_to_db
import config
import psycopg2
from configparser import ConfigParser


class DataBase:
    def __init__(self):
        self.db = None
        self.conn = None
        self.cursor = None
        config = ConfigParser()
        config.read('config.ini')
        self.ip = config.get('config', 'ip')
        self.name_db = config.get('config', 'name_db')
        self.user_db = config.get('config', 'user_db')
        self.password_db = config.get('config', 'password_db')

    def connect_to_db(self):
        self.conn = psycopg2.connect(dbname="Company",
                                     user="postgres",
                                     password="pol_ool_123",
                                     host="localhost")
        try:

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
        self.execute(row)
        try:
           # self.execute(row)
            return self.cursor.fetchall()
        except:
            print(row)
            print("Не удалось получить данные из БД")
            return []

    def execute(self, text):
        self.cursor.execute(text)
        try:
           # self.cursor.execute(text)
            pass
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
        print(data)
        self.connect_to_db()
        self.cursor.execute(data)
        self.conn.commit()
        if data:
            try:
                pass
            except:
                print("Не удалось сделать коммит.")
            print("OK")

    def init_list(self, item, fields, table, people=False):
        rows = self.get_data("*", table)
        item.addItems(["(нет)"])
        if not rows and rows != []:
            return False
        if not people:
            for row in rows:
                item.addItems([row[-1] + ". " + row[0]])
            return rows
        else:
            for row in rows:
                item.addItems([str(row[-1]) + ". " + str(row[0]) + " " + ".".join([str(row[1][0]), str(row[2][0])]) + "."])
            return rows

    def my_update(self, data, table):
        print(data)
        self.cursor.execute(my_update(data, table))
        self.conn.commit()
        try:
            pass
        except:
            print("Не удалось обновить данные")

    def kill_value(self, my_id, table):
        self.execute("DELETE FROM {0} WHERE id = '{1}'".format(table, my_id))
        self.conn.commit()

    def new_note(self, date, name, number):
        self.my_commit(add_to_db((date, name, number), "notes"))

    def create_db(self):
        conn = psycopg2.connect(dbname='Company',
                                user='postgres',
                                password='pol_ool_123',
                                host='localhost')
        db = conn.cursor()
        list_db_ = [
            "CREATE TABLE contracts (name text, customer text, number text, date text, object text, type_work text, "
            "place text, id text)",
            "CREATE TABLE bosses (family text, name text, surname text, post text, email text, phone text, sex text"
            ", id text)",
            "CREATE TABLE drivers (family text, name text, surname text, birthday text, passport text, adr text,"
            " id text)",
            "CREATE TABLE company (company text, adr text, ogrn text, inn text, kpp text, bik text, korbill text, "
            "rbill text, bank text, family text, name text, surname text, post text, count_attorney text,"
            "date_attorney text, id text)",
            "CREATE TABLE auto (model text, brand text, gov_number text, track_number text, id text)",
            "CREATE TABLE drivers (family text, name text, surname text, birthday text, passport text, adr text,"
            " id text)",
            "CREATE TABLE contracts (name text, customer text, number text, date text, object text, type_work text, "
            "place text, id text)",
            "CREATE TABLE bosses (family text, name text, surname text, post text, email text, phone text, sex text,"
            " id text)",
            "CREATE TABLE musics (name text, link text, id text)",
            "CREATE TABLE materials (name text, measure text, value text, provider text, contract text, id text)",
            "CREATE TABLE workers (family text, name text, surname text, birthday text, post text, phone text, "
            "passport text, passport_got text, adr text, live_adr text, inn text, snils text, numb_contract text, "
            "date_contract text, numb_h text, numb_group_h text, date_h text, numb_study text, numb_study_card text,"
            "d_study text, numb_protocol text, numb_card text, d_protocol text, object text, id text)",
            "CREATE TABLE itrs (family text, name text, surname text, post text, passport text, passport_date text, "
            "passport_got text, adr text, live_adr text, auto text, inn text, "
            "snils text, n_employment_contract text, date_employment_contract text, "
            "ot_protocol text, ot_date text, ot_card text, "
            "PTM_protocol text, PTM_date text, PTM_card text, "
            "es_protocol text, es_group text, es_card text, es_date text, "
            "h_protocol text, h_date text, h_group text, h_card text, "
            "industrial_save text, "
            "st_protocol text, st_card text, st_date text, birthday text, id text)",
            "CREATE TABLE finance (id text, date text, value text, recipient text, comment text, id text)",
            "CREATE TABLE bills (date text, value text, buyer text, name_file text, comment text, id text)",
            "CREATE TABLE notes (date text, name text, id text)"]
        g = iter(range(len(list_db_)))
        for item in list_db_:
            try:
                db.execute(item)
                conn.commit()
                print(str(next(g)) + " OK item" + item[13:20])
            except:
                print("ERROR " + item)
        print("Create " + str(next(g)) + " database!")
