from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.template import TempForm
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = '../designer_ui/new_driver.ui'
fields = ["family", "name", "surname", "birthday", "passport", "id"]


class NewDriver(TempForm):
    def __init__(self, parent=None):
        super(NewDriver, self).__init__(designer_file)
        self.parent = parent
        self.table = "drivers"
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        if not self.rows_from_db:
            self.close()
        self.table = "drivers"

        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        if not self.rows_from_db:
            self.close()

        self.list_ui = [self.family, self.name, self.surname, self.passport, self.adr, self.d_birthday]
        self.slice_set = len(self.list_ui)
        self.slice_get = len(self.list_ui) - 1
        self.slice_clean = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        for item in self.list_ui:
            item.setValidator(symbols)

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_data()
            self.but_status("add")
            return
        self.but_status("change")

        family = text[:-3]
        for row in self.rows_from_db:
            if family in row:
                self.set_data(row)

    def set_data(self, data):
        self.family.setText(data[0])
        self.name.setText(data[1])
        self.surname.setText(data[2])
        self.d_birthday.setDate(Date.fromString(data[3]))
        self.passport.clear()
        self.adr.clear()
        self.passport.append(data[4])
        self.adr.append(data[5])

    def get_data(self):
        data = list()
        for item in self.list_ui:
            try:
                data.append(item.text())
            except:
                data.append(item.toPlainText())
        if "" in data or "01.01.2000" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return
        return data

    def clean_data(self):
        for item in self.list_ui:
            try:
                item.setText("")
            except:
                item.clear()
