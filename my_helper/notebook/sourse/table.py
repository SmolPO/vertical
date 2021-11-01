import openpyxl as xlsx
from PyQt5.QtWidgets import QMessageBox as mes
from openpyxl.styles import Side
import os
import datetime as dt
from PyQt5.QtWidgets import QInputDialog
from my_helper.notebook.sourse.database import get_path, statues, short_name, count_days
month = ["январь", "февраль", "март", "апрель", "май", "июнь",
         "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]


class NewTable:
    def __init__(self, parent=None):
        self.parent = parent

    def create_table(self):
        list_people = list()
        rows = self.parent.db.get_data("family, name, surname, status, id", "workers") + \
               self.parent.db.get_data("family, name, surname, status, id", "itrs")
        if not rows:
            mes.question(self.parent, "Сообщение", "Не получилось получить данные из базу данных", mes.Cancel)
            return
        for row in rows:
            if row[-2] != statues[2]:
                list_people.append(short_name(row))
        list_people.sort()
        cur_month = QInputDialog.getItem(self.parent, "Выберите месяц", "Месяц", month, 0)
        path = get_path("path_pat_tabel" + str(cur_month.index(cur_month)))
        path_save = get_path("table_save") + "/" + str(dt.datetime.now().date()) + ".xlxs"
        try:
            doc = xlsx.open(path)
        except:
            mes.question(self.parent, "Сообщение", "Файл не найден" + path, mes.Cancel)
            return
        sheet = doc["covid"]
        delta = 5
        sheet.cell(row=3, column=1).value = str(cur_month) + " " + str(dt.datetime.now().year)
        for ind in range(1, len(list_people)):
            sheet.cell(row=ind + delta, column=1).value = ind
            sheet.cell(row=ind + delta, column=2).value = list_people[ind - 1]["family"]
            for i in range(1, count_days.index(cur_month) + 2):
                sheet.cell(row=ind + delta, column=i).Border(top=Side(border_style='thin', color='FF000000'),
                                                             right=Side(border_style='thin', color='FF000000'),
                                                             bottom=Side(border_style='thin', color='FF000000'),
                                                             left=Side(border_style='thin', color='FF000000'))
        doc.print_area = "A1:Z" + str(len(list_people) + delta)
        try:
            doc.save(path_save)
            os.startfile(path_save, "print")
        except:
            mes.question(self.parent, "Сообщение", "Неверный путь для сохранения файла." + path_save +
                         " Файл не сохранен", mes.Cancel)

