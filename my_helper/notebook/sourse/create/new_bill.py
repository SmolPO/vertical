from PyQt5.QtWidgets import *
from datetime import datetime as dt
import os
import openpyxl
from my_helper.notebook.sourse.database import *
from my_helper.notebook.sourse.create.new_template import TempForm, set_cb_text


class NewBill(TempForm):
    def __init__(self, parent):
        self.status_ = True
        self.conf = Ini(self)
        ui_file = self.conf.get_path_ui("new_bill")
        if not ui_file:
            self.status_ = False
            return
        super(NewBill, self).__init__(ui_file, parent, "bills")
        if not self.status_:
            return
        self.b_bill.clicked.connect(self.ev_bill)
        if self.parent.db.init_list(self.cb_buyer, "*", "itrs", people=True) == ERR:
            self.status_ = False
            return
        self.filename = ""
        self.list_ui = [self.date, self.sb_value, self.cb_buyer, self.file_path, self.note]
        self.date.setDate(dt.datetime.now().date())
        self.init_operations()
        self.bill = True

    def init_mask(self):
        return

    def init_operations(self):
        rows = self.parent.db.get_data("*", self.table)
        if rows == ERR:
            self.status_ = False
            return
        self.cb_select.addItem(empty)
        for row in rows:
            self.cb_select.addItems([". ".join((row[-1], row[0]))])

    def ev_bill(self):
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         self.conf.get_path("path") + self.conf.get_path("path_scan"),
                                                         "PDF Files(*.pdf)")
        if self.filename:
            self.file_path.setText(self.filename.split("/")[-1])
        if self.filename == ERR:
            return

    def _select(self, text):
        return True

    def create_note(self, value, date, people):
        try:
            wb = openpyxl.load_workbook(self.conf.get_path("path") + self.conf.get_path("path_bills") +
                                    "/" + str(dt.now().year) +
                                    "/" + str(dt.now().month) +
                                    "/" + str(dt.now().month) + str(dt.now().year) + ".xlsx")
        except:
            return msg_er(self, GET_FILE)
        try:
            sheet = wb['bills']
        except:
            return msg_er(self, GET_PAGE)
        row = sheet['F2'].value
        sheet['A' + str(row + 3)].value = int(row) + 1
        sheet['B' + str(row + 3)].value = date
        sheet['C' + str(row + 3)].value = value
        sheet['D' + str(row + 3)].value = people
        sheet['F2'].value = int(row) + 1
        path = self.conf.get_path("path") + self.conf.get_path("path_bills") + \
               "/" + str(dt.now().year) + \
               "/" + str(dt.now().month) + \
               "/" + str(dt.now().month) + str(dt.now().year) + ".xlsx"
        if path == ERR:
            return
        try:
            wb.save(path)
            os.startfile(path)
        except:
            return msg_er(self, GET_FILE)


