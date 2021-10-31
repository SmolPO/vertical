from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
import os
import docxtpl
from configparser import ConfigParser
from my_helper.notebook.sourse.database import get_path, count_days
import logging
# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
#  сделать мессаджбоксы на Сохранить


class TempPass(QDialog):
    def __init__(self, designer_file, parent, table):
        super(TempPass, self).__init__()
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.table = table
        # my_pass
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_open.clicked.connect(self.my_open_file)
        # self.b_save.clicked.connect(self.save_pattern)
        # self.b_kill.clicked.connect(self.kill_pattern)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(get_next_number())

        self.list_month = ["январь", "февраль", "март", "апрель",
                           "май", "июнь", "июль", "август", "сентябрь",
                           "октябрь", "ноябрь", "декабрь"]
        self.data = dict()
        self.main_file = get_path("path") + get_path("path_pat_notes")
        self.print_folder = get_path("path") + get_path("path_notes_docs")

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
        try:
            doc = docxtpl.DocxTemplate(self.main_file)
        except:
            mes.question(self, "Сообщение", "Файл не найден" + self.main_file, mes.Cancel)
            return
        doc.render(self.data)
        doc.save(print_file)
        self._create_data(print_file)
        set_next_number(int(self.number.text()) + 1)
        self.close()
        os.startfile(print_file)

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
        os.startfile(self.print_file)

    def save_pattern(self):
        pass

    def kill_pattern(self):
        pass

    def get_contract(self, name):
        # получить номер договора по короткому имени
        for row in self.parent.db.get_data("number, date, object, place, type_work, name", "contracts"):
            if name in row:
                self.data["contract"] = " от ".join(row[:2])
                self.data["object_name"] = row[2]
                self.data["part"] = row[3]
                self.data["type_work"] = row[4]

    def get_worker(self, family):
        rows = self.parent.db.get_data("family, name, surname, post, passport, "
                                       "passport_got, birthday, adr,  live_adr", "workers")
        if family == "all":
            return rows
        for row in rows:
            if family[:-5] == row[0]:  # на форме фамилия в виде Фамилия И.О.
                return row

    def get_worker_week(self, family):
        # получить номер договора по короткому имени
        for row in self.parent.db.get_data("family, name, surname, post, passport, passport_got, "
                                           "birthday, adr,  live_adr", "workers"):
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

    def ev_cancel(self):
        self.close()

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


path_conf = "B:/my_config.ini"


def get_next_number():
    config = ConfigParser()
    config.read(path_conf)
    number_note = config.get('config', 'number')
    next_number = int(number_note) + 1
    return int(number_note)


def set_next_number(n):
    config = ConfigParser()
    config.read(path_conf)
    number_note = config.get('config', 'number')
    next_number = n
    config.set("config", 'number', str(next_number))
    with open(path_conf, 'w') as configfile:
        config.write(configfile)
    return int(number_note)


