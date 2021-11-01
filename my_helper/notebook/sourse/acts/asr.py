from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.database import get_path_ui, get_path, get_config
import docxtpl
import os
import datetime as dt
import pymorphy2

designer_file = get_path_ui("asr")
si = ["тн", "т", "кг", "м2", "м", "м/п", "мм", "м3", "л", "мм", "шт"]


class Asr(QDialog):
    def __init__(self, parent, contract):
        super(Asr, self).__init__()
        if not self.check_start():
            return
        self.parent = parent
        self.year.setCurrentIndex(dt.datetime.now().year-2021)
        self.b_print.clicked.connect(self.ev_print)
        self.b_change.clicked.connect(self.ev_change)
        self.b_kill.clicked.connect(self.ev_kill)
        self.b_close.clicked.connect(self.ev_close)
        self.cb_select.activated[str].connect(self.ev_select)
        self.numbers.textChanged.connect(self.change_count)
        self.init_bosses()
        self.init_SI()
        self.ind = 0
        self.path = get_path("path") + get_path("path_pat_patterns")
        self.my_id = 0
        self.contract = contract

    def check_start(self):
        self.status_ = True
        self.path_ = designer_file
        try:
            uic.loadUi(designer_file, self)
            return True
        except:
            mes.question(self, "Сообщение", "Не удалось открыть форму " + designer_file, mes.Cancel)
            self.status_ = False
            return False

    def change_count(self):
        print(len(self.numbers.toPlainText().split(",")))
        self.count.setValue(len(self.numbers.toPlainText().split(",")))

    def init_bosses(self):
        self.parent.parent.db.init_list(self.boss_1, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_2, "id, family, name, surname", "itrs", people=True)
        self.parent.parent.db.init_list(self.boss_3, "id, family, name, surname", "bosses", people=True)
        self.parent.parent.db.init_list(self.boss_4, "id, family, name, surname", "bosses", people=True)
        pass

    def init_SI(self):
        for item in si:
            self.cb_SI.addItem(item)

    def create_data(self, day_start, day_end, number):
        if len(day_end) == 1:
            day_end = "0" + day_end
        if len(day_start) == 1:
            day_start = "0" + day_start
        morph = pymorphy2.MorphAnalyzer()
        data = dict()
        bosses = [self.boss_1, self.boss_2, self.boss_3, self.boss_4]
        tables = ["itrs", "itrs", "bosses", "bosses"]
        for ind in range(1, 5):
            boss = bosses[ind-1].currentText()
            post = self.get_post(boss.split(".")[0], tables[ind-1])
            family = boss[boss.index(".")+2:]
            val = post + "__" + family + "_"*(100-len(post + "__" + family))
            data["boss_" + str(ind)] = val
        val = "_______" if self.sb_value.value() == 0 else "__" + str(self.sb_value.value()) + "__"
        data["work"] = self.work.toPlainText() + val + self.cb_SI.currentText()
        print(data["work"])
        materials = self.material.currentText() if self.material.currentText() != "(нет)" else "_"*40
        data["material"] = materials
        data["next_work"] = self.next_work.toPlainText()
        data["day_end"] = day_end
        data["day_start"] = day_start
        data["month"] = morph.parse(self.month.currentText())[0].inflect({'gent'})[0].capitalize().lower()
        data["year"] = self.year.currentText()
        data["number"] = number
        data["company"] = get_config("company")
        return data

    def get_data(self):
        data = list()
        data.append(self.boss_1.currentText() + self.get_post(self.boss_1.currentText().split(".")[0], "itrs"))
        data.append(self.boss_2.currentText() + self.get_post(self.boss_2.currentText().split(".")[0], "itrs"))
        data.append(self.boss_3.currentText() + self.get_post(self.boss_3.currentText().split(".")[0], "bosses"))
        data.append(self.boss_4.currentText() + self.get_post(self.boss_4.currentText().split(".")[0], "bosses"))
        data.append(self.work.toPlainText() + "_" * 10 + self.cb_SI.currentText())
        data.append(self.material.currentText())
        data.append(self.next_work.text())
        return data

    def get_post(self, my_id, table):
        rows = self.parent.parent.db.get_data("*", table)
        for item in rows:
            if str(item[-1]) == my_id:
                print(item)
                return item[3]
        return "."

    def ev_print(self):
        if not self.check_input():
            return False
        ind = 1
        if self.days_start.toPlainText() == "":
            day_end = "______"
            day_start = "______"
        else:
            day_end = self.days_end.toPlainText().split(",")[ind]
            day_start = self.days_start.toPlainText().split(",")[ind]
        if self.numbers.toPlainText() == "":
            number = "______"
        else:
            number = self.numbers.toPlainText().split(",")[ind]
        self.data = self.create_data(day_start, day_end, number)
        path = self.path + "/asr.docx"
        try:
            doc = docxtpl.DocxTemplate(path)
        except:
            mes.question(self, "Сообщение", "Файл " + path + " не найден", mes.Ok)
            return False
        doc.render(self.data)
        path = get_path("path") + get_path("contract") + "/102021" + "/1.docx"
        doc.save(path)
        os.startfile(path)
        self.save_pattern()

    def save_pattern(self):
        data = list()
        data.append(self.data["work"])
        data.append(self.data["value"])
        data.append(self.data["si"])
        data.append(self.data["material"])
        data.append(self.data["day_start"])
        data.append(self.data["day_end"])
        data.append(self.data["month"])
        data.append(self.data["year"])
        data.append(self.data["boss_1"])
        data.append(self.data["boss_2"])
        data.append(self.data["boss_3"])
        data.append(self.data["boss_4"])
        return data

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

    def check_input(self):
        print(len(self.numbers.toPlainText().split(",")),
              len(self.days_start.toPlainText().split(",")),
              len(self.numbers.toPlainText().split(",")))
        if len(self.work.toPlainText()) < 3:
            mes.question(self, "Сообщение", "Укажите вид работ", mes.Ok)
            return False
        elif len(self.next_work.toPlainText()) < 3:
            mes.question(self, "Сообщение", "Укажите следующие работы", mes.Ok)
            return False
        elif self.cb_SI.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите единицы измерения", mes.Ok)
            return False
        elif self.month.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите месяц", mes.Ok)
            return False
        elif self.boss_1.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите первого босса", mes.Ok)
            return False
        elif self.boss_2.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите второго босса", mes.Ok)
            return False
        elif self.boss_3.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите третьего босса", mes.Ok)
            return False
        elif self.boss_4.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите четвертого босса", mes.Ok)
            return False
        elif self.count.value() == 0:
            mes.question(self, "Сообщение", "Укажите количество актов", mes.Ok)
            return False
        elif len(self.days_start.toPlainText().split(",")) != \
                len(self.days_end.toPlainText().split(",")):
            mes.question(self, "Сообщение", "Количесттво дней начала не совпадает с количеством дней окончания",
                         mes.Ok)
            return False

        elif self.numbers.toPlainText().split(",") != "" and \
             len(self.days_start.toPlainText().split(",")) != \
             len(self.numbers.toPlainText().split(",")):
            mes.question(self, "Сообщение",
                         "Не совпадает кол-во дней и кол-во номеров актов. Проверьте. Дней начала: " +
                         str(len(self.days_start.toPlainText().split(","))) + ", Номеров: " +
                         str(len(self.numbers.toPlainText().split(","))),
                         mes.Ok)
            return False
        elif self.days_start.toPlainText().split(",") != "" and \
             len(self.days_start.toPlainText().split(",")) != self.count.value():
            mes.question(self, "Сообщение", "Количество бланков не совпадает с количеством дат", mes.Ok)
            return False
        return True