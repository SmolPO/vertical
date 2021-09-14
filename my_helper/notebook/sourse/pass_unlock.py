from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from my_helper.notebook.sourse.inserts import get_from_db
import datetime as dt
import os
import docx
import docxtpl
#  сделать мессаджбоксы на Сохранить
main_file = "B:/my_helper/unlock.docx"
print_file = "B:/my_helper/to_print/unlock.docx"
designer_file = '../designer_ui/pass_unlock.ui'


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
        self.d_to.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())
        self.rows_from_db = self.from_db("*", self.table)
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}

    def init_workers(self):
        self.cb_worker.addItem("(нет)")
        for name in self.from_db("family, name", self.table):
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
        for row in self.from_db("family, name, surname, post, live_adr", self.table):
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