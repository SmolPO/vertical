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
        self.slice_select = 10
        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.list_ui = list()
        self.current_id = self.next_id
        self.date.setDate(dt.now().date())
        self.init_operations()

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
            self.cb_select.addItems([", ".join((row[0], row[-1]))])
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
        path = get_path("path") + get_path("path_bills") + "/" + \
               str(str(dt.now())[:10].replace("-", ".") + "_" + str(self.current_id + 1) + ".pdf")
        print(path)
        try:
            os.replace(self.filename, path)
        except:
            return msg(self, "Проблема с правом доступа. "
                             "1. - вручную скопируйте файл в папку со счетами,"
                             " 2 - Снова нажмите Выбрать файл и укажите файл чека в новом месте")
        self.create_note(self.sb_value.value(), self.date.text().replace("-", "."), self.cb_buyer.currentText()[:-5])
        return data

    def check_input(self):
        if self.sb_value.value() == 0:
            return False
        if self.cb_buyer.currentIndex() == 0:
            return False
        if self.filename == "":
            return False
        return True

    def _clean_data(self):
        self.current_id = 1
        self.date.setDate(zero)
        self.cb_buyer.setCurrentIndex(0)
        self.sb_value.setValue(0)
        self.note.clear()
        return True

    def _create_filename(self):
        my_list = [[], []]
        list_id = []

        for item in self.rows_from_db:
            my_list[0].append(item[3].split("/")[-1].split("_")[0])
            my_list[1].append(item[3].split("/")[-1].split("_")[1][:-4])
        for item in my_list:
            if my_list[0] == self.date.text():
                list_id.append(my_list[1])
        print(my_list)
        print(list_id)

    def ev_bill(self):
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         get_path("path") + get_path("scan"),
                                                         "PDF Files(*.pdf)")
        if self.filename:
            self.rb_isfile.setChecked(True)
        else:
            self.rb_isfile.setChecked(False)
        return

    def _ev_select(self, text):
        for row in self.rows_from_db:
            print(text[12:])
            if text[12:] in row:
                self.set_data(row)
                return
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
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


