from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class NewBoss(QMainWindow):
    def __init__(self):
        super(NewBoss, self).__init__()
        uic.loadUi('../designer_ui/settings.ui', self)
        # pass
        self.b_OK.clicked.connect(self.ev_OK)
        self.b_cancel.clicked.connect(self.ev_cancel)

    def ev_OK(self):
        print("OK")

    def ev_cancel(self):
        print("cancel")
