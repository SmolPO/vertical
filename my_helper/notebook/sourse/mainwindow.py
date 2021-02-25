from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QCheckBox, QVBoxLayout, QMessageBox
import sys
import os
import logging
from datetime import datetime as dt
import configparser
import openpyxl
import psycopg2
from new_boss import NewBoss
from add_worker import AddWorker
from pdf_module import check_file, create_covid
from new_contract import NewContact
from email_module import send_post
from my_tools import Notepad
import inserts as ins
import config as conf
from notebook import Notebook
from PyPDF2 import PdfFileMerger as pypdf


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('../designer_ui/main_menu.ui', self)
        # pass
        self.b_pass_week.clicked.connect(self.ev_pass_week)
        self.b_pass_month.clicked.connect(self.ev_pass_month)
        self.b_pass_auto.clicked.connect(self.ev_pass_auto)
        self.b_pass_recover.clicked.connect(self.ev_pass_recover)
        self.b_pass_unlock.clicked.connect(self.ev_pass_unlock)
        self.b_pass_issue.clicked.connect(self.ev_pass_issue)
        # create
        self.b_new_person.clicked.connect(self.ev_new_person)
        self.b_new_bill.clicked.connect(self.ev_new_bill)
        self.b_new_build.clicked.connect(self.ev_new_build)
        self.b_new_boss.clicked.connect(self.ev_new_boss)
        self.b_new_boss_post.clicked.connect(self.ev_new_boss_post)
        self.b_new_invoice.clicked.connect(self.ev_new_invoice)

        self.b_create_act.clicked.connect(self.ev_create_act)
        self.b_get_material.clicked.connect(self.ev_get_material)
        self.b_pdf_check.clicked.connect(self.ev_pdf_check)
        self.b_send_covid.clicked.connect(self.ev_send_covid)
        self.b_connect.clicked.connect(self.ev_connect)

        self.b_journal.clicked.connect(self.ev_journal)
        self.b_tabel.clicked.connect(self.ev_tabel)
        self.b_scan.clicked.connect(self.ev_scan)
        self.b_attorney.clicked.connect(self.ev_attorney)
        self.b_invoice.clicked.connect(self.ev_invoice)

        self.b_notepad.clicked.connect(self.ev_notepad)

        self.get_param_from_widget = None
        self.current_build = "(Объект)"
        self.company = 'ООО "Вертикаль"'
        self.new_worker = None
        self.new_boss = None
        self.new_contract = None
        self.ui_l_company.text = self.company
        self.ui_l_build.text = self.current_build
        self.config = configparser.ConfigParser()

        self.init_notif()

        # Database
        self.connect_to_database()
        builds = self.database_cur.execute(ins.get_builds())
        for item in builds:
            self.cb_builds.addItems(item)

        self.handle = Notebook()
        self.handle.start()

    def ev_pass_week(self):
        # TODO: выбор нескольких дней по календарю или из формы
        # открыть диалоговое окно для выбора дней. Открыть календарь.
        items = ("сб", "сб и вск", "вск", "другой день")
        chose, ok = QInputDialog.getItem(self, "Пропуск на выходные", "Выберите день", items)
        days = list()
        weekday = dt.now().weekday()
        day_now = dt.now().day
        if ok:
            if "сб" in chose:
                rest_day = ".".join((str(x) for x in (5 - weekday + dt.now().day, dt.now().month, dt.now().year)))
                days.append(rest_day)
            if "вск" in chose:
                rest_day = ".".join((str(x) for x in (6 - weekday + dt.now().day, dt.now().month, dt.now().year)))
                days.append(rest_day)
            if "другой день" in chose:
                chose, ok = QInputDialog.getInt(self, "Выберите день", "День:", day_now, day_now, 31, 1)
                if ok:
                    rest_day = ".".join((str(x) for x in (chose, dt.now().month, dt.now().year)))
                    days.append(rest_day)
                else:
                    return False
        else:
            return False

        # запрос в БД
        self.current_build = self.cb_builds.text
        # workers = self.database_cur.execute(ins.pass_week(self.current_build))
        workers = [["Kalent", "Ivan", "Semonovich", "монтажник", "01.08.1996"]]

        #  добавление в xlsx
        if not self.open_wb("week"):
            return

        for person in workers:
            self.add_new_row_to_excel(person)
        self.set_numder_and_date()
        self.set_week_days(days)
        self.wb.save(conf.path_for_print + "/week_print.xlsx")
        self.wb.close()
        os.startfile(conf.path_for_print + "/week_print.xlsx")

        # уведомление
        self.add_notif("Отправить на согласование выходные", 0)

        # TODO: отправить сообщение на сервер для уведомления в приложение
        print("pass week")

    def ev_pass_month(self):
        """
        получить из БД список сотрудников, дата рождения, паспортные, место жительства
        сформировать документ
        направить на печать
        """
        # БД
        workers = self.database_cur.execute(ins.full_workers_data)

        # xlsx
        if not self.open_wb("month"):
            return
        self.set_numder_and_date()
        self.set_month_date()
        for person in workers:
            self.add_new_row_to_excel(person)
        self.wb.save(conf.path_for_print + "/month_print.xlsx")
        self.wb.close()
        os.startfile(conf.path_for_print + "/month_print.xlsx")

        # уведомения
        self.add_notif("Отправить на согласование месяц", 0)

        # TODO: отправить сообщение на сервер для уведомления в приложение
        print("pass month")

    def ev_pass_auto(self):
        """
        получить из БД список машин, номер, владельцы
        сформировать документ
        печать
        """
        # БД
        cars = self.database_cur.execute(ins.auto)

        # xlsx
        if not self.open_wb("auto"):
            return
        self.set_numder_and_date()
        for auto in cars:
            self.add_next_auto(auto)
        self.wb.save(conf.path_for_print + "/auto_print.xlsx")
        self.wb.close()
        os.startfile(conf.path_for_print + "/auto_print.xlsx")

        # увведомление
        self.add_notif("Отправить на согласование авто", 0)

        # TODO: отправить сообщение на сервер для уведомления в приложение
        print("pass auto")

    def ev_pass_recover(self):
        """
        получить список работников
        открыть диалоговое окно с выбором сотрудника
        cформировать документ
        печать
        TODO: передача данных между окнами
        """
        # БД
        workers = self.database_cur.execute(ins.workers_with_adr)
        items = []
        for person in workers:
            items.append(person[0] + " " + ".".join((person[1][0], person[2][0])))
        family, ok = QInputDialog.getItem(self, "Выберите сотрудника", items, 0, "Список")
        if not ok:
            return

        # xlsx
        if not self.open_wb("recovery"):
            return
        # БД
        people = self.database_cur.execute(ins.get_person(family))
        worker = list()  # TODO проверить сборку данных
        worker.append(" ".join(*people[:2]))
        worker.append(people[3])
        worker.append(" ".join(people[4:9]))  # паспорт, адрес
        worker.append(people[10])  # адрес

        # xlsx
        self.set_numder_and_date()
        self.add_new_row_to_excel(worker)
        self.wb.save(conf.path_for_print + "/recovery_print.xlsx")
        self.wb.close()
        os.startfile(conf.path_for_print + "/recovery_print.xlsx")

        # уведомление
        self.add_notif("Отправить на согласование восстановление", 0)
        self.add_notif("Написать ковид журнал на работника", 0)
        # TODO: отправить сообщение на сервер для уведомления в приложение
        print("pass rec")

    def ev_pass_issue(self):
        """
        диалоговое окно с вводом нового сотрудника
        ввод данных
        добавление в БД
        TODO: передача между формами
        """
        wnd = AddWorker()
        wnd.exec_()
        if not self.new_worker:
            return
        self.database_cur.execute(ins.add_worker(self.new_worker))
        self.new_worker = None
        print("pass issue")
        # TODO: отправить сообщение на сервер для уведомления в приложение

    def ev_pass_unlock(self):
        """
        получить список работников
        открыть диалоговое окно с выбором сотрудника
        cформировать документ
        печать
        """
        workers = self.database_cur.execute(ins.workers_with_adr)
        # выбор сотрудника
        people = list()
        for person in workers:
            people.append(person[0])
        family, ok = QInputDialog.getItem(self, "Выберите работника", people, 0, "список")
        if not ok:
            return
        bad_people = list()
        for one in workers:
            if family == one:
                bad_people = one

        # узнать сколько дней в месяце
        start_date = ".".join(str(x) for x in (dt.now().day, dt.now().month, dt.now().year))
        num_days = [31, 28 if dt.now().year / 4 else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        max_day = num_days[dt.now().month]
        end_date = ".".join(str(x) for x in (max_day, dt.now().month, dt.now().year))
        title = "Прошу вас разблокировать электронный пропуск {post} организации " \
                "{company} {family} {name} {surname} c {start_date} по {end_month}".format(post=bad_people[3],
                                                                                           company=self.company,
                                                                                           family=bad_people[1],
                                                                                           name=bad_people[0],
                                                                                           surname=bad_people[2],
                                                                                           start_date=start_date,
                                                                                           end_month=end_date)

        # xlsx
        if not self.open_wb("unlock"):
            return
        self.set_numder_and_date()
        self.set_title(title)
        self.wb.save(conf.path_for_print + "/unlock_print.xlsx")
        self.wb.close()
        os.startfile(conf.path_for_print + "/unlock_print.xlsx")

        # уведомление
        self.add_notif("Отправить на согласование разблокировку", 0)
        print("pass unlock")

    def ev_new_boss(self):
        """
        диалоговое окно с формой для нового босса
        заполнение данных
        добавление в БД
        """
        wnd = NewBoss()
        wnd.exec_()
        if not self.new_boss:
            return
        self.database_cur.execute(ins.add_boss(self.new_boss))
        self.new_boss = None
        print("new boss")

    def ev_new_bill(self):
        os.startfile(conf.path + "/scan.exe")
        date, price, number = check_file()
        os.replace("", conf.path_OCR + "/bills/{0}.jpg".format(".".join((str(x) for x in (dt.now().day,
                                                                                         dt.now().month,
                                                                                         dt.now().year)))))
        # xlsx
        if not self.open_wb("bill"):
            return
        # TODO добавление в конец файла

        self.add_next_bill((date, price, number))
        self.wb.save(conf.path_OCR + "/bills.xlsx")
        self.wb.close()
        print("new bill")

    def ev_new_build(self):
        """
        открыть форму для нового объекта
        заполнить данные
        добавить объект в БД
        получить новый список объектов для списка объектов на главном меню
        """
        wnd = NewContact(self)
        wnd.exec_()
        if not self.new_contract:
            return
        self.database_cur.execute(ins.new_contract(self.new_contract))
        self.new_contract = None
        print("new build")

    def ev_new_person(self):
        """
        открыть окно для нового сотрудника
        заполнить данные
        отправить в БД
        """
        wnd = AddWorker()
        wnd.exec_()
        if not self.new_worker:
            return
        self.database_cur.execute(ins.add_worker(self.new_worker))
        self.new_worker = None
        print("new person")

    def ev_create_act(self):
        pass
        print("create act")

    def ev_get_material(self):
        """
        открыть форму для ввода название материала и даты завоза
        сформировать документ
        печать
        """
        pass
        print("get mat")

    def ev_pdf_check(self):
        """
        открыть директорию
        рассортировать все отсканированные файлы по папкам
        """
        check_file()
        print("pdf check")

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
            QMessageBox(self, "Нет файла с ковидом")
            os.startfile(conf.path_scan)
            return
        # отправить письмо
        create_covid()
        to_email = "kalent_ivan@mail.ru"
        if not send_post("Ковидный журнал", "Доброе утро", to_email, conf.path_OCR + "/covid/covid_01_01.pdf"):
            QMessageBox(self, "Сообщение не отправилось").show()
        print("send covid")

    def ev_connect(self):
        # подключиться к серверу
        self.handle.connect_to_server()
        self.r_connect.setChecked(True)
        print("connect")

    def ev_new_invoice(self):
        """
        открыть сканер
        добавить накладную в папку
        """
        print("create invoice")

    def ev_new_boss_post(self):
        """
        получить весь список боссов
        открыть окно для нового босса. Боса можно выбрать старого или ввести новые данные.
        ввести данные
        добавить в БД
        """
        print("new post of boss")

    def ev_journal(self):
        # печать ковид журнала
        os.startfile(conf.path_default + "/covid.xlsx", "print")
        print("journal")

    def ev_tabel(self):
        os.startfile(conf.path_default + "/табель.xlsx", "print")
        print("tabel")

    def ev_scan(self):
        os.startfile(conf.path + "/scan.exe")
        print("scan")

    def ev_attorney(self):
        os.startfile(conf.path_default + "/доверенность.xlsx", "print")
        print("attorney")

    def ev_invoice(self):
        os.startfile(conf.path_default + "/накладная.xlsx", "print")
        print("invoice")

    def ev_notepad(self):
        wnd = Notepad()
        wnd.show()
        pass

    # работа с Excel
    def open_wb(self, sheet):
        # открытие файла
        try:
            self.wb = openpyxl.load_workbook(conf.path_xlsx)
        except:
            QMessageBox(self, "Нет xlsx файла по адресу {0}".format(conf.path_xlsx)).show()
            return False

        # открытие листа
        if sheet in self.wb.sheetnames:
            self.sheet = self.wb[sheet]
            return True
        else:
            QMessageBox("Нет листа {0} в xlsx файле".format(sheet)).show()
            logging.info("Нет листа {0} в xlsx файле".format(sheet))
            print("Нет листа {0} в xlsx файле".format(sheet))
            return False

    def add_new_row_to_excel(self, row, start_row=10):
        self.sheet.insert_rows(idx=start_row, amount=1)
        i = iter(range(10))
        # thin_border = Border(left=Side(style='thin'),
        #                     right=Side(style='thin'),
        #                    top=Side(style='thin'),
        #                   bottom=Side(style='thin'))
        for item in row:
            cell = self.sheet.cell(row=start_row, column=next(i)+1)
            cell.value = item
        #   cell.border = thin_border

    def add_next_auto(self, row):
        driver = " ".join(row[2:])
        add_row = [row[0], row[1], driver]
        # thin_border = Border(left=Side(style='thin'),
        #                     right=Side(style='thin'),
        #                    top=Side(style='thin'),
        #                   bottom=Side(style='thin'))
        self.sheet.insert_rows(idx=10, amount=1)
        i = iter(range(10))
        for item in add_row:
            cell = self.sheet.cell(row=10, column=next(i)+1)
            cell.value = item
            # cell.border = thin_border

    def add_next_bill(self, date):
        cell_count = self.sheet.cell(row=1, column=10)
        count = cell_count.value
        cell_count.value = count + 1
        i = iter(range(4))
        for item in date:
            cell = self.sheet.cell(row=count, column=next(i)+1)
            cell.value = item

    def set_week_days(self, days):
        if len(days) > 1:
            title = "Прошу Вас разрешить работы в выходные дни {0} г. и {1}. по ремонту {2} работникам {3}, " \
                    "с рабочей сменой с 07-00 до 19-00 часов:".format(days[0], days[1], self.current_build, self.company)
        else:
            title = "Прошу Вас разрешить работы в выходной день {0} г. по ремонту {1} работникам {2}, " \
                    "с рабочей сменой с 07-00 до 19-00 часов:".format(days[0], self.current_build, self.company)
        cell = self.sheet.cell(row=5, column=1)
        cell.value = title

    def set_number_and_date(self):
        if dt.now().month < 10:
            month = "0" + str(dt.now().month)
        else:
            month = str(dt.now().month)
        date = ".".join((str(x) for x in (dt.now().day, month, dt.now().year)))
        cell_count = self.sheet.cell(row=3, column=1)
        cell_data = self.sheet.cell(row=4, column=1)
        cell_count.value = "Исх. №" + self.next_number_doc()
        cell_data.value = "от " + date

    def set_month_date(self):
        next_month = 1 if dt.now().month == 12 else dt.now().month + 1
        year = dt.now().year if dt.now().month < 12 else dt.now().year + 1
        num_days = [31, 28 if dt.now().year / 4 else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if next_month < 10:
            next_month = "0" + str(next_month)
        max_day = num_days[dt.now().month]
        first_date = ".".join((str(x) for x in ("01", next_month, year)))
        end_date = ".".join((str(x) for x in (max_day, next_month, year)))
        title = "Прошу Вас продлить электронные пропуска для организации и производства работ " \
                "на территории ПАО «Дорогобуж» " \
                "работникам  {0} с {1} г. по {2} г. с рабочей сменой " \
                "с 07-00 до 19-00 часов:".format(self.company, first_date, end_date)
        cell_title = self.sheet.cell(row=5, column=1)
        cell_title.value = title

    def set_title(self, title, type_doc=5):
        cell_title = self.sheet.cell(row=type_doc, column=1)
        cell_title.value = title

    # database
    def connect_to_database(self):
        self.database_conn = psycopg2.connect(dbname='Company',
                                              user='postgres',
                                              password='pol_ool_123',
                                              host='localhost')
        self.database_cur = self.database_conn.cursor()
        if not self.database_conn:
            return False
        return True

    # Прочее
    def next_number_doc(self):
        self.config.read(conf.path_conf_ini)
        next_number = int(self.config.get("conf", "next_number"))
        self.config.set("conf", "next_number", str(int(next_number)+1))
        return str(next_number)

    def get_new_worker(self, worker):
        """
        получаем полный список данных нового работника
        добавляем в БД
        """
        self.new_worker = worker
        print(worker)

    def set_new_boss(self, boss):
        self.new_boss = boss

    def on_click_notif(self): # TODO переделать в XML
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
        f = open(conf.path + "/notif.txt", "r")
        for line in f.readlines():
            if line[1] == '0':
                self.ui_notification.addItem(QCheckBox(line[5:-4]))
                print(line[5:-3])

    def add_notif(self, message, mode):
        r_butt = QCheckBox(message)
        r_butt.clicked.connect(self.on_click_notif)
        self.ui_notification.addWidget(r_butt)
        f = open(conf.path + "/notif.txt", "a")
        f.write(str([mode, message]) + "\n")


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
