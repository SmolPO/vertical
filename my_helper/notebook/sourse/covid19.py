import openpyxl as xlsx
from PyQt5.QtWidgets import QMessageBox as mes
from openpyxl.styles import Side, Border
import os
import logging
import datetime as dt
from my_helper.notebook.sourse.database import *
logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)


class NewCovid:
    def __init__(self, parent=None):
        self.parent = parent
        self.border = Border(top=Side(border_style='thin', color='FF000000'),
                           right=Side(border_style='thin', color='FF000000'),
                           bottom=Side(border_style='thin', color='FF000000'),
                           left=Side(border_style='thin', color='FF000000'))

    def create_covid(self):
        list_people = list()
        try:
            rows = self.parent.db.get_data("family, name, surname, post, status, id", "workers") + \
                   self.parent.db.get_data("family, name, surname, post, status, id", "itrs")
        except:
            return msg(self, my_errors["3_get_db"])
        if not rows:
            return msg(self, my_errors["3_get_db"])
        for row in rows:
            if row[-2] == statues[0]:
                list_people.append({"family": short_name(row), "post": row[3]})
        list_people.sort(key=lambda x: x["family"])
        if not list_people:
            mes.question(self.parent, "Сообщение", "Нет рабочих в Базе данных", mes.Cancel)
            return
        path = get_path("path") + get_path("path_pat_covid")
        path_save = path
        try:
            doc = xlsx.open(path)
        except:
            return msg(self, my_errors["4_get_file"])
        try:
            page = "covid"
            sheet = doc[page]
        except:
            return msg(self, my_errors["6_get_sheet"])
        delta = 2
        count_column = 9
        for ind in range(1, 50):
            for j in range(1, 10):
                sheet.cell(row=ind + delta, column=j).value = ""
        for ind in range(1, len(list_people) + 1):
            sheet.cell(row=ind + delta, column=1).value = ind
            sheet.cell(row=ind + delta, column=2).value = dt.datetime.now().date()
            sheet.cell(row=ind + delta, column=3).value = list_people[ind-1]["family"]
            sheet.cell(row=ind + delta, column=4).value = list_people[ind-1]["post"]
            for i in range(1, 9):
                sheet.cell(row=ind + delta, column=count_column).border = self.border
        doc.print_area = "A1:G" + str(len(list_people) + delta)
        try:
            doc.save(path_save)
            os.startfile(path_save)
        except:
            mes.question(self.parent, "Сообщение", "Неверный путь для сохранения файла." + path_save +
                                      " Файл не сохранен", mes.Cancel)
