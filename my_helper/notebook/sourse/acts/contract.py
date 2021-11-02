from PyQt5 import uic
import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtWidgets import QMessageBox as mes
from my_helper.notebook.sourse.database import get_path_ui, my_errors, get_path
designer_file = get_path_ui("contract")


class Contract(QDialog):
    def __init__(self, parent):
        super(Contract, self).__init__()
        if not self.check_start():
            return
        self.parent = parent
        self.b_contract.clicked.connect(self.ev_open)
        self.b_def.clicked.connect(self.ev_open)
        self.b_ekr.clicked.connect(self.ev_open)
        self.b_exit.clicked.connect(self.close)
        # self.b_scaner.clicked.connect(self.ev_scaner)
        self.path = parent.path + get_path("path_docs")

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

    def ev_open(self):
        print(self.path)
        print(os.listdir(self.path), self.sender().text() + ".pdf")
        if self.sender().text() + ".pdf" in os.listdir(self.path):
            try:
                path = self.path + "/" + self.sender().text() + ".pdf"
                print(path)
                os.startfile(path)
            except:
                mes.question(self, "Внимание", my_errors["4_not_file"], mes.Cancel)
                return
        else:
            mes.question(self, "Внимание", "Нет файла", mes.Cancel)
            return
