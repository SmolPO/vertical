from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.inserts import get_from_db
import datetime as dt
import os
import docx
import docxtpl
#  сделать мессаджбоксы на Сохранить
main_file = "B:/my_helper/week.docx"
print_file = "B:/my_helper/to_print/week.docx"
designer_file = "../designer_ui/pass_week.ui"


class WeekPass(QDialog):
    def __init__(self, parent):
        super(WeekPass, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.workers = [self.worker_1, self.worker_2, self.worker_3,
                        self.worker_4, self.worker_5, self.worker_6,
                        self.worker_7, self.worker_8, self.worker_9]
        self.table = "contract"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_other.stateChanged.connect(self.other_days)
        self.cb_sun.stateChanged.connect(self.week_days)
        self.cb_sub.stateChanged.connect(self.week_days)
        self.d_from.setEnabled(False)
        self.d_to.setEnabled(False)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())
        self.data = {"number": "", "date": "", "week_day": "", "contract": "", "type_work": "",
                     "part": "", "company": "", "customer": "", "post_boss": "", "boss_part": ""}
        self.list_ui = (self.worker_1, self.worker_2, self.worker_3, self.worker_4,
                        self.worker_5, self.worker_6, self.worker_7, self.worker_8, self.worker_9)
        self.rows_from_db = self.from_db("*", self.table)
        self.init_object()
        self.init_boss()
        self.init_workers()

    # выбор дня
    def other_days(self, state):
        if state == Qt.Checked:
            self.cb_sun.setEnabled(False)
            self.cb_sub.setEnabled(False)
            self.d_from.setEnabled(True)
            self.d_to.setEnabled(True)
        else:
            self.cb_sun.setEnabled(True)
            self.cb_sub.setEnabled(True)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)

    def week_days(self, state):
        if state == Qt.Checked:
            self.cb_other.setEnabled(False)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)
        elif not self.cb_sun.isChecked() and not self.cb_sub.isChecked():
            self.cb_other.setEnabled(True)

    # заполнение список
    def get_days(self):
        data = []
        now_weekday = dt.datetime.now().weekday()
        if self.cb_other.isChecked():
            data.append([self.d_from.text(), self.d_to.text()])
            return data
        if self.cb_sun.isChecked():
            sub_day = dt.datetime.now() + dt.timedelta(5 - now_weekday)
            data.append(".".join((str(sub_day.day), str(sub_day.month), str(sub_day.year))))
        if self.cb_sub.isChecked():
            sun_day = dt.datetime.now() + dt.timedelta(6 - now_weekday)
            data.append(".".join([str(sun_day.day), str(sun_day.month), str(sun_day.year)]))
        return data

    def init_object(self):
        self.cb_object.addItem("(нет)")
        for row in self.rows_from_db:
            self.cb_object.addItem(row[0])

    def init_boss(self):
        for people in self.from_db("family, name, surname, post", "bosses"):
            try:
                family = people[0] + " " + people[1][0] + ". " + people[2][0] + "."
                self.cb_boss_part.addItem(family)       # брать из БД
            except:
                pass

    def init_workers(self):
        for item in self.list_ui:
            item.addItem("(нет)")
            item.activated[str].connect(self.new_worker)
            item.setEnabled(False)
        self.list_ui[0].setEnabled(True)
        for name in self.from_db("family, name, surname, post, passport, "
                                 "passport_got, birthday, adr,  live_adr", "workers"):
            family = name[0] + " " + ".".join([name[1][0], name[2][0]]) + "."
            for item in self.list_ui:
                item.addItem(family)

    # обработчики кнопок
    def ev_ok(self):
        self.data["customer"] = self.parent.customer
        self.data["company"] = self.parent.company
        self.data["number"] = "Исх. № " + self.number.text()
        self.data["date"] = "от. " + self.d_note.text()
        self.data["boss_part"] = self.cb_boss_part.currentText()
        self.data["post_boss"] = "Начальник цеха"
        self.get_contract(self.cb_object.currentText())
        self.get_week_days()

        doc = docxtpl.DocxTemplate(main_file)
        doc.render(self.data)
        doc.save(print_file)

        # Заполнить таблицу
        doc = docx.Document(print_file)
        i = iter(range(1, 100))
        for elem in self.list_ui:
            family = elem.currentText()
            if family != "(нет)":
                doc.tables[1].add_row()
                people = self.get_worker(family)
                doc.tables[1].rows[1].cells[0].text = str(next(i))
                doc.tables[1].rows[1].cells[1].text = " ".join(people[:3])
                doc.tables[1].rows[1].cells[2].text = people[3]
                doc.tables[1].rows[1].cells[3].text = people[6]
                doc.tables[1].rows[1].cells[4].text = " ".join(people[4:6])
                doc.tables[1].rows[1].cells[5].text = people[7]
                doc.tables[1].rows[1].cells[6].text = people[8]
        doc.save(print_file)
        self.close()
        os.startfile(print_file)

    def ev_cancel(self):
        self.close()

    def new_worker(self):
        flag = True
        for item in self.list_ui:
            if item.currentText() != "(нет)":
                item.setEnabled(True)
            else:
                item.setEnabled(flag)
                flag = False

    def my_open_file(self):
        os.startfile(print_file)

    def get_contract(self, name):
        # получить номер договора по короткому имени
        for row in self.from_db("number, date, object, part, work", "contract"):
            if name in row:
                self.data["contract"] = " от ".join(row[:2])
                self.data["object_name"] = row[2]
                self.data["part"] = row[3]
                self.data["type_work"] = row[4]

    def get_worker(self, family):
        # получить номер договора по короткому имени
        for row in self.from_db("family, name, surname, post, passport, passport_got, "
                                "birthday, adr,  live_adr", "workers"):
            if family[:-5] == row[0]:
                return row
            return row

    def get_week_days(self):
        if self.cb_other.isChecked():
            self.data["week_day"] = "в выходные дни с " + self.d_from.text() + " до " + self.d_to.text()
        else:
            if len(self.get_days()) > 1:
                self.data["week_day"] = "в выходные дни с " + str(self.get_days()[0]) + " до " + str(self.get_days()[1])
            else:
                self.data["week_day"] = "в выходной день " + str(self.get_days()[0])

    def save_pattern(self):
        pass

    def kill_pattern(self):
        pass

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()