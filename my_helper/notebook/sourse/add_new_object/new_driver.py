from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from ..inserts import get_from_db
designer_file = '../../designer_ui/new_driver.ui'


class NewDriver(QDialog):
    def __init__(self, parent):
        super(NewDriver, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.bosses = []
        self.table = "drivers"
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)

        self.cb_select.addItems(["(нет)"])
        self.parent.db.execute(get_from_db("family, name", self.table))
        for row in self.parent.db.fetchall():
            self.cb_select.addItems(row[0] + " " + row[1][0] + ".")
        self.but_status("add")
        self.list_ui = [self.family, self.name, self.surname, self.d_birthday, self.passport, self.adr]

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.passport.setValidator(symbols)
        self.adr.setValidator(symbols)

    def ev_OK(self):
        if not self.get_data():
            return
        self.parent.get_new_driver(self.get_data())
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_data()
            self.but_status("add")
            return
        self.but_status("change")

        self.parent.db.execute(get_from_db("*", self.table))
        rows = self.parent.db.fetchall()
        for row in rows:
            if text[:-4] in row:
                self.set_data(row)

    def ev_change(self):
        self.parent.db.execute(get_from_db("*", self.table))
        rows = self.parent.db.fetchall()
        for row in rows:
            if self.family.text() in row:
                self.my_update()
                print("update")

    def ev_kill(self):
        self.parent.db.execute('SELECT * FROM ' + self.table)
        rows = self.parent.db.fetchall()
        for row in rows:
            if self.family.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    self.parent.database_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        for item, i in self.list_ui, range(len(data)):
            item.setText(data[i])

    def get_data(self):
        data = list()
        for item in self.list_ui:
            data.append(item.text())
        if "" in data:
            answer = QMessageBox.question(self, "Внимание",
                                          "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return None
        return data

    def clean_data(self):
        for item in self.list_ui:
            item.setText("")

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.family.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.family.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_driver(self.get_data())
        self.close()


