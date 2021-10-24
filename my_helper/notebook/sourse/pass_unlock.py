from pass_template import TempPass
import datetime as dt
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.new_template import from_str
#  сделать мессаджбоксы на Сохранить
from database import DataBase, get_path, get_path_ui
designer_file = get_path_ui("pass_unlock")
count_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class UnlockPass(TempPass):
    def __init__(self, parent):
        super(UnlockPass, self).__init__(designer_file, parent, "workers")
        # pass
        self.d_from.setDate(dt.datetime.now().date())
        self.d_to.setDate(Date(*from_str(".".join([str(count_days[dt.datetime.now().month + 1]),
                                                   str(dt.datetime.now().month),
                                                   str(dt.datetime.now().year)]))))
        self.cb_all_days.stateChanged.connect(self.all_days)
        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}
        self.main_file += "/pass_unlock.docx"
        self.count_days = 14

    def init_workers(self):
        self.cb_worker.addItem("(нет)")
        for name in self.parent.db.get_data("family, name, id", self.table):
            self.cb_worker.addItem(name[-1] + ". " + " ".join((name[0], name[1][0])) + ".")

    def _get_data(self):
        family = self.cb_worker.currentText().split(".")[0]
        # self.count_days = Date(*from_str(self.d_from.text())) - dt.timedelta(days=self.sb_days.value())
        for row in self.parent.db.get_data("family, name, surname, post, live_adr, id", self.table):
            if family == str(row[-1]):  # на форме фамилия в виде Фамилия И.
                self.data["family"] = row[0]
                self.data["name"] = row[1]
                self.data["surname"] = row[2]
                self.data["post"] = row[3]
                self.data["adr"] = row[4]
                self.data["start_date"] = self.d_from.text()
                self.data["end_date"] = self.d_to.text()

    def check_input(self):
        return True

    def _create_data(self, doc):
        return True

    def _ev_ok(self):
        return True

    def all_days(self, state):
        self.sb_days.setEnabled(not state)
        self.sb_days.setValue(14)
        self.count_days = 14
        pass