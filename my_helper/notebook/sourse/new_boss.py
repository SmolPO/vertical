from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.inserts import get_from_db
from my_helper.notebook.sourse.new_template import TempForm, from_str
from database import DataBase, get_path, get_path_ui
import logging
logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_boss")
fields = ["family", "name", "surname", "post", "email", "phone", "id"]


class NewBoss(TempForm):
    def __init__(self, parent):
        super(NewBoss, self).__init__(designer_file)
        self.parent = parent
        self.table = "bosses"
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        self.slice_select = -5
        self.slice_set = 6
        self.slice_get = 6
        self.slice_clean = 6
        self.list_ui = list([self.family, self.name, self.surname, self.post, self.email, self.phone, self.cb_sex])
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))

        for item in self.list_ui[0:4]:
            item.setValidator(symbols)
        self.phone.setValidator(QREVal(QRE("[0-9]{11}")))
        self.email.QREVal(QRE("[a-zA-Z ._@ 0-9]{30}"))

    def _set_data(self, data):
        self.cb_sex.setCurrentIndex(0) if data[6] == "М" else self.cb_sex.setCurrentIndex(1)

    def _get_data(self, data):
        data.append(self.cb_sex.currentText())
        return data

    def check_input(self):
        if "" in list([self.family.text(),
                       self.name.text(),
                       self.surname.text(),
                       self.post.text()]):
            return False
        return True

    def _clean_data(self):
        return True

    def _ev_select(self, text):
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True