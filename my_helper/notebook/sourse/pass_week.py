from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import inserts
import datetime as dt
import xml.etree.ElementTree as ET
import docx
import docxtpl
#  сделать мессаджбоксы на Сохранить


class WeekPass(QDialog):
    def __init__(self, parent):
        super(WeekPass, self).__init__()
        uic.loadUi('../designer_ui/week_work.ui', self)
        # pass
        self.parent = parent
        self.workers = [self.worker_1, self.worker_2, self.worker_3,
                   self.worker_4, self.worker_5, self.worker_6,
                   self.worker_7, self.worker_8, self.worker_9]
        self.table = "contract"
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_other.stateChanged.connect(self.other_days)
        self.cb_sun.stateChanged.connect(self.week_days)
        self.cb_sub.stateChanged.connect(self.week_days)
        self.d_from.setEnabled(False)
        self.d_to.setEnabled(False)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())
        self.data = {"customer": "", "company": "", "start_date": "", "end_date": "",
                     "post": "", "family": "", "name": "", "surname": "", "adr": "",
                     "number": "", "data": "", "str_1": "", "str_2": "", "str_3": ""}
        self.list_ui = (self.worker_1, self.worker_2, self.worker_3, self.worker_4,
                        self.worker_5, self.worker_6, self.worker_7, self.worker_8, self.worker_9)
        self.init_object()
        self.init_recipient()
        self.init_workers()

    # выбор дня
    def other_days(self, state):
        if state == Qt.Checked:
            self.cb_sun.setEnabled(False)
            self.cb_sub.setEnabled(False)
            self.d_from.setEnabled(True)
            self.d_to.setEnabled(True)
        else:
            self.cb_sun.setEnabled(True)
            self.cb_sub.setEnabled(True)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)

    def week_days(self, state):
        if state == Qt.Checked:
            self.cb_other.setEnabled(False)
            self.d_from.setEnabled(False)
            self.d_to.setEnabled(False)
        elif not self.cb_sun.isChecked() and not self.cb_sub.isChecked():
            self.cb_other.setEnabled(True)

    # заполнение список
    def get_days(self):
        data = []
        now_weekday = dt.datetime.now().weekday()
        if self.cb_other.isChecked():
            data.append([self.d_from.text(), self.d_to.text()])
            return data
        if self.cb_sun.isChecked():
            sub_day = dt.datetime.now() + dt.timedelta(5 - now_weekday)
            data.append(sub_day)
        if self.cb_sub.isChecked():
            sun_day = dt.datetime.now() + dt.timedelta(6 - now_weekday)
            data.append(sun_day)
        return data

    def init_object(self):
        self.cb_object.addItem("(нет)")
        self.parent.database_cur.execute(inserts.get_names_objects())
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            self.cb_object.addItem(row[0])

    def init_recipient(self):
        self.parent.database_cur.execute(inserts.get_bosses())
        rows = self.parent.database_cur.fetchall()
        self.cb_who.addItem("(нет)")
        for post in rows:
            self.cb_who.addItem(post[0])

    def init_workers(self):
        self.parent.database_cur.execute(inserts.get_workers("Ф И.О."))
        rows = self.parent.database_cur.fetchall()
        for item in self.workers:
            item.addItem("(нет)")
        for name in rows:
            family = name[0] + " " + ".".join([name[1][0], name[2][0]]) + "."
            for item in self.workers:
                item.addItem(family)

    # обработчики кнопок
    def ev_OK(self):
        self.data["customer"] = self.parent.customer
        self.data["company"] = self.parent.company
        self.data["number"] = "Исх. № " + self.number.text()
        self.data["data"] = "от. " + self.d_note.text()

        # номер исх
        self.get_contract(self.cb_object.currentText())
        if self.cb_other.isChecked():
            self.data["week_day"] = "в выходные дни с " + self.d_from.text() + " до " + self.d_to.text()
        else:
            if len(self.get_days()) > 1:
                self.data["week_day"] = "в выходные дни с " + str(self.get_days()[0]) + " до " + str(self.get_days()[1])
            else:
                self.data["week_day"] = "в выходной день " + str(self.get_days()[0])
        doc = docxtpl.DocxTemplate("B:/my_helper/week_1.docx")
        doc.render(self.data)
        doc.save("B:/my_helper/to_print/week.docx")
        # Заполнить таблицу
        doc = docx.Document("B:/my_helper/week_1.docx")
        for elem in self.list_ui:
            family = elem.currentText()
            if family != "(нет)":
                doc.tables[1].add_row()
                people = self.get_worker(family)
                doc.tables[1].rows[1].cells[0].text = "1"
                doc.tables[1].rows[1].cells[1].text = " ".join(people[0:2])
                doc.tables[1].rows[1].cells[2].text = people[3]
                doc.tables[1].rows[1].cells[3].text = people[6]
                doc.tables[1].rows[1].cells[4].text = " ".join(people[4:6])
                doc.tables[1].rows[1].cells[5].text = people[7]
                doc.tables[1].rows[1].cells[6].text = people[8]
        doc.save("B:/my_helper/to_print/week.docx")
        self.close()

    def ev_cancel(self):
        self.close()

    def my_open_file(self):
        print("open file")
        pass

    def get_contract(self, name):
        # получить номер договора по короткому имени
        self.parent.database_cur.execute(inserts.get_contracts())
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if name in row:
                self.data["contract"] = row[0]
                self.data["object_name"] = row[1]
                self.data["part"] = row[2]
                self.data["type_work"] = row[3]

    def get_worker(self, family):
        # получить номер договора по короткому имени
        self.parent.database_cur.execute(inserts.pass_workers())
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if family[:-5] == row[0]:
                return row
            return row



