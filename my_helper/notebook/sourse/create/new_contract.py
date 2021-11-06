from PyQt5.QtCore import QDate as Date
from PyQt5.QtCore import QRegExp as QRE
from PyQt5.QtGui import QRegExpValidator as QREVal
from PyQt5.QtWidgets import QMessageBox as mes
import os
import PyPDF2
from my_helper.notebook.sourse.create.new_template import TempForm
from my_helper.notebook.sourse.database import *

# logging.basicConfig(filename=get_path("path") + "/log_file.log", level=logging.INFO)
designer_file = get_path_ui("new_contract")
fields = ["name", "customer", "number", "date", "object", "type_work", "place", "id"]
statues_cntr = ["Начат", "Заершен"]
_zero = "01.01.2000"


class NewContact(TempForm):
    def __init__(self, parent=None):
        super(NewContact, self).__init__(designer_file, parent, "contracts")
        if not self.status_:
            return
        self.init_mask()
        try:
            self.parent.db.init_list(self.cb_select, "name, id", self.table)
        except:
            msg(self, my_errors["3_get_db"])
            return
        self.list_ui = [self.name, self.cb_comp, self.part, self.number, self.date, self.my_object, self.work]

        self.slice_set = 0
        self.slice_get = 0
        self.slice_clean = 0
        self.slice_select = len(self.list_ui)
        self.current_id = self.next_id
        self.cb_comp.addItem(self.parent.customer)

    def init_mask(self):
        symbols = QREVal(QRE("[а-яА-Я ]{30}"))
        self.name.setValidator(symbols)
        self.number.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.part.setValidator(QREVal(QRE("[а-яА-Яa-zA-Z /_-., 0-9]{1000}")))
        self.price.setValidator(QREVal(QRE("[,0-9]{1000}")))

    def _ev_select(self, text):
        self.slice_select = len(text)
        return True

    def _clean_data(self):
        list_ui = [self.name, self.part, self.number]
        for item in list_ui:
            item.setText("")
        self.cb_comp.setCurrentIndex(0)
        self.date.setDate(zero)
        self.my_object.clear()
        self.work.clear()
        self.date_end.setDate(zero)
        self.price.setText("")
        self.NDS.setChecked(True)
        self.avans.setValue(0)

    def _set_data(self, data):
        """
        "(name, customer, number, date, object, type_work, place, "
                        "price, date_end, nds, avans, status, id)"
        :param data:
        :return:
        """
        self.my_object.clear()
        self.work.clear()
        self.name.setText(data[0])
        g = iter(range(len(self.rows_from_db) + 1))
        for item in self.rows_from_db:
            next(g)
            if data[-1] == item[-1]:
                self.cb_comp.setCurrentIndex(next(g))
                break
        self.number.setText(data[2])
        self.date.setDate(from_str(data[3]))
        self.my_object.append(data[4])
        self.work.append(data[5])
        self.part.setText(data[6])
        self.price.setText(data[7])
        self.date_end.setDate(from_str(data[8]))
        self.NDS.setChecked(True) if data[9] == "да" else self.NDS.setChecked(False)
        self.avans.setValue(int(data[10]))
        self.status.setCurrentIndex(statues_cntr.index(data[-2]))
        self.current_id = data[-1]

    def _get_data(self, data):
        data.append(self.name.text())
        data.append(self.cb_comp.currentText())
        data.append(self.number.text())
        data.append(self.date.text())
        data.append(self.my_object.toPlainText())
        data.append(self.work.toPlainText())
        data.append(self.part.text())
        data.append(self.price.text())
        data.append(self.date_end.text())
        data.append("да" if self.NDS.isChecked() else "нет")
        data.append(str(self.avans.value()))
        data.append(self.status.currentText())
        self.create_docs()
        return data

    def create_docs(self):
        path = get_path("path") + get_path("path_contracts") + "/" + str(self.number.text())
        folders = ["", "/документы", "/документы/ППР", "/документы/Договор", "/документы/Приложение"]
        for item in folders:
            os.mkdir(path + item)
        pdf_merger = PyPDF2.PdfFileMerger()
        folder = get_path("path") + get_path("path_scan")
        answer = mes.question(self, "Добавление Договора", "Отсканируйте ЕКР в PDF по порядку и затем нажмите ОК. "
                                                           "Программа сохранит его в папку", mes.Ok | mes.Cancel)
        if answer == mes.Ok:
            answer = mes.question(self, "Добавление Договора", "Вы точно отсканировали?", mes.Ok | mes.Cancel)
            if answer == mes.Ok:
                files = os.listdir(folder)
                path_to = path + "/документы/Договор/ЕКР.pdf"
                for doc in files:
                    if ".pdf" in doc:
                        pdf_merger.append(str(folder + "/" + doc))
                pdf_merger.write(path_to)
                os.remove()



        pass

    def check_input(self):
        if "" in list([self.name.text(), self.number.text(),
                       self.my_object.toPlainText(), self.work.toPlainText(),
                      self.part.text(), self.price.text(), self.date_end.text()]) or self.date.text() == _zero:
            return msg(self, "Заполните все поля")
        return True

    def _ev_ok(self):
        return True

    def _but_status(self, status):
        return True