from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.create.new_template import TempForm, from_str
from my_helper.notebook.sourse.database import get_path_ui, zero

# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_driver")
fields = ["family", "name", "surname", "birthday", "passport", "id"]


class NewDriver(TempForm):
    def __init__(self, parent=None):
        super(NewDriver, self).__init__(designer_file)
        self.parent = parent
        self.table = "drivers"
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        self.list_ui = [self.family, self.name, self.surname, self.d_birthday, self.passport, self.adr, ]
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
        return True

    def _set_data(self, data):
        print(data)
        self.passport.clear()
        self.adr.clear()
        self.passport.append(data[4])
        self.adr.append(data[5])
        self.d_birthday.setDate(Date(*from_str(data[3])))

    def _get_data(self, data):
        data.append(self.d_birthday.text())
        data.append(self.passport.toPlainText())
        data.append(self.adr.toPlainText())
        return data

    def _clean_data(self):
        for item in self.list_ui[:-1]:
            try:
                item.setText("")
            except:
                item.clear()
        return False

    def check_input(self):
        data = self.get_data()
        if "" in data:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        else:
            if self.d_birthday.text() == zero:
                ans = mes.question(self, "Сообщение", "Дата рождения точно " + zero + "?", mes.Ok | mes.Cancel)
                if ans == mes.Ok:
                    return True
                else:
                    return False
            else:
                return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True