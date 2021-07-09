from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date

"""
валидация, защита от ввода в табл в разнобой
"""
class NewContact(QDialog):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(parent)
        uic.loadUi('../designer_ui/new_contract.ui', self)
        # pass
        self.parent = parent
        self.table = "contract"
        self.contract = []
        self.comp = []
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_del.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_chouse.activated[str].connect(self.ev_select)
        self.but_status("add")

        self.cb_chouse.addItems(["(нет)"])
        self.cb_comp.addItems(["(нет)"])

        contract = self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        comp = self.parent.database_cur.execute('SELECT * FROM company')
        if not comp:
            msg = QMessageBox.question("Внимание", "Нельзя добавить договор пока не добавленини одна организация",
                                       QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.close()

        for row in contract:
            self.cb_chouse.addItems([row[0]])
        for row in comp:
            self.cb_comp.addItems([row[0]])

    def ev_OK(self):
        self.parent.get_new_bosses(self.get_all_text())
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_kill(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        print(self.family.text())
        for row in rows:
            if self.family.text() in row:
                data = self.get_all_text()
                answer = QMessageBox.question(self, "Удаление записи", "Вы действительно хотите удалить запись " + str(data) + "?",
                                     QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.database_cur.execute("SELECT * FROM {0} WHERE number = '{1}'".format(
                        self.table, self.number.text()))
                    self.parent.database_conn.commit()  # TODO удаление
                    return
                if answer == QMessageBox.Cancel:
                    return
                pass
        pass

    def ev_select(self, text):
        if text == "(нет)":
            self.clean_all_text()
            self.but_status("add")
            return
        else:
            self.but_status("change")

        self.parent.database_cur.execute('SELECT * FROM contract')
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if text in row:
                self.set_all_text(row)

    def ev_change(self):
        self.parent.database_cur.execute('SELECT * FROM ' + self.table)
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if self.number.text() in row:
                self.update()
                print("update")
        pass

    def clean_all_text(self):
        self.name.setText("")
        self.cb_cust.setCurrentText("")  # TODO set text
        self.number.setText("")
        self.date.setDate(Date.fromString("01.01.2000", "dd.mm.yyyy"))
        self.object.setText("")
        self.work.setText("")
        self.part.setText("")

    def set_all_text(self, data):
        self.name.setText(data[0])
        self.cb_cust.setCurrentText(data[1])  # TODO set text
        self.number.setText(data[2])
        self.date.setDate(Date.fromString(data[3], "dd.mm.yyyy"))
        self.object.setText(data[4])
        self.work.setText(data[5])
        self.part.setText(data[6])

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