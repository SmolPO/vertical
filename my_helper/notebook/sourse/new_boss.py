from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = '../designer_ui/new_boss.ui'


class NewBoss(QDialog):
    def __init__(self, parent):
        super(NewBoss, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.bosses = []
        self.table = "bosses"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_del.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_chouse.activated[str].connect(self.ev_select)
        self.but_status("add")
        self.rows_from_db = self.from_db("*", self.table)
        self.cb_chouse.addItems(["(нет)"])
        for row in self.rows_from_db:
            self.cb_chouse.addItems([row[0]])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(symbols)
        self.phone.setValidator(QREVal(QRE("[0-9]{11}")))
        self.email.QREVal(QRE("[a-zA-Z ._@ 0-9]{30}"))

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
        else:
            self.but_status("change")

        for row in self.rows_from_db:
            if text in row:
                self.set_data(row)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.family.text() in row and self.name.text() in row:
                self.my_update()
                print("update")
        pass

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.family.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    print("DELETE FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    print(row)
                    self.parent.db.execute("DELETE FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        self.family.setText(data[0])
        self.family.setEnabled(False)
        self.name.setText(data[1])
        self.surname.setText(data[2])
        self.post.setText(data[3])
        self.email.setText(data[4])
        self.phone.setText(data[5])
        self.cb_sex.setCurrentIndex(0) if data[6] == "М" else self.cb_sex.setCurrentIndex(1)

    def get_data(self):
        if not self.check_input():
            return list([self.family.text(),
                         self.name.text(),
                         self.surname.text(),
                         self.post.text(),
                         self.email.text(),
                         self.phone.text(),
                         self.cb_sex.currentText()])
        else:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)

    def check_input(self):
        if "" in list([self.family.text(),
                     self.name.text(),
                     self.surname.text(),
                     self.post.text()]):
            return False
        return True

    def clean_data(self):
        self.name.setText("")
        self.family.setText("")
        self.surname.setText("")
        self.post.setText("")
        self.email.setText("")
        self.phone.setText("")

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_del.setEnabled(False)
            self.family.setEnabled(True)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_del.setEnabled(True)
            self.family.setEnabled(False)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_data(self.get_data())
        self.close()
        pass

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()
