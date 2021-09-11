from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
designer_file = '../../designer_ui/new_boss.ui'


class NewBoss(QDialog):
    def __init__(self, parent):
        super(NewBoss, self).__init__()
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.bosses = []
        self.table = "bosses"
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_del.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_chouse.activated[str].connect(self.ev_select)
        self.but_status("add")

        self.cb_chouse.addItems(["(нет)"])
        self.parent.db.execute('SELECT * FROM ' + self.table)
        for row in self.parent.db.fetchall():
            self.cb_chouse.addItems([row[0]])

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))

        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(symbols)
        self.phone.setValidator(QREVal(QRE("[0-9]{11}")))
        self.email.QREVal(QRE("[a-zA-Z ._@ 0-9]{30}"))

    def ev_OK(self):
        if '' in self.get_data():
            return
        self.parent.get_new_bosses(self.get_data())
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

        self.parent.db.execute('SELECT * FROM ' + self.table)
        rows = self.parent.db.fetchall()
        for row in rows:
            if text in row:
                self.set_data(row)

    def ev_change(self):
        self.parent.db.execute('SELECT * FROM ' + self.table)
        rows = self.parent.db.fetchall()
        for row in rows:
            if self.family.text() in row and self.name.text() in row:
                self.my_update()
                print("update")
        pass

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
        self.name.setText(data[0])
        self.family.setText(data[1])
        self.family.enabled = False
        self.surname.setText(data[2])
        self.post.setText(data[3])
        self.email.setText(data[4])
        self.phone.setText(data[5])

    def get_data(self):
        return list([self.name.text(),
                     self.family.text(),
                     self.surname.text(),
                     self.post.text(),
                     self.email.text(),
                     self.phone.text()])

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
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_del.setEnabled(True)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_bosses(self.get_data())
        self.close()
        pass

