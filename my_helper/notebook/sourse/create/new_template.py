from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import my_helper.notebook.sourse.inserts as ins
from PyQt5.QtWidgets import QMessageBox as mes
import logging
from my_helper.notebook.sourse.database import *


class TempForm (QDialog):
    def __init__(self, designer_file, parent, table):
        super(TempForm, self).__init__()
        if not self.check_start(designer_file):
            return
        self.parent = parent
        self.table = table
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.close)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)
        self.but_status("add")
        self.parent.db.execute("UPDATE itrs SET id = '1' where status = '1'")
        # self.parent.db.execute("UPDATE workers SET d_vac_2 = '25.02.2000' where id = '1'")
        self.parent.db.conn.commit()

        self.rows_from_db = self.parent.db.get_data("*", self.table)
        self.current_id = int(self.rows_from_db[-1][-1]) + 1
        self.vac = False

    def check_start(self, ui_file):
        self.status_ = True
        self.path_ = ui_file
        try:
            uic.loadUi(ui_file, self)
            return True
        except:
            return msg(self, my_errors["1_get_ui"])

    def check_input(self):
        data = set(self.get_data())
        empty = {"", "01.01.2000", "(нет)"}
        if data.intersection(empty):
            return msg(self, "Заполните все поля")
        if self.vac:
            if not self.check_vac():
                return False
        return True

    def ev_ok(self):
        if not self.check_input():
            return False
        data = self.get_data()
        if not data:
            return
        self.parent.db.my_commit(ins.add_to_db(data, self.table))
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
            if text.split(". ")[0] == str(row[-1]):
                self.set_data(row)

    def set_data(self, data):
        k = 0
        print(data)
        for item in self.list_ui:
            print(k, data[k])
            print(type(item))
            if "QLineEdit" in str(type(item)):
                item.setText(data[k])
            if "QTextEdit" in str(type(item)):
                item.clear()
                item.append(data[k])
            if "QDateEdit" in str(type(item)):
                print(from_str(data[k]))
                item.setDate(from_str(data[k]))
            if "QComboBox" in str(type(item)):
                ind = item.findText(data[k])
                if ind == -1:
                    ind = item.findText(data[-1] + ". " + str(data[k]))
                item.setCurrentIndex(ind)
            if "QSpinBox" in str(type(item)):
                item.setValue(int(data[k]))
            if "QCheckBox" in str(type(item)):
                item.setChecked(True) if data[k] == "да" else item.setChecked(False)
            k = k + 1
        if self.vac:
            self.set_vac_data(data[-3])
        self.current_id = data[-1]

    def get_data(self):
        data = list()
        for item in self.list_ui:
            if "QLineEdit" in str(type(item)):
                val = item.text()
            if "QTextEdit" in str(type(item)):
                val = item.toPlainText()
            if "QDateEdit" in str(type(item)):
                val = item.text()
            if "QComboBox" in str(type(item)):
                val = item.currentText()
            if "QSpinBox" in str(type(item)):
                val = str(item.value())
            if "QCheckBox" in str(type(item)):
                val = "да" if item.isChecked() else "нет"
            data.append(val)
        if not data:
            return False
        data.append(str(self.current_id))
        return data

    def clean_data(self):
        for item in self.list_ui:
            if "QLineEdit" in str(type(item)):
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

    def ev_change(self):
        answer = mes.question(self, "Изменение записи", "Вы действительно хотите изменить запись на " +
                              str(self.get_data()) + "?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            data = self.get_data()
            data[-1] = str(self.current_id)
            self.parent.db.my_update(data, self.table)
            answer = mes.question(self, "Сообщение", "Запись изменена", mes.Ok)
            if answer == mes.Ok:
                self.close()

    def ev_kill(self):
        answer = mes.question(self, "Удаление записи", "Вы действительно хотите удалить запись " +
                                      str(self.get_data()) + "?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            self.parent.db.kill_value(self.current_id, self.table)
            answer = mes.question(self, "Сообщение", "Запись удалена", mes.Ok)
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
        self.place.append("нет" if self.cb_vac.currentIndex() == issue_type else self.my_mem)
        self.d_vac_2.setEnabled(True if self.cb_vac.currentIndex() == sputnik_V else False)

    def set_vac_data(self, vac):
        list_vac = [self.d_vac_1, self.d_vac_2, self.place, self.vac_doc]
        if vac == "2 дозы":
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(True)
            list_vac[2].setEnabled(True)
            list_vac[3].setEnabled(True)
        if vac == "1 дозы":
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(False)
            list_vac[2].setEnabled(True)
            list_vac[3].setEnabled(True)
        if vac == "Болел":
            list_vac[0].setEnabled(True)
            list_vac[1].setEnabled(False)
            list_vac[2].setEnabled(False)
            list_vac[3].setEnabled(True)

    def check_vac(self):
        list_vac = [self.d_vac_1.text(), self.d_vac_2.text(), self.place.toPlainText(),
                    self.vac_doc.text(), self.cb_vac.currentIndex()]
        m_val = {"year": 6, "type": -1, "SputnikV": 0, "Lite": 1, "issue": 2, "d_vac_1": 0, "d_vac_2": 1,
                 "min_len": 3, "place": 2, "doc": 3}  # магические переменные
        try:
            vac_safe = int(get_config("vac_safe"))
            vac_do = int(get_config("vac_do"))
            vac_days = int(get_config("vac_days"))
            cv_safe = int(get_config("cv_safe"))
        except:
            return msg(self, my_errors["2_get_ini"])

        if list_vac[m_val["type"]] == m_val["SputnikV"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                return msg(self, "Укажите место прививки")

            if time_delta("now", list_vac[m_val["d_vac_2"]]) > vac_safe:
                return msg(self, "Сертификат устарел. С даты прививки прошло более " + str(vac_safe) + " дней.")

            delta = time_delta(list_vac[m_val["d_vac_2"]], list_vac[m_val["d_vac_1"]])
            if delta < vac_days:
                return msg(self, "Между прививками прошло " + str(delta) + " дней. "
                                                                           "Это менее " + str(vac_days) + " дней")

            if delta > vac_do:
                return msg(self, "Между прививками прошло " + str(delta) + "дней. "
                                                                           "Это более " + str(vac_do) + " дней.")

        elif list_vac[m_val["type"]] == m_val["Lite"]:

            if len(list_vac[m_val["place"]]) < m_val["min_len"]:
                return msg(self, "Укажите место прививки")

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > vac_safe:
                return msg(self, "Сертификат устарел. С даты прививки прошло более " + str(vac_safe) + " дней.")

        elif list_vac[m_val["type"]] == m_val["issue"]:

            if len(list_vac[m_val["doc"]]) < m_val["min_len"]:
                return msg(self, "Укажите номер сертификата")

            if time_delta("now", list_vac[m_val["d_vac_1"]]) > cv_safe:
                return msg(self, "Сертификат устарел, необходима вакцинация")
        return True


def set_cb_text(combobox, data, rows):
    i = iter(range(1000))
    for item in rows:
        if item[2] == data:
            combobox.setCurrentIndex(next(i) + 1)
            return
        next(i)
