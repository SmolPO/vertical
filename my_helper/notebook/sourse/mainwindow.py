from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QMessageBox
import sys
import os
import requests
import logging
from datetime import datetime as dt
from configparser import ConfigParser
import openpyxl
import psycopg2
from my_helper.notebook.sourse.new_boss import NewBoss
from my_helper.notebook.sourse.new_itr import NewITR
from my_helper.notebook.sourse.new_worker import NewWorker
from my_helper.notebook.sourse.nw_company import NewCompany
from my_helper.notebook.sourse.new_auto import NewAuto
from my_helper.notebook.sourse.new_driver import NewDriver
from pdf_module import check_file, create_covid
from my_helper.notebook.sourse.new_contract import NewContact
from my_helper.notebook.sourse.material import NewMaterial
from my_email import send_post
from my_helper.notebook.sourse.pass_week import WeekPass
from my_helper.notebook.sourse.pass_unlock import UnlockPass
from my_helper.notebook.sourse.pass_month import MonthPass
from my_helper.notebook.sourse.pass_get import GetPass
from my_helper.notebook.sourse.pass_auto import AutoPass
from my_helper.notebook.sourse.pass_drive import DrivePass
from my_tools import Notepad
from music import Music
import inserts as ins
import config as conf
"""
План
1. Добавление в БД сотрудника (изменил форму)
2. Добавление прорабов
3. Формирование служебок
4. модуль сканирование
5. формирование приказов
6. блокнот и уведомления
7. склад, накладные
8. чеки
9. отправка писем по почте
10. деньги на ТК
Срок к концу недели
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('../designer_ui/main_menu.ui', self)
        print("pass")
        self.b_pass_week.clicked.connect(self.ev_btn_create_pass)
        self.b_pass_month.clicked.connect(self.ev_btn_create_pass)
        self.b_pass_auto.clicked.connect(self.ev_btn_create_pass)
        self.b_pass_drive.clicked.connect(self.ev_btn_create_pass)
        self.b_pass_unlock.clicked.connect(self.ev_btn_create_pass)
        self.b_pass_issue.clicked.connect(self.ev_btn_create_pass)
        # create
        self.b_new_person.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_bill.clicked.connect(self.ev_new_bill)
        self.b_new_build.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_boss.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_itr.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_invoice.clicked.connect(self.ev_btn_start_file)
        self.b_new_company.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_auto.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_driver.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_material.clicked.connect(self.ev_btn_add_to_db)

        self.b_create_act.clicked.connect(self.ev_create_act)
        self.b_pdf_check.clicked.connect(self.ev_pdf_check)
        self.b_send_covid.clicked.connect(self.ev_send_covid)
        self.b_connect.clicked.connect(self.ev_connect)

        self.b_journal.clicked.connect(self.ev_btn_start_file)
        self.b_tabel.clicked.connect(self.ev_btn_start_file)
        self.b_scan.clicked.connect(self.ev_btn_start_file)
        self.b_attorney.clicked.connect(self.ev_btn_start_file)
        self.b_invoice.clicked.connect(self.ev_btn_start_file)
        # self.cb_builds.activated[str].connect(self.change_build)
        self.b_notepad.clicked.connect(self.ev_btn_start_file)
        self.b_music.clicked.connect(self.ev_btn_add_to_db)

        self.get_param_from_widget = None
        self.current_build = "Объект"
        self.company = 'ООО "Вертикаль"'
        self.customer = 'ПАО "Дорогобуж"'
        self.new_worker = []
        self.data_to_db = None

        self.ui_l_company.setText(self.company)
        # self.ui_l_build.setText(self.current_build)
        self.config = ConfigParser()
        self.init_notif()

        # Database
        self.connect_to_db()
        self.test_func()
        self.get_weather()

    def test_func(self):
        self.b_create_act.setEnabled(False)
        self.b_pdf_check.setEnabled(False)
        self.b_send_covid.setEnabled(False)
        self.b_connect.setEnabled(False)
        self.b_new_invoice.setEnabled(False)
        self.b_new_bill.setEnabled(False)

    def change_build(self, text):
        self.ui_l_cur_build.setText(text)
        self.ui_l_cur_build.adjustSize()

    def ev_btn_create_pass(self):
        name = self.sender().text()
        wnd = None
        if name == "Продление на месяц":
            wnd = MonthPass(self)
        elif name == "Пропуск на выходные":
            wnd = WeekPass(self)
        elif name == "Разблокировка пропуска":
            wnd = UnlockPass(self)
        elif name == "Выдать пропуск":
            wnd = GetPass(self)
        elif name == "Продление на машину":
            wnd = AutoPass(self)
        elif name == "Разовый пропуск на машину":
            wnd = DrivePass(self)
        wnd.exec_()

    def ev_btn_start_file(self):
        name = self.sender().text()
        if name == "Доверенность":
            try:
                os.startfile(conf.path_default + "/Доверенность.xlsx", "print")
            except:
                print("Not found")
        if name == "Сканировать":
            try:
                os.startfile(conf.path + "/scan.exe")
            except:
                print("Not found")
        elif name == "Накладная":
            try:
                os.startfile(conf.path_default + "/накладная.xlsx", "print")
            except:
                print("Not found")
        elif name == "Журнал-ковид":
            try:
                os.startfile(conf.path_default + "/Ковидный журнал.xls")
            except:
                print("Not found")
        elif name == "Табель":
            try:
                os.startfile(conf.path_default + "/Табель.xlsx")
            except:
                print("Not found")
        elif name == "Блокнот":
            wnd = Notepad()
            wnd.exec_()
        elif name == "Музыка":
            wnd = Music(self)
            wnd.exec_()
        pass

    def ev_btn_add_to_db(self):
        name = self.sender().text()
        wnd = None
        table = None
        if name == "Автомобиль":
            wnd, table = NewAuto(self), "auto"
        elif name == "Водитель":
            wnd, table = NewDriver(self), "drivers"
        elif name == "Босс":
            wnd, table = NewBoss(self), "bosses"
        elif name == "Договор":
            self.db.execute('SELECT * FROM company')
            rows = self.db.fetchall()
            if not rows:
                msg = QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте Заказчика", QMessageBox.Ok)
                if msg == QMessageBox.Ok:
                    return
            wnd, table = NewContact(self), "contract"
        elif name == "Заказчик":
            wnd, table = NewCompany(self), "company"
        elif name == "Сотрудник":
            wnd, table = NewWorker(self), "workers"
        elif name == "Прораб":
            wnd, table = NewITR(self), "itr"
        elif name == "Ввоз материалов":
            wnd, table = NewMaterial(self), "materials"
        elif name == "Музыка":
            wnd, table = Music(self), "music"
        wnd.exec_()
        if self.data_to_db:
            self.commit(ins.add_to_db(self.data_to_db, table))

    def commit(self, query):
        if self.data_to_db:
            print(self.data_to_db)
            self.db.execute(query)
            self.db_conn.commit()
            self.data_to_db = None
            print("OK")

    def ev_new_bill(self):
        try:
            os.startfile(conf.path + "/scan.exe")
        except:
            print("не могу запустить сканер")
            return
        date, price, number = check_file()
        tmp = ".".join((str(x) for x in (dt.now().day, dt.now().month, dt.now().year)))
        os.replace("", conf.path_OCR + "/bills/{0}.jpg".format(tmp))
        # xlsx
        if not self.open_wb("bill"):
            return
        # TODO добавление в конец файла

        self.add_next_bill((date, price, number))
        self.wb.save(conf.path_OCR + "/bills.xlsx")
        self.wb.close()
        print("new bill")

    def ev_create_act(self):
        pass
        print("pass create act")

    def ev_pdf_check(self):
        """
        открыть директорию
        рассортировать все отсканированные файлы по папкам
        """
        check_file()
        print("pdf check")
        print("not check file")

    def ev_send_covid(self):
        """
        если нет соответствующего файла, то открыть окно для сканирования
        сформировать письмо
        взять ковид из папки
        отправить
        """
        try:
            covid = open(conf.path + conf.path_to_covid + "/covid{0}_{1}".format(dt.now().day, dt.now().month))
        except:
            print("not found file")
            try:
                os.startfile(conf.path_scan)
            except:
                print("not start scaner")
                return
            return
        # отправить письмо
        create_covid()
        to_email = "kalent_ivan@mail.ru"
        if not send_post("Ковидный журнал", "Доброе утро", to_email, conf.path_OCR + "/covid/covid_01_01.pdf"):
            QMessageBox(self, "Сообщение не отправилось").show()
        print("send covid")

    def ev_connect(self):
        # подключиться к серверу
        try:
            self.handle.connect_to_server()
            self.r_connect.setChecked(True)
            print("connect")
        except:
            print("not connect")
            self.r_connect.setChecked(False)

    """____________________________________"""

    # работа с Excel
    def get_next_number(self):
        # init
        config = ConfigParser()
        config.read('config.ini')
        # read
        number_note = config.get('config', 'number')
        # write
        next_number = int(number_note) + 1
        config.set('config', 'number', str(next_number))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return int(number_note)

    # database
    def connect_to_db(self):
        self.db_conn = psycopg2.connect(dbname='Company',
                                        user='postgres',
                                        password='pol_ool_123',
                                        host='localhost')
        self.db = self.db_conn.cursor()
        if not self.db_conn:
            return False
        return True

    def get_new_data(self, data):
        self.data_to_db = data

    # Прочее
    def get_number_doc(self):
        self.config.read(conf.path_conf_ini)
        next_number = int(self.config.get("conf", "next_number"))
        return str(next_number)

    def on_click_notif(self):  # TODO переделать в XML
        # read
        sender = self.sender()
        notif = sender.get_text()
        f = open(conf.path + "/notif.txt", "r")
        buffer = ""
        mes = ""
        for line in f.readlines():
            if notif in line and line[1] == "0":
                mes = line[0] + "1" + line[2:]
            else:
                mes = line
            buffer = buffer + mes
        f.close()
        f = open(conf.path + "/notif.txt", "w")
        f.write(buffer)
        f.close()

    def init_notif(self):
        pass

    def add_notif(self, message, mode):
        r_butt = QCheckBox(message)
        r_butt.clicked.connect(self.on_click_notif)
        self.ui_notification.addWidget(r_butt)
        f = open(conf.path + "/notif.txt", "a")
        f.write(str([mode, message]) + "\n")

    def get_weather(self):
        s_city = "Dorogobuzh"
        city_id = 0
        appid = "38462e21b3c595cfa5d4da0a88687dbe"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            city_id = data['list'][0]['id']
        except Exception as e:
            print("Exception (find):", e)
            pass
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            self.l_weather.setText(data['weather'][0]['description'])
            self.l_temp.setText(str(round(data['main']['temp_max'])) + " C")
        except Exception as e:
            print("Exception (weather):", e)

    def music(self):
        playlist = list(["https://atmoradio.ru/", "https://radio7.ru/", "https://radio.yandex.ru/"])


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
