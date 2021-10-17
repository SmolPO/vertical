from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QMessageBox, QAction
import sys
import os
import requests
import logging
from datetime import datetime as dt
from configparser import ConfigParser
from my_helper.notebook.sourse.new_boss import NewBoss
from my_helper.notebook.sourse.new_itr import NewITR
from my_helper.notebook.sourse.new_worker import NewWorker
from my_helper.notebook.sourse.nw_company import NewCompany
from my_helper.notebook.sourse.new_auto import NewAuto
from my_helper.notebook.sourse.new_driver import NewDriver
from my_helper.notebook.sourse.new_bill import NewBill
from pdf_module import check_file, create_covid
from my_helper.notebook.sourse.new_contract import NewContact
from my_helper.notebook.sourse.material import NewMaterial
from my_helper.notebook.sourse.new_TB import NewTB, CountPeople
from my_email import send_post
from my_helper.notebook.sourse.pass_week import WeekPass
from my_helper.notebook.sourse.pass_unlock import UnlockPass
from my_helper.notebook.sourse.pass_month import MonthPass
from my_helper.notebook.sourse.pass_get import GetPass
from my_helper.notebook.sourse.pass_auto import AutoPass
from my_helper.notebook.sourse.pass_drive import DrivePass
from my_helper.notebook.sourse.settings import Settings
from database import DataBase
from my_tools import Notepad
from music import Music
from get_money import GetMoney
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
key_for_db = "host=95.163.249.246 dbname=Vertical_db user=office password=9024EgrGvz#m87Y1"


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
        self.b_tb.clicked.connect(self.ev_btn_create_pass)
        # create
        self.b_new_person.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_build.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_boss.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_itr.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_invoice.clicked.connect(self.ev_btn_start_file)
        self.b_new_company.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_auto.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_driver.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_material.clicked.connect(self.ev_btn_add_to_db)
        self.b_new_bill.clicked.connect(self.ev_btn_add_to_db)

        exitAction = QAction('Настройки', self)
        exitAction.setStatusTip('Настройки')
        exitAction.triggered.connect(self.ev_settings)

        menu = self.menu
        fileMenu = menu.addMenu("Настройки")
        fileMenu.addAction(exitAction)

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
        self.b_get_money.clicked.connect(self.ev_btn_add_to_db)
        # self.menu.setting.settings.exitAction.triggered.connect(self.settings)
        self.b_scan.setEnabled(False)

        self.get_param_from_widget = None
        self.current_build = "Объект"
        self.company = 'ООО "Вертикаль"'
        self.customer = 'ПАО "Дорогобуж"'
        self.new_worker = []
        self.data_to_db = None

        # self.ui_l_build.setText(self.current_build)
        self.config = ConfigParser()
        self.init_notif()

        # Database
        self.db = DataBase()
        self.db.connect_to_db()
        self.get_weather()

    def ev_settings(self):
        wnd = Settings(self)
        wnd.exec_()

    def ev_btn_create_pass(self):
        name = self.sender().text()
        wnd = None
        if name == "Продление на месяц":
            if self.is_have_some("workers"):
                wnd = MonthPass(self)
            else:
                return
        elif name == "Пропуск на выходные":
            if self.is_have_some("workers"):
                wnd = WeekPass(self)
            else:
                return
        elif name == "Разблокировка пропуска":
            if self.is_have_some("workers"):
                wnd = UnlockPass(self)
            else:
                return
        elif name == "Выдать пропуск":
            if self.is_have_some("workers"):
                wnd = GetPass(self)
            else:
                return
        elif name == "Продление на машину":
            if self.is_have_some("auto"):
                wnd = AutoPass(self)
            else:
                return
        elif name == "Распечатать ТБ":
            self.count_people_tb = int()
            wnd = CountPeople(self)
            wnd.exec_()
            if self.count_people_tb > 0:
                wnd = NewTB(self)
        elif name == "Разовый пропуск на машину":
            if self.is_have_some("drivers"):
                wnd = DrivePass(self)
            else:
                return
        wnd.exec_()

    def ev_btn_start_file(self):
        name = self.sender().text()
        if name == "Доверенность":
            try:
                os.startfile(conf.path_default + "/attourney.xlsx", "print")
            except:
                print("Not found")
        if name == "Сканировать":
            try:
                os.startfile("C:\Program Files\Pantum\ptm6500\PushScan\ptm6500app.exe")
            except:
                print("Not found")
        elif name == "Накладная":
            try:
                os.startfile(conf.path_default + "/invoice.xlsx", "print")
            except:
                print("Not found")
        elif name == "Журнал-ковид":
            try:
                os.startfile(conf.path_default + "/covid.xls", "print")
            except:
                print("Not found")
        elif name == "Табель":
            try:
                os.startfile(conf.path_default + "/table.xlsx")
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
            data = self.db.get_data("*", "company")
            if not data:
                QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте Заказчика", QMessageBox.Ok)
                return
            wnd, table = NewContact(self), "contracts"
        elif name == "Заказчик":
            wnd, table = NewCompany(self), "company"
        elif name == "Сотрудник":
            wnd, table = NewWorker(self), "workers"
        elif name == "Прораб":
            wnd, table = NewITR(self), "itrs"
        elif name == "Ввоз материалов":
            wnd, table = NewMaterial(self), "materials"
        elif name == "Музыка":
            wnd, table = Music(self), "musics"
        elif name == "Чек":
            wnd, table = NewBill(self), "biils"
        elif name == "Заявка на деньги":
            wnd, table = GetMoney(self), "finances"
        wnd.exec_()

    def ev_create_act(self):
        pass
        print("pass create act")

    def ev_pdf_check(self):
        """
        открыть директорию
        рассортировать все отсканированные файлы по папкам
        """
        check_file()

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

    def is_have_some(self, table):
        auto = self.db.get_data("*", table)
        if not auto:
            QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте кого-то/что-то)", QMessageBox.Ok)
            return False
        return True

if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
