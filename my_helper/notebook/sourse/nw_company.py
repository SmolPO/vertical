from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.inserts import get_from_db
designer_file = "../designer_ui/add_company.ui"
fields = ["company", "adr", "ogrn", "inn", "kpp", "bik", "korbill", "rbill", "bank", "family", "name", "surname",
          "post", "count_attorney", "date_attorney", "id"]


class NewCompany(QDialog):
    def __init__(self, parent=None):
        super(NewCompany, self).__init__(parent)
        uic.loadUi(designer_file, self)
        # pass
        self.parent = parent
        self.new_company = []
        self.table = "company"
        self.b_ok.clicked.connect(self.ev_ok)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_change.clicked.connect(self.ev_change)
        self.cb_select.activated[str].connect(self.ev_select)
        self.but_status("add")
        self.init_mask()
        self.current_id = 0

        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        if not self.rows_from_db and self.rows_from_db != []:
            self.close()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я]{30}"))
        number_prot = QREVal(QRE("[А-Яа-я /- 0-9]{10}"))
        #  self.adr.appendPlainText(data[1])
        self.ogrn.setValidator(QREVal(QRE("[0-9]{14}")))
        self.inn.setValidator(QREVal(QRE("[0-9]{10}")))
        self.kpp.setValidator(QREVal(QRE("[0-9]{9}")))
        self.bik.setValidator(QREVal(QRE("[0-9]{8}")))
        self.korbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.rbill.setValidator(QREVal(QRE("[0-9]{20}")))
        self.bank.setValidator(number_prot)
        self.family.setValidator(symbols)
        self.name.setValidator(symbols)
        self.surname.setValidator(symbols)
        self.post.setValidator(symbols)
        self.count_dovr.setValidator(number_prot)

    def ev_ok(self):
        data = self.get_data()
        if not data:
            return
        self.parent.get_new_data(data)
        self.close()

    def ev_cancel(self):
        self.close()

    def ev_change(self):
        self.parent.db.update(self.get_data())
        self.close()

    def ev_kill(self):
        self.parent.db.kill_value(self.get_data())
        self.close()

    """    for row in self.rows_from_db:
            if self.company.text() in row:
                data = self.get_data()
                answer = QMessageBox.question(self, "Удаление записи", "Вы действительно хотите удалить запись "
                                              + str(data) + "?", QMessageBox.Ok | QMessageBox.Cancel)
                if answer == QMessageBox.Ok:
                    self.parent.db.execute("DELETE FROM {0} WHERE company = '{1}'".format(self.table,
                                                                                          self.company.text()))
                    self.parent.db.my_commit()
                    self.close()"""

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

    def set_data(self, data):
        self.company.setText(data[fields.index("company")])
        self.adr.appendPlainText(data[fields.index("adr")])
        self.ogrn.setText(data[fields.index("ogrn")])
        self.inn.setText(data[fields.index("inn")])
        self.kpp.setText(data[fields.index("kpp")])
        self.bik.setText(data[fields.index("bik")])
        self.korbill.setText(data[fields.index("korbill")])
        self.rbill.setText(data[fields.index("rbill")])
        self.bank.setText(data[fields.index("bank")])
        self.family.setText(data[fields.index("family")])
        self.name.setText(data[fields.index("name")])
        self.surname.setText(data[fields.index("surname")])
        self.post.setText(data[fields.index("post")])
        self.count_dovr.setText(data[fields.index("count_attorney")])
        self.date_dovr.setDate(Date.fromString(data[fields.index("date_attorney")], "dd.mm.yyyy"))
        self.current_id = data[fields.index("id")]

    def clear(self):
        self.company.setText("")
        self.adr.clear()
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
        self.current_id = 0

    def get_data(self):
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
        if "" in data or "01.01.2000" in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return []
        else:
            return data

    def but_status(self, status):
        if status == "add":
            self.b_ok.setEnabled(True)
            self.b_change.setEnabled(False)
            self.b_kill.setEnabled(False)
            self.company.setEnabled(True)
        if status == "change":
            self.b_ok.setEnabled(False)
            self.b_change.setEnabled(True)
            self.b_kill.setEnabled(True)
            self.company.setEnabled(False)
