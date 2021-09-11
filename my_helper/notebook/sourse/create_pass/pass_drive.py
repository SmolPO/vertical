from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import datetime as dt
import os
import docxtpl
from ..inserts import get_from_db

#  сделать мессаджбоксы на Сохранить
main_file = "B:/my_helper/drive.docx"
print_file = "B:/my_helper/to_print/drive.docx"
designer_file = '../../designer_ui/pass_drive.ui'


class DrivePass(QDialog):
    def __init__(self, parent):
        super(DrivePass, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_contract.activated[str].connect(self.contract_changed)
        self.cb_auto.activated[str].connect(self.auto_changed)
        self.cb_driver.activated[str].connect(self.driver_changed)

        self.cb_activ.stateChanged.connect(self.manual_set)
        self.d_arrive.dateChanged.connect(self.date_changed)
        self.input_text.textChanged.connect(self.text_changed)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())
        self.data = {"number": "", "date": "", "text_note": "", "brand": "",
                     "gov_number": "", "track_number": " ", "passport": "", "adr": ""}
        self.work = ""
        self.data_arrive = ""
        self.contract = ""
        self.my_text = ""
        self.contracts = [[]]
        self.init_auto()
        self.init_drivers()
        self.init_object()

    # инициализация
    def init_drivers(self):
        self.cb_drivers.addItem("(нет)")
        self.parent.db.execute(get_from_db("family, name", "auto"))
        rows = self.parent.db.fetchall()
        for row in rows:
            self.cb_drivers.addItem(" ".join((row[0], row[1][0] + ".")))

    def init_auto(self):
        self.cb_auto.addItem("(нет)")
        self.parent.db.execute(get_from_db("model, gov_number", "auto"))
        rows = self.parent.db_cur.fetchall()
        for row in rows:
            self.cb_auto.addItem(row[0])

    def init_object(self):
        self.cb_object.addItem("(нет)")
        self.parent.db.execute(get_from_db("name", "contract"))
        rows = self.parent.db.fetchall()
        for row in rows:
            self.cb_contracts.addItem(row[0])

    # для заполнения текста
    def get_data(self):
        self.data["number"] = "Исх. № " + self.number.text()
        self.data["date"] = "от. " + self.d_note.text()
        self.data["text_note"] = self.note.toPlainText()
        self.data["contract"] = self.cb_contracts.currentText()
        self.data["d_arrive"] = self.d_arrive.text()
        if "" in self.data:
            return None

    # обработчики кнопок
    def ev_OK(self):
        if not self.get_data():
            return
        doc = docxtpl.DocxTemplate(main_file)
        doc.render(self.data)
        doc.save(print_file)
        os.startfile(print_file)
        self.close()

    def ev_cancel(self):
        self.close()

    def my_open_file(self):
        os.startfile(print_file)

    def data_changed(self):
        self.data_arrive = self.d_arrive.text()
        self.change_note()

    def contract_changed(self):
        self.parent.db.execute(get_from_db("*", "contract"))
        rows = self.parent.db_cur.fetchall()
        for row in rows:
            if self.cb_contracts.currentText() == row[0]:
                self.work = " ".join(row[4:7])
                self.contract = " от ".join(row[2:4])
        self.change_note()

    def text_changed(self):
        self.my_text = self.note_text.text()

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
            self.cb_contract.setEnabled(False)
        else:
            self.note.setEnabled(False)
            self.input_text.setEnabled(True)
            self.d_arrive.setEnabled(True)
            self.cb_contract.setEnabled(True)

    def auto_changed(self):
        self.parent.db.execute(get_from_db("*", "auto"))
        rows = self.parent.db_cur.fetchall()
        for row in rows:
            if self.cb_auto.currentText() == row[0]:
                self.data["model"] = row[0]
                self.data["brand"] = row[1]
                self.data["gov_number"] = row[2]
                self.data["track_number"] = "п/п " + row[-1] if row[-1] else " "

    def driver_changed(self):
        self.parent.db.execute(get_from_db("*", "drivers"))
        rows = self.parent.db_cur.fetchall()
        for row in rows:
            if self.cb_drivers.currentText()[:-3] == row[0]:
                self.data["password"] = " ".join(row[:])
                self.data["adr"] = row[-1]
