from PyQt5.QtCore import Qt
import datetime as dt
from my_helper.notebook.sourse.my_pass.pass_template import TempPass
from PyQt5.QtWidgets import QMessageBox as mes
#  сделать мессаджбоксы на Сохранить
from my_helper.notebook.sourse.database import *
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("pass_driver")


class DrivePass(TempPass):
    def __init__(self, parent):
        super(DrivePass, self).__init__(designer_file, parent, "drivers")
        if not self.status_:
            return
        self.cb_contracts.activated[str].connect(self.contract_changed)
        self.cb_auto.activated[str].connect(self.auto_changed)
        self.cb_drivers.activated[str].connect(self.driver_changed)

        self.cb_activ.stateChanged.connect(self.manual_set)
        self.d_arrive.dateChanged.connect(self.date_changed)
        self.input_text.textChanged.connect(self.change_note)
        self.input_text.textChanged.connect(self.change_note)

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
        self.d_arrive.setDate(dt.datetime.now().date())
        self.main_file += "/pass_drive.docx"

    # инициализация
    def init_drivers(self):
        self.cb_drivers.addItem(empty)
        try:
            people = self.parent.db.get_data("family, name", self.table)
        except:
            return msg(self, my_errors["3_get_db"])
        if not people:
            return
        for row in people:
            self.cb_drivers.addItem(" ".join((row[0], row[1][0] + ".")))

    def init_auto(self):
        self.cb_auto.addItem(empty)
        try:
            auto = self.parent.db.get_data("gov_number", "auto")
        except:
            return msg(self, my_errors["3_get_db"])
        if not auto:
            return
        for row in auto:
            self.cb_auto.addItem(row[0])

    def init_contracts(self):
        self.cb_contracts.addItem(empty)
        try:
            contracts = self.parent.db.get_data("name", "contracts")
        except:
            return msg(self, my_errors["3_get_db"])
        if not contracts:
            return
        for row in contracts:
            self.cb_contracts.addItem(row[0])

    # для заполнения текста
    def _get_data(self):
        self.data["text_note"] = self.note.toPlainText()
        self.data["contract"] = self.cb_contracts.currentText()
        self.data["d_arrive"] = self.d_arrive.text()

    # обработчики кнопок
    def _ev_ok(self):
        return True

    def date_changed(self):
        self.data_arrive = self.d_arrive.text()
        self.change_note()

    def contract_changed(self):
        try:
            rows = self.parent.db.get_data("*", "contracts")
        except:
            return msg(self, my_errors["3_get_db"])
        for row in rows:
            if self.cb_contracts.currentText() == row[0]:
                self.work = " ".join(row[4:7])
                self.contract = " от ".join(row[2:4])
            if self.cb_contracts.currentText() == empty:
                self.work = ""
                self.contract = ""
        self.change_note()

    def change_note(self):
        text = list()
        text.append("Прошу Вашего разрешения оформить разовый электронный пропуск на ")
        text.append(self.data_arrive)
        text.append("с 08-00 до 17-00 для проезда на территорию")
        text.append(self.parent.customer)
        text.append(" и ")
        text.append(self.input_text.toPlainText())
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
        try:
            rows = self.parent.db.get_data("*", "auto")
        except:
            return msg(self, my_errors["3_get_db"])
        for row in rows:
            print(self.cb_auto.currentText(), row[0])
            if self.cb_auto.currentText() == row[0]:
                self.data["auto"] = " ".join(row[1:3])
                self.data["gov_number"] = row[0]
                self.data["track"] = " " if row[-2] == empty else "п/п " + row[-2]

    def driver_changed(self):
        try:
            people = self.parent.db.get_data("*", self.table)
        except:
            return msg(self, my_errors["3_get_db"])
        if not people:
            return
        for row in people:
            if self.cb_drivers.currentText()[:-3] == row[0]:
                self.data["passport"] = " ".join(row[:-1])
                self.data["adr"] = row[-2]

    def _create_data(self, doc):
        pass

    def check_input(self):
        for key in self.data.keys():
            if self.data[key] == empty or self.data[key] == "":
                return msg(self, my_errors["13_full_all_fields"])
        return True