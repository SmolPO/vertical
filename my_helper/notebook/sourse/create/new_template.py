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
        # self.parent.db.execute("UPDATE itrs SET status = 'работает' where family = 'Сорокин'")
        # self.parent.db.conn.commit()
        try:
            self.rows_from_db = self.parent.db.get_data("*", self.table)
        except:
            msg(self, my_errors["3_get_db"])
            return
        try:
            self.next_id = self.parent.db.get_next_id(self.table)
        except:
            msg(self, my_errors["3_get_db"])
            return

    def check_start(self, ui_file):
        self.status_ = True
        self.path_ = ui_file
        try:
            uic.loadUi(ui_file, self)
            return True
        except:
            return msg(self, my_errors["1_get_ui"])

    def ev_ok(self):
        if not self.check_input():
            return False
        if not self._ev_ok():
            return
        data = self.get_data()
        if not data:
            return
        self.parent.db.my_commit(ins.add_to_db(data, self.table))
        try:
            pass
        except:
            return msg(self, my_errors["9_commit"])
        self.close()

    def ev_select(self, text):
        if text == empty:
            self.clean_data()
            self.but_status("add")
            self.current_id = self.next_id
            return
        else:
            self.but_status("change")

        if self._ev_select(text):
            for row in self.rows_from_db:
                if text.split(".")[0] == str(row[-1]):
                    self.set_data(row)
                    return

    def set_data(self, data):
        i = iter(range(len(data)))
        for item in self.list_ui[:self.slice_set]:
            item.setText(data[next(i)])
        self.current_id = data[-1]
        self._set_data(data)

    def get_data(self):
        data = list()
        for item in self.list_ui[:self.slice_get]:
            data.append(item.text())
        data = self._get_data(data)
        if not data:
            return False
        data.append(str(self.current_id))
        return data

    def clean_data(self):
        if self._clean_data():
            for item in self.list_ui[:self.slice_clean]:
                item.setText("")

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
        if not self._but_status(status):
            return False
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)


def set_cb_text(combobox, data, rows):
    i = iter(range(1000))
    for item in rows:
        if item[2] == data:
            combobox.setCurrentIndex(next(i) + 1)
            return
        next(i)