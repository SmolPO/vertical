from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.create.new_template import TempForm, from_str
from PyQt5.QtWidgets import QMessageBox as mes
"""
валидация, защита от ввода в табл в разнобой
"""
from my_helper.notebook.sourse.database import get_path_ui

# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_contract")
fields = ["name", "customer", "number", "date", "object", "type_work", "place", "id"]
zero = "01.01.2000"


class NewContact(TempForm):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(designer_file)
        self.parent = parent
        self.table = "contracts"
        self.init_mask()
        self.parent.db.init_list(self.cb_comp, "company", "company")
        self.parent.db.init_list(self.cb_select, "name", self.table)
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.list_ui = [self.name, self.cb_comp, self.part, self.number, self.date, self.my_object, self.work]

        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))

    def _ev_select(self, text):
        self.slice_select = len(text)
        return True

    def _clean_data(self):
        self.name.setText("")
        self.cb_comp.setCurrentIndex(0)
        self.part.setText("")
        self.number.setText("")
        self.date.setDate(Date(*from_str("01.01.2000")))
        self.my_object.clear()
        self.work.clear()
        self.cb_comp.setCurrentText("(нет)")

    def _set_data(self, data):
        self.name.setText(data[0])
        g = iter(range(len(self.rows_from_db) + 1))
        for item in self.rows_from_db:
            next(g)
            if data[-1] == item[-1]:
                self.cb_comp.setCurrentIndex(next(g))
                break
        self.part.setText(data[6])
        self.number.setText(data[0])
        self.date.setDate(Date(*from_str(data[3])))
        self.my_object.clear()
        self.work.clear()
        self.my_object.append(data[4])
        self.work.append(data[5])

    def _get_data(self, data):
        data.append(self.name.text())
        data.append(self.cb_comp.currentText())
        data.append(self.number.text())
        data.append(self.date.text())
        data.append(self.my_object.toPlainText())
        data.append(self.work.toPlainText())
        data.append(self.part.text())
        return data

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.my_object.toPlainText(), self.work.toPlainText(),
                      self.part.text()]) or self.date.text() == zero:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True