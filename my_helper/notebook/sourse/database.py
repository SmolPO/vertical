from my_helper.notebook.sourse.inserts import get_from_db, my_update, add_to_db
import psycopg2
import datetime as dt
from configparser import ConfigParser
from PyQt5.QtCore import QDate as Date
import logging
from PyQt5.QtWidgets import QMessageBox as mes
path_conf = "B:/my_helper/my_config.ini"
empty = "(нет)"
si = ["тн", "т", "кг", "м2", "м", "м/п", "мм", "м3", "л", "мм", "шт"]
count_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
statues = ["работает", "отпуск", "уволен"]
my_errors = {"1_get_ui": "Не удалось найти файл дизайна",
             "2_get_ini": "Не удалось получить данные из config: ",
             "3_get_db": "Не удалось получить данные из Базы данных",
             "4_get_file": " Файл не найден",
             "5_get_next_id": "Не удалось получить следущий номер",
             "6_get_sheet": "Не странице в файле ",
             "7_conn": "Нет подключения к базе данных",
             "8_init_list": "Не удалось получить данные из Базы данных",
             "9_commit": "Не удалось добавить данные в базу данных",
             "10_update": "Не удалось обновить данные в базе данных",
             "11_kill": "Не удалось удалить данные из базы данных",
             "12_web": "Не удалось открыть ссылку ",
             "13_full_all_fields": "Заполните все поля",
             "14_add_people": "Добавьте сотрудников",
             "15_add_contract": "Добавьте договор"}


class DataBase:
    def __init__(self, path):
        path_conf = path
        self.db = None
        self.conn = None
        self.cursor = None
        config = ConfigParser()
        config.read(path_conf)
        try:
            self.ip = config.get('database', 'ip')
            self.name_db = config.get('database', 'name_db')
            self.user_db = config.get('database', 'user_db')
            self.password_db = config.get('database', 'password_db')
        except:
            return

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(dbname=self.name_db, user=self.user_db, password=self.password_db, host=self.ip)
            if not self.conn:
                return False
            self.cursor = self.conn.cursor()
            return True
        except:
            print("Нет соединения с базой данных по интернету")
            return False

    def get_data(self, fields, table):
        row = get_from_db(fields, table)
        print(row)
        self.execute(row)

        return self.cursor.fetchall()
        try:
           pass
        except:
            print(row)
            print("Не удалось получить данные из БД")
            return []

    def execute(self, text):
        self.cursor.execute(text)
        try:
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
        rows = self.get_data(fields, table)
        if not rows and rows != []:
            return False
        if not people:
            for row in rows:
                item.addItems([row[-1] + ". " + row[0]])
            return rows
        else:
            for row in rows:
                item.addItems([str(row[-1]) + ". " + short_name(row[:3])])
            return rows

    def my_update(self, data, table):
        self.cursor.execute(my_update(data, table))
        self.conn.commit()
        try:
            pass
        except:
            print("Не удалось обновить данные")

    def kill_value(self, my_id, table):
        self.execute("DELETE FROM {0} WHERE id = '{1}'".format(table, my_id))
        self.conn.commit()
        try:
            pass
        except:
            return

    def new_note(self, date, name, number):
        self.my_commit(add_to_db((date, name, number), "notes"))

    def create_db(self):
        conn = psycopg2.connect(dbname=self.name_db, user=self.user_db, password=self.password_db, host=self.ip)
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
            "CREATE TABLE notes (date text, name text, id text)",
            "CREATE TABLE asrs (work text, value text, si text, material text, days text, month text, year text, "
            "boss_1 text, boss_2 text, boss_3 text, boss_4 text, contract text, id text)"]
        g = iter(range(len(list_db_)))
        for item in list_db_:
            try:
                db.execute(item)
                conn.commit()
                print(str(next(g)) + " OK item" + item[13:20])
            except:
                print("ERROR " + item)
        print("Create " + str(next(g)) + " database!")


def get_path(my_type):
    config = ConfigParser()
    config.read(path_conf, encoding="utf-8")
    return str(config.get('path', my_type))


def get_config(my_type):
    config = ConfigParser()
    config.read(path_conf, encoding="utf-8")
    try:
        return config.get('config', my_type)
    except:
        print("get_config")
        return False


def get_from_ini(my_type, part):
    config = ConfigParser()
    config.read(path_conf, encoding="utf-8")
    try:
        return config.get(part, my_type)
    except:
        print("get_from_ini")
        return False


def get_path_ui(my_type):
    return get_from_ini("ui_files", "ui_files") + get_from_ini(my_type, "ui_files")


def get_next_number():
    config = ConfigParser()
    config.read(path_conf)
    number_note = config.get('config', 'number')
    next_number = int(number_note) + 1
    return int(number_note)


def set_next_number(n):
    config = ConfigParser()
    config.read(path_conf)
    number_note = config.get('config', 'number')
    next_number = n
    config.set("config", 'number', str(next_number))
    with open(path_conf, 'w') as configfile:
        config.write(configfile)
    return int(number_note)


def short_name(data):
    print(data)
    return data[0] + " " + data[1][0] + "." + data[2][0] + "."


def time_delta(date_1, date_2):
    if date_1 == "now":
        a = dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)
    else:
        a = dt.datetime(int(date_1[6:]), int(date_1[3:5]), int(date_1[:2]))
    b = dt.datetime(int(date_2[6:]), int(date_2[3:5]), int(date_2[:2]))
    return (a - b).days


def msg(widgets, text):
    mes.question(widgets, "Сообщение", text, mes.Cancel)
    return False


def from_str(date):
    symbols = [".", ",", "-", "/", "_"]
    for item in symbols:
        tmp = date.split(item)
        if len(tmp) == 3:
            if len(tmp[0]) == 4:
                return Date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            if len(tmp[2]) == 4:
                return Date(int(tmp[2]), int(tmp[1]), int(tmp[0]))


def yong_date(young, old):
    if int(young[6:10]) > int(old[6:10]):
        return True
    if int(young[6:10]) < int(old[6:10]):
        return False

    if int(young[2:4]) > int(old[2:4]):
        return True
    if int(young[2:4]) < int(old[2:4]):
        return old

    if int(young[:2]) > int(old[:2]):
        return True
    if int(young[:2]) < int(old[:2]):
        return False

    else:
        return False


def get_val(ui):
    return "".join(ui.currentText().split(". ")[1:])


zero = from_str("01.01.2000")