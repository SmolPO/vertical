from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QAction, QInputDialog
import sys
import requests
from new_boss import NewBoss
from new_itr import NewITR
from new_worker import NewWorker
from nw_company import NewCompany
from new_auto import NewAuto
from new_driver import NewDriver
from new_bill import NewBill
from covid19 import NewCovid
from table import NewTable
from pdf_module import PDFModule
from new_contract import NewContact
from material import NewMaterial
from new_TB import NewTB, CountPeople
from acts import Acts
from my_email import *
from pass_week import WeekPass
from pass_unlock import UnlockPass
from pass_month import MonthPass
from pass_get import GetPass
from pass_auto import AutoPass
from pass_drive import DrivePass
from settings import Settings
from database import *
from my_tools import Notepad
from music import Web
from get_money import GetMoney


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.path = "B:/my_helper/my_config.ini"
        self.conf = Ini(self)
        path = self.conf.get_path_ui("main_menu")
        if path == ERR:
            return
        try:
            uic.loadUi(path, self)
        except:
            msg_er(self, GET_UI + path)
            return

        self.db = DataBase(self, self.path)
        if self.db.connect_to_db() == ERR:
            return
        check = self.conf.get_config("is_created_db")
        if check == ERR:
            return
        if check == "NO":
            if self.db.create_db() == ERR:
                return
            if self.conf.set_val("config", "is_create_db", "YES") == ERR:
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
        sqlAction = QAction('Запрос в базу данных', self)
        sqlAction.setStatusTip('SQL запрос')
        sqlAction.triggered.connect(self.sql_mes)
        exitAction.triggered.connect(self.ev_settings)

        menu = self.menu
        fileMenu = menu.addMenu("Настройки")
        fileMenu.addAction(exitAction)
        fileMenu.addAction(sqlAction)

        self.b_empty.clicked.connect(self.ev_btn_start_file)

        self.b_scan.clicked.connect(self.ev_btn_start_file)
        self.b_attorney.clicked.connect(self.ev_btn_start_file)
        self.b_invoice.clicked.connect(self.ev_btn_start_file)

        self.b_scan.setEnabled(False)

        self.get_param_from_widget = None
        self.company = self.conf.get_config("company")
        self.customer = self.conf.get_config("customer")
        if self.company == ERR:
            self.company = "<Подрядчик>"
        if self.customer == ERR:
            self.company = "<Заказчик>"
        self.company_ = ""
        self.customer_ = ""
        self.check_company()
        self.new_worker = []
        self.data_to_db = None
        self.init_notif()
        self.get_weather()
        self.city = self.conf.get_config("city")
        if self.city == ERR:
            self.city = "<город>"

    def ev_settings(self):
        wnd = Settings(self)
        if not wnd.status_:
            return
        wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
        wnd.exec_()

    def start_wnd(self):
        name = self.sender().text()
        trans = {"workers": "рабочих", "auto": "авто", "contracts": "договоры"}
        forms = {"Продление на месяц": (MonthPass, "workers"),
                 "Пропуск на выходные": (WeekPass, "workers"),
                 "Разблокировка пропуска": (UnlockPass, "workers"),
                 "Ввоз материалов": (NewMaterial, "contracts"),
                 "Выдать пропуск": (GetPass, "workers"),
                 "Продление на машину": (AutoPass, "auto"),
                 "Блокнот": (Notepad, None),
                 "Сайты": (Web, None),
                 "Исполнительная": (Acts, "contracts"),
                 "Сканер": (PDFModule, None),
                 "Автомобиль": (NewAuto, None),
                 "Заказчик": (NewCompany, None),
                 "Договор": (NewContact, "company"),
                 "Водитель": (NewDriver, None),
                 "Босс": (NewBoss, "company"),
                 "Сотрудник": (NewWorker, "contracts"),
                 "Прораб": (NewITR, None),
                 "Чек": (NewBill, None),
                 "Заявка на деньги": (GetMoney, None),
                 "Разовый пропуск": (DrivePass, "contracts")}
        _wnd = forms.get(name, "")
        if _wnd:
            if _wnd[1]:
                if name == "Договор":
                    data = self.db.get_data("status", "company")
                    if not ("Заказчик",) in data:
                        msg_info(self, "Введите сначала данные Заказчика")
                        return
                    else:
                        wnd = _wnd[0](self)
                else:
                    check = self.is_have_some(_wnd[1])
                    if check == ERR:
                        return
                    elif check:
                        wnd = _wnd[0](self)
                    else:
                        msg_info(self, "База данных пока не заполнена. Добавбте сначала " + trans[_wnd[1]])
                        return
            else:
                wnd = _wnd[0](self)
        elif name == "Распечатать ТБ":
            self.count_people_tb = int()
            wnd = CountPeople(self)
            if not wnd.status_:
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
             return
        wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
        wnd.exec_()
        if self.sender().text() == "Заказчик":
           self.check_company()

    def check_company(self):
        company = self.db.get_data("*", "company")
        if company == ERR:
            return
        for item in company:
            if item[-2] == "Подрядчик":
                self.company_ = item
            if item[-2] == "Заказчик":
                self.customer_ = item

    def ev_btn_start_file(self):
        files = {"Доверенность": "/Доверенность.xlsx",
                 "Накладная": "/Накладная.xlsx",
                 "Бланк": "/Бланк.doc"}
        name = self.sender().text()
        paths = [self.conf.get_path("path"), self.conf.get_path("path_pat_patterns")]
        if ERR in paths:
            return
        path = "".join(paths) + files[name]

        if name == "Бланк":
            try:
                os.startfile(path)
            except:
                msg_info(self, GET_FILE + path)
            return
        try:
            count, ok = QInputDialog.getInt(self, name, "Кол-во копий")
            if ok:
                for ind in range(count):
                    try:
                        os.startfile(path, "print")
                    except:
                        msg_info(self, GET_FILE + path)
        except:
            mes.question(self, "Сообщение", GET_FILE + path, mes.Cancel)
            return

    def get_new_data(self, data):
        self.data_to_db = data

    def on_click_notif(self):  # TODO переделать в XML
        # read
        sender = self.sender()
        notif = sender.get_text()
        f = open(self.conf.get_path("main_path") + "/notif.txt", "r")
        buffer = ""
        for line in f.readlines():
            if notif in line and line[1] == "0":
                mes = line[0] + "1" + line[2:]
            else:
                mes = line
            buffer = buffer + mes
        f.close()
        f = open(self.conf.get_config("main_path") + "/notif.txt", "w")
        f.write(buffer)
        f.close()

    def init_notif(self):
        pass

    def add_notif(self, message, mode):
        r_butt = QCheckBox(message)
        r_butt.clicked.connect(self.on_click_notif)
        self.ui_notification.addWidget(r_butt)
        f = open(self.conf.get_config("main_path") + "/notif.txt", "a")
        f.write(str([mode, message]) + "\n")

    def get_weather(self):
        s_city = self.conf.get_from_ini("city", "weather")
        city_id = 0
        appid = self.conf.get_from_ini("appid", "weather")
        try:
            res = requests.get(self.conf.get_from_ini("site_find", "weather"),
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            city_id = data['list'][0]['id']
        except Exception as e:
            self.l_weather.setText("погода")
            self.l_temp.setText("температура")
            pass
        try:
            res = requests.get(self.conf.get_from_ini("site_weather", "weather"),
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            self.l_weather.setText(data['weather'][0]['description'])
            self.l_temp.setText(str(round(data['main']['temp_max'])) + " C")
        except Exception as e:
            self.l_weather.setText("погода")
            self.l_temp.setText("температура")

    def is_have_some(self, table):
        data = self.db.get_data("*", table)
        if data == ERR:
            return ERR
        if not data:
             return False
        return True

    def sql_mes(self):
        text, ok = QInputDialog.getText(self, "SQL запрос", "Введите запрос")
        if ok:
            if text:
                try:
                    self.db.execute(text)
                except:
                    msg_info(self, "Запос не удался")
                    return
                file = open("text.txt", "w")
                file.write(str(self.db.cursor.fetchall()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setFixedSize(ex.geometry().width(), ex.geometry().height())
    ex.show()
    sys.exit(app.exec())
