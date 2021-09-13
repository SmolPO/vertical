from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import datetime as dt
import os
import docxtpl
from my_helper.notebook.sourse.inserts import get_from_db

#  сделать мессаджбоксы на Сохранить
main_file = "B:/my_helper/drive.docx"
print_file = "B:/my_helper/to_print/drive.docx"
designer_file = '../designer_ui/pass_drive.ui'


class DrivePass(QDialog):
    def __init__(self, parent):
        super(DrivePass, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.table = "drivers"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_contracts.activated[str].connect(self.contract_changed)
        self.cb_auto.activated[str].connect(self.auto_changed)
        self.cb_drivers.activated[str].connect(self.driver_changed)

        self.cb_activ.stateChanged.connect(self.manual_set)
        self.d_arrive.dateChanged.connect(self.date_changed)
        self.input_text.textChanged.connect(self.text_changed)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())
        self.data = {"number": "", "date": "", "text_note": "", "auto": "",
                     "gov_number": "", "track_number": " ", "passport": "", "adr": ""}
        self.work = ""
        self.data_arrive = ""
        self.contract = ""
        self.my_text = ""
        self.contracts = [[]]
        self.init_auto()
        self.init_drivers()
        self.init_contracts()
        self.rows_from_db = self.from_db("*", self.table)
        self.d_arrive.setDate(dt.datetime.now().date())

    # инициализация
    def init_drivers(self):
        self.cb_drivers.addItem("(нет)")
        for row in self.from_db("family, name", self.table):
            self.cb_drivers.addItem(" ".join((row[0], row[1][0] + ".")))

    def init_auto(self):
        self.cb_auto.addItem("(нет)")
        for row in self.from_db("model, gov_number", "auto"):
            self.cb_auto.addItem(row[0])

    def init_contracts(self):
        self.cb_contracts.addItem("(нет)")
        for row in self.from_db("name", "contract"):
            self.cb_contracts.addItem(row[0])

    # для заполнения текста
    def get_data(self):
        self.data["number"] = "Исх. № " + self.number.text()
        self.data["date"] = "от. " + self.d_note.text()
        self.data["text_note"] = self.note.toPlainText()
        self.data["contract"] = self.cb_contracts.currentText()
        self.data["d_arrive"] = self.d_arrive.text()
        if "" in self.data:
            return False
        return True

    # обработчики кнопок
    def ev_ok(self):
        if not self.get_data():
            return
        doc = docxtpl.DocxTemplate(main_file)
        doc.render(self.data)
        doc.save(print_file)
        self.close()
        os.startfile(print_file)

    def ev_cancel(self):
        self.close()

    def my_open_file(self):
        os.startfile(print_file)

    def date_changed(self):
        self.data_arrive = self.d_arrive.text()
        self.change_note()

    def contract_changed(self):
        for row in self.from_db("*", "contract"):
            if self.cb_contracts.currentText() == row[0]:
                self.work = " ".join(row[4:7])
                self.contract = " от ".join(row[2:4])
            if self.cb_contracts.currentText() == "(нет)":
                self.work = ""
                self.contract = ""
        self.change_note()

    def text_changed(self):
        self.my_text = self.input_text.toPlainText()
        self.change_note()

    def change_note(self):
        text = list()
        text.append("Прошу Вашего разрешения оформить разовый электронный пропуск на ")
        text.append(self.data_arrive)
        text.append("с 08-00 до 17-00 для проезда на территорию")
        text.append(self.parent.customer)
        text.append(" и ")
        text.append(self.my_text)
        text.append(self.work)
        text.append(self.contract)
        self.note.setText(" ".join(text))

    def manual_set(self, state):
        if state == Qt.Checked:
            self.note.setEnabled(True)
            self.input_text.setEnabled(False)
            self.d_arrive.setEnabled(False)
            self.cb_contracts.setEnabled(False)
        else:
            self.note.setEnabled(False)
            self.input_text.setEnabled(True)
            self.d_arrive.setEnabled(True)
            self.cb_contracts.setEnabled(True)

    def auto_changed(self):
        for row in self.from_db("*", "auto"):
            if self.cb_auto.currentText() == row[0]:
                self.data["auto"] = " ".join(row[:2])
                self.data["gov_number"] = row[2]
                self.data["track_number"] = "п/п " + row[-1] if row[-1] else " "

    def driver_changed(self):
        for row in self.from_db("*", "drivers"):
            if self.cb_drivers.currentText()[:-3] == row[0]:
                self.data["passport"] = " ".join(row[:])
                self.data["adr"] = row[-1]

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()