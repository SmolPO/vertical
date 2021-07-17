from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal

class NewBoss(QDialog):
    def __init__(self, parent):
        super(NewBoss, self).__init__()
        uic.loadUi('../designer_ui/new_boss.ui', self)
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
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        for row in self.parent.database_cur.fetchall():
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
        self.parent.get_new_bosses(self.get_all_text())
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_all_text()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if text in row:
                self.set_all_text(row)

    def ev_change(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.family.text() in row and self.name.text() in row:
                self.update()
                print("update")
        pass

    def ev_kill(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.family.text() in row:
                data = self.get_all_text()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.database_cur.execute("SELECT * FROM {0} WHERE family = '{1}'".format(
                        self.table, self.family.text()))
                    self.parent.database_conn.commit()  # TODO удаление
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_all_text(self, data):
        self.name.setText(data[0])
        self.family.setText(data[1])
        self.surname.setText(data[2])
        self.post.setText(data[3])
        self.email.setText(data[4])
        self.phone.setText(data[5])

    def get_all_text(self):
        return list([self.name.text(),
                     self.family.text(),
                     self.surname.text(),
                     self.post.text(),
                     self.email.text(),
                     self.phone.text()])

    def clean_all_text(self):
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

    def update(self):

        pass

