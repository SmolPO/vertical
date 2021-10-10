from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.inserts import get_from_db
"""
валидация, защита от ввода в табл в разнобой
"""
designer_file = '../designer_ui/new_contract.ui'

fields = ["name", "customer", "number", "date", "object", "type_work", "place", "id"]

class NewContact(QDialog):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(parent)
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.table = "contract"
        self.contract = []
        self.comp = []
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_chouse.activated[str].connect(self.ev_select)
        self.but_status("add")
        self.init_mask()

        self.parent.db.init_list(self.cb_comp, "*", self.table)
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        if not self.rows_from_db:
            self.close()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))

    def ev_ok(self):
        data = self.get_data()
        if not data:
            return
        self.parent.get_new_data(data)
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.name.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи", "Вы действительно хотите удалить запись "
                                              + str(data) + "?", QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE number = '{1}'".format(self.table, self.number.text()))
                    self.parent.db.my_commit()
                    self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clear()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        for row in self.rows_from_db:
            if text in row:
                self.set_data(row)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.number.text() in row:
                self.my_update()
                print("update")

    def clear(self):
        self.name.setText("")
        self.cb_comp.setCurrentText("")  # TODO set text
        self.number.setText("")
        self.date.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))
        self.object.setText("")
        self.work.setText("")
        self.part.setText("")

    def set_data(self, data):
        self.name.setText(data[0])
        #  self.cb_cust.setCurrentText(data[1])  # TODO set text
        self.number.setText(data[2])
        self.date.setDate(Date.fromString(data[3], "dd.mm.yyyy"))
        self.object.setText(data[4])
        self.work.setText(data[5])
        self.part.setText(data[6])

    def get_data(self):
        if not self.check_input():
            return list([self.name.text(), self.number.text(),
                         self.date.text(), self.object.toPlainText(), self.work.toPlainText(),
                         self.part.text()])
        else:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.object.toPlainText(), self.work.toPlainText(),
                      self.part.text()]) and self.date.text() != "01.01.2000":
            return False
        return True

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
            self.number.setEnabled(True)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)
            self.number.setEnabled(False)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_data(self.get_data())
        self.close()
        pass

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()