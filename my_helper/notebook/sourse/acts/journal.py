from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import docxtpl
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.database import get_path_ui
designer_file = get_path_ui("journal")


class Journal(QDialog):
    def __init__(self, parent):
        super(Journal, self).__init__()
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.b_print.clicked.connect(self.ev_print)
        self.count_p2 = 0
        self.count_p5 = 0
        self.path = ""
        self.data = dict()
        self.init_bosses()

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
        data["boss_1_post"] = self.get_post(self.boss_1.currentText().split(".")[0], "itrs")
        data["boss_2_post"] = self.get_post(self.boss_2.currentText().split(".")[0], "itrs")
        data["boss_3_post"] = self.get_post(self.boss_3.currentText().split(".")[0], "bosses")
        data["boss_4_post"] = self.get_post(self.boss_4.currentText().split(".")[0], "bosses")
        data["date"] = self.date.text()
        self.count_p2 = self.sb_p2.value()
        self.count_p5 = self.sb_p5.value()
        return data

    def get_post(self, my_id, table):
        rows = self.parent.parent.db.get_data("*", table)
        for item in rows:
            if item[-1] == my_id:
                print(item)
                return item[4]
        return "."

    def ev_print(self):
        self.data = self.get_data()
        if not self.check_input():
            return False
        try:
            doc = docxtpl.DocxTemplate(self.path)
            doc.render(self.data)
            path = self.path
            doc.save(path)
        except:
            pass
        self.close()

    def check_input(self):
        if self.number.value() == 0:
            mes.question(self, "Сообщение", "Укажите номер журнала", mes.Ok)
            return False
        if self.sb_p2.value() == 0:
            mes.question(self, "Сообщение", "Укажите кол-во страниц раздела 2", mes.Ok)
            return False
        if self.sb_p5.value() == 0:
            mes.question(self, "Сообщение", "Укажите кол-во страниц раздела 5", mes.Ok)
            return False
        if self.date.text() == "01.01.2000":
            mes.question(self, "Сообщение", "Укажите дату начала работ", mes.Ok)
            return False
        if self.boss_1.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите первого босса", mes.Ok)
            return False
        if self.boss_2.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите второго босса", mes.Ok)
            return False
        if self.boss_3.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите третьего босса", mes.Ok)
            return False
        if self.boss_4.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите четвертого босса", mes.Ok)
            return False
        if self.name.toPlainText() == "" or len(self.name.toPlainText()) < 3:
            mes.question(self, "Сообщение", "Укажите название журнала", mes.Ok)
            return False
        return True