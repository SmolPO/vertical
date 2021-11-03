from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
import docx
import logging
import pymorphy2
import docxtpl
from my_helper.notebook.sourse.my_pass.pass_template import TempPass
from my_helper.notebook.sourse.database import *
designer_file = get_path_ui("pass_unlock")


class UnlockPass(TempPass):
    def __init__(self, parent):
        super(UnlockPass, self).__init__(designer_file, parent, "workers")
        if not self.status_:
            return
        self.parent = parent
        # my_pass
        self.d_from.setDate(dt.datetime.now().date())
        self.d_to.setDate(Date(*from_str(".".join([str(count_days[dt.datetime.now().month - 1]),
                                                   str(dt.datetime.now().month),
                                                   str(dt.datetime.now().year)]))))
        self.cb_all_days.stateChanged.connect(self.all_days)
        try:
            self.rows_from_db = self.parent.db.get_data("*", self.table)
        except:
            mes.question(self, "Сообщение", my_errors["8_get_data"], mes.Cancel)
            return
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}
        self.main_file += "/pass_unlock.docx"
        self.count_days = 14

    def init_workers(self):
        for name in self.parent.db.get_data("family, name, id", self.table):
            self.cb_worker.addItem(str(name[-1]) + ". " + " ".join((name[0], name[1][0])) + ".")
        for name in self.parent.db.get_data("family, name, id", "itrs"):
            self.cb_worker.addItem(str(name[-1]) + ". " + " ".join((name[0], name[1][0])) + ".")

    def _get_data(self):
        family = self.cb_worker.currentText().split(".")[0]
        morph = pymorphy2.MorphAnalyzer()
        for row in self.parent.db.get_data("family, name, surname, post, live_adr, id", "itrs"):
            if family == str(row[-1]):  # на форме фамилия в виде Фамилия И.
                self.data["family"] = morph.parse(row[0])[0].inflect({'datv'})[0].capitalize()
                self.data["name"] = morph.parse(row[1])[0].inflect({'datv'})[0].capitalize()
                self.data["surname"] = morph.parse(row[2])[0].inflect({'datv'})[0].capitalize()
                self.data["post"] = morph.parse(row[3])[0].inflect({'datv'})[0]
                self.data["adr"] = row[4]
                self.data["start_date"] = self.d_from.text()
                self.data["end_date"] = self.d_to.text()
                self.count_days = self.sb_days.value()
                # self.create_covid(self.data["family"].capitalize() + " " + self.data["name"][0].upper()
                #                   + "." + self.data["surname"][0].upper() + ".", self.data["post"].capitalize())
                return

    def check_input(self):
        return True

    def _create_data(self, doc):
        note = ["Настоящим письмом информируем Вас о прохождение вакцинации от Covid-19 сотрудником ООО «Вертикаль»"]
        fields = {"vac_1": ["№ п/п", "ФИО", "Должность", "Дата прививки", "Место вакцинации"],
                  "vac_2": ["№ п/п", "ФИО", "Должность", "Дата первой прививки",
                            "Дата второй прививки", "Место вакцинации"],
                  "anti": ["№ п/п", "ФИО", "Должность", "Номер сертификата", "Дата сертификата"]}
        data = {"number": "", "date": ""}
        data["number"] = get_next_number()
        data["date"] = str(dt.datetime.now().date())
        data["note"] = note[0]
        people_id = self.cb_worker.currentText().split(".")[0]
        people = []
        key = "vac"
        table = doc.add_table(rows=2, cols=5)
        for i in range(len(fields[key])):
            cell = table.cell(0, i)
            cell.text = fields[key][i]
            cell = table.cell(1, i)
            cell.text = people[i]
        # записываем в ячейку данные
        for row in self.parent.db.get_data("family, name, surname, post, id", "itrs"):
            if people_id == str(row[-1]):
                pass
        path = get_path("path_vac")
        try:
            doc = docxtpl.DocxTemplate(path)
        except:
            mes.question(self, "Сообщение", my_errors["4_not_file"] + self.main_file, mes.Cancel)
            return

        return True

    def _ev_ok(self):
        return True

    def all_days(self, state):
        self.sb_days.setEnabled(not state)
        self.sb_days.setValue(14)
        self.count_days = 14
        pass

    def create_covid(self, family, post):
        path = get_path("path") + get_path("path_covid") + "/covid.xlsx"
        try:
            wb = openpyxl.load_workbook(path)
        except:
            mes.question(self, "Сообщение", my_errors["4_not_find"] + path, mes.Cancel)
            return
        try:
            sheet = wb['unlock']
        except:
            mes.question(self, "Сообщение", my_errors["9_not_sheet"] + 'unlock', mes.Cancel)
            return
        for i in range(self.count_days):
            sheet['A' + str(i + 3)].value = i + 1
            sheet['B' + str(i + 3)].value = dt.datetime.now().date() - dt.timedelta(self.count_days - i)
            sheet['C' + str(i + 3)].value = family
            sheet['D' + str(i + 3)].value = post
        try:
            wb.save(get_path("path") + get_path("path_covid") + "/" + str(family) + ".xlsx")
            os.startfile(get_path("path") + get_path("path_covid") + "/" + str(family) + ".xlsx")
        except:
            mes.question(self, "Сообщение", my_errors["4_not_file"], mes.Cancel)
            return

    def create_vac(self):

        pass
