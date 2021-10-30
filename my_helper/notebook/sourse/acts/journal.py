from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import docxtpl
from my_helper.notebook.sourse.database import get_path_ui
designer_file = get_path_ui("journal")


class Journal(QDialog):
    def __init__(self, parent):
        super(Journal, self).__init__()
        self.parent = parent
        self.b_print.clicked.connect(self.ev_print)
        self.count_p2 = 0
        self.count_p5 = 0
        self.path = ""
        self.data = dict()

    def init_bosses(self):
        self.parent.parent.db.init_list(self.boss_1, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_2, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_3, "id, family, name, surname", "bosses", people=True)
        self.parent.parent.db.init_list(self.boss_4, "id, family, name, surname", "bosses", people=True)
        pass

    def get_data(self):
        data = dict()
        data["name"] = self.name.toPlainText()
        data["number"] = self.number.value()
        data["boss_1"] = self.boss_1.currentText()
        data["boss_2"] = self.boss_2.currentText()
        data["boss_3"] = self.boss_3.currentText()
        data["boss_4"] = self.boss_4.currentText()
        data["date"] = self.date.text()
        self.count_p2 = self.sb_p2.value()
        self.count_p5 = self.sb_p5.value()
        return data

    def ev_print(self):
        self.data = self.get_data()
        if not self.check_input():
            return False
        doc = docxtpl.DocxTemplate(self.path)
        doc.render(self.data)
        path = self.path
        doc.save(path)

    def check_input(self):
        print(self.data)
        if "" in self.data or "0" in self.data:
            return False
        return True
