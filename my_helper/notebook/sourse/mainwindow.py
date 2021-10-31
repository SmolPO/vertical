from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QMessageBox, QAction
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
from database import DataBase, get_path, get_config, get_from_ini
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
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        try:
            print(get_path("ui_files"))
        except:
            f = open("text.txt")
            f.write("нет файла с настройками")
            return
        try:
            self.db = DataBase()
            self.db.connect_to_db()
        except:
            f = open("text.txt")
            f.write("нет связи с базой данных")
            return
        uic.loadUi(get_path("path") + get_path("ui_files") + '/main_menu.ui', self)
        print("my_pass")
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

        self.b_act.clicked.connect(self.ev_btn_start_file)
        self.b_pdf_check.clicked.connect(self.ev_btn_start_file)
        # self.b_connect.clicked.connect(self.ev_connect)

        self.b_journal.clicked.connect(self.ev_btn_start_file)
        self.b_tabel.clicked.connect(self.ev_btn_start_file)
        self.b_scan.clicked.connect(self.ev_btn_start_file)
        self.b_attorney.clicked.connect(self.ev_btn_start_file)
        self.b_invoice.clicked.connect(self.ev_btn_start_file)
        # self.cb_builds.activated[str].connect(self.change_build)
        self.b_notepad.clicked.connect(self.ev_btn_start_file)
        self.b_music.clicked.connect(self.ev_btn_add_to_db)
        self.b_get_money.clicked.connect(self.ev_btn_add_to_db)
        self.b_empty.clicked.connect(self.ev_btn_start_file)
        # self.menu.setting.settings.exitAction.triggered.connect(self.settings)
        self.b_scan.setEnabled(False)

        self.get_param_from_widget = None
        self.current_build = "Объект"
        self.company = get_config("company")
        self.customer = get_config("customer")
        self.new_worker = []
        self.data_to_db = None

        # self.ui_l_build.setText(self.current_build)
        self.config = ConfigParser()
        self.init_notif()

        # Database
        self.db = DataBase()
        self.db.connect_to_db()
        self.get_weather()
        # logging

        logging.debug("This is a debug message")

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
                path = get_path("path") + get_path("path_pat_patterns") + "/attorney.xlsx"
                os.startfile(path, "print")
            except:
                mes.question(self, "Сообщение", "Файл по пути " + path + "не найден", mes.Cancel)
                return
        if name == "Сканировать":
            try:
                os.startfile(get_path("path_scaner"))
            except:
                mes.question(self, "Сообщение", "Сканер не открывается")
                return
        elif name == "Накладная":
            try:
                path = get_path("path") + get_path("path_pat_patterns") + "/invoice.xlsx"
                os.startfile(path , "print")
            except:
                mes.question(self, "Сообщение", "Файл по пути " + path + "не открывается")
                return
        elif name == "Журнал-ковид":
            try:
                path = get_path("path") + get_path("path_pat_patterns") + "/covid.xls"
                os.startfile(path, "print")
            except:
                mes.question(self, "Сообщение", "Файл по пути " + path + "не открывается")
        elif name == "Табель":
            try:
                path = get_path("path") + get_path("path_pat_patterns") + "/table.xls"
                os.startfile(path)
            except:
                mes.question(self, "Сообщение", "Файл по пути " + path + "не найден", mes.Cancel)
        elif name == "Бланк":
            path_blank = ""
            try:
                path_blank = get_path("path") + get_path("path_pat_patterns") + "/blank.doc"
                path_to = get_path("path") + get_path("path_send") + "/" + str(dt.now()) + ".docx"
                shutil.copy2(path_blank, path_to)
                os.startfile(path_to)
            except:
                mes.question(self, "Сообщение", "Файл по пути " + path_blank + " не найден", mes.Cancel)
                return
        elif name == "Блокнот":
            wnd = Notepad()
            wnd.exec_()
        elif name == "Сайты":
            wnd = Web(self)
            wnd.exec_()
        elif name == "Исполнительная":
            wnd = Acts(self)
            wnd.exec_()
        elif name == "Сканер":
            wnd = PDFModule(self)
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
            if not self.db.get_data("*", "contracts"):
                QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте Объекты", QMessageBox.Ok)
                return
            wnd, table = NewWorker(self), "workers"
        elif name == "Прораб":
            wnd, table = NewITR(self), "itrs"
        elif name == "Ввоз материалов":
            if not self.db.get_data("*", "contracts"):
                QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте Объекты", QMessageBox.Ok)
                return
            wnd, table = NewMaterial(self), "materials"
        elif name == "Сайты":
            wnd, table = Web(self), "musics"
        elif name == "Чек":
            wnd, table = NewBill(self), "bills"
        elif name == "Заявка на деньги":
            wnd, table = GetMoney(self), "finances"
        else:
            return
        wnd.exec_()

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
            print("Exception (find):", e)
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
            print("Exception (weather):", e)

    def is_have_some(self, table):
        auto = self.db.get_data("*", table)
        if not auto:
            QMessageBox.question(self, "ВНИМАНИЕ", "Для начала добавьте кого-то/что-то)", QMessageBox.Ok)
            return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
