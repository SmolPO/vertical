from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
import os
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.acts.journal import Journal
from my_helper.notebook.sourse.acts.asr import Asr
from my_helper.notebook.sourse.acts.contract import Contract
from my_helper.notebook.sourse.acts.report import CreateReport
from my_helper.notebook.sourse.database import get_path, get_path_ui, my_errors
designer_file = get_path_ui("acts")


class Acts(QDialog):
    def __init__(self, parent):
        super(Acts, self).__init__()
        if not self.check_start():
            return
        self.parent = parent
        uic.loadUi(designer_file, self)
        self.b_save.clicked.connect(self.ev_save)
        self.b_asr.clicked.connect(self.ev_start)
        self.b_add.clicked.connect(self.ev_add)
        self.b_latter.clicked.connect(self.ev_latter)
        self.b_month.clicked.connect(self.ev_month)
        self.b_create.clicked.connect(self.ev_xlsx)
        self.b_exit.clicked.connect(self.ev_exit)
        self.cb_select.activated[str].connect(self.ev_select)
        self.path = get_path("path") + get_path("path_contracts")
        self.contract = ""
        self.init_contracts()

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

    def init_contracts(self):
        rows = self.parent.db.get_data("id, number", "contracts")
        for item in rows:
            self.cb_select.addItem(". ".join(item))

    def ev_start(self):
        if self.cb_select.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Сначала выберите договор", mes.Cancel)
            return False
        menu = {self.b_asr.text(): Asr}
        name = self.sender().text()
        self.path = self.path + "/" + "".join(self.cb_select.currentText().split(". ")[1:])
        wnd = menu[name](self)
        if not wnd.status_:
            mes.question(self, "Сообщение", "Не найден файл дизайна " + wnd._path, mes.Cancel)
            return
        wnd.setFixedSize(wnd.geometry().width(), wnd.geometry().height())
        wnd.exec_()
        return

    def ev_save(self):
        """"
        архивировать папку
        переместить куда то
        """
        pass

    def ev_add(self):
        if self.cb_select.currentText() == "(нет)":
            mes.question(self, "Сообщение", "Сначала выберите договор", mes.Cancel)
            return False
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         get_path("path") + get_path("path_scan"),
                                                         "*.*(*.*)")
        if not self.filename:
            return
        tmp = self.filename.split(".")[-1]
        path_save = self.path + "/" + "".join(self.cb_select.currentText().split(". ")[1:]) + get_path("others")
        name, ok = QInputDialog.getText(self, "Введите имя файла", "Имя (без расширения)")
        if ok:
            try:
                path_save = path_save + "/" + name + "." + tmp
                os.replace(self.filename, path_save)
                mes.question(self, "Сообщение", "Файл добавлен", mes.Ok)
            except:
                mes.question(self, "Сообщение", my_errors["4_not_file"] + path_save, mes.Cancel)
                return
        pass

    def ev_latter(self):
        try:
            path_from = get_path("path") + get_path("path_pat_patterns") + "/Бланк.doc"
            path_to = get_path("path") + "/Исходящие/Письма/Письмо.doc"
            os.replace(path_from, path_to)
            os.startfile(path_to)
        except:
            mes.question(self, "Сообщение", "Файл " + path_from + " не найден", mes.Ok)
            return False
        pass

    def ev_month(self):
        os.startfile(self.path)
        pass

    def ev_xlsx(self):
        wnd = CreateReport(self)
        wnd.exec_()
        os.startfile(self.path)
        pass

    def ev_exit(self):
        self.close()

    def ev_select(self):
        if self.cb_select.currentText() != "(нет)":
            self.contract = self.cb_select.currentText().split(".")[1]
        pass
