from PyQt5 import uic
import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from my_helper.notebook.sourse.database import get_path_ui
designer_file = get_path_ui("contract")


class Contract(QDialog):
    def __init__(self, parent):
        super(Contract, self).__init__()
        self.parent = parent
        uic.loadUi(designer_file)
        self.b_contract.clicked.connect(self.ev_open)
        self.b_def.clicked.connect(self.ev_open)
        self.b_ekr.clicked.connect(self.ev_open)
        # self.b_scaner.clicked.connect(self.ev_scaner)
        self.path = ""

    def ev_open(self):
        os.startfile(self.path + "/" + self.sender().text() + ".docx")

