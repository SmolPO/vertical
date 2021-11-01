from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate as Date
from PyQt5.QtWidgets import QMessageBox as mes
import datetime as dt
from configparser import ConfigParser
from my_helper.notebook.sourse.my_pass.pass_template import TempPass
from my_helper.notebook.sourse.create.new_template import from_str
from my_helper.notebook.sourse.database import get_path, get_path_ui, count_days
import logging
import docx
#  logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("pass_month")


class MonthPass(TempPass):
    def __init__(self, parent):
        super(MonthPass, self).__init__(designer_file, parent, "workers")
        if not self.status_:
            return
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.my_open_file)
        self.count_people = 0
        self.d_from.setDate(dt.datetime.now().date())
        self.d_to.setDate(Date(*from_str(".".join([str(count_days[dt.datetime.now().month - 1]),
                                                   str(dt.datetime.now().month),
                                                   str(dt.datetime.now().year)]))))
        self.cb_all.stateChanged.connect(self.set_enabled_workers)
        self.cb_manual_set.stateChanged.connect(self.set_dates)

        self.list_ui = (self.worker_1, self.worker_2, self.worker_3, self.worker_4, self.worker_5, self.worker_6,
                        self.worker_7, self.worker_8, self.worker_9, self.worker_10)
        self.data = {"customer": "", "company": "", "start_date": "", "end_date": "", "number": "", "date": ""}
        self.init_workers()
        self.init_cb_month()
        self.set_dates(self.cb_manual_set.isChecked())
        self.main_file += "/pass_month.docx"

    # инициализация
    def init_cb_month(self):
        month = dt.datetime.now().month - 1
        for elem in self.list_month[month:]:
            self.cb_month.addItem(elem)

    def init_workers(self):
        for item in self.list_ui:
            item.addItem("(нет)")
            item.activated[str].connect(self.new_worker)
            item.setEnabled(False)
        self.list_ui[0].setEnabled(True)
        for name in self.parent.db.get_data("family, name, surname, post, passport, "
                                            "passport_got, birthday, adr,  live_adr", "workers"):
            family = name[0] + " " + ".".join([name[1][0], name[2][0]]) + "."
            for item in self.list_ui:
                item.addItem(family)

    # флаг на выбор всех
    def set_enabled_workers(self, state):
        for elem in self.list_ui:
            elem.setEnabled(state != Qt.Checked)
        if state != Qt.Checked:
            self.new_worker()

    # получить данные
    # для заполнения текста
    def _get_data(self):
        if self.cb_manual_set.isChecked():
            self.data["start_date"] = self.d_from.text()
            self.data["end_date"] = self.d_to.text()
            return
        next_month = self.list_month.index(self.cb_month.currentText()) + 1
        # если конец года: увеличить год и месяц в 1
        if next_month == 13:
            config = ConfigParser()
            config.read('config.ini')
            self.new_year__week = config.get('config', 'new_year')
            next_day =  self.new_year__week
            next_month = "01"  # MessageBox для ввода первого дня
            next_year = str(dt.datetime.now().year + 1)
        else:
            next_day = "01"
            next_month = str(next_month)
            if int(next_month) < 10:
                next_month = "0" + next_month
            next_year = str(dt.datetime.now().year)
        if int(next_year) / 4 == 0:
            end_next_month = str(count_days[12])
        else:
            end_next_month = str(count_days[int(next_month)])
        self.data["start_date"] = ".".join((next_day, next_month, next_year))
        self.data["end_date"] = ".".join((end_next_month, next_month, next_year))
     
    # обработчики кнопок
    def _create_data(self, path):
        # Заполнить таблицу
        workers = []
        if self.cb_all.isChecked():
            workers = self.get_worker("all")
        else:
            for elem in self.list_ui:
                if elem.currentText() != "(нет)":
                    workers.append(self.get_worker(elem.currentText()))
        i = 1
        doc = docx.Document(path)
        for people in workers:
            doc.tables[1].add_row()
            doc.tables[1].rows[i].cells[0].text = str(i)
            doc.tables[1].rows[i].cells[1].text = " ".join(people[0:3])
            doc.tables[1].rows[i].cells[2].text = people[3]
            doc.tables[1].rows[i].cells[3].text = people[6]
            doc.tables[1].rows[i].cells[4].text = " ".join(people[4:6])
            doc.tables[1].rows[i].cells[5].text = people[7]
            doc.tables[1].rows[i].cells[6].text = people[8]
            i += 1
        doc.save(path)

    def check_input(self):
        if self.list_ui[0].currentText() == "(нет)":
            mes.question(self, "Сообщение", "Укажите сотрудников", mes.Cancel)
            return False
        return True

    def _ev_ok(self):
        return True