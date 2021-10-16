from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from my_helper.notebook.sourse.pass_template import get_next_number
from PyQt5.QtWidgets import QMessageBox as mes
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import docx
import docxtpl
import os
designer_file = '../designer_ui/new_worker.ui'


class NewTB(QDialog):
    def __init__(self, parent=None):
        super(NewTB, self).__init__()
        # pass
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.table = "workers"
        self.rows_from_db = self.parent.db.init_list(self.cb_select, "*", self.table, people=True)
        self.main_file = ""
        self.print_file = ""
        self.current_id = self.next_id
        self.list_ui = list()
        self.init_list()

    def init_list(self):
        """
        создать таблицу 0 | ФИО
        добавить все ФИО работающих сотрудников
        :return:
        """
        self.parent.db.init_list(self.cb_contract, "name", "contracts")
        return

    def get_list_people(self):
        """
        Найти все строки, где поставили галочку
        Найти всех сотрудников с такими данными
        Проверить есть ли отсканированный протокол?
        Создать протокол
        Печать протокола
        :param data:
        :return: список Фамилия, Имя, отчество, Номер протокола, Дата протокола, Номер удостоверения
        """
        data = list()
        for people in data:

            pass
        return data

    def _ev_ok(self):
        people = self.get_list_people()
        self.create_protocols(people)
        return True

    def create_protocols(self, people):
        """
        список протоколов: просмотреть всех сотрудников и найти номера протоколов
        :param people:
        :return:
        """
        print_numbers = []
        _types = {"ОТ": "/1", "ПТМ": "/2", "ЭБ": "/3"}
        for item in people:
            number = item[3]
            if not number in print_numbers:
                workers = self.my_find(number, "family, name, surname, numb_protocol, d_protocol")
                print_numbers.append(number)
                for key in _types.keys():
                    self.print_doc(workers, _types[key])
        return

    def get_number_docs(self):
        """
        получить список номеров
        :return:
        """
        numbers = {"OT": "", "PTM": "", "ES": ""}
        return numbers

    def my_find(self, number, field):
        rows = self.parent.db.get_data(field, self.table)
        result = []
        for row in rows:
            if row[0] == number:
                result.append(row)
        return result

    def print_doc(self, workers, _type):
        data = dict()
        data["number"] = get_next_number()
        data["date"] = workers[4] + _type  # номер столбца с датой
        data["number_doc"] = workers[3] # номер протокол
        doc = docxtpl.DocxTemplate(self.main_file)
        doc.render(self.data)
        try:
            doc.save(self.print_file)
        except:
            self.close()
        self.create_table(workers)
        os.startfile(self.print_file)
        return

    def create_table(self, data):
        i = 1
        g = iter(range(len(data)))
        doc = docx.Document(self.print_file)
        for item in data:
            doc.tables[1].add_row()
            doc.tables[1].rows[i].cells[0].text = str(i)
            doc.tables[1].rows[i].cells[1].text = " ".join(item[:3]) # ФИО
            doc.tables[1].rows[i].cells[2].text = item[3]   # профессия
            doc.tables[1].rows[i].cells[3].text = "Сдал №" + item[4]
            i = next(g)
        doc.save(self.print_file)
