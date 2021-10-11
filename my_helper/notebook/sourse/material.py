from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.template import TempForm
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.inserts import my_update

designer_file = '../designer_ui/materials.ui'
si = ["тн", "т", "кг", "м2", "м", "м/п", "мм", "м3", "л", "мм", "шт"]


class NewMaterial(TempForm):
    def __init__(self, parent=None):
        super(NewMaterial, self).__init__(designer_file)
        self.parent = parent
        self.bosses = []
        self.table = "materials"
        self.provider_ = ""
        self.add_new = True
        self.provider.stateChanged.connect(self.provider_select)
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        self.parent.db.init_list(self.cb_contracts, "name", self.table)
        self.cb_contracts.addItems(["(нет)"])

        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = 0
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id
        self.list_ui = list()

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я 0-9]{9}"))
        self.name.setValidator(symbols)
        self.value.setValidator(symbols)

    def _ev_ok(self):
        if not self.add_new:
            self.my_update()
            self.close()
            return True

    def _ev_select(self, text):
        return True

    def _set_data(self, data):
        i = iter(range(1, 6))
        self.name.setText(data[next(i)])
        self.cb_si.setCurrentIndex(si.index(data[next(i)]))
        self.value.setText(data[next(i)])
        self.summ.setText(data[3])
        self.provider.setChecked(True if data[next(i)] == "Заказчик" else False)

        contracts = self.from_db("name, number", "contracts")
        j = iter(range(len(contracts)))
        for item in contracts:
            if data[4] in item:
                self.cb_contracts.setCurrentIndex(next(j))
            next(j)

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
        data.append(self.contract.currentText())
        return data

    def clean_data(self):
        self.name.setText("")
        self.value.setText("")
        self.summ.setText("0")
        self.cb_select.setCurrentIndex(0)
        self.cb_contracts.setCurrentIndex(0)

    def _but_status(self, status):
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
        return False

    def my_update(self):
        self.parent.db.execute(my_update(self.cb_select.currentText(), "value",
                   str(int(self.summ.text()) + int(self.value.text())), self.table))
        self.parent.db_conn.commit()
        self.close()

    def provider_select(self):
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"


