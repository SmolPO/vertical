from PyQt5 import uic
import os
from PyQt5.QtWidgets import QDialog
from my_helper.notebook.sourse.database import *


class Contract(QDialog):
    def __init__(self, parent):
        super(Contract, self).__init__()
        self.conf = Ini(self)
        self.ui_file = self.conf.get_path_ui("contract")
        if not self.check_start():
            return
        self.parent = parent

        self.b_contract.clicked.connect(self.ev_open)
        self.b_def.clicked.connect(self.ev_open)
        self.b_ekr.clicked.connect(self.ev_open)
        self.b_exit.clicked.connect(self.close)
        # self.b_scaner.clicked.connect(self.ev_scaner)
        self.path = parent.path + self.conf.get_path("path_docs")

    def check_start(self):
        self.status_ = True
        try:
            uic.loadUi(self.ui_file, self)
            return True
        except:
            mes.question(self, "Сообщение", "Не удалось открыть форму " + self.ui_file, mes.Cancel)
            self.status_ = False
            return False

    def ev_open(self):
        if self.sender().text() + ".pdf" in os.listdir(self.path):
            try:
                path = self.path + "/" + self.sender().text() + ".pdf"
                os.startfile(path)
            except:
                msg_er(self, GET_FILE)
                return
        else:
            msg_er(self, GET_FILE)
            return
