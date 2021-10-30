from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from my_helper.notebook.sourse.database import get_path_ui
import docxtpl
import os
from PyQt5.QtWidgets import QMessageBox as mes
designer_file = get_path_ui("asr")
si = ["тн", "т", "кг", "м2", "м", "м/п", "мм", "м3", "л", "мм", "шт"]


class Asr(QDialog):
    def __init__(self, parent):
        super(Asr, self).__init__()
        uic.loadUi(designer_file, self)
        self.parent = parent
        self.b_print.clicked.connect(self.ev_print)
        self.b_change.clicked.connect(self.ev_change)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_close.clicked.connect(self.ev_close)
        self.cb_select.activated[str].connect(self.ev_select)
        self.init_bosses()
        self.ind = 0
        self.path = ""
        self.my_id = 0

    def init_bosses(self):
        self.parent.parent.db.init_list(self.boss_1, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_2, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_3, "id, family, name, surname", "bosses", people=True)
        self.parent.parent.db.init_list(self.boss_4, "id, family, name, surname", "bosses", people=True)
        pass

    def create_data(self, day):
        data = dict()
        data["boss_1"] = self.boss_1.currentText() + self.get_post(self.boss_1.currentText().split(".")[0], "itrs")
        data["boss_2"] = self.boss_2.currentText() + self.get_post(self.boss_2.currentText().split(".")[0], "itrs")
        data["boss_3"] = self.boss_3.currentText() + self.get_post(self.boss_3.currentText().split(".")[0], "bosses")
        data["boss_4"] = self.boss_4.currentText() + self.get_post(self.boss_4.currentText().split(".")[0], "bosses")
        data["work"] = self.work.toPlainText() + "_" * 10 + self.cb_SI.currentText()
        data["material"] = self.material.text()
        data["next_work"] = self.next_work.text()
        data["date"] = day
        return data

    def get_data(self):
        data = list()
        data.append(self.boss_1.currentText() + self.get_post(self.boss_1.currentText().split(".")[0], "itrs"))
        data.append(self.boss_2.currentText() + self.get_post(self.boss_2.currentText().split(".")[0], "itrs"))
        data.append(self.boss_3.currentText() + self.get_post(self.boss_3.currentText().split(".")[0], "bosses"))
        data.append(self.boss_4.currentText() + self.get_post(self.boss_4.currentText().split(".")[0], "bosses"))
        data.append(self.work.toPlainText() + "_" * 10 + self.cb_SI.currentText())
        data.append(self.material.text())
        data.append(self.next_work.text())
        return data

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
            self.set_data(day)
            doc.render(self.data)
            path = self.path + "/" + day + ".docx"
            doc.save(path)
            os.startfile(path, "print")

    def ev_select(self):
        rows = self.parent.parent.db.get_data("*", "asrs")
        for row in rows:
            if self.cb_select.currentText().split(". ")[0] == row[-1]:
                print(row)
                self.work.clean()
                self.next_work.clean()
                self.work.append(row[0])
                self.material.setText(row[1])
                self.next_work.append(row[2])
                self.cb_SI.setCurrentIndex(si.index(row[3]))
                self.month.setCurrentIndex(row[4])
                self.days.clean()
                self.days.append(row[5])
                self.my_id = row[-1]
            pass

    def ev_change(self):
        answer = mes.question(self, "Изменение записи", "Вы действительно хотите изменить запись на " +
                              str(self.get_data()) + "?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            data = self.get_data()
            data.append(str(self.my_id))
            self.parent.db.my_update(data, self.table)
            answer = mes.question(self, "Сообщение", "Запись изменена", mes.Ok)
            if answer == mes.Ok:
                self.close()

    def ev_kill(self):
        answer = mes.question(self, "Удаление записи", "Вы действительно хотите удалить запись " +
                              str(self.get_data()) + "?", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            self.parent.db.kill_value(self.my_id, self.table)
            answer = mes.question(self, "Сообщение", "Запись удалена", mes.Ok)
            if answer == mes.Ok:
                self.close()

    def ev_close(self):
        self.close()