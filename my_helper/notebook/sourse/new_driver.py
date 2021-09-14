from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import QDate as Date
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = '../designer_ui/new_driver.ui'


class NewDriver(QDialog):
    def __init__(self, parent):
        super(NewDriver, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.bosses = []
        self.table = "drivers"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)

        self.cb_select.addItems(["(нет)"])
        for row in self.from_db("family, name", self.table):
            self.cb_select.addItems([row[0] + " " + row[1][0] + "."])
        self.but_status("add")
        self.list_ui = [self.family, self.name, self.surname, self.d_birthday, self.passport, self.adr]
        self.rows_from_db = self.from_db("*", self.table)

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.passport.setValidator(symbols)
        self.adr.setValidator(symbols)

    def ev_ok(self):
        data = self.get_data()
        if not data:
            return
        self.parent.get_new_data(data)
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_data()
            self.but_status("add")
            return
        self.but_status("change")
        family = text[:-3]
        for row in self.rows_from_db:
            if family in row:
                self.set_data(row)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.family.text() in row:
                self.my_update()
                print("update")

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.family.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        self.family.setText(data[0])
        self.name.setText(data[1])
        self.surname.setText(data[2])
        self.d_birthday.setDate(Date.fromString(data[3]))
        self.passport.clear()
        self.adr.clear()
        self.passport.append(data[4])
        self.adr.append(data[5])

    def get_data(self):
        data = list()
        for item in self.list_ui:
            try:
                data.append(item.text())
            except:
                data.append(item.toPlainText())
        if "" in data or "01.01.2000" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return
        return data

    def clean_data(self):
        for item in self.list_ui:
            try:
                item.setText("")
            except:
                item.clear()

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
        self.parent.get_new_data(self.get_data())
        self.close()


