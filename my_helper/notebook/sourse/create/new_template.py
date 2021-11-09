from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import my_helper.notebook.sourse.inserts as ins
from datetime import datetime as dt
import openpyxl
import os
from my_helper.notebook.sourse.database import *


class TempForm (QDialog):
    def __init__(self, ui_file, parent, table):
        super(TempForm, self).__init__()
        self.status_ = True
        self.conf = Ini(self)
        self.path_ = ui_file
        if self.check_start(ui_file) == ERR:
            return
        self.parent = parent
        self.table = table
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.close)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)
        self.but_status("add")

        self.rows_from_db = self.parent.db.get_data("*", self.table)
        if self.rows_from_db == ERR:
            return
        self.current_id = int(self.rows_from_db[-1][-1]) + 1
        self.vac = False
        self.bill = False

    def check_start(self, ui_file):
        try:
            uic.loadUi(ui_file, self)
            return True
        except:
            return msg_er(self, LOAD_UI)

    def check_input(self):
        data = set(self.get_data())
        if data == ERR:
            return
        empty = {"", ZERO, NOT}
        if data.intersection(empty):
            msg_info(self, FULL_ALL)
            return
        if self.vac:
            if not self.check_vac():
                msg_info(self, CHECK_COVID)
                return False
        return True

    def ev_ok(self):
        if not self.check_input() or self.check_input() == ERR:
            return False
        data = self.get_data()
        if not data:
            return
        if self.parent.db.my_commit(ins.add_to_db(data, self.table)) == ERR:
            return
        if self.bill:
            if self.create_bill(data) == ERR:
                return
        self.close()

    def ev_select(self, text):
        self._select(text)
        if text == empty:
            self.clean_data()
            self.but_status("add")
            self.current_id = int(self.rows_from_db[-1][-1]) + 1
            return
        else:
            self.but_status("change")
        for row in self.rows_from_db:
            if str(text.split(". ")[0]) == str(row[-1]):
                self.set_data(row)

    def set_data(self, data):
        k = 0
        for item in self.list_ui:
            if "QLineEdit" in str(type(item)):
                item.setText(data[k])
            if "QLabel" in str(type(item)):
                item.setText(data[k])
            if "QTextEdit" in str(type(item)):
                item.clear()
                item.append(data[k])
            if "QDateEdit" in str(type(item)):
                item.setDate(from_str(data[k]))
            if "QComboBox" in str(type(item)):
                ind = item.findText(data[k])
                if ind == -1:
                    ind = get_index(item, data[k])
                item.setCurrentIndex(ind)
            if "QSpinBox" in str(type(item)):
                item.setValue(int(data[k]))
            if "QCheckBox" in str(type(item)):
                item.setChecked(True) if data[k] == YES else item.setChecked(False)
            k = k + 1
        if self.vac:
            if self.set_vac_data(data[-3]) == ERR:
                return
        self.current_id = data[-1]

    def get_data(self):
        data = list()
        val = ""
        for item in self.list_ui:
            if "QLineEdit" in str(type(item)):
                val = item.text()
            elif "QLabel" in str(type(item)):
                val = item.text()
            elif "QTextEdit" in str(type(item)):
                val = item.toPlainText()
            elif "QDateEdit" in str(type(item)):
                val = item.text()
            elif "QComboBox" in str(type(item)):
                if item.currentText().split(". ")[0].isdigit():
                    val = "".join(item.currentText().split(". ")[1:])
            elif "QSpinBox" in str(type(item)):
                val = str(item.value())
            elif "QCheckBox" in str(type(item)):
                val = YES if item.isChecked() else NO
            elif "str" in str(type(item)):
                val = item
            else:
                return False
            data.append(val)
        if not data:
            return False
        data.append(str(self.current_id))
        return data

    def clean_data(self):
        for item in self.list_ui:
            if "QLineEdit" in str(type(item)):
                item.setText("")
            if "QLabel" in str(type(item)):
                item.setText("")
            if "QTextEdit" in str(type(item)):
                item.clear()
            if "QDateEdit" in str(type(item)):
                item.setDate(zero)
            if "QComboBox" in str(type(item)):
                item.setCurrentIndex(0)
            if "QCheckBox" in str(type(item)):
                item.setChecked(False)
            if "QSpinBox" in str(type(item)):
                item.setValue(0)
            if "str" in str(type(item)):
                item = ""

    def ev_change(self):
        data = self.get_data()
        if not data:
            return
        answer = msg_q(self, CHANGE_NOTE + str(data) + "?")
        if answer == mes.OK:
            data[-1] = str(self.current_id)
            if self.parent.db.my_update(data, self.table) == ERR:
                return
            answer = msg_q(self, CHANGED_NOTE)
            if answer == mes.Ok:
                self.close()

    def ev_kill(self):
        data = self.get_data()
        if not data:
            return
        answer = msg_q(self, KILL_NOTE + str(data) + "?")
        if answer == mes.Ok:
            if self.parent.db.kill_value(self.current_id, self.table) == ERR:
                return
            answer = msg_q(self, KILLD_NOTE)
            if answer == mes.Ok:
                self.close()

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)

    def change_vac(self):
        issue_type = 2
        sputnik_V = 0
        self.place.setEnabled(self.cb_vac.currentIndex() != issue_type)
        self.my_mem = self.place.toPlainText() if self.cb_vac.currentIndex() == issue_type else self.my_mem
        self.place.clear()
        self.place.append(NO if self.cb_vac.currentIndex() == issue_type else self.my_mem)
        self.d_vac_2.setEnabled(True if self.cb_vac.currentIndex() == sputnik_V else False)

    def set_vac_data(self, vac):
        list_vac = [self.d_vac_1, self.d_vac_2, self.place, self.vac_doc]
        if vac == SPUTNIK:
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(True)
            list_vac[2].setEnabled(True)
            list_vac[3].setEnabled(True)
        if vac == SP_LITE:
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(False)
            list_vac[2].setEnabled(True)
            list_vac[3].setEnabled(True)
        if vac == COVID:
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(False)
            list_vac[2].setEnabled(False)
            list_vac[3].setEnabled(True)

    def check_vac(self):
        list_vac = [self.d_vac_1.text(), self.d_vac_2.text(), self.place.toPlainText(),
                    self.vac_doc.text(), self.cb_vac.currentIndex()]
        m_val = {"year": 6, "type": -1, "SputnikV": 0, "Lite": 1, "issue": 2, "d_vac_1": 0, "d_vac_2": 1,
                 "min_len": 3, "place": 2, "doc": 3}  # магические переменные
        vac_safe = int(self.conf.get_config("vac_safe"))
        vac_do = int(self.conf.get_config("vac_do"))
        vac_days = int(self.conf.get_config("vac_days"))
        cv_safe = int(self.conf.get_config("cv_safe"))
        if vac_safe == ERR or vac_do == ERR or vac_days == ERR or cv_safe == ERR:
            return ERR

        if list_vac[m_val["type"]] == m_val["SputnikV"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                msg_info(self, PLACE_VAC)
                return False

            if time_delta("now", list_vac[m_val["d_vac_2"]]) > vac_safe:
                msg_info(self, OLD_DOC.format(str(vac_safe)))
                return False

            delta = time_delta(list_vac[m_val["d_vac_2"]], list_vac[m_val["d_vac_1"]])

            if delta < vac_days:
                msg_info(self, ERR_VAC_MANY.format(str(delta), str(vac_days)))
                return False

            if delta > vac_do:
                msg_info(self, ERR_VAC_MACH.format(str(delta), str(vac_days)))
                return False

        elif list_vac[m_val["type"]] == m_val["Lite"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                msg_info(self, PLACE_VAC)
                return False

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > vac_safe:
                msg_info(self, OLD_DOC.format(str(vac_safe)))
                return False

        elif list_vac[m_val["type"]] == m_val["issue"]:

            if len(list_vac[m_val["doc"]]) < m_val["min_len"]:
                msg_info(self, NUMBER_DOC)
                return False

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > cv_safe:
                msg_info(self, OLD_DOC.format(str(cv_safe)))
                return False

        return True

    def create_bill(self, data):
        path_1 = self.conf.get_path("path")
        path_2 = self.conf.get_path("path_bills")
        if path_1 == ERR or path_2 == ERR:
            return ERR
        path = path_1 + path_2 + "/" + str(str(dt.datetime.now())[:10].replace("-", ".") + "_" +
                                           str(self.current_id + 1) + ".pdf")
        try:
            os.replace(self.filename, path)
        except:
            return msg_er(self, PERMISSION_ERR + path)
        if self.create_report(self.sb_value.value(),
                              self.date.text().replace("-", "."),
                              self.cb_buyer.currentText()[:-5]) == ERR:
            return ERR
        return data

    def create_report(self, value, date, people):
        path_1 = self.conf.get_path("path")
        path_2 = self.conf.get_path("path_bills")
        if path_1 == ERR or path_2 == ERR:
            return ERR
        path = path_1 + path_2 + "/" + str(dt.datetime.now().year) + \
                                  "/" + str(dt.datetime.now().month) + \
                                  "/" + str(dt.datetime.now().month) + str(dt.datetime.now().year) + ".xlsx"
        try:
            wb = openpyxl.load_workbook(path)
        except:
            return msg_er(self, GET_FILE + path)
        try:
            sheet = wb['bills']
        except:
            return msg_er(self, GET_PAGE + 'bills')
        row = sheet['F2'].value
        sheet['A' + str(row + 3)].value = int(row) + 1
        sheet['B' + str(row + 3)].value = date
        sheet['C' + str(row + 3)].value = value
        sheet['D' + str(row + 3)].value = people
        sheet['F2'].value = int(row) + 1
        try:
            wb.save(path)
            os.startfile(path)
        except:
            return msg_er(self, GET_FILE + path)


def set_cb_text(combobox, data, rows):
    i = iter(range(1000))
    for item in rows:
        if item[2] == data:
            combobox.setCurrentIndex(next(i) + 1)
            return
        next(i)
