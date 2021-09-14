from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtCore import Qt
from my_helper.notebook.sourse.inserts import get_from_db, update_mat
designer_file = '../designer_ui/materials.ui'
si = ["тн", "т", "кг", "м2", "м", "м/п", "мм", "м3", "л", "мм", "шт"]


class NewMaterial(QDialog):
    def __init__(self, parent=None):
        super(NewMaterial, self).__init__(parent)
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.bosses = []
        self.table = "materials"
        self.provider_ = ""
        self.add_new = True
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)

        self.cb_select.activated[str].connect(self.ev_select)
        self.provider.stateChanged.connect(self.provider_select)

        self.cb_select.addItems(["(нет)"])
        for row in self.from_db("name", self.table):
            self.cb_select.addItems([row[0]])
        self.but_status("add")
        self.rows_from_db = self.from_db("*", self.table)

    def from_db(self, fields, table):
        self.parent.db.execute(get_from_db(fields, table))
        return self.parent.db.fetchall()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        self.name.setValidator(symbols)
        self.value.setValidator(symbols)

    def ev_ok(self):
        if not self.add_new:
            self.my_update()
            self.close()
            return

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
            if text in row:
                self.set_data(row)

    def ev_change(self):
        for row in self.rows_from_db:
            if self.name.text() in row:
                self.my_update()

    def ev_kill(self):
        for row in self.rows_from_db:
            if self.name.text() in row:
                data = [self.name.text(),  self.summ.text(), self.cb_si.currentText()]
                answer = QMessageBox.question(self, "Удаление записи",
                                              "Вы действительно хотите удалить запись " + str(data) + "?",
                                              QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE name = '{1}'".format(
                        self.table, self.name.text()))
                    self.parent.db_conn.commit()
                    self.close()
                    return
                if answer == QMessageBox.Cancel:
                    return

    def set_data(self, data):
        i = iter(range(1, 6))
        self.name.setText(data[next(i)])
        self.cb_si.setCurrentIndex(si.index(data[next(i)]))
        self.value.setText(data[next(i)])
        self.summ.setText(data[3])
        self.provider.setChecked(True if data[next(i)] == "Заказчик" else False)

    def get_data(self):
        if self.name.text() == "" or \
           self.value.text() == "":
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        data = list((self.name.text(), self.cb_si.currentText()))
        if self.add_new:
            data.append(self.value.text())
        else:
            data.append(str(int(self.value.text()) + int(self.summ.text())))
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"
        data.append(self.provider_)
        return data

    def clean_data(self):
        self.name.setText("")
        self.value.setText("")
        self.summ.setText("0")

    def but_status(self, status):
        if status == "add":
            self.add_new = True
            self.name.setEnabled(True)
            self.cb_si.setEnabled(True)
            self.b_kill.setEnabled(False)
        if status == "change":
            self.add_new = False
            self.name.setEnabled(False)
            self.cb_si.setEnabled(False)
            self.b_kill.setEnabled(True)

    def my_update(self):
        self.parent.db.execute(update_mat(self.cb_select.currentText(), "value",
                   str(int(self.summ.text()) + int(self.value.text())), self.table))
        self.parent.db_conn.commit()
        self.close()

    def provider_select(self):
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"


