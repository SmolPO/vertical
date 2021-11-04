from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
import os
import docxtpl
from my_helper.notebook.sourse.database import *
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
#  сделать мессаджбоксы на Сохранить


class TempPass(QDialog):
    def __init__(self, designer_file, parent, table):
        super(TempPass, self).__init__()
        self.parent = parent
        if not self.check_start(designer_file):
            return
        self.table = table
        # my_pass
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.close)
        self.b_open.clicked.connect(self.my_open_file)
        # self.b_save.clicked.connect(self.save_pattern)
        # self.b_kill.clicked.connect(self.kill_pattern)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(get_next_number())

        self.list_month = ["январь", "февраль", "март", "апрель",
                           "май", "июнь", "июль", "август", "сентябрь",
                           "октябрь", "ноябрь", "декабрь"]
        self.data = dict()
        try:
            self.main_file = get_path("path") + get_path("path_pat_notes")
            self.print_folder = get_path("path") + get_path("path_notes_docs")
        except:
            msg(self, my_errors["2_get_ini"])
            return
        fields = "family, name, surname, post, passport, passport_got, birthday, adr,  live_adr"
        self.people_all = self.parent.db.get_data(fields, "workers") + self.parent.db.get_data(fields, "itrs")
        self.people_mark = list()
        fields = "family, name, surname, post, passport, passport_got, " \
                 "birthday, adr,  live_adr, d_vac_1, d_vac_2, place, vac_doc, id"
        rows_w = self.parent.db.get_data(fields, "workers")
        rows_i = self.parent.db.get_data(fields, "itrs")
        self.all_people = rows_w + rows_i

    def check_start(self, designer_file):
        self.status_ = True
        self.path_ = designer_file
        print(designer_file)
        try:
            uic.loadUi(designer_file, self)
            return True
        except:
            self.status_ = False
            return msg(self, my_errors["1_get_ui"])

    # флаг на выбор всех
    def set_dates(self, state):
        self.d_to.setEnabled(state == Qt.Checked)
        self.d_from.setEnabled(state == Qt.Checked)
        self.cb_month.setEnabled(state != Qt.Checked)

    # обработчики кнопок
    def ev_ok(self):
        if not self._ev_ok():
            return False
        self._get_data()
        self.data["number"] = "Исх. № " + self.number.text()
        self.data["date"] = "от. " + self.d_note.text()
        self.data["customer"] = self.parent.customer
        self.data["company"] = self.parent.company
        if not self.check_input():
            return False
        print_file = self.print_folder + "/" + self.number.text() + "_" + self.d_note.text() + ".docx"

        path = self.main_file
        doc = docxtpl.DocxTemplate(path)
        doc.render(self.data)
        path = print_file
        doc.save(path)
        self._create_data(path)
        set_next_number(int(self.number.text()) + 1)
        self.close()
        os.startfile(path)

    def new_worker(self):
        flag = True
        for item in self.list_ui:
            if item.currentText() != "(нет)":
                item.setEnabled(True)
            else:
                item.setEnabled(flag)
                flag = False
        pass

    def my_open_file(self):
        try:
            os.startfile(self.print_file)
        except:
            return msg(self, my_errors["4_get_file"] + self.print_file)

    def save_pattern(self):
        pass

    def kill_pattern(self):
        pass

    def get_contract(self, name):
        # получить номер договора по короткому имени
        try:
            rows = self.parent.db.get_data("number, date, object, place, type_work, name", "contracts")
        except:
            return msg(self, my_errors["3_get_db"])
        for row in rows:
            if name in row:
                self.data["contract"] = " от ".join(row[:2])
                self.data["object_name"] = row[2]
                self.data["part"] = row[3]
                self.data["type_work"] = row[4]

    def get_worker(self, family):
        try:
            rows = self.parent.db.get_data("family, name, surname, post, passport, "
                                       "passport_got, birthday, adr,  live_adr, id", "workers")
        except:
            return msg(self, my_errors["3_get_db"])
        if family == "all":
            return rows
        for row in rows:
            if family[:-5] == row[0]:  # на форме фамилия в виде Фамилия И.О.
                return row

    def get_worker_week(self, family):
        # получить номер договора по короткому имени
        try:
            rows = self.parent.db.get_data("family, name, surname, post, passport, passport_got, "
                                           "birthday, adr,  live_adr", "workers")
        except:
            return msg(self, my_errors["3_get_db"])
        for row in rows:
            if family[:-5] == row[0]:
                return row
            return row

    def get_week_days(self):
        if self.cb_other.isChecked():
            self.data["week_day"] = "в выходные дни с " + self.d_from.text() + " до " + self.d_to.text()
        else:
            if len(self.get_days()) > 1:
                self.data["week_day"] = "в выходные дни с " + str(self.get_days()[0]) + " до " + str(self.get_days()[1])
            else:
                self.data["week_day"] = "в выходной день " + str(self.get_days()[0])

    def other_days(self, state):
        if state == Qt.Checked:
            self.cb_sun.setEnabled(False)
            self.cb_sub.setEnabled(False)
            self.d_from.setEnabled(True)
            self.d_to.setEnabled(True)
        else:
            self.cb_sun.setEnabled(True)
            self.cb_sub.setEnabled(True)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)

    def week_days(self, state):
        if state == Qt.Checked:
            self.cb_other.setEnabled(False)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)
        elif not self.cb_sun.isChecked() and not self.cb_sub.isChecked():
            self.cb_other.setEnabled(True)

    def get_end_month(self):
        next_month = dt.datetime.now().month
        # если конец года: увеличить год и месяц в 1
        next_day = count_days[next_month]
        next_month = str(next_month)
        if int(next_month) < 10:
            next_month = "0" + next_month
        next_year = str(dt.datetime.now().year)

        if int(next_year) / 4 == 0:
            end_next_month = str(count_days[12])
        else:
            end_next_month = str(count_days[int(next_month)])
        print(".".join((end_next_month, next_month, next_year)))
        return (end_next_month, next_month, next_year)

    def check_row(self, row):
        my_id = int(row.split(".")[0])
        family = row.split(".")[1][1:-2]
        s_name = row.split(".")[1][-1]
        s_sur = row.split(".")[2]
        for item in self.all_people:
            if str(my_id) == str(item[-1]):
                if family == item[0]:
                    if s_name == item[1][0]:
                        if s_sur == item[2][0]:
                            return item