from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import inserts
import datetime as dt
import xml.etree.ElementTree as ET
import docx
#  сделать мессаджбоксы на Сохранить


class MonthPass(QDialog):
    def __init__(self, parent):
        super(MonthPass, self).__init__()
        uic.loadUi('../designer_ui/pass_month.ui', self)
        # pass
        self.parent = parent
        self.workers = [self.worker_1, self.worker_2, self.worker_3,
                   self.worker_4, self.worker_5, self.worker_6,
                   self.worker_7, self.worker_8, self.worker_9]
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.my_open_file)

        self.cb_all.stateChanged.connect(self.week_days)

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())

        self.get_recipient()
        self.get_workers()
        #  self.get_example()

    def get_recipient(self):
        self.parent.database_cur.execute(inserts.get_bosses())
        rows = self.parent.database_cur.fetchall()
        self.cb_who.addItem("(нет)")
        for post in rows:
            self.cb_who.addItem(post[0])

    # шаблоны
    def get_example(self, ):
        root_node = ET.parse('sample.xml').getroot()
        for tag in root_node.findall('pattern/name'):
            name = tag.get("name")
            if name == "pattern":
                item_name = tag.get("object_name")
                item_who = tag.get("who")
                item_list = tag.get("list_workers")
                return item_name, item_who, item_list

    def zip_pattern(self, pattern):
        tree = ET.parse("xml_test.xml")
        glob_root = tree.getroot()
        new_pattern = ET.SubElement(glob_root, "pattern")
        patter_name = ET.SubElement(new_pattern, "name")
        patter_name.text = pattern["name"]

        item_name = ET.SubElement(new_pattern, "object_name")
        item_who = ET.SubElement(new_pattern, "who")
        item_list = ET.SubElement(new_pattern, "list_workers")
        item_name.text = pattern["object_name"]
        item_who.text = pattern["who"]
        for item in pattern["list_workers"]:
            el = ET.SubElement(item_list, "worker")
            el.text = item
        tree.write("xml_test.xml")

    def get_data(self):
        days = self.get_days()
        date = self.d_note.text()
        number = self.number.text()
        who = self.cb_who.currentText()
        name_ob = self.cb_object.text()
        workers = self.get_list()
        return list([number, date, who, name_ob, days, workers])

    # обработчики кнопок
    def ev_OK(self):
        doc = docx.Document("B:/my_helper/week.docx")
        # номер исх
        doc.tables[0].rows[0].cells[0].text = "Исх. № " + self.number.text()
        # дата
        doc.tables[0].rows[1].cells[0].text = "от. " + self.d_note.text()
        # Просим Ваc
        company = self.parent.company
        if self.cb_other.isChecked():
            data = "в выходные дни с " + self.d_from.text() + " до " + self.d_to.text()
        else:
            if len(self.get_days()) > 1:
                data = "в выходные дни с " + str(self.get_days()[0]) + " до " + str(self.get_days()[1])
            else:
                data = "в выходной день " + str(self.get_days()[0])
        doc.paragraphs[6].add_run(
            "Прошу Вас продлить электронный пропуск с {0} по {1} "
            "с рабочей сменой с 07-00 до 19-00 часов:".format(data[0], data[1]))
        # Заполнить таблицу
        list_ui = (self.worker_1, self.worker_2, self.worker_3, self.worker_4, self.worker_5, self.worker_6,
                   self.worker_7, self.worker_8, self.worker_9)
        for elem in list_ui:
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
        doc.save("B:/my_helper/to_print/month.docx")
        self.close()

    def ev_cancel(self):
        self.close()

    def save_pattern(self):
        data = {"who": self.cb_who.text(),
                "object_name": self.cb_object.text(),
                "workers": self.get_list()}
        self.zip_pattern(data)
        # запоковать в словарь
        # сохранить в файл

    def my_open_file(self):
        print("open file")
        pass

    def kill_pattern(self):
        pass

    def get_worker(self, family):
        # получить номер договора по короткому имени
        self.parent.database_cur.execute(inserts.pass_week())
        rows = self.parent.database_cur.fetchall()
        for row in rows:
            if family[:-4] == row[0]:
                return row
            return row

    # Заполнение служебки
    def create_note(self, data):
        doc = docx.Document("B:/my_helper/week.docx")
        pass




