from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from my_helper.notebook.sourse.database import get_path_ui
import docxtpl
import os
designer_file = get_path_ui("asr")


class Asr(QDialog):
    def __init__(self, parent):
        super(Asr, self).__init__()
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.b_print.clicked.connect(self.ev_print)
        self.init_bosses()
        self.ind = 0
        self.path = ""

    def init_bosses(self):
        self.parent.parent.db.init_list(self.boss_1, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_2, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_3, "id, family, name, surname", "bosses", people=True)
        self.parent.parent.db.init_list(self.boss_4, "id, family, name, surname", "bosses", people=True)
        pass

    def get_data(self, day):
        data = dict()
        data["boss_1"] = self.boss_1.currentText() + self.get_post(self.boss_1.currentText().split(".")[0], "itrs")
        data["boss_2"] = self.boss_2.currentText() + self.get_post(self.boss_2.currentText().split(".")[0], "itrs")
        data["boss_3"] = self.boss_3.currentText() + self.get_post(self.boss_3.currentText().split(".")[0], "bosses")
        data["boss_4"] = self.boss_4.currentText() + self.get_post(self.boss_4.currentText().split(".")[0], "bosses")
        data["work"] = self.work.toPlainText() + "_" * 10 + self.cb_SI.currentText()
        data["material"] = self.material.text()
        data["next_work"] = self.next_work.text()
        data["date"] = day

    def get_post(self, my_id, table):
        rows = self.parent.parent.db.get_data("*", table)
        for item in rows:
            if item[-1] == my_id:
                print(item)
                return item[4]
        return "."

    def ev_print(self):
        for day in self.dates.toPlainText().split(", "):
            doc = docxtpl.DocxTemplate(self.path)
            self.get_data(day)
            doc.render(self.data)
            path = self.path + "/" + day + ".docx"
            doc.save(path)
            os.startfile(path, "print")
