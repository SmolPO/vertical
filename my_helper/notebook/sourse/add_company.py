from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date


class AddCompany(QDialog):
    def __init__(self, parent=None):
        super(AddCompany, self).__init__(parent)
        uic.loadUi('../designer_ui/add_company.ui', self)
        # pass
        self.parent = parent
        self.new_company = []
        self.table = "company"
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

    def ev_OK(self):
        self.parent.get_new_bosses(self.get_all_text())
        self.close()

    def ev_cancel(self):
        self.close()

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

    def ev_change(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.family.text() in row and self.name.text() in row:
                self.update()
                print("update")
        pass

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_all_text()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        for row in self.parent.database_cur.fetchall():
            if text in row:
                self.set_all_text(row)

    def set_all_text(self, data):
        self.company.setText(data[0])
        self.adr.appendPlainText(data[1])
        self.ogrn.setText(str(data[2]))
        self.inn.setText(str(data[3]))
        self.kpp.setText(str(data[4]))
        self.bik.setText(str(data[5]))
        self.korbill.setText(str(data[6]))
        self.rbill.setText(str(data[7]))
        self.bank.setText(data[8])
        self.family.setText(data[9])
        self.name.setText(data[10])
        self.surname.setText(data[11])
        self.post.setText(data[12])
        self.count_dovr.setText(data[13])
        self.date_dovr.setText(data[14])

    def clean_all_text(self):
        self.company.setText("")
        self.adr.append("")
        self.ogrn.setText("")
        self.inn.setText("")
        self.kpp.setText("")
        self.bik.setText("")
        self.korbill.setText("")
        self.rbill.setText("")
        self.bank.setText("")
        self.family.setText("")
        self.name.setText("")
        self.surname.setText("")
        self.post.setText("")
        self.count_dovr.setText("")
        self.date_dovr.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))

    def get_all_text(self):
        data = list([self.company.text(),
                    self.adr.toPlainText(),
                    self.ogrn.text(),
                    self.inn.text(),
                    self.kpp.text(),
                    self.bik.text(),
                    self.korbill.text(),
                    self.rbill.text(),
                    self.bank.text(),
                    self.family.text(),
                    self.name.text(),
                    self.surname.text(),
                    self.post.text(),
                    self.count_dovr.text(),
                    self.date_dovr.text()])
        return data

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