from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *


class NewMaterial(TempForm):
    def __init__(self, parent=None):
        self.conf = Ini(self)
        ui_file = self.conf.get_path_ui("materials")
        if not ui_file or ui_file == ERR:
            self.status_ = False
            return
        super(NewMaterial, self).__init__(ui_file, parent, "materials")
        if not self.status_:
            return
        self.provider_ = ""
        self.add_new = True
        self.provider.stateChanged.connect(self.provider_select)
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table)
        if self.rows_from_db == ERR:
            return
        if self.parent.db.init_list(self.cb_contracts, "number, id", "contracts") == ERR:
            return
        self.init_mask()
        self.list_ui = [self.value, self.name, self.cb_contracts, self.cb_si]

    def init_mask(self):
        self.value.setValidator(QREVal(QRE("[0-9]{9}")))

    def _ev_select(self, text):
        self.slice_select = len(text)
        if text != NOT:
            self.add_new = False
        else:
            self.add_new = True
        return True

    def _set_data(self, data):
        if not data:
            return
        contracts = self.parent.db.get_data("name, number", "contracts")
        if contracts == ERR:
            return
        i = iter(range(0, 5))
        self.name.setText(data[next(i)])
        self.cb_si.setCurrentIndex(si.index(data[next(i)]))
        self.value.setText(data[next(i)])
        self.summ.setText(data[2])
        self.provider.setChecked(True if data[next(i)] == "Заказчик" else False)
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

    def provider_select(self):
        self.provider_ = "Заказчик" if self.provider.isChecked() else "Подрядчик"