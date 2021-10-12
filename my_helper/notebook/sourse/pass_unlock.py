from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from my_helper.notebook.sourse.inserts import get_from_db
import datetime as dt
import os
from PyQt5.QtCore import QDate as Date
from PyQt5 import QtCore, QtGui, QtWidgets
import docx
import docxtpl
#  сделать мессаджбоксы на Сохранить
main_file = "D:/my_helper/unlock.docx"
print_file = "D:/my_helper/to_print/unlock.docx"
designer_file = '../designer_ui/pass_unlock.ui'
count_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

class UnlockPass(QDialog):
    def __init__(self, parent):
        super(UnlockPass, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.table = "workers"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_open.clicked.connect(self.my_open_file)
        self.d_note.setDate(dt.datetime.now().date())
        self.d_from.setDate(dt.datetime.now().date())
        self.d_to.setDate(QtCore.QDate(*self.get_end_month()))
        # self.d_to.setDate(Date.fromString(self.get_end_month()))
        self.number.setValue(self.parent.get_next_number())
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}

    def get_end_month(self):
        next_month = dt.datetime.now().month
        # если конец года: увеличить год и месяц в 1
        next_day = count_days[next_month]
        next_month = str(next_month)
        if int(next_month) < 10:
            next_month = "0" + next_month
        next_year = str(dt.datetime.now().year)

        if int(next_year) / 4 == 0:
            end_next_month = str(count_days[12])
        else:
            end_next_month = str(count_days[int(next_month)])
        print(".".join((end_next_month, next_month, next_year)))
        return (end_next_month, next_month, next_year)

    def init_workers(self):
        self.cb_worker.addItem("(нет)")
        for name in self.parent.db.get_data("family, name", self.table):
            self.cb_worker.addItem(" ".join((name[0], name[1][0])) + ".")

    # обработчики кнопок
    def ev_ok(self):
        if not self.get_data():
            return None

        doc = docxtpl.DocxTemplate(main_file)
        doc.render(self.data)
        doc.save(print_file)
        self.close()
        os.startfile(print_file)


    def ev_cancel(self):
        self.close()

    def my_open_file(self):
        os.startfile(main_file)
        pass

    def get_data(self):
        family = self.cb_worker.currentText()
        for row in self.parent.db.get_data("family, name, surname, post, live_adr", self.table):
            if family[:-3] == row[0]:  # на форме фамилия в виде Фамилия И.
                self.data["number"] = "Исх. № " + self.number.text()
                self.data["data"] = "от. " + self.d_note.text()
                self.data["family"] = row[0]
                self.data["name"] = row[1]
                self.data["surname"] = row[2]
                self.data["post"] = row[3]
                self.data["adr"] = row[4]
                self.data["start_date"] = self.d_from.text()
                self.data["end_date"] = self.d_to.text()
                self.data["customer"] = self.parent.customer
                self.data["company"] = self.parent.company
                if "" in self.data:
                    return False
                return True

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()