from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
import os
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.acts.journal import Journal
from my_helper.notebook.sourse.acts.asr import Asr
from my_helper.notebook.sourse.acts.contract import Contract
from my_helper.notebook.sourse.database import get_path, get_path_ui
designer_file = get_path_ui("acts")


class Acts(QDialog):
    def __init__(self, parent):
        super(Acts, self).__init__()
        self.parent = parent
        uic.loadUi(designer_file, self)
        self.b_journal.clicked.connect(self.ev_start)
        self.b_save.clicked.connect(self.ev_save)
        self.b_asr.clicked.connect(self.ev_start)
        self.b_add.clicked.connect(self.ev_add)
        self.b_contract.clicked.connect(self.ev_start)
        self.b_latter.clicked.connect(self.ev_latter)
        self.b_month.clicked.connect(self.ev_month)
        self.b_xlxs.clicked.connect(self.ev_xlsx)
        self.b_exit.clicked.connect(self.ev_exit)
        self.cb_select.activated[str].connect(self.ev_select)
        self.path = get_path("path") + get_path("contracts")
        self.contract = ""
        self.init_contracts()

    def init_contracts(self):
        rows = self.parent.db.get_data("id, number", "contracts")
        for item in rows:
            self.cb_select.addItem(". ".join(item))

    def ev_start(self):
        name = self.sender().text()
        if name == self.b_journal.text():
            wnd = Journal(self)
            wnd.exec_()
        elif name == self.b_asr.text():
            wnd = Asr(self, self.contract)
            wnd.exec_()
        elif name == self.b_contract.text():
            wnd = Contract(self)
            wnd.exec_()
        return

    def ev_save(self):
        """"
        архивировать папку
        переместить куда то
        """
        pass

    def ev_add(self):
        self.filename, tmp = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         get_path("path"),
                                                         "PDF Files(*.pdf)")
        os.replace(self.filename, self.filename)
        pass

    def ev_latter(self):
        try:
            path_from = get_path("path") + get_path("path_pat_patterns") + "/blank.doc"
            path_to = self.path + "Письма/Письмо.doc"
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
        os.startfile(self.path)
        pass

    def ev_exit(self):
        self.close()

    def ev_select(self):
        self.contract = self.cb_select.currentText().split(".")[1]
        pass
