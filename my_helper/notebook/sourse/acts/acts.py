from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
import os
from my_helper.notebook.sourse.database import get_path_ui
from my_helper.notebook.sourse.acts.journal import Journal
from my_helper.notebook.sourse.acts.asr import Asr
from my_helper.notebook.sourse.acts.contract import Contract
from my_helper.notebook.sourse.database import DataBase, get_path, get_path_ui
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
        self.path = "B:/my_helper/Исполнительные"
        self.contract = ""
        self.init_contracts()

    def init_contracts(self):
        rows = self.parent.db.get_data("id, number", "contracts")
        for item in rows:
            self.cb_select.addItem(". ".join(item))

    def ev_start(self):
        name = self.sender().text()
        if name == "Журнал":
            wnd = Journal(self)
            wnd.exec_()
        elif name == "АСР":
            wnd = Asr(self)
            wnd.exec_()
        elif name == "Договор":
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
                                                         "B:/my_helper/scan",
                                                         "PDF Files(*.pdf)")
        os.replace(self.filename, self.filename)
        pass

    def ev_latter(self):
        try:
            os.replace(get_path("path") + get_path("path_pat_patterns") + "/blank.doc",
                       self.path + "Письма/Письмо.doc")
            os.startfile(self.path + "Письма/Письмо.doc")
        except:
            print("Not found")
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
        pass
