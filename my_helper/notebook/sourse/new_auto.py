from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = '../designer_ui/new_auto_2.ui'


class NewAuto(QDialog):
    def __init__(self, parent=None):
        super(NewAuto, self).__init__(parent)
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.bosses = []
        self.table = "auto"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)
        self.is_track.stateChanged.connect(self.have_track)

        self.cb_select.addItems(["(нет)"])
        for row in self.from_db("gov_number, model", self.table):
            self.cb_select.addItems([" ".join((row[:2]))])
        self.but_status("add")
        self.track_number.setEnabled(False)
        self.list_ui = [self.model, self.brand, self.gov_number, self.track_number]
        self.rows_from_db = self.from_db("*", self.table)

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))

        self.model.setValidator(symbols)
        self.brand.setValidator(symbols)
        self.gov_number.setValidator(symbols)
        self.track_number.setValidator(symbols)

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

        for row in self.rows_from_db:
            if text.split()[0] in row:
                self.set_data(row)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.gov_number.text() in row:
                self.my_update()
                print("update")

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.gov_number.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE gov_number = '{1}'".format(
                        self.table, self.gov_number.text()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        i = iter(range(len(data)))
        for item in self.list_ui:
            item.setText(data[next(i)])

    def get_data(self):
        if self.model.text() == "" or \
           self.brand.text() == "" or \
           self.gov_number.text() == "" or (self.is_track.isChecked() and self.track_number.text() == ""):
            QMessageBox.question(self, "Внимание",
                                          "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return
        data = list((self.model.text(),
                     self.brand.text(),
                     self.gov_number.text()))
        if self.is_track.isChecked():
            data.append(self.track_number.text())
        else:
            data.append("")
        return data

    def clean_data(self):
        for item in self.list_ui:
            item.setText("")

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.gov_number.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.gov_number.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)

    def my_update(self):
        self.ev_kill()
        self.parent.get_new_data(self.get_data())
        self.close()

    def have_track(self, state):
        if state == Qt.Checked:
            self.track_number.setEnabled(True)
        else:
            self.track_number.setEnabled(False)


