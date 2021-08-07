from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
import inserts
import datetime as dt
import xml.etree.ElementTree as ET
#  сделать неактивными кнопки до заполнения всех полей, сделать галку для отключения это фичи в настройках
#  сделать мессаджбоксы на Сохранить


class WeekPass(QDialog):
    def __init__(self, parent):
        super(WeekPass, self).__init__()
        uic.loadUi('../designer_ui/week_work.ui', self)
        # pass
        self.parent = parent
        self.list_workers = []
        self.table = "contract"
        self.b_ok.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)
        self.b_save.clicked.connect(self.save_pattern)
        self.b_kill.clicked.connect(self.kill_pattern)
        self.b_open.clicked.connect(self.open_file)

        self.cb_other.stateChanged.connect(self.other_days)
        self.cb_sun.stateChanged.connect(self.week_days)
        self.cb_sub.stateChanged.connect(self.week_days)
        self.d_from.enabled = False
        self.d_to.enabled = False
        self.cb_sun.enabled = True
        self.cb_sub.enabled = True

        self.d_note.setDate(dt.datetime.now().date())
        self.number.setValue(self.parent.get_next_number())

        self.get_my_object()
        self.get_who()
        self.get_workers()
        #  self.get_example()

    def other_days(self, state):
        if state == Qt.Checked:
            self.d_from.enabled = True
            self.d_to.enabled = True
            self.cb_sun.enabled = False
            self.cb_sub.enabled = False
        else:
            self.d_from.enabled = False
            self.d_to.enabled = False
            self.cb_sun.enabled = True
            self.cb_sub.enabled = True

    def week_days(self, state):
        if state == Qt.Checked:
            self.cb_other.enabled = False
        elif not self.cb_sun.is_Checked() and not \
                self.cb_sub.is_Checked():
            self.cb_other.enabled = True

    def get_my_object(self):
        objects = self.parent.database_cur.execute(inserts.get_names_objects())
        self.cb_object.addItem("(нет)")
        for name in objects:
            self.cb_object.addItem(name)

    def get_who(self):
        who = self.parent.database_cur.execute(inserts.get_bosses())
        self.cb_who.addItem("(нет)")
        for post in who:
            self.cb_who.addItem(post)

    def get_workers(self):
        workers = self.parent.database_cur.execute(inserts.get_workers("Ф И.О."))
        for item in self.list_workers:
            item.addItem("(нет)")
        for name in workers:
            for item in self.list_workers:
                item.addItem(name)

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

    def ev_OK(self):
        self.parent.get_new_week_pass(self.get_data())
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

    def kill_pattern(self):

        pass

    def get_data(self):
        days = self.get_days()
        date = self.d_note.text()
        number = self.number.text()
        who = self.cb_who.text()
        name_ob = self.cb_object.text()
        workers = self.get_list()
        return list([number, date, who, name_ob, days, workers])

    def get_list(self):
        workers = []
        for item in self.list_workers.items():
            if not item.text():
                continue
            else:
                workers.append(item.text())
        return workers

    def get_days(self):
        data = []
        now_weeday = dt.datetime.now().weekday()
        if self.cb_other.is_checked:
            data.append([self.d_from.text(), self.d_to.text()])
            return data
        if self.cb_sun.is_checked:
            sub_day = dt.datetime.now() + dt.timedelta(5 - now_weeday)
            data.append(sub_day)
        if self.cb_sub.is_checked:
            sun_day = dt.datetime.now() + dt.timedelta(6 - now_weeday)
            data.append(sun_day)
        return data

    def open_file(self):
        print("open file")
        pass

