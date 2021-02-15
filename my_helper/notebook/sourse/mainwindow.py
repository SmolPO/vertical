from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os
import logging
import datetime
import openpyxl
from openpyxl.styles.borders import Border, Side
import psycopg2
from add_company import AddCompany
from new_boss import NewBoss

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

        self.get_param_from_widget = None
        self.current_build = None
        self.company = 'ООО "Вертикаль"'

    def ev_pass_week(self):
        # открыть диалоговое окно дл выбора дней. Открыть календарь.

        days = [6, 7]
        workbook, sheet = self.open_wb(name="week")
        insert = "SELECT name, family, surname, post, birthdate, passport_seria, passport_number, address,  live_address " + \
                 "FROM workers WHERE build = '" + self.current_build + "'"
        rows = self.database_cur.execute(insert)
        self.wb, self.sheet = self.open_wb("week")
        i = iter(range(10))
        for row in rows:
            self.add_new_row_to_excel(row)
            next(i)
        self.set_numder_and_date()
        self.set_week_days(days)
        self.wb.save("./week_print.xlsx")
        self.wb.close()
        self.wb, self.sheet = None, None
        os.startfile("./week_print.xlsx")
        print("pass week")

    def ev_pass_month(self):
        # получить из БД список сотрудников, дата рождения, паспортные, место жительства
        # сформировать документ
        # направить на печать
        self.open_wb('month')
        insert = "SELECT name, family, surname, post, birthdate, passport_seria, passport_number, address,  live_address " + \
                 "FROM workers"
        rows = self.database_cur.execute(insert)
        self.set_numder_and_date()
        for row in rows:
            self.add_new_row_to_excel(row)

        self.wb.save("./week_print.xlsx")
        self.wb.close()
        print("pass month")

    def ev_pass_auto(self):
        # получить из БД список машин, номер, владельцы
        # сформировать документ
        # направить на печать
        print("pass auto")

    def ev_pass_recover(self):
        # получить список работников
        # открыть диалоговое окно с выбором сотрудника
        # cформировать документ
        # отправить на печать
        print("pass rec")

    def ev_pass_issue(self):
        # диалоговое окно с вводом нового сотрудника
        # ввод данных
        # добавление в БД
        print("pass issue")

    def ev_pass_unlock(self):
        # получить список работников
        # открыть диалоговое окно с выбором сотрудника
        # cформировать документ
        # отправить на печать
        print("pass unlock")

    def ev_new_boss(self):
        # диалоговое окно с формой для нового босса
        # заполнение данных
        # добавление в БД
        wnd = NewBoss()
        wnd.show()
        print("new boss")

    def ev_new_bill(self):
        # открыть сканер
        # распознать отсканированный
        # добавить значение в БД
        # сохранить скрин в папку месяца
        print("new bill")

    def ev_new_build(self):
        # открыть форму для нового объекта
        # заполнить данные
        # добавить объект в БД
        # получить новый список объектов для списка объектов на главном меню
        print("new build")

    def ev_new_person(self):
        # открыть окно для нового сотрудника
        # заполнить данные
        # отправить в БД
        print("new person")

    def ev_create_act(self):
        print("create act")

    def ev_get_material(self):
        # открыть форму для ввода название материала и даты завоза
        # сформировать документ
        # печать
        print("get mat")

    def ev_pdf_check(self):
        # открыть директорию
        # рассортировать все отсканированные файлы по папкам
        print("pdf check")

    def ev_send_covid(self):
        # если нет соответствующего файла, то открыть окно для сканирования
        # сформировать письмо
        # взять ковид из папки
        # отправить
        print("send covid")

    def ev_connect(self):
        # подключиться к серверу
        self.r_connect.setChecked(True)
        print("connect")

    def ev_new_invoice(self):
        # открыть сканер
        # добавить накладную в папку
        print("create invoice")

    def ev_new_boss_post(self):
        # получить весь список боссов
        # открыть окно для нового босса. Боса можно выбрать старого или ввести новые данные.
        # ввести данные
        # добавить в БД
        print("new post of boss")

    def ev_journal(self):
        # печать ковид журнала
        print("journal")

    def ev_tabel(self):
        # печать табеля
        print("tabel")

    def ev_scan(self):
        # открыть сканер
        print("scan")

    def ev_attorney(self):
        # печать доверенности
        self.r_connect.setChecked(True)
        print("attorney")

    def ev_invoice(self):
        # печать накладной
        self.r_connect.setChecked(True)
        print("invoice")

    # работа с Excel
    def open_wb(self, name):
        path = "D:/test.xlsx"
        wb_obj = openpyxl.load_workbook(path)
        if name in wb_obj.sheetnames:
            my_sheet = wb_obj[name]
            return wb_obj, my_sheet
        else:
            logging.info("данного листа в книге не существует")
            print("нет выбранного листа " + name)
            return None, None

    def add_new_row_to_excel(self, row):
        self.sheet.insert_rows(idx=10, amount=1)
        i = iter(range(10))
        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))
        for item in row:
            cell = self.sheet.cell(row=10, column=next(i))
            cell.value = item
            cell.border = thin_border

    def set_week_days(self, days):
        if len(days) > 1:
            title = "Прошу Вас разрешить работы в выходные дни {0} г. и {1}. по ремонту {2} работникам {3}, " \
                    "с рабочей сменой с 07-00 до 19-00 часов:".format(*days, self.current_build, self.company)
        else:
            title = "Прошу Вас разрешить работы в выходной день {0} г. и {1}. по ремонту {2} работникам {3}, " \
                    "с рабочей сменой с 07-00 до 19-00 часов:".format(*days, self.current_build, self.company)
        cell = self.sheet.cell(row=15, column=1)
        cell.value = title

    def set_numder_and_date(self):
        if datetime.datetime.now().month < 10:
            month = "0" + str(datetime.datetime.now().month)
        else:
            month = str(datetime.datetime.now().month)
        date = str(datetime.datetime.now().day) + "." + \
                month + "." + \
                str(datetime.datetime.now().year)
        cell_count = self.sheet.cell(row=5, column=0)
        cell_data = self.sheet.cell(row=6, column=0)
        cell_count.value = "Исх. №" + self.next_number_doc()
        cell_data.value = "от " + date

    def set_month_date(self):
        now_month = datetime.datetime.now().month
        next_month = 1 if now_month == 12 else now_month + 1
        num_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 29)
        if datetime.datetime.now().year / 4 == 0:
            ind = num_days[12]
        else:
            ind = next_month
        max_day = num_days[ind]

        pass

    # database
    def connect_to_database(self):
        self.database_conn = psycopg2.connect(dbname='Company', user='postgres',
                                                password='pol_ool_123', host='localhost')
        self.database_cur = self.database_conn.cursor()
        pass

    # Прочее
    def next_number_doc(self):
        return "600"


if __name__ == "__main__":
    # app = Notebook()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
