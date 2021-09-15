from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
import datetime as dt
import webbrowser
from config import link_fuer
import docxtpl
import os
from my_helper.notebook.sourse.inserts import get_from_db, update_mat
designer_file = '../designer_ui/music.ui'
main_file = ""
print_file = ""


class GetMoney(QDialog):
    def __init__(self, parent=None):
        super(GetMoney, self).__init__(parent)
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.bosses = []
        self.table = "bills"

        self.b_ok.clicked.connect(self.ev_start)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_get_fuer.clicked.connect(self.ev_fuer)
        self.cb_pattern.activated[str].connect(self.ev_pattern)
        self.date.setDate(dt.datetime.now().date())
        self.data = {"date": "", "summ": "", "note": "", "family": "", "post": "", "reciver": ""}

        for row in self.from_db("id", self.table):
            self.cb_pattern.addItems([row])

    def ev_fuer(self):
        webbrowser.open(link_fuer)

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()

    def ev_cancel(self):
        self.close()

    def set_data(self, data):
        self.cb_rec.setText(data[0])
        self.summ.setText(data[1])
        self.note.setText(data[2])
        self.date.setDate(Date.fromString(data[3], "dd.mm.yyyy"))

    def get_data(self):
        status = 0
        next_id = len(self.from_db("*", self.table))
        data = list((self.date.text(), self.summ.text(),
                     self.cb_rec.currentText(), self.note.add_link.text(), status, next_id))
        if "" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        return data

    def clean_data(self):
        self.name.setText("")
        self.add_link.setText("")

    def ev_select(self):
        for row in self.from_db("*", self.table):
            if self.cb_pattern.currentText().split()[0] in row:
                self.set_data(row)

    def create_note(self):
        doc = docxtpl.DocxTemplate(main_file)
        doc.render(self.data)
        doc.save(print_file)
        self.close()
        os.startfile(print_file)
