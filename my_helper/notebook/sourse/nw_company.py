from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.new_template import TempForm, from_str
from database import DataBase, get_path, get_path_ui
import logging
logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("add_company")
fields = ["company", "adr", "ogrn", "inn", "kpp", "bik", "korbill", "rbill", "bank", "family", "name", "surname",
          "post", "count_attorney", "date_attorney", "id"]
zero = "01.01.2000"


class NewCompany(TempForm):
    def __init__(self, parent=None):
        super(NewCompany, self).__init__(designer_file)
        self.parent = parent
        self.table = "company"
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.init_mask()
        self.list_ui = [self.company, self.ogrn, self.inn, self.kpp, self.adr,
                        self.bik, self.korbill, self.rbill, self.bank, self.family,
                        self.name, self.surname, self.post, self.count_dovr, self.date_dovr]
        self.slice_set = len(self.list_ui) - 1
        self.slice_get = len(self.list_ui)
        self.slice_clean = len(self.list_ui) - 1
        self.slice_select = len(self.list_ui) - 1
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))
        number_prot = QREVal(QRE("[А-Яа-я /- 0-9]{10}"))
        self.ogrn.setValidator(QREVal(QRE("[0-9]{14}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{10}")))
        self.kpp.setValidator(QREVal(QRE("[0-9]{9}")))
        self.bik.setValidator(QREVal(QRE("[0-9]{8}")))
        self.korbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.rbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.bank.setValidator(number_prot)
        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(QREVal(QRE("[а-яА-Я -]{30}")))
        self.count_dovr.setValidator(number_prot)

    def _ev_select(self, text):
        return True

    def _set_data(self, data):
        print(data[-2])
        print(from_str(data[-2]))
        self.date_dovr.setDate(Date(*from_str(data[-2])))
        self.current_id = data[fields.index("id")]

    def _clean_data(self):
        for item in self.list_ui[:-1]:
                item.setText("")
        self.list_ui[-1].setDate(Date.fromString(zero))
        return False

    def _get_data(self, data):
        return data

    def _but_status(self, status):
        return True

    def check_input(self):
        data = self.get_data()
        if "" in data:
            mes.question(self, "Сообщение", "Заполните все поля", mes.Cancel)
            return False
        else:
            if self.list_ui[-2].text() == zero:
                ans = mes.question(self, "Сообщение", "Дата доверенности точно " + zero + "?", mes.Ok | mes.Cancel)
                if ans == mes.Ok:
                    return True
                else:
                    return False
            else:
                return True

    def _ev_ok(self):
        return True