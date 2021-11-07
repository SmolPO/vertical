from PyQt5.QtCore import QDate as Date
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox as mes
from datetime import datetime as dt
import os
import openpyxl
from my_helper.notebook.sourse.database import *
from my_helper.notebook.sourse.create.new_template import TempForm, set_cb_text
#  logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_bill")


class NewBill(TempForm):
    def __init__(self, parent):
        super(NewBill, self).__init__(designer_file, parent, "bills")
        if not self.status_:
            return
        self.b_bill.clicked.connect(self.ev_bill)
        try:
            self.parent.db.init_list(self.cb_buyer, "*", "itrs", people=True)
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.filename = ""
        self.list_ui = [self.date, self.sb_value, self.cb_buyer, self.file_path, self.note]
        self.date.setDate(dt.datetime.now().date())
        self.init_operations()
        self.bill = True

    def init_mask(self):
        return

    def init_operations(self):
        try:
            rows = self.parent.db.get_data("*", self.table)
        except:
            self.status_ = False
            return msg(self, my_errors["3_get_db"])
        self.cb_select.addItem(empty)
        for row in rows:
            self.cb_select.addItems([". ".join((row[-1], row[0]))])
        return

    def _set_data(self, data):
        self.current_id = data[5]
        self.date.setDate(from_str(data[0]))
        set_cb_text(self.cb_buyer, data[2], self.rows_from_db)
        self.sb_value.setValue(int(data[1]))
        self.note.clear()
        self.note.append(data[4])

    def _get_data(self, data):
        data.append(self.date.text())
        data.append(str(self.sb_value.value()))
        data.append(self.cb_buyer.currentText()[:-5])
        self._create_filename()
        data.append(self.filename)
        data.append(self.note.toPlainText())


    def ev_bill(self):
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         get_path("path") + get_path("path_scan"),
                                                         "PDF Files(*.pdf)")
        if self.filename:
            self.file_path.setText(self.filename.split("/")[-1])
        return

    def _select(self, text):
        return True

    def create_note(self, value, date, people):
        try:
            wb = openpyxl.load_workbook(get_path("path") + get_path("path_bills") +
                                    "/" + str(dt.now().year) +
                                    "/" + str(dt.now().month) +
                                    "/" + str(dt.now().month) + str(dt.now().year) + ".xlsx")
        except:
            return msg(self, my_errors["4_get_file"])
        try:
            sheet = wb['bills']
        except:
            return msg(self, my_errors["6_get_sheet"])
        row = sheet['F2'].value
        sheet['A' + str(row + 3)].value = int(row) + 1
        sheet['B' + str(row + 3)].value = date
        sheet['C' + str(row + 3)].value = value
        sheet['D' + str(row + 3)].value = people
        sheet['F2'].value = int(row) + 1
        try:
            wb.save(get_path("path") + get_path("path_bills") +
                        "/" + str(dt.now().year) +
                        "/" + str(dt.now().month) +
                        "/" + str(dt.now().month) + str(dt.now().year) + ".xlsx")
        except:
            return msg(self, my_errors["4_get_file"])
        try:
            os.startfile(get_path("path") + get_path("path_bills") +
                        "/" + str(dt.now().year) +
                        "/" + str(dt.now().month) +
                        "/" + str(dt.now().month) + str(dt.now().year) + ".xlsx")
        except:
            return msg(self, my_errors["4_get_file"])


