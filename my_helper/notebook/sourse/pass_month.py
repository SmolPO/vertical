from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import inserts
import datetime as dt
import docx
import docxtpl
#  сделать мессаджбоксы на Сохранить
count_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class MonthPass(QDialog):
    def __init__(self, parent):
        super(MonthPass, self).__init__()
        uic.loadUi('../designer_ui/pass_month.ui', self)
        # pass
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_all.stateChanged.connect(self.set_enabled_workers)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())

        self.list_ui = (self.worker_1, self.worker_2, self.worker_3, self.worker_4, self.worker_5, self.worker_6,
                   self.worker_7, self.worker_8, self.worker_9)
        self.list_month = ["январь", "февраль", "март", "апрель",
                           "май", "июнь", "июль", "август", "сентябрь",
                           "октябрь", "ноябрь", "декабрь"]
        self.data = {"customer": "", "company": "", "start_date": "", "end_date": "",
                "post": "", "family": "", "name": "", "surname": "", "adr": "",
                "number": "", "data": "", "str_1": "", "str_2": "", "str_3": ""}
        self.init_recipient()
        self.init_workers()
        self.init_cb_month()

    # инициализация
    def init_cb_month(self):
        for elem in self.list_month:
            self.cb_month.addItem(elem)

    def init_recipient(self):
        self.parent.database_cur.execute(inserts.get_bosses())
        rows = self.parent.database_cur.fetchall()
        self.cb_boss.addItem("(нет)")
        for post in rows:
            self.cb_boss.addItem(post[0])

    def init_workers(self):
        self.parent.database_cur.execute(inserts.pass_workers())
        rows = self.parent.database_cur.fetchall()
        for item in self.list_ui:
            item.addItem("(нет)")
        for name in rows:
            family = name[0] + " " + ".".join([name[1][0], name[2][0]]) + "."
            for item in self.list_ui:
                item.addItem(family)

    # флаг на выбор всех
    def set_enabled_workers(self, state):
        for elem in self.list_ui:
            elem.setEnabled(state != Qt.Checked)

    # получить данные
    # для заполнения текста
    def get_data(self):
        next_month = self.list_month.index(self.cb_month.currentText()) + 1
        print("month: ", self.cb_month.currentText(), " index:", next_month)
        # если конец года: увеличить год и месяц в 1
        if next_month == 13:
            next_day = "09"
            next_month = "01"  # MessageBox для ввода первого дня
            next_year = str(dt.datetime.now().year + 1)
        else:
            next_day = "01"
            next_month = str(next_month)
            if int(next_month) < 10:
                next_month = "0" + next_month
            next_year = str(dt.datetime.now().year)

        if int(next_year) / 4 == 0:
            end_next_month = str(count_days[12])
        else:
            end_next_month = str(count_days[int(next_month)])

        self.data["customer"] = self.parent.customer
        self.data["company"] = self.parent.company
        self.data["start_date"] = ".".join((next_day, next_month, next_year))
        self.data["end_date"] = ".".join((end_next_month, next_month, next_year))

    # получить босса
    def get_boss(self):
        boss = []
        self.parent.database_cur.execute(inserts.get_bosses("all"))
        bosses = self.parent.database_cur.fetchall()
        for item in bosses:
            if self.cb_boss.currentText() == item[3]:
                boss = item  # фамилия, имя, отчество, должность, пол
                break
        short_name = str(boss[1] + " " + ".".join((boss[0][0], boss[2][0])) + ".")  # склонение!!!!
        post_split = boss[3].split(" ")
        i = []
        if len(post_split) <= 4:
            i = [0, 2, 4]
        elif len(post_split) <= 6:
            i = [0, 2, 6]
        elif len(post_split) <= 8:
            i = [0, 4, 8]
        self.data["str_1"] = " ".join(post_split[i[0]:i[1]])
        self.data["str_2"] = " ".join(post_split[i[1]:i[2]])
        self.data["str_2" if self.data["str_2"] == "" else "str_3"] = short_name
        title = "Уважаемая " if boss[4] == "Ж" else "Уважаемый "
        self.data["title"] = title + boss[0] + " " + boss[2] + "!"

    def get_worker(self, family):
        self.parent.database_cur.execute(inserts.pass_workers())
        rows = self.parent.database_cur.fetchall()
        if family == "all":
            return rows
        for row in rows:
            if family[:-5] == row[0]:  # на форме фамилия в виде Фамилия И.О.
                return row

    # обработчики кнопок
    def ev_OK(self):
        self.date["number"] = "Исх. № " + self.number.text(),
        self.data["data"] = "от. " + self.d_note.text()

        self.get_data()
        self.get_boss()
        doc = docxtpl.DocxTemplate("B:/my_helper/month.docx")
        doc.render(self.data)

        doc.save("B:/my_helper/to_print/month.docx")
        doc = docx.Document("B:/my_helper/month.docx")
        # Заполнить таблицу
        workers = []
        if self.cb_all.isChecked():
            workers = self.get_worker("all")
        else:
            for elem in self.list_ui:
                if elem.currentText() != "(нет)":
                    workers.append(self.get_worker(elem.currentText()))
        i = 1
        for people in workers:
            doc.tables[1].add_row()
            doc.tables[1].rows[i].cells[0].text = str(i)
            doc.tables[1].rows[i].cells[1].text = " ".join(people[0:2])
            doc.tables[1].rows[i].cells[2].text = people[3]
            doc.tables[1].rows[i].cells[3].text = people[6]
            doc.tables[1].rows[i].cells[4].text = " ".join(people[4:6])
            doc.tables[1].rows[i].cells[5].text = people[7]
            doc.tables[1].rows[i].cells[6].text = people[8]
            i += 1
        doc.save("B:/my_helper/to_print/month.docx")
        self.close()

    def ev_cancel(self):
        self.close()

    def save_pattern(self):
        data = {"who": self.cb_who.text(),
                "object_name": self.cb_object.text(),
                "workers": self.get_list()}
        self.zip_pattern(data)
        # запоковать в словарь
        # сохранить в файл

    def my_open_file(self):
        print("open file")
        pass

    def kill_pattern(self):
        pass






