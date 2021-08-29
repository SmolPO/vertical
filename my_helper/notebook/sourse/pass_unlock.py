from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
import inserts
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
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_open.clicked.connect(self.my_open_file)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())

        self.init_workers()

    def init_workers(self):
        self.parent.database_cur.execute(inserts.get_workers("ФИО"))
        rows = self.parent.database_cur.fetchall()
        self.cb_worker.addItem("(нет)")
        for name in rows:
            self.cb_worker.addItem(name[0] + " " + ".".join([name[1][0], name[2][0]]) + ".")

    # обработчики кнопок
    def ev_OK(self):
        worker = self.get_worker(self.cb_worker.currentText())
        worker["number"] = "Исх. № " + self.number.text()
        worker["data"] = "от. " + self.d_note.text()

        doc = docxtpl.DocxTemplate(main_file)
        doc.render(worker)
        doc.save(print_file)
        os.startfile(print_file, "print")
        self.close()

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
        os.startfile(main_file)
        pass

    def get_worker(self, family):
        data = {"customer": "", "company": "", "start_date": "", "end_date": "",
                "post": "", "family": "", "name": "", "surname": "", "adr": "", "number": "", "data": ""}
        self.parent.database_cur.execute(inserts.pass_workers())
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if family[:-5] == row[0]:  # на форме фамилия в виде Фамилия И.О.
                data["family"] = row[0]
                data["name"] = row[1]
                data["surname"] = row[2]
                data["post"] = row[3]
                data["adr"] = row[8]
                data["start_date"] = self.d_from.text()
                data["end_date"] = self.d_to.text()
                data["customer"] = self.parent.customer
                data["company"] = self.parent.company
                return data
