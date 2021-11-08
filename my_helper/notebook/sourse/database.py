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

ERR = -1

GET_UI = "Не удалось найти файл дизайна: "
GET_INI = "Не удалось получить данные из config: "
GET_FILE = "Не удалось найти файл: "
GET_PAGE = "Нет странице в файле: "
GET_DB = "Не удалось получить данные из Базы данных"
GET_NEXT_ID = "Ошибка при работе с БД"
LOAD_UI = "Не удалось загрузить файл дизайна"
CREATE_FOLDER = "Не удалось создать папку: "
CONNECT_DB = "Нет подключения к базе данных"
UPDATE_DB = "Не удалось обновить данные в базе данных"
KILL_DB = "Не удалось удалить данные из базы данных"
ADD_DB = "Не удалось добавить данные в базу данных"
FULL_ALL = "Заполните все поля"
ADD_CONTRACT = "Добавьте договор"
ADD_PEOPLE = "Добавьте сотрудников"
OPEN_WEB = "Не удалось открыть ссылку "
BIG_INDEX = "Ошибка: big index"
PERMISSION_ERR = "Проблема с правом доступа. " \
                 " 1. - вручную скопируйте файл в папку со счетами," \
                 " 2 - Снова нажмите Выбрать файл и укажите файл чека в новом месте"

CREATE_DB = "База данных успешно создана"
CREATE_DOCS = "Не удалось создать файлы с документацией"
CREATE_ACT = "Не удалось создать исполнительную"
CREATE_JOURNAL = "Не удалось создать журнал"
WRONG_DATE = "Дата начала старше даты окончания договора"
CHECK_COVID = "Не правильно заполнены данные по вакцинации"

KILLD_NOTE = "Запись удалена"
KILL_NOTE = "Вы действительно хотите удалить запись: "
CHANGED_NOTE = "Запись изменена"
CHANGE_NOTE = "Вы действительно хотите изменить запись на "
YES = "да"
NO = "нет"
PLACE_VAC = "Укажите место прививки"
OLD_DOC = "Сертификат устарел. С даты получения прошло более, чем {0} дней."
ERR_VAC_MANY = "Между прививками прошло {0} дней. Это менее {1} дней"
ERR_VAC_MACH = "Между прививками прошло {0} дней. Это менее {1} дней"
NUMBER_DOC = "Укажите номер сертификата"

SPUTNIK = "2 дозы"
SP_LITE = "1 доза"
COVID = "болел"

dictionary = {"Производитель работ": {"gent": "прооизводителя работ", "datv": "прооизводителю работ"},
              "Технический директор": {"gent": "технического директора", "datv": "техническому директору"}}


class DataBase:
    def __init__(self, parent, path):
        self.parent = parent
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
                return msg_er(self.parent, CONNECT_DB)
            self.cursor = self.conn.cursor()
            if not self.cursor:
                return msg_er(self.parent, CONNECT_DB)
        except:
            return msg_er(self.parent, CONNECT_DB)

    def get_data(self, fields, table):
        try:
            row = get_from_db(fields, table)
            self.execute(row)
            return self.cursor.fetchall()
        except:
            return msg_er(self.parent, GET_DB)

    def execute(self, text):
        try:
            self.cursor.execute(text)
        except:
            return msg_er(self.parent, GET_DB)
        return True

    def get_next_id(self, table):
        try:
            rows = self.get_data("id", table)
            if not rows:
                return 1
            return int(max(rows)[0]) + 1
        except:
            return msg_er(self.parent, GET_NEXT_ID)

    def my_commit(self, data):
        if data:
            try:
                self.connect_to_db()
                self.cursor.execute(data)
                self.conn.commit()
                return True
            except:
                return msg_er(self.parent, ADD_DB)

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
        try:
            self.cursor.execute(my_update(data, table))
            self.conn.commit()
        except:
            return msg_er(self.parent, UPDATE_DB)

    def kill_value(self, my_id, table):
        try:
            self.execute("DELETE FROM {0} WHERE id = '{1}'".format(table, my_id))
            self.conn.commit()
        except:
            return msg_er(self.parent, KILL_DB)

    def new_note(self, date, name, number):
        self.my_commit(add_to_db((date, name, number), "notes"))

    def create_db(self):
        try:
            conn = psycopg2.connect(dbname=self.name_db, user=self.user_db, password=self.password_db, host=self.ip)
            db = conn.cursor()
        except:
            return msg_er(self.parent, CONNECT_DB)
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
            except:
                print("ERROR " + item)
        msg_info(self.parent, CREATE_DB)


class Ini:
    def __init__(self, parent):
        self.parent = parent

    def get_path(self, my_type):
        try:
            config = ConfigParser()
            config.read(path_conf, encoding="utf-8")
            return str(config.get('path', my_type))
        except:
            return msg_er(self, GET_INI)

    def get_config(self, my_type):
        config = ConfigParser()
        config.read(path_conf, encoding="utf-8")
        try:
            return config.get('config', my_type)
        except:
            return msg_er(self, GET_INI)

    def get_from_ini(self, my_type, part):
        config = ConfigParser()
        config.read(path_conf, encoding="utf-8")
        try:
            return config.get(part, my_type)
        except:
            return msg_er(self, GET_INI)

    def get_path_ui(self, my_type):
        path_2 = self.get_from_ini(my_type, "ui_files")
        path_1 = self.get_from_ini("ui_files", "ui_files")
        if path_1 and path_2:
            return path_1 + path_2
        else:
            return msg_er(self, GET_INI)

    def get_next_number(self):
        try:
            config = ConfigParser()
            config.read(path_conf)
            number_note = config.get('config', 'number')
            next_number = int(number_note) + 1
            return int(number_note)
        except:
            return msg_er(self, GET_INI)

    def set_next_number(self, n):
        try:
            config = ConfigParser()
            config.read(path_conf)
            number_note = config.get('config', 'number')
            next_number = n
            config.set("config", 'number', str(next_number))
            with open(path_conf, 'w') as configfile:
                config.write(configfile)
            return int(number_note)
        except:
            return msg_er(self, GET_INI)


def short_name(data):
    print(data)
    print(data[0] + " " + data[1][0] + "." + data[2][0] + ".")
    return data[0] + " " + data[1][0] + "." + data[2][0] + "."


def time_delta(date_1, date_2):
    if date_1 == "now":
        a = dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)
    else:
        a = dt.datetime(int(date_1[6:]), int(date_1[3:5]), int(date_1[:2]))
    b = dt.datetime(int(date_2[6:]), int(date_2[3:5]), int(date_2[:2]))
    return (a - b).days


logging.basicConfig(filename=Ini("").get_path("path") + "/log_file.log", level=logging.INFO)


def msg_er(widgets, text):
    mes.question(widgets, "Сообщение", text, mes.Cancel)
    logging.info(text + str(dt.datetime.now()))
    return -1


def msg_info(widgets, text):
    mes.question(widgets, "Сообщение", text, mes.Cancel)
    return True


def msg_q(widgets, text):
    return mes.question(widgets, "Сообщение", text, mes.Ok | mes.Cancel)


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


def get_index(cb, text):
    for ind in range(cb.count()):
        cb.setCurrentIndex(ind)
        if text in cb.currentText():
            return ind
    return -1


zero = from_str("01.01.2000")