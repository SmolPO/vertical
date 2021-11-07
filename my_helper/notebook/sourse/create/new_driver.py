from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *

# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_driver")
fields = ["family", "name", "surname", "birthday", "passport", "id"]


class NewDriver(TempForm):
    def __init__(self, parent=None):
        super(NewDriver, self).__init__(designer_file, parent, "drivers")
        if not self.status_:
            return
        try:
            self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        except:
            mes.question(self, "Внимание", my_errors["5_init_list"], mes.Cancel)
            return
        self.list_ui = [self.family, self.name, self.surname, self.d_birthday, self.passport, self.adr]

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        for item in self.list_ui:
            item.setValidator(symbols)

    def _select(self, text):
        return True