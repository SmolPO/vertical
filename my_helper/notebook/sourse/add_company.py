from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class AddCompany(QMainWindow):
    def __init__(self):
        super(AddCompany, self).__init__()
        uic.loadUi('../designer_ui/new_company.ui', self)
        # pass
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)

    def ev_OK(self):
        print("OK")

    def ev_cancel(self):
        print("cancel")



