from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *

designer_file = get_path_ui("new_boss")
fields = ["family", "name", "surname", "post", "email", "phone", "id"]


class NewBoss(TempForm):
    def __init__(self, parent):
        super(NewBoss, self).__init__(designer_file, parent, "bosses")
        if not self.status_:
            return
        try:
            self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.list_ui = list([self.family, self.name, self.surname, self.post, self.email, self.phone, self.cb_sex])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))

        for item in self.list_ui[0:4]:
            item.setValidator(symbols)
        self.phone.setValidator(QREVal(QRE("[0-9]{11}")))
        self.email.QREVal(QRE("[a-zA-Z ._@ 0-9]{30}"))

    def _set_data(self, data):
        self.cb_sex.setCurrentIndex(0) if data[6] == "М" else self.cb_sex.setCurrentIndex(1)

    def _select(self, data):
        return True