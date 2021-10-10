from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.inserts import get_from_db
from my_helper.notebook.sourse.template import TempForm
"""
валидация, защита от ввода в табл в разнобой
"""
designer_file = '../designer_ui/new_contract.ui'
fields = ["name", "customer", "number", "date", "object", "type_work", "place", "id"]


class NewContact(TempForm):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(designer_file)
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.table = "contract"
        self.contract = []
        self.comp = []
        self.init_mask()
        self.parent.db.init_list(self.cb_comp, "*", self.table)
        self.list_ui = [self.name, self.customer, self.number, self.date, self.adr, self.d_birthday]
        self.slice_set = 3
        self.slice_get = 3
        self.slice_clean = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))

    def _ev_select(self, text):
        return True

    def _clean_date(self):
        self.cb_comp.setCurrentText("(нет)")  # TODO set text
        self.date.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

    def _set_data(self, data):
        self.date.setDate(Date.fromString(data[3], "dd.mm.yyyy"))

    def _get_data(self, data):
       return data

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.my_object.toPlainText(), self.work.toPlainText(),
                      self.part.text()]) and self.date.text() != "01.01.2000":
            return False
        return True
