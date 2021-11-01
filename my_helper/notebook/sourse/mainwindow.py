from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QMessageBox, QAction, QInputDialog
import sys
import os
import requests
import logging
from PyQt5.QtWidgets import QMessageBox as mes
from datetime import datetime as dt
from configparser import ConfigParser
from my_helper.notebook.sourse.create.new_boss import NewBoss
from my_helper.notebook.sourse.create.new_itr import NewITR
from my_helper.notebook.sourse.create.new_worker import NewWorker
from my_helper.notebook.sourse.create.nw_company import NewCompany
from my_helper.notebook.sourse.create.new_auto import NewAuto
from my_helper.notebook.sourse.create.new_driver import NewDriver
from my_helper.notebook.sourse.create.new_bill import NewBill
from my_helper.notebook.sourse.covid19 import NewCovid
from my_helper.notebook.sourse.table import NewTable
from pdf_module import PDFModule
from my_helper.notebook.sourse.create.new_contract import NewContact
from my_helper.notebook.sourse.create.material import NewMaterial
from my_helper.notebook.sourse.create.new_TB import NewTB, CountPeople
from my_helper.notebook.sourse.acts.acts import Acts
from my_email import send
from my_helper.notebook.sourse.my_pass.pass_week import WeekPass
from my_helper.notebook.sourse.my_pass.pass_unlock import UnlockPass
from my_helper.notebook.sourse.my_pass.pass_month import MonthPass
from my_helper.notebook.sourse.my_pass.pass_get import GetPass
from my_helper.notebook.sourse.my_pass.pass_auto import AutoPass
from my_helper.notebook.sourse.my_pass.pass_drive import DrivePass
from my_helper.notebook.sourse.settings import Settings
from database import DataBase, get_path, get_config, get_from_ini, my_errors
from my_tools import Notepad
from music import Web
from get_money import GetMoney
import shutil
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
logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.path = input()
        self.path = "B:/my_helper/my_config.ini"
        try:
            uic.loadUi(get_path("path") + get_path("ui_files") + '/main_menu.ui', self)
        except:
            mes.question(self, "Сообщение", my_errors["1_ui"] +
                         get_path("path") + get_path("ui_files") + '/main_menu.ui', mes.Cancel)
            return
        try:
            self.db = DataBase(self.path)
            self.db.connect_to_db()
        except:
            mes.question(self, "Сообщение", my_errors["3_conn"], mes.Cancel)
            return
        self.b_pass_week.clicked.connect(self.start_wnd)
        self.b_pass_month.clicked.connect(self.start_wnd)
        self.b_pass_auto.clicked.connect(self.start_wnd)
        self.b_pass_drive.clicked.connect(self.start_wnd)
        self.b_pass_unlock.clicked.connect(self.start_wnd)
        self.b_pass_issue.clicked.connect(self.start_wnd)
        self.b_tb.clicked.connect(self.start_wnd)
        self.b_new_person.clicked.connect(self.start_wnd)
        self.b_new_build.clicked.connect(self.start_wnd)
        self.b_new_boss.clicked.connect(self.start_wnd)
        self.b_new_itr.clicked.connect(self.start_wnd)
        # self.b_new_invoice.clicked.connect(self.start_wnd)
        self.b_new_company.clicked.connect(self.start_wnd)
        self.b_new_auto.clicked.connect(self.start_wnd)
        self.b_new_driver.clicked.connect(self.start_wnd)
        self.b_new_material.clicked.connect(self.start_wnd)
        self.b_new_bill.clicked.connect(self.start_wnd)
        self.b_notepad.clicked.connect(self.start_wnd)
        self.b_music.clicked.connect(self.start_wnd)
        self.b_get_money.clicked.connect(self.start_wnd)
        self.b_act.clicked.connect(self.start_wnd)
        self.b_pdf_check.clicked.connect(self.start_wnd)
        self.b_journal.clicked.connect(self.start_wnd)
        self.b_tabel.clicked.connect(self.start_wnd)

        exitAction = QAction('Настройки', self)
        exitAction.setStatusTip('Настройки')
        exitAction.triggered.connect(self.ev_settings)

        menu = self.menu
        fileMenu = menu.addMenu("Настройки")
        fileMenu.addAction(exitAction)

        # self.b_connect.clicked.connect(self.ev_connect)
        self.b_empty.clicked.connect(self.ev_btn_start_file)

        self.b_scan.clicked.connect(self.ev_btn_start_file)
        self.b_attorney.clicked.connect(self.ev_btn_start_file)
        self.b_invoice.clicked.connect(self.ev_btn_start_file)

        self.b_scan.setEnabled(False)

        self.get_param_from_widget = None
        self.current_build = "Объект"
        self.company = get_config("company")
        self.customer = get_config("customer")
        self.new_worker = []
        self.data_to_db = None
        self.init_notif()
        self.get_weather()

    def ev_settings(self):
        wnd = Settings(self)
        wnd.exec_()

    def start_wnd(self):
        name = self.sender().text()
        trans = {"workers": "рабочих", "auto": "авто", "contracts": "договоры"}
        forms = {"Продление на месяц": (MonthPass, "workers"),
                 "Пропуск на выходные": (WeekPass, "workers"),
                 "Разблокировка пропуска": (UnlockPass, "workers"),
                 "Выдать пропуск": (GetPass, "workers"),
                 "Продление на машину": (AutoPass, "auto"),
                 "Блокнот": (Notepad, None),
                 "Сайты": (Web, None),
                 "Исполнительная": (Acts, "contracts"),
                 "Сканер": (PDFModule, None),
                 "Автомобиль": (NewAuto, None),
                 "Водитель": (NewDriver, None),
                 "Босс": (NewBoss, None),
                 "Прораб": (NewITR, None),
                 "Чек": (NewBill, None),
                 "Заявка на деньги": (GetMoney, None),
                 "Разовый пропуск на машину": (DrivePass, None)}
        _wnd = forms.get(name, "")
        if _wnd:
            if _wnd[1]:
                if self.is_have_some(_wnd[1]):
                    wnd = _wnd[0](self)
                else:
                    mes.question(self, "Сообщение", "База данных пока не заполнена. Введите " + trans[_wnd[1]],
                                 mes.Cancel)
                    return
            else:
                wnd = _wnd[0](self)
        elif name == "Распечатать ТБ":
            self.count_people_tb = int()
            wnd = CountPeople(self)
            if not wnd._status:
                mes.question(self, "Сообщение", my_errors["1_ui"] + wnd._path, mes.Cancel)
                return
            wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
            wnd.exec_()
            if self.count_people_tb > 0:
                wnd = NewTB(self)
            else:
                return
        elif name == "Журнал-ковид":
            wnd = NewCovid(self)
            wnd.create_covid()
            return
        elif name == "Табель":
            wnd = NewTable(self)
            wnd.create_table()
            return
        else:
            return
        if not wnd.status_:
            mes.question(self, "Сообщение", my_errors["1_ui"] + wnd._path, mes.Cancel)
            return
        wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
        wnd.exec_()

    def ev_btn_start_file(self):
        files = {"Доверенность": "/Доверенность.xlsx", "Накладная": "/Накладная.xlsx", "Бланк": "/Бланк.doc"}
        name = self.sender().text()
        try:
            path = get_path("path") + get_path("path_pat_patterns") + files[name]
        except:
            mes.question(self, "Сообщение", my_errors["2_get_path"], mes.Cancel)
            return
        try:
            os.startfile(path, "print")
        except:
            mes.question(self, "Сообщение", my_errors["4_not_file"] + path, mes.Cancel)
            return

    def get_new_data(self, data):
        self.data_to_db = data

    def on_click_notif(self):  # TODO переделать в XML
        # read
        sender = self.sender()
        notif = sender.get_text()
        f = open(get_path("main_path") + "/notif.txt", "r")
        buffer = ""
        for line in f.readlines():
            if notif in line and line[1] == "0":
                mes = line[0] + "1" + line[2:]
            else:
                mes = line
            buffer = buffer + mes
        f.close()
        f = open(get_config("main_path") + "/notif.txt", "w")
        f.write(buffer)
        f.close()

    def init_notif(self):
        pass

    def add_notif(self, message, mode):
        r_butt = QCheckBox(message)
        r_butt.clicked.connect(self.on_click_notif)
        self.ui_notification.addWidget(r_butt)
        f = open(get_config("main_path") + "/notif.txt", "a")
        f.write(str([mode, message]) + "\n")

    def get_weather(self):
        s_city = get_from_ini("city", "weather")
        city_id = 0
        appid = get_from_ini("appid", "weather")
        try:
            res = requests.get(get_from_ini("site_find", "weather"),
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            city_id = data['list'][0]['id']
        except Exception as e:
            self.l_weather.setText("погода")
            self.l_temp.setText("температура")
            pass
        try:
            res = requests.get(get_from_ini("site_weather", "weather"),
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            self.l_weather.setText(data['weather'][0]['description'])
            self.l_temp.setText(str(round(data['main']['temp_max'])) + " C")
        except Exception as e:
            self.l_weather.setText("погода")
            self.l_temp.setText("температура")

    def is_have_some(self, table):
        auto = self.db.get_data("*", table)
        if not auto:
            QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте кого-то/что-то)", QMessageBox.Ok)
            return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setFixedSize(587, 591)
    ex.show()
    sys.exit(app.exec())
