import logging
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import get_path_ui, get_path, empty, si

logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("materials")


class NewMaterial(TempForm):
    def __init__(self, parent=None):
        super(NewMaterial, self).__init__(designer_file)
        if not self.status_:
            return
        self.parent = parent
        self.table = "materials"
        self.provider_ = ""
        self.add_new = True
        self.provider.stateChanged.connect(self.provider_select)
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        self.parent.db.init_list(self.cb_contracts, "name", "contracts")

        self.init_mask()
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = 0
        self.next_id = self.parent.db.get_next_id(self.table)
        self.current_id = self.next_id
        self.list_ui = list()

    def init_mask(self):
        self.name.setValidator(QREVal(QRE("[а-яА-Я 0-9]{9}")))
        self.value.setValidator(QREVal(QRE("[0-9]{9}")))

    def _ev_ok(self):
        return True

    def _ev_select(self, text):
        self.slice_select = len(text)
        if text != "(нет)":
            self.add_new = False
        else:
            self.add_new = True
        return True

    def _set_data(self, data):
        i = iter(range(0, 5))
        self.name.setText(data[next(i)])
        self.cb_si.setCurrentIndex(si.index(data[next(i)]))
        self.value.setText(data[next(i)])
        self.summ.setText(data[2])
        self.provider.setChecked(True if data[next(i)] == "Заказчик" else False)

        contracts = self.parent.db.get_data("name, number", "contracts")
        j = iter(range(len(contracts)))
        for item in contracts:
            if data[4] in item:
                self.cb_contracts.setCurrentIndex(next(j) + 1)
                return
            next(j)

    def _get_data(self, data):
        data.append(self.name.text())
        data.append(self.cb_si.currentText())
        if self.add_new:
            data.append(self.value.text())
        else:
            data.append(str(int(self.value.text()) + int(self.summ.text())))
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"
        data.append(self.provider_)
        data.append(self.cb_contracts.currentText())
        return data

    def _clean_data(self):
        self.name.setText("")
        self.value.setText("")
        self.summ.setText("0")
        self.cb_select.setCurrentIndex(0)
        self.cb_contracts.setCurrentIndex(0)

    def _but_status(self, status):
        return True

    def provider_select(self):
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"

    def check_input(self):
        data = [self.value.text(), self.name.text(), self.cb_contracts.currentText(), self.cb_si.currentText()]
        if "" in data or empty in data:
            QMessageBox.question(self, "Внимание", "Заполните все поля перед добавлением", QMessageBox.Cancel)
            return False
        return True
