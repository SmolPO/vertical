from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
import docx
import os
import logging
import openpyxl
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
        self.d_to.setDate(from_str(".".join([str(count_days[dt.datetime.now().month - 1]),
                                             str(dt.datetime.now().month),
                                             str(dt.datetime.now().year)])))
        self.cb_all_days.stateChanged.connect(self.all_days)
        try:
            self.rows_from_db = self.parent.db.get_data("*", self.table)
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.init_workers()
        self.data = {"number": "", "data": "", "customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": ""}
        self.vac_path = self.main_file + "/Вакцинация.docx"
        self.main_file += "/Разблокировка.docx"
        self.count_days = 14

    def init_workers(self):
        for people in self.all_people:
            if people[-2] != 3:
                self.cb_worker.addItem(str(people[-1]) + ". " + short_name(people))

    def _get_data(self):
        family = self.cb_worker.currentText()
        morph = pymorphy2.MorphAnalyzer()
        people = self.check_row(family)  # на форме фамилия в виде Фамилия И.
        self.data["family"] = morph.parse(people[0])[0].inflect({'datv'})[0].capitalize()
        self.data["name"] = morph.parse(people[1])[0].inflect({'datv'})[0].capitalize()
        self.data["surname"] = morph.parse(people[2])[0].inflect({'datv'})[0].capitalize()
        self.data["post"] = morph.parse(people[3])[0].inflect({'datv'})[0]
        self.data["adr"] = people[8]
        self.data["start_date"] = self.d_from.text()
        self.data["end_date"] = self.d_to.text()
        self.count_days = self.sb_days.value()


    def check_input(self):
        return True

    def _ev_ok(self):
        return True

    def all_days(self, state):
        self.sb_days.setEnabled(not state)
        self.sb_days.setValue(14)
        self.count_days = 14
        pass

    def _create_data(self, _):
        family = self.cb_worker.currentText()
        self.create_vac(family)
        pass

    def create_vac(self, family):
        note = ["Настоящим письмом информируем Вас о прохождение вакцинации от Covid-19 сотрудником ООО «Вертикаль»"]
        people = self.check_row(family)
        data_vac = people[-5:-1]
        doc = docx.Document(self.vac_path)
        next_id = set_next_number(int(self.number.value()) + 1)
        doc.tables[0].rows[0].cells[0].text = "Исх. " + str(next_id)
        doc.tables[0].rows[1].cells[0].text = "от " + self.d_note.text()
        doc.tables[1].rows[1].cells[0].text = "1"
        doc.tables[1].rows[1].cells[1].text = " ".join(people[:3])
        doc.tables[1].rows[1].cells[2].text = people[3]
        if data_vac[3][:2] == "S5":
            doc.tables[1].add_column(200)
            doc.tables[1].rows[0].cells[3].text = "Дата первой прививки"
            doc.tables[1].rows[0].cells[4].text = "Дата второй прививки"
            doc.tables[1].rows[0].cells[5].text = "Место вакцинации"

            doc.tables[1].rows[1].cells[3].text = data_vac[0]
            doc.tables[1].rows[1].cells[4].text = data_vac[1]
            doc.tables[1].rows[1].cells[5].text = data_vac[2]
            pass
        elif data_vac[3][:2] == "SL":
            self.data["d_vac_1"] = data_vac[0]
            self.data["place"] = data_vac[2]
            doc.tables[1].rows[0].cells[3].text = "Дата прививки"
            doc.tables[1].rows[0].cells[4].text = "Место вакцинации"
            doc.tables[1].rows[1].cells[3].text = data_vac[0]
            doc.tables[1].rows[1].cells[4].text = data_vac[2]
        elif data_vac[3][:2] == "CV":
            self.data["d_vac_1"] = data_vac[0]
            self.data["vac_doc"] = data_vac[3][2:]
            doc.tables[1].rows[0].cells[3].text = "Номер сертификата"
            doc.tables[1].rows[0].cells[4].text = "Дата получения"

            doc.tables[1].rows[1].cells[3].text = data_vac[0]
            doc.tables[1].rows[1].cells[4].text = data_vac[3]
            pass
        path = get_path("path") + get_path("path_notes_docs") + "/" + str(next_id) + "_" + self.d_note.text() + ".docx"
        doc.save(path)
        os.startfile(path)
        pass
