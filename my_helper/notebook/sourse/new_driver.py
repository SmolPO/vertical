from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.template import TempForm
designer_file = '../designer_ui/new_driver.ui'
fields = ["family", "name", "surname", "birthday", "passport", "id"]


class NewDriver(TempForm):
    def __init__(self, parent=None):
        super(NewDriver, self).__init__(designer_file)
        self.parent = parent
        self.table = "drivers"
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        self.list_ui = [self.family, self.name, self.surname, self.passport, self.adr, self.d_birthday]
        self.slice_set = 3
        self.slice_get = 3
        self.slice_clean = len(self.list_ui)
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        for item in self.list_ui:
            item.setValidator(symbols)

    def _ev_select(self, text):
        family = text[:-5]
        print(family)
        for row in self.rows_from_db:
            if family in row:
                self.set_data(row)
        return False

    def _set_data(self, data):
        self.passport.clear()
        self.adr.clear()
        self.passport.append(data[3])
        self.adr.append(data[4])
        self.d_birthday.setDate(Date.fromString(data[5]))

    def _get_data(self, data):
        data.append(self.passport.toPlainText())
        data.append(self.adr.toPlainText())
        data.append(self.d_birthday.text())
        return data

    def _clean_data(self):
        for item in self.list_ui[:-1]:
            try:
                item.setText("")
            except:
                item.clear()
        return False

    def check_input(self):
        if "" in self.list_ui[:5]:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        else:
            if self.d_birthday.text() == "01.01.2000":
                ans = mes.question(self, "Сообщение", "Дата рождения точно 01.01.2000?", mes.Ok | mes.Cancel)
                if ans == mes.Ok:
                    return True
                else:
                    return False
            else:
                return True
    def _ev_ok(self):
        return

    def _but_status(self, status):
        return True