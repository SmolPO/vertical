import openpyxl as xlsx
from PyQt5.QtWidgets import QMessageBox as mes
from openpyxl.styles import Side
import os
import datetime as dt
from my_helper.notebook.sourse.database import get_path, statues, short_name


class NewCovid:
    def __init__(self, parent=None):
        self.parent = parent

    def create_covid(self):
        list_people = list()
        rows = self.parent.db.get_data("family, name, surname, status, id", "workers") + \
               self.parent.db.get_data("family, name, surname, status, id", "itrs")
        if not rows:
            mes.question(self.parent, "Сообщение", "Не получилось получить данные из базу данных", mes.Cancel)
            return
        for row in rows:
            if row[-2] == statues[0]:
                list_people.append({"family": short_name(row), "post": row[3]})
        list_people.sort(key=lambda x: x["family"])
        path = get_path("path_pat_covid")
        path_save = get_path("covid_save") + "/" + str(dt.datetime.now().date()) + ".xlxs"
        try:
            doc = xlsx.open(path)
        except:
            mes.question(self.parent, "Сообщение", "Файл не найден" + path, mes.Cancel)
            return
        sheet = doc["covid"]
        delta = 5
        for ind in range(1, len(list_people)):
            sheet.cell(row=ind + delta, column=1).value = ind
            sheet.cell(row=ind + delta, column=2).value = dt.datetime.now().date()
            sheet.cell(row=ind + delta, column=3).value = list_people[ind-1]["family"]
            sheet.cell(row=ind + delta, column=4).value = list_people[ind-1]["post"]
            for i in range(1, 10):
                sheet.cell(row=ind + delta, column=i).Border(top=Side(border_style='thin', color='FF000000'),
                                                             right=Side(border_style='thin', color='FF000000'),
                                                             bottom=Side(border_style='thin', color='FF000000'),
                                                             left=Side(border_style='thin', color='FF000000'))
        doc.print_area = "A1:G" + str(len(list_people) + delta)
        try:
            doc.save(path_save)
            os.startfile(path_save, "print")
        except:
            mes.question(self.parent, "Сообщение", "Неверный путь для сохранения файла." + path_save +
                                      " Файл не сохранен", mes.Cancel)
