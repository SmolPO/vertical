from PyQt5 import uic
from PyQt5.QtCore import Qt
import datetime as dt
import os
import docxtpl
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.my_pass.pass_template import TempPass
from my_helper.notebook.sourse.database import get_path, get_path_ui, get_config, empty, count_days, my_errors
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("pass_auto")


class AutoPass(TempPass):
    def __init__(self, parent):
        super(AutoPass, self).__init__(designer_file, parent, "auto")
        uic.loadUi(designer_file, self)
        # my_pass
        self.b_open.clicked.connect(self.my_open_file)
        self.b_clean.clicked.connect(self.clean_data)
        self.add_auto.clicked.connect(self.next_auto)
        self.cb_drivers.activated[str].connect(self.driver_changed)
        self.cb_activ.stateChanged.connect(self.manual_set)

        self.data = {"number": "", "date": "", "start_date": "", "end_date": "",
                     "auto": list(), "gov_numbers": list(), "people": list(list())}

        self.init_auto()
        self.init_drivers()
        self.list_ui = list([self.driver_1, self.driver_2, self.driver_3, self.driver_4,
                             self.driver_5, self.driver_6, self.driver_7])
        self.count = 0
        try:
            self.main_file = get_path("path") + get_path("path_pat_notes") + "/pass_auto.docx"
            self.print_file = get_path("path") + get_path("path_notes_docs")
        except:
            mes.question(self, "Внимание", my_errors["2_get_path"], mes.Cancel)
            return

    # инициализация
    def init_drivers(self):
        try:
            drivers = self.parent.db.get_data("family, name", self.table)
        except:
            mes.question(self, "Внимание", my_errors["2_get_path"], mes.Cancel)
            return False
        for item in self.list_ui:
            item.addItem(empty)
        for row in drivers:
            for item in self.list_ui:
                item.addItem(" ".join((row[0], row[1][0] + ".")))
                item.activated[str].connect(self.new_driver)

    def init_auto(self):
        auto = list()
        try:
            auto = self.parent.db.get_data("model, gov_number", "auto")
        except:
            mes.question(self, "Внимание", my_errors["2_get_path"], mes.Cancel)
            return False
        auto.append([empty])
        for row in auto:
            self.cb_auto.addItem(row[0])

    # для заполнения текста
    def get_data(self):
        try:
            rows = self.parent.db.get_data("*", "auto")
        except:
            mes.question(self, "Внимание", my_errors["2_get_path"], mes.Cancel)
            return False
        for row in rows:
            if self.cb_auto.currentText() in row:
                self.data["auto"].append(" ".join(row[:2]))
                self.data["gov_number"].append(row[2])
        for row in self.parent.db.get_data("family, name, surname, birthday, passport", "drivers"):
            for item in self.list_ui:
                if item.currentText()[:-3] in row:
                    self.data["people"][self.count].append(" ".join(row))

        self.data["number"] = "Исх. № " + self.number.text()
        self.data["date"] = "от. " + self.d_note.text()
        if "" in self.data:
            return False
        return True

    # обработчики кнопок
    def ev_ok(self):
        if not self.get_data():
            return
        try:
            doc = docxtpl.DocxTemplate(self.main_file)
        except:
            mes.question(self, "Внимание", my_errors["4_not_file"] + self.main_file, mes.Cancel)
            return False
        doc.render(self.data)
        try:
            doc.save(self.print_file)
        except:
            mes.question(self, "Внимание", my_errors["4_not_file"] + self.print_file, mes.Cancel)
            return False
        try:
            os.startfile(self.print_file)
        except:
            mes.question(self, "Внимание", my_errors["4_not_file"] + self.print_file, mes.Cancel)
            return False

    def _set_enabled(self, status):
        self.d_note.setEnabled(status)
        self.number.setEnabled(status)
        self.cb_month.setEnabled(status)
        self.d_from.setEnabled(status)
        self.d_to.setEnabled(status)

    def next_auto(self):
        self.get_date()
        self.my_setEnabled(False)
        self.list_auto.append(self.cb_auto.currentText())

    def kill_last_auto(self):
        self.date["auto"].pop()
        self.data["people"].pop()
        self.list_auto.pop()
        if len(self.date["auto"]) == 1:
            self._set_enabled(True)

    def clean_data(self):
        self.data = {"number": "", "date": "", "start_date": "", "end_date": "",
                     "auto": list(), "gov_numbers": list(), "people": list(list())}
        self.list_auto.clear()

    def ev_cancel(self):
        self.close()

    def my_open_file(self):
        pass

    def manual_set(self, state):
        if state == Qt.Checked:
            self.cb_mounth.setEnabled(False)
            self.d_from.setEnabled(True)
            self.d_to.setEnabled(True)
        else:
            self.cb_mounth.setEnabled(True)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)

    def new_worker(self):
        flag = True
        for item in self.list_ui:
            if item.currentText() != empty:
                item.setEnabled(True)
            else:
                item.setEnabled(flag)
                flag = False

    def get_dates(self):
        if not self.cb_chouse.isChecked():
            month = self.list_month.index(self.cb_month.currentText()) + 1
            if month == 13:
                day, month, year = get_config("new_year"), "01", str(dt.datetime.now().year + 1)  # работаем с 9 января
            else:
                day, month, year = "01", str(month), str(dt.datetime.now().year)
                if int(month) < 10:
                    month = "0" + month
            end_month = str(count_days[12]) if int(year) / 4 == 0 else str(count_days[int(month)])
            self.data["start_date"] = ".".join((day, month, year))
            self.data["end_date"] = ".".join((end_month, month, year))
        else:
            self.data["start_date"] = self.d_from.text()
            self.data["end_date"] = self.d_to.text()

    def check_input(self):
        return True
